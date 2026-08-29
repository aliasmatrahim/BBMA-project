#!/usr/bin/env python3
"""Deterministic C2-A model for legal identity-preserving journey transitions."""
from dataclasses import dataclass, replace
from enum import Enum, auto


class Stage(Enum):
    CANDIDATE = auto()
    CREATED = auto()
    VALIDATED = auto()
    GEOMETRY = auto()
    SIZED = auto()
    RISK_PASSED = auto()
    PORTFOLIO_PASSED = auto()
    EXECUTED = auto()
    MONITORED = auto()
    RECOVERED = auto()
    CLOSED = auto()


NEXT = {
    Stage.CANDIDATE: {Stage.CREATED},
    Stage.CREATED: {Stage.VALIDATED},
    Stage.VALIDATED: {Stage.GEOMETRY},
    Stage.GEOMETRY: {Stage.SIZED},
    Stage.SIZED: {Stage.RISK_PASSED},
    Stage.RISK_PASSED: {Stage.PORTFOLIO_PASSED},
    Stage.PORTFOLIO_PASSED: {Stage.EXECUTED},
    Stage.EXECUTED: {Stage.MONITORED},
    Stage.MONITORED: {Stage.RECOVERED, Stage.CLOSED},
    Stage.RECOVERED: {Stage.CLOSED},
}


@dataclass(frozen=True)
class Identity:
    pair: str
    direction: str
    candle_time: int
    sequence_hash: str
    decision_id: str = ""
    execution_hash: str = ""
    ticket: int = 0
    magic: int = 0
    open_time: int = 0


def transition(stage: Stage, target: Stage, before: Identity, after: Identity) -> Stage:
    if target not in NEXT.get(stage, set()):
        raise ValueError("illegal stage transition")

    immutable = ("pair", "direction", "candle_time", "sequence_hash")
    if any(getattr(before, field) != getattr(after, field) for field in immutable):
        raise ValueError("candidate identity drift")

    if target.value >= Stage.CREATED.value and not after.decision_id:
        raise ValueError("missing DecisionID")
    if stage.value >= Stage.CREATED.value and before.decision_id != after.decision_id:
        raise ValueError("DecisionID drift")

    if target.value >= Stage.EXECUTED.value:
        if not after.execution_hash or after.ticket <= 0 or after.magic <= 0 or after.open_time <= 0:
            raise ValueError("incomplete execution identity")
    if stage.value >= Stage.EXECUTED.value:
        durable = ("execution_hash", "ticket", "magic", "open_time")
        if any(getattr(before, field) != getattr(after, field) for field in durable):
            raise ValueError("execution identity drift")

    return target


def expect_rejected(fn, label: str) -> None:
    try:
        fn()
    except ValueError:
        return
    raise AssertionError(f"accepted invalid journey: {label}")


def run_direction(direction: str, ticket: int) -> int:
    identity = Identity("EURUSD", direction, 1_777_777_700, "SEQ-4TF")
    stage = transition(Stage.CANDIDATE, Stage.CREATED, identity,
                       replace(identity, decision_id=f"D-{direction}"))
    identity = replace(identity, decision_id=f"D-{direction}")

    for target in (Stage.VALIDATED, Stage.GEOMETRY, Stage.SIZED,
                   Stage.RISK_PASSED, Stage.PORTFOLIO_PASSED):
        stage = transition(stage, target, identity, identity)

    executed = replace(identity, execution_hash=f"H-{direction}", ticket=ticket,
                       magic=4701001, open_time=1_777_777_715)
    stage = transition(stage, Stage.EXECUTED, identity, executed)
    stage = transition(stage, Stage.MONITORED, executed, executed)
    stage = transition(stage, Stage.RECOVERED, executed, executed)
    stage = transition(stage, Stage.CLOSED, executed, executed)
    assert stage is Stage.CLOSED
    return 10


def main() -> None:
    cases = run_direction("BUY", 101) + run_direction("SELL", 102)
    base = Identity("EURUSD", "BUY", 1_777_777_700, "SEQ-4TF", "D-BUY")
    executed = replace(base, execution_hash="H-BUY", ticket=101,
                       magic=4701001, open_time=1_777_777_715)

    invalid = (
        (lambda: transition(Stage.CREATED, Stage.GEOMETRY, base, base), "skip M16"),
        (lambda: transition(Stage.VALIDATED, Stage.GEOMETRY, base,
                            replace(base, pair="GBPUSD")), "pair drift"),
        (lambda: transition(Stage.VALIDATED, Stage.GEOMETRY, base,
                            replace(base, decision_id="D-OTHER")), "DecisionID drift"),
        (lambda: transition(Stage.PORTFOLIO_PASSED, Stage.EXECUTED, base, base),
         "missing execution identity"),
        (lambda: transition(Stage.EXECUTED, Stage.MONITORED, executed,
                            replace(executed, execution_hash="H-OTHER")), "hash drift"),
        (lambda: transition(Stage.EXECUTED, Stage.MONITORED, executed,
                            replace(executed, ticket=999)), "ticket drift"),
        (lambda: transition(Stage.MONITORED, Stage.RECOVERED, executed,
                            replace(executed, magic=0)), "magic drift"),
        (lambda: transition(Stage.RECOVERED, Stage.VALIDATED, executed, executed),
         "reverse transition"),
    )
    for fn, label in invalid:
        expect_rejected(fn, label)
        cases += 1

    print(f"BBMA_CORE_END_TO_END_JOURNEY_MODEL=PASS cases={cases}")


if __name__ == "__main__":
    main()
