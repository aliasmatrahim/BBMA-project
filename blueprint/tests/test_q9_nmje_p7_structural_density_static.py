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
        "Version 4.9.4 - Q9 Entry Displacement Telemetry",
        '#property version   "4.94"',
        '#define BBMA_BUILD_TAG      "V494_Q9_P10_ENTRY_DISPLACEMENT_20260919"',
        '#define BBMA_SOURCE_REV_TAG "Q9_P10_ENTRY_DISPLACEMENT_101_20260919"',
        "enum ENUM_NMJE_STRUCTURE_STAGE_BIT",
        "NMJE_STRUCTURE_EXTREME   = 1",
        "NMJE_STRUCTURE_TPW       = 2",
        "NMJE_STRUCTURE_MHV       = 4",
        "NMJE_STRUCTURE_DIRECTION = 8",
        "NMJE_STRUCTURE_REENTRY   = 16",
        "NMJE_STRUCTURE_MOMENTUM  = 32",
        "struct NMJEStructuralDensityState",
        "NMJEStructuralDensityState StructureDensity;",
        "NMJEStructuralDensityState    NMJEStructureDensity;",
    )

    add = body("void NMJE_AddComponentStructureStages(")
    require(
        add,
        "SIGNAL_EXTREME",
        "NMJE_STRUCTURE_EXTREME",
        "SIGNAL_MLV",
        "NMJE_STRUCTURE_TPW",
        "NMJE_STRUCTURE_MHV",
        "SIGNAL_RE_ENTRY",
        "NMJE_STRUCTURE_REENTRY",
        "SIGNAL_CSD",
        "SIGNAL_ECSD",
        "NMJE_STRUCTURE_DIRECTION",
        "SIGNAL_CSM",
        "NMJE_STRUCTURE_MOMENTUM",
    )

    resolved = body("int NMJE_BuildResolvedJourneyStructureMask(")
    require(
        resolved,
        "!journey.Valid || !journey.Resolved",
        'journey.JourneyID == ""',
        'journey.ParentEventID == ""',
        "journey.ParentDirection != direction",
        "NMJE_IsExtremeSupporting(state.extreme_h1_buy_lifecycle)",
        "NMJE_IsExtremeSupporting(state.extreme_m15_buy_lifecycle)",
        "NMJE_IsMLVSupporting(state.mlv_buy_state)",
        "state.mlv_buy_state.State == MLV_DIRECTION_TAKEN",
        "NMJE_IsConfirmedRE(state.re_h1_buy_state)",
        "NMJE_IsConfirmedRE(state.re_m15_buy_state)",
        "journey.ParentSignal == SIGNAL_CSD",
        "journey.ParentSignal == SIGNAL_ECSD",
        "journey.ParentSignal == SIGNAL_CSM",
        "NESTED_PARENT_H4_RE",
        "NESTED_PARENT_D1_RE",
    )
    for forbidden in ("RequirementCompleteness", "SequenceCompleteness",
                      "PatternStrength", "PriorityTier", "Score", "Threshold",
                      "OrderSend(", "MarketInfo", "iRSI", "iMACD", "iStochastic", "iADX"):
        assert forbidden not in resolved, forbidden

    prefix = body("int NMJE_BuildStructurePrefixMask(")
    require(prefix, "break;", "NMJE_STRUCTURE_EXTREME", "NMJE_STRUCTURE_MOMENTUM")

    valid = body("bool NMJE_IsStructuralDensityValid(")
    require(
        valid,
        "density.PrefixMask != NMJE_BuildStructurePrefixMask(density.StageMask)",
        "density.StageCount == NMJE_CountStructureStages(density.StageMask)",
    )

    cand = body("void NMJE_BuildCandidateStructuralDensity(")
    require(
        cand,
        "candidate.ComponentCount",
        "NMJE_AddComponentStructureStages(candidate.Components[i], mask)",
        "NMJE_BuildResolvedJourneyStructureMask(state, journey",
        "NMJE_FinalizeStructuralDensity(mask, density)",
    )
    for forbidden in ("candidate.Valid =", "PriorityTier =", "RequirementCompleteness",
                      "SequenceCompleteness", "PatternStrength"):
        assert forbidden not in cand, forbidden

    shadow = body("void NMJE_PrintStructuralDensityShadow(")
    require(
        shadow,
        "IsCandidateEligible(candidates[i])",
        "IsCandidateAllowedByD1Owner(candidates[i], pairState)",
        "[Q9-P7-DENSITY]",
        "density.StageMask",
        "density.PrefixMask",
        "density.StageCount",
    )
    for forbidden in ("candidates[i].Valid =", "CompareCanonicalCandidates(",
                      "PriorityEngine_Atomic(", "InvalidationEngine_Atomic(",
                      "DEC_REJECTED", "DEC_INVALIDATED"):
        assert forbidden not in shadow, forbidden

    freeze = body("void NMJE_FreezeValidatedDecisionAttribution(")
    require(
        freeze,
        "decision.DecisionState != DEC_VALIDATED",
        "NMJE_BuildDecisionStructuralDensity(g_pair_states[pairIndex], journey",
        "decision.NMJEStructureDensity",
    )

    build = body("bool BuildNMJEShadowAttribution(")
    require(
        build,
        "NMJE_IsStructuralDensityValid(decision.NMJEStructureDensity)",
        "attribution.StructureDensity = decision.NMJEStructureDensity;",
    )

    load = body("bool LoadNMJEShadowAttribution(")
    save = body("bool SaveNMJEShadowAttribution(")
    require(
        load,
        'GlobalVariableCheck(base + "SDM")',
        'GlobalVariableCheck(base + "SDP")',
        'GlobalVariableCheck(base + "SDC")',
        "hasSDM != hasSDP",
        "hasSDM != hasSDC",
        "NMJE_IsStructuralDensityValid(info.nmje_attribution.StructureDensity)",
    )
    require(
        save,
        'GlobalVariableSet(base + "SDM", (double)a.StructureDensity.StageMask)',
        'GlobalVariableSet(base + "SDP", (double)a.StructureDensity.PrefixMask)',
        'GlobalVariableSet(base + "SDC", (double)a.StructureDensity.StageCount)',
    )

    process = body("void ProcessPair(")
    assert process.index("NMJE_PrintStructuralDensityShadow(") < process.index("PriorityEngine_Atomic(")
    assert process.index("InvalidationEngine_Atomic(") < process.index(
        "NMJE_FreezeValidatedDecisionAttribution("
    )

    outcome = body("void NMJE_PrintClosedOutcomeShadow(")
    require(outcome, '" SD="', '" SDM="', '" SDP="', '" SDC="')

    protected = (
        ("BuildPossibleCombinations", "void BuildPossibleCombinations("),
        ("ValidateSequence", "void ValidateSequence("),
        ("CompareCanonicalCandidates", "int CompareCanonicalCandidates("),
        ("PriorityEngine_Atomic", "void PriorityEngine_Atomic("),
        ("InvalidationEngine_Atomic", "void InvalidationEngine_Atomic("),
        ("CheckRiskBeforeTrade", "RiskStatus CheckRiskBeforeTrade("),
        ("RunEntryPreflightAndExecute", "bool RunEntryPreflightAndExecute("),
        ("SendOrderWithRetry", "int SendOrderWithRetry("),
    )
    for name, signature in protected:
        segment = body(signature)
        for marker in ("NMJE_STRUCTURE_", "StructureDensity", "StageCount", "PrefixMask", "SDM"):
            assert marker not in segment, f"{name}:{marker}"

    # Legacy candidate-completeness fields are not repurposed by P7.
    assert SRC.count("RequirementCompleteness") == 5
    assert SRC.count("SequenceCompleteness") == 5
    assert SRC.count("PatternStrength") == 5

    for forbidden in (
        "MinStructuralDensity",
        "StructuralDensityScore",
        "REJ_STRUCTURAL_DENSITY",
        "EnableStructuralDensityGate",
        "HighestDensityWins",
    ):
        assert forbidden not in SRC, forbidden

    assert SRC.count("OrderSend(") == 1
    assert SRC.count("OrderClose(") == 3
    assert SRC.count("OrderModify(") == 0
    assert SRC.count("OrderDelete(") == 0
    print("Q9_NMJE_P7_STRUCTURAL_DENSITY_STATIC=PASS")

if __name__ == "__main__":
    main()
