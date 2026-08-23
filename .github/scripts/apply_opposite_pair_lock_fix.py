from pathlib import Path

p = Path('blueprint/source/BBMA_EA.mq4')
s = p.read_text(encoding='utf-8')

old_header = 'Version 4.5.1 - P3-M2-11 Mode2 Diagnostic Trace'
new_header = 'Version 4.5.1 - P3-M2-11.1 Mode2 Diagnostic Closure'
if s.count(old_header) != 1:
    raise SystemExit(f'build header anchor count={s.count(old_header)}')
s = s.replace(old_header, new_header, 1)

old = '''   if(decision.DecisionState == DEC_VALIDATED)
      RunEntryPreflightAndExecute(decision, actual);
   g_pair_states[pairIndex].last_decision = decision;
'''
new = '''   if(decision.DecisionState == DEC_VALIDATED)
      RunEntryPreflightAndExecute(decision, actual);

   if(EntryMode == 2 && decision.Valid)
      Print("[P3M2][DECISION_FINAL] Pair=", actual,
            " Signal=", EnumToString(decision.SignalType),
            " Dir=", EnumToString(decision.Direction),
            " State=", EnumToString(decision.DecisionState),
            " Reason=", EnumToString(decision.RejectionReason),
            " DecisionID=", decision.DecisionID);

   g_pair_states[pairIndex].last_decision = decision;
'''
if s.count(old) != 1:
    raise SystemExit(f'final decision trace anchor count={s.count(old)}')
s = s.replace(old, new, 1)

if '[P3M2][DECISION_FINAL]' not in s:
    raise SystemExit('final decision trace missing')
if s.count('{') != s.count('}'):
    raise SystemExit('brace imbalance')

p.write_text(s, encoding='utf-8')
print('P3-M2-11.1 final decision trace closure applied')
