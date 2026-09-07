#!/usr/bin/env python3
import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_BUILD = "4.81"
EXPECTED_SOURCE_HASH = "D6B0ADB94BB4EFB2829B33519550D349FABCB8C77251B6477E17489651F2089D"
EXPECTED_RUNTIME_MQ4_SHA = "5DE9FD783BB930CC0591612479FE9D9440C938C142D91CB3BA978A233A658D57"
EXPECTED_RUNTIME_EX4_SHA = "05733566540A2E5F0BA109BADA7EB17920DF5853201DAA5D9E8023E65C1912C0"
FORBIDDEN_RUNTIME_MARKERS = (
    "LEDGER_DISABLED", "OrderSend", "OrderClose", "OrderModify",
    "OrderDelete", "DEC_EXECUTED",
)
FROZEN_CP_FIELDS = (
    "BuildID", "SourceHash", "ConfigFingerprint", "DecisionID", "Pair",
    "Direction", "SignalType", "EntryTime", "EntryM5Open", "ExpiryTime",
    "EntryPrice", "StopLoss", "TakeProfit", "Digits",
)


def parse_args():
    p = argparse.ArgumentParser(description="Verify Build 4.81 C10 live physical-restart evidence")
    p.add_argument("evidence_dir", type=Path)
    p.add_argument("--json", action="store_true", dest="json_output")
    return p.parse_args()


def read_key_values(path):
    data = {}
    for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            data[key.strip()] = value.strip()
    return data


def read_csv_checked(path):
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        raw = [row for row in csv.reader(fh, strict=True) if any(cell != "" for cell in row)]
    if not raw:
        raise ValueError(f"empty CSV: {path.name}")
    header = raw[0]
    width = len(header)
    malformed = [idx + 2 for idx, row in enumerate(raw[1:]) if len(row) != width]
    if malformed:
        raise ValueError(f"row-width mismatch {path.name}: lines {malformed}")
    return header, [dict(zip(header, row)) for row in raw[1:]]


def active_row(path, decision_id=None):
    _, rows = read_csv_checked(path)
    matches = [r for r in rows if r.get("RecordType") == "ACTIVE"]
    if decision_id is not None:
        matches = [r for r in matches if r.get("DecisionID") == decision_id]
    if len(matches) != 1:
        raise ValueError(f"expected one ACTIVE row in {path.name}, found {len(matches)}")
    return matches[0]


def iso_utc(value):
    if not value or value == "NA":
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def audit_event_files(evidence_dir, expected_config, decision_id):
    problems = []
    duplicate_summary = {}
    target_outcomes = []
    for prefix, id_field in (("bbma_signal_C10S1_", "EventID"), ("bbma_outcome_C10O1_", "OutcomeEventID")):
        domains = defaultdict(list)
        for path in sorted(evidence_dir.glob(prefix + "*.csv")):
            try:
                _, rows = read_csv_checked(path)
            except Exception as exc:
                problems.append(str(exc))
                continue
            for row in rows:
                domain = (row.get("Schema"), row.get("BuildID"), row.get("SourceHash"), row.get("ConfigFingerprint"))
                if (row.get("BuildID") != EXPECTED_BUILD or
                    row.get("SourceHash") != EXPECTED_SOURCE_HASH or
                    row.get("ConfigFingerprint") != expected_config):
                    continue
                domains[domain].append((row.get(id_field, ""), path.name, row))
                if prefix.startswith("bbma_outcome") and row.get("DecisionID") == decision_id:
                    target_outcomes.append(row)
        for domain, items in domains.items():
            ids = defaultdict(list)
            for event_id, name, _ in items:
                if event_id:
                    ids[event_id].append(name)
            dups = {event_id: names for event_id, names in ids.items() if len(names) > 1}
            if dups:
                duplicate_summary[str(domain)] = dups
                problems.append(f"duplicate {id_field} inside provenance domain {domain}")
    return problems, duplicate_summary, target_outcomes


def main():
    args = parse_args()
    ev = args.evidence_dir.resolve()
    result = {"evidence_dir": str(ev), "status": "FAIL", "checks": {}, "problems": []}
    try:
        identity = read_key_values(ev / "identity.txt")
        decision_id = identity["DecisionID"]
        expected_config = identity["ConfigFingerprint"]
        result["identity"] = identity
        if identity.get("BuildID") != EXPECTED_BUILD:
            result["problems"].append("identity BuildID mismatch")
        if identity.get("SourceHash") != EXPECTED_SOURCE_HASH:
            result["problems"].append("identity SourceHash mismatch")
        runtime_artifact_ok = (identity.get("RuntimeMQ4SHA") == EXPECTED_RUNTIME_MQ4_SHA and
                               identity.get("RuntimeEX4SHA") == EXPECTED_RUNTIME_EX4_SHA)
        if not runtime_artifact_ok:
            result["problems"].append("runtime MQ4/EX4 artifact identity mismatch")
        result["checks"]["runtime_artifact_identity"] = runtime_artifact_ok

        pre = active_row(ev / "checkpoint_pre_restart_ACTIVE.csv", decision_id)
        post = active_row(ev / "checkpoint_post_restart.csv", decision_id)
        field_mismatches = [f for f in FROZEN_CP_FIELDS if pre.get(f) != post.get(f)]
        if field_mismatches:
            result["problems"].append("checkpoint frozen-field mismatch: " + ",".join(field_mismatches))
        for row_name, row in (("pre", pre), ("post", post)):
            if row.get("BuildID") != EXPECTED_BUILD or row.get("SourceHash") != EXPECTED_SOURCE_HASH:
                result["problems"].append(f"{row_name} checkpoint source identity mismatch")
            if row.get("ConfigFingerprint") != expected_config:
                result["problems"].append(f"{row_name} checkpoint config mismatch")
        result["checks"]["exact_active_recovery"] = not field_mismatches

        entry_epoch = int(pre.get("EntryTime", "0") or 0)
        entry_m5 = int(pre.get("EntryM5Open", "0") or 0)
        last_m5 = int(pre.get("LastM5Closed", "0") or 0)
        expected_entry_m5 = entry_epoch - (entry_epoch % 300) if entry_epoch > 0 else 0
        enrollment_ok = expected_entry_m5 > 0 and entry_m5 == expected_entry_m5 and last_m5 >= expected_entry_m5 - 300
        if not enrollment_ok:
            result["problems"].append("M5 enrollment anchor is not proven from entry_time")
        result["checks"]["m5_enrollment_anchor"] = enrollment_ok

        launch = (ev / "launch_config.ini").read_text(encoding="utf-8-sig", errors="replace")
        params = read_key_values(ev / "launch_parameters.set")
        launch_ok = "ExpertsTrades=false" in launch and "ExpertParameters=BBMA_C10DB_SHADOW_20PAIR_I81.set" in launch
        params_ok = params.get("InstanceID") == "81" and params.get("MaxTradePerPair") == "0" and params.get("MaxTotalTrade") == "0" and params.get("EnableC10StatisticsLedger", "").lower() == "true" and params.get("EnableC10ShadowOutcomes", "").lower() == "true"
        if not launch_ok:
            result["problems"].append("launch config does not prove ExpertsTrades=false / expected parameter set")
        if not params_ok:
            result["problems"].append("parameter set does not prove InstanceID=81 / zero trade caps / C10 shadow enabled")
        result["checks"]["safe_launch_config"] = launch_ok and params_ok

        event_problems, duplicates, target_outcomes = audit_event_files(ev, expected_config, decision_id)
        result["problems"].extend(event_problems)
        result["duplicates"] = duplicates
        result["checks"]["duplicate_free"] = not duplicates

        chronology_ok = True
        for row in target_outcomes:
            entry_dt = iso_utc(row.get("EntryTimeUTC"))
            exit_dt = iso_utc(row.get("ExitTimeUTC"))
            if entry_dt and exit_dt and exit_dt < entry_dt:
                chronology_ok = False
                result["problems"].append("target outcome precedes enrollment")
        if len(target_outcomes) > 1:
            result["problems"].append("duplicate target DecisionID outcome")
        result["checks"]["target_outcome_chronology"] = chronology_ok and len(target_outcomes) <= 1

        log_path = ev / "mql4_post_restart.log"
        log_text = log_path.read_text(encoding="utf-8-sig", errors="replace")
        recovery_count = len(re.findall(r"\[C10\]\[SHADOW_RECOVERY\]\s+Active=1", log_text))
        ready_pattern = re.compile(r"\[C10\]\[READY\].*Config=" + re.escape(expected_config) + r".*Authority=NONE")
        ready_ok = bool(ready_pattern.search(log_text))
        forbidden = {marker: log_text.count(marker) for marker in FORBIDDEN_RUNTIME_MARKERS if marker in log_text}
        if recovery_count < 1:
            result["problems"].append("missing post-restart SHADOW_RECOVERY Active=1")
        if not ready_ok:
            result["problems"].append("missing post-restart READY with exact config and Authority=NONE")
        if forbidden:
            result["problems"].append("forbidden runtime markers: " + json.dumps(forbidden, sort_keys=True))
        result["checks"]["recovery_marker"] = recovery_count >= 1
        result["checks"]["authority_none"] = ready_ok
        result["checks"]["zero_broker_actions_and_no_ledger_disable"] = not forbidden
        result["runtime_marker_counts"] = {"recovery_active1": recovery_count, **forbidden}

        result["status"] = "PASS" if not result["problems"] else "FAIL"
    except Exception as exc:
        result["problems"].append(f"verification exception: {exc}")

    rendered = json.dumps(result, indent=2, sort_keys=True)
    (ev / "VERIFIER_RESULT.json").write_text(rendered + "\n", encoding="utf-8")
    if args.json_output:
        print(rendered)
    else:
        print("C10_481_LIVE_PHYSICAL_RESTART=" + result["status"])
        for key, value in sorted(result.get("checks", {}).items()):
            print(f"{key}={'PASS' if value else 'FAIL'}")
        for problem in result["problems"]:
            print("PROBLEM=" + problem)
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
