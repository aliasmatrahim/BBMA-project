from pathlib import Path
BASE=Path(r"D:\BBMA\Workspace\m19-selection-failclosed-101\blueprint\source\BBMA_EA.mq4")
OUT=Path(r"D:\BBMA\MT4_TesterRunner_OfflineDiag\MQL4\Experts\BBMA_EA_M19_504_GBPUSD_HARNESS.mq4")
s=BASE.read_text(encoding="utf-8")
a='   if(requested == "") return "";\n\n   // 1) Exact broker symbol wins'
b='   if(requested == "") return "";\n\n   // #214 TESTER ADAPTER: current test symbol fallback only.\n   if(IsTesting())\n   {\n      string testerSymbol = Symbol();\n      if(testerSymbol == requested || RemoveSuffix(testerSymbol) == RemoveSuffix(requested))\n         return testerSymbol;\n   }\n\n   // 1) Exact broker symbol wins'
assert s.count(a)==1
s=s.replace(a,b,1)
a='bool IsTerminalConnected()\n{\n   return IsConnected();\n}'
b='bool IsTerminalConnected()\n{\n   if(IsTesting()) return true;\n   return IsConnected();\n}'
assert s.count(a)==1
s=s.replace(a,b,1)
a='''   ResetLastError();
   if(!EventSetTimer(1))
   {
      int timerError = GetLastError();
      g_is_initialized = false;
      Log(DBG_ERROR, "Failed to register EA timer, error=" + IntegerToString(timerError));
      return INIT_FAILED;
   }'''
b='''   // #214 TESTER ADAPTER: MT4 tester rejects EventSetTimer; OnTick remains processing driver.
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
assert s.count(a)==1
s=s.replace(a,b,1)
OUT.write_text(s,encoding='utf-8',newline='\n')
print(OUT)
