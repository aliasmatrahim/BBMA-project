#!/usr/bin/env python3
"""Stage-D1 durable shadow-attribution firewall for Issue #101 P4."""
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
        "struct NMJEShadowAttributionState",
        "string               JourneyHash;",
        "string               ParentEventHash;",
        "string               M5EventHash;",
        "string               M5ReasonHash;",
        "NMJEM5RefinementState        NMJEM5Refinement;",
        "NMJEShadowAttributionState nmje_attribution;",
    )

    freeze = function_body("FreezeNMJEShadowSnapshot")
    validate = function_body("ValidateNMJEShadowSnapshot")
    require(freeze, "decision.NMJEM5Refinement = journey.M5Refinement;")
    require(
        validate,
        "M5_PRESENCE_MISMATCH",
        "M5_LINEAGE_INVALID",
        "M5_SNAPSHOT_MISMATCH",
        "frozenM5.EventID != currentM5.EventID",
        "frozenM5.ParentEventID != currentM5.ParentEventID",
        "frozenM5.JourneyID != currentM5.JourneyID",
    )

    build = function_body("BuildNMJEShadowAttribution")
    require(
        build,
        "SHORT_HASH(decision.NMJEJourneyID)",
        "SHORT_HASH(decision.NMJEParentEventID)",
        "NMJE_M5LineageSnapshotValid(m5)",
        "SHORT_HASH(m5.EventID)",
        "SHORT_HASH(m5.Reason)",
    )

    save = function_body("SaveNMJEShadowAttribution")
    load = function_body("LoadNMJEShadowAttribution")
    require(
        save,
        "NMJEAttributionGVBase(info.ticket)",
        'GlobalVariableDel(base + "V")',
        'NMJEStoreHex16(base, "X", info.execution_hash)',
        'NMJEStoreHex16(base, "J", a.JourneyHash)',
        'NMJEStoreHex16(base, "P", a.ParentEventHash)',
        'GlobalVariableSet(base + "V", 3.0)',
        "LoadNMJEShadowAttribution(verify)",
    )
    require(
        load,
        "storedExecutionHash != info.execution_hash",
        'NMJELoadHex16(base, "J", info.nmje_attribution.JourneyHash)',
        'NMJELoadHex16(base, "P", info.nmje_attribution.ParentEventHash)',
        "info.nmje_attribution.Durable = true;",
    )

    process_entry = function_body("ProcessEntry")
    require(
        process_entry,
        "BuildNMJEShadowAttribution(decision, OrderOpenPrice(), snapshot.Point,",
        "SaveExecutionIdentityHash(",
        "SaveNMJEShadowAttribution(info)",
        "[NMJE-P4-OPEN]",
    )
    if process_entry.index("BuildNMJEShadowAttribution(") > process_entry.index(
        "SaveNMJEShadowAttribution(info)"
    ):
        raise AssertionError("attribution is persisted before it is frozen")

    recovery = function_body("RecoverExistingOrders")
    require(
        recovery,
        "LoadNMJEShadowAttribution(info)",
        "Missing/corrupt attribution never",
        "[NMJE-P4-RECOVER]",
    )
    recovery_load = recovery.index("LoadNMJEShadowAttribution(info)")
    next_recovery_assignment = recovery.find("info.recovery_state =", recovery_load)
    if next_recovery_assignment < 0:
        raise AssertionError("canonical trade recovery state handling missing")
    between = recovery[recovery_load:next_recovery_assignment]
    if "nmjeAttributionRecovered" in between and "if(nmjeAttributionRecovered)" in between:
        raise AssertionError("attribution recovery controls trade recovery state")

    outcome = function_body("NMJE_PrintClosedOutcomeShadow")
    require(
        outcome,
        "[NMJE-P4-OUT]",
        '" TICKET="',
        '" DIDH="',
        '" JH="',
        '" PH="',
        '" M5E="',
        '" M5RH="',
        '" NET="',
        "OrderCloseTime()",
    )

    # P4 may observe ProcessEntry after a successful order, but must remain
    # absent from selection, ranking, invalidation outcomes, risk and OrderSend.
    for name in (
        "BuildPossibleCombinations",
        "CompareCanonicalCandidates",
        "IsCandidateEligible",
        "CalculateLotSize",
        "CheckRiskBeforeTrade",
        "SendOrderWithRetry",
    ):
        body = function_body(name)
        for forbidden in (
            "nmje_attribution",
            "NMJEM5Refinement",
            "SaveNMJEShadowAttribution",
            "LoadNMJEShadowAttribution",
        ):
            if forbidden in body:
                raise AssertionError(f"P4 authority leak in {name}: {forbidden}")

    invalidation = function_body("InvalidationEngine_Atomic")
    shadow_start = invalidation.index("bool nmjeShadowMatch")
    validated = invalidation.index("decision.DecisionState = DEC_VALIDATED;", shadow_start)
    shadow_segment = invalidation[shadow_start:validated]
    for forbidden in ("return;", "DEC_REJECTED", "DEC_INVALIDATED", "RejectionReason ="):
        if forbidden in shadow_segment:
            raise AssertionError(f"shadow comparison gained authority: {forbidden}")

    require(
        SRC,
        "bool           EnableC044Lifecycle                = false;",
        "bool           EnableD1TPWLifecycle               = false;",
    )
    print("NMJE_V2_M5_STAGE_D1_ATTRIBUTION_STATIC=PASS")


if __name__ == "__main__":
    main()

