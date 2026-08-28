#!/usr/bin/env python3
"""Stage-E3 P7 structural-presence metadata firewall."""
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
        "int                  StructureMask;",
        "int                  StructureCount;",
        "int                  RequirementCompleteness;",
        "int                  SequenceCompleteness;",
        "int                          NMJEStructureMask;",
        "int                          NMJEStructureCount;",
        "int                          NMJERequirementCompleteness;",
        "int                          NMJESequenceCompleteness;",
    )

    mask = function_body("NMJE_BuildStructureMask")
    require(
        mask,
        "NMJE_NodeSupportsDirection(journey.D1Node, direction)",
        "NMJE_NodeSupportsDirection(journey.H4Node, direction)",
        "NMJE_NodeSupportsDirection(journey.H1Node, direction)",
        "NMJE_NodeSupportsDirection(journey.M15Node, direction)",
        "journey.M5Refinement.Present",
        "journey.M5Refinement.Direction == direction",
        "journey.M5Refinement.Relation == NESTED_SUPPORTING",
        "journey.M5Refinement.Relation == NESTED_ALIGNED",
        "mask |= 1",
        "mask |= 2",
        "mask |= 4",
        "mask |= 8",
        "mask |= 16",
    )
    for forbidden in ("Score", "Weight", "Threshold", "MarketInfo", "iRSI", "iMACD"):
        if forbidden in mask:
            raise AssertionError(f"density is not pure structure presence: {forbidden}")

    priority = function_body("PriorityEngine_Atomic")
    require(
        priority,
        "decision.NMJERequirementCompleteness = selected.RequirementCompleteness;",
        "decision.NMJESequenceCompleteness = selected.SequenceCompleteness;",
        "FreezeNMJEShadowSnapshot(pairState, decision);",
    )
    if priority.index("decision.NMJERequirementCompleteness") > priority.index(
        "FreezeNMJEShadowSnapshot(pairState, decision)"
    ):
        raise AssertionError("selected completeness is not frozen after selection")

    freeze = function_body("FreezeNMJEShadowSnapshot")
    validate = function_body("ValidateNMJEShadowSnapshot")
    require(
        freeze,
        "NMJE_BuildStructureMask(journey, decision.Direction)",
        "NMJE_CountStructureBits(decision.NMJEStructureMask)",
    )
    require(
        validate,
        "NMJE_BuildStructureMask(current, decision.Direction)",
        "STRUCTURE_DENSITY_MISMATCH",
    )

    build = function_body("BuildNMJEShadowAttribution")
    save = function_body("SaveNMJEShadowAttribution")
    load = function_body("LoadNMJEShadowAttribution")
    outcome = function_body("NMJE_PrintClosedOutcomeShadow")
    require(
        build,
        "attribution.StructureMask = decision.NMJEStructureMask;",
        "attribution.StructureCount = decision.NMJEStructureCount;",
        "attribution.RequirementCompleteness = decision.NMJERequirementCompleteness;",
        "attribution.SequenceCompleteness = decision.NMJESequenceCompleteness;",
    )
    require(
        save,
        'GlobalVariableSet(base + "SM", (double)a.StructureMask)',
        'GlobalVariableSet(base + "SC", (double)a.StructureCount)',
        'GlobalVariableSet(base + "RQ", (double)a.RequirementCompleteness)',
        'GlobalVariableSet(base + "SQ", (double)a.SequenceCompleteness)',
    )
    require(
        load,
        "NMJE_CountStructureBits(info.nmje_attribution.StructureMask)",
        "info.nmje_attribution.StructureCount",
    )
    require(
        outcome,
        '" SM="',
        '" SC="',
        '" RQ="',
        '" SQ="',
    )

    # Density and completeness are frozen after canonical selection and never
    # enter eligibility, comparison, risk, execution, lifecycle, or M16 result.
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
        for forbidden in (
            "NMJEStructure",
            "NMJERequirementCompleteness",
            "NMJESequenceCompleteness",
            "NMJE_BuildStructureMask",
        ):
            if forbidden in body:
                raise AssertionError(f"P7 authority leak in {name}: {forbidden}")

    invalidation = function_body("InvalidationEngine_Atomic")
    shadow_start = invalidation.index("bool nmjeShadowMatch")
    validated = invalidation.index("decision.DecisionState = DEC_VALIDATED;", shadow_start)
    segment = invalidation[shadow_start:validated]
    require(segment, "StructureMask=", "StructureCount=", '" Req="', '" Seq="')
    for forbidden in ("return;", "DEC_REJECTED", "DEC_INVALIDATED", "RejectionReason ="):
        if forbidden in segment:
            raise AssertionError(f"P7 density gained M16 authority: {forbidden}")

    for forbidden in (
        "NMJE_DENSITY_SCORE",
        "MinNMJEStructureCount",
        "REJ_NMJE_DENSITY",
        "EnableNMJEDensityGate",
    ):
        if forbidden in SRC:
            raise AssertionError(f"P7 activation marker present: {forbidden}")

    print("NMJE_V2_M5_STAGE_E3_P7_DENSITY_STATIC=PASS")


if __name__ == "__main__":
    main()

