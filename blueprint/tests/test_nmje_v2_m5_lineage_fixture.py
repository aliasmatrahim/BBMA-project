#!/usr/bin/env python3
"""Synthetic Stage-A lineage fixtures for Issue #101.

This is a provenance-only model. It deliberately contains no price, indicator,
candidate-eligibility, ranking, rejection, or execution logic.
"""
from dataclasses import dataclass
from hashlib import sha256

RELATIONS = {"BUILDING", "SUPPORTING", "ALIGNED", "CONFLICT", "UNRESOLVED"}

def identity(domain: str, *parts: object) -> str:
    if not domain or any(part in (None, "", 0) for part in parts):
        raise ValueError("identity input missing")
    raw = "|".join((domain, *(str(part) for part in parts)))
    return sha256(raw.encode("utf-8")).hexdigest()[:16]

@dataclass(frozen=True)
class ParentChain:
    d1_owner_event_id: str
    h4_owner_event_id: str
    h1_journey_event_id: str
    m15_setup_event_id: str
    journey_id: str

    def validate(self) -> None:
        for value in (
            self.d1_owner_event_id,
            self.h4_owner_event_id,
            self.h1_journey_event_id,
            self.m15_setup_event_id,
            self.journey_id,
        ):
            if not value:
                raise ValueError("parent lineage incomplete")

@dataclass(frozen=True)
class M5Snapshot:
    event_id: str
    parent_event_id: str
    journey_id: str
    closed_candle_time: int
    relation: str
    chain: ParentChain

def d1_owner_id(pair: str, state: str, direction: str, epoch_start: int) -> str:
    return identity("D1OWN", pair, state, direction, epoch_start)

def m5_snapshot(
    pair: str,
    direction: str,
    event_type: str,
    event_start: int,
    closed_candle_time: int,
    relation: str,
    chain: ParentChain,
) -> M5Snapshot:
    chain.validate()
    if relation not in RELATIONS:
        raise ValueError("non-canonical relation")
    if closed_candle_time <= 0:
        raise ValueError("M5 observation must use a closed candle")
    return M5Snapshot(
        event_id=identity("M5CTX", pair, direction, event_type, event_start),
        parent_event_id=chain.m15_setup_event_id,
        journey_id=chain.journey_id,
        closed_candle_time=closed_candle_time,
        relation=relation,
        chain=chain,
    )

def recover(snapshot: M5Snapshot, expected: ParentChain) -> M5Snapshot:
    expected.validate()
    if snapshot.chain != expected:
        raise ValueError("stale child cannot migrate to a different parent chain")
    if snapshot.parent_event_id != expected.m15_setup_event_id:
        raise ValueError("M5 ParentEventID mismatch")
    if snapshot.journey_id != expected.journey_id:
        raise ValueError("M5 JourneyID mismatch")
    return snapshot

def main() -> None:
    d1_before = d1_owner_id("AUDCAD", "BUY_CONFIRMED", "BUY", 1700000000)
    d1_after_refresh = d1_owner_id("AUDCAD", "BUY_CONFIRMED", "BUY", 1700000000)
    assert d1_before == d1_after_refresh

    chain = ParentChain(
        d1_owner_event_id=d1_before,
        h4_owner_event_id=identity("H4OWN", "AUDCAD", "BUY", 1700003600),
        h1_journey_event_id=identity("H1CTX", "AUDCAD", "BUY", 1700007200),
        m15_setup_event_id=identity("M15SET", "AUDCAD", "BUY", 1700008100),
        journey_id=identity("JOURNEY", "AUDCAD", d1_before, 1700003600),
    )
    first = m5_snapshot(
        "AUDCAD", "BUY", "RE_ENTRY_CONTEXT", 1700008400, 1700008700,
        "SUPPORTING", chain,
    )
    refreshed = m5_snapshot(
        "AUDCAD", "BUY", "RE_ENTRY_CONTEXT", 1700008400, 1700009000,
        "CONFLICT", chain,
    )
    assert first.event_id == refreshed.event_id
    assert first.parent_event_id == refreshed.parent_event_id
    assert recover(first, chain) == first

    transitioned_d1 = d1_owner_id("AUDCAD", "TRANSITION", "NONE", 1700086400)
    transitioned_chain = ParentChain(
        d1_owner_event_id=transitioned_d1,
        h4_owner_event_id=identity("H4OWN", "AUDCAD", "BUY", 1700090000),
        h1_journey_event_id=identity("H1CTX", "AUDCAD", "BUY", 1700093600),
        m15_setup_event_id=identity("M15SET", "AUDCAD", "BUY", 1700094500),
        journey_id=identity("JOURNEY", "AUDCAD", transitioned_d1, 1700090000),
    )
    try:
        recover(first, transitioned_chain)
    except ValueError as exc:
        assert "stale child" in str(exc)
    else:
        raise AssertionError("stale M5 child silently migrated to a new owner epoch")

    try:
        ParentChain(d1_before, "", "H1", "M15", "J").validate()
    except ValueError as exc:
        assert "incomplete" in str(exc)
    else:
        raise AssertionError("incomplete lineage did not fail closed")

    print("NMJE_V2_M5_LINEAGE_FIXTURE=PASS")

if __name__ == "__main__":
    main()
