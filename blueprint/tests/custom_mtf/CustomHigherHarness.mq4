#property strict
#define OnInit CanonicalOnInit
#define OnDeinit CanonicalOnDeinit
#define OnTick CanonicalOnTick
#define OnTimer CanonicalOnTimer
#include "..\\..\\source\\BBMA_EA.mq4"
#undef OnInit
#undef OnDeinit
#undef OnTick
#undef OnTimer
#ifdef CUSTOM_HIGHER_BASELINE
bool RefreshCustomCanonicalOwners(int pairIndex,int tf,datetime latest){return false;}
#endif
#include "CustomOwnerTestEquality.mqh"
int passed=0,failed=0;
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[CUSTOM-HIGHER] ",name," ",ok?"PASS":"FAIL");}
void ReadFixture(int index,int tf,TimeframeData &data,ReEntryData &re,ExtremeLifecycleData &extreme)
{
 if(tf==PERIOD_D1){data=g_pair_states[index].d1_data;re=g_pair_states[index].re_d1_buy_state;extreme=g_pair_states[index].extreme_d1_buy_lifecycle;}
 if(tf==PERIOD_H4){data=g_pair_states[index].h4_data;re=g_pair_states[index].re_h4_buy_state;extreme=g_pair_states[index].extreme_h4_buy_lifecycle;}
 if(tf==PERIOD_H1){data=g_pair_states[index].h1_data;re=g_pair_states[index].re_h1_buy_state;extreme=g_pair_states[index].extreme_h1_buy_lifecycle;}
 if(tf==PERIOD_M15){data=g_pair_states[index].m15_data;re=g_pair_states[index].re_m15_buy_state;extreme=g_pair_states[index].extreme_m15_buy_lifecycle;}
}
int OnInit()
{
 g_pair_count=3;for(int p=0;p<3;p++){InitPairState(g_pair_states[p]);g_pair_states[p].actual_symbol=Symbol();g_pair_states[p].pair_enabled=true;g_pair_canonical_scope[p]=false;}
 g_pair_states[1].actual_symbol="UNAVAILABLE_SYMBOL_FIXTURE";g_pair_canonical_scope[2]=true;
 g_processing_time=TimeCurrent();int frames[4]={PERIOD_D1,PERIOD_H4,PERIOD_H1,PERIOD_M15};
 for(int i=0;i<4;i++)
 {
  int tf=frames[i];datetime latest=GetLatestClosedCandleTime(Symbol(),tf);
  bool ok=RefreshCustomCanonicalOwners(0,tf,latest);
  TimeframeData data;ReEntryData re;ExtremeLifecycleData extreme;ReadFixture(0,tf,data,re,extreme);
  Check("custom_only_closed_source_"+IntegerToString(tf),ok && data.is_valid && data.is_closed && data.timeframe==tf && data.candle_time==latest && data.barIndex>=1);
  Check("existing_canonical_slots_updated_"+IntegerToString(tf),ok && re.Timeframe==tf && re.Direction==DIR_BUY && extreme.Timeframe==tf && extreme.Direction==DIR_BUY);
  CustomOwnerView view;ReadCustomOwnerView(0,tf,"RE",DIR_BUY,latest,view);
  Check("cold_snapshot_context_only_"+IntegerToString(tf),view.recoveryOnly && !view.entryWindowOpen && !view.entryEligible && !view.executionAvailable);
  ReEntryData beforeRE=re;ExtremeLifecycleData beforeEXT=extreme;
  bool duplicate=RefreshCustomCanonicalOwners(0,tf,latest);ReadFixture(0,tf,data,re,extreme);
  Check("duplicate_preserves_existing_owner_"+IntegerToString(tf),duplicate && SameReEntryData(beforeRE,re) && SameExtremeLifecycleData(beforeEXT,extreme));
 }
 datetime h1=GetLatestClosedCandleTime(Symbol(),PERIOD_H1);
 g_pair_states[2].re_h1_buy_state.EntryPrice=42;
 Check("canonical_scope_not_advanced_again",!RefreshCustomCanonicalOwners(2,PERIOD_H1,h1) && g_pair_states[2].re_h1_buy_state.EntryPrice==42 && g_pair_states[2].h1_data.candle_time==0);
 Check("missing_symbol_not_given_chart_state",!RefreshCustomCanonicalOwners(1,PERIOD_H1,h1) && g_pair_states[1].h1_data.candle_time==0 && g_pair_states[1].re_h1_buy_state.EntryPrice==0);
 Check("aux_TF_not_duplicated_here",!RefreshCustomCanonicalOwners(0,PERIOD_M1,h1));
 Check("invalid_pair_rejected",!RefreshCustomCanonicalOwners(3,PERIOD_H1,h1));
 Check("D1_major_owner_uses_existing_M11",g_pair_states[0].d1_major_trend_owner.LastProcessedD1CandleTime==GetLatestClosedCandleTime(Symbol(),PERIOD_D1));
 Check("unrecovered_H4_not_invented",!g_pair_states[0].h4_direction_owner.RecoveryComplete);
#ifndef CUSTOM_HIGHER_BASELINE
 // Trusted-recovery fixture verifies delegation, not cold-start certification.
 ZeroMemory(g_pair_states[0].custom_canonical[1]);
 g_pair_states[0].h4_direction_owner.RecoveryComplete=true;
 g_pair_states[0].h4_direction_owner.LastProcessedH4CandleTime=0;
 datetime h4=GetLatestClosedCandleTime(Symbol(),PERIOD_H4);
 bool delegated=RefreshCustomCanonicalOwners(0,PERIOD_H4,h4);
 Check("recovered_H4_delegates_existing_owner",delegated && g_pair_states[0].h4_direction_owner.RecoveryComplete && g_pair_states[0].h4_direction_owner.LastProcessedH4CandleTime==h4);
#endif
 Print("[CUSTOM-HIGHER-SUMMARY] passed=",passed," failed=",failed);return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
