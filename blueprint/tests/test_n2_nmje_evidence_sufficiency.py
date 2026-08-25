#!/usr/bin/env python3
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "blueprint" / "tools" / "n2_nmje_evidence_sufficiency.py"
spec = importlib.util.spec_from_file_location("n2_nmje_evidence_sufficiency", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)

report = {
    "correlated_decisions": 4,
    "matched_outcomes": 3,
    "overall": {
        "trades": 3,
        "wins": 1,
        "losses": 1,
        "breakeven": 1,
        "win_rate_ex_be_pct": 50.0,
        "net_profit": 6.0,
        "avg_net_profit": 2.0,
    },
    "by_relation": {
        "ALIGNED": {"trades": 1, "wins": 0, "losses": 1, "breakeven": 0, "net_profit": -4.0, "avg_net_profit": -4.0},
        "SUPPORTING": {"trades": 1, "wins": 1, "losses": 0, "breakeven": 0, "net_profit": 10.0, "avg_net_profit": 10.0},
        "CONFLICT": {"trades": 1, "wins": 0, "losses": 0, "breakeven": 1, "net_profit": 0.0, "avg_net_profit": 0.0},
    },
    "by_signal": {},
    "by_relation_signal": {},
    "integrity": {
        "duplicate_outcome_rows": [],
        "duplicate_correlation_decision_ids": [],
        "unmatched_outcomes": [{"decision_id": "UNKNOWN"}],
        "decisions_without_outcome": [{"decision_id": "D4"}],
    },
}

evidence = mod.build_evidence(report)
assert evidence["data_status"] == "PARTIAL_COVERAGE", evidence
assert evidence["coverage"]["coverage_pct"] == 75.0, evidence
assert evidence["identity_integrity"]["valid_for_attribution"] is True, evidence
assert evidence["overall"]["decisive_trades"] == 2, evidence
assert evidence["overall"]["win_rate_ex_be_pct"] == 50.0, evidence
ci = evidence["overall"]["win_rate_wilson_95"]
assert ci is not None, evidence
assert 9.45 < ci["low_pct"] < 9.46, ci
assert 90.54 < ci["high_pct"] < 90.55, ci
assert evidence["by_relation"]["CONFLICT"]["win_rate_wilson_95"] is None, evidence
assert evidence["guardrails"]["minimum_sample_size_invented"] is False, evidence
assert evidence["guardrails"]["nested_execution_gate_authorized"] is False, evidence

invalid = dict(report)
invalid["integrity"] = dict(report["integrity"])
invalid["integrity"]["duplicate_outcome_rows"] = [{"decision_id": "D1"}]
invalid_evidence = mod.build_evidence(invalid)
assert invalid_evidence["data_status"] == "IDENTITY_INVALID", invalid_evidence
assert invalid_evidence["identity_integrity"]["valid_for_attribution"] is False, invalid_evidence

complete = dict(report)
complete["correlated_decisions"] = 3
complete["integrity"] = {
    "duplicate_outcome_rows": [],
    "duplicate_correlation_decision_ids": [],
    "unmatched_outcomes": [],
    "decisions_without_outcome": [],
}
complete_evidence = mod.build_evidence(complete)
assert complete_evidence["data_status"] == "COMPLETE_OBSERVED_SAMPLE", complete_evidence
assert complete_evidence["coverage"]["coverage_pct"] == 100.0, complete_evidence

print("N2-04 NMJE evidence sufficiency synthetic self-test PASS")
