#!/usr/bin/env python3
from pathlib import Path
from tempfile import TemporaryDirectory
import importlib.util


def load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> int:
    safety = load_module(
        'blueprint/tools/dashboard_chain_safety_fix.py',
        'dashboard_chain_safety_fix_stage',
    )
    premat = load_module(
        'blueprint/tools/dashboard_chain_prematerialization_fix.py',
        'dashboard_chain_prematerialization_fix_stage',
    )

    old_live = '''string DashLivePosition(int pairIndex, ENUM_DIRECTION &direction)
{
   direction = DIR_NONE;
   int total = OrdersTotal();
   for(int i = 0; i < total; i++)
   {
      if(!OrderSelect(i, SELECT_BY_POS, MODE_TRADES)) continue;
      int selectedPairIndex = -1;
      if(!IsExactEAOwnedSelectedOrder(selectedPairIndex)) continue;
      if(selectedPairIndex != pairIndex) continue;
      int type = OrderType();
      if(type == OP_BUY)
      {
         direction = DIR_BUY;
         return "POS↑";
      }
      if(type == OP_SELL)
      {
         direction = DIR_SELL;
         return "POS↓";
      }
   }
   return "";
}'''

    old_rank = '''   if(buyRank > 0 || sellRank > 0)
   {
      if(buyRank >= sellRank)
      {
         rowDirection = DIR_BUY;
         status = buyStatus;
         setup = buySetup;
         chain = buyChain;
      }
      else
      {
         rowDirection = DIR_SELL;
         status = sellStatus;
         setup = sellSetup;
         chain = sellChain;
      }
   }

   position = DashLivePosition(pairIndex, positionDirection);'''

    old_refresh = '''void RefreshDashboardLiveTradeCount()
{
   if(!ShowDashboard) return;
   // Timer refresh keeps both chain lifecycle and live broker position in sync.
   UpdateDashboard();
   g_dashboard_needs_update = false;
}'''

    old_decision_helper = '''bool DashDecisionComplete(PairState &state)
{
   if(!state.last_decision.Valid) return false;
   return (state.last_decision.DecisionState == DEC_VALIDATED ||
           state.last_decision.DecisionState == DEC_EXECUTED);
}'''

    old_decision_display = '''      string finalSetup = DashSignalText(state.last_decision.SignalType);
      if(finalSetup != "-") setup = finalSetup;
      if(DashDecisionComplete(state))
      {
         setup += "✓";
         if(rank < 40) rank = 40;
      }
      else if(state.last_decision.DecisionState == DEC_REJECTED ||
              state.last_decision.DecisionState == DEC_EXPIRED)
      {
         status = "INV";
      }'''

    old_deinit = '''   g_is_scanning = false;
   g_is_managing_trade = false;
   g_dashboard_needs_update = false;
   if(ShowDashboard)
      Comment("");
   Log(DBG_FULL, "EA deinitialized, reason: " + IntegerToString(reason));'''

    fixture = (
        'COMPOSITION_PREFIX\n' + old_live + '\nMID_A\n' + old_rank +
        '\nMID_B\n' + old_refresh + '\nMID_C\n' + old_decision_helper +
        '\nMID_D\n' + old_decision_display + '\nMID_E\n' + old_deinit +
        '\nCOMPOSITION_SUFFIX\n'
    )

    with TemporaryDirectory() as td:
        target = Path(td) / 'BBMA_EA.mq4'
        target.write_text(fixture, encoding='utf-8')
        safety.SRC = target
        premat.SRC = target

        rc1 = safety.main()
        assert rc1 == 0, rc1
        after_safety = target.read_text(encoding='utf-8')

        # Producer/consumer handoff contract: these are the exact classes of
        # text the prematerialization stage is expected to consume.
        assert 'string DashLivePositionSignature()' in after_safety
        assert 'bool DashDecisionValidated(PairState &state)' in after_safety
        assert 'bool DashDecisionExecuted(PairState &state)' in after_safety
        assert 'if(finalSetup != "-") setup = finalSetup;' in after_safety
        assert old_deinit in after_safety

        rc2 = premat.main()
        assert rc2 == 0, rc2
        out = target.read_text(encoding='utf-8')

    assert 'COMPOSITION_PREFIX' in out and 'COMPOSITION_SUFFIX' in out

    # Primary safety stage survives the second stage.
    assert 'int buyCount = 0;' in out
    assert 'int sellCount = 0;' in out
    assert 'status = "MIX";' in out
    assert 'bool DashDecisionValidated(PairState &state)' in out
    assert 'bool DashDecisionExecuted(PairState &state)' in out
    assert 'status = "VAL";' in out
    assert 'status = "EXE";' in out

    # Prematerialization stage hardens without consuming unrelated changes.
    assert 'int tickets[];' in out
    assert 'int pairIndexes[];' in out
    assert 'int orderTypes[];' in out
    assert 'while(b >= 0 && tickets[b] > keyTicket)' in out
    assert 'chain = "DEC:REM" + arrow;' in out
    assert 'chain = "DEC:RRE" + arrow;' in out
    assert 'chain = "DEC:REE" + arrow;' in out
    assert 'chain = "DEC:RE" + arrow;' in out
    assert 'DashREConfirmed(h4re, direction) &&' in out
    assert 'DashMLVReady(m15mlv, direction))' in out
    assert 'DashREConfirmed(d1re, direction) &&' in out
    assert 'DashExtremeReady(h4ext, direction) &&' in out
    assert 'ClearDashboardObjects();\n   Comment("");' in out

    # Old unsafe/redundant contracts must be gone after the full chain.
    assert 'if(buyRank >= sellRank)' not in out
    assert 'bool DashDecisionComplete(PairState &state)' not in out
    assert 'if(finalSetup != "-") setup = finalSetup;' not in out
    assert '// Timer refresh keeps both chain lifecycle and live broker position in sync.' not in out
    assert 'if(ShowDashboard)\n      Comment("");\n   Log(DBG_FULL, "EA deinitialized' not in out

    assert out.count('string DashLivePosition(') == 1
    assert out.count('string DashLivePositionSignature()') == 1
    assert out.count('void RefreshDashboardLiveTradeCount()') == 1

    print('DASHBOARD_STAGE_COMPOSITION_SELFTEST=PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
