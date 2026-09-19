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
        "Version 4.9.1 - Q9 NMJE Maturity Fingerprint",
        '#property version   "4.91"',
        '#define BBMA_BUILD_TAG      "V491_Q9_P6_MATURITY_FINGERPRINT_20260919"',
        '#define BBMA_SOURCE_REV_TAG "Q9_P6_MATURITY_FINGERPRINT_101_20260919"',
        "struct NMJEShadowAttributionState",
        "NMJEShadowAttributionState nmje_attribution;",
        "NMJEM5RefinementState        NMJEM5Refinement;",
    )

    process_pair = body("void ProcessPair(")
    assert process_pair.index("InvalidationEngine_Atomic(") < process_pair.index(
        "NMJE_FreezeValidatedDecisionAttribution("
    ) < process_pair.index("RunEntryPreflightAndExecute(")

    freeze = body("void NMJE_FreezeValidatedDecisionAttribution(")
    require(
        freeze,
        "decision.DecisionState != DEC_VALIDATED",
        "decision.NMJEJourneyID = journey.JourneyID;",
        "decision.NMJEParentEventID = journey.ParentEventID;",
        "decision.NMJEM5Refinement = journey.M5Refinement;",
    )
    for forbidden in ("DEC_REJECTED", "DEC_INVALIDATED", "RejectionReason", "OrderSend("):
        assert forbidden not in freeze

    build = body("bool BuildNMJEShadowAttribution(")
    require(
        build,
        "SHORT_HASH(decision.NMJEJourneyID)",
        "SHORT_HASH(decision.NMJEParentEventID)",
        "NMJE_M5LineageSnapshotValid(m5)",
        "SHORT_HASH(m5.EventID)",
        "SHORT_HASH(m5.Reason)",
    )

    save = body("bool SaveNMJEShadowAttribution(")
    load = body("bool LoadNMJEShadowAttribution(")
    require(
        save,
        "ClearNMJEShadowAttribution(info.ticket);",
        'NMJEStoreHex16(base, "X", info.execution_hash)',
        'NMJEStoreHex16(base, "J", a.JourneyHash)',
        'NMJEStoreHex16(base, "P", a.ParentEventHash)',
        'GlobalVariableSet(base + "V", 1.0)',
        "LoadNMJEShadowAttribution(verify)",
    )
    assert save.index('GlobalVariableSet(base + "V", 1.0)') > save.index(
        'NMJEStoreHex16(base, "P", a.ParentEventHash)'
    )
    require(
        load,
        'GlobalVariableGet(base + "M") != info.magic_number',
        'GlobalVariableGet(base + "O")) != info.open_time',
        "storedExecutionHash != info.execution_hash",
        "info.nmje_attribution.Durable = true;",
    )

    entry = body("void ProcessEntry(")
    require(
        entry,
        "BuildNMJEShadowAttribution(decision, info.nmje_attribution);",
        "SaveExecutionIdentityHash(",
        "SaveC044Checkpoint(info)",
        "SaveNMJEShadowAttribution(info)",
        "[NMJE-P4-OPEN]",
    )
    assert entry.index("SendOrderWithRetry(") < entry.index(
        "BuildNMJEShadowAttribution("
    ) < entry.index("SaveNMJEShadowAttribution(info)")
    assert entry.index("SaveC044Checkpoint(info)") < entry.index(
        "SaveNMJEShadowAttribution(info)"
    )
    p4_segment = entry[entry.index("bool nmjeAttributionPersisted"):entry.index("[P3S5][EXEC_ID]")]
    for forbidden in ("recovery_state =", "DecisionState =", "RejectionReason ="):
        assert forbidden not in p4_segment, forbidden

    recovery = body("void RecoverExistingOrders(")
    require(
        recovery,
        "LoadNMJEShadowAttribution(info)",
        "[NMJE-P4-RECOVER]",
        "AddToMonitoredTrades(info)",
    )
    seg = recovery[recovery.index("LoadNMJEShadowAttribution(info)"):recovery.index("AddToMonitoredTrades(info)")]
    assert "recovery_state =" not in seg
    assert "if(nmjeAttributionRecovered)" not in seg

    outcome = body("void NMJE_PrintClosedOutcomeShadow(")
    require(
        outcome,
        "OrderTicket() != info.ticket",
        "OrderSymbol() != info.pair",
        "OrderMagicNumber() != info.magic_number",
        "[NMJE-P4-OUT]",
        '" NET="',
        "OrderCloseTime()",
    )

    compact = body("void CompactMonitoredTrades(")
    assert compact.index("NMJE_PrintClosedOutcomeShadow(") < compact.index(
        "ClearNMJEShadowAttribution("
    )

    signatures = (
        ("CompareCanonicalCandidates", "int CompareCanonicalCandidates("),
        ("PriorityEngine_Atomic", "void PriorityEngine_Atomic("),
        ("InvalidationEngine_Atomic", "void InvalidationEngine_Atomic("),
        ("RunEntryPreflightAndExecute", "bool RunEntryPreflightAndExecute("),
        ("CheckRiskBeforeTrade", "RiskStatus CheckRiskBeforeTrade("),
        ("SendOrderWithRetry", "int SendOrderWithRetry("),
    )
    for name, signature in signatures:
        b = body(signature)
        for marker in ("nmje_attribution", "SaveNMJEShadowAttribution", "LoadNMJEShadowAttribution"):
            assert marker not in b, f"{name}:{marker}"

    for marker in ("NMJE_PassExecutionGate", "REJ_NMJE_RELATION", "REJ_NMJE_M5", "N3_POLICY_ACTIVE"):
        assert marker not in SRC

    assert SRC.count("OrderSend(") == 1
    assert SRC.count("OrderClose(") == 3
    assert SRC.count("OrderModify(") == 0
    assert SRC.count("OrderDelete(") == 0
    print("Q9_NMJE_P4_ATTRIBUTION_STATIC=PASS")

if __name__ == "__main__":
    main()
