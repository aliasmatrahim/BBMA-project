#!/usr/bin/env python3
"""Fail-closed P0 + R1-R6 analyzer for BBMA v4.59 runtime bundles."""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

BLOB = "dc83e62748c93171d89a312e9f7a53c06d97e261"
SHA = "0a42ee2e6c32810f655b592d8738f500e8b63b4e08c4c874e82452f75ce94b2e"
SCHEMA = "BBMA_V459_RUNTIME_BUNDLE_V1"
ASSERT_SCHEMA = "BBMA_V459_RUNTIME_ASSERTIONS_V1"
EXPECTED_BLOB = BLOB
EXPECTED_SHA256 = SHA
GATES = {
    "BASELINE": {"d1_tpw": False, "c044": False},
    "R1_D1TPW": {"d1_tpw": True, "c044": False},
    "R2_C044": {"d1_tpw": False, "c044": True},
}
PROFILE_GATES = GATES
CASES = (
    "P0_EXEC_ID_DURABLE",
    "P0_RESTART_RECOVERY",
    "P0_EXEC_ID_UNIQUENESS",
    "R1_CHECKPOINT_RESTART",
    "R1_TPW_COMPLETION_CLOSE",
    "R1_IDEMPOTENCY",
    "R2_CHECKPOINT_RESTART",
    "R2_FAILED_MOMENTUM_CLOSE",
    "R2_MOMENTUM_REARM",
    "R2_CYCLE_SUPERSESSION",
    "R2_M20_PRECEDENCE",
    "R3_D1_OWNER_MATRIX",
    "R3_D1O_IDENTITY",
    "R4_VALIDATION_TIMING",
    "R4_M17_SL_GEOMETRY",
    "R5_TRADELOCK",
    "R5_CUMULATIVE_RISK",
    "R5_P3_BCD",
    "R6_N2_CHAIN",
    "N3_FIREWALL",
)

KV = re.compile(r"([A-Za-z0-9_]+)=([^\s]+)")
GV = re.compile(r"\[V459-OBS\]\[GV\].*?TS=(\d+).*?Name=([^\s]+).*?Value=([-+0-9.eE]+)")
START = re.compile(r"\[V459-OBS\]\[START\].*?TS=(\d+)")
HIST = re.compile(r"\[V459-OBS\]\[HIST\].*?Ticket=(\d+).*?CloseTime=(\d+)")
OPEN = re.compile(r"\[V459-OBS\]\[OPEN\].*?Ticket=(\d+)")
OWNER = re.compile(r"\[D1-10A\]\s+[^\s]+\s+D1=([BSTU])\b")
TIME_TOKEN = r"\d{4}\.\d{2}\.\d{2}\s+\d{2}:\d{2}(?::\d{2})?"
EXEC = re.compile(
    r"\[P3M[12]\]\[EXEC\].*?Ticket=(\d+).*?Signal=([^\s]+).*?ValidateCandle=("
    + TIME_TOKEN + r")\s+OrderOpen=(" + TIME_TOKEN + r")"
)


@dataclass
class R:
    status: str
    detail: str
    evidence: list

    def d(self):
        return {"status": self.status, "detail": self.detail, "evidence": self.evidence}


def fields(line: str) -> dict[str, str]:
    return {m.group(1): m.group(2) for m in KV.finditer(line)}


def parse_mt4_time(value: str) -> datetime:
    for fmt in ("%Y.%m.%d %H:%M:%S", "%Y.%m.%d %H:%M"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    raise ValueError(f"unsupported MT4 timestamp: {value}")


def load(bundle: Path):
    manifest_path = bundle / "manifest.json"
    if not manifest_path.is_file():
        raise ValueError(f"missing manifest: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    issues = []
    if manifest.get("schema") != SCHEMA:
        issues.append("schema mismatch")
    profile = manifest.get("profile")
    if profile not in GATES:
        issues.append("unsupported profile")
    src = manifest.get("canonical_source", {})
    if src.get("blob") != BLOB or src.get("sha256") != SHA:
        issues.append("canonical identity mismatch")
    if src.get("property_version") not in (None, "4.59"):
        issues.append("property version mismatch")
    if profile in GATES and manifest.get("expected_gates") != GATES[profile]:
        issues.append("profile/gate mismatch")

    paths, lines = [], []
    for name in manifest.get("files", []):
        path = bundle / "raw" / str(name)
        if not path.is_file():
            raise ValueError(f"missing raw log: {path}")
        paths.append(path)
        lines += path.read_text(encoding="utf-8", errors="ignore").splitlines()
    if not paths:
        raise ValueError("bundle has no logs")
    return manifest, issues, paths, lines


def assertions(bundle: Path, paths: list[Path]) -> dict[str, R]:
    path = bundle / "assertions.json"
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if payload.get("schema") != ASSERT_SCHEMA:
        raise ValueError("assertion schema mismatch")
    texts = {"raw/" + p.name: p.read_text(encoding="utf-8", errors="ignore") for p in paths}
    out = {}
    for row in payload.get("assertions", []):
        cid = row.get("case_id")
        status = row.get("status")
        refs = row.get("evidence_refs", [])
        if cid not in CASES or status not in ("PASS", "FAIL") or not refs:
            raise ValueError("invalid assertion row")
        for ref in refs:
            if "#" not in ref:
                raise ValueError("bad assertion ref")
            rel, needle = ref.split("#", 1)
            if rel not in texts or not needle or needle not in texts[rel]:
                raise ValueError(f"assertion ref not found: {ref}")
        out[cid] = R(status, str(row.get("note", "indexed raw evidence")), refs)
    return out


def snapshots(lines: list[str], prefix: str):
    out = defaultdict(lambda: defaultdict(dict))
    for line in lines:
        m = GV.search(line)
        if not m or not m.group(2).startswith(prefix + "|"):
            continue
        z = re.search(r"\|T(\d+)\|([^\s]+)$", m.group(2))
        if z:
            out[int(z.group(1))][int(m.group(1))][z.group(2)] = float(m.group(3))
    return out


def history(lines: list[str]) -> dict[int, int]:
    out = {}
    for line in lines:
        m = HIST.search(line)
        if m:
            ticket = int(m.group(1))
            out[ticket] = max(out.get(ticket, 0), int(m.group(2)))
    return out


def p0_exec_rows(lines: list[str]) -> list[dict]:
    rows = []
    for idx, line in enumerate(lines):
        if "[P3S5][EXEC_ID]" not in line:
            continue
        f = fields(line)
        try:
            ticket = int(f.get("Ticket", "0"))
        except ValueError:
            ticket = 0
        rows.append({"index": idx, "line": line, "ticket": ticket, "fields": f})
    return rows


def recovery_rows(lines: list[str]) -> list[dict]:
    rows = []
    for idx, line in enumerate(lines):
        if "[P3S5][RECOVERY]" not in line:
            continue
        f = fields(line)
        try:
            ticket = int(f.get("Ticket", "0"))
        except ValueError:
            ticket = 0
        rows.append({"index": idx, "line": line, "ticket": ticket, "fields": f})
    return rows


def p0_durable(lines: list[str]) -> R:
    rows = p0_exec_rows(lines)
    if not rows:
        return R("INCOMPLETE", "no fresh v4.59 EXEC_ID evidence", [])
    explicit_fail = [r["line"] for r in rows if r["fields"].get("Persist") == "FAIL" or r["fields"].get("Local") == "N"]
    if explicit_fail:
        return R("FAIL", "execution identity local persistence failure observed", explicit_fail[:3])
    good = []
    for r in rows:
        f = r["fields"]
        h = f.get("ExpectedHash", "")
        if r["ticket"] > 0 and f.get("Persist") == "PASS" and f.get("Local") == "Y" and len(h) == 16:
            good.append(r["line"])
    if good:
        return R("PASS", "fresh execution persisted to authoritative terminal identity store", good[:3])
    return R("INCOMPLETE", "EXEC_ID rows exist but no Persist=PASS Local=Y 16-hex identity", [r["line"] for r in rows[:3]])


def identity(lines: list[str]) -> R:
    by_hash = defaultdict(set)
    for row in p0_exec_rows(lines):
        h = row["fields"].get("ExpectedHash", "")
        if h and h != "-" and row["ticket"] > 0:
            by_hash[h].add(row["ticket"])
    duplicates = {h: sorted(tickets) for h, tickets in by_hash.items() if len(tickets) > 1}
    if duplicates:
        return R("FAIL", "same execution hash maps to multiple tickets", [str(duplicates)])
    if by_hash:
        return R("PASS", "observed execution hashes are one-ticket-per-hash", [f"hashes={len(by_hash)}"])
    return R("INCOMPLETE", "no EXEC_ID evidence", [])


def p0_restart(lines: list[str]) -> R:
    starts = sum(bool(START.search(line)) for line in lines)
    execs = p0_exec_rows(lines)
    recs = recovery_rows(lines)
    if not execs:
        return R("INCOMPLETE", "no fresh EXEC_ID ticket to recover", [])
    exec_by_ticket = {r["ticket"]: r for r in execs if r["ticket"] > 0 and r["fields"].get("Persist") == "PASS" and r["fields"].get("Local") == "Y"}
    if not exec_by_ticket:
        return R("INCOMPLETE", "no locally persisted fresh ticket", [])

    bad = []
    good = []
    for rec in recs:
        if rec["ticket"] not in exec_by_ticket:
            continue
        f = rec["fields"]
        state = f.get("State", "")
        cause = f.get("Cause", "")
        hash_found = f.get("HashFound", "")
        if state == "REC_IDENTITY_MISSING_FROZEN" or hash_found == "N":
            bad.append(rec["line"])
            continue
        accepted = state in ("REC_NORMAL", "REC_PARTIAL_INFERRED")
        accepted = accepted or (state == "REC_IDENTITY_HASH_ONLY" and cause == "EXECUTION_HASH_ONLY" and hash_found == "Y")
        if accepted and hash_found == "Y":
            good.append(rec["line"])
    if bad:
        return R("FAIL", "fresh persisted ticket lost durable identity on recovery", bad[:3])
    if starts >= 2 and good:
        return R("PASS", "same fresh ticket recovered after restart epoch with durable hash", good[:3])
    detail = f"need >=2 V459 observer START epochs and accepted same-ticket recovery; starts={starts} accepted={len(good)}"
    return R("INCOMPLETE", detail, good[:3])


def recover_normal(lines: list[str], ticket: int) -> list[str]:
    out = []
    for row in recovery_rows(lines):
        if row["ticket"] != ticket:
            continue
        if row["fields"].get("State") in ("REC_NORMAL", "REC_PARTIAL_INFERRED"):
            out.append(row["line"])
    return out


def lifecycle(profile: str, lines: list[str]) -> dict[str, R]:
    out = {}
    starts = sum(bool(START.search(x)) for x in lines)
    hist = history(lines)
    ident = identity(lines)
    if profile == "R1_D1TPW":
        snap = snapshots(lines, "D1TPW")
        tickets = [t for t, values in snap.items() if any("LP" in frame for frame in values.values())]
        frozen = [x for x in lines if "D1TPW lifecycle frozen" in x]
        good = [(t, recover_normal(lines, t)) for t in tickets if recover_normal(lines, t)]
        out["R1_CHECKPOINT_RESTART"] = (
            R("FAIL", "D1TPW freeze observed", frozen[:3]) if frozen else
            R("PASS", "checkpoint recovered after restart", good[0][1][:2]) if starts >= 2 and good else
            R("INCOMPLETE", "need 2 START epochs + checkpoint + normal/partial recovery", [])
        )
        done = []
        for ticket, values in snap.items():
            for _, frame in sorted(values.items()):
                if frame.get("L") == 1 and frame.get("XL", 0) > 0 and hist.get(ticket, 0) >= int(frame["XL"]):
                    done.append((ticket, int(frame["XL"]), hist[ticket]))
        out["R1_TPW_COMPLETION_CLOSE"] = (
            R("FAIL", "D1TPW freeze observed", frozen[:3]) if frozen else
            R("PASS", "TPW latch followed by same-ticket history close", [str(done[0])]) if done else
            R("INCOMPLETE", "need L=1 XL>0 then same ticket closed", [])
        )
        out["R1_IDEMPOTENCY"] = ident

    if profile == "R2_C044":
        snap = snapshots(lines, "C044")
        tickets = [t for t, values in snap.items() if any("ST" in frame for frame in values.values())]
        frozen = [x for x in lines if "C044 lifecycle frozen" in x]
        good = [(t, recover_normal(lines, t)) for t in tickets if recover_normal(lines, t)]
        out["R2_CHECKPOINT_RESTART"] = (
            R("FAIL", "C044 freeze observed", frozen[:3]) if frozen else
            R("PASS", "checkpoint/replay recovered after restart", good[0][1][:2]) if starts >= 2 and good else
            R("INCOMPLETE", "need 2 START epochs + checkpoint + normal/partial recovery", [])
        )
        for cid, reason in (("R2_FAILED_MOMENTUM_CLOSE", 1), ("R2_CYCLE_SUPERSESSION", 2)):
            done = []
            for ticket, values in snap.items():
                for _, frame in sorted(values.items()):
                    if frame.get("ST") == 3 and frame.get("XR") == reason and frame.get("XL", 0) > 0 and hist.get(ticket, 0) >= int(frame["XL"]):
                        done.append((ticket, int(frame["XL"]), hist[ticket]))
            out[cid] = (
                R("FAIL", "C044 freeze observed", frozen[:3]) if frozen else
                R("PASS", f"latched XR={reason} then closed", [str(done[0])]) if done else
                R("INCOMPLETE", f"need ST=3 XR={reason} XL>0 then close", [])
            )
        rearms = []
        for ticket, values in snap.items():
            ordered = sorted(values.items())
            for idx, (_, frame) in enumerate(ordered):
                if frame.get("ST") != 2:
                    continue
                if any(later.get("ST") == 1 and later.get("EP", 0) > frame.get("EP", -1) for _, later in ordered[idx + 1:]):
                    rearms.append(ticket)
                    break
        out["R2_MOMENTUM_REARM"] = R("PASS", "WAIT_NEXT_REENTRY -> newer WAIT_OUTER_TEST epoch", [str(rearms[0])]) if rearms else R("INCOMPLETE", "need ST=2 -> newer ST=1 epoch", [])
    return out


def d1_owner_matrix(lines: list[str]) -> R:
    states = {m.group(1) for x in lines if (m := OWNER.search(x))}
    if states >= {"B", "S", "T", "U"}:
        return R("PASS", "B/S/T/U D1 owner states all observed", [str(sorted(states))])
    return R("INCOMPLETE", f"owner states={sorted(states)}", [])


def timing(lines: list[str]) -> R:
    rows = []
    for line in lines:
        m = EXEC.search(line)
        if not m:
            continue
        validated = parse_mt4_time(m.group(3))
        opened = parse_mt4_time(m.group(4))
        rows.append((int(m.group(1)), (opened - validated).total_seconds()))
    bad = [row for row in rows if row[1] <= 0]
    if bad:
        return R("FAIL", "order at/before validation timestamp", [str(x) for x in bad[:3]])
    if rows:
        return R("PASS", "all observed orders strictly after validation timestamp", [f"executions={len(rows)}"])
    return R("INCOMPLETE", "no EXEC timing evidence", [])


def m17(lines: list[str]) -> R:
    coverage = {"BUY": 0, "SELL": 0, "JPY": 0, "NONJPY": 0}
    bad, count = [], 0
    for line in lines:
        if "[M17-SL][STRUCT]" not in line:
            continue
        f = fields(line)
        count += 1
        try:
            direction = f["Dir"]
            pair = f["Pair"]
            raw = float(f["RawSpreadPips"])
            buffer_pips = float(f["SpreadBufferPips"])
            structural = float(f["StructuralSL"])
            final = float(f["FinalBrokerSL"])
            tp = float(f["TP"])
        except Exception:
            bad.append("unparseable M17 row")
            continue
        if direction == "DIR_BUY":
            coverage["BUY"] = 1
        elif direction == "DIR_SELL":
            coverage["SELL"] = 1
        else:
            bad.append("unknown M17 direction: " + direction)
            continue
        coverage["JPY" if "JPY" in pair.upper() else "NONJPY"] = 1
        if direction == "DIR_BUY" and (abs(buffer_pips) > 1e-9 or final > structural + 1e-12):
            bad.append(line)
        if direction == "DIR_SELL" and (buffer_pips + 1e-9 < max(2, math.ceil(raw - 1e-9)) or final + 1e-12 < structural):
            bad.append(line)
        if (f.get("C044") == "Y" or f.get("D1TPW") == "Y") and abs(tp) > 1e-9:
            bad.append(line)
    if bad:
        return R("FAIL", "M17 geometry violation", bad[:3])
    if count and all(coverage.values()):
        return R("PASS", "BUY+SELL and JPY+non-JPY geometry observed", [f"rows={count}"])
    return R("INCOMPLETE", f"M17 valid rows={count}; coverage={coverage}", [])


def n2(lines: list[str], paths: list[Path]) -> R:
    counts = {k: sum(k in x for x in lines) for k in ("[N1-NMJE]", "[N2-NMJE-DEC]", "[N2-NMJE-OUT]")}
    if not all(counts.values()):
        return R("INCOMPLETE", f"chain counts={counts}", [])
    try:
        import n2_nmje_auto_research_pipeline as tool
        with tempfile.TemporaryDirectory() as td:
            report = tool.run(paths, Path(td))
        reconciliation = report["reconciliation"]
        evidence = report["evidence"]
        matched = report["attribution"].get("matched_outcomes", 0)
        if not reconciliation.get("identity_valid") or evidence.get("data_status") == "IDENTITY_INVALID":
            return R("FAIL", "N2 identity reconciliation invalid", [])
        if matched:
            return R("PASS", "N2 closed outcome identity attributed", [f"matched={matched}"])
        return R("INCOMPLETE", "N2 markers exist; no attributed close yet", [])
    except Exception as exc:
        return R("FAIL", f"N2 pipeline error: {exc}", [])


def simple_presence(lines: list[str], markers: tuple[str, ...], detail: str) -> R:
    evidence = [line for line in lines if any(marker in line for marker in markers)]
    if evidence:
        return R("PASS", detail, evidence[:3])
    return R("INCOMPLETE", "required runtime evidence not observed", [])


def analyze_bundle(bundle: Path) -> dict:
    manifest, issues, paths, lines = load(bundle)
    asserted = assertions(bundle, paths)
    results = {case: R("INCOMPLETE", "no applicable evidence in this bundle", []) for case in CASES}

    if issues:
        fail = "; ".join(issues)
        return {
            "bundle": str(bundle),
            "profile": manifest.get("profile"),
            "manifest_issues": issues,
            "cases": {case: R("FAIL", fail, []).d() for case in CASES},
        }

    blocked = bool(manifest.get("hosted_smoke_only")) or not bool(manifest.get("broker_connected")) or not bool(manifest.get("session_authenticated"))
    if blocked:
        why = "hosted/no authenticated connected broker session"
        for case in CASES:
            if case != "N3_FIREWALL":
                results[case] = R("BLOCKED", why, [])

    alltext = "\n".join(lines)
    results["N3_FIREWALL"] = (
        R("FAIL", "unapproved N3 execution marker observed", [])
        if any(marker in alltext for marker in ("N3_POLICY_ACTIVE", "N3_EXECUTION_POLICY"))
        else R("PASS", "N3 policy remains NONE/inactive", [])
    )

    if not blocked:
        results["P0_EXEC_ID_DURABLE"] = p0_durable(lines)
        results["P0_RESTART_RECOVERY"] = p0_restart(lines)
        results["P0_EXEC_ID_UNIQUENESS"] = identity(lines)
        for key, value in lifecycle(manifest["profile"], lines).items():
            results[key] = value
        results["R3_D1_OWNER_MATRIX"] = d1_owner_matrix(lines)
        results["R3_D1O_IDENTITY"] = identity(lines)
        results["R4_VALIDATION_TIMING"] = timing(lines)
        results["R4_M17_SL_GEOMETRY"] = m17(lines)
        results["R5_TRADELOCK"] = simple_presence(lines, ("REJ_TRADE_LOCK", "LOCK_ONE_POSITION", "LOCK_SAME_DIRECTION"), "trade-lock runtime decision evidence observed")
        results["R5_CUMULATIVE_RISK"] = simple_presence(lines, ("REJ_TOTAL_RISK", "Total risk limit exceeded"), "cumulative risk guard evidence observed")
        results["R5_P3_BCD"] = simple_presence(lines, ("[P3M1][", "[P3M2]["), "P3 B/C/D execution-path telemetry observed")
        results["R6_N2_CHAIN"] = n2(lines, paths)

        # Human/operator assertions are accepted only when they point to exact raw
        # evidence in an authenticated broker bundle. They never rescue a bad
        # manifest identity and never override the N3 firewall.
        for case, result in asserted.items():
            if case != "N3_FIREWALL":
                results[case] = result

    return {
        "schema": "BBMA_V459_RUNTIME_REPORT_V1",
        "bundle": str(bundle),
        "profile": manifest.get("profile"),
        "manifest_issues": [],
        "broker_connected": bool(manifest.get("broker_connected")),
        "session_authenticated": bool(manifest.get("session_authenticated")),
        "hosted_smoke_only": bool(manifest.get("hosted_smoke_only")),
        "cases": {case: results[case].d() for case in CASES},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("bundle", nargs="+")
    ap.add_argument("--output")
    args = ap.parse_args()

    reports = []
    failed = False
    for item in args.bundle:
        report = analyze_bundle(Path(item).resolve())
        reports.append(report)
        if any(row.get("status") == "FAIL" for row in report["cases"].values()):
            failed = True

    payload = {"schema": "BBMA_V459_RUNTIME_MULTI_REPORT_V1", "reports": reports}
    rendered = json.dumps(payload, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 2 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
