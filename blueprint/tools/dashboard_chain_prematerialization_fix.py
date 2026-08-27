#!/usr/bin/env python3
"""Final prematerialization hardening for the isolated compact dashboard.

This stage runs after dashboard_chain_safety_fix.py and fixes three display-only
issues discovered by static review:
1. make the live-position refresh signature independent of MT4 order-pool
   enumeration order;
2. keep displayed SETUP and CHAIN in the same REM/RRE/REE/RE family when a
   last decision is shown;
3. remove BBMA_DASH_ chart objects during EA deinitialization.

No strategy, risk, validation, lifecycle or execution authority is added.
"""
from pathlib import Path
import sys

SRC = Path('blueprint/source/BBMA_EA.mq4')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected exactly one match, got {count}')
    return text.replace(old, new, 1)


def main() -> int:
    text = SRC.read_text(encoding='utf-8')

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

    new_signature = '''string DashLivePositionSignature()
{
   // Build an order-invariant identity set. SELECT_BY_POS enumeration order is
   // not presentation authority and must not cause false dashboard redraws.
   int tickets[];
   int pairIndexes[];
   int orderTypes[];
   int owned = 0;
   int total = OrdersTotal();

   for(int i = 0; i < total; i++)
   {
      if(!OrderSelect(i, SELECT_BY_POS, MODE_TRADES)) continue;
      int selectedPairIndex = -1;
      if(!IsExactEAOwnedSelectedOrder(selectedPairIndex)) continue;

      ArrayResize(tickets, owned + 1);
      ArrayResize(pairIndexes, owned + 1);
      ArrayResize(orderTypes, owned + 1);
      tickets[owned] = OrderTicket();
      pairIndexes[owned] = selectedPairIndex;
      orderTypes[owned] = OrderType();
      owned++;
   }

   // Ticket is unique for live MT4 orders, so ticket-ordering is a stable key.
   for(int a = 1; a < owned; a++)
   {
      int keyTicket = tickets[a];
      int keyPair = pairIndexes[a];
      int keyType = orderTypes[a];
      int b = a - 1;
      while(b >= 0 && tickets[b] > keyTicket)
      {
         tickets[b + 1] = tickets[b];
         pairIndexes[b + 1] = pairIndexes[b];
         orderTypes[b + 1] = orderTypes[b];
         b--;
      }
      tickets[b + 1] = keyTicket;
      pairIndexes[b + 1] = keyPair;
      orderTypes[b + 1] = keyType;
   }

   string signature = "";
   for(int s = 0; s < owned; s++)
   {
      signature += IntegerToString(pairIndexes[s]) + ":" +
                   IntegerToString(tickets[s]) + ":" +
                   IntegerToString(orderTypes[s]) + ";";
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

    new_decision = '''      string finalSetup = DashSignalText(state.last_decision.SignalType);
      if(finalSetup != "-")
      {
         setup = finalSetup;

         // Keep SETUP and CHAIN in the same family. If the current component
         // lifecycle no longer reconstructs the full family, show a DEC marker
         // rather than pairing the decision with another family's chain.
         if(finalSetup == "REM")
         {
            chain = "DEC:REM" + arrow;
            if(DashREConfirmed(h4re, direction))
            {
               chain = "H4:RE" + arrow;
               if(DashExtremeReady(h1ext, direction))
               {
                  chain += ">H1:EXT" + arrow;
                  if(DashMLVReady(m15mlv, direction))
                     chain += ">M15:MHV" + arrow;
               }
            }
         }
         else if(finalSetup == "RRE")
         {
            chain = "DEC:RRE" + arrow;
            if(DashREConfirmed(d1re, direction))
            {
               chain = "D1:RE" + arrow;
               if(DashREConfirmed(h4re, direction))
               {
                  chain += ">H4:RE" + arrow;
                  if(DashExtremeReady(h1ext, direction))
                     chain += ">H1:EXT" + arrow;
               }
            }
         }
         else if(finalSetup == "REE")
         {
            chain = "DEC:REE" + arrow;
            if(DashREConfirmed(d1re, direction))
            {
               chain = "D1:RE" + arrow;
               if(DashExtremeReady(h4ext, direction))
               {
                  chain += ">H4:EXT" + arrow;
                  if(DashExtremeReady(h1ext, direction))
                     chain += ">H1:EXT" + arrow;
               }
            }
         }
         else if(finalSetup == "RE")
         {
            chain = "DEC:RE" + arrow;
            if(DashREConfirmed(h1re, direction))
               chain = "H1:RE" + arrow;
         }
      }

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

    new_deinit = '''   g_is_scanning = false;
   g_is_managing_trade = false;
   g_dashboard_needs_update = false;

   // Display cleanup only. Never leave BBMA_DASH_ labels orphaned after EA
   // removal, recompile or chart shutdown.
   ClearDashboardObjects();
   Comment("");
   Log(DBG_FULL, "EA deinitialized, reason: " + IntegerToString(reason));'''

    try:
        text = replace_once(text, old_signature, new_signature,
                            'order-invariant live signature')
        text = replace_once(text, old_decision, new_decision,
                            'setup/chain family consistency')
        text = replace_once(text, old_deinit, new_deinit,
                            'dashboard deinit cleanup')
    except RuntimeError as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 3

    required = [
        'int tickets[];',
        'int pairIndexes[];',
        'int orderTypes[];',
        'ArrayResize(tickets, owned + 1);',
        'while(b >= 0 && tickets[b] > keyTicket)',
        'IntegerToString(tickets[s])',
        'chain = "DEC:REM" + arrow;',
        'chain = "DEC:RRE" + arrow;',
        'chain = "DEC:REE" + arrow;',
        'chain = "DEC:RE" + arrow;',
        'ClearDashboardObjects();\n   Comment("");',
    ]
    for token in required:
        if token not in text:
            print(f'ERROR: required prematerialization token missing: {token}',
                  file=sys.stderr)
            return 4

    forbidden = [
        old_signature,
        'if(ShowDashboard)\n      Comment("");\n   Log(DBG_FULL, "EA deinitialized',
    ]
    for token in forbidden:
        if token in text:
            print(f'ERROR: forbidden prematerialization token remains: {token[:80]}',
                  file=sys.stderr)
            return 5

    SRC.write_text(text, encoding='utf-8')
    print('DASHBOARD_PREMATERIALIZATION_FIX=APPLIED')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
