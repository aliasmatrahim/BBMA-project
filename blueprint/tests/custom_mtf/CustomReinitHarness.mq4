#property strict
// Broker catalog fixture; canonical resolver body is extracted by runner.
string catalog[];
int FixtureSymbolsTotal(bool selected){return ArraySize(catalog);}
string FixtureSymbolName(int i,bool selected){return catalog[i];}
bool FixtureSymbolSelect(string name,bool selected){return true;}
#include "CanonicalResolverFixture.mqh"
#include "..\\..\\source\\custom_mtf\\CustomInputs.mqh"
input bool ExpectedValid=true;
int OnInit()
{
 StringSplit(Symbol()+",XAUUSD,EURUSD",44,catalog);
 string firstReason,secondReason;
 bool first=InitializeCustomInputs(firstReason);string firstPayload=g_custom_config_payload;
 g_custom_config_payload="STALE";g_custom_config_hash="STALE";g_custom_use.available[0]=true;
 g_custom_slots[4].context.atomCount=7;
 bool second=InitializeCustomInputs(secondReason);
 bool clean=g_custom_config_hash=="" && !g_custom_use.available[0] && g_custom_slots[4].context.atomCount==0;
 bool validPayload=(second ? g_custom_config_payload!="" && g_custom_config_payload==firstPayload : g_custom_config_payload=="");
 bool ok=first==ExpectedValid && second==ExpectedValid && firstReason==secondReason && clean && validPayload;
 Print("[CUSTOM-REINIT] expected=",ExpectedValid," first=",first," second=",second," reason=",secondReason," clean=",clean," passed=",ok);
 return ok?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
