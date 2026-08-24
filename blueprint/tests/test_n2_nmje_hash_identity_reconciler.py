#!/usr/bin/env python3
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "blueprint" / "tools" / "n2_nmje_hash_identity_reconciler.py"
spec = importlib.util.spec_from_file_location("n2_nmje_hash_identity_reconciler", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(mod)

assert mod.mql4_short_hash("") == "0000000000000000"
assert len(mod.mql4_short_hash("EURUSD|2026.08.25 00:00|1|8|ABC")) == 16

d1 = "EURUSD|2026.08.25 00:00|1|8|AAA"
d2 = "GBPUSD|2026.08.25 00:15|2|9|BBB"
h1 = mod.mql4_short_hash(d1)
h2 = mod.mql4_short_hash(d2)
assert h1 != h2

correlation = {
    "rows": [
        {"decision": {"decision_id": d1, "decision_hash": h1, "pair": "EURUSD", "signal": "SIGNAL_REM"}},
        {"decision": {"decision_id": d2, "decision_hash": h2, "pair": "GBPUSD", "signal": "SIGNAL_RE_ENTRY"}},
    ]
}
extraction = {
    "valid_exact_rows": [
        {
            "decision_id": d1,
            "decision_hash": h1,
            "pair": "EURUSD",
            "ticket": 101,
            "net_profit": 3.0,
            "close_time": 1770000000,
            "recovery_state": "REC_NORMAL",
        }
    ],
    "hash_only_rows": [
        {
            "decision_id": "-",
            "decision_hash": h2,
            "pair": "GBPUSD",
            "ticket": 102,
            "net_profit": -1.0,
            "close_time": 1770000100,
            "recovery_state": "REC_IDENTITY_HASH_ONLY",
        },
        {
            "decision_id": "-",
            "decision_hash": "FFFFFFFFFFFFFFFF",
            "pair": "USDJPY",
            "ticket": 103,
            "net_profit": 2.0,
            "close_time": 1770000200,
            "recovery_state": "REC_IDENTITY_HASH_ONLY",
        },
    ],
    "duplicate_tickets": [],
    "duplicate_decision_ids": [],
}

report = mod.reconcile(correlation, extraction)
assert report["identity_valid"] is True, report
assert report["logged_decision_hash_mismatches"] == [], report
assert report["exact_outcome_identity_issues"] == [], report
assert report["exact_outcome_count"] == 1, report
assert report["validated_exact_outcome_count"] == 1, report
assert report["hash_only_input_count"] == 2, report
assert report["reconciled_hash_only_count"] == 1, report
assert report["combined_outcome_count"] == 2, report
assert report["combined_rows"][0]["identity_provenance"] == "FULL_DECISION_ID_PLUS_HASH", report
assert report["reconciled_rows"][0]["decision_id"] == d2, report
assert report["reconciled_rows"][0]["identity_provenance"] == "UNIQUE_SHORT_HASH_PLUS_PAIR", report
assert len(report["unresolved_hash_only_rows"]) == 1, report
assert report["unresolved_hash_only_rows"][0]["unresolved_reason"] == "HASH_NOT_FOUND_IN_VALIDATED_DECISIONS", report

pair_bad = dict(extraction)
pair_bad["valid_exact_rows"] = []
pair_bad["hash_only_rows"] = [dict(extraction["hash_only_rows"][0])]
pair_bad["hash_only_rows"][0]["pair"] = "EURUSD"
pair_report = mod.reconcile(correlation, pair_bad)
assert pair_report["reconciled_hash_only_count"] == 0, pair_report
assert pair_report["unresolved_hash_only_rows"][0]["unresolved_reason"] == "PAIR_IDENTITY_MISMATCH", pair_report

# Logged DEC DIDH must agree with the hash reconstructed from decoded DecisionID.
hash_bad_corr = {
    "rows": [
        {"decision": {"decision_id": d2, "decision_hash": "BADHASH", "pair": "GBPUSD"}},
    ]
}
hash_bad_ext = {
    "valid_exact_rows": [],
    "hash_only_rows": [dict(extraction["hash_only_rows"][0])],
    "duplicate_tickets": [],
    "duplicate_decision_ids": [],
}
hash_bad = mod.reconcile(hash_bad_corr, hash_bad_ext)
assert hash_bad["identity_valid"] is False, hash_bad
assert len(hash_bad["logged_decision_hash_mismatches"]) == 1, hash_bad
assert hash_bad["reconciled_hash_only_count"] == 0, hash_bad
assert hash_bad["unresolved_hash_only_rows"][0]["unresolved_reason"] == "HASH_NOT_FOUND_IN_VALIDATED_DECISIONS", hash_bad

# Full outcome DIDH mismatch must be excluded and fail identity validation.
out_hash_bad = {
    "valid_exact_rows": [dict(extraction["valid_exact_rows"][0])],
    "hash_only_rows": [],
    "duplicate_tickets": [],
    "duplicate_decision_ids": [],
}
out_hash_bad["valid_exact_rows"][0]["decision_hash"] = "BADHASH"
out_hash_report = mod.reconcile(correlation, out_hash_bad)
assert out_hash_report["identity_valid"] is False, out_hash_report
assert out_hash_report["validated_exact_outcome_count"] == 0, out_hash_report
assert out_hash_report["combined_outcome_count"] == 0, out_hash_report
assert out_hash_report["exact_outcome_identity_issues"][0]["identity_issue"] == "OUTCOME_DECISION_HASH_MISMATCH", out_hash_report

# Full outcome pair mismatch must also be excluded and fail closed.
out_pair_bad = {
    "valid_exact_rows": [dict(extraction["valid_exact_rows"][0])],
    "hash_only_rows": [],
    "duplicate_tickets": [],
    "duplicate_decision_ids": [],
}
out_pair_bad["valid_exact_rows"][0]["pair"] = "USDJPY"
out_pair_report = mod.reconcile(correlation, out_pair_bad)
assert out_pair_report["identity_valid"] is False, out_pair_report
assert out_pair_report["validated_exact_outcome_count"] == 0, out_pair_report
assert out_pair_report["exact_outcome_identity_issues"][0]["identity_issue"] == "OUTCOME_PAIR_IDENTITY_MISMATCH", out_pair_report

original_hash = mod.mql4_short_hash
try:
    mod.mql4_short_hash = lambda text, chars=16: "COLLISION"
    collision_corr = {
        "rows": [
            {"decision": {"decision_id": "D-A", "pair": "EURUSD"}},
            {"decision": {"decision_id": "D-B", "pair": "EURUSD"}},
        ]
    }
    collision_ext = {
        "valid_exact_rows": [],
        "hash_only_rows": [{
            "decision_id": "-", "decision_hash": "COLLISION", "pair": "EURUSD",
            "ticket": 999, "net_profit": 1.0, "close_time": 1770000300,
            "recovery_state": "REC_IDENTITY_HASH_ONLY",
        }],
        "duplicate_tickets": [],
        "duplicate_decision_ids": [],
    }
    collision = mod.reconcile(collision_corr, collision_ext)
    assert collision["identity_valid"] is False, collision
    assert collision["reconciled_hash_only_count"] == 0, collision
    assert collision["unresolved_hash_only_rows"][0]["unresolved_reason"] == "HASH_COLLISION", collision
finally:
    mod.mql4_short_hash = original_hash

print("N2-14 NMJE exact + hash-only identity fail-closed self-test PASS")
