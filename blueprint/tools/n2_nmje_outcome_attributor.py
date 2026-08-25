#!/usr/bin/env python3
"""Attribute realized trade outcomes to NMJE/D1O validated-decision context.

Research/diagnostic only. Only exact DecisionID joins are allowed. D1O authority,
opportunity family and cycle metadata are carried through when present so the
new execution extension can be measured separately from legacy strategy paths.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


def load_correlation(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_outcomes(path: Path) -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    duplicates: list[dict] = []
    seen: set[str] = set()
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"decision_id", "net_profit"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise SystemExit("Outcome CSV missing column(s): " + ", ".join(sorted(missing)))
        for line_no, raw in enumerate(reader, 2):
            decision_id = (raw.get("decision_id") or "").strip()
            if not decision_id:
                raise SystemExit(f"Outcome CSV line {line_no}: empty decision_id")
            try:
                net_profit = float((raw.get("net_profit") or "").strip())
            except ValueError as exc:
                raise SystemExit(f"Outcome CSV line {line_no}: invalid net_profit") from exc
            row = dict(raw)
            row["decision_id"] = decision_id
            row["net_profit"] = net_profit
            row["_line_no"] = line_no
            if decision_id in seen:
                duplicates.append(row)
            seen.add(decision_id)
            rows.append(row)
    return rows, duplicates


def classify_profit(value: float, epsilon: float = 1e-9) -> str:
    if value > epsilon:
        return "WIN"
    if value < -epsilon:
        return "LOSS"
    return "BREAKEVEN"


def bucket_summary(rows: list[dict]) -> dict:
    profits = [float(r["net_profit"]) for r in rows]
    outcomes = Counter(classify_profit(x) for x in profits)
    decisive = outcomes["WIN"] + outcomes["LOSS"]
    return {
        "trades": len(rows),
        "wins": outcomes["WIN"],
        "losses": outcomes["LOSS"],
        "breakeven": outcomes["BREAKEVEN"],
        "win_rate_ex_be_pct": (outcomes["WIN"] / decisive * 100.0) if decisive else None,
        "net_profit": sum(profits),
        "avg_net_profit": (sum(profits) / len(profits)) if profits else None,
    }


def attribute(correlation: dict, outcomes: list[dict], duplicate_outcomes: list[dict]) -> dict:
    decisions_by_id: dict[str, dict] = {}
    duplicate_correlation_ids: list[str] = []
    for row in correlation.get("rows", []):
        decision = row.get("decision") or {}
        decision_id = decision.get("decision_id")
        if not decision_id:
            continue
        if decision_id in decisions_by_id:
            duplicate_correlation_ids.append(decision_id)
            continue
        decisions_by_id[decision_id] = row

    duplicate_outcome_ids = {row["decision_id"] for row in duplicate_outcomes}
    matched: list[dict] = []
    unmatched_outcomes: list[dict] = []
    matched_ids: set[str] = set()

    for outcome in outcomes:
        did = outcome["decision_id"]
        if did in duplicate_outcome_ids:
            continue
        correlated = decisions_by_id.get(did)
        if correlated is None:
            unmatched_outcomes.append(outcome)
            continue
        decision = correlated["decision"]
        enriched = {
            "decision_id": did,
            "pair": decision.get("pair"),
            "signal": decision.get("signal"),
            "direction": decision.get("direction"),
            "relation": decision.get("relation"),
            "parent": decision.get("parent"),
            "journey": decision.get("journey"),
            "authority": decision.get("authority") or "LEGACY_UNSPECIFIED",
            "opportunity_family": decision.get("opportunity_family") or "NONE",
            "opportunity_cycle": decision.get("opportunity_cycle") or "-",
            "match_mode": correlated.get("match_mode"),
            "net_profit": outcome["net_profit"],
            "outcome": classify_profit(outcome["net_profit"]),
            "ticket": outcome.get("ticket", ""),
            "close_time": outcome.get("close_time", ""),
        }
        matched.append(enriched)
        matched_ids.add(did)

    decisions_without_outcome = [
        {
            "decision_id": did,
            "pair": row["decision"].get("pair"),
            "signal": row["decision"].get("signal"),
            "relation": row["decision"].get("relation"),
            "authority": row["decision"].get("authority") or "LEGACY_UNSPECIFIED",
            "opportunity_family": row["decision"].get("opportunity_family") or "NONE",
        }
        for did, row in decisions_by_id.items() if did not in matched_ids
    ]

    by_relation: dict[str, list[dict]] = defaultdict(list)
    by_signal: dict[str, list[dict]] = defaultdict(list)
    by_relation_signal: dict[str, list[dict]] = defaultdict(list)
    by_authority: dict[str, list[dict]] = defaultdict(list)
    by_opportunity_family: dict[str, list[dict]] = defaultdict(list)
    by_opportunity_family_signal: dict[str, list[dict]] = defaultdict(list)

    for row in matched:
        by_relation[str(row["relation"])].append(row)
        by_signal[str(row["signal"])].append(row)
        by_relation_signal[f"{row['relation']}|{row['signal']}"] .append(row)
        by_authority[str(row["authority"])].append(row)
        by_opportunity_family[str(row["opportunity_family"])].append(row)
        by_opportunity_family_signal[f"{row['opportunity_family']}|{row['signal']}"] .append(row)

    return {
        "matched_outcomes": len(matched),
        "correlated_decisions": len(decisions_by_id),
        "outcome_rows": len(outcomes),
        "overall": bucket_summary(matched),
        "by_relation": {k: bucket_summary(v) for k, v in sorted(by_relation.items())},
        "by_signal": {k: bucket_summary(v) for k, v in sorted(by_signal.items())},
        "by_relation_signal": {k: bucket_summary(v) for k, v in sorted(by_relation_signal.items())},
        "by_authority": {k: bucket_summary(v) for k, v in sorted(by_authority.items())},
        "by_opportunity_family": {k: bucket_summary(v) for k, v in sorted(by_opportunity_family.items())},
        "by_opportunity_family_signal": {
            k: bucket_summary(v) for k, v in sorted(by_opportunity_family_signal.items())
        },
        "integrity": {
            "duplicate_outcome_rows": duplicate_outcomes,
            "duplicate_correlation_decision_ids": sorted(set(duplicate_correlation_ids)),
            "unmatched_outcomes": unmatched_outcomes,
            "decisions_without_outcome": decisions_without_outcome,
        },
        "rows": matched,
    }


def print_report(report: dict) -> None:
    print("N2/D1O OUTCOME ATTRIBUTION")
    print("==========================")
    print(f"Correlated decisions : {report['correlated_decisions']}")
    print(f"Outcome rows         : {report['outcome_rows']}")
    print(f"Matched outcomes     : {report['matched_outcomes']}")
    print()
    overall = report["overall"]
    print(
        "Overall: "
        f"trades={overall['trades']} wins={overall['wins']} "
        f"losses={overall['losses']} BE={overall['breakeven']} "
        f"net={overall['net_profit']:.2f}"
    )
    print()
    print("By D1 authority")
    for key, stats in report["by_authority"].items():
        wr = stats["win_rate_ex_be_pct"]
        wr_text = "n/a" if wr is None else f"{wr:.2f}%"
        print(f"  {key:18s} trades={stats['trades']:4d} winrate(ex-BE)={wr_text:>8s} net={stats['net_profit']:.2f}")
    print()
    print("By D1 opportunity family")
    for key, stats in report["by_opportunity_family"].items():
        wr = stats["win_rate_ex_be_pct"]
        wr_text = "n/a" if wr is None else f"{wr:.2f}%"
        print(f"  {key:18s} trades={stats['trades']:4d} winrate(ex-BE)={wr_text:>8s} net={stats['net_profit']:.2f}")
    print()
    integrity = report["integrity"]
    print("Integrity")
    print(f"  duplicate outcome rows          : {len(integrity['duplicate_outcome_rows'])}")
    print(f"  duplicate correlation DecisionID: {len(integrity['duplicate_correlation_decision_ids'])}")
    print(f"  unmatched outcomes              : {len(integrity['unmatched_outcomes'])}")
    print(f"  decisions without outcome       : {len(integrity['decisions_without_outcome'])}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("correlation_json", type=Path)
    parser.add_argument("outcomes_csv", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    correlation = load_correlation(args.correlation_json)
    outcomes, duplicates = load_outcomes(args.outcomes_csv)
    report = attribute(correlation, outcomes, duplicates)
    print_report(report)
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        print(f"\nJSON: {args.json_path}")
    if report["integrity"]["duplicate_outcome_rows"]:
        return 2
    if report["integrity"]["duplicate_correlation_decision_ids"]:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
