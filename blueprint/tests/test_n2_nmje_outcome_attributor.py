#!/usr/bin/env python3
from pathlib import Path
import csv
import importlib.util
import tempfile

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "blueprint" / "tools" / "n2_nmje_outcome_attributor.py"
spec = importlib.util.spec_from_file_location("n2_nmje_outcome_attributor", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)

correlation = {
    "rows": [
        {
            "decision": {
                "decision_id": "D1",
                "pair": "EURUSD",
                "signal": "SIGNAL_REM",
                "direction": "S",
                "relation": "SUPPORTING",
                "parent": "H4_RE/S",
                "journey": "J1",
            },
            "match_mode": "EXACT_JOURNEY",
            "context": {},
        },
        {
            "decision": {
                "decision_id": "D2",
                "pair": "EURUSD",
                "signal": "SIGNAL_RE_ENTRY",
                "direction": "S",
                "relation": "ALIGNED",
                "parent": "H4_RE/S",
                "journey": "J1",
            },
            "match_mode": "EXACT_JOURNEY",
            "context": {},
        },
        {
            "decision": {
                "decision_id": "D3",
                "pair": "GBPUSD",
                "signal": "SIGNAL_RRE",
                "direction": "B",
                "relation": "CONFLICT",
                "parent": "H4_RE/B",
                "journey": "J2",
            },
            "match_mode": "EXACT_JOURNEY",
            "context": {},
        },
        {
            "decision": {
                "decision_id": "D4",
                "pair": "USDJPY",
                "signal": "SIGNAL_REE",
                "direction": "B",
                "relation": "BUILDING",
                "parent": "D1_RE/B",
                "journey": "J3",
            },
            "match_mode": "EXACT_JOURNEY",
            "context": {},
        },
    ]
}

with tempfile.TemporaryDirectory() as td:
    csv_path = Path(td) / "outcomes.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["decision_id", "net_profit", "ticket"])
        writer.writeheader()
        writer.writerow({"decision_id": "D1", "net_profit": "10.0", "ticket": "101"})
        writer.writerow({"decision_id": "D2", "net_profit": "-4.0", "ticket": "102"})
        writer.writerow({"decision_id": "D3", "net_profit": "0.0", "ticket": "103"})
        writer.writerow({"decision_id": "UNKNOWN", "net_profit": "3.0", "ticket": "999"})

    outcomes, duplicates = mod.load_outcomes(csv_path)
    report = mod.attribute(correlation, outcomes, duplicates)

assert report["matched_outcomes"] == 3, report
assert report["correlated_decisions"] == 4, report
assert report["outcome_rows"] == 4, report
assert report["overall"]["trades"] == 3, report
assert report["overall"]["wins"] == 1, report
assert report["overall"]["losses"] == 1, report
assert report["overall"]["breakeven"] == 1, report
assert report["overall"]["win_rate_ex_be_pct"] == 50.0, report
assert report["overall"]["net_profit"] == 6.0, report
assert report["by_relation"]["SUPPORTING"]["net_profit"] == 10.0, report
assert report["by_relation"]["ALIGNED"]["net_profit"] == -4.0, report
assert report["by_relation"]["CONFLICT"]["breakeven"] == 1, report
assert len(report["integrity"]["unmatched_outcomes"]) == 1, report
assert len(report["integrity"]["decisions_without_outcome"]) == 1, report
assert report["integrity"]["duplicate_outcome_rows"] == [], report
assert report["integrity"]["duplicate_correlation_decision_ids"] == [], report

# Duplicate outcome identity must be surfaced and excluded from attribution.
dup_outcomes = [
    {"decision_id": "D1", "net_profit": 10.0},
    {"decision_id": "D1", "net_profit": -10.0},
]
dup_rows = [{"decision_id": "D1", "net_profit": -10.0}]
dup_report = mod.attribute(correlation, dup_outcomes, dup_rows)
assert dup_report["matched_outcomes"] == 0, dup_report
assert len(dup_report["integrity"]["duplicate_outcome_rows"]) == 1, dup_report

print("N2-03 NMJE outcome attribution synthetic self-test PASS")
