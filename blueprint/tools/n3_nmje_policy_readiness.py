#!/usr/bin/env python3
"""Evaluate N2 NMJE evidence for N3 strategy-review readiness.

This tool is diagnostic only. It never chooses or activates an execution policy,
never edits EA source, and never converts statistical differences into a trade
rule. `REVIEW_READY` means only that the evidence bundle is fit to be reviewed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

VALID_DATA_STATUSES = {
    "IDENTITY_INVALID",
    "PARTIAL_COVERAGE",
    "COMPLETE_OBSERVED_SAMPLE",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _bucket_snapshot(group: dict) -> dict:
    result: dict[str, dict] = {}
    for name, raw in sorted((group or {}).items()):
        raw = raw or {}
        interval = raw.get("win_rate_wilson_95")
        result[str(name)] = {
            "trades": int(raw.get("trades", 0) or 0),
            "decisive_trades": int(raw.get("decisive_trades", 0) or 0),
            "wins": int(raw.get("wins", 0) or 0),
            "losses": int(raw.get("losses", 0) or 0),
            "breakeven": int(raw.get("breakeven", 0) or 0),
            "win_rate_ex_be_pct": raw.get("win_rate_ex_be_pct"),
            "win_rate_wilson_95": interval,
            "net_profit": float(raw.get("net_profit", 0.0) or 0.0),
        }
    return result


def build_readiness(evidence: dict) -> dict:
    data_status = str(evidence.get("data_status") or "").strip()
    identity = evidence.get("identity_integrity") or {}
    coverage = evidence.get("coverage") or {}
    guardrails = evidence.get("guardrails") or {}

    identity_valid = bool(identity.get("valid_for_attribution", False))
    correlated = int(coverage.get("correlated_decisions", 0) or 0)
    matched = int(coverage.get("matched_outcomes", 0) or 0)
    coverage_pct = coverage.get("coverage_pct")
    interpretation = str(evidence.get("interpretation") or "")

    reasons: list[str] = []
    warnings: list[str] = []

    if data_status not in VALID_DATA_STATUSES:
        reasons.append("UNKNOWN_N2_DATA_STATUS")

    if not identity_valid or data_status == "IDENTITY_INVALID":
        readiness = "IDENTITY_BLOCKED"
        if not identity_valid:
            reasons.append("IDENTITY_NOT_VALID_FOR_ATTRIBUTION")
        if data_status == "IDENTITY_INVALID":
            reasons.append("N2_DATA_STATUS_IDENTITY_INVALID")
    elif data_status != "COMPLETE_OBSERVED_SAMPLE":
        readiness = "EVIDENCE_COLLECTION"
        reasons.append("N2_OBSERVED_SAMPLE_NOT_COMPLETE")
    elif correlated <= 0 or matched <= 0:
        readiness = "EVIDENCE_COLLECTION"
        reasons.append("NO_ATTRIBUTED_CLOSED_OUTCOME_SAMPLE")
    elif interpretation != "DESCRIPTIVE_RESEARCH_ONLY":
        readiness = "EVIDENCE_COLLECTION"
        reasons.append("N2_INTERPRETATION_BOUNDARY_MISSING")
    else:
        readiness = "REVIEW_READY"
        reasons.append("COMPLETE_OBSERVED_SAMPLE_WITH_VALID_IDENTITY")

    by_relation = _bucket_snapshot(evidence.get("by_relation") or {})
    by_signal = _bucket_snapshot(evidence.get("by_signal") or {})
    relation_with_trades = [k for k, v in by_relation.items() if v["trades"] > 0]
    relation_without_decisive = [k for k, v in by_relation.items() if v["trades"] > 0 and v["decisive_trades"] == 0]
    relation_wide_uncertainty = []
    for name, bucket in by_relation.items():
        interval = bucket.get("win_rate_wilson_95")
        if not interval:
            continue
        width = interval.get("width_pct")
        if width is not None and float(width) > 50.0:
            # Research warning only. This is not an activation threshold.
            relation_wide_uncertainty.append(name)

    if len(relation_with_trades) < 2:
        warnings.append("RELATION_DIVERSITY_LIMITED")
    if relation_without_decisive:
        warnings.append("RELATION_BUCKET_WITHOUT_DECISIVE_OUTCOMES")
    if relation_wide_uncertainty:
        warnings.append("RELATION_BUCKETS_HAVE_WIDE_UNCERTAINTY")
    if guardrails.get("nested_execution_gate_authorized") is True:
        warnings.append("N2_GUARDRAIL_INCONSISTENT_EXECUTION_AUTHORITY")
        if readiness == "REVIEW_READY":
            readiness = "EVIDENCE_COLLECTION"
            reasons.append("N2_EXECUTION_GUARDRAIL_MUST_REMAIN_FALSE")

    return {
        "n3_phase": "EXECUTION_INTELLIGENCE_STAGING",
        "readiness": readiness,
        "n2_data_status": data_status,
        "n2_interpretation": interpretation,
        "identity_valid": identity_valid,
        "coverage": {
            "correlated_decisions": correlated,
            "matched_outcomes": matched,
            "coverage_pct": coverage_pct,
        },
        "observed_relation_buckets": by_relation,
        "observed_signal_buckets": by_signal,
        "relation_buckets_with_trades": relation_with_trades,
        "relation_buckets_without_decisive_outcomes": relation_without_decisive,
        "relation_buckets_wide_uncertainty": relation_wide_uncertainty,
        "reasons": reasons,
        "warnings": warnings,
        "execution_policy": "NONE",
        "automatic_policy_authorized": False,
        "source_modification_authorized": False,
        "activation_authorized": False,
        "requires_real_forward_evidence_for_strategy_claim": True,
        "requires_explicit_strategy_approval_for_activation": True,
        "interpretation": "REVIEW_READINESS_ONLY_NOT_A_TRADING_EDGE",
    }


def print_report(report: dict) -> None:
    print("N3 NMJE POLICY READINESS")
    print("========================")
    print(f"Readiness             : {report['readiness']}")
    print(f"N2 data status        : {report['n2_data_status']}")
    print(f"Identity valid        : {'YES' if report['identity_valid'] else 'NO'}")
    cov = report["coverage"]
    pct = cov["coverage_pct"]
    pct_text = "n/a" if pct is None else f"{float(pct):.2f}%"
    print(f"Outcome coverage      : {cov['matched_outcomes']}/{cov['correlated_decisions']} ({pct_text})")
    print(f"Relation buckets      : {len(report['relation_buckets_with_trades'])}")
    print(f"Execution policy      : {report['execution_policy']}")
    print("Activation authorized : NO")
    if report["warnings"]:
        print("Warnings              : " + ", ".join(report["warnings"]))
    print("Interpretation        : REVIEW READINESS ONLY; NO AUTOMATIC POLICY")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence_json", type=Path)
    parser.add_argument("--json", dest="json_path", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.evidence_json.is_file():
        raise SystemExit(f"Missing N2 evidence: {args.evidence_json}")
    report = build_readiness(load_json(args.evidence_json))
    print_report(report)
    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        print(f"\nJSON: {args.json_path}")
    return 2 if report["readiness"] == "IDENTITY_BLOCKED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
