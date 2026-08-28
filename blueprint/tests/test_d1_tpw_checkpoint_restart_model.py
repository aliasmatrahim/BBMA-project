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
    print("D1_TPW_CHECKPOINT_RESTART_MODEL=PASS")


if __name__ == "__main__":
    main()

