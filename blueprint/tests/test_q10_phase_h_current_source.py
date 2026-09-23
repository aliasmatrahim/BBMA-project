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


def test_r4_frozen_snapshot_is_single_and_shared_across_m17_m21_m19():
    preflight = body("bool RunEntryPreflightAndExecute(")
    assert preflight.count("RiskValidationSnapshot snapshot;") == 1
    assert preflight.count("BuildRiskValidationSnapshot(pair, decision, snapshot);") == 1
    assert "ResolveExecutionReferencePrice(decision, snapshot)" in preflight
    assert "ResolveApprovedInitialSLTP(decision, snapshot)" in preflight
    assert "snapshot.StopLoss = decision.StopLoss;" in preflight
    assert "ValidateSLTP(decision, snapshot, sltpRejection)" in preflight
    assert "CalculateLotSize(decision, snapshot, lotValid)" in preflight
    assert "CheckRiskBeforeTrade(decision, snapshot, lot)" in preflight


def test_r303_immediate_ema_close_slope_is_algebraically_coupled():
    ema = body("double EMA(")
    classify = body("bool M11_ClassifyD1OwnerValues(")
    update = body("void UpdateD1MajorTrendOwner(")

    assert "MODE_EMA, PRICE_CLOSE" in ema
    assert "#define EMA50_PERIOD            50" in SRC
    assert "close1 > ma50_1 && ma50_1 > ma50_2" in classify
    assert "close1 < ma50_1 && ma50_1 < ma50_2" in classify
    assert "state.d1_data.barIndex + 1" in update

    alpha = 2.0 / 51.0
    for previous, close in (
        (1.0, 1.2),
        (1.2, 1.0),
        (1.2345, 1.3456),
        (1.3456, 1.2345),
        (100.0, 101.0),
        (101.0, 100.0),
    ):
        current = alpha * close + (1.0 - alpha) * previous
        assert (close > current) == (current > previous)
        assert (close < current) == (current < previous)


def test_r3_transition_unresolved_and_h4_no_owner_are_fail_closed():
    classify = body("bool M11_ClassifyD1OwnerValues(")
    unresolved = body("void SetD1OwnerUnresolved(")
    ready = body("bool IsD1MajorTrendOwnerExecutionReady(")
    re = body("void BuildConfirmedReEntryCandidate(")
    ext = body("void BuildStandaloneExtremeCandidate(")

    assert "ownerState = D1_TRANSITION;" in classify
    transition_block = classify.split("else", 1)[1]
    assert "direction = DIR_NONE;" in transition_block

    assert "owner.State = D1_OWNER_UNRESOLVED;" in unresolved
    assert "owner.Direction = DIR_NONE;" in unresolved
    assert "owner.IsValid = false;" in unresolved

    assert "D1_OWNER_BUY_CONFIRMED" in ready
    assert "D1_OWNER_SELL_CONFIRMED" in ready
    assert ready.rstrip().endswith("return false;\n}")

    for candidate_builder in (re, ext):
        assert "!h4Owner.RecoveryComplete" in candidate_builder
        assert "!h4Owner.IsValid" in candidate_builder
        assert "h4Owner.State != H4_OWNER_ACTIVE" in candidate_builder


def test_r4_targetless_sell_sl_can_change_without_rr_tp_manufacture():
    resolve = body("bool ResolveApprovedInitialSLTP(")
    validate = body("bool ValidateSLTP(")

    assert "decision.TakeProfit = targetlessLifecycle ? 0.0 : normalizedTP;" in resolve
    assert "brokerSL += roundedSpreadBufferPips * pipValue;" in resolve
    assert "if(MinRRRatio > 0.0)" in validate
    assert "REJ_INVALID_RR" in validate
    # Validation may reject bad RR, but it has no authority to move TakeProfit.
    minrr = validate.split("if(MinRRRatio > 0.0)", 1)[1]
    assert "decision.TakeProfit =" not in minrr


def test_r4_source_owner_mismatch_is_fail_closed_without_window_substitution():
    match = body("bool ResolveMatchingReEntryLifecycle(")
    anchor = body("bool ResolveSourceOwnedStructuralAnchor(")
    resolve = body("bool ResolveApprovedInitialSLTP(")
    preflight = body("bool RunEntryPreflightAndExecute(")

    # Exact canonical owner identity is mandatory.
    assert "reEntry.Direction != source.Direction" in match
    assert "reEntry.Timeframe != source.Timeframe" in match
    assert "reEntry.ConfirmationCandle != source.CandleTime" in match
    assert "return false;" in match

    # M17 resolves only that source-owned lifecycle/window and fails closed.
    assert "if(!ResolveMatchingReEntryLifecycle(pair, source, reEntry)) return false;" in anchor
    assert "iBarShift(pair, source.Timeframe, startTime, true)" in anchor
    assert "iBarShift(pair, source.Timeframe," in anchor
    assert "if(iTime(pair, source.Timeframe, startShift) != startTime) return false;" in anchor
    assert "if(!IsCandleClosed(barTime, tfSeconds)) return false;" in anchor

    assert "bool structuralResolved = standaloneExtreme" in resolve
    assert "? ResolveStandaloneExtremeStructuralAnchor(" in resolve
    assert ": ResolveSourceOwnedStructuralAnchor(" in resolve
    assert "if(!structuralResolved) return false;" in resolve

    # Preflight converts unresolved source-owned SL/TP into an attributable reject;
    # it does not try another timeframe/window.
    assert "if(!ResolveApprovedInitialSLTP(decision, snapshot))" in preflight
    reject = preflight.split("if(!ResolveApprovedInitialSLTP(decision, snapshot))", 1)[1].split("snapshot.StopLoss", 1)[0]
    assert "DEC_REJECTED" in reject
    assert "REJ_SLTP_UNRESOLVED" in reject


def test_r5_unknown_existing_risk_never_becomes_zero_budget():
    calc = body("double CalculateTotalRisk(")
    risk = body("RiskStatus CheckRiskBeforeTrade(")

    for fail_closed in (
        "if(!OrderSelect(",
        "if(g_monitored_trades[i].current_sl <= 0)",
        "if(existingRisk <= 0)",
        "if(newRisk <= 0)",
    ):
        assert fail_closed in calc

    assert calc.count("valid = false;") >= 4
    assert "if(!riskValid)" in risk
    unresolved = risk.split("if(!riskValid)", 1)[1].split("double equity", 1)[0]
    assert "status.allowed = false;" in unresolved
    assert "REJ_TOTAL_RISK" in unresolved
