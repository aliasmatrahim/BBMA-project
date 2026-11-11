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
int passed=0,failed=0;
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[CUSTOM-M09PRODUCER] ",name," ",ok?"PASS":"FAIL");}
void FixtureOwner(int index,int tf,MLVData &owner,bool write)
{
 if(tf==PERIOD_M15)
 {if(write)g_pair_states[index].mlv_buy_state=owner;else owner=g_pair_states[index].mlv_buy_state;return;}
#ifndef CUSTOM_M09PRODUCER_BASELINE
 int canonical=CustomCanonicalTFIndex(tf);
 if(canonical>=0)
 {if(write)g_pair_states[index].custom_higher_mhv_buy[canonical]=owner;else owner=g_pair_states[index].custom_higher_mhv_buy[canonical];return;}
 int aux=tf==PERIOD_M1?0:(tf==PERIOD_M5?1:2);
 if(write)g_pair_states[index].custom_aux[aux].mhvBuy=owner;else owner=g_pair_states[index].custom_aux[aux].mhvBuy;
#endif
}
void RecoveryFixture(int tf,bool required)
{
 int canonical=CustomCanonicalTFIndex(tf);
 if(canonical>=0)g_pair_states[0].custom_canonical[canonical].recoveryRequired=required;
 else {int aux=tf==PERIOD_M1?0:(tf==PERIOD_M5?1:2);g_pair_states[0].custom_aux[aux].recoveryRequired=required;}
}
int OnInit()
{
 g_pair_count=2;for(int p=0;p<2;p++){InitPairState(g_pair_states[p]);g_pair_states[p].actual_symbol=p==0?Symbol():"UNAVAILABLE_SYMBOL_FIXTURE";g_pair_canonical_scope[p]=false;}
 g_processing_time=TimeCurrent();
 for(int t=0;t<7;t++)
 {
  int tf=CustomTFValue(t);datetime latest=iTime(Symbol(),tf,1);
  // Trusted completed-owner fixture tests wiring, not historical formation/recovery.
  MLVData owner;ZeroMemory(owner);owner.State=MLV_DIRECTION_TAKEN;owner.Direction=DIR_BUY;owner.ParentExtremeDirection=DIR_SELL;owner.Timeframe=tf;
  owner.IsValid=true;owner.ParentRawCandleTime=iTime(Symbol(),tf,5);owner.ParentConfirmationCandleTime=iTime(Symbol(),tf,4);
  owner.StartCandleTime=iTime(Symbol(),tf,4);owner.ConfirmationCandleTime=iTime(Symbol(),tf,3);owner.DirectionTakeoverCandleTime=iTime(Symbol(),tf,2);
  owner.LastUpdateCandleTime=iTime(Symbol(),tf,2);owner.FrozenMarkedBody=1.2;owner.PreviousClose=iClose(Symbol(),tf,2);
  FixtureOwner(0,tf,owner,true);
  bool ready=RefreshCustomRequestedOwners(0,tf,latest);
  Check("closed_source_"+IntegerToString(tf),ready);
  CustomOwnerView a,b;bool mhv=ReadCustomOwnerView(0,tf,"MHV",DIR_BUY,latest,a);bool mlv=ReadCustomOwnerView(0,tf,"MLV",DIR_BUY,latest,b);
  Check("existing_M09_engine_advances_"+IntegerToString(tf),mhv && a.readable && a.structuralValid && a.sourceBar==latest && a.timeframe==tf);
  Check("MHV_MLV_one_identity_"+IntegerToString(tf),mlv && b.structuralValid && b.eventId==a.eventId && StringLen(a.eventId)>0);
  Check("cold_observation_context_only_"+IntegerToString(tf),a.recoveryOnly && !a.entryWindowOpen && !a.entryEligible && !a.executionAvailable);
  MLVData before;ZeroMemory(before);FixtureOwner(0,tf,before,false);RefreshCustomRequestedOwners(0,tf,latest);FixtureOwner(0,tf,owner,false);
  Check("duplicate_no_owner_progress_"+IntegerToString(tf),owner.LastUpdateCandleTime==before.LastUpdateCandleTime && owner.ParentRawCandleTime==before.ParentRawCandleTime && owner.FrozenMarkedBody==before.FrozenMarkedBody);
  Check("other_symbol_not_borrowed_"+IntegerToString(tf),!RefreshCustomRequestedOwners(1,tf,latest) && !ReadCustomOwnerView(1,tf,"MHV",DIR_BUY,latest,b));
  RecoveryFixture(tf,true);Check("recovery_hides_M09_view_"+IntegerToString(tf),!ReadCustomOwnerView(0,tf,"MHV",DIR_BUY,latest,b));RecoveryFixture(tf,false);
 }
 Check("M15_existing_slots_reused",g_pair_states[0].mlv_buy_state.LastUpdateCandleTime==iTime(Symbol(),PERIOD_M15,1));
 g_pair_canonical_scope[0]=true;CustomOwnerView view;
 Check("canonical_higher_M09_unavailable",!ReadCustomOwnerView(0,PERIOD_H1,"MHV",DIR_BUY,iTime(Symbol(),PERIOD_H1,1),view));
 Check("no_orders",OrdersTotal()==0 && OrdersHistoryTotal()==0);
 Print("[CUSTOM-M09PRODUCER-SUMMARY] passed=",passed," failed=",failed);return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
