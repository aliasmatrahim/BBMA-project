#!/usr/bin/env python3
"""Stage-C2 M5 shadow classification and authority firewall for Issue #101."""
from pathlib import Path
import re


SRC = Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")


def function_body(name: str) -> str:
    match = re.search(rf"\b{re.escape(name)}\s*\([^)]*\)\s*\{{", SRC, re.S)
    if not match:
        raise AssertionError(f"missing function: {name}")
    start = match.end() - 1
    depth = 0
    for index in range(start, len(SRC)):
        if SRC[index] == "{":
            depth += 1
        elif SRC[index] == "}":
            depth -= 1
            if depth == 0:
                return SRC[start + 1:index]
    raise AssertionError(f"unterminated function: {name}")


def require(text: str, *markers: str) -> None:
    for marker in markers:
        if marker not in text:
            raise AssertionError(f"missing marker: {marker}")


def main() -> None:
    require(
        SRC,
        "NMJE_M5_CONTEXT_RE_ENTRY = 1",
        "NMJE_M5_CONTEXT_EXTREME = 2",
        "ReEntryData          re_m5_buy_state;",
        "ReEntryData          re_m5_sell_state;",
        "ExtremeLifecycleData extreme_m5_buy_lifecycle;",
        "ExtremeLifecycleData extreme_m5_sell_lifecycle;",
        "state.re_m5_buy_state.Timeframe = PERIOD_M5;",
        "state.re_m5_sell_state.Timeframe = PERIOD_M5;",
        "state.extreme_m5_buy_lifecycle.Timeframe = PERIOD_M5;",
        "state.extreme_m5_sell_lifecycle.Timeframe = PERIOD_M5;",
    )

    process = function_body("ProcessPair")
    require(
        process,
        "DetectExtreme(actual, DIR_BUY,\n                                         g_pair_states[pairIndex].m5_data, m5Band)",
        "DetectExtreme(actual, DIR_SELL,\n                                          g_pair_states[pairIndex].m5_data, m5Band)",
        "UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_m5_buy_lifecycle",
        "UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_m5_sell_lifecycle",
        "ResolveOppositeExtremeSupersession(g_pair_states[pairIndex].extreme_m5_buy_lifecycle",
        "UpdateReEntryState(g_pair_states[pairIndex].re_m5_buy_state",
        "UpdateReEntryState(g_pair_states[pairIndex].re_m5_sell_state",
    )

    build = function_body("NMJE_BuildM5Refinement")
    require(
        build,
        "NMJE_SelectConfirmedRE(state.re_m5_buy_state",
        "NMJE_SelectCandidateRE(state.re_m5_buy_state",
        "NMJE_IsExtremeActive(state.extreme_m5_buy_lifecycle)",
        "NMJE_IsExtremeActive(state.extreme_m5_sell_lifecycle)",
        "snapshot.ParentEventID = journey.ParentEventID;",
        "snapshot.JourneyID = journey.JourneyID;",
        "snapshot.ClosedCandleTime = state.m5_data.candle_time;",
        "snapshot.EventID = NMJE_M5ContextEventID",
        "NMJE_M5LineageSnapshotValid(snapshot)",
        "M5_CONFIRMED_RE_ALIGNED",
        "M5_TEMPORARY_CONFIRMED_RE_OPPOSES_PARENT",
        "M5_CANDIDATE_RE_SUPPORTING",
        "M5_CANDIDATE_RETRACEMENT_BUILDING",
        "M5_EXTREME_SUPPORTING",
        "M5_TEMPORARY_EXTREME_OPPOSES_PARENT",
    )
    for relation in (
        "snapshot.Relation = NESTED_ALIGNED;",
        "snapshot.Relation = NESTED_SUPPORTING;",
        "snapshot.Relation = NESTED_BUILDING;",
        "snapshot.Relation = NESTED_CONFLICT;",
    ):
        if relation not in build:
            raise AssertionError(f"canonical relation mapping missing: {relation}")

    update = function_body("UpdateNestedJourneyObservation")
    parent_index = update.index("journey.ParentEventID = parentEventID;")
    journey_index = update.index("journey.JourneyID = NMJE_BuildJourneyID")
    shadow_index = update.index("NMJE_BuildM5Refinement(")
    store_index = update.index("g_nested_journeys[pairIndex] = journey;", shadow_index)
    if not (parent_index < journey_index < shadow_index < store_index):
        raise AssertionError("M5 shadow lineage is not bound after parent/journey identity")

    # M5 cannot create a clock or any independent signal family.
    is_new = function_body("IsNewCandle")
    if "PERIOD_M5" in is_new or "M5_CandleTime" in is_new:
        raise AssertionError("M5 processing clock authority introduced")
    for forbidden in (
        "DetectCSD(actual, PERIOD_M5",
        "DetectECSD(actual, PERIOD_M5",
        "DetectCSM(actual, PERIOD_M5",
        "EnableNMJEM5Execution",
        "M5_PROCESSING_CLOCK",
        "M5_EXECUTION_AUTHORITY",
        "REJ_NMJE_M5",
    ):
        if forbidden in SRC:
            raise AssertionError(f"M5 authority or signal-family leak: {forbidden}")

    # Prove M5 state/refinement is absent from candidate, ranking, rejection,
    # execution, D1TPW and C044 owner-consumption paths.
    authority_functions = (
        "BuildPossibleCombinations",
        "PriorityEngine_Atomic",
        "InvalidationEngine_Atomic",
        "ProcessEntry",
        "RunEntryPreflightAndExecute",
        "AdvanceD1TPWLifecycleForPair",
        "AdvanceC044OwnerEventsForPair",
        "GetC044OwnerReEntrySnapshot",
        "GetC044OwnerExtremeSnapshot",
    )
    for name in authority_functions:
        body = function_body(name)
        for forbidden in ("re_m5_", "extreme_m5_", "M5Refinement"):
            if forbidden in body:
                raise AssertionError(f"M5 decision-path leak in {name}: {forbidden}")

    if process.index("UpdateNestedJourneyObservation(pairIndex);") > process.index(
        "PriorityEngine_Atomic("
    ):
        raise AssertionError("shadow observation moved after final M15 authority")

    print("NMJE_V2_M5_STAGE_C2_SHADOW_STATIC=PASS")


if __name__ == "__main__":
    main()

