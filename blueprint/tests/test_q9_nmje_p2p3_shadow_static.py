#!/usr/bin/env python3
from pathlib import Path

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
        "Version 4.8.8 - Q9 NMJE M5 Shadow Context",
        '#property version   "4.88"',
        '#define BBMA_BUILD_TAG      "V488_Q9_NMJE_M5_SHADOW_20260918"',
        '#define BBMA_SOURCE_REV_TAG "Q9_C1C2_P2_M5_SHADOW_101_20260918"',
        "NMJE_M5_CONTEXT_RE_ENTRY = 1",
        "NMJE_M5_CONTEXT_EXTREME = 2",
        "struct NMJEM5RefinementState",
        "TimeframeData        m5_data;",
        "ReEntryData          re_m5_buy_state;",
        "ExtremeLifecycleData extreme_m5_buy_lifecycle;",
        "NMJEM5RefinementState    M5Refinement;",
    )

    # M15 remains the only processing clock.
    is_new = body("bool IsNewCandle(")
    assert "PERIOD_M15" in is_new
    assert "PERIOD_M5" not in is_new
    assert "M5_CandleTime" not in is_new

    process = body("void ProcessPair(")
    require(
        process,
        "GetDataForTimeframe(actual, PERIOD_M5",
        "UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_m5_buy_lifecycle",
        "UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_m5_sell_lifecycle",
        "UpdateReEntryState(g_pair_states[pairIndex].re_m5_buy_state",
        "UpdateReEntryState(g_pair_states[pairIndex].re_m5_sell_state",
        "NMJE_PrintEqualEligibilityCoherenceShadow(",
        "PriorityEngine_Atomic(",
    )
    for forbidden in (
        "DetectCSD(actual, PERIOD_M5",
        "DetectECSD(actual, PERIOD_M5",
        "DetectCSM(actual, PERIOD_M5",
    ):
        assert forbidden not in process, forbidden
    assert process.index("NMJE_PrintEqualEligibilityCoherenceShadow(") < process.index("PriorityEngine_Atomic(")

    build = body("void NMJE_BuildM5Refinement(")
    require(
        build,
        "snapshot.ParentEventID = journey.ParentEventID;",
        "snapshot.JourneyID = journey.JourneyID;",
        "snapshot.EventID = NMJE_M5ContextEventID",
        "M5_CONFIRMED_RE_ALIGNED",
        "M5_TEMPORARY_CONFIRMED_RE_OPPOSES_PARENT",
        "M5_CANDIDATE_RE_SUPPORTING",
        "M5_CANDIDATE_RETRACEMENT_BUILDING",
        "M5_EXTREME_SUPPORTING",
        "M5_TEMPORARY_EXTREME_OPPOSES_PARENT",
        "NMJE_M5LineageSnapshotValid(snapshot)",
    )
    assert "journey.Relation =" not in build
    for relation in (
        "snapshot.Relation = NESTED_ALIGNED;",
        "snapshot.Relation = NESTED_SUPPORTING;",
        "snapshot.Relation = NESTED_BUILDING;",
        "snapshot.Relation = NESTED_CONFLICT;",
    ):
        assert relation in build

    coherence = body("void NMJE_PrintEqualEligibilityCoherenceShadow(")
    require(
        coherence,
        "if(eligibleCount < 2) return;",
        "IsCandidateEligible(candidates[i])",
        "IsCandidateAllowedByD1Owner(candidates[i], pairState)",
        "[Q9-P2-COHERENCE]",
        "ParentMatch=",
        "M5Match=",
    )
    for forbidden in (
        "CompareCanonicalCandidates(",
        "PriorityEngine_Atomic(",
        "InvalidationEngine_Atomic(",
        "OrderSend(",
        "OrderClose(",
        "OrderModify(",
        "OrderDelete(",
    ):
        assert forbidden not in coherence, f"P2 authority leak: {forbidden}"

    # P2 remains metadata-only: no ranking/comparator change.
    comparator = body("int CompareCanonicalCandidates(")
    for forbidden in ("M5Refinement", "Q9-P2", "Coherence", "NMJE"):
        assert forbidden not in comparator, f"comparator drift: {forbidden}"

    priority = body("void PriorityEngine_Atomic(")
    for forbidden in ("M5Refinement", "Q9-P2-COHERENCE", "NMJE_PrintEqualEligibility"):
        assert forbidden not in priority, f"M15 selection leak: {forbidden}"

    invalidation = body("void InvalidationEngine_Atomic(")
    for forbidden in ("M5Refinement", "Q9-P2-COHERENCE", "re_m5_", "extreme_m5_"):
        assert forbidden not in invalidation, f"M16 leak: {forbidden}"

    for forbidden in (
        "NMJE_PassExecutionGate",
        "REJ_NMJE_RELATION",
        "REJ_NMJE_M5",
        "EnableNMJEM5Execution",
        "M5_PROCESSING_CLOCK",
        "M5_EXECUTION_AUTHORITY",
        "N3_POLICY_ACTIVE",
    ):
        assert forbidden not in SRC, f"authority leak: {forbidden}"

    assert SRC.count("OrderSend(") == 1
    assert SRC.count("OrderClose(") == 3
    assert SRC.count("OrderModify(") == 0
    assert SRC.count("OrderDelete(") == 0

    print("Q9_NMJE_P2P3_SHADOW_STATIC=PASS")

if __name__ == "__main__":
    main()
