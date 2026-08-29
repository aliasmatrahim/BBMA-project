#!/usr/bin/env python3
"""Pure model for D1TPW M23 close retry/restart idempotency."""
from dataclasses import dataclass


@dataclass
class Trade:
    managed: bool = True
    frozen: bool = False
    latched: bool = True
    latch_candle: int = 1787875200
    identity_valid: bool = True
    order_open: bool = True
    checkpoint: bool = True
    close_attempts: int = 0
    checkpoint_clears: int = 0


def execute_close(trade: Trade, broker_outcome: str) -> bool:
    if not trade.managed or trade.frozen or not trade.latched:
        return False
    if trade.latch_candle <= 0 or not trade.identity_valid:
        return False
    if not trade.order_open:
        if trade.checkpoint:
            trade.checkpoint = False
            trade.checkpoint_clears += 1
        return True

    trade.close_attempts += 1
    if broker_outcome != "success":
        return False
    trade.order_open = False
    if trade.checkpoint:
        trade.checkpoint = False
        trade.checkpoint_clears += 1
    return True


def main() -> None:
    immediate = Trade()
    assert execute_close(immediate, "success")
    assert immediate.close_attempts == 1 and immediate.checkpoint_clears == 1
    assert execute_close(immediate, "success")
    assert immediate.close_attempts == 1 and immediate.checkpoint_clears == 1

    retry = Trade()
    assert not execute_close(retry, "retryable")
    assert retry.order_open and retry.latched and retry.checkpoint
    assert execute_close(retry, "success")
    assert retry.close_attempts == 2 and retry.checkpoint_clears == 1

    # A restart after durable latch reconstructs the same close obligation.
    restarted = Trade()
    recovered = Trade(**restarted.__dict__)
    assert execute_close(recovered, "success")
    assert recovered.close_attempts == 1 and not recovered.order_open

    already_closed = Trade(order_open=False)
    assert execute_close(already_closed, "success")
    assert already_closed.close_attempts == 0 and already_closed.checkpoint_clears == 1

    for blocked in (
        Trade(managed=False),
        Trade(frozen=True),
        Trade(latched=False),
        Trade(latch_candle=0),
        Trade(identity_valid=False),
    ):
        assert not execute_close(blocked, "success")
        assert blocked.close_attempts == 0 and blocked.order_open

    print("D1_TPW_CLOSE_IDEMPOTENCY_MODEL=PASS scenarios=9")


if __name__ == "__main__":
    main()

