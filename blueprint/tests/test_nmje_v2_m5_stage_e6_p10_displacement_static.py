#!/usr/bin/env python3
"""Stage-E6 P10 entry-displacement telemetry authority firewall."""
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
        "enum ENUM_NMJE_ENTRY_DISPLACEMENT",
        "NMJE_DISPLACEMENT_UNRESOLVED",
        "NMJE_DISPLACEMENT_FLAT",
        "NMJE_DISPLACEMENT_FAVORABLE",
        "NMJE_DISPLACEMENT_ADVERSE",
        "bool                 EntryDisplacementPresent;",
        "double               SourceConfirmationPrice;",
        "double               ValidationEntryPrice;",
        "double               BrokerExecutionPrice;",
        "double               StructuralAnchorPrice;",
        "double               ConfirmationToValidationPips;",
        "double               ValidationToExecutionPips;",
        "double               ExecutionFromAnchorPips;",
    )

    anchor = function_body("ResolveSourceOwnedStructuralAnchor")
    require(
        anchor,
        "sourceConfirmationPrice = reEntry.EntryPrice;",
        "sourceConfirmationPrice <= 0.0",
        "ResolveMatchingReEntryLifecycle(pair, source, reEntry)",
    )
    initial = function_body("ResolveApprovedInitialSLTP")
    require(
        initial,
        "decision.NMJEEntryDisplacementSourcePresent = false;",
        "decision.NMJESourceConfirmationPrice = 0.0;",
        "decision.NMJEStructuralAnchorPrice = 0.0;",
        "sourceConfirmationPrice",
        "decision.NMJEEntryDisplacementSourcePresent = true;",
        "decision.NMJESourceConfirmationPrice = sourceConfirmationPrice;",
        "decision.NMJEStructuralAnchorPrice = structuralAnchor;",
    )
    if initial.index("NMJEEntryDisplacementSourcePresent = true") < initial.index(
        "decision.StopLoss = normalizedSL"
    ):
        raise AssertionError("P10 source geometry freezes before M17 succeeds")

    build = function_body("BuildNMJEShadowAttribution")
    require(
        build,
        "GetPipValue(decision.Pair)",
        "directionSign * (brokerExecutionPrice - decision.EntryPrice)",
        "directionSign * (decision.EntryPrice -",
        "decision.NMJESourceConfirmationPrice) / pipValue",
        "directionSign * (brokerExecutionPrice -",
        "decision.NMJEStructuralAnchorPrice) / pipValue",
        "MathAbs(validationToExecution) <= pointSize * 0.5",
        "NMJE_DISPLACEMENT_FLAT",
        "NMJE_DISPLACEMENT_FAVORABLE",
        "NMJE_DISPLACEMENT_ADVERSE",
    )
    for forbidden in (
        "DecisionState",
        "RejectionReason",
        "return false; // P10",
        "OrderSend",
        "CalculateLotSize",
        "CheckRiskBeforeTrade",
    ):
        if forbidden in build:
            raise AssertionError(f"P10 classification gained authority: {forbidden}")

    process = function_body("ProcessEntry")
    require(
        process,
        "if(OrderSelect(ticket, SELECT_BY_TICKET))",
        "BuildNMJEShadowAttribution(decision, OrderOpenPrice(), snapshot.Point,",
        "SaveNMJEShadowAttribution(info)",
        "DISP=",
    )
    if process.index("BuildNMJEShadowAttribution(") < process.index(
        "if(OrderSelect(ticket, SELECT_BY_TICKET))"
    ):
        raise AssertionError("P10 uses a requested rather than selected broker fill")

    save = function_body("SaveNMJEShadowAttribution")
    load = function_body("LoadNMJEShadowAttribution")
    outcome = function_body("NMJE_PrintClosedOutcomeShadow")
    require(
        save,
        'GlobalVariableSet(base + "DP"',
        'GlobalVariableSet(base + "DC"',
        'GlobalVariableSet(base + "SP"',
        'GlobalVariableSet(base + "VP"',
        'GlobalVariableSet(base + "EP"',
        'GlobalVariableSet(base + "SA"',
        'GlobalVariableSet(base + "CV"',
        'GlobalVariableSet(base + "VE"',
        'GlobalVariableSet(base + "EA"',
        'GlobalVariableSet(base + "V", 3.0)',
    )
    require(
        load,
        "attributionVersion != 1 && attributionVersion != 2",
        'string p10Keys[9] = {"DP","DC","SP","VP","EP","SA","CV","VE","EA"};',
        "EntryDisplacementPresent",
        "NMJE_DISPLACEMENT_ADVERSE",
    )
    require(
        outcome,
        '" DISP="',
        '" SRC="',
        '" VAL="',
        '" EXEC="',
        '" ANCH="',
        '" CVP="',
        '" VEP="',
        '" EAP="',
    )

    # P10 cannot become a pre-send filter, candidate input, M16 authority, risk
    # input, lifecycle input, or execution-deviation replacement.
    for name in (
        "BuildPossibleCombinations",
        "CompareCanonicalCandidates",
        "IsCandidateEligible",
        "InvalidationEngine_Atomic",
        "CalculateLotSize",
        "CheckRiskBeforeTrade",
        "SendOrderWithRetry",
        "AdvanceD1TPWLifecycleForPair",
        "AdvanceC044OwnerEventsForPair",
    ):
        body = function_body(name)
        for forbidden in (
            "EntryDisplacement",
            "ConfirmationToValidationPips",
            "ValidationToExecutionPips",
            "ExecutionFromAnchorPips",
        ):
            if forbidden in body:
                raise AssertionError(f"P10 authority leak in {name}: {forbidden}")

    for forbidden in (
        "EnableEntryDisplacementGate",
        "MaxEntryDisplacementPips",
        "REJ_ENTRY_DISPLACEMENT",
        "DelayForEntryDisplacement",
    ):
        if forbidden in SRC:
            raise AssertionError(f"P10 activation marker present: {forbidden}")

    require(
        SRC,
        "Version 4.7.1 - D1TPW Restart-Safe Checkpoint Hardening",
        '#property version   "4.71"',
    )
    print("NMJE_V2_M5_STAGE_E6_P10_DISPLACEMENT_STATIC=PASS")


if __name__ == "__main__":
    main()

