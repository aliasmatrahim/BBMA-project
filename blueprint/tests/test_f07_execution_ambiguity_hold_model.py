#!/usr/bin/env python3
"""Deterministic F07 policy model; no broker/terminal mutation."""

from dataclasses import dataclass

@dataclass
class Hold:
    active: bool = False
    persisted: bool = False
    monitored: bool = False
    tombstone: bool = False
    frozen: bool = False

def load(active_marker: bool, payload_complete: bool) -> Hold:
    if not active_marker:
        return Hold()
    return Hold(active=True, persisted=payload_complete)

def latch(persist_ok: bool) -> Hold:
    return Hold(active=True, persisted=persist_ok)

def reconcile(h: Hold, match: str = "none", identity_save: bool = True,
              registry_capacity: bool = True) -> Hold:
    if not h.active or not h.persisted:
        return h
    if match == "none":
        return h
    if match == "closed":
        if not identity_save:
            return h
        h.tombstone = True
        h.active = False
        h.persisted = False
        return h
    if match == "open":
        if not registry_capacity:
            return h
        h.monitored = True
        h.frozen = True
        if not identity_save:
            return h
        h.tombstone = True
        h.active = False
        h.persisted = False
        return h
    raise AssertionError(match)

def main():
    # Ambiguity always enters a hold, even if persistence verification fails.
    h = latch(False)
    assert h.active and not h.persisted

    # Restart with an active marker but partial payload must remain fail-closed.
    h = load(True, False)
    assert h.active and not h.persisted

    # No broker match never releases by elapsed ticks/time.
    h = latch(True)
    for _ in range(1000):
        h = reconcile(h, "none")
    assert h.active and h.persisted and not h.monitored

    # Late-visible live execution is frozen/monitored before hold release.
    h = reconcile(latch(True), "open", identity_save=True, registry_capacity=True)
    assert not h.active and h.monitored and h.frozen and h.tombstone

    # A broker-observed closed execution only needs durable idempotency.
    h = reconcile(latch(True), "closed", identity_save=True)
    assert not h.active and not h.monitored and h.tombstone

    # Identity-persistence or registry-capacity failure cannot release the hold.
    h = reconcile(latch(True), "open", identity_save=False, registry_capacity=True)
    assert h.active and h.monitored and h.frozen and not h.tombstone
    h = reconcile(latch(True), "open", identity_save=True, registry_capacity=False)
    assert h.active and not h.monitored and not h.tombstone

    print("F07_EXECUTION_AMBIGUITY_HOLD_MODEL=PASS")

if __name__ == "__main__":
    main()
