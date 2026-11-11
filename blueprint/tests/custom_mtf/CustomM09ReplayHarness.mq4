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
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[CUSTOM-M09REPLAY] ",name," ",ok?"PASS":"FAIL");}
void Stage(int index,int tf,TimeframeData &data,CustomAuxLifecycle &owner,bool write)
{
 if(CustomCanonicalTFIndex(tf)>=0){if(write)StoreCustomCanonicalSource(index,tf,data,owner);else LoadCustomCanonicalSource(index,tf,data,owner);return;}
 int slot=tf==PERIOD_M1?0:(tf==PERIOD_M5?1:2);
 if(write)g_pair_states[index].custom_aux[slot]=owner;else owner=g_pair_states[index].custom_aux[slot];
 if(tf==PERIOD_M1){if(write)g_pair_states[index].m1_data=data;else data=g_pair_states[index].m1_data;}
 if(tf==PERIOD_M5){if(write)g_pair_states[index].m5_data=data;else data=g_pair_states[index].m5_data;}
 if(tf==PERIOD_M30){if(write)g_pair_states[index].m30_data=data;else data=g_pair_states[index].m30_data;}
}
void CompletedFixture(string symbol,int tf,datetime seed,ENUM_DIRECTION direction,MLVData &owner)
{
 ZeroMemory(owner);owner.State=MLV_DIRECTION_TAKEN;owner.Direction=direction;owner.ParentExtremeDirection=direction==DIR_BUY?DIR_SELL:DIR_BUY;
 owner.Timeframe=tf;owner.IsValid=true;owner.LastUpdateCandleTime=seed;owner.ParentRawCandleTime=iTime(symbol,tf,10);
 owner.ParentConfirmationCandleTime=iTime(symbol,tf,9);owner.StartCandleTime=iTime(symbol,tf,8);owner.ConfirmationCandleTime=iTime(symbol,tf,7);
 owner.DirectionTakeoverCandleTime=iTime(symbol,tf,6);owner.FrozenMarkedBody=iClose(symbol,tf,7);owner.PreviousClose=iClose(symbol,tf,5);
}
int OnInit()
{
 for(int t=0;t<7;t++)
 {
  int tf=CustomTFValue(t),seconds=GetTimeframeSeconds(tf);datetime seed=iTime(Symbol(),tf,5),target=iTime(Symbol(),tf,1);
  g_pair_count=3;for(int p=0;p<3;p++){InitPairState(g_pair_states[p]);g_pair_states[p].actual_symbol=Symbol();g_pair_canonical_scope[p]=false;}
  g_processing_time=seed+seconds;bool seeded=true;
  for(int i=0;i<3;i++)
  {
   if(!RefreshCustomRequestedOwners(i,tf,seed))seeded=false;
   TimeframeData data;CustomAuxLifecycle owner;Stage(i,tf,data,owner,false);
   // Trusted anchor-state fixture; this does not certify its historical formation.
   CompletedFixture(Symbol(),tf,seed,DIR_BUY,owner.mhvBuy);CompletedFixture(Symbol(),tf,seed,DIR_SELL,owner.mhvSell);Stage(i,tf,data,owner,true);
  }
  Check("seed_trusted_anchor_"+IntegerToString(tf),seeded);
  bool continuous=true;for(int shift=4;shift>=1;shift--){datetime candle=iTime(Symbol(),tf,shift);g_processing_time=candle+seconds;if(!RefreshCustomRequestedOwners(0,tf,candle))continuous=false;}
  Check("continuous_control_"+IntegerToString(tf),continuous);
  g_processing_time=target+seconds;bool ready=RefreshCustomRequestedOwners(1,tf,target);
  TimeframeData a,b;CustomAuxLifecycle control,replayed;Stage(0,tf,a,control,false);Stage(1,tf,b,replayed,false);
  Check("four_bar_catchup_"+IntegerToString(tf),ready && replayed.lastClosed==target && replayed.lastReplayBars==4 && !replayed.recoveryRequired);
  Check("all_M09_M08_M12_fields_match_"+IntegerToString(tf),ready && SameOwners(control,replayed));
  Check("both_M09_owners_advanced_"+IntegerToString(tf),replayed.mhvBuy.LastUpdateCandleTime==target && replayed.mhvSell.LastUpdateCandleTime==target && replayed.mhvBuy.Timeframe==tf && replayed.mhvSell.Timeframe==tf);
  CustomOwnerView view;bool readable=ReadCustomOwnerView(1,tf,"MHV",DIR_BUY,target,view);
  Check("recovered_view_context_only_"+IntegerToString(tf),readable && view.recoveryOnly && !view.entryWindowOpen && !view.entryEligible && !view.executionAvailable);
  CustomAuxLifecycle before=replayed;RefreshCustomRequestedOwners(1,tf,target);Stage(1,tf,b,replayed,false);
  Check("duplicate_idempotent_all_fields_"+IntegerToString(tf),SameOwners(before,replayed));
  Stage(2,tf,b,replayed,false);replayed.mhvBuy.LastUpdateCandleTime=seed+seconds;Stage(2,tf,b,replayed,true);before=replayed;
  bool future=RefreshCustomRequestedOwners(2,tf,target);Stage(2,tf,b,replayed,false);
  Check("future_M09_anchor_holds_without_reset_"+IntegerToString(tf),!future && replayed.recoveryRequired && replayed.recoveryReason=="WAIT_REPLAY_OWNER_ANCHOR" && SameOwners(before,replayed));
 }
 Check("no_orders",OrdersTotal()==0 && OrdersHistoryTotal()==0);
 Print("[CUSTOM-M09REPLAY-SUMMARY] passed=",passed," failed=",failed);return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
