from pathlib import Path
import sys

BASE = Path(r"D:\BBMA\Workspace\m19-selection-failclosed-101\blueprint\source\BBMA_EA.mq4")
CAND = Path(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\MQL4\Experts\BBMA_EA_M19_504_GBPUSD_HARNESS.mq4")
base = BASE.read_text(encoding="utf-8")
if not CAND.exists():
    print("RED: harness candidate missing")
    raise SystemExit(1)
cand = CAND.read_text(encoding="utf-8")

symbol_old = '   if(requested == "") return "";\n\n   // 1) Exact broker symbol wins'
symbol_new = '   if(requested == "") return "";\n\n   // #214 TESTER ADAPTER: current test symbol fallback only.\n   if(IsTesting())\n   {\n      string testerSymbol = Symbol();\n      if(testerSymbol == requested || RemoveSuffix(testerSymbol) == RemoveSuffix(requested))\n         return testerSymbol;\n   }\n\n   // 1) Exact broker symbol wins'
conn_old = 'bool IsTerminalConnected()\n{\n   return IsConnected();\n}'
conn_new = 'bool IsTerminalConnected()\n{\n   if(IsTesting()) return true;\n   return IsConnected();\n}'
timer_old = '''   ResetLastError();
   if(!EventSetTimer(1))
   {
      int timerError = GetLastError();
      g_is_initialized = false;
      Log(DBG_ERROR, "Failed to register EA timer, error=" + IntegerToString(timerError));
      return INIT_FAILED;
   }'''
timer_new = '''   // #214 TESTER ADAPTER: MT4 tester rejects EventSetTimer; OnTick remains processing driver.
   if(!IsTesting())
   {
      ResetLastError();
      if(!EventSetTimer(1))
      {
         int timerError = GetLastError();
         g_is_initialized = false;
         Log(DBG_ERROR, "Failed to register EA timer, error=" + IntegerToString(timerError));
         return INIT_FAILED;
      }
   }'''
expected = base.replace(symbol_old, symbol_new, 1).replace(conn_old, conn_new, 1).replace(timer_old, timer_new, 1)
checks = [
    ('base replacements exact', expected != base),
    ('candidate equals exact adapter transform', cand == expected),
    ('build identity preserved', '#property version   "5.04"' in cand and 'V504_M19_SELECTION_FAIL_CLOSED_20260921' in cand),
    ('source revision preserved', 'M19_SELECTION_FAIL_CLOSED_101_20260921' in cand),
]
failed = [name for name, ok in checks if not ok]
for name, ok in checks:
    print(('PASS: ' if ok else 'FAIL: ') + name)
if failed:
    raise SystemExit(1)
print('D1O503_TESTER_ADAPTER_INVARIANT=PASS')
