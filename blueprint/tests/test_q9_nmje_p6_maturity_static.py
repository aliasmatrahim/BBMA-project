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
    raise AssertionError(signature)

def require(text: str, *markers: str) -> None:
    for marker in markers:
        assert marker in text, marker

def main() -> None:
    require(
        SRC,
        "Version 4.9.2 - Q9 NMJE Structural Density",
        '#property version   "4.92"',
        '#define BBMA_BUILD_TAG      "V492_Q9_P7_STRUCTURAL_DENSITY_20260919"',
        '#define BBMA_SOURCE_REV_TAG "Q9_P7_STRUCTURAL_DENSITY_101_20260919"',
        "enum ENUM_NMJE_JOURNEY_MATURITY",
        "NMJE_MATURITY_NONE",
        "NMJE_MATURITY_OWNER_ONLY",
        "NMJE_MATURITY_EXTREME_DEVELOPING",
        "NMJE_MATURITY_EXTREME_MATURE",
        "NMJE_MATURITY_MHV_DEVELOPING",
        "NMJE_MATURITY_MHV_MATURE",
        "NMJE_MATURITY_DIRECTION_STAGE",
        "NMJE_MATURITY_REENTRY_CANDIDATE",
        "NMJE_MATURITY_REENTRY_CONFIRMED",
        "NMJE_MATURITY_MOMENTUM_CONTINUATION",
        "NMJE_MATURITY_OWNER_TRANSITION",
        "NMJE_MATURITY_UNRESOLVED",
        "ENUM_NMJE_JOURNEY_MATURITY Maturity;",
        "ENUM_NMJE_JOURNEY_MATURITY M5Maturity;",
        "ENUM_NMJE_JOURNEY_MATURITY   NMJEMaturity;",
        "int                  ContextStateCode;",
        "int                  M5ContextStateCode;",
    )

    classify = body("ENUM_NMJE_JOURNEY_MATURITY NMJE_ClassifyJourneyMaturity(")
    require(
        classify,
        "D1_OWNER_UNRESOLVED",
        "D1_TRANSITION",
        "NMJE_IsConfirmedRE(state.re_h1_buy_state)",
        "NMJE_IsConfirmedRE(state.re_m15_buy_state)",
        "NMJE_IsCandidateRE(state.re_h1_buy_state)",
        "NMJE_IsCandidateRE(state.re_m15_buy_state)",
        "journey.ParentSignal == SIGNAL_CSM",
        "journey.ParentSignal == SIGNAL_CSD",
        "journey.ParentSignal == SIGNAL_ECSD",
        "NMJE_IsMLVSupporting(state.mlv_buy_state)",
        "NMJE_IsMLVActive(state.mlv_buy_state)",
        "NMJE_IsExtremeSupporting(state.extreme_h1_buy_lifecycle)",
        "NMJE_IsExtremeSupporting(state.extreme_m15_buy_lifecycle)",
        "NMJE_IsExtremeActive(state.extreme_h1_buy_lifecycle)",
        "NMJE_IsExtremeActive(state.extreme_m15_buy_lifecycle)",
        'journey.ParentEventID != "" && journey.JourneyID != ""',
    )
    for forbidden in ("Score", "Weight", "Threshold", "MarketInfo", "iRSI", "iMACD", "iStochastic", "iADX"):
        assert forbidden not in classify, forbidden

    m5class = body("ENUM_NMJE_JOURNEY_MATURITY NMJE_ClassifyM5Maturity(")
    require(
        m5class,
        "snapshot.ContextCode == NMJE_M5_CONTEXT_RE_ENTRY",
        "snapshot.ContextStateCode == RE_STATE_CONFIRMED",
        "snapshot.ContextCode == NMJE_M5_CONTEXT_EXTREME",
        "snapshot.ContextStateCode == EXT_MAT_RAW",
        "NMJE_MATURITY_EXTREME_MATURE",
        "NMJE_MATURITY_UNRESOLVED",
    )

    m5build = body("void NMJE_BuildM5Refinement(")
    require(
        m5build,
        "snapshot.ContextStateCode = (int)selectedRE.State;",
        "snapshot.ContextStateCode = (int)selectedExtreme.Maturity;",
        "NMJE_CommitM5Refinement(journey, snapshot);",
    )
    assert "OrderSend(" not in m5build

    update = body("void UpdateNestedJourneyObservation(")
    require(
        update,
        "NMJE_ClassifyJourneyMaturity(g_pair_states[pairIndex], journey)",
        "NMJE_MaturityText(journey.Maturity)",
        "NMJE_MaturityText(journey.M5Refinement.Maturity)",
    )

    freeze = body("void NMJE_FreezeValidatedDecisionAttribution(")
    require(
        freeze,
        "decision.DecisionState != DEC_VALIDATED",
        "decision.NMJEMaturity = journey.Maturity;",
    )

    build = body("bool BuildNMJEShadowAttribution(")
    require(
        build,
        "attribution.Maturity = decision.NMJEMaturity;",
        "attribution.M5Maturity = m5.Maturity;",
        "attribution.M5ContextStateCode = m5.ContextStateCode;",
    )

    save = body("bool SaveNMJEShadowAttribution(")
    load = body("bool LoadNMJEShadowAttribution(")
    require(
        save,
        'GlobalVariableSet(base + "JM", (double)a.Maturity)',
        'GlobalVariableSet(base + "M5M", (double)a.M5Maturity)',
        'GlobalVariableSet(base + "M5S", (double)a.M5ContextStateCode)',
    )
    require(
        load,
        'GlobalVariableCheck(base + "JM")',
        'GlobalVariableCheck(base + "M5M")',
        'GlobalVariableCheck(base + "M5S")',
        "NMJE_MATURITY_UNRESOLVED",
    )

    outcome = body("void NMJE_PrintClosedOutcomeShadow(")
    require(
        outcome,
        '" MAT="',
        "NMJE_MaturityText(info.nmje_attribution.Maturity)",
        '" M5MAT="',
        "NMJE_MaturityText(info.nmje_attribution.M5Maturity)",
        '" M5STATE="',
    )

    # Hard authority firewall: maturity must not enter selection, validation,
    # risk, preflight or broker execution.
    for name, signature in (
        ("CompareCanonicalCandidates", "int CompareCanonicalCandidates("),
        ("PriorityEngine_Atomic", "void PriorityEngine_Atomic("),
        ("InvalidationEngine_Atomic", "void InvalidationEngine_Atomic("),
        ("CheckRiskBeforeTrade", "RiskStatus CheckRiskBeforeTrade("),
        ("RunEntryPreflightAndExecute", "bool RunEntryPreflightAndExecute("),
        ("SendOrderWithRetry", "int SendOrderWithRetry("),
    ):
        segment = body(signature)
        for marker in ("NMJEMaturity", "M5Maturity", "NMJE_MATURITY_"):
            assert marker not in segment, f"{name}:{marker}"

    for forbidden in (
        "NMJE_MATURITY_SCORE",
        "MinNMJEMaturity",
        "REJ_NMJE_MATURITY",
        "EnableNMJEMaturityGate",
        "M5_MATURITY_AUTHORITY",
    ):
        assert forbidden not in SRC, forbidden

    assert SRC.count("OrderSend(") == 1
    assert SRC.count("OrderClose(") == 3
    assert SRC.count("OrderModify(") == 0
    assert SRC.count("OrderDelete(") == 0
    print("Q9_NMJE_P6_MATURITY_STATIC=PASS")

if __name__ == "__main__":
    main()
