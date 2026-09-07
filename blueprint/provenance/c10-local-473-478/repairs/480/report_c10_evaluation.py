#!/usr/bin/env python3
"""Deterministic C10 development/evaluation reporter.

Realized and shadow populations are always grouped separately. The reporter
does not score, select, optimize, or write EA state.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable


SIGNAL_HEADER = (
    "Schema,BuildID,SourceHash,ConfigFingerprint,RunID,EventID,EventTimeUTC,"
    "DecisionID,AttemptSeq,Pair,Direction,SetupFamily,EntryTimeframe,"
    "D1OwnerEpochID,H4JourneyID,H1SetupID,M15CandidateID,M5EventID,"
    "NMJERelation,SignalState,ReasonCode,IntendedEntry,IntendedSL,IntendedTP,"
    "SLSource,TPSource,SpreadPips"
).split(",")

OUTCOME_HEADER = (
    "Schema,BuildID,SourceHash,ConfigFingerprint,RunID,OutcomeEventID,"
    "OutcomeTimeUTC,Mode,DecisionID,ExecutionID,OrderTicket,Pair,Direction,"
    "SetupFamily,EntryTimeframe,EntryTimeUTC,ExitTimeUTC,EntryPrice,ExitPrice,"
    "IntendedSL,IntendedTP,Lot,SpreadPips,SlippagePips,GrossPL,Commission,"
    "Swap,NetPL,RiskAmount,RMultiple,MFEPips,MAEPips,HoldingSeconds,ExitReason,"
    "EvidenceResolution"
).split(",")


class EvidenceError(RuntimeError):
    pass


@dataclass(frozen=True)
class Window:
    name: str
    start: date
    end: date

    def contains(self, value: date) -> bool:
        return self.start <= value <= self.end


def parse_day(value: str) -> date:
    return date.fromisoformat(value)


def parse_utc_day(value: str) -> date:
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise EvidenceError(f"invalid UTC timestamp: {value}") from exc
    return parsed.replace(tzinfo=timezone.utc).date()


def validate_windows(development: Window, evaluation: Window) -> None:
    if development.start > development.end or evaluation.start > evaluation.end:
        raise EvidenceError("window start must not be after window end")
    if not (development.end < evaluation.start or evaluation.end < development.start):
        raise EvidenceError("development and evaluation windows overlap")


def window_for(day: date, windows: tuple[Window, Window]) -> str | None:
    matches = [window.name for window in windows if window.contains(day)]
    if len(matches) > 1:
        raise EvidenceError("one event matched multiple windows")
    return matches[0] if matches else None


def load_rows(paths: Iterable[Path], expected_header: list[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(paths):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames != expected_header:
                raise EvidenceError(f"schema mismatch: {path}")
            for line_number, row in enumerate(reader, start=2):
                if None in row or any(value is None for value in row.values()):
                    raise EvidenceError(f"row shape mismatch: {path}:{line_number}")
                row["__source"] = path.name
                row["__line"] = str(line_number)
                rows.append(row)
    return rows


def dedupe_event_rows(rows: list[dict[str, str]], id_field: str) -> list[dict[str, str]]:
    """Deduplicate only inside one immutable ledger provenance domain.

    Event IDs are deterministic decision identities and can legitimately repeat
    across builds/configurations.  A global EventID key therefore turns a
    side-by-side legacy/namespaced audit into a false integrity failure.
    """
    seen: dict[tuple[str, str, str, str], dict[str, str]] = {}
    for row in rows:
        event_id = row[id_field]
        if not event_id or event_id == "NA":
            raise EvidenceError(f"missing {id_field}")
        provenance = (
            row["BuildID"], row["SourceHash"], row["ConfigFingerprint"]
        )
        if any(not value or value == "NA" for value in provenance):
            raise EvidenceError(f"missing provenance for {id_field}: {event_id}")
        key = (*provenance, event_id)
        canonical = {k: v for k, v in row.items() if not k.startswith("__")}
        if key in seen and canonical != seen[key]:
            raise EvidenceError(
                f"conflicting duplicate {id_field} in provenance domain: {event_id}"
            )
        seen[key] = canonical
    return [dict(seen[key]) for key in sorted(seen)]


def numeric_present(value: str) -> bool:
    if value in ("", "NA"):
        return False
    try:
        float(value)
    except ValueError as exc:
        raise EvidenceError(f"invalid numeric evidence: {value}") from exc
    return True


def build_report(
    signal_rows: list[dict[str, str]],
    outcome_rows: list[dict[str, str]],
    development: Window,
    evaluation: Window,
) -> dict:
    validate_windows(development, evaluation)
    windows = (development, evaluation)
    signal_rows = dedupe_event_rows(signal_rows, "EventID")
    outcome_rows = dedupe_event_rows(outcome_rows, "OutcomeEventID")

    decision_windows: dict[tuple[str, str, str, str], set[str]] = {}
    latest_signal: dict[tuple[str, str, str, str, str], dict[str, str]] = {}
    for row in signal_rows:
        window = window_for(parse_utc_day(row["EventTimeUTC"]), windows)
        if window is None:
            continue
        identity = (
            row["BuildID"], row["SourceHash"], row["ConfigFingerprint"],
            row["DecisionID"],
        )
        decision_windows.setdefault(identity, set()).add(window)
        key = (window, *identity)
        try:
            attempt = int(row["AttemptSeq"])
        except ValueError as exc:
            raise EvidenceError("AttemptSeq must be an integer") from exc
        prior = latest_signal.get(key)
        if prior is None or attempt > int(prior["AttemptSeq"]):
            latest_signal[key] = row

    outcome_identity: set[tuple[str, str, str, str, str]] = set()
    grouped: dict[tuple[str, ...], dict] = {}
    for row in outcome_rows:
        if row["Mode"] not in ("REALIZED", "SHADOW"):
            raise EvidenceError(f"unsupported Mode: {row['Mode']}")
        window = window_for(parse_utc_day(row["OutcomeTimeUTC"]), windows)
        if window is None:
            continue
        decision_key = (
            row["BuildID"], row["SourceHash"], row["ConfigFingerprint"],
            row["DecisionID"],
        )
        decision_windows.setdefault(decision_key, set()).add(window)
        unique_key = (window, row["Mode"], *decision_key)
        if unique_key in outcome_identity:
            raise EvidenceError(
                "multiple outcomes for one DecisionID/mode/window: " + row["DecisionID"]
            )
        outcome_identity.add(unique_key)
        group_key = (
            window, row["BuildID"], row["SourceHash"],
            row["ConfigFingerprint"], row["Mode"], row["Pair"],
            row["SetupFamily"], row["Direction"], row["EntryTimeframe"],
        )
        group = grouped.setdefault(
            group_key,
            {
                "outcomes": Counter(),
                "rows": 0,
                "spread_present": 0,
                "slippage_present": 0,
                "excursion_present": 0,
            },
        )
        group["rows"] += 1
        group["outcomes"][row["ExitReason"]] += 1
        group["spread_present"] += int(numeric_present(row["SpreadPips"]))
        group["slippage_present"] += int(numeric_present(row["SlippagePips"]))
        mfe = numeric_present(row["MFEPips"])
        mae = numeric_present(row["MAEPips"])
        if mfe != mae:
            raise EvidenceError("MFE and MAE coverage must be paired")
        group["excursion_present"] += int(mfe and mae)

    crossing = [identity for identity, names in decision_windows.items() if len(names) > 1]
    if crossing:
        raise EvidenceError(f"DecisionID crosses development/evaluation windows: {crossing[0][3]}")

    signal_denominators: dict[str, Counter] = {
        development.name: Counter(), evaluation.name: Counter()
    }
    for key, row in latest_signal.items():
        window = key[0]
        signal_denominators[window][row["SignalState"]] += 1

    output_groups: list[dict] = []
    for key in sorted(grouped):
        group = grouped[key]
        outcomes = dict(sorted(group["outcomes"].items()))
        eligible = outcomes.get("TP", 0) + outcomes.get("SL", 0)
        output_groups.append(
            {
                "window": key[0],
                "build_id": key[1],
                "source_hash": key[2],
                "config_fingerprint": key[3],
                "mode": key[4],
                "pair": key[5],
                "setup_family": key[6],
                "direction": key[7],
                "entry_timeframe": key[8],
                "rows": group["rows"],
                "outcomes": outcomes,
                "eligible_tp_sl": eligible,
                "win_rate_tp_sl": (
                    round(outcomes.get("TP", 0) / eligible, 8) if eligible else None
                ),
                "spread_coverage": group["spread_present"],
                "slippage_coverage": group["slippage_present"],
                "excursion_coverage": group["excursion_present"],
            }
        )

    return {
        "policy": {
            "population_separation": "REALIZED_AND_SHADOW_NEVER_POOLED",
            "eligible_win_rate": "TP_DIVIDED_BY_TP_PLUS_SL",
            "ambiguous_unknown_expired": "VISIBLE_SEPARATE_DENOMINATORS",
            "authority": "NONE",
        },
        "windows": {
            development.name: {"from": str(development.start), "to": str(development.end)},
            evaluation.name: {"from": str(evaluation.start), "to": str(evaluation.end)},
        },
        "signal_denominators": {
            name: dict(sorted(values.items()))
            for name, values in signal_denominators.items()
        },
        "groups": output_groups,
    }


def write_report(report: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "c10_evaluation_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    columns = [
        "window", "build_id", "source_hash", "config_fingerprint", "mode",
        "pair", "setup_family", "direction", "entry_timeframe", "rows",
        "eligible_tp_sl", "win_rate_tp_sl", "spread_coverage",
        "slippage_coverage", "excursion_coverage", "outcomes",
    ]
    with (output_dir / "c10_evaluation_groups.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for group in report["groups"]:
            row = {key: group[key] for key in columns if key != "outcomes"}
            row["outcomes"] = json.dumps(group["outcomes"], sort_keys=True)
            writer.writerow(row)
    lines = [
        "# C10 Evaluation Report",
        "",
        "Policy: REALIZED and SHADOW are never pooled. TP/SL win rate excludes "
        "AMBIGUOUS, UNKNOWN and EXPIRED, which remain visible.",
        "",
        "| Window | Mode | Pair | Setup | Direction | Rows | TP/SL eligible | Win rate | Spread | Slippage | MFE/MAE |",
        "|---|---|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for group in report["groups"]:
        rate = "NA" if group["win_rate_tp_sl"] is None else f"{group['win_rate_tp_sl']:.4f}"
        lines.append(
            f"| {group['window']} | {group['mode']} | {group['pair']} | "
            f"{group['setup_family']} | {group['direction']} | {group['rows']} | "
            f"{group['eligible_tp_sl']} | {rate} | {group['spread_coverage']} | "
            f"{group['slippage_coverage']} | {group['excursion_coverage']} |"
        )
    (output_dir / "c10_evaluation_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger-dir", type=Path, required=True)
    parser.add_argument("--development-from", required=True)
    parser.add_argument("--development-to", required=True)
    parser.add_argument("--evaluation-from", required=True)
    parser.add_argument("--evaluation-to", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    development = Window(
        "development", parse_day(args.development_from), parse_day(args.development_to)
    )
    evaluation = Window(
        "evaluation", parse_day(args.evaluation_from), parse_day(args.evaluation_to)
    )
    signals = load_rows(args.ledger_dir.glob("bbma_signal_C10S1_*.csv"), SIGNAL_HEADER)
    outcomes = load_rows(args.ledger_dir.glob("bbma_outcome_C10O1_*.csv"), OUTCOME_HEADER)
    report = build_report(signals, outcomes, development, evaluation)
    write_report(report, args.output_dir)
    print(
        f"C10_EVALUATION_REPORT=PASS groups={len(report['groups'])} "
        "authority=NONE populations=SEPARATE"
    )


if __name__ == "__main__":
    main()
