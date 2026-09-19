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
        "struct NMJEEntryDisplacementState",
        "NMJEEntryDisplacementState EntryDisplacement;",
        "NMJEEntryDisplacementState entry_displacement;",
        "double               SourceReferencePrice;",
        "double               PreflightReferencePrice;",
        "double               BrokerOpenPrice;",
        "double               SourceToPreflightPips;",
        "double               PreflightToOpenPips;",
        "double               SourceToOpenPips;",
    )

    valid = body("bool NMJE_IsEntryDisplacementValid(")
    require(
        valid,
        "state.SourceSignal != SIGNAL_RE_ENTRY",
        "state.SourceSignal != SIGNAL_EXTREME",
        "state.SourceTimeframe <= 0",
        "state.SourceCandleTime <= 0",
        "state.SourceReferencePrice <= 0.0",
        "state.PreflightReferencePrice <= 0.0",
        "state.BrokerOpenPrice <= 0.0",
    )

    norm = body("double NMJE_DirectionNormalizedDisplacementPips(")
    require(
        norm,
        "direction == DIR_BUY",
        "(toPrice - fromPrice) / pipValue",
        "direction == DIR_SELL",
        "(fromPrice - toPrice) / pipValue",
    )
    for forbidden in ("Threshold", "Score", "Reject", "DecisionState", "RejectionReason"):
        assert forbidden not in norm, forbidden

    build = body("bool NMJE_BuildEntryDisplacementAttribution(")
    require(
        build,
        "decision.HasSLTPSourceComponent",
        "ComponentIdentity source = decision.SLTPSourceComponent;",
        "IsApprovedSLTPSourceComponent(decision, source)",
        "ResolveClosedSourceShift(decision.Pair, source)",
        "iClose(decision.Pair, source.Timeframe, shift)",
        "GetPipValue(decision.Pair)",
        "state.PreflightReferencePrice = decision.EntryPrice;",
        "state.BrokerOpenPrice = brokerOpenPrice;",
        "state.SourceToPreflightPips",
        "state.PreflightToOpenPips",
        "state.SourceToOpenPips",
    )
    for forbidden in (
        "candidate.",
        "PriorityTier",
        "DecisionState =",
        "RejectionReason =",
        "OrderSend(",
        "AllowedExecutionDeviation",
        "MaxSpread",
        "ATR",
        "iATR",
    ):
        assert forbidden not in build, forbidden

    load = body("bool LoadNMJEShadowAttribution(")
    save = body("bool SaveNMJEShadowAttribution(")
    clear = body("void ClearNMJEShadowAttribution(")
    require(
        load,
        'GlobalVariableCheck(base + "DP")',
        '"DSG","DTF","DCT","DSP","DPP","DBP","D12","D2B","D1B"',
        "NMJE_IsEntryDisplacementValid(info.nmje_attribution.EntryDisplacement)",
    )
    require(
        save,
        'GlobalVariableSet(base + "DP", 1.0)',
        'GlobalVariableSet(base + "DSG"',
        'GlobalVariableSet(base + "DTF"',
        'GlobalVariableSet(base + "DCT"',
        'GlobalVariableSet(base + "DSP"',
        'GlobalVariableSet(base + "DPP"',
        'GlobalVariableSet(base + "DBP"',
        'GlobalVariableSet(base + "D12"',
        'GlobalVariableSet(base + "D2B"',
        'GlobalVariableSet(base + "D1B"',
        "verify.nmje_attribution.EntryDisplacement.Present",
    )
    require(clear, '"DP","DSG","DTF","DCT","DSP","DPP","DBP","D12","D2B","D1B"')

    entry = body("void ProcessEntry(")
    require(
        entry,
        "info.initial_entry_price = OrderOpenPrice();",
        "NMJE_BuildEntryDisplacementAttribution(",
        "decision, info.initial_entry_price, info.entry_displacement",
        "BuildNMJEShadowAttribution(decision, info.nmje_attribution);",
        "info.nmje_attribution.EntryDisplacement = info.entry_displacement;",
        "[NMJE-P4-OPEN]",
        "[Q9-P10-DISP-OPEN]",
        '" DISP="',
        '" D12="',
        '" D2B="',
        '" D1B="',
    )
    assert entry.index("SendOrderWithRetry(") < entry.index(
        "info.initial_entry_price = OrderOpenPrice();"
    ) < entry.index("NMJE_BuildEntryDisplacementAttribution(")
    assert entry.index("NMJE_BuildEntryDisplacementAttribution(") < entry.index(
        "BuildNMJEShadowAttribution("
    )
    assert "info.entry_displacement.Present" in entry

    recovery = body("void RecoverExistingOrders(")
    require(
        recovery,
        "LoadNMJEShadowAttribution(info)",
        "info.entry_displacement = info.nmje_attribution.EntryDisplacement;",
    )

    outcome = body("void NMJE_PrintClosedOutcomeShadow(")
    require(outcome, "info.entry_displacement.Present", "[Q9-P10-DISP-OUT]", '" DISP="', '" DSIG="', '" DTF="', '" DSP="',
            '" DPP="', '" DBP="', '" D12="', '" D2B="', '" D1B="')

    # P10 must not become authority before/at selection, validation, risk or order send.
    protected = (
        ("BuildPossibleCombinations", "void BuildPossibleCombinations("),
        ("ValidateSequence", "void ValidateSequence("),
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
        for marker in (
            "EntryDisplacement", "SourceToPreflightPips",
            "PreflightToOpenPips", "SourceToOpenPips", "Q9-P10"
        ):
            assert marker not in segment, f"{name}:{marker}"

    for forbidden in (
        "MaxEntryDisplacement",
        "MinEntryDisplacement",
        "EntryDisplacementThreshold",
        "REJ_ENTRY_DISPLACEMENT",
        "EnableEntryDisplacementGate",
        "DisplacementScore",
    ):
        assert forbidden not in SRC, forbidden

    assert SRC.count("OrderSend(") == 1
    assert SRC.count("OrderClose(") == 3
    assert SRC.count("OrderModify(") == 0
    assert SRC.count("OrderDelete(") == 0
    print("Q9_P10_ENTRY_DISPLACEMENT_STATIC=PASS")

if __name__ == "__main__":
    main()
