#!/usr/bin/env python3
"""Analyze broker/demo runtime evidence for D1 owner, D1O dedup and timing.

Diagnostic only. This tool never changes EA state or strategy semantics. It reads
MT4 Journal/Experts logs that already contain current D1O-07 telemetry.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from d1o_canonical_dedup_log_analyzer import analyze as analyze_dedup
from d1o_canonical_dedup_log_analyzer import parse as parse_dedup

OWNER_RE = re.compile(
    r"\[D1-10A\]\s+(?P<pair>\S+)\s+"
    r"D1=(?P<state>[BSTU])\s+H4=(?P<h4>\S+)\s+F=(?P<final>.*)$"
)
EXEC_RE = re.compile(
    r"\[(?P<mode>P3M[12])\]\[EXEC\]\s+"
    r"Ticket=(?P<ticket>\d+)\s+Pair=(?P<pair>\S+)\s+"
    r"DecisionID=(?P<decision_id>\S+)\s+Signal=(?P<signal>\S+)\s+"
    r"Dir=(?P<direction>\S+)\s+"
    r"ValidateCandle=(?P<validate>\d{4}\.\d{2}\.\d{2}\s+\d{2}:\d{2}(?::\d{2})?)\s+"
    r"OrderOpen=(?P<order_open>\d{4}\.\d{2}\.\d{2}\s+\d{2}:\d{2}(?::\d{2})?)"
)

STATE_NAMES = {
    "B": "BUY_CONFIRMED",
    "S": "SELL_CONFIRMED",
    "T": "TRANSITION",
    "U": "UNRESOLVED",
}


@dataclass(frozen=True)
class OwnerRecord:
    file: str
    line_no: int
    pair: str
    state: str
    h4: str
    final: str


@dataclass(frozen=True)
class ExecutionRecord:
    file: str
    line_no: int
    mode: str
    ticket: int
    pair: str
    decision_id: str
    signal: str
    direction: str
    validate: str
    order_open: str
    delta_seconds: int


def parse_mt4_time(value: str) -> datetime:
    for fmt in ("%Y.%m.%d %H:%M:%S", "%Y.%m.%d %H:%M"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    raise ValueError(f"Unsupported MT4 timestamp: {value}")


def parse_runtime(paths: Iterable[Path]) -> tuple[list[OwnerRecord], list[ExecutionRecord]]:
    owners: list[OwnerRecord] = []
    executions: list[ExecutionRecord] = []
    for path in paths:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line_no, line in enumerate(handle, 1):
                m = OWNER_RE.search(line)
                if m:
                    owners.append(OwnerRecord(str(path), line_no, **m.groupdict()))

                m = EXEC_RE.search(line)
                if m:
                    fields = m.groupdict()
                    validate_dt = parse_mt4_time(fields["validate"])
                    open_dt = parse_mt4_time(fields["order_open"])
                    executions.append(
                        ExecutionRecord(
                            file=str(path),
                            line_no=line_no,
                            mode=fields["mode"],
                            ticket=int(fields["ticket"]),
                            pair=fields["pair"],
                            decision_id=fields["decision_id"],
                            signal=fields["signal"],
                            direction=fields["direction"],
                            validate=fields["validate"],
                            order_open=fields["order_open"],
                            delta_seconds=int((open_dt - validate_dt).total_seconds()),
                        )
                    )
    return owners, executions


def analyze(paths: list[Path]) -> dict:
    owners, executions = parse_runtime(paths)
    opportunities, decisions = parse_dedup(paths)
    dedup = analyze_dedup(opportunities, decisions)

    state_counts = Counter(row.state for row in owners)
    pairs_by_state: defaultdict[str, set[str]] = defaultdict(set)
    for row in owners:
        pairs_by_state[row.state].add(row.pair)

    owner_matrix = {
        "rows": len(owners),
        "state_counts": {code: state_counts.get(code, 0) for code in ("B", "S", "T", "U")},
        "state_names": STATE_NAMES,
        "pairs_by_state": {code: sorted(pairs_by_state.get(code, set())) for code in ("B", "S", "T", "U")},
        "missing_states": [code for code in ("B", "S", "T", "U") if state_counts.get(code, 0) == 0],
    }
    owner_matrix["all_four_states_observed"] = not owner_matrix["missing_states"]

    timing_violations = [asdict(row) for row in executions if row.delta_seconds <= 0]
    deltas = [row.delta_seconds for row in executions]
    timing = {
        "execution_rows": len(executions),
        "by_mode": dict(sorted(Counter(row.mode for row in executions).items())),
        "strict_before_count": sum(1 for row in executions if row.delta_seconds > 0),
        "non_strict_or_reversed": timing_violations,
        "min_delta_seconds": min(deltas) if deltas else None,
        "max_delta_seconds": max(deltas) if deltas else None,
    }

    dedup_integ = dedup["integrity"]
    dedup_fatal = bool(
        dedup_integ["cycle_identity_conflicts"]
        or dedup_integ["family_mismatch_decisions"]
        or dedup_integ["missing_sequence_hash_decisions"]
        or dedup_integ["sequence_hash_direction_conflicts"]
    )

    coverage = {
        "d1_owner_matrix_complete": owner_matrix["all_four_states_observed"],
        "d1o_dedup_observed": dedup["opportunity_decisions"] > 0 and dedup["unique_execution_hashes"] > 0,
        "validation_to_order_timing_observed": len(executions) > 0,
    }
    coverage["all_requested_runtime_evidence_observed"] = all(coverage.values())

    return {
        "files": [str(p) for p in paths],
        "d1_owner_matrix": owner_matrix,
        "d1o_canonical_dedup": dedup,
        "validation_to_order_timing": timing,
        "coverage": coverage,
        "integrity": {
            "dedup_fatal": dedup_fatal,
            "timing_violation_count": len(timing_violations),
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--json", dest="json_path", type=Path)
    args = ap.parse_args()

    missing = [str(path) for path in args.paths if not path.is_file()]
    if missing:
        raise SystemExit("Missing log file(s): " + ", ".join(missing))

    report = analyze(args.paths)
    text = json.dumps(report, indent=2, sort_keys=True)
    print(text)
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(text + "\n", encoding="utf-8")

    fatal = report["integrity"]["dedup_fatal"] or report["integrity"]["timing_violation_count"] > 0
    return 2 if fatal else 0


if __name__ == "__main__":
    raise SystemExit(main())
