#property strict
// Broker I/O fixtures only. Resolver functions are extracted from current EA by runner.
string catalog[];
int FixtureSymbolsTotal(bool selected){return ArraySize(catalog);}
string FixtureSymbolName(int i,bool selected){return catalog[i];}
bool FixtureSymbolSelect(string name,bool selected){return name!="BLOCKED";}
#include "CanonicalResolverFixture.mqh"
#ifndef CUSTOM_SYMBOL_BASELINE
#include "..\\..\\source\\custom_mtf\\CustomSymbols.mqh"
#else
bool BuildCustomUniverse(int mode,string list,string chart,string &watch[],string &out[],string &reason){ArrayResize(out,0);reason="MISSING_CAPABILITY";return false;}
bool ResolveCustomSubset(string text,string &universe[],string &out[],string &reason){ArrayResize(out,0);reason="MISSING_CAPABILITY";return false;}
#endif
int passed=0,failed=0;
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[CUSTOM-SYMBOL] ",name," ",ok?"PASS":"FAIL");}
int OnInit()
{
 StringSplit("XAUUSD.a,GBPUSD.a,EURUSD.a,USDJPY.a,USDJPY.b,BLOCKED",44,catalog);
 string watch[],u[],sub[],reason;StringSplit("XAUUSD.a,GBPUSD.a",44,watch);
 bool ok=BuildCustomUniverse(0,"","XAUUSD.a",watch,u,reason);
 Check("chart_only",ok && ArraySize(u)==1 && u[0]=="XAUUSD.a");
 ok=BuildCustomUniverse(2,"XAUUSD,GBPUSD.a,XAUUSD.a","",watch,u,reason);
 Check("unique_suffix_and_alias_collapse",ok && ArraySize(u)==2 && u[0]=="XAUUSD.a" && u[1]=="GBPUSD.a");
 bool allResult=ResolveCustomSubset(" all ",u,sub,reason);
 Check("all_is_primary_universe",allResult && ArraySize(sub)==2 && sub[0]=="XAUUSD.a" && sub[1]=="GBPUSD.a");
 Check("subset_alias",ResolveCustomSubset("GBPUSD",u,sub,reason) && ArraySize(sub)==1 && sub[0]=="GBPUSD.a");
 Check("outside_universe_rejected",!ResolveCustomSubset("EURUSD",u,sub,reason) && ArraySize(sub)==0);
 Check("typo_rejected",!BuildCustomUniverse(2,"GOLDTYPO","",watch,u,reason) && ArraySize(u)==0);
 Check("ambiguous_suffix_rejected",!BuildCustomUniverse(2,"USDJPY","",watch,u,reason));
 Check("explicit_variant",BuildCustomUniverse(2,"USDJPY.b","",watch,u,reason) && ArraySize(u)==1 && u[0]=="USDJPY.b");
 Check("unselectable_rejected",!BuildCustomUniverse(2,"BLOCKED","",watch,u,reason));
 Check("empty_token_rejected",!BuildCustomUniverse(2,"XAUUSD,","",watch,u,reason));
 Check("empty_list_rejected",!BuildCustomUniverse(2,"","",watch,u,reason));
 Check("unknown_mode_rejected",!BuildCustomUniverse(3,"XAUUSD","",watch,u,reason));
 ok=BuildCustomUniverse(1,"","",watch,u,reason);watch[0]="EURUSD.a";
 Check("market_watch_frozen_copy",ok && ArraySize(u)==2 && u[0]=="XAUUSD.a");
 Print("[CUSTOM-SYMBOL-SUMMARY] passed=",passed," failed=",failed);
 return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
