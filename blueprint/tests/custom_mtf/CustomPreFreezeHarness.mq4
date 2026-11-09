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
#include "CustomOwnerTestEquality.mqh"
int passed=0,failed=0;
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[CUSTOM-PREFREEZE] ",name," ",ok?"PASS":"FAIL");}
void Seed(int tf,ENUM_DIRECTION side,TimeframeData &data,CustomAuxLifecycle &owner)
{
 ZeroMemory(owner);int seconds=GetTimeframeSeconds(tf);datetime latest=data.candle_time;
 data.open=1.5;data.close=side==DIR_BUY?1.4:1.6;data.high=1.7;data.low=1.3;
 data.bollinger[0]=2;data.bollinger[1]=1.5;data.bollinger[2]=1;
 owner.extremeBuy.Maturity=EXT_MAT_REVERSAL_CONFIRMED;owner.extremeBuy.Direction=DIR_BUY;owner.extremeBuy.Timeframe=tf;owner.extremeBuy.IsValid=true;
 owner.extremeBuy.RawCandleTime=latest-4*seconds;owner.extremeBuy.ConfirmationCandleTime=latest-3*seconds;owner.extremeBuy.LastUpdateCandleTime=latest;
 owner.extremeSell=owner.extremeBuy;owner.extremeSell.Direction=DIR_SELL;
 owner.mhvBuy.State=MLV_DIRECTION_TAKEN;owner.mhvBuy.Direction=DIR_BUY;owner.mhvBuy.ParentExtremeDirection=DIR_SELL;owner.mhvBuy.Timeframe=tf;owner.mhvBuy.IsValid=true;
 owner.mhvBuy.ParentRawCandleTime=owner.extremeSell.RawCandleTime;owner.mhvBuy.ParentConfirmationCandleTime=owner.extremeSell.ConfirmationCandleTime;
 owner.mhvBuy.StartCandleTime=latest-2*seconds;owner.mhvBuy.ConfirmationCandleTime=latest-2*seconds;owner.mhvBuy.LastUpdateCandleTime=latest-seconds;
 owner.mhvBuy.FrozenMarkedBody=1.2;owner.mhvBuy.PreviousClose=data.close;
 owner.mhvSell=owner.mhvBuy;owner.mhvSell.Direction=DIR_SELL;owner.mhvSell.ParentExtremeDirection=DIR_BUY;
 if(side==DIR_BUY){owner.mhvBuy.SupersessionCandidateActive=true;owner.mhvBuy.SupersessionRawCandleTime=latest-seconds;}
 else{owner.mhvSell.SupersessionCandidateActive=true;owner.mhvSell.SupersessionRawCandleTime=latest-seconds;}
 owner.reBuy.EntryPrice=77;owner.reSell.EntryPrice=88;
 // Isolate handover from unrelated historical momentum in these synthetic
 // price trajectories, using the existing testable M10 snapshot channel.
 M10MomentumSnapshot momentum;ReadM10MomentumSnapshot(Symbol(),tf,1,momentum);
 int momentumSlot=CustomTFIndex(tf);
 g_pair_states[0].m10_momentum[momentumSlot].buy=false;
 g_pair_states[0].m10_momentum[momentumSlot].sell=false;
 StoreCustomCanonicalSource(0,tf,data,owner);g_pair_states[0].canonical_mhv_observed[CustomCanonicalTFIndex(tf)]=false;
 g_pair_states[0].tf_snapshot.M15_CandleTime=GetLatestClosedCandleTime(Symbol(),PERIOD_M15);
 g_pair_states[0].is_processing=true;g_processed_candle_time[0]=0;
}
int OnInit()
{
 g_pair_count=2;for(int p=0;p<2;p++){InitPairState(g_pair_states[p]);g_pair_states[p].actual_symbol=Symbol();g_pair_canonical_scope[p]=true;}
 g_processing_time=TimeCurrent();int frames[3]={PERIOD_D1,PERIOD_H4,PERIOD_H1};
 for(int slot=0;slot<3;slot++)for(int d=0;d<2;d++)
 {
  int tf=frames[slot],seconds=GetTimeframeSeconds(tf);ENUM_DIRECTION side=d==0?DIR_BUY:DIR_SELL;
  datetime latest=GetLatestClosedCandleTime(Symbol(),tf);TimeframeData data;ReadCustomAuxClosedData(Symbol(),tf,latest,data);
  CustomAuxLifecycle before,expected,after,other,otherAfter;Seed(tf,side,data,before);expected=before;
  TimeframeData otherData;LoadCustomCanonicalSource(1,tf,otherData,other);
  BollingerBand band;ZeroMemory(band);band.TOP_BB=2;band.MID_BB=1.5;band.LOW_BB=1;band.Width=1;
  AdvanceMHVSourceOwners(Symbol(),data,band,expected.extremeBuy,expected.extremeSell,expected.mhvBuy,expected.mhvSell,false);
  string tag=IntegerToString(tf)+"_"+IntegerToString(d);
  bool installation=!SameExtremeLifecycleData(before.extremeBuy,expected.extremeBuy) || !SameExtremeLifecycleData(before.extremeSell,expected.extremeSell);
  Check("fixture_parent_install_"+tag,installation);
  g_pair_states[0].is_processing=false;bool rejected=!AdvanceCanonicalMHVBeforeFreeze(0,tf,latest);LoadCustomCanonicalSource(0,tf,data,after);
  Check("inactive_phase_rejected_"+tag,rejected && SameOwners(before,after));g_pair_states[0].is_processing=true;
  bool updated=AdvanceCanonicalMHVBeforeFreeze(0,tf,latest);LoadCustomCanonicalSource(0,tf,data,after);expected.lastClosed=latest;
  Check("before_completed_cycle_stamp_"+tag,updated && g_processed_candle_time[0]==0);
  Check("atomic_shared_engine_result_"+tag,SameOwners(expected,after) && !after.recoveryRequired && after.contextOnlyThrough==latest);
  LoadCustomCanonicalSource(1,tf,otherData,otherAfter);Check("symbol_isolation_"+tag,SameOwners(other,otherAfter));
  before=after;AdvanceCanonicalMHVBeforeFreeze(0,tf,latest);LoadCustomCanonicalSource(0,tf,data,after);Check("duplicate_unchanged_"+tag,SameOwners(before,after));
  g_pair_states[0].is_processing=false;g_processed_candle_time[0]=GetLatestClosedCandleTime(Symbol(),PERIOD_M15);
  bool observed=ObserveCanonicalMHVSource(0,tf,latest);LoadCustomCanonicalSource(0,tf,data,after);Check("post_cycle_reuses_transaction_"+tag,observed && SameOwners(before,after));
  Seed(tf,side,data,before);ZeroMemory(g_custom_use);AdvanceCanonicalMHVBeforeFreeze(0,tf,latest);LoadCustomCanonicalSource(0,tf,data,after);
  bool noRequests=SameOwners(expected,after);Seed(tf,side,data,before);for(int i=0;i<77;i++)g_custom_use.signalEnabled[i]=true;
  AdvanceCanonicalMHVBeforeFreeze(0,tf,latest);LoadCustomCanonicalSource(0,tf,data,after);Check("request_independent_helper_"+tag,noRequests && SameOwners(expected,after));
  Seed(tf,side,data,before);before.lastClosed=latest-3*seconds;before.mhvBuy.LastUpdateCandleTime=before.lastClosed;before.mhvSell.LastUpdateCandleTime=before.lastClosed;StoreCustomCanonicalSource(0,tf,data,before);
  bool held=AdvanceCanonicalMHVBeforeFreeze(0,tf,latest);LoadCustomCanonicalSource(0,tf,data,after);Check("gap_remains_HOLD_"+tag,held && after.recoveryRequired && SameOwners(before,after));
  Seed(tf,side,data,before);before.mhvBuy.LastUpdateCandleTime=latest+seconds;StoreCustomCanonicalSource(0,tf,data,before);
  held=AdvanceCanonicalMHVBeforeFreeze(0,tf,latest);LoadCustomCanonicalSource(0,tf,data,after);Check("future_anchor_HOLD_"+tag,held && after.recoveryRequired && SameOwners(before,after));
 }
 Check("no_orders",OrdersTotal()==0 && OrdersHistoryTotal()==0);
 Print("[CUSTOM-PREFREEZE-SUMMARY] passed=",passed," failed=",failed);return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
