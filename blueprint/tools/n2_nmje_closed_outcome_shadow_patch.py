from pathlib import Path
import subprocess

SRC = Path('blueprint/source/BBMA_EA.mq4')
EXPECTED_BLOB = 'eb55cd82f0c8c00b09f7191394fedae8f80c37c2'


def git_blob(path: Path) -> str:
    return subprocess.check_output(['git', 'hash-object', str(path)], text=True).strip()


def extract_function(text: str, name: str) -> str:
    needle = name + '('
    pos = text.find(needle)
    if pos < 0:
        raise RuntimeError(f'function not found: {name}')
    line_start = text.rfind('\n', 0, pos) + 1
    brace = text.find('{', pos)
    if brace < 0:
        raise RuntimeError(f'opening brace not found: {name}')
    depth = 0
    i = brace
    in_string = False
    escape = False
    while i < len(text):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == '\\':
                escape = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return text[line_start:i + 1]
        i += 1
    raise RuntimeError(f'unterminated function: {name}')


if not SRC.exists():
    raise SystemExit('source missing')

actual = git_blob(SRC)
if actual != EXPECTED_BLOB:
    raise SystemExit(f'unexpected baseline source blob: {actual}')

text = SRC.read_text(encoding='utf-8')
if '[N2-NMJE-OUT]' in text:
    raise SystemExit('N2 closed-outcome shadow already present')
if 'NMJE_LogIdentityToken' not in text or '[N2-NMJE-DEC]' not in text:
    raise SystemExit('N2-01A decision telemetry prerequisite missing')

critical_names = [
    'BuildPossibleCombinations',
    'ValidateSequence',
    'PriorityEngine_Atomic',
    'InvalidationEngine_Atomic',
    'ResolveApprovedInitialSLTP',
    'RunEntryPreflightAndExecute',
    'ManagePositions',
]
critical_before = {name: extract_function(text, name) for name in critical_names}
append_count_before = text.count('AppendValidatedCandidate(')
order_send_before = text.count('OrderSend(')
order_close_before = text.count('OrderClose(')
order_modify_before = text.count('OrderModify(')

old_compact = '''void CompactMonitoredTrades()\n{\n   int write = 0;\n   for(int i = 0; i < g_monitored_count; i++)\n   {\n      bool removeClosed = false;\n      if(OrderSelect(g_monitored_trades[i].ticket, SELECT_BY_TICKET))\n         removeClosed = (OrderCloseTime() != 0);\n      if(removeClosed) continue;\n      if(write != i) g_monitored_trades[write] = g_monitored_trades[i];\n      write++;\n   }\n   g_monitored_count = write;\n}\n'''
if text.count(old_compact) != 1:
    raise SystemExit(f'CompactMonitoredTrades anchor count={text.count(old_compact)}')

new_compact = r'''// N2-13: read-only closed-order outcome telemetry.
// Called only after OrderSelect() proves that the monitored ticket is closed.
// It never changes order state, trade lifecycle, risk, exit logic or registry identity.
void NMJE_PrintClosedOutcomeShadow(TradeInfo &info)
{
   if(info.ticket <= 0 || info.pair == "") return;
   if(OrderTicket() != info.ticket) return;
   if(OrderCloseTime() == 0) return;

   // Fail closed on registry/order identity mismatch rather than attributing
   // realized P/L to the wrong research identity.
   if(OrderSymbol() != info.pair) return;
   if(info.magic_number <= 0 || OrderMagicNumber() != info.magic_number) return;

   string decisionToken = "-";
   if(info.decision_id != "")
      decisionToken = NMJE_LogIdentityToken(info.decision_id);

   string decisionHash = info.execution_hash;
   if(decisionHash == "") decisionHash = "-";

   double netProfit = OrderProfit() + OrderSwap() + OrderCommission();

   Print("[N2-NMJE-OUT] PAIR=", info.pair,
         " TICKET=", IntegerToString(info.ticket),
         " DID=", decisionToken,
         " DIDH=", decisionHash,
         " NET=", DoubleToString(netProfit, 8),
         " CLOSE=", IntegerToString((int)OrderCloseTime()),
         " REC=", EnumToString(info.recovery_state));
}

void CompactMonitoredTrades()
{
   int write = 0;
   for(int i = 0; i < g_monitored_count; i++)
   {
      bool removeClosed = false;
      if(OrderSelect(g_monitored_trades[i].ticket, SELECT_BY_TICKET))
         removeClosed = (OrderCloseTime() != 0);
      if(removeClosed)
      {
         // Emit at most once: the row is discarded immediately afterwards.
         NMJE_PrintClosedOutcomeShadow(g_monitored_trades[i]);
         continue;
      }
      if(write != i) g_monitored_trades[write] = g_monitored_trades[i];
      write++;
   }
   g_monitored_count = write;
}
'''

text = text.replace(old_compact, new_compact, 1)
text = text.replace('Version 4.5.1 - N2-01 NMJE Decision Shadow',
                    'Version 4.5.1 - N2-13 Closed Outcome Shadow', 1)
text = text.replace('BBMA EA V4.5.1 N2-01 initialized successfully',
                    'BBMA EA V4.5.1 N2-13 initialized successfully', 1)

for name in critical_names:
    after = extract_function(text, name)
    if after != critical_before[name]:
        raise SystemExit(f'critical function changed unexpectedly: {name}')

if text.count('AppendValidatedCandidate(') != append_count_before:
    raise SystemExit('candidate append count changed')
if text.count('OrderSend(') != order_send_before:
    raise SystemExit('OrderSend call count changed')
if text.count('OrderClose(') != order_close_before:
    raise SystemExit('OrderClose call count changed')
if text.count('OrderModify(') != order_modify_before:
    raise SystemExit('OrderModify call count changed')
if text.count('NMJE_PrintClosedOutcomeShadow(g_monitored_trades[i]);') != 1:
    raise SystemExit('closed-outcome shadow call must appear exactly once')
if text.count('[N2-NMJE-OUT]') != 1:
    raise SystemExit('closed-outcome marker must appear exactly once in source')

shadow = extract_function(text, 'NMJE_PrintClosedOutcomeShadow')
for forbidden in ['OrderSend(', 'OrderClose(', 'OrderModify(', 'PriorityEngine_Atomic(',
                  'InvalidationEngine_Atomic(', 'RunEntryPreflightAndExecute(']:
    if forbidden in shadow:
        raise SystemExit(f'forbidden ownership call in outcome shadow: {forbidden}')

SRC.write_text(text, encoding='utf-8', newline='\n')
print('N2-13 NMJE closed-outcome shadow patch applied')
print('baseline_blob=', actual)
print('new_blob=', git_blob(SRC))
