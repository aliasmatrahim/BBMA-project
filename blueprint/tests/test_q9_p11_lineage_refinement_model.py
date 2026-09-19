#!/usr/bin/env python3

NONE = 0
FIRST = 1
CONTINUATION = 2
NEW_JOURNEY = 3
UNRESOLVED = 4

def valid_event_id(value: str) -> bool:
    return len(value) == 16

def classify(parent: str, root: str, previous_root: str = "") -> int:
    if not parent:
        return NONE
    if not valid_event_id(root):
        return UNRESOLVED
    if valid_event_id(previous_root) and previous_root != root:
        return NEW_JOURNEY
    if parent == root:
        return FIRST
    return CONTINUATION

def main() -> None:
    a = "A" * 16
    b = "B" * 16
    c = "C" * 16

    assert classify("", "", "") == NONE
    assert classify(a, "", "") == UNRESOLVED
    assert classify(a, "bad", "") == UNRESOLVED

    assert classify(a, a, "") == FIRST
    assert classify(b, a, "") == CONTINUATION
    assert classify(c, a, a) == CONTINUATION

    assert classify(c, b, a) == NEW_JOURNEY
    assert classify(b, b, a) == NEW_JOURNEY

    # Restart / malformed prior observer state must never invent NEW_JOURNEY.
    assert classify(c, b, "") == CONTINUATION
    assert classify(c, b, "bad") == CONTINUATION
    assert classify(c, b, "\x00") == CONTINUATION
    assert classify(b, b, "") == FIRST

    print("Q9_P11_LINEAGE_REFINEMENT_MODEL=PASS")

if __name__ == "__main__":
    main()
