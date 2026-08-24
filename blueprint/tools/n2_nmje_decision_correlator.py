#!/usr/bin/env python3
"""Correlate N1 NMJE journey observations with N2 validated-decision shadow tags.

Research/diagnostic only. This tool never changes EA source or trading logic.

Usage:
  python blueprint/tools/n2_nmje_decision_correlator.py path/to/log.txt
  python blueprint/tools/n2_nmje_decision_correlator.py logs/*.log --json out.json
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

N1_RE = re.compile(
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

N2_RE = re.compile(
    r"\[N2-NMJE-DEC\]\s+"
    r"(?P<pair>\S+)\s+"
    r"SIG=(?P<signal>\S+)\s+"
    r"DIR=(?P<direction>\S+)\s+"
    r"REL=(?P<relation>\S+)\s+"
    r"P=(?P<parent>\S+)\s+"
    r"J=(?P<journey>\S+)\s+"
    r"DID=(?P<decision_id>\S+)"
)


@dataclass(frozen=True)
class JourneyObservation:
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


@dataclass(frozen=True)
class DecisionShadow:
    file: str
    line_no: int
    pair: str
    signal: str
    direction: str
    relation: str
    parent: str
    journey: str
    decision_id: str


def iter_records(paths: Iterable[Path]) -> tuple[list[JourneyObservation], list[DecisionShadow]]:
    observations: list[JourneyObservation] = []
    decisions: list[DecisionShadow] = []

    for path in paths:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line_no, line in enumerate(handle, 1):
                n1 = N1_RE.search(line)
                if n1:
                    observations.append(
                        JourneyObservation(file=str(path), line_no=line_no, **n1.groupdict())
                    )
                    continue

                n2 = N2_RE.search(line)
                if n2:
                    decisions.append(
                        DecisionShadow(file=str(path), line_no=line_no, **n2.groupdict())
                    )

    return observations, decisions


def correlate(
    observations: list[JourneyObservation], decisions: list[DecisionShadow]
) -> dict:
    by_pair: dict[str, list[JourneyObservation]] = defaultdict(list)
    for obs in observations:
        by_pair[obs.pair].append(obs)

    rows: list[dict] = []
    orphan_decisions: list[dict] = []
    context_mismatches: list[dict] = []
    duplicate_decision_ids: list[dict] = []
    seen_decision_ids: set[str] = set()

    for dec in decisions:
        if dec.decision_id in seen_decision_ids:
            duplicate_decision_ids.append(asdict(dec))
        seen_decision_ids.add(dec.decision_id)

        previous = [
            obs
            for obs in by_pair.get(dec.pair, [])
            if obs.file == dec.file and obs.line_no < dec.line_no
        ]

        exact = [
            obs
            for obs in previous
            if dec.journey != "-" and obs.journey == dec.journey
        ]

        context = None
        match_mode = "ORPHAN"
        if exact:
            context = exact[-1]
            match_mode = "EXACT_JOURNEY"
        elif dec.journey == "-" and previous:
            # No journey identity exists on the decision, so only a same-pair
            # previous observation may be shown as weak diagnostic context.
            context = previous[-1]
            match_mode = "PAIR_FALLBACK_NO_JOURNEY"

        row = {
            "decision": asdict(dec),
            "match_mode": match_mode,
            "context": asdict(context) if context else None,
        }
        rows.append(row)

        if context is None:
            orphan_decisions.append(asdict(dec))
            continue

        mismatches = {}
        for field in ("relation", "parent", "journey"):
            decision_value = getattr(dec, field)
            context_value = getattr(context, field)
            if decision_value != context_value:
                mismatches[field] = {
                    "decision": decision_value,
                    "context": context_value,
                }

        if mismatches:
            context_mismatches.append(
                {
                    "decision_id": dec.decision_id,
                    "pair": dec.pair,
                    "match_mode": match_mode,
                    "mismatches": mismatches,
                }
            )

    signal_names = sorted({d.signal for d in decisions})
    relation_names = sorted({d.relation for d in decisions})

    return {
        "n1_observation_count": len(observations),
        "n2_decision_count": len(decisions),
        "unique_decision_ids": len({d.decision_id for d in decisions}),
        "unique_decision_journeys": len({d.journey for d in decisions if d.journey != "-"}),
        "decision_relation_counts": dict(Counter(d.relation for d in decisions)),
        "decision_signal_counts": dict(Counter(d.signal for d in decisions)),
        "decision_direction_counts": dict(Counter(d.direction for d in decisions)),
        "decision_relation_by_signal": {
            signal: dict(Counter(d.relation for d in decisions if d.signal == signal))
            for signal in signal_names
        },
        "decision_signal_by_relation": {
            relation: dict(Counter(d.signal for d in decisions if d.relation == relation))
            for relation in relation_names
        },
        "exact_journey_matches": sum(
            1 for row in rows if row["match_mode"] == "EXACT_JOURNEY"
        ),
        "pair_fallback_matches": sum(
            1 for row in rows if row["match_mode"] == "PAIR_FALLBACK_NO_JOURNEY"
        ),
        "orphan_decisions": orphan_decisions,
        "context_mismatches": context_mismatches,
        "duplicate_decision_ids": duplicate_decision_ids,
        "rows": rows,
    }


def print_report(report: dict) -> None:
    print("N2 NMJE DECISION CORRELATION")
    print("============================")
    print(f"N1 observations       : {report['n1_observation_count']}")
    print(f"N2 validated decisions: {report['n2_decision_count']}")
    print(f"Unique DecisionIDs    : {report['unique_decision_ids']}")
    print(f"Decision journeys     : {report['unique_decision_journeys']}")
    print()

    print("Validated decisions by nested relation")
    for key, value in sorted(report["decision_relation_counts"].items()):
        print(f"  {key:12s} {value}")
    print()

    print("Validated decisions by signal")
    for key, value in sorted(report["decision_signal_counts"].items()):
        print(f"  {key:22s} {value}")
    print()

    print("Relation by signal")
    for signal, values in report["decision_relation_by_signal"].items():
        summary = ", ".join(f"{k}={v}" for k, v in sorted(values.items()))
        print(f"  {signal}: {summary}")
    print()

    print("Correlation integrity")
    print(f"  exact JourneyID matches : {report['exact_journey_matches']}")
    print(f"  pair fallback matches   : {report['pair_fallback_matches']}")
    print(f"  orphan decisions        : {len(report['orphan_decisions'])}")
    print(f"  context mismatches      : {len(report['context_mismatches'])}")
    print(f"  duplicate DecisionIDs   : {len(report['duplicate_decision_ids'])}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="MT4 Experts/Journal log file(s)")
    parser.add_argument("--json", dest="json_path", type=Path, help="write full JSON report")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    missing = [str(path) for path in args.paths if not path.is_file()]
    if missing:
        raise SystemExit("Missing log file(s): " + ", ".join(missing))

    observations, decisions = iter_records(args.paths)
    report = correlate(observations, decisions)
    print_report(report)

    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        print(f"\nJSON: {args.json_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
