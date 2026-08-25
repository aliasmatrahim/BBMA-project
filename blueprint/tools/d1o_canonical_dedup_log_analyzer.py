#!/usr/bin/env python3
"""Analyze D1O-07 canonical LTF dedup telemetry.

Diagnostic only. D1 cycle/family are attribution metadata. Reuse of one
execution sequence hash across D1 attribution changes is therefore expected
when the fresh lower-timeframe Re-Entry identity is unchanged.
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
DEC_RE = re.compile(
    r"\[N2-NMJE-DEC\]\s+(?P<pair>\S+).*?\sDIR=(?P<direction>[BS-]).*?\sAUTH=(?P<authority>\S+)\s+"
    r"OFAM=(?P<family>\S+)\s+OC=(?P<cycle>\S+)"
    r"(?:\s+LTF=(?P<ltf_cluster>\S+))?"
    r"(?:\s+OSH=(?P<sequence_hash>\S+))?"
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
class DecisionRecord:
    file: str
    line_no: int
    pair: str
    direction: str
    authority: str
    family: str
    cycle: str
    ltf_cluster: str = ""
    sequence_hash: str = ""

def parse(paths: Iterable[Path]) -> tuple[list[OpportunityRecord], list[DecisionRecord]]:
    opportunities: list[OpportunityRecord] = []
    decisions: list[DecisionRecord] = []
    for path in paths:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line_no, line in enumerate(handle, 1):
                m = D1_OPP_RE.search(line)
                if m:
                    opportunities.append(OpportunityRecord(str(path), line_no, **m.groupdict()))
                    continue
                m = DEC_RE.search(line)
                if m:
                    fields = m.groupdict()
                    fields["ltf_cluster"] = fields.get("ltf_cluster") or ""
                    fields["sequence_hash"] = fields.get("sequence_hash") or ""
                    decisions.append(DecisionRecord(str(path), line_no, **fields))
    return opportunities, decisions

def analyze(opportunities: list[OpportunityRecord], decisions: list[DecisionRecord]) -> dict:
    cycle_identity: dict[tuple[str, str], tuple[str, str]] = {}
    cycle_conflicts: list[dict] = []
    for row in opportunities:
        if row.cycle in ("", "-"):
            continue
        key = (row.pair, row.cycle)
        identity = (row.family, row.direction)
        prior = cycle_identity.get(key)
        if prior is not None and prior != identity:
            cycle_conflicts.append({"pair": row.pair, "cycle": row.cycle,
                                    "first": prior, "later": identity, "line_no": row.line_no})
        else:
            cycle_identity[key] = identity

    opp = [d for d in decisions if d.authority == "OPP"]
    missing_hash = [asdict(d) for d in opp if d.sequence_hash in ("", "-")]
    unknown_cycle = [asdict(d) for d in opp
                     if d.cycle in ("", "-") or (d.pair, d.cycle) not in cycle_identity]
    family_mismatch = []
    for d in opp:
        ident = cycle_identity.get((d.pair, d.cycle))
        if ident is not None and d.family != ident[0]:
            family_mismatch.append({"decision": asdict(d), "cycle_family": ident[0]})

    by_hash: defaultdict[tuple[str, str], list[DecisionRecord]] = defaultdict(list)
    for d in opp:
        if d.sequence_hash not in ("", "-"):
            by_hash[(d.pair, d.sequence_hash)].append(d)

    direction_conflicts: list[dict] = []
    cross_attribution_reuse: list[dict] = []
    for (pair, seq), rows in sorted(by_hash.items()):
        directions = sorted({r.direction for r in rows})
        attributions = sorted({(r.family, r.cycle) for r in rows})
        clusters = sorted({r.ltf_cluster or "UNKNOWN" for r in rows})
        if len(directions) > 1:
            direction_conflicts.append({"pair": pair, "sequence_hash": seq,
                                        "directions": directions,
                                        "attributions": attributions,
                                        "ltf_clusters": clusters})
        if len(attributions) > 1:
            cross_attribution_reuse.append({"pair": pair, "sequence_hash": seq,
                                            "attributions": attributions,
                                            "ltf_clusters": clusters,
                                            "classification": "EXPECTED_IF_LTF_IDENTITY_UNCHANGED"})

    return {
        "opportunity_rows": len(opportunities),
        "opportunity_decisions": len(opp),
        "decisions_by_ltf_cluster": dict(sorted(Counter(d.ltf_cluster or "UNKNOWN" for d in opp).items())),
        "unique_execution_hashes": len(by_hash),
        "cross_d1_attribution_hash_reuse": cross_attribution_reuse,
        "integrity": {
            "cycle_identity_conflicts": cycle_conflicts,
            "unknown_cycle_decisions": unknown_cycle,
            "family_mismatch_decisions": family_mismatch,
            "missing_sequence_hash_decisions": missing_hash,
            "sequence_hash_direction_conflicts": direction_conflicts,
        },
    }

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--json", dest="json_path", type=Path)
    args = ap.parse_args()
    missing = [str(p) for p in args.paths if not p.is_file()]
    if missing:
        raise SystemExit("Missing log file(s): " + ", ".join(missing))
    opportunities, decisions = parse(args.paths)
    report = analyze(opportunities, decisions)
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    integ = report["integrity"]
    fatal = (integ["cycle_identity_conflicts"] or integ["family_mismatch_decisions"] or
             integ["missing_sequence_hash_decisions"] or integ["sequence_hash_direction_conflicts"])
    return 2 if fatal else 0

if __name__ == "__main__":
    raise SystemExit(main())
