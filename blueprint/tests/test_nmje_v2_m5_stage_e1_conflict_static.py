#!/usr/bin/env python3
"""Stage-E1 P5 deterministic conflict-subtype metadata firewall."""
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
        "enum ENUM_NMJE_CONFLICT_SUBTYPE",
        "NMJE_CONFLICT_TEMPORARY_RETRACEMENT",
        "NMJE_CONFLICT_LOCAL_CHILD_OPPOSITION",
        "NMJE_CONFLICT_PARENT_DIRECTION",
        "NMJE_CONFLICT_OWNER_TRANSITION",
        "NMJE_CONFLICT_STRUCTURAL",
        "NMJE_CONFLICT_UNRESOLVED_PROVENANCE",
        "ENUM_NMJE_CONFLICT_SUBTYPE ConflictSubtype;",
        "ENUM_NMJE_CONFLICT_SUBTYPE M5ConflictSubtype;",
        "ENUM_NMJE_CONFLICT_SUBTYPE   NMJEConflictSubtype;",
    )

    classify = function_body("NMJE_ClassifyConflictSubtype")
    require(
        classify,
        'StringFind(reason, "D1_TRANSITION")',
        "NMJE_CONFLICT_OWNER_TRANSITION",
        "relation == NESTED_UNRESOLVED",
        "NMJE_CONFLICT_UNRESOLVED_PROVENANCE",
        'StringFind(reason, "CANDIDATE_RETRACEMENT")',
        "NMJE_CONFLICT_TEMPORARY_RETRACEMENT",
        'StringFind(reason, "H4_LOCAL_OPPOSES_D1")',
        "NMJE_CONFLICT_PARENT_DIRECTION",
        'StringFind(reason, "OPPOSES_PARENT")',
        "NMJE_CONFLICT_LOCAL_CHILD_OPPOSITION",
        "relation == NESTED_CONFLICT",
        "NMJE_CONFLICT_STRUCTURAL",
    )

    m5_commit = function_body("NMJE_CommitM5Refinement")
    require(
        m5_commit,
        "NMJE_ClassifyConflictSubtype(snapshot.Relation, snapshot.Reason)",
        "journey.M5Refinement = snapshot;",
    )

    update = function_body("UpdateNestedJourneyObservation")
    require(
        update,
        "journey.ConflictSubtype =",
        "NMJE_ClassifyConflictSubtype(journey.Relation, journey.Reason)",
        "NMJE_BuildM5Refinement(g_pair_states[pairIndex], journey)",
        "NMJE_ConflictSubtypeText(journey.ConflictSubtype)",
        "NMJE_ConflictSubtypeText(journey.M5Refinement.ConflictSubtype)",
    )
    if update.rindex("NMJE_ClassifyConflictSubtype(journey.Relation, journey.Reason)") > update.index(
        "NMJE_BuildM5Refinement(g_pair_states[pairIndex], journey)"
    ):
        raise AssertionError("base conflict subtype is not finalized before M5 binding")

    freeze = function_body("FreezeNMJEShadowSnapshot")
    validate = function_body("ValidateNMJEShadowSnapshot")
    require(freeze, "decision.NMJEConflictSubtype = journey.ConflictSubtype;")
    require(
        validate,
        "current.ConflictSubtype != decision.NMJEConflictSubtype",
        "frozenM5.ConflictSubtype != currentM5.ConflictSubtype",
    )

    build = function_body("BuildNMJEShadowAttribution")
    save = function_body("SaveNMJEShadowAttribution")
    load = function_body("LoadNMJEShadowAttribution")
    outcome = function_body("NMJE_PrintClosedOutcomeShadow")
    require(
        build,
        "attribution.ConflictSubtype = decision.NMJEConflictSubtype;",
        "attribution.M5ConflictSubtype = m5.ConflictSubtype;",
    )
    require(
        save,
        'GlobalVariableSet(base + "C", (double)a.ConflictSubtype)',
        'GlobalVariableSet(base + "M5C", (double)a.M5ConflictSubtype)',
    )
    require(
        load,
        'GlobalVariableGet(base + "C")',
        'GlobalVariableGet(base + "M5C")',
        "NMJE_CONFLICT_UNRESOLVED_PROVENANCE",
    )
    require(
        outcome,
        '" SUB="',
        "NMJE_ConflictSubtypeText(info.nmje_attribution.ConflictSubtype)",
        '" M5SUB="',
        "NMJE_ConflictSubtypeText(info.nmje_attribution.M5ConflictSubtype)",
    )

    # P5 is descriptive only. It cannot participate in eligibility, candidate
    # comparison, risk, execution, lifecycle, or M16 outcome control.
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
            "ConflictSubtype",
            "NMJE_ClassifyConflictSubtype",
            "NMJE_ConflictSubtypeText",
        ):
            if forbidden in body:
                raise AssertionError(f"P5 authority leak in {name}: {forbidden}")

    invalidation = function_body("InvalidationEngine_Atomic")
    shadow_start = invalidation.index("bool nmjeShadowMatch")
    validated = invalidation.index("decision.DecisionState = DEC_VALIDATED;", shadow_start)
    shadow_segment = invalidation[shadow_start:validated]
    require(shadow_segment, "NMJE_ConflictSubtypeText(decision.NMJEConflictSubtype)")
    for forbidden in ("return;", "DEC_REJECTED", "DEC_INVALIDATED", "RejectionReason ="):
        if forbidden in shadow_segment:
            raise AssertionError(f"P5 subtype gained M16 authority: {forbidden}")

    for forbidden in (
        "EnableNMJEConflictGate",
        "REJ_NMJE_CONFLICT",
        "NMJE_CONFLICT_SCORE",
    ):
        if forbidden in SRC:
            raise AssertionError(f"P5 activation marker present: {forbidden}")

    print("NMJE_V2_M5_STAGE_E1_P5_CONFLICT_STATIC=PASS")


if __name__ == "__main__":
    main()

