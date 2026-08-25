#!/usr/bin/env python3
"""Analyze D1 Opportunity Journey runtime logs.

Research/diagnostic only. Counts unique D1 opportunity cycles, watch-only eCSD
observations, validated decisions attributed to opportunity families/cycles and
LTF clusters, and basic identity anomalies. It never changes EA strategy or
execution state.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

D1_OPP_RE = re.compile(
    r"\[D1-OPP\]\s+(?P<pair>\S+)\s+"
    r"F=(?P<family>\S+)\s+DIR=(?P<direction>[BS-])\s+"
    r"ACTIVE=(?P<active>[YN])\s+TACT=(?P<tactical>[YN])\s+"
    r"SRC=(?P<source>\d{4}\.\d{2}\.\d{2}\s+\d{2}:\d{2}(?::\d{2})?)\s+"
    r"ACT=(?P<activation>\d{4}\.\d{2}\.\d{2}\s+\d{2}:\d{2}(?::\d{2})?)\s+"
    r"CYCLE=(?P<cycle>\S+)\s+R=(?P<reason>.*)$"
)

WATCH_RE = re.compile(
    r"\[D1-OPP-WATCH\]\s+(?P<pair>\S+)\s+eCSD=(?P<direction>[BS])\s+Action=WATCH_ONLY"
)

DEC_RE = re.compile(
    r"\[N2-NMJE-DEC\]\s+(?P<pair>\S+).*?\sAUTH=(?P<authority>\S+)\s+"
    r"OFAM=(?P<family>\S+)\s+OC=(?P<cycle>\S+)"
    r"(?:\s+LTF=(?P<ltf_cluster>\S+))?"
    r"(?:\s+OSH=(?P<opportunity_sequence_hash>\S+))?"
)


@dataclass(frozen=True)
class OpportunityRecord:
    file: str
    line_no: int
    pair: str
    family: str
    direction: str
    active: str
    tactical: str
    source: str
    activation: str
    cycle: str
    reason: str


@dataclass(frozen=True)
class WatchRecord:
    file: str
    line_no: int
    pair: str
    direction: str


@dataclass(frozen=True)
class DecisionRecord:
    file: str
    line_no: int
    pair: str
    authority: str
    family: str
    cycle: str
    ltf_cluster: str = ""
    opportunity_sequence_hash: str = ""


def parse(paths: Iterable[Path]) -> tuple[list[OpportunityRecord], list[WatchRecord], list[DecisionRecord]]:
    opportunities: list[OpportunityRecord] = []
    watches: list[WatchRecord] = []
    decisions: list[DecisionRecord] = []
    for path in paths:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line_no, line in enumerate(handle, 1):
                m = D1_OPP_RE.search(line)
                if m:
                    opportunities.append(OpportunityRecord(str(path), line_no, **m.groupdict()))
                    continue
                m = WATCH_RE.search(line)
                if m:
                    watches.append(WatchRecord(str(path), line_no, **m.groupdict()))
                    continue
                m = DEC_RE.search(line)
                if m:
                    fields = m.groupdict()
                    fields["ltf_cluster"] = fields.get("ltf_cluster") or ""
                    fields["opportunity_sequence_hash"] = fields.get("opportunity_sequence_hash") or ""
                    decisions.append(DecisionRecord(str(path), line_no, **fields))
    return opportunities, watches, decisions


def analyze(opportunities: list[OpportunityRecord], watches: list[WatchRecord], decisions: list[DecisionRecord]) -> dict:
    cycle_identity: dict[tuple[str, str], tuple[str, str]] = {}
    cycle_conflicts: list[dict] = []
    active_cycles: set[tuple[str, str]] = set()
    family_cycles: defaultdict[str, set[tuple[str, str]]] = defaultdict(set)

    for row in opportunities:
        if row.cycle in ("", "-"):
            continue
        key = (row.pair, row.cycle)
        identity = (row.family, row.direction)
        previous = cycle_identity.get(key)
        if previous is not None and previous != identity:
            cycle_conflicts.append({
                "pair": row.pair,
                "cycle": row.cycle,
                "first": {"family": previous[0], "direction": previous[1]},
                "later": {"family": row.family, "direction": row.direction},
                "line_no": row.line_no,
            })
        else:
            cycle_identity[key] = identity
        if row.active == "Y":
            active_cycles.add(key)
            family_cycles[row.family].add(key)

    opp_decisions = [d for d in decisions if d.authority == "OPP"]
    decisions_by_family = Counter(d.family for d in opp_decisions)
    decisions_by_ltf_cluster = Counter((d.ltf_cluster or "UNKNOWN") for d in opp_decisions)
    decisions_by_family_ltf = Counter(
        f"{d.family}|{d.ltf_cluster or 'UNKNOWN'}" for d in opp_decisions
    )
    decisions_by_cycle = Counter((d.pair, d.cycle) for d in opp_decisions if d.cycle not in ("", "-"))
    unknown_cycle_decisions = [
        asdict(d) for d in opp_decisions
        if d.cycle in ("", "-") or (d.pair, d.cycle) not in cycle_identity
    ]
    family_mismatch_decisions = []
    for d in opp_decisions:
        key = (d.pair, d.cycle)
        identity = cycle_identity.get(key)
        if identity is not None and d.family != identity[0]:
            family_mismatch_decisions.append({
                "decision": asdict(d),
                "cycle_family": identity[0],
                "cycle_direction": identity[1],
            })

    sequence_hash_conflicts = []
    sequence_owner: dict[tuple[str, str], tuple[str, str]] = {}
    for d in opp_decisions:
        if d.opportunity_sequence_hash in ("", "-"):
            continue
        key = (d.pair, d.opportunity_sequence_hash)
        identity = (d.cycle, d.ltf_cluster)
        prior = sequence_owner.get(key)
        if prior is not None and prior != identity:
            sequence_hash_conflicts.append({
                "pair": d.pair,
                "sequence_hash": d.opportunity_sequence_hash,
                "first": {"cycle": prior[0], "ltf_cluster": prior[1]},
                "later": {"cycle": d.cycle, "ltf_cluster": d.ltf_cluster},
                "line_no": d.line_no,
            })
        else:
            sequence_owner[key] = identity

    cycles_without_decision = [
        {"pair": pair, "cycle": cycle, "family": cycle_identity[(pair, cycle)][0]}
        for pair, cycle in sorted(active_cycles)
        if decisions_by_cycle[(pair, cycle)] == 0
    ]

    return {
        "opportunity_log_rows": len(opportunities),
        "watch_only_ecsd_rows": len(watches),
        "unique_active_cycles": len(active_cycles),
        "active_cycles_by_family": {k: len(v) for k, v in sorted(family_cycles.items())},
        "watch_only_ecsd_by_direction": dict(Counter(w.direction for w in watches)),
        "opportunity_validated_decisions": len(opp_decisions),
        "decisions_by_opportunity_family": dict(sorted(decisions_by_family.items())),
        "decisions_by_ltf_cluster": dict(sorted(decisions_by_ltf_cluster.items())),
        "decisions_by_family_ltf_cluster": dict(sorted(decisions_by_family_ltf.items())),
        "decisions_by_cycle": {
            f"{pair}|{cycle}": count for (pair, cycle), count in sorted(decisions_by_cycle.items())
        },
        "cycles_without_validated_decision": cycles_without_decision,
        "integrity": {
            "cycle_identity_conflicts": cycle_conflicts,
            "unknown_cycle_decisions": unknown_cycle_decisions,
            "family_mismatch_decisions": family_mismatch_decisions,
            "sequence_hash_conflicts": sequence_hash_conflicts,
        },
    }


def print_report(report: dict) -> None:
    print("D1O OPPORTUNITY LOG ANALYSIS")
    print("============================")
    print(f"Opportunity rows           : {report['opportunity_log_rows']}")
    print(f"Unique active cycles       : {report['unique_active_cycles']}")
    print(f"Watch-only eCSD rows       : {report['watch_only_ecsd_rows']}")
    print(f"Opportunity decisions      : {report['opportunity_validated_decisions']}")
    print()
    print("Active cycles by family")
    for family, count in report["active_cycles_by_family"].items():
        print(f"  {family:12s} {count}")
    print()
    print("Validated decisions by LTF cluster")
    for cluster, count in report["decisions_by_ltf_cluster"].items():
        print(f"  {cluster:12s} {count}")
    print()
    integ = report["integrity"]
    print("Integrity")
    print(f"  cycle identity conflicts : {len(integ['cycle_identity_conflicts'])}")
    print(f"  unknown-cycle decisions  : {len(integ['unknown_cycle_decisions'])}")
    print(f"  family mismatches        : {len(integ['family_mismatch_decisions'])}")
    print(f"  sequence hash conflicts  : {len(integ['sequence_hash_conflicts'])}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    args = parser.parse_args()
    missing = [str(p) for p in args.paths if not p.is_file()]
    if missing:
        raise SystemExit("Missing log file(s): " + ", ".join(missing))
    opportunities, watches, decisions = parse(args.paths)
    report = analyze(opportunities, watches, decisions)
    print_report(report)
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        print(f"\nJSON: {args.json_path}")
    integ = report["integrity"]
    if integ["cycle_identity_conflicts"]:
        return 2
    if integ["family_mismatch_decisions"]:
        return 3
    if integ["sequence_hash_conflicts"]:
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
