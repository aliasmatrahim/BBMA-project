#!/usr/bin/env python3
"""Deterministic model for Q9 P1 epoch/lineage semantics.

This is provenance-only. It models no BBMA entry, risk or execution rule.
"""
from dataclasses import dataclass
from hashlib import sha256

BUY = ("BUY_CONFIRMED", "BUY")
SELL = ("SELL_CONFIRMED", "SELL")
TRANSITION = ("TRANSITION", "NONE")

@dataclass(frozen=True)
class D1Bar:
    candle_time: int
    state: str
    direction: str

def resolve_epoch(history_newest_first: list[D1Bar]) -> int | None:
    if len(history_newest_first) < 2:
        return None
    current = history_newest_first[0]
    epoch = current.candle_time
    for prior in history_newest_first[1:]:
        if (prior.state, prior.direction) != (current.state, current.direction):
            return epoch
        epoch = prior.candle_time
    # Exact older boundary was not available.
    return None

def event_id(pair: str, state: str, direction: str, epoch: int | None) -> str:
    if not pair or not epoch:
        return ""
    raw = f"D1OWN|{pair}|{state}|{direction}|{epoch}"
    return sha256(raw.encode()).hexdigest()[:16]

def journey_id(pair: str, parent_kind: str, parent_event_id: str) -> str:
    if not pair or not parent_event_id:
        return ""
    return f"J2|{pair}|{parent_kind}|{parent_event_id}"

def main() -> None:
    # Same owner across ordinary newer closed-D1 refresh retains epoch.
    before = [
        D1Bar(300, *BUY),
        D1Bar(200, *BUY),
        D1Bar(100, *SELL),
    ]
    after = [
        D1Bar(400, *BUY),
        D1Bar(300, *BUY),
        D1Bar(200, *BUY),
        D1Bar(100, *SELL),
    ]
    assert resolve_epoch(before) == 200
    assert resolve_epoch(after) == 200
    e1 = event_id("GBPUSD", *BUY, resolve_epoch(before))
    e2 = event_id("GBPUSD", *BUY, resolve_epoch(after))
    assert e1 == e2
    assert journey_id("GBPUSD", "D1_OWNER", e1) == journey_id("GBPUSD", "D1_OWNER", e2)

    # A real owner transition creates a new epoch and identity.
    changed = [
        D1Bar(500, *SELL),
        D1Bar(400, *BUY),
        D1Bar(300, *BUY),
        D1Bar(200, *BUY),
        D1Bar(100, *SELL),
    ]
    assert resolve_epoch(changed) == 500
    assert event_id("GBPUSD", *SELL, 500) != e1

    # Restart with identical closed history reconstructs the same exact identity.
    restart_epoch = resolve_epoch(after)
    assert restart_epoch == 200
    assert event_id("GBPUSD", *BUY, restart_epoch) == e1

    # Missing older boundary fails closed rather than inventing an epoch.
    incomplete = [
        D1Bar(400, *BUY),
        D1Bar(300, *BUY),
        D1Bar(200, *BUY),
    ]
    assert resolve_epoch(incomplete) is None
    assert event_id("GBPUSD", *BUY, resolve_epoch(incomplete)) == ""
    assert journey_id("GBPUSD", "D1_OWNER", "") == ""

    print("Q9_NMJE_P1_EPOCH_MODEL=PASS")

if __name__ == "__main__":
    main()
