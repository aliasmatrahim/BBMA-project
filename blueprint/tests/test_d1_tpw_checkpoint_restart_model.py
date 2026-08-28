#!/usr/bin/env python3
"""Deterministic restart model for the D1TPW v2 checkpoint contract."""
from copy import deepcopy


VERSION = 2
REQUIRED = {"V", "D", "X", "LP", "L", "XL", "F", "OT", "MG", "P", "C", "E"}


def load(store: dict, expected: dict) -> bool:
    if not REQUIRED.issubset(store) or store["V"] != VERSION:
        return False
    if store["D"] != expected["D"] or store["OT"] != expected["OT"]:
        return False
    if store["MG"] != expected["MG"] or store["P"] != expected["P"]:
        return False
    if store["E"] != expected["E"] or not store["C"]:
        return False
    if store["X"] <= 0 or store["LP"] < store["X"]:
        return False
    if bool(store["L"]) != (store["XL"] > 0):
        return False
    if store["F"] and store["L"]:
        return False
    return True


def main() -> None:
    expected = {"D": 1, "OT": 1787932800, "MG": 61001,
                "P": "1111222233334444", "E": "aaaabbbbccccdddd"}
    valid = {"V": VERSION, "D": 1, "X": 1787788800, "LP": 1787875200,
             "L": 0, "XL": 0, "F": 0, "OT": expected["OT"],
             "MG": expected["MG"], "P": expected["P"],
             "C": "0123456789abcdef", "E": expected["E"]}
    assert load(valid, expected)

    torn = deepcopy(valid)
    torn.pop("V")
    assert not load(torn, expected)

    for key, wrong in (("V", 1), ("P", "ffff222233334444"),
                       ("C", ""), ("E", "ffffbbbbccccdddd"),
                       ("OT", expected["OT"] + 1), ("MG", expected["MG"] + 1)):
        changed = deepcopy(valid)
        changed[key] = wrong
        assert not load(changed, expected), key

    invalid_cursor = deepcopy(valid)
    invalid_cursor["LP"] = invalid_cursor["X"] - 86400
    assert not load(invalid_cursor, expected)

    impossible_state = deepcopy(valid)
    impossible_state.update({"L": 1, "XL": valid["LP"], "F": 1})
    assert not load(impossible_state, expected)

    replay = deepcopy(valid)
    assert load(replay, expected)
    assert replay == valid

    # Every possible torn-write prefix must fail until V is committed last.
    payload_order = ["D", "X", "LP", "L", "XL", "F", "OT", "MG", "P", "C", "E"]
    torn_checks = 0
    partial = {}
    for key in payload_order:
        partial[key] = valid[key]
        assert not load(partial, expected), key
        torn_checks += 1
    committed = deepcopy(partial)
    committed["V"] = VERSION
    assert load(committed, expected)

    # Ticket namespaces must not permit one trade to recover another trade's
    # execution identity even on the same pair/open time/magic.
    ticket_a = deepcopy(valid)
    ticket_b = deepcopy(valid)
    ticket_b["E"] = "1111bbbbccccdddd"
    assert load(ticket_a, expected)
    assert not load(ticket_b, expected)
    expected_b = deepcopy(expected)
    expected_b["E"] = ticket_b["E"]
    assert load(ticket_b, expected_b)

    # Repeated restarts are read-only and preserve the exact committed state.
    restart_state = deepcopy(valid)
    for _ in range(5):
        assert load(restart_state, expected)
        assert restart_state == valid

    print(f"D1_TPW_CHECKPOINT_RESTART_MODEL=PASS torn_checks={torn_checks} restarts=5")


if __name__ == "__main__":
    main()

