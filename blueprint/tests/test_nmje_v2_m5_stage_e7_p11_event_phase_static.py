#!/usr/bin/env python3
"""Stage-E7 P11 first/continuation/new-journey lineage firewall."""
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
        "enum ENUM_NMJE_EVENT_PHASE",
        "NMJE_EVENT_PHASE_UNRESOLVED",
        "NMJE_EVENT_PHASE_FIRST",
        "NMJE_EVENT_PHASE_CONTINUATION",
        "NMJE_EVENT_PHASE_NEW_JOURNEY",
        "ENUM_NMJE_EVENT_PHASE EventPhase;",
        "bool                 EventPhaseCheckpointDurable;",
        "ENUM_NMJE_EVENT_PHASE   EventPhase;",
        "bool                    EventPhaseCheckpointDurable;",
        "ENUM_NMJE_EVENT_PHASE        NMJEEventPhase;",
        "bool                         NMJEEventPhaseCheckpointDurable;",
    )

    load_checkpoint = function_body("LoadNMJEEventPhaseCheckpoint")
    save_checkpoint = function_body("SaveNMJEEventPhaseCheckpoint")
    require(
        load_checkpoint,
        'GlobalVariableCheck(base + "V")',
        'GlobalVariableCheck(base + "H")',
        'GlobalVariableCheck(base + "F")',
        'GlobalVariableCheck(base + "T")',
        'NMJELoadHex16(base, "J", journeyHash)',
        'NMJELoadHex16(base, "P", parentEventHash)',
        'NMJELoadHex16(base, "D", d1EventHash)',
    )
    require(
        save_checkpoint,
        'GlobalVariableDel(base + "V")',
        'GlobalVariableSet(base + "H"',
        'GlobalVariableSet(base + "F"',
        'GlobalVariableSet(base + "T"',
        'NMJEStoreHex16(base, "J", journeyHash)',
        'NMJEStoreHex16(base, "P", parentEventHash)',
        'NMJEStoreHex16(base, "D", d1EventHash)',
        'GlobalVariableSet(base + "V", 1.0)',
    )
    if save_checkpoint.index('GlobalVariableSet(base + "V", 1.0)') < save_checkpoint.index(
        'NMJEStoreHex16(base, "D", d1EventHash)'
    ):
        raise AssertionError("P11 checkpoint version is not written last")

    update = function_body("UpdateNestedJourneyObservation")
    require(
        update,
        "journey.EventPhase = NMJE_EVENT_PHASE_UNRESOLVED;",
        "LoadNMJEEventPhaseCheckpoint(",
        "priorPhaseUpdateCandle == journey.UpdateCandleTime",
        "? priorEventPhase : NMJE_EVENT_PHASE_UNRESOLVED;",
        "priorPhaseUpdateCandle < journey.UpdateCandleTime",
        "if(!priorPhaseHadParent)",
        "journey.EventPhase = NMJE_EVENT_PHASE_FIRST;",
        "else if(samePriorIdentity)",
        "journey.EventPhase = NMJE_EVENT_PHASE_CONTINUATION;",
        "journey.EventPhase = NMJE_EVENT_PHASE_NEW_JOURNEY;",
        "priorJourneyHash == currentJourneyHash",
        "priorParentEventHash == currentParentEventHash",
        "priorD1EventHash == currentD1EventHash",
        "SaveNMJEEventPhaseCheckpoint(",
        "PHASE=",
        "PDUR=",
    )
    for forbidden in (
        "TimeCurrent",
        "GetTickCount",
        "newest",
        "oldest",
        "CompareCanonicalCandidates",
        "DecisionState",
        "RejectionReason",
    ):
        if forbidden in update:
            raise AssertionError(f"P11 phase is not identity-only: {forbidden}")

    freeze = function_body("FreezeNMJEShadowSnapshot")
    validate = function_body("ValidateNMJEShadowSnapshot")
    build = function_body("BuildNMJEShadowAttribution")
    require(
        freeze,
        "decision.NMJEEventPhase = journey.EventPhase;",
        "journey.EventPhaseCheckpointDurable;",
    )
    require(
        validate,
        "current.EventPhase != decision.NMJEEventPhase",
        "EVENT_PHASE_METADATA_MISMATCH",
    )
    require(
        build,
        "attribution.EventPhase = decision.NMJEEventPhase;",
        "decision.NMJEEventPhaseCheckpointDurable;",
    )

    save = function_body("SaveNMJEShadowAttribution")
    load = function_body("LoadNMJEShadowAttribution")
    outcome = function_body("NMJE_PrintClosedOutcomeShadow")
    require(
        save,
        'GlobalVariableSet(base + "F", (double)a.EventPhase)',
        'GlobalVariableSet(base + "FD", a.EventPhaseCheckpointDurable ? 1.0 : 0.0)',
        'GlobalVariableSet(base + "V", 3.0)',
    )
    require(
        load,
        "attributionVersion != 1 && attributionVersion != 2 &&",
        "attributionVersion != 3",
        "if(attributionVersion >= 3)",
        'GlobalVariableCheck(base + "F")',
        'GlobalVariableCheck(base + "FD")',
    )
    require(outcome, '" PHASE="', '" FDUR="')

    for name in (
        "BuildPossibleCombinations",
        "CompareCanonicalCandidates",
        "IsCandidateEligible",
        "CalculateLotSize",
        "CheckRiskBeforeTrade",
        "SendOrderWithRetry",
        "AdvanceD1TPWLifecycleForPair",
        "AdvanceC044OwnerEventsForPair",
    ):
        body = function_body(name)
        for forbidden in ("NMJEEventPhase", "NMJE_EVENT_PHASE", "EventPhaseCheckpoint"):
            if forbidden in body:
                raise AssertionError(f"P11 authority leak in {name}: {forbidden}")

    for forbidden in (
        "EnableFirstEventGate",
        "PreferNewestJourney",
        "PreferEarliestJourney",
        "REJ_EVENT_PHASE",
        "DelayForContinuation",
    ):
        if forbidden in SRC:
            raise AssertionError(f"P11 activation marker present: {forbidden}")

    require(
        SRC,
        "Version 4.7.0 - NMJE v2 Event Phase Lineage",
        '#property version   "4.70"',
    )
    print("NMJE_V2_M5_STAGE_E7_P11_EVENT_PHASE_STATIC=PASS")


if __name__ == "__main__":
    main()

