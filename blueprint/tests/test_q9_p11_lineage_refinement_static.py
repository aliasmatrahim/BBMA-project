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
        "Version 4.9.6 - Q9 Strict Journey Lineage",
        '#property version   "4.96"',
        '#define BBMA_BUILD_TAG      "V496_Q9_P11_STRICT_JOURNEY_LINEAGE_20260920"',
        '#define BBMA_SOURCE_REV_TAG "Q9_P11_STRICT_JOURNEY_LINEAGE_101_20260920"',
        '[F7-BUILD] EA=BBMA_EA Build=4.96 BuildTag=',
        "enum ENUM_NMJE_LINEAGE_EVENT_CLASS",
        "NMJE_LINEAGE_NONE",
        "NMJE_LINEAGE_FIRST",
        "NMJE_LINEAGE_CONTINUATION",
        "NMJE_LINEAGE_NEW_JOURNEY",
        "NMJE_LINEAGE_UNRESOLVED",
        "ENUM_NMJE_LINEAGE_EVENT_CLASS LineageClass;",
        "string                  LineageRootEventID;",
        "string                  PreviousLineageRootEventID;",
        "ENUM_NMJE_LINEAGE_EVENT_CLASS NMJELineageClass;",
        "string                       NMJELineageRootEventID;",
        "string                       NMJEPreviousLineageRootEventID;",
        "ENUM_NMJE_LINEAGE_EVENT_CLASS LineageClass;",
        "string               LineageRootHash;",
        "string               PreviousLineageRootHash;",
    )

    canonical = body("bool NMJE_IsCanonicalLineageEventID(")
    require(canonical, "StringLen(eventID) == 16")

    root = body("bool NMJE_ResolveLineageRootEventID(")
    require(
        root,
        "journey.ParentEventID",
        "journey.JourneyID",
        "NMJE_IsCanonicalLineageEventID(journey.ParentEventID)",
        'reason = "CANONICAL_JOURNEY_ROOT";',
    )
    for forbidden in (
        "D1_OWNER_BUY_CONFIRMED",
        "D1_OWNER_SELL_CONFIRMED",
        "NMJE_D1OwnerEventID(",
        "H4_OWNER_ACTIVE",
        "NMJE_H4OwnerEventID(",
        "OrderSend(",
        "PriorityTier",
        "RejectionReason",
        "Candidate",
        "Sleep(",
    ):
        assert forbidden not in root, forbidden

    apply = body("void NMJE_ApplyFirstContinuationLineage(")
    require(
        apply,
        "journey.LineageClass = NMJE_LINEAGE_NONE;",
        "journey.LineageClass = NMJE_LINEAGE_UNRESOLVED;",
        "previous.JourneyID != journey.JourneyID",
        "previous.ParentEventID != journey.ParentEventID",
        "journey.LineageClass = NMJE_LINEAGE_NEW_JOURNEY;",
        "journey.PreviousLineageRootEventID = previous.ParentEventID;",
        "journey.ParentEventID == rootEventID",
        "journey.LineageClass = NMJE_LINEAGE_FIRST;",
        'journey.LineageReason = "CONTINUATION_EVENT_ID_UNPROVABLE";',
    )
    assert "journey.LineageClass = NMJE_LINEAGE_CONTINUATION;" not in apply
    for forbidden in ("TimeCurrent(", "GetProcessingBarIndex", "MaxWaitBars", "OrderSend(", "Reject"):
        assert forbidden not in apply, forbidden

    update = body("void UpdateNestedJourneyObservation(")
    require(
        update,
        "NMJE_ApplyFirstContinuationLineage(g_pair_states[pairIndex], previous, journey);",
        "NMJE_PrintFirstContinuationLineage(journey);",
    )
    assert update.index("journey.JourneyID = NMJE_BuildJourneyID") < update.index(
        "NMJE_ApplyFirstContinuationLineage("
    )

    telemetry = body("void NMJE_PrintFirstContinuationLineage(")
    require(
        telemetry,
        "[Q9-P11-LINEAGE]",
        "NMJE_LineageClassText(journey.LineageClass)",
        "journey.LineageRootEventID",
        "journey.PreviousLineageRootEventID",
        "journey.ParentEventID",
        "journey.JourneyID",
    )

    freeze = body("void NMJE_FreezeValidatedDecisionAttribution(")
    require(
        freeze,
        "decision.NMJELineageClass = journey.LineageClass;",
        "decision.NMJELineageRootEventID = journey.LineageRootEventID;",
        "decision.NMJEPreviousLineageRootEventID = journey.PreviousLineageRootEventID;",
    )

    build = body("bool BuildNMJEShadowAttribution(")
    require(
        build,
        "attribution.LineageClass = decision.NMJELineageClass;",
        "attribution.LineageClass == NMJE_LINEAGE_CONTINUATION",
        "attribution.LineageClass = NMJE_LINEAGE_UNRESOLVED;",
        "attribution.LineageRootHash = SHORT_HASH(decision.NMJELineageRootEventID);",
        "PreviousLineageRootHash",
    )

    load = body("bool LoadNMJEShadowAttribution(")
    save = body("bool SaveNMJEShadowAttribution(")
    clear = body("void ClearNMJEShadowAttribution(")
    require(
        load,
        'GlobalVariableCheck(base + "LC")',
        "info.nmje_attribution.LineageClass == NMJE_LINEAGE_CONTINUATION",
        "info.nmje_attribution.LineageClass = NMJE_LINEAGE_UNRESOLVED;",
        'NMJELoadHex16(base, "L", info.nmje_attribution.LineageRootHash)',
        'GlobalVariableCheck(base + "LP")',
        'NMJELoadHex16(base, "N", info.nmje_attribution.PreviousLineageRootHash)',
    )
    require(
        save,
        'GlobalVariableSet(base + "LC", (double)a.LineageClass)',
        'NMJEStoreHex16(base, "L", a.LineageRootHash)',
        'GlobalVariableSet(base + "LP",',
        'NMJEStoreHex16(base, "N", a.PreviousLineageRootHash)',
        "verify.nmje_attribution.LineageClass == a.LineageClass",
    )
    assert "a.LineageClass == NMJE_LINEAGE_CONTINUATION" not in save
    require(clear, '"LC"', '"LP"', '"L"', '"N"')

    decision_shadow = body("void NMJE_PrintValidatedDecisionShadow(")
    require(decision_shadow, '" LC="', '" LR="')

    protected = (
        ("BuildPossibleCombinations", "void BuildPossibleCombinations("),
        ("ValidateSequence", "void ValidateSequence("),
        ("BuildConfirmedReEntryCandidate", "void BuildConfirmedReEntryCandidate("),
        ("BuildStandaloneExtremeCandidate", "void BuildStandaloneExtremeCandidate("),
        ("BuildD1OpportunityCandidate", "void BuildD1OpportunityCandidate("),
        ("CompareCanonicalCandidates", "int CompareCanonicalCandidates("),
        ("PriorityEngine_Atomic", "void PriorityEngine_Atomic("),
        ("InvalidationEngine_Atomic", "void InvalidationEngine_Atomic("),
        ("ResolveApprovedInitialSLTP", "bool ResolveApprovedInitialSLTP("),
        ("CheckRiskBeforeTrade", "RiskStatus CheckRiskBeforeTrade("),
        ("RunEntryPreflightAndExecute", "bool RunEntryPreflightAndExecute("),
        ("IsSignalAllowed", "bool IsSignalAllowed("),
        ("SendOrderWithRetry", "int SendOrderWithRetry("),
    )
    for name, signature in protected:
        segment = body(signature)
        for marker in ("LineageClass", "LineageRootEventID", "Q9-P11-LINEAGE"):
            assert marker not in segment, f"{name}:{marker}"

    for forbidden in (
        "LineageScore",
        "REJ_NMJE_LINEAGE",
        "EnableLineageGate",
        "MinContinuation",
        "NewestEventWins",
        "OldestEventWins",
    ):
        assert forbidden not in SRC, forbidden

    assert SRC.count("OrderSend(") == 1
    assert SRC.count("OrderClose(") == 3
    assert SRC.count("OrderModify(") == 0
    assert SRC.count("OrderDelete(") == 0
    print("Q9_P11_LINEAGE_REFINEMENT_STATIC=PASS")

if __name__ == "__main__":
    main()
