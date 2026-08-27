#!/usr/bin/env python3
from pathlib import Path
from tempfile import TemporaryDirectory
import importlib.util


def load_module():
    path = Path('blueprint/tools/dashboard_chain_prematerialization_fix.py')
    spec = importlib.util.spec_from_file_location('dashboard_chain_prematerialization_fix', path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_module()

    old_signature = '''string DashLivePositionSignature()
{
   string signature = "";
   int total = OrdersTotal();
   for(int i = 0; i < total; i++)
   {
      if(!OrderSelect(i, SELECT_BY_POS, MODE_TRADES)) continue;
      int selectedPairIndex = -1;
      if(!IsExactEAOwnedSelectedOrder(selectedPairIndex)) continue;
      signature += IntegerToString(selectedPairIndex) + ":" +
                   IntegerToString(OrderTicket()) + ":" +
                   IntegerToString(OrderType()) + ";";
   }
   return signature;
}'''

    old_decision = '''      string finalSetup = DashSignalText(state.last_decision.SignalType);
      if(finalSetup != "-") setup = finalSetup;
      if(DashDecisionExecuted(state))
      {
         setup += "✓";
         status = "EXE";
         if(rank < 40) rank = 40;
      }
      else if(DashDecisionValidated(state))
      {
         // Validation is not execution. Keep it visible without the execution
         // check mark so operators never infer that a broker order exists.
         setup += "~";
         status = "VAL";
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
        'PREFIX\n' + old_signature + '\nMID1\n' + old_decision +
        '\nMID2\n' + old_deinit + '\nSUFFIX\n'
    )

    with TemporaryDirectory() as td:
        target = Path(td) / 'BBMA_EA.mq4'
        target.write_text(fixture, encoding='utf-8')
        module.SRC = target
        rc = module.main()
        assert rc == 0, rc
        out = target.read_text(encoding='utf-8')

    assert 'PREFIX' in out and 'SUFFIX' in out

    # Order-invariant live signature hardening.
    assert 'int tickets[];' in out
    assert 'int pairIndexes[];' in out
    assert 'int orderTypes[];' in out
    assert 'ArrayResize(tickets, owned + 1);' in out
    assert 'while(b >= 0 && tickets[b] > keyTicket)' in out
    assert 'IntegerToString(tickets[s])' in out
    assert old_signature not in out
    assert out.count('string DashLivePositionSignature()') == 1

    # Setup/chain family consistency.
    assert 'chain = "DEC:REM" + arrow;' in out
    assert 'chain = "DEC:RRE" + arrow;' in out
    assert 'chain = "DEC:REE" + arrow;' in out
    assert 'chain = "DEC:RE" + arrow;' in out
    assert 'if(finalSetup == "REM")' in out
    assert 'else if(finalSetup == "RRE")' in out
    assert 'else if(finalSetup == "REE")' in out
    assert 'else if(finalSetup == "RE")' in out
    assert 'setup += "✓";' in out
    assert 'setup += "~";' in out

    # Deinitialization must remove chart objects even when ShowDashboard is false.
    assert 'ClearDashboardObjects();\n   Comment("");' in out
    assert 'if(ShowDashboard)\n      Comment("");\n   Log(DBG_FULL, "EA deinitialized' not in out

    print('DASHBOARD_PREMATERIALIZATION_FIX_SELFTEST=PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
