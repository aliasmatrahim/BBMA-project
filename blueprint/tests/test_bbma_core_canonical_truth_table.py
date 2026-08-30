#!/usr/bin/env python3
"""Deterministic C1-A golden truth-table and topology fixture checks."""
from __future__ import annotations

import json
from pathlib import Path


FIXTURE = Path(
    "blueprint/tests/fixtures/bbma_core_golden_truth_table.json"
)


def transition_map(rows: list[dict[str, str]]) -> dict[tuple[str, str], str]:
    result: dict[tuple[str, str], str] = {}
    for row in rows:
        key = (row["from"], row["event"])
        if key in result:
            raise AssertionError(f"ambiguous golden transition: {key}")
        result[key] = row["to"]
    return result


def validate_combination(
    expected: list[list[str]], components: list[list[str]], directions: list[str]
) -> bool:
    return (
        components == expected
        and len(directions) == 3
        and directions[0] in {"BUY", "SELL"}
        and len(set(directions)) == 1
    )


def main() -> None:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert data["schema_version"] == 1
    assert data["build"] == "4.72"
    assert data["directions"] == ["BUY", "SELL"]

    authority = data["authority"]
    assert authority == {
        "strategic_owner": "D1",
        "immediate_owner": "H4",
        "setup_context": "H1",
        "processing_clock": "M15",
        "shadow_context": "M5",
        "order_send_owner": "M22",
        "execution_policy": "NONE",
    }
    assert data["timeframes"] == {
        "primary": ["D1", "H4", "H1", "M15"],
        "shadow_only": ["M5"],
        "excluded": ["W1", "M30", "M1"],
    }

    expected_writers = {
        "BB_SHAPE": "M07",
        "EXTREME": "M08",
        "MHV_MLV": "M09",
        "CSM_CSD_ECSD": "M10",
        "RE_ENTRY": "M12",
        "COMBINATION_COLLECTION": "M13",
        "SEQUENCE_VALIDATION": "M14",
        "FINAL_SIGNAL_AUTHORITY": "M15",
    }
    assert data["writers"] == expected_writers

    transitions = {
        family: transition_map(rows)
        for family, rows in data["transitions"].items()
    }
    expected_counts = {"EXTREME": 9, "MLV": 10, "RE_ENTRY": 15}
    assert {name: len(rows) for name, rows in transitions.items()} == expected_counts

    # The same canonical transition table applies to BUY and SELL; direction
    # changes the source geometry, never the state labels or authority.
    symmetry_checks = 0
    for direction in data["directions"]:
        assert direction in {"BUY", "SELL"}
        assert transitions["EXTREME"][("NONE", "RAW_DETECTED")] == "RAW"
        assert transitions["EXTREME"][("RAW", "SUBSEQUENT_REVERSAL")] == "REVERSAL_CONFIRMED"
        assert transitions["MLV"][("LOSS_DEVELOPING", "MOVE_AWAY")] == "FORMATION_ESTABLISHED"
        assert transitions["RE_ENTRY"][("CANDIDATE_TYPE3", "MA5_OR_MA50_TOUCH")] == "CONFIRMED"
        symmetry_checks += 4

    # Undefined state/event pairs fail closed in the fixture; no implicit
    # promotion, newest-state inference, or generic fallback is permitted.
    for family, state, event in (
        ("EXTREME", "RAW", "RETEST_TOUCH"),
        ("MLV", "PARENT_READY", "LATER_ECSD_OR_CSD"),
        ("RE_ENTRY", "NONE", "MA5_MA10_TOUCH"),
        ("RE_ENTRY", "CANDIDATE_TYPE1", "INTRINSIC_EXPIRY"),
    ):
        assert (state, event) not in transitions[family]

    assert data["specific_reentry_precedence"] == [
        "TYPE3", "TYPE4", "TYPE2", "TYPE1"
    ]

    combinations = data["combinations"]
    expected_combinations = {
        "REM": [["RE_ENTRY", "H4"], ["EXTREME", "H1"], ["MLV", "M15"]],
        "RRE": [["RE_ENTRY", "D1"], ["RE_ENTRY", "H4"], ["EXTREME", "H1"]],
        "REE": [["RE_ENTRY", "D1"], ["EXTREME", "H4"], ["EXTREME", "H1"]],
    }
    assert combinations == expected_combinations
    topology_checks = 0
    for signature, expected in expected_combinations.items():
        for direction in data["directions"]:
            assert validate_combination(expected, combinations[signature], [direction] * 3)
            topology_checks += 1
        assert not validate_combination(expected, combinations[signature], ["BUY", "SELL", "BUY"])
        assert not validate_combination(expected, list(reversed(combinations[signature])), ["BUY"] * 3)
        topology_checks += 2

    assert data["semantic_sources"] == {
        "D1_OPPORTUNITY_RE_ENTRY": ["H1_RE_ENTRY", "M15_RE_ENTRY_FALLBACK"],
        "LEGACY_RE_ENTRY": ["H1_RE_ENTRY"],
        "REM": ["H4_RE_ENTRY"],
        "RRE": ["D1_RE_ENTRY"],
        "REE": ["D1_RE_ENTRY"],
    }

    print(
        "BBMA_CORE_CANONICAL_TRUTH_TABLE=PASS "
        f"transitions={sum(expected_counts.values())} "
        f"symmetry_checks={symmetry_checks} topology_checks={topology_checks}"
    )


if __name__ == "__main__":
    main()
