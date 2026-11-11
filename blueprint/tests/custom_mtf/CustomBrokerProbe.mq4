#property strict
// Test-only probe of actual offline tester APIs; canonical resolver extracted by runner.
#include "CanonicalNativeResolver.mqh"
int OnInit()
{
 int all=SymbolsTotal(false),selected=SymbolsTotal(true);
 ResetLastError();bool selectable=SymbolSelect(Symbol(),true);int error=GetLastError();
 string actual=FindActualSymbol(Symbol());
 Print("[BROKER-PROBE] symbol=",Symbol()," all=",all," selected=",selected," selectable=",selectable," error=",error," actual=",actual," point=",MarketInfo(Symbol(),MODE_POINT));
 return INIT_SUCCEEDED;
}
void OnTick(){}
