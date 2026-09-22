#!/usr/bin/env python3
"""F05 deterministic ownership uncertainty model."""
from enum import IntEnum

class Ownership(IntEnum):
    UNKNOWN=-1
    EXCLUDED=0
    LIVE_OWNED=1

def basket(state, negative_net=13.0, reference_equity=1000.0):
    if state == Ownership.UNKNOWN:
        return 0.0, False
    if state != Ownership.LIVE_OWNED:
        return 0.0, True
    return abs(negative_net) / reference_equity * 100.0, True

def portfolio_admission(state, current_total, max_total):
    if state == Ownership.UNKNOWN:
        return False
    observed = current_total + (1 if state == Ownership.LIVE_OWNED else 0)
    return observed + 1 <= max_total

def tradelock(mode, state, existing_dir, proposed_dir):
    if mode == 0:
        return True
    if state == Ownership.UNKNOWN:
        return False
    if state != Ownership.LIVE_OWNED:
        return True
    if mode == 2:
        return False
    if mode == 1:
        return existing_dir == proposed_dir
    raise AssertionError(mode)

def manage_portfolio(latched, state, threshold=1.0):
    pct, valid = basket(state)
    if latched:
        return True
    if not valid:
        return False
    return pct >= threshold

def main():
    pct, valid = basket(Ownership.UNKNOWN)
    assert pct == 0.0 and not valid
    pct, valid = basket(Ownership.LIVE_OWNED)
    assert valid and abs(pct - 1.3) < 1e-12

    assert not portfolio_admission(Ownership.UNKNOWN, 0, 1)
    assert portfolio_admission(Ownership.EXCLUDED, 0, 1)

    assert tradelock(0, Ownership.UNKNOWN, 1, 2)
    assert not tradelock(1, Ownership.UNKNOWN, 1, 2)
    assert not tradelock(2, Ownership.UNKNOWN, 1, 1)
    assert tradelock(1, Ownership.LIVE_OWNED, 1, 1)
    assert not tradelock(1, Ownership.LIVE_OWNED, 1, 2)

    # Unknown observation must not fabricate an emergency threshold breach.
    assert manage_portfolio(False, Ownership.UNKNOWN) is False

    print("F05_SELECTION_UNCERTAINTY_MODEL=PASS")

if __name__ == "__main__":
    main()
