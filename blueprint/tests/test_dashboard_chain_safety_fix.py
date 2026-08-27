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

    fixture = (
        'UNRELATED_PREFIX\n' + old_live + '\nMID_A\n' + old_rank +
        '\nMID_B\n' + old_refresh + '\nUNRELATED_SUFFIX\n'
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

    print('DASHBOARD_CHAIN_SAFETY_FIX_SELFTEST=PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
