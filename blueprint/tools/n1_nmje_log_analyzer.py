#!/usr/bin/env python3
"""Analyze N1 NMJE observation lines from MT4 Experts/Journal logs.

Observation/research only. This tool never changes EA source or trading logic.

Usage:
  python blueprint/tools/n1_nmje_log_analyzer.py path/to/log.txt
  python blueprint/tools/n1_nmje_log_analyzer.py logs/*.log --json out.json
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

LINE_RE = re.compile(
    r"\[N1-NMJE\]\s+"
    r"(?P<pair>\S+)\s+"
    r"REL=(?P<relation>\S+)\s+"
    r"P=(?P<parent>\S+)\s+"
    r"J=(?P<journey>\S+)\s+"
    r"D1=(?P<d1>\S+)\s+"
    r"H4=(?P<h4>\S+)\s+"
    r"H1=(?P<h1>\S+)\s+"
    r"M15=(?P<m15>\S+)\s+"
    r"R=(?P<reason>\S+)"
)

VALID_RELATIONS = {
    "N/A",
    "BUILDING",
    "SUPPORTING",
    "ALIGNED",
    "CONFLICT",
    "UNRESOLVED",
}


@dataclass(frozen=True)
class Observation:
    file: str
    line_no: int
    pair: str
    relation: str
    parent: str
    journey: str
    d1: str
    h4: str
    h1: str
    m15: str
    reason: str


def iter_observations(paths: Iterable[Path]) -> Iterable[Observation]:
    for path in paths:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line_no, line in enumerate(handle, 1):
                match = LINE_RE.search(line)
                if not match:
                    continue
                values = match.groupdict()
                yield Observation(
                    file=str(path),
                    line_no=line_no,
                    pair=values["pair"],
                    relation=values["relation"],
                    parent=values["parent"],
                    journey=values["journey"],
                    d1=values["d1"],
                    h4=values["h4"],
                    h1=values["h1"],
                    m15=values["m15"],
                    reason=values["reason"],
                )


def transitions(values: list[str]) -> Counter[str]:
    result: Counter[str] = Counter()
    if not values:
        return result
    previous = values[0]
    for current in values[1:]:
        if current != previous:
            result[f"{previous}->{current}"] += 1
        previous = current
    return result


def build_report(observations: list[Observation]) -> dict:
    relation_counts = Counter(o.relation for o in observations)
    reason_counts = Counter(o.reason for o in observations)
    pair_counts = Counter(o.pair for o in observations)
    parent_counts = Counter(o.parent for o in observations)

    by_pair: dict[str, list[Observation]] = defaultdict(list)
    by_journey: dict[str, list[Observation]] = defaultdict(list)
    for obs in observations:
        by_pair[obs.pair].append(obs)
        if obs.journey != "-":
            by_journey[obs.journey].append(obs)

    pair_relation_counts = {
        pair: dict(Counter(o.relation for o in rows))
        for pair, rows in sorted(by_pair.items())
    }
    pair_relation_transitions = {
        pair: dict(transitions([o.relation for o in rows]))
        for pair, rows in sorted(by_pair.items())
    }

    deterministic_violations: list[dict] = []
    for journey, rows in sorted(by_journey.items()):
        identities = {(o.pair, o.parent) for o in rows}
        if len(identities) > 1:
            deterministic_violations.append(
                {
                    "journey": journey,
                    "identities": sorted([list(x) for x in identities]),
                    "locations": [f"{o.file}:{o.line_no}" for o in rows],
                }
            )

    invalid_relations = [
        asdict(o) for o in observations if o.relation not in VALID_RELATIONS
    ]

    conflict_rows = [asdict(o) for o in observations if o.relation == "CONFLICT"]
    unresolved_rows = [asdict(o) for o in observations if o.relation == "UNRESOLVED"]

    return {
        "observation_count": len(observations),
        "unique_pairs": len(by_pair),
        "unique_journeys": len(by_journey),
        "relation_counts": dict(relation_counts),
        "parent_counts": dict(parent_counts),
        "reason_counts": dict(reason_counts),
        "pair_counts": dict(pair_counts),
        "pair_relation_counts": pair_relation_counts,
        "pair_relation_transitions": pair_relation_transitions,
        "deterministic_journey_violations": deterministic_violations,
        "invalid_relation_rows": invalid_relations,
        "conflict_rows": conflict_rows,
        "unresolved_rows": unresolved_rows,
    }


def print_report(report: dict) -> None:
    print("N1 NMJE LOG ANALYSIS")
    print("====================")
    print(f"Observations : {report['observation_count']}")
    print(f"Pairs        : {report['unique_pairs']}")
    print(f"Journeys     : {report['unique_journeys']}")
    print()

    print("Relations")
    for key, value in sorted(report["relation_counts"].items()):
        print(f"  {key:12s} {value}")
    print()

    print("Parents")
    for key, value in sorted(report["parent_counts"].items()):
        print(f"  {key:18s} {value}")
    print()

    print("Top reasons")
    for key, value in Counter(report["reason_counts"]).most_common(15):
        print(f"  {key:36s} {value}")
    print()

    print("Per-pair relation transitions")
    any_transition = False
    for pair, values in report["pair_relation_transitions"].items():
        if not values:
            continue
        any_transition = True
        summary = ", ".join(f"{k}={v}" for k, v in sorted(values.items()))
        print(f"  {pair}: {summary}")
    if not any_transition:
        print("  none observed")
    print()

    print("Integrity")
    print(
        "  deterministic JourneyID violations: "
        f"{len(report['deterministic_journey_violations'])}"
    )
    print(f"  invalid relation rows: {len(report['invalid_relation_rows'])}")
    print(f"  conflict rows: {len(report['conflict_rows'])}")
    print(f"  unresolved rows: {len(report['unresolved_rows'])}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="MT4 log file(s)")
    parser.add_argument("--json", dest="json_path", type=Path, help="write full JSON report")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    missing = [str(p) for p in args.paths if not p.is_file()]
    if missing:
        raise SystemExit("Missing log file(s): " + ", ".join(missing))

    observations = list(iter_observations(args.paths))
    report = build_report(observations)
    print_report(report)

    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        print(f"\nJSON: {args.json_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
