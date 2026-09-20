#!/usr/bin/env python3
from pathlib import Path

SRC = Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")


def body(signature):
    start = SRC.index(signature)
    brace = SRC.index("{", start)
    depth = 0
    for i in range(brace, len(SRC)):
        if SRC[i] == "{":
            depth += 1
        elif SRC[i] == "}":
            depth -= 1
            if depth == 0:
                return SRC[start:i + 1]
    raise AssertionError(signature)


def main():
    for marker in (
        "Version 4.9.9 - M17 Broker Distance Guards",
        '#property version   "4.99"',
        "V499_M17_BROKER_DISTANCE_GUARDS_20260921",
        "M17_BROKER_DISTANCE_GUARDS_216_20260921",
    ):
        assert marker in SRC, marker

    assert "double               FreezeLevel;" in SRC

    snap = body("void BuildRiskValidationSnapshot(")
    assert "snapshot.StopLevel = MarketInfo(pair, MODE_STOPLEVEL);" in snap
    assert "snapshot.FreezeLevel = MarketInfo(pair, MODE_FREEZELEVEL);" in snap

    helper = body("bool ValidateFrozenBrokerDistanceGeometry(")
    for marker in (
        "snapshot.Bid",
        "snapshot.Ask",
        "snapshot.StopLevel",
        "snapshot.FreezeLevel",
        "MathMax(stopDistance, freezeDistance)",
        "decision.StopLoss >= closePrice",
        "decision.StopLoss <= closePrice",
        "decision.TakeProfit <= closePrice",
        "decision.TakeProfit >= closePrice",
    ):
        assert marker in helper, marker
    assert "MarketInfo(" not in helper

    validate = body("bool ValidateSLTP(")
    assert "if(MinRRRatio > 0.0)" in validate
    assert "REJ_INVALID_RR" in validate
    assert "ValidateFrozenBrokerDistanceGeometry(decision, snapshot, false, rejection)" in validate
    assert "ValidateFrozenBrokerDistanceGeometry(decision, snapshot, true, rejection)" in validate
    assert "MathAbs(decision.StopLoss - closePrice)" not in validate
    assert "MathAbs(decision.TakeProfit - closePrice)" not in validate

    # M17 rejects invalid broker geometry; it never moves an approved level.
    assert "decision.StopLoss =" not in helper
    assert "decision.TakeProfit =" not in helper

    # Single broker execution authority remains unchanged.
    assert SRC.count("OrderSend(") == 1
    print("M17_BROKER_DISTANCE_STATIC=PASS")


if __name__ == "__main__":
    main()
