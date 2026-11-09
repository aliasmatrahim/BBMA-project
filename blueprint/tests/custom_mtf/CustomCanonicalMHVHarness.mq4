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
#ifdef CUSTOM_CANONICAL_MHV_BASELINE
bool ObserveCanonicalMHVSource(int pairIndex,int tf,datetime latest){return false;}
#endif
#include "CustomOwnerTestEquality.mqh"
int passed=0,failed=0;
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[CUSTOM-CANONMHV] ",name," ",ok?"PASS":"FAIL");}
bool LegacySame(CustomAuxLifecycle &a,CustomAuxLifecycle &b)
{
 return SameExtremeLifecycleData(a.extremeBuy,b.extremeBuy) && SameExtremeLifecycleData(a.extremeSell,b.extremeSell) && SameReEntryData(a.reBuy,b.reBuy) && SameReEntryData(a.reSell,b.reSell);
}
void SeedFixture(int tf,TimeframeData &data,CustomAuxLifecycle &owner)
{
 ZeroMemory(owner);int seconds=GetTimeframeSeconds(tf);datetime latest=data.candle_time;
 owner.extremeBuy.Maturity=EXT_MAT_REVERSAL_CONFIRMED;owner.extremeBuy.Direction=DIR_BUY;owner.extremeBuy.Timeframe=tf;owner.extremeBuy.IsValid=true;
 owner.extremeBuy.RawCandleTime=latest-4*seconds;owner.extremeBuy.ConfirmationCandleTime=latest-3*seconds;owner.extremeBuy.LastUpdateCandleTime=latest;
 owner.extremeSell=owner.extremeBuy;owner.extremeSell.Direction=DIR_SELL;
 owner.mhvBuy.State=MLV_DIRECTION_TAKEN;owner.mhvBuy.Direction=DIR_BUY;owner.mhvBuy.ParentExtremeDirection=DIR_SELL;owner.mhvBuy.Timeframe=tf;owner.mhvBuy.IsValid=true;
 owner.mhvBuy.ParentRawCandleTime=owner.extremeSell.RawCandleTime;owner.mhvBuy.ParentConfirmationCandleTime=owner.extremeSell.ConfirmationCandleTime;
 owner.mhvBuy.StartCandleTime=latest-2*seconds;owner.mhvBuy.ConfirmationCandleTime=latest-2*seconds;owner.mhvBuy.LastUpdateCandleTime=latest-seconds;
 owner.mhvBuy.FrozenMarkedBody=1.2;owner.mhvBuy.PreviousClose=data.close;
 owner.mhvSell=owner.mhvBuy;owner.mhvSell.Direction=DIR_SELL;owner.mhvSell.ParentExtremeDirection=DIR_BUY;
 owner.reBuy.EntryPrice=77;owner.reSell.EntryPrice=88;
 StoreCustomCanonicalSource(0,tf,data,owner);
#ifndef CUSTOM_CANONICAL_MHV_BASELINE
 g_pair_states[0].canonical_mhv_observed[CustomCanonicalTFIndex(tf)]=false;
#endif
}
int OnInit()
{
 g_pair_count=2;for(int p=0;p<2;p++){InitPairState(g_pair_states[p]);g_pair_states[p].actual_symbol=Symbol();g_pair_canonical_scope[p]=p==0;}
 g_processing_time=TimeCurrent();datetime canonicalStamp=GetLatestClosedCandleTime(Symbol(),PERIOD_M15);g_processed_candle_time[0]=canonicalStamp; // Trusted completed-canonical-cycle fixture.
 int frames[3]={PERIOD_D1,PERIOD_H4,PERIOD_H1};
 for(int slot=0;slot<3;slot++)
 {
  int tf=frames[slot],seconds=GetTimeframeSeconds(tf);datetime latest=GetLatestClosedCandleTime(Symbol(),tf);TimeframeData data;ReadCustomAuxClosedData(Symbol(),tf,latest,data);
  CustomAuxLifecycle before,after;SeedFixture(tf,data,before);bool handled=ObserveCanonicalMHVSource(0,tf,latest);
  CustomOwnerView a,b;bool mhv=ReadCustomOwnerView(0,tf,"MHV",DIR_BUY,latest,a);bool mlv=ReadCustomOwnerView(0,tf,"MLV",DIR_BUY,latest,b);
  Check("canonical_source_readable_"+IntegerToString(tf),handled && mhv && a.readable && a.structuralValid && a.sourceBar==latest);
  Check("one_MHV_MLV_identity_"+IntegerToString(tf),mlv && b.eventId==a.eventId && StringLen(a.eventId)>0);
  LoadCustomCanonicalSource(0,tf,data,after);Check("no_legacy_owner_mutation_"+IntegerToString(tf),LegacySame(before,after));
  Check("cold_context_no_entry_"+IntegerToString(tf),a.recoveryOnly && !a.entryWindowOpen && !a.entryEligible && !a.executionAvailable);
  before=after;ObserveCanonicalMHVSource(0,tf,latest);LoadCustomCanonicalSource(0,tf,data,after);
  Check("duplicate_all_owner_fields_"+IntegerToString(tf),SameOwners(before,after));
  TimeframeData stale=data;stale.candle_time=latest-seconds;StoreCustomCanonicalSource(0,tf,stale,after);
  bool waited=!ObserveCanonicalMHVSource(0,tf,latest) && !ReadCustomOwnerView(0,tf,"MHV",DIR_BUY,latest,a);
  StoreCustomCanonicalSource(0,tf,data,after);Check("wait_for_current_canonical_data_"+IntegerToString(tf),waited);
  g_processed_candle_time[0]=0;
  Check("wait_for_completed_canonical_cycle_"+IntegerToString(tf),!ObserveCanonicalMHVSource(0,tf,latest) && !ReadCustomOwnerView(0,tf,"MHV",DIR_BUY,latest,a));
  g_processed_candle_time[0]=canonicalStamp;
  Check("no_controller_or_legacy_execution_"+IntegerToString(tf),g_processed_candle_time[0]==canonicalStamp && !g_pair_states[0].last_decision.Valid);
  SeedFixture(tf,data,before);before.lastClosed=latest-3*seconds;before.mhvBuy.LastUpdateCandleTime=before.lastClosed;before.mhvSell.LastUpdateCandleTime=before.lastClosed;StoreCustomCanonicalSource(0,tf,data,before);
  bool gap=ObserveCanonicalMHVSource(0,tf,latest);LoadCustomCanonicalSource(0,tf,data,after);
  Check("canonical_gap_holds_without_replay_"+IntegerToString(tf),gap && after.recoveryRequired && after.recoveryReason=="WAIT_CANONICAL_M09_RECOVERY" && SameOwners(before,after));
  SeedFixture(tf,data,before);before.mhvBuy.LastUpdateCandleTime=latest+seconds;StoreCustomCanonicalSource(0,tf,data,before);
  bool future=ObserveCanonicalMHVSource(0,tf,latest);LoadCustomCanonicalSource(0,tf,data,after);
  Check("future_M09_watermark_holds_"+IntegerToString(tf),future && after.recoveryRequired && after.recoveryReason=="WAIT_CANONICAL_M09_OWNER_ANCHOR" && SameOwners(before,after));
  // Force a real M09 parent-install request on trusted synthetic source snapshots.
  data.open=1.5;data.close=1.4;data.high=1.7;data.low=1.3;data.bollinger[0]=2;data.bollinger[1]=1.5;data.bollinger[2]=1;
  ENUM_DIRECTION side=DetectCSM(Symbol(),tf,DIR_SELL,1)?DIR_SELL:DIR_BUY;
  if(side==DIR_SELL)data.close=1.6;
  SeedFixture(tf,data,before);MLVData pending=side==DIR_BUY?before.mhvBuy:before.mhvSell;
  pending.SupersessionCandidateActive=true;pending.SupersessionRawCandleTime=latest-seconds;
  if(side==DIR_BUY)before.mhvBuy=pending;else before.mhvSell=pending;
  StoreCustomCanonicalSource(0,tf,data,before);
  ExtremeLifecycleData parent=side==DIR_BUY?before.extremeSell:before.extremeBuy;ExtremeLifecycleData originalParent=parent;
  BollingerBand band;ZeroMemory(band);band.TOP_BB=2;band.MID_BB=1.5;band.LOW_BB=1;band.Width=1;
  UpdateCanonicalMLVState(pending,Symbol(),side,data,band,parent,false);
  Check("fixture_requests_parent_install_"+IntegerToString(tf),!SameExtremeLifecycleData(parent,originalParent));
  bool held=ObserveCanonicalMHVSource(0,tf,latest);LoadCustomCanonicalSource(0,tf,data,after);
  Check("parent_handover_becomes_HOLD_"+IntegerToString(tf),held && after.recoveryRequired && after.recoveryReason=="WAIT_CANONICAL_M09_PARENT_HANDOVER");
  Check("no_partial_M09_or_parent_commit_"+IntegerToString(tf),SameMLVData(before.mhvBuy,after.mhvBuy) && SameMLVData(before.mhvSell,after.mhvSell) && LegacySame(before,after));
  Check("held_owner_unavailable_"+IntegerToString(tf),!ReadCustomOwnerView(0,tf,"MHV",side,latest,a));
 }
 Check("custom_only_not_advanced_twice",!ObserveCanonicalMHVSource(1,PERIOD_H1,iTime(Symbol(),PERIOD_H1,1)));
 Check("M15_existing_producer_preserved",!ObserveCanonicalMHVSource(0,PERIOD_M15,iTime(Symbol(),PERIOD_M15,1)));
 Check("aux_existing_producer_preserved",!ObserveCanonicalMHVSource(0,PERIOD_M1,iTime(Symbol(),PERIOD_M1,1)));
 Check("invalid_index_rejected",!ObserveCanonicalMHVSource(2,PERIOD_H1,iTime(Symbol(),PERIOD_H1,1)));
 Check("no_orders",OrdersTotal()==0 && OrdersHistoryTotal()==0);
 Print("[CUSTOM-CANONMHV-SUMMARY] passed=",passed," failed=",failed);return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
