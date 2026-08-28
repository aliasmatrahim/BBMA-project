#!/usr/bin/env python3
"""Stage-E4 P8 parent-provenance stability firewall."""
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
        "bool                    ParentRetained;",
        "string                  ParentSelectionReason;",
        "bool                         NMJEParentRetained;",
        "string                       NMJEParentSelectionReason;",
        "bool                 ParentRetained;",
        "string               ParentSelectionReasonHash;",
    )

    retain = function_body("NMJE_TryRetainPreviousParent")
    require(
        retain,
        "previous.ParentEventID == \"\"",
        "previous.JourneyID == \"\"",
        "NMJE_BuildD1Node(state, currentD1)",
        "currentD1.CanonicalEventID != previous.D1Node.CanonicalEventID",
        "previous.ParentKind == NESTED_PARENT_H4_RE",
        "NMJE_ReEntryEventID(state.actual_symbol, selected)",
        "previous.ParentKind == NESTED_PARENT_H4_OWNER",
        "NMJE_H4OwnerEventID(state.actual_symbol",
        "previous.ParentKind == NESTED_PARENT_D1_RE",
        "previous.ParentKind == NESTED_PARENT_D1_OWNER",
        "NMJE_D1OwnerEventID(state.actual_symbol",
        'reason = "PREVIOUS_CANONICAL_PARENT_RETAINED";',
    )
    for forbidden in (
        "TimeCurrent",
        "GetTickCount",
        "Sleep(",
        "candleCount",
        "waitBars",
        "DecisionState",
        "RejectionReason",
    ):
        if forbidden in retain:
            raise AssertionError(f"P8 is not provenance-only: {forbidden}")

    update = function_body("UpdateNestedJourneyObservation")
    require(
        update,
        "NestedJourneyState previousJourney = g_nested_journeys[pairIndex];",
        "NMJE_TryRetainPreviousParent(",
        "if(!hasParent)",
        "hasParent = NMJE_ResolveParent(",
        "journey.ParentRetained = parentRetained;",
        "PREVIOUS_CANONICAL_PARENT_RETAINED",
        "CANONICAL_PARENT_TRANSITION",
        "CANONICAL_PARENT_SELECTED",
        "PREVIOUS_PARENT_INVALID_NO_REPLACEMENT",
    )
    if update.index("NMJE_TryRetainPreviousParent(") > update.index(
        "hasParent = NMJE_ResolveParent("
    ):
        raise AssertionError("fresh parent selection bypasses prior canonical parent")

    freeze = function_body("FreezeNMJEShadowSnapshot")
    validate = function_body("ValidateNMJEShadowSnapshot")
    require(
        freeze,
        "decision.NMJEParentRetained = journey.ParentRetained;",
        "decision.NMJEParentSelectionReason = journey.ParentSelectionReason;",
    )
    require(
        validate,
        "current.ParentRetained != decision.NMJEParentRetained",
        "current.ParentSelectionReason != decision.NMJEParentSelectionReason",
        "PARENT_STABILITY_METADATA_MISMATCH",
    )

    build = function_body("BuildNMJEShadowAttribution")
    save = function_body("SaveNMJEShadowAttribution")
    load = function_body("LoadNMJEShadowAttribution")
    outcome = function_body("NMJE_PrintClosedOutcomeShadow")
    require(
        build,
        "attribution.ParentRetained = decision.NMJEParentRetained;",
        "SHORT_HASH(decision.NMJEParentSelectionReason)",
    )
    require(
        save,
        'GlobalVariableSet(base + "PR", a.ParentRetained ? 1.0 : 0.0)',
        'NMJEStoreHex16(base, "A", a.ParentSelectionReasonHash)',
    )
    require(
        load,
        'NMJELoadHex16(base, "A", info.nmje_attribution.ParentSelectionReasonHash)',
        'GlobalVariableGet(base + "PR")',
    )
    require(outcome, '" PR="', '" PAH="')

    # Parent retention is used only by the descriptive journey observer.
    for name in (
        "BuildPossibleCombinations",
        "CompareCanonicalCandidates",
        "IsCandidateEligible",
        "PriorityEngine_Atomic",
        "CalculateLotSize",
        "CheckRiskBeforeTrade",
        "SendOrderWithRetry",
        "AdvanceD1TPWLifecycleForPair",
        "AdvanceC044OwnerEventsForPair",
    ):
        body = function_body(name)
        for forbidden in (
            "NMJE_TryRetainPreviousParent",
            "NMJEParentRetained",
            "NMJEParentSelectionReason",
        ):
            if forbidden in body:
                raise AssertionError(f"P8 authority leak in {name}: {forbidden}")

    invalidation = function_body("InvalidationEngine_Atomic")
    shadow_start = invalidation.index("bool nmjeShadowMatch")
    validated = invalidation.index("decision.DecisionState = DEC_VALIDATED;", shadow_start)
    segment = invalidation[shadow_start:validated]
    require(segment, "ParentRetained=", "ParentSelection=")
    for forbidden in ("return;", "DEC_REJECTED", "DEC_INVALIDATED", "RejectionReason ="):
        if forbidden in segment:
            raise AssertionError(f"P8 stability gained M16 authority: {forbidden}")

    for forbidden in (
        "EnableNMJEHysteresisGate",
        "NMJEParentWaitBars",
        "REJ_NMJE_HYSTERESIS",
        "DelayM15ForNMJE",
    ):
        if forbidden in SRC:
            raise AssertionError(f"P8 timing/activation marker present: {forbidden}")

    print("NMJE_V2_M5_STAGE_E4_P8_STABILITY_STATIC=PASS")


if __name__ == "__main__":
    main()

