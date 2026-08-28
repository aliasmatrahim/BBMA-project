#!/usr/bin/env python3
"""Stage-E2 P6 categorical BBMA maturity metadata firewall."""
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
        "enum ENUM_NMJE_JOURNEY_MATURITY",
        "NMJE_MATURITY_OWNER_ONLY",
        "NMJE_MATURITY_EXTREME_DEVELOPING",
        "NMJE_MATURITY_EXTREME_MATURE",
        "NMJE_MATURITY_REENTRY_CANDIDATE",
        "NMJE_MATURITY_REENTRY_CONFIRMED",
        "NMJE_MATURITY_MHV_DEVELOPING",
        "NMJE_MATURITY_MHV_MATURE",
        "NMJE_MATURITY_CONFLICTED",
        "NMJE_MATURITY_OWNER_TRANSITION",
        "NMJE_MATURITY_UNRESOLVED",
        "int                  ContextStateCode;",
        "ENUM_NMJE_JOURNEY_MATURITY M5Maturity;",
        "ENUM_NMJE_JOURNEY_MATURITY   NMJEMaturity;",
    )

    base = function_body("NMJE_ClassifyJourneyMaturity")
    require(
        base,
        "NMJE_IsConfirmedRE(state.re_h1_buy_state)",
        "NMJE_IsConfirmedRE(state.re_m15_buy_state)",
        "NMJE_IsCandidateRE(state.re_h1_buy_state)",
        "NMJE_IsCandidateRE(state.re_m15_buy_state)",
        "NMJE_IsMLVSupporting(state.mlv_buy_state)",
        "NMJE_IsMLVActive(state.mlv_buy_state)",
        "NMJE_IsExtremeSupporting(state.extreme_h1_buy_lifecycle)",
        "NMJE_IsExtremeSupporting(state.extreme_m15_buy_lifecycle)",
        "NMJE_IsExtremeActive(state.extreme_h1_buy_lifecycle)",
        "NMJE_IsExtremeActive(state.extreme_m15_buy_lifecycle)",
        "journey.ParentEventID != \"\"",
    )
    for forbidden in ("Score", "Weight", "Threshold", "MarketInfo", "iRSI", "iMACD"):
        if forbidden in base:
            raise AssertionError(f"non-categorical maturity input: {forbidden}")

    m5 = function_body("NMJE_ClassifyM5Maturity")
    require(
        m5,
        "snapshot.ContextCode == NMJE_M5_CONTEXT_RE_ENTRY",
        "snapshot.ContextStateCode == RE_STATE_CONFIRMED",
        "snapshot.ContextStateCode == RE_STATE_CANDIDATE",
        "snapshot.ContextCode == NMJE_M5_CONTEXT_EXTREME",
        "snapshot.ContextStateCode == EXT_MAT_RAW",
        "snapshot.ContextStateCode == EXT_MAT_REVERSAL_CONFIRMED",
        "snapshot.ContextStateCode == EXT_MAT_RETEST_PHASE",
        "snapshot.ContextStateCode == EXT_MAT_RETEST_READY",
    )

    build_m5 = function_body("NMJE_BuildM5Refinement")
    require(
        build_m5,
        "snapshot.ContextStateCode = (int)selectedRE.State;",
        "snapshot.ContextStateCode = (int)selectedExtreme.Maturity;",
        "snapshot.Maturity = NMJE_ClassifyM5Maturity(snapshot);",
    )

    update = function_body("UpdateNestedJourneyObservation")
    require(
        update,
        "journey.Maturity =",
        "NMJE_ClassifyJourneyMaturity(g_pair_states[pairIndex], journey)",
        "NMJE_MaturityText(journey.Maturity)",
        "NMJE_MaturityText(journey.M5Refinement.Maturity)",
    )

    freeze = function_body("FreezeNMJEShadowSnapshot")
    validate = function_body("ValidateNMJEShadowSnapshot")
    require(freeze, "decision.NMJEMaturity = journey.Maturity;")
    require(
        validate,
        "current.Maturity != decision.NMJEMaturity",
        "frozenM5.ContextStateCode != currentM5.ContextStateCode",
        "frozenM5.Maturity != currentM5.Maturity",
    )

    attribution = function_body("BuildNMJEShadowAttribution")
    save = function_body("SaveNMJEShadowAttribution")
    load = function_body("LoadNMJEShadowAttribution")
    outcome = function_body("NMJE_PrintClosedOutcomeShadow")
    require(
        attribution,
        "attribution.Maturity = decision.NMJEMaturity;",
        "attribution.M5Maturity = m5.Maturity;",
        "attribution.M5ContextStateCode = m5.ContextStateCode;",
    )
    require(
        save,
        'GlobalVariableSet(base + "JM", (double)a.Maturity)',
        'GlobalVariableSet(base + "M5M", (double)a.M5Maturity)',
        'GlobalVariableSet(base + "M5S", (double)a.M5ContextStateCode)',
    )
    require(
        load,
        'GlobalVariableGet(base + "JM")',
        'GlobalVariableGet(base + "M5M")',
        'GlobalVariableGet(base + "M5S")',
    )
    require(
        outcome,
        '" MAT="',
        "NMJE_MaturityText(info.nmje_attribution.Maturity)",
        '" M5MAT="',
        "NMJE_MaturityText(info.nmje_attribution.M5Maturity)",
    )

    # P6 cannot become a score, eligibility threshold, decision delay or gate.
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
        for forbidden in ("NMJEMaturity", "M5Maturity", "NMJE_MATURITY_"):
            if forbidden in body:
                raise AssertionError(f"P6 authority leak in {name}: {forbidden}")

    invalidation = function_body("InvalidationEngine_Atomic")
    shadow_start = invalidation.index("bool nmjeShadowMatch")
    validated = invalidation.index("decision.DecisionState = DEC_VALIDATED;", shadow_start)
    segment = invalidation[shadow_start:validated]
    require(segment, "NMJE_MaturityText(decision.NMJEMaturity)")
    for forbidden in ("return;", "DEC_REJECTED", "DEC_INVALIDATED", "RejectionReason ="):
        if forbidden in segment:
            raise AssertionError(f"P6 maturity gained M16 authority: {forbidden}")

    for forbidden in (
        "NMJE_MATURITY_SCORE",
        "MinNMJEMaturity",
        "REJ_NMJE_MATURITY",
        "EnableNMJEMaturityGate",
    ):
        if forbidden in SRC:
            raise AssertionError(f"P6 activation marker present: {forbidden}")

    print("NMJE_V2_M5_STAGE_E2_P6_MATURITY_STATIC=PASS")


if __name__ == "__main__":
    main()

