#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "blueprint" / "tools" / "n3_nmje_policy_readiness.py"
spec = importlib.util.spec_from_file_location("n3_nmje_policy_readiness", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)


def bucket(trades: int, wins: int, losses: int, be: int = 0, width: float | None = 20.0) -> dict:
    decisive = wins + losses
    interval = None if decisive == 0 or width is None else {
        "low_pct": 30.0,
        "high_pct": 30.0 + width,
        "width_pct": width,
    }
    return {
        "trades": trades,
        "decisive_trades": decisive,
        "wins": wins,
        "losses": losses,
        "breakeven": be,
        "win_rate_ex_be_pct": (wins / decisive * 100.0) if decisive else None,
        "win_rate_wilson_95": interval,
        "net_profit": 1.0,
    }


base = {
    "data_status": "COMPLETE_OBSERVED_SAMPLE",
    "interpretation": "DESCRIPTIVE_RESEARCH_ONLY",
    "coverage": {
        "correlated_decisions": 20,
        "matched_outcomes": 20,
        "coverage_pct": 100.0,
        "unmatched_outcomes": 0,
        "decisions_without_outcome": 0,
    },
    "identity_integrity": {
        "duplicate_outcome_rows": 0,
        "duplicate_correlation_decision_ids": 0,
        "valid_for_attribution": True,
    },
    "by_relation": {
        "ALIGNED": bucket(10, 6, 4),
        "CONFLICT": bucket(10, 4, 6),
    },
    "by_signal": {
        "SIGNAL_RE_ENTRY": bucket(20, 10, 10),
    },
    "guardrails": {
        "minimum_sample_size_invented": False,
        "nested_execution_gate_authorized": False,
        "win_rate_edge_claimed": False,
    },
}

# Complete, identity-valid evidence may become REVIEW_READY, but never active.
ready = mod.build_readiness(base)
assert ready["readiness"] == "REVIEW_READY", ready
assert ready["execution_policy"] == "NONE", ready
assert ready["automatic_policy_authorized"] is False, ready
assert ready["source_modification_authorized"] is False, ready
assert ready["activation_authorized"] is False, ready
assert ready["requires_explicit_strategy_approval_for_activation"] is True, ready

# Invalid identity must fail closed regardless of apparent performance.
invalid = dict(base)
invalid["identity_integrity"] = dict(base["identity_integrity"])
invalid["identity_integrity"]["valid_for_attribution"] = False
invalid["data_status"] = "IDENTITY_INVALID"
blocked = mod.build_readiness(invalid)
assert blocked["readiness"] == "IDENTITY_BLOCKED", blocked
assert blocked["activation_authorized"] is False, blocked

# Partial coverage remains evidence collection.
partial = dict(base)
partial["data_status"] = "PARTIAL_COVERAGE"
partial["coverage"] = dict(base["coverage"])
partial["coverage"]["matched_outcomes"] = 12
partial["coverage"]["coverage_pct"] = 60.0
collecting = mod.build_readiness(partial)
assert collecting["readiness"] == "EVIDENCE_COLLECTION", collecting
assert collecting["execution_policy"] == "NONE", collecting

# No attributed closed outcomes cannot become review-ready even if status is malformed as complete.
empty = dict(base)
empty["coverage"] = dict(base["coverage"])
empty["coverage"]["correlated_decisions"] = 0
empty["coverage"]["matched_outcomes"] = 0
empty["coverage"]["coverage_pct"] = None
empty_report = mod.build_readiness(empty)
assert empty_report["readiness"] == "EVIDENCE_COLLECTION", empty_report

# Missing descriptive-only boundary must fail safe.
wrong_interp = dict(base)
wrong_interp["interpretation"] = "EXECUTION_READY"
wrong_report = mod.build_readiness(wrong_interp)
assert wrong_report["readiness"] == "EVIDENCE_COLLECTION", wrong_report
assert wrong_report["activation_authorized"] is False, wrong_report

# Even statistically dramatic synthetic data can only be REVIEW_READY.
strong = dict(base)
strong["by_relation"] = {
    "ALIGNED": bucket(100, 95, 5, width=8.0),
    "CONFLICT": bucket(100, 5, 95, width=8.0),
}
strong_report = mod.build_readiness(strong)
assert strong_report["readiness"] == "REVIEW_READY", strong_report
assert strong_report["automatic_policy_authorized"] is False, strong_report
assert strong_report["activation_authorized"] is False, strong_report
assert strong_report["source_modification_authorized"] is False, strong_report

# Wide uncertainty is visible as warning, never converted into a hidden hard gate.
wide = dict(base)
wide["by_relation"] = {
    "ALIGNED": bucket(2, 1, 1, width=80.0),
    "CONFLICT": bucket(2, 1, 1, width=80.0),
}
wide_report = mod.build_readiness(wide)
assert wide_report["readiness"] == "REVIEW_READY", wide_report
assert "RELATION_BUCKETS_HAVE_WIDE_UNCERTAINTY" in wide_report["warnings"], wide_report
assert wide_report["activation_authorized"] is False, wide_report

print("N3 NMJE policy-readiness activation-firewall self-test PASS")
