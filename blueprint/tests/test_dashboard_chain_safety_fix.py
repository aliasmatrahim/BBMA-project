#!/usr/bin/env python3
from pathlib import Path
from tempfile import TemporaryDirectory
import importlib.util


def load_module():
    path = Path('blueprint/tools/dashboard_chain_safety_fix.py')
    spec = importlib.util.spec_from_file_location('dashboard_chain_safety_fix', path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_module()

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

    old_decision_display = '''      if(DashDecisionComplete(state))
      {
         setup += "✓";
         if(rank < 40) rank = 40;
      }
      else if(state.last_decision.DecisionState == DEC_REJECTED ||
              state.last_decision.DecisionState == DEC_EXPIRED)
      {
         status = "INV";
      }'''

    fixture = (
        'UNRELATED_PREFIX\n' + old_live + '\nMID_A\n' + old_rank +
        '\nMID_B\n' + old_refresh + '\nMID_C\n' + old_decision_helper +
        '\nMID_D\n' + old_decision_display + '\nUNRELATED_SUFFIX\n'
    )

    with TemporaryDirectory() as td:
        target = Path(td) / 'BBMA_EA.mq4'
        target.write_text(fixture, encoding='utf-8')
        module.SRC = target
        rc = module.main()
        assert rc == 0, rc
        out = target.read_text(encoding='utf-8')

    assert 'UNRELATED_PREFIX' in out
    assert 'UNRELATED_SUFFIX' in out
    assert 'int buyCount = 0;' in out
    assert 'int sellCount = 0;' in out
    assert 'POS↑x' in out and 'POS↓x' in out
    assert 'status = "MIX";' in out
    assert 'chain = "B:" + buyChain + " | S:" + sellChain;' in out
    assert 'if(buyRank >= sellRank)' not in out
    assert out.count('string DashLivePosition(') == 1

    assert 'string DashLivePositionSignature()' in out
    assert 'IntegerToString(OrderTicket())' in out
    assert 'static string lastLiveSignature = "__INIT__";' in out
    assert 'if(currentLiveSignature == lastLiveSignature) return;' in out
    assert '// Timer refresh keeps both chain lifecycle and live broker position in sync.' not in out
    assert out.count('void RefreshDashboardLiveTradeCount()') == 1

    assert 'bool DashDecisionComplete(PairState &state)' not in out
    assert 'bool DashDecisionValidated(PairState &state)' in out
    assert 'bool DashDecisionExecuted(PairState &state)' in out
    assert 'status = "VAL";' in out
    assert 'status = "EXE";' in out
    assert 'setup += "~";' in out
    assert 'setup += "✓";' in out
    assert 'DEC_VALIDATED ||' not in out
    assert 'if(DashDecisionExecuted(state))' in out
    assert 'else if(DashDecisionValidated(state))' in out

    print('DASHBOARD_CHAIN_SAFETY_FIX_SELFTEST=PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
