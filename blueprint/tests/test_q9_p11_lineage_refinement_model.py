#!/usr/bin/env python3

NONE = 0
FIRST = 1
CONTINUATION = 2
NEW_JOURNEY = 3
UNRESOLVED = 4


def valid_event_id(value: str) -> bool:
    return len(value) == 16


def classify(parent: str, journey: str,
             previous_parent: str = "", previous_journey: str = "") -> int:
    if not parent and not journey:
        return NONE
    if not valid_event_id(parent) or not journey:
        return UNRESOLVED
    previous_valid = valid_event_id(previous_parent) and bool(previous_journey)
    if previous_valid and (
        previous_parent != parent or previous_journey != journey
    ):
        return NEW_JOURNEY
    # Strict policy: current canonical parent is this JourneyID's root.
    # No separate canonical continuation-event identity exists yet.
    return FIRST


def main() -> None:
    a = "A" * 16
    b = "B" * 16
    j1 = "J2|GBPUSD|H4_OWNER|" + a
    j2 = "J2|GBPUSD|H4_RE|" + b

    assert classify("", "") == NONE
    assert classify("bad", j1) == UNRESOLVED
    assert classify(a, "") == UNRESOLVED

    assert classify(a, j1) == FIRST
    assert classify(a, j1, a, j1) == FIRST
    assert classify(b, j2, a, j1) == NEW_JOURNEY

    # A higher-owner family remaining unchanged cannot merge canonical journeys.
    assert classify(b, j2, a, j1) != CONTINUATION

    # Restart without prior observer memory must not invent a transition.
    assert classify(b, j2, "", "") == FIRST

    print("Q9_P11_LINEAGE_REFINEMENT_MODEL=PASS")


if __name__ == "__main__":
    main()
