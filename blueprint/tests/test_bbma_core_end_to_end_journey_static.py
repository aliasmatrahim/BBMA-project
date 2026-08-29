#!/usr/bin/env python3
"""Bind C2-A journey, single-writer and recovery invariants to build 4.71."""
from hashlib import sha256
from pathlib import Path
import re


SOURCE_PATH = Path("blueprint/source/BBMA_EA.mq4")
SRC = SOURCE_PATH.read_text(encoding="utf-8")
EXPECTED_SOURCE_SHA256 = "c6a87f613495547ee3cf52a8fe041ae6f9a63396075c0c755a7475b9f488a7bb"


def function_body(name: str) -> str:
    declaration = re.search(rf"(?m)^[A-Za-z_][^\r\n]*\b{re.escape(name)}\s*\(", SRC)
    if declaration is None:
        raise AssertionError(f"missing function: {name}")
    brace = SRC.find("{", declaration.start())
    depth = 0
    for index in range(brace, len(SRC)):
        if SRC[index] == "{":
            depth += 1
        elif SRC[index] == "}":
            depth -= 1
            if depth == 0:
                return SRC[brace:index + 1]
    raise AssertionError(f"unterminated function: {name}")


def require(name: str, *markers: str) -> str:
    body = function_body(name)
    for marker in markers:
        if marker not in body:
            raise AssertionError(f"{name} missing invariant: {marker}")
    return body


def require_order(name: str, *markers: str) -> None:
    body = require(name, *markers)
    positions = [body.index(marker) for marker in markers]
    if positions != sorted(positions):
        raise AssertionError(f"{name} journey order drift: {markers}")


def main() -> None:
    digest = sha256(SOURCE_PATH.read_bytes()).hexdigest()
    if digest != EXPECTED_SOURCE_SHA256:
        raise AssertionError(f"EA source drift: {digest}")

    require_order(
        "ProcessPair",
        "UpdateD1MajorTrendOwner(",
        "UpdateRuntimeH4DirectionalOwner(",
        "UpdateD1OpportunityJourney(",
        "UpdateNestedJourneyObservation(",
        "PriorityEngine_Atomic(",
        "InvalidationEngine_Atomic(",
        "NMJE_PrintValidatedDecisionShadow(",
        "RunEntryPreflightAndExecute(",
        "last_decision = decision",
    )
    require(
        "PriorityEngine_Atomic",
        "FreezeD1OpportunitySnapshot(pairState, selected, decision)",
        "FreezeD1OwnerSnapshot(pairState, decision)",
        "decision.Components[c] = selected.Components[c]",
        "decision.SequenceHash = selected.SequenceHash",
        "decision.DecisionState = DEC_CREATED",
        "FreezeNMJEShadowSnapshot(pairState, decision)",
        "decision.DecisionID = GenerateDecisionID(",
    )
    require_order(
        "InvalidationEngine_Atomic",
        "decision.DecisionState != DEC_CREATED",
        "ValidateDecisionD1AuthoritySnapshot(",
        "ValidateDecisionOwnerSnapshot(",
        "ValidateNMJEShadowSnapshot(",
        "decision.DecisionState = DEC_VALIDATED",
    )
    require(
        "InvalidationEngine_Atomic",
        "N3 shadow comparison only. No rejection is permitted from this result.",
    )

    require_order(
        "RunEntryPreflightAndExecute",
        "BuildRiskValidationSnapshot(",
        "ResolveExecutionReferencePrice(",
        "ResolveApprovedInitialSLTP(",
        "snapshot.StopLoss = decision.StopLoss",
        "ValidateSLTP(",
        "CalculateLotSize(",
        "CheckRiskBeforeTrade(",
        "FinalPortfolioGuard(",
        "ProcessEntry(",
    )
    require(
        "CalculateLotSize",
        "decision.DecisionState != DEC_VALIDATED",
        "snapshot.EntryPrice - decision.EntryPrice",
        "snapshot.StopLoss - decision.StopLoss",
    )

    require_order(
        "ProcessEntry",
        "decision.DecisionID == \"\"",
        "IsDecisionExecuted(decision.DecisionID)",
        "FindExistingExecutionTicket(",
        "EnsureMonitoredRegistryCapacity(",
        "CreateOrderComment(decision.DecisionID",
        "SendOrderWithRetry(",
        "info.decision_id = decision.DecisionID",
        "expectedExecutionHash = SHORT_HASH(decision.DecisionID)",
        "SaveExecutionIdentityHash(",
        "AddToMonitoredTrades(info)",
        "MarkDecisionExecuted(decision.DecisionID, ticket)",
    )
    send = require(
        "SendOrderWithRetry",
        "FindExistingExecutionTicket(",
        "deviation > frozenAllowedDeviation",
        "OrderSend(",
        "IsAmbiguousError(error)",
    )
    if len(re.findall(r"\bOrderSend\s*\(", SRC)) != 1 or send.count("OrderSend(") != 1:
        raise AssertionError("OrderSend must have exactly one M22 callsite")

    manage = require(
        "ManagePositions",
        "g_portfolio_emergency_close_requested",
        "REC_CORRUPTED",
        "REC_RECOVERY_INVALID",
        "REC_IDENTITY_MISSING_FROZEN",
        "EnableD1TPWLifecycle",
        "ExecuteLatchedD1TPWClose(",
        "EnableC044Lifecycle",
        "ExecuteLatchedC044Close(",
    )
    close_owners = (
        function_body("ExecuteLatchedC044Close")
        + function_body("ExecuteLatchedD1TPWClose")
        + manage
    )
    if len(re.findall(r"\bOrderClose\s*\(", SRC)) != 3:
        raise AssertionError("unexpected broker-close callsite count")
    if len(re.findall(r"\bOrderClose\s*\(", close_owners)) != 3:
        raise AssertionError("OrderClose escaped M23 owners")

    require_order(
        "InitializeEA",
        "RecoverH4DirectionalOwners()",
        "RebuildExecutionHistory()",
        "RecoverExistingOrders()",
        "g_is_initialized = true",
    )
    require(
        "RecoverExistingOrders",
        "IsExactEAOwnedSelectedOrder(pairIdx)",
        "LoadPersistedExecutionHashForTicket(",
        "ExtractExecutionHash(comment, brokerExecutionHash)",
        "ParseOrderCommentFull(",
        "TARGETLESS_CHECKPOINT_AMBIGUOUS",
        "TARGETLESS_CHECKPOINT_MISSING_OR_INVALID",
        "TARGETLESS_DURABLE_IDENTITY_REQUIRED",
        "INVALID_GEOMETRY",
        "MISSING_EXECUTION_HASH",
        "AddToMonitoredTrades(info)",
        "UpsertExecutionHashTombstone(",
    )

    if len(re.findall(r"decision\.DecisionState\s*=\s*DEC_CREATED", SRC)) != 1:
        raise AssertionError("DEC_CREATED writer drift")
    if len(re.findall(r"decision\.DecisionState\s*=\s*DEC_VALIDATED", SRC)) != 1:
        raise AssertionError("DEC_VALIDATED writer drift")
    executed_writes = re.findall(r"decision\.DecisionState\s*=\s*DEC_EXECUTED", SRC)
    if len(executed_writes) != 2 or function_body("ProcessEntry").count(
        "decision.DecisionState = DEC_EXECUTED"
    ) != 2:
        raise AssertionError("DEC_EXECUTED writer escaped M22")

    if not re.search(r"(?m)^bool\s+EnableD1TPWLifecycle\s*=\s*false\s*;", SRC):
        raise AssertionError("D1TPW gate activated")
    if not re.search(r"(?m)^bool\s+EnableC044Lifecycle\s*=\s*false\s*;", SRC):
        raise AssertionError("C044 gate activated")
    if re.search(r"\bPERIOD_W1\b|\bPERIOD_M30\b|\bPERIOD_M1\b", SRC):
        raise AssertionError("excluded timeframe authority introduced")

    print("BBMA_CORE_END_TO_END_JOURNEY_STATIC=PASS")


if __name__ == "__main__":
    main()
