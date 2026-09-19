#!/usr/bin/env python3
from pathlib import Path
import re

SRC = Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")

def body(signature: str) -> str:
    start = SRC.index(signature)
    brace = SRC.index("{", start)
    depth = 0
    for i in range(brace, len(SRC)):
        if SRC[i] == "{":
            depth += 1
        elif SRC[i] == "}":
            depth -= 1
            if depth == 0:
                return SRC[brace + 1:i]
    raise AssertionError(f"unterminated function: {signature}")

def require(text: str, *markers: str) -> None:
    for marker in markers:
        assert marker in text, f"missing marker: {marker}"

def main() -> None:
    require(
        SRC,
        "Version 4.8.7 - Q9 NMJE Lineage Provenance",
        '#property version   "4.87"',
        '#define BBMA_BUILD_TAG      "V487A_Q9_NMJE_LINEAGE_TRACEFIX_20260918"',
        '#define BBMA_SOURCE_REV_TAG "Q9_P1_NMJE_LINEAGE_TRACEFIX_101_20260918"',
        "datetime             EpochStartCandleTime;",
        "string               CanonicalEventID;",
        "string                  ParentEventID;",
        "NMJE_ReEntryEventID(",
        "NMJE_ExtremeEventID(",
        "NMJE_MLVEventID(",
        "NMJE_D1OwnerEventID(",
        "NMJE_H4OwnerEventID(",
        'return "J2|" + pair + "|" + NMJE_ParentText(kind) + "|" + parentEventID;',
        'parentReason = "PARENT_EVENT_ID_UNRESOLVED";',
        'Log(DBG_FULL, "BBMA EA " + string(BBMA_BUILD_TAG) + " initialized successfully");',
    )
    assert "V4.8.6 Structural Lifetime Authority Repair initialized successfully" not in SRC

    # Q9 P1 must remain provenance-only.
    for forbidden in (
        "NMJE_PassExecutionGate",
        "REJ_NMJE_RELATION",
        "EnableNMJEM5Execution",
        "NMJE_BuildM5Node(",
        "M5_PROCESSING_CLOCK",
        "N3_POLICY_ACTIVE",
        "PERIOD_M5",
    ):
        assert forbidden not in SRC, f"authority/M5 leak: {forbidden}"

    # Broker ownership must be byte-count stable relative to Build 4.86 baseline.
    assert SRC.count("OrderSend(") == 1
    assert SRC.count("OrderClose(") == 3
    assert SRC.count("OrderModify(") == 0
    assert SRC.count("OrderDelete(") == 0

    # Existing architecture owners must remain present.
    require(
        SRC,
        "MODULE 15: PRIORITY ENGINE (FINAL SIGNAL AUTHORITY)",
        "MODULE 16: CONFLICT & INVALIDATION ENGINE",
        "MODULE 22: ORDER EXECUTION ENGINE (DUMB EXECUTOR)",
        "[N1-NMJE]",
        "[N2-NMJE-DEC]",
        "[N2-NMJE-OUT]",
    )

    d1_id = body("string NMJE_D1OwnerEventID(")
    require(d1_id, "owner.EpochStartCandleTime", "NMJE_IdentityHash(raw)")
    assert "owner.SourceCandleTime" not in d1_id

    epoch = body("bool M11_ResolveD1OwnerEpochStart(")
    require(
        epoch,
        "iBarShift(pair, PERIOD_D1, owner.SourceCandleTime, true)",
        "iBars(pair, PERIOD_D1)",
        "M11_ClassifyD1OwnerAtShift(",
        "epochStart = 0;",
    )

    classifier = body("bool M11_ClassifyD1OwnerValues(")
    require(
        classifier,
        "close1 > ma50_1 && ma50_1 > ma50_2",
        "close1 < ma50_1 && ma50_1 < ma50_2",
        "D1_OWNER_BUY_CONFIRMED",
        "D1_OWNER_SELL_CONFIRMED",
        "D1_TRANSITION",
    )
    # The canonical price-side + MA50-slope predicates must exist in one owner only.
    assert SRC.count("close1 > ma50_1 && ma50_1 > ma50_2") == 1
    assert SRC.count("close1 < ma50_1 && ma50_1 < ma50_2") == 1

    historical = body("bool M11_ClassifyD1OwnerAtShift(")
    require(
        historical,
        "if(pair == \"\" || shift < 1) return false;",
        "iTime(pair, PERIOD_D1, shift)",
        "iClose(pair, PERIOD_D1, shift)",
        "EMA(pair, PERIOD_D1, EMA50_PERIOD, shift)",
        "EMA(pair, PERIOD_D1, EMA50_PERIOD, shift + 1)",
        "M11_ClassifyD1OwnerValues(close1, ma50_1, ma50_2,",
    )

    live_owner = body("void UpdateD1MajorTrendOwner(")
    require(
        live_owner,
        "M11_ClassifyD1OwnerValues(owner.Close1, owner.MA50_1, owner.MA50_2,",
    )
    assert "owner.Close1 > owner.MA50_1" not in live_owner
    assert "owner.Close1 < owner.MA50_1" not in live_owner

    journey = body("string NMJE_BuildJourneyID(")
    require(journey, "parentEventID", '"J2|"')
    for forbidden in ("TimeCurrent(", "TimeLocal(", "GetTickCount(", "MathRand(", "MarketInfo("):
        assert forbidden not in journey

    parent = body("bool NMJE_ResolveParent(")
    require(
        parent,
        "NMJE_ReEntryEventID(state.actual_symbol, selected)",
        "NMJE_H4OwnerEventID(state.actual_symbol, state.h4_direction_owner)",
        "NMJE_D1OwnerEventID(state.actual_symbol, state.d1_major_trend_owner)",
    )

    print("Q9_NMJE_P1_CURRENT_OWNER_STATIC=PASS")

if __name__ == "__main__":
    main()
