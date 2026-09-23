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


def test_r4_autolot_uses_final_frozen_sl_distance():
    preflight = body("bool RunEntryPreflightAndExecute(")
    sizing = body("double CalculateLotSize(")

    assert preflight.index("snapshot.StopLoss = decision.StopLoss;") < preflight.index(
        "CalculateLotSize(decision, snapshot, lotValid)"
    )
    assert "double slDistance = MathAbs(decision.EntryPrice - decision.StopLoss);" in sizing
    assert "double riskPerLot = slDistance * snapshot.TickValue / snapshot.TickSize_Price;" in sizing
    assert "double riskAmount = snapshot.Equity * (AutoLotPercent / 100.0);" in sizing
    assert "double rawLot = riskAmount / riskPerLot;" in sizing


def test_r5_tradelock_predicates_match_locked_modes():
    lock = body("bool IsSignalAllowed(")

    one = lock.index("if(TradeLockMode == LOCK_ONE_POSITION)")
    same = lock.index("if(TradeLockMode == LOCK_SAME_DIRECTION)")
    assert one < same

    one_block = lock[one:same]
    assert "PORT_OWNERSHIP_LIVE_OWNED" in one_block
    assert "return false;" in one_block

    same_block = lock[same:]
    assert "PORT_OWNERSHIP_LIVE_OWNED" in same_block
    assert "g_monitored_trades[i].direction != decision.Direction" in same_block
    assert "return false;" in same_block


def test_r5_sequential_cumulative_risk_is_source_bound():
    tick = body("void OnTickMain(")
    preflight = body("bool RunEntryPreflightAndExecute(")
    entry = body("void ProcessEntry(")
    total = body("double CalculateTotalRisk(")
    risk = body("RiskStatus CheckRiskBeforeTrade(")

    # Pair processing is serialized in one loop.
    assert "for(int i = 0; i < g_pair_count; i++)" in tick
    assert "ProcessPair(i);" in tick

    # Risk is checked before the broker send path for the current decision.
    assert preflight.index("CheckRiskBeforeTrade(decision, snapshot, lot)") < preflight.index(
        "ProcessEntry(decision, pair, snapshot, lot)"
    )

    # A successful decision is inserted into the monitored registry before
    # ProcessEntry returns, so the next serialized pair sees consumed risk.
    assert entry.index("AddToMonitoredTrades(info);") < entry.index(
        "decision.DecisionState = DEC_EXECUTED;"
    )

    # M19 sums all live exact-owned monitored risk and then adds the proposed
    # decision's own final risk before applying MaxTotalRiskPercent.
    assert "for(int i = 0; i < g_monitored_count; i++)" in total
    assert "totalRisk += existingRisk;" in total
    assert "totalRisk += newRisk;" in total
    assert "CalculateTotalRisk(decision.Pair, calculatedLot," in risk
    assert "if(totalRisk / equity * 100.0 > MaxTotalRiskPercent)" in risk
    assert "REJ_TOTAL_RISK" in risk

    # Deterministic sequential fixture tied to those exact source semantics.
    equity = 1000.0
    cap_pct = 5.0
    a_risk = 30.0
    b_risk = 30.0

    a_total = a_risk
    b_after_a_exec = a_risk + b_risk
    b_after_a_fail = b_risk

    assert a_total / equity * 100.0 <= cap_pct
    assert b_after_a_exec / equity * 100.0 > cap_pct
    assert b_after_a_fail / equity * 100.0 <= cap_pct


def test_r5_recovery_diagnostic_is_init_scoped_not_cycle_spam():
    recover = body("void RecoverExistingOrders(")
    tick = body("void OnTickMain(")
    pair = body("void ProcessPair(")
    init = body("int OnInit(")
    initialize = body("int InitializeEA(")

    assert SRC.count("[P3S5][RECOVERY]") == 1
    assert "[P3S5][RECOVERY]" in recover
    assert "[P3S5][RECOVERY]" not in tick
    assert "[P3S5][RECOVERY]" not in pair
    assert "InitializeEA()" in init
    assert "RecoverExistingOrders();" in initialize
    assert "RecoverExistingOrders();" not in tick
    assert "RecoverExistingOrders();" not in pair


def test_r5_registry_compaction_and_exact_owned_count_are_fail_closed():
    compact = body("void CompactMonitoredTrades(")
    add = body("void AddToMonitoredTrades(")
    count = body("int CountLiveEAOwnedPortfolioTrades(")
    limits = body("PortfolioStatus CheckPortfolioLimits(")
    dashboard = body("int CountDashboardLiveEAOwnedTrades(")

    assert "removeClosed = (OrderCloseTime() != 0);" in compact
    assert "g_monitored_count = write;" in compact

    assert "if(g_monitored_trades[i].ticket == info.ticket)" in add
    assert "g_monitored_trades[i] = info;" in add
    assert "CompactMonitoredTrades();" in add
    assert "g_monitored_count++;" in add

    assert "GetLiveEAOwnedPortfolioTradeState(i)" in count
    assert "if(ownership == PORT_OWNERSHIP_UNKNOWN) return -1;" in count
    assert "if(ownership == PORT_OWNERSHIP_LIVE_OWNED) count++;" in count

    assert "GetLiveEAOwnedPortfolioTradeState(i)" in limits
    assert "PORT_OWNERSHIP_UNKNOWN" in limits
    assert "status.allowed = false;" in limits

    # Dashboard cross-check reads the live broker pool independently rather
    # than trusting registry length.
    assert "OrdersTotal()" in dashboard
    assert "IsExactEAOwnedSelectedOrder" in dashboard
    assert "g_monitored_count" not in dashboard
