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
    raise AssertionError(signature)

def require(text: str, *markers: str) -> None:
    for marker in markers:
        assert marker in text, marker

def main() -> None:
    require(
        SRC,
        "Version 4.9.3 - Q9 NMJE Provenance Stability",
        '#property version   "4.93"',
        '#define BBMA_BUILD_TAG      "V493_Q9_P8_PROVENANCE_STABILITY_20260919"',
        '#define BBMA_SOURCE_REV_TAG "Q9_P8_PROVENANCE_STABILITY_101_20260919"',
        "ENUM_NESTED_RELATION StableRelation;",
        "string               StableEventID;",
        "string               StabilityReason;",
        "string                  RelationEvidenceID;",
        "string                  StableRelationEvidenceID;",
        "bool                    ParentTransitioned;",
        "string                  PreviousParentEventID;",
        "ENUM_NESTED_RELATION         NMJEStableRelation;",
        "string                       NMJEStableRelationEvidenceID;",
    )

    # Raw parent source precedence remains current-owner based only.
    parent = body("bool NMJE_ResolveParent(")
    require(
        parent,
        "NMJE_SelectConfirmedRE(state.re_h4_buy_state",
        "state.h4_direction_owner.State == H4_OWNER_ACTIVE",
        "NMJE_SelectConfirmedRE(state.re_d1_buy_state",
        "D1_OWNER_BUY_CONFIRMED",
        "D1_OWNER_SELL_CONFIRMED",
    )
    for forbidden in (
        "NMJE_SelectCandidateRE(",
        "re_h1_",
        "re_m15_",
        "re_m5_",
        "extreme_h1_",
        "extreme_m15_",
        "extreme_m5_",
        "StableRelation",
    ):
        assert forbidden not in parent, forbidden

    relation_evidence = body("string NMJE_BuildRelationEvidenceID(")
    require(
        relation_evidence,
        'journey.Reason == "H1_RE_ALIGNED_WITH_PARENT"',
        'journey.Reason == "CONFIRMED_H1_RE_OPPOSES_PARENT"',
        'journey.Reason == "LTF_STRUCTURE_SUPPORTING_PARENT"',
        'journey.Reason == "H4_LOCAL_OPPOSES_D1"',
        'journey.Reason == "H4_OWNER_ALIGNED_WITH_D1"',
        "NMJE_D1OwnerEventID(state.actual_symbol",
        "(int)state.d1_major_trend_owner.State",
        "NMJE_SelectConfirmedRE(state.re_h1_buy_state",
        "NMJE_IsExtremeSupporting(state.extreme_h1_buy_lifecycle)",
        "NMJE_IsMLVSupporting(state.mlv_buy_state)",
        "NMJE_IdentityHash(evidence)",
    )
    assert "journey.D1Node.CanonicalEventID" not in relation_evidence
    # Candidate/developing child state is deliberately not promoted to stable evidence.
    assert "NMJE_SelectCandidateRE(" not in relation_evidence
    assert "NMJE_IsExtremeActive(" not in relation_evidence
    assert "NMJE_IsMLVActive(" not in relation_evidence

    stable = body("void NMJE_ApplyJourneyProvenanceStability(")
    require(
        stable,
        "previous.ParentEventID",
        "previous.JourneyID",
        "journey.ParentTransitioned = true;",
        'journey.StabilityReason = "PARENT_CONTEXT_LOST";',
        '"PARENT_TRANSITION_CURRENT_EVIDENCE"',
        '"PARENT_TRANSITION_RAW_INIT"',
        '"CURRENT_CANONICAL_EVIDENCE"',
        '"HOLD_LAST_PROVEN_RELATION"',
        "previous.StableRelationEvidenceID",
        "previous.StableRelation",
    )
    for forbidden in (
        "Sleep(",
        "TimeCurrent(",
        "GetProcessingBarIndex",
        "MaxWaitBars",
        "CandidateExpiry",
        "PriorityTier",
        "RejectionReason",
        "OrderSend(",
    ):
        assert forbidden not in stable, forbidden

    m5stable = body("bool NMJE_M5HasStableEvidence(")
    require(
        m5stable,
        "RE_STATE_CONFIRMED",
        "EXT_MAT_REVERSAL_CONFIRMED",
        "EXT_MAT_RETEST_PHASE",
        "EXT_MAT_RETEST_READY",
    )
    assert "RE_STATE_CANDIDATE" not in m5stable
    assert "EXT_MAT_RAW" not in m5stable

    apply_m5 = body("void NMJE_ApplyM5ProvenanceStability(")
    require(
        apply_m5,
        "NMJE_M5HasStableEvidence(current)",
        "previous.M5Refinement.StableEventID",
        '"HOLD_LAST_PROVEN_M5_RELATION"',
        '"PARENT_TRANSITION_CLEARS_M5_STABILITY"',
    )
    assert "current.Present = true" not in apply_m5

    update = body("void UpdateNestedJourneyObservation(")
    require(
        update,
        "NestedJourneyState previous = g_nested_journeys[pairIndex];",
        "NMJE_ApplyJourneyProvenanceStability(g_pair_states[pairIndex]",
        "NMJE_BuildM5Refinement(g_pair_states[pairIndex], journey);",
        "NMJE_ApplyM5ProvenanceStability(previous, journey);",
        "NMJE_PrintProvenanceStability(journey);",
        '" SREL="',
        '" PTR="',
    )
    build_pos = update.index("NMJE_BuildM5Refinement(g_pair_states[pairIndex], journey);")
    apply_pos = update.index("NMJE_ApplyM5ProvenanceStability(previous, journey);", build_pos)
    assert build_pos < apply_pos

    telemetry = body("void NMJE_PrintProvenanceStability(")
    require(
        telemetry,
        "[Q9-P8-STABILITY]",
        '" REL="',
        '" SREL="',
        '" RE="',
        '" SE="',
        '" PTR="',
        '" PPE="',
        '" M5REL="',
        '" M5SREL="',
        '" M5STAB="',
    )

    freeze = body("void NMJE_FreezeValidatedDecisionAttribution(")
    require(
        freeze,
        "decision.DecisionState != DEC_VALIDATED",
        "decision.NMJEStableRelation = journey.StableRelation;",
        "decision.NMJEStableRelationEvidenceID = journey.StableRelationEvidenceID;",
        "decision.NMJEParentTransitioned = journey.ParentTransitioned;",
        "decision.NMJEPreviousParentEventID = journey.PreviousParentEventID;",
    )

    decision_shadow = body("void NMJE_PrintValidatedDecisionShadow(")
    require(decision_shadow, '" SREL="', '" SE="', '" PTR="', '" PPE="')

    # P8 is deliberately in-memory/frozen shadow metadata only. Durable P4-P7
    # trade-attribution persistence is not widened by this patch.
    for signature in (
        "bool BuildNMJEShadowAttribution(",
        "bool LoadNMJEShadowAttribution(",
        "bool SaveNMJEShadowAttribution(",
        "void ClearNMJEShadowAttribution(",
    ):
        segment = body(signature)
        for marker in ("NMJEStableRelation", "StableRelationEvidenceID",
                       "ParentTransitioned", "PreviousParentEventID",
                       "StableEventID"):
            assert marker not in segment, f"{signature}:{marker}"

    # Hard authority firewall.
    protected = (
        ("BuildPossibleCombinations", "void BuildPossibleCombinations("),
        ("ValidateSequence", "void ValidateSequence("),
        ("BuildConfirmedReEntryCandidate", "void BuildConfirmedReEntryCandidate("),
        ("BuildStandaloneExtremeCandidate", "void BuildStandaloneExtremeCandidate("),
        ("BuildD1OpportunityCandidate", "void BuildD1OpportunityCandidate("),
        ("CompareCanonicalCandidates", "int CompareCanonicalCandidates("),
        ("PriorityEngine_Atomic", "void PriorityEngine_Atomic("),
        ("InvalidationEngine_Atomic", "void InvalidationEngine_Atomic("),
        ("CheckRiskBeforeTrade", "RiskStatus CheckRiskBeforeTrade("),
        ("RunEntryPreflightAndExecute", "bool RunEntryPreflightAndExecute("),
        ("IsSignalAllowed", "bool IsSignalAllowed("),
        ("SendOrderWithRetry", "int SendOrderWithRetry("),
    )
    for name, signature in protected:
        segment = body(signature)
        for marker in ("StableRelation", "RelationEvidenceID", "ParentTransitioned",
                       "PreviousParentEventID", "Q9-P8-STABILITY"):
            assert marker not in segment, f"{name}:{marker}"

    for forbidden in (
        "MinStableRelationBars",
        "RelationCooldown",
        "HysteresisBars",
        "REJ_NMJE_STABILITY",
        "EnableNMJEStabilityGate",
        "StableRelationScore",
    ):
        assert forbidden not in SRC, forbidden

    assert SRC.count("OrderSend(") == 1
    assert SRC.count("OrderClose(") == 3
    assert SRC.count("OrderModify(") == 0
    assert SRC.count("OrderDelete(") == 0
    print("Q9_NMJE_P8_PROVENANCE_STABILITY_STATIC=PASS")

if __name__ == "__main__":
    main()
