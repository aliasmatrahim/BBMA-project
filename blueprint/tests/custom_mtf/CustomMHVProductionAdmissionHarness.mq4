#property strict
// SIG06 diagnostic: actual production recovery admission, no calendar override.
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
struct OriginOwners {ExtremeLifecycleData buy;ExtremeLifecycleData sell;MLVData mhvBuy;MLVData mhvSell;};
#include "CustomMHVOriginCodec.mqh"
int passed=0,failed=0,cases=0;
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[MHV-ADMISSION] ",name," ",ok?"PASS":"FAIL");}
bool SameData(TimeframeData &a,TimeframeData &b)
{
 for(int k=0;k<10;k++)if(a.ma[k]!=b.ma[k])return false;
 for(int k=0;k<3;k++)if(a.bollinger[k]!=b.bollinger[k])return false;
 return a.trend==b.trend && a.open==b.open && a.close==b.close && a.high==b.high && a.low==b.low &&
 a.point==b.point && a.digits==b.digits && a.barIndex==b.barIndex && a.data_count==b.data_count &&
 a.candle_time==b.candle_time && a.is_valid==b.is_valid && a.is_closed==b.is_closed && a.timeframe==b.timeframe;
}
bool SameMetadata(CustomAuxLifecycle &a,CustomAuxLifecycle &b)
{
 return a.recoveryRequired==b.recoveryRequired && a.contextOnlyThrough==b.contextOnlyThrough && a.lastReplayBars==b.lastReplayBars;
}
bool SameSourceOwners(CustomAuxLifecycle &a,OriginOwners &b)
{
 return SameExtremeLifecycleData(a.extremeBuy,b.buy) && SameExtremeLifecycleData(a.extremeSell,b.sell) &&
 SameMLVData(a.mhvBuy,b.mhvBuy) && SameMLVData(a.mhvSell,b.mhvSell);
}
bool LoadSnapshots(int tf,OriginOwners &states[],datetime &times[])
{
 string file="sig06_mhv_origin_checkpoint_ny_calendar_v7_"+IntegerToString(tf)+".csv";
 int h=FileOpen(file,FILE_READ|FILE_CSV|FILE_ANSI,';');if(h==INVALID_HANDLE)return false;
 string value;bool ok=OriginReadKey(h,"source",value) && value=="a62672ae1874fcbf61c671af01da09ef45ffe6972abd998ec70c5f9a74c238cb";
 ok=ok && OriginReadKey(h,"tf",value) && StringToInteger(value)==tf;
 ok=ok && OriginReadKey(h,"anchor",value);datetime anchor=(datetime)StringToInteger(value);
 int shift=iBarShift(Symbol(),tf,anchor,true);ok=ok && shift>24;
 for(int k=0;k<25 && ok;k++)
 {ok=ReadOriginSnapshot(h,k==0?"anchor":"step"+IntegerToString(k),states[k]);times[k]=iTime(Symbol(),tf,shift-k);}
 bool end=FileIsEnding(h);FileClose(h);return ok && end;
}
void MakeOwner(OriginOwners &source,datetime stamp,int tf,CustomAuxLifecycle &owner)
{
 ZeroMemory(owner);owner.extremeBuy=source.buy;owner.extremeSell=source.sell;owner.mhvBuy=source.mhvBuy;owner.mhvSell=source.mhvSell;
 owner.reBuy.Direction=DIR_BUY;owner.reSell.Direction=DIR_SELL;owner.reBuy.Timeframe=tf;owner.reSell.Timeframe=tf;
 owner.lastClosed=stamp;owner.contextOnlyThrough=stamp;owner.recoveryRequired=true;
}
void TestBoundary(int tf,OriginOwners &states[],datetime &times[],int gapIndex,int prefix,bool initiallyHeld)
{
 int start=gapIndex-1-prefix;string key=IntegerToString(tf)+"_"+IntegerToString((int)times[gapIndex])+"_prefix"+IntegerToString(prefix)+"_held"+IntegerToString((int)initiallyHeld);
 Check(key+"_snapshot_start_available",start>=0);if(start<0)return;
 cases++;g_processing_time=times[gapIndex]+tf*60;
 CustomAuxLifecycle owner;MakeOwner(states[start],times[start],tf,owner);owner.recoveryRequired=initiallyHeld;
 TimeframeData data;bool inputReady=ReadCustomAuxClosedData(Symbol(),tf,times[start],data);Check(key+"_actual_closed_input",inputReady);if(!inputReady)return;
 CustomAuxLifecycle before=owner,control=owner;TimeframeData beforeData=data;bool prefixOk=true;
 for(int step=start+1;step<gapIndex;step++)
 {
  TimeframeData next;if(!ReadCustomAuxClosedData(Symbol(),tf,times[step],next) || !AdvanceCustomAuxLifecycle(Symbol(),next,control)){prefixOk=false;break;}
 }
 Check(key+"_control_prefix_advances",prefixOk && control.lastClosed==times[gapIndex-1]);
 Check(key+"_prefix_source_matches_frozen_snapshot",prefixOk && SameSourceOwners(control,states[gapIndex-1]));
 bool admitted=ReplayCustomAuxOwnerSource(Symbol(),tf,times[gapIndex],data,owner);
 Check(key+"_production_rejects_non_nominal_gap",!admitted && owner.recoveryReason=="WAIT_REPLAY_HISTORY_CONTINUITY");
 Check(key+"_all_structural_fields_rollback",SameOwners(before,owner));
 Check(key+"_all_data_fields_rollback",SameData(beforeData,data));
 Check(key+"_recovery_metadata_preserved",SameMetadata(before,owner));
 CustomAuxLifecycle first=owner;TimeframeData firstData=data;
 bool retried=ReplayCustomAuxOwnerSource(Symbol(),tf,times[gapIndex],data,owner);
 Check(key+"_retry_idempotent",!retried && SameOwners(first,owner) && SameMetadata(first,owner) && SameData(firstData,data) && owner.recoveryReason==first.recoveryReason);
 InitPairState(g_pair_states[0]);g_pair_states[0].actual_symbol=Symbol();g_pair_canonical_scope[0]=false;
 StoreCustomCanonicalSource(0,tf,beforeData,before);
 g_processing_time=TimeCurrent();datetime routerTarget=GetLatestClosedCandleTime(Symbol(),tf);
 Check(key+"_actual_latest_router_target",routerTarget>=times[gapIndex] && routerTarget>before.lastClosed);
 bool ready=RefreshCustomRequestedOwners(0,tf,routerTarget);
 TimeframeData storedData;CustomAuxLifecycle stored;LoadCustomCanonicalSource(0,tf,storedData,stored);
 Check(key+"_actual_router_holds",!ready && stored.recoveryRequired && stored.recoveryReason=="WAIT_REPLAY_HISTORY_CONTINUITY");
 Check(key+"_actual_canonical_store_preserved",SameOwners(before,stored) && SameData(beforeData,storedData));
 for(int side=0;side<2;side++)
 {
  CustomOwnerView view;ENUM_DIRECTION direction=side==0?DIR_BUY:DIR_SELL;
  bool readable=ReadCustomOwnerView(0,tf,"MHV",direction,routerTarget,view);
  Check(key+"_MHV_view_unavailable_"+IntegerToString(side),!readable && view.reason=="WAIT_OWNER_RECOVERY" &&
    !view.readable && !view.entryEligible && !view.entryWindowOpen && !view.executionAvailable && StringLen(view.eventId)==0);
 }
 Print("[MHV-ADMISSION-CASE] tf=",tf," start=",(int)times[start]," previous=",(int)times[gapIndex-1],
 " target=",(int)times[gapIndex]," routerTarget=",(int)routerTarget," prefix=",prefix," initiallyHeld=",initiallyHeld," routerReason=",stored.recoveryReason," reason=",owner.recoveryReason);
}
int OnInit()
{
 g_pair_count=1;
 for(int t=0;t<2;t++)
 {
  int tf=t==0?PERIOD_H4:PERIOD_D1;OriginOwners states[25];datetime times[25];
  bool loaded=LoadSnapshots(tf,states,times);Check("load_exact_frozen_snapshot_"+IntegerToString(tf),loaded);if(!loaded)continue;
  for(int step=1;step<25;step++)if(times[step]!=times[step-1]+tf*60)
  {for(int hold=0;hold<2;hold++){TestBoundary(tf,states,times,step,0,hold==1);TestBoundary(tf,states,times,step,2,hold==1);}}
 }
 Check("six_boundaries_two_prefix_two_HOLD_states",cases==24);
 Check("no_orders",OrdersTotal()==0 && OrdersHistoryTotal()==0);
 Print("[MHV-ADMISSION-SUMMARY] cases=",cases," passed=",passed," failed=",failed," scope=PRODUCTION_FAIL_FROZEN_NOT_RECOVERY_ACCEPTANCE");
 return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
void OnTimer(){}
void OnDeinit(const int reason){}
