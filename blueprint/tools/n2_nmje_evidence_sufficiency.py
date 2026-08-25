#!/usr/bin/env python3
"""Summarize N2 NMJE outcome evidence without making trading claims.

Research/diagnostic only. This tool never changes EA source or trading logic.

Usage:
  python blueprint/tools/n2_nmje_evidence_sufficiency.py outcome_report.json
  python blueprint/tools/n2_nmje_evidence_sufficiency.py outcome_report.json --json evidence.json

The input is the JSON emitted by n2_nmje_outcome_attributor.py.
No minimum sample size is invented here. Instead the report exposes sample counts,
coverage, identity integrity and a Wilson 95% interval for decisive win rate so
future strategy decisions can be based on visible evidence rather than a point
estimate alone.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

Z_95 = 1.959963984540054


def load_report(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def wilson_interval(wins: int, losses: int, z: float = Z_95) -> dict | None:
    n = wins + losses
    if n <= 0:
        return None
    p = wins / n
    z2 = z * z
    denom = 1.0 + z2 / n
    center = (p + z2 / (2.0 * n)) / denom
    half = z * math.sqrt((p * (1.0 - p) + z2 / (4.0 * n)) / n) / denom
    low = max(0.0, center - half)
    high = min(1.0, center + half)
    return {
        "low_pct": low * 100.0,
        "high_pct": high * 100.0,
        "width_pct": (high - low) * 100.0,
    }


def summarize_bucket(stats: dict) -> dict:
    trades = int(stats.get("trades", 0) or 0)
    wins = int(stats.get("wins", 0) or 0)
    losses = int(stats.get("losses", 0) or 0)
    breakeven = int(stats.get("breakeven", 0) or 0)
    decisive = wins + losses
    win_rate = (wins / decisive * 100.0) if decisive else None
    return {
        "trades": trades,
        "decisive_trades": decisive,
        "wins": wins,
        "losses": losses,
        "breakeven": breakeven,
        "win_rate_ex_be_pct": win_rate,
        "win_rate_wilson_95": wilson_interval(wins, losses),
        "net_profit": float(stats.get("net_profit", 0.0) or 0.0),
        "avg_net_profit": stats.get("avg_net_profit"),
    }


def summarize_group(group: dict) -> dict:
    return {str(key): summarize_bucket(value or {}) for key, value in sorted(group.items())}


def build_evidence(report: dict) -> dict:
    integrity = report.get("integrity") or {}
    duplicate_outcomes = integrity.get("duplicate_outcome_rows") or []
    duplicate_decisions = integrity.get("duplicate_correlation_decision_ids") or []
    unmatched_outcomes = integrity.get("unmatched_outcomes") or []
    decisions_without_outcome = integrity.get("decisions_without_outcome") or []

    correlated = int(report.get("correlated_decisions", 0) or 0)
    matched = int(report.get("matched_outcomes", 0) or 0)
    coverage_pct = (matched / correlated * 100.0) if correlated else None

    if duplicate_outcomes or duplicate_decisions:
        data_status = "IDENTITY_INVALID"
    elif unmatched_outcomes or decisions_without_outcome:
        data_status = "PARTIAL_COVERAGE"
    else:
        data_status = "COMPLETE_OBSERVED_SAMPLE"

    return {
        "data_status": data_status,
        "interpretation": "DESCRIPTIVE_RESEARCH_ONLY",
        "coverage": {
            "correlated_decisions": correlated,
            "matched_outcomes": matched,
            "coverage_pct": coverage_pct,
            "unmatched_outcomes": len(unmatched_outcomes),
            "decisions_without_outcome": len(decisions_without_outcome),
        },
        "identity_integrity": {
            "duplicate_outcome_rows": len(duplicate_outcomes),
            "duplicate_correlation_decision_ids": len(duplicate_decisions),
            "valid_for_attribution": not (duplicate_outcomes or duplicate_decisions),
        },
        "overall": summarize_bucket(report.get("overall") or {}),
        "by_relation": summarize_group(report.get("by_relation") or {}),
        "by_signal": summarize_group(report.get("by_signal") or {}),
        "by_relation_signal": summarize_group(report.get("by_relation_signal") or {}),
        "guardrails": {
            "minimum_sample_size_invented": False,
            "nested_execution_gate_authorized": False,
            "win_rate_edge_claimed": False,
            "purpose": "Expose uncertainty and data quality before any future strategy decision.",
        },
    }


def print_bucket(name: str, bucket: dict) -> None:
    wr = bucket["win_rate_ex_be_pct"]
    ci = bucket["win_rate_wilson_95"]
    wr_text = "n/a" if wr is None else f"{wr:.2f}%"
    ci_text = "n/a" if ci is None else f"{ci['low_pct']:.2f}%..{ci['high_pct']:.2f}%"
    print(
        f"{name}: trades={bucket['trades']} decisive={bucket['decisive_trades']} "
        f"WR(ex-BE)={wr_text} Wilson95={ci_text} net={bucket['net_profit']:.2f}"
    )


def print_report(evidence: dict) -> None:
    print("N2 NMJE EVIDENCE SUFFICIENCY")
    print("============================")
    print(f"Data status : {evidence['data_status']}")
    cov = evidence["coverage"]
    cov_text = "n/a" if cov["coverage_pct"] is None else f"{cov['coverage_pct']:.2f}%"
    print(
        f"Coverage    : {cov['matched_outcomes']}/{cov['correlated_decisions']} "
        f"({cov_text})"
    )
    ident = evidence["identity_integrity"]
    print(f"Identity OK : {'YES' if ident['valid_for_attribution'] else 'NO'}")
    print()
    print_bucket("Overall", evidence["overall"])
    print()
    print("By nested relation")
    for relation, bucket in evidence["by_relation"].items():
        print_bucket(f"  {relation}", bucket)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outcome_report_json", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    evidence = build_evidence(load_report(args.outcome_report_json))
    print_report(evidence)
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8")
        print(f"\nJSON: {args.json_path}")
    return 2 if evidence["data_status"] == "IDENTITY_INVALID" else 0


if __name__ == "__main__":
    raise SystemExit(main())
