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
    # C044 must survive later EA build-identity changes unchanged.
    for marker in (
        "EnableC044Lifecycle                = true;",
    ):
        assert marker in SRC, marker

    load = body("bool LoadC044Checkpoint(")
    replay_fail = """if(!LoadC044ReplaySeed(info, committedGeneration))
   {
      ResetC044TradeState(info);
      return false;
   }"""
    generation_fail = """if(!GlobalVariableCheck(base + "CM") || !GlobalVariableCheck(base + "G") ||
      GlobalVariableGet(base + "CM") != committedGeneration ||
      GlobalVariableGet(base + "G") != committedGeneration)
   {
      ResetC044TradeState(info);
      return false;
   }"""
    assert replay_fail in load
    assert generation_fail in load
    assert load.index("if(state == C044_LIFE_FROZEN)") < load.index(replay_fail)

    recover = body("void RecoverExistingOrders(")
    assert "targetlessRecovered = LoadC044Checkpoint(info);" in recover
    assert "REC_IDENTITY_MISSING_FROZEN" in recover
    assert "TARGETLESS_CHECKPOINT_MISSING_OR_INVALID" in recover

    advance = body("void AdvanceC044OwnerEventsForPair(")
    assert "c044_lifecycle_managed" in advance
    assert "C044_LIFE_FROZEN" in advance

    reducer = body("bool ProcessC044OwnerClosedCandle(")
    for marker in (
        "DetectCSM(pair, info.c044_owner_timeframe,",
        "C044_EXIT_OPPOSITE_CSM",
        "C044_EXIT_FAILED_MOMENTUM",
        "C044_EXIT_CYCLE_SUPERSEDED",
        "C044_LIFE_WAIT_NEXT_REENTRY",
        "REENTRY_REARM",
    ):
        assert marker in reducer
    assert "outer-BB" not in reducer
    assert "Outer" not in reducer

    assert SRC.count("OrderSend(") == 1
    print("C044_FAIL_FROZEN_RECOVERY_STATIC=PASS")


if __name__ == "__main__":
    main()
