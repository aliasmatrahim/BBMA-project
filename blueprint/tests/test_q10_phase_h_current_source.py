from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = (ROOT / "blueprint" / "source" / "BBMA_EA.mq4").read_text(encoding="utf-8")


def body(signature: str) -> str:
    start = SRC.index(signature)
    brace = SRC.index("{", start)
    depth = 0
    for i in range(brace, len(SRC)):
        depth += (SRC[i] == "{") - (SRC[i] == "}")
        if depth == 0:
            return SRC[start:i + 1]
    raise AssertionError(signature)


def test_d1_and_h4_fail_closed_current_owner():
    d1 = body("bool IsD1MajorTrendOwnerExecutionReady(")
    assert "D1_OWNER_BUY_CONFIRMED" in d1
    assert "D1_OWNER_SELL_CONFIRMED" in d1
    assert d1.rstrip().endswith("return false;\n}")

    re = body("void BuildConfirmedReEntryCandidate(")
    assert "!h4Owner.RecoveryComplete" in re
    assert "!h4Owner.IsValid" in re
    assert "h4Owner.State != H4_OWNER_ACTIVE" in re
    assert "h4Owner.Direction != reEntry.Direction" in re
    assert "fallback" in re

    ext = body("void BuildStandaloneExtremeCandidate(")
    assert "!h4Owner.RecoveryComplete" in ext
    assert "!h4Owner.IsValid" in ext
    assert "h4Owner.State != H4_OWNER_ACTIVE" in ext


def test_targetless_lifecycle_never_manufactures_rr_or_tp():
    resolve = body("bool ResolveApprovedInitialSLTP(")
    validate = body("bool ValidateSLTP(")
    assert "decision.TakeProfit = targetlessLifecycle ? 0.0 : normalizedTP;" in resolve
    assert "if(MinRRRatio > 0.0)" in validate
    assert "REJ_INVALID_RR" in validate
    assert "ValidateFrozenBrokerDistanceGeometry(decision, snapshot, false, rejection)" in validate


def test_risk_unknown_observation_fails_closed():
    risk = body("RiskStatus CheckRiskBeforeTrade(")
    calc = body("double CalculateTotalRisk(")
    limits = body("PortfolioStatus CheckPortfolioLimits(")
    assert "if(!riskValid)" in risk and "REJ_TOTAL_RISK" in risk
    assert "if(newRisk <= 0)" in calc and "valid = false;" in calc
    assert "if(!OrderSelect(" in calc and "valid = false;" in calc
    assert "if(g_monitored_trades[i].current_sl <= 0)" in calc
    assert "if(existingRisk <= 0)" in calc
    assert "PORT_OWNERSHIP_UNKNOWN" in limits and "status.allowed = false;" in limits


def test_execution_error_classes_and_ambiguity_hold_are_fail_closed():
    retryable = body("bool IsRetryableError(")
    ambiguous = body("bool IsAmbiguousError(")
    send = body("int SendOrderWithRetry(")
    process = body("void ProcessEntry(")
    reconcile = body("bool ReconcileExecutionAmbiguityHold(")
    preflight = body("bool RunEntryPreflightAndExecute(")

    for code in ("135", "138", "146"):
        assert code in retryable
    for code in ("4", "6", "128", "141"):
        assert code in ambiguous

    assert "if(IsAmbiguousError(error))" in send
    ambiguous_block = send.split("if(IsAmbiguousError(error))", 1)[1].split("if(IsRetryableError(error))", 1)[0]
    assert "FindExistingExecutionTicket(" in ambiguous_block
    assert "return -2;" in ambiguous_block
    assert "retry++" not in ambiguous_block

    retry_block = send.split("if(IsRetryableError(error))", 1)[1]
    assert "retry++" in retry_block
    assert "retry < MaxRetry" in retry_block

    assert process.count("LatchExecutionAmbiguity(") >= 2
    assert "REJ_AMBIGUOUS_RESULT" in process
    assert "OrderSend(" not in reconcile
    assert "g_execution_ambiguity.Active" in preflight
    assert "REJ_AMBIGUOUS_RESULT" in preflight


def test_local_execution_identity_is_primary_over_broker_comment():
    process = body("void ProcessEntry(")
    assert "bool localIdentityPersisted = SaveExecutionIdentityHash(" in process
    assert "bool brokerHashMatch" in process
    assert "info.execution_hash = localIdentityPersisted" in process
    assert "? expectedExecutionHash" in process
    assert ": (brokerHashMatch ? brokerExecutionHash : \"\")" in process


def test_hard_invalid_and_ambiguity_results_remain_distinct():
    send = body("int SendOrderWithRetry(")
    process = body("void ProcessEntry(")
    assert "if(IsFatalError(error))" in send
    assert "return -1;" in send
    assert "return -2;" in send
    assert "if(ticket == -2)" in process
    assert "REJ_AMBIGUOUS_RESULT" in process
    assert "REJ_BROKER_ERROR" in process


def test_n3_and_observer_have_no_execution_authority():
    assert "N3_POLICY_ACTIVE" not in SRC
    assert "N3_EXECUTION_POLICY" not in SRC
    assert "REJ_NMJE_RELATION" not in SRC
    assert SRC.count("OrderSend(") == 1

    shadow = body("void NMJE_PrintValidatedDecisionShadow(")
    outcome = body("void NMJE_PrintClosedOutcomeShadow(")
    for forbidden in ("OrderSend(", "OrderClose(", "OrderModify(", "OrderDelete("):
        assert forbidden not in shadow
        assert forbidden not in outcome
