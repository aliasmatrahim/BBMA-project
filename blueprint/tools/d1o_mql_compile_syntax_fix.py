#!/usr/bin/env python3
"""Compile-safety normalizer for D1O generated MQL4.

This contains no strategy change. It replaces a few compact expressions emitted
by the D1O patcher with explicit assignments that are safer under strict MQL4
struct/enum typing. Apply only after d1_opportunity_execution_patch.py.
"""
from pathlib import Path

p = Path('blueprint/source/BBMA_EA.mq4')
text = p.read_text(encoding='utf-8')
if 'Version 4.5.1 - D1O-02 Opportunity Execution' not in text:
    raise SystemExit('D1O generated source not present')


def repl(old: str, new: str, label: str):
    global text
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1, got {n}')
    text = text.replace(old, new, 1)

repl(
'''   selected = buyValid ? buyState : sellState;
   return true;
''',
'''   if(buyValid) selected = buyState;
   else selected = sellState;
   return true;
''', 'D1 RE struct conditional assignment')

repl(
'''   selected = buyValid ? buyState : sellState;
   return true;
}

bool D1OpportunityTPWCompletedSince''',
'''   if(buyValid) selected = buyState;
   else selected = sellState;
   return true;
}

bool D1OpportunityTPWCompletedSince''', 'D1 Extreme struct conditional assignment')

repl(
'''      ReEntryData owner = (next.Direction == DIR_BUY)
                          ? g_pair_states[pairIndex].re_d1_buy_state
                          : g_pair_states[pairIndex].re_d1_sell_state;
''',
'''      ReEntryData owner;
      ZeroMemory(owner);
      if(next.Direction == DIR_BUY)
         owner = g_pair_states[pairIndex].re_d1_buy_state;
      else
         owner = g_pair_states[pairIndex].re_d1_sell_state;
''', 'persistent D1 RE owner assignment')

repl(
'''      ExtremeLifecycleData owner = (next.Direction == DIR_BUY)
                                   ? g_pair_states[pairIndex].extreme_d1_buy_lifecycle
                                   : g_pair_states[pairIndex].extreme_d1_sell_lifecycle;
''',
'''      ExtremeLifecycleData owner;
      ZeroMemory(owner);
      if(next.Direction == DIR_BUY)
         owner = g_pair_states[pairIndex].extreme_d1_buy_lifecycle;
      else
         owner = g_pair_states[pairIndex].extreme_d1_sell_lifecycle;
''', 'persistent D1 Extreme owner assignment')

repl(
'''   ReEntryData h1 = (opportunity.Direction == DIR_BUY)
                     ? state.re_h1_buy_state : state.re_h1_sell_state;
   ReEntryData m15 = (opportunity.Direction == DIR_BUY)
                      ? state.re_m15_buy_state : state.re_m15_sell_state;
''',
'''   ReEntryData h1, m15;
   ZeroMemory(h1); ZeroMemory(m15);
   if(opportunity.Direction == DIR_BUY)
   {
      h1 = state.re_h1_buy_state;
      m15 = state.re_m15_buy_state;
   }
   else
   {
      h1 = state.re_h1_sell_state;
      m15 = state.re_m15_sell_state;
   }
''', 'LTF RE struct assignment')

repl(
'''   return MathMin(a, b);
}
''',
'''   return (a < b) ? a : b;
}
''', 'datetime min typing')

p.write_text(text, encoding='utf-8')
print('D1O compile-safety syntax normalizer PASS')
