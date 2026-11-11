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
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[CUSTOM-RECOVERY] ",name," ",ok?"PASS":"FAIL");}
#include "CustomOwnerTestEquality.mqh"
int OnInit()
{
 g_pair_count=3;for(int p=0;p<3;p++){InitPairState(g_pair_states[p]);g_pair_states[p].actual_symbol=Symbol();}
 int frames[3]={PERIOD_M1,PERIOD_M5,PERIOD_M30};
 for(int slot=0;slot<3;slot++)
 {
  int tf=frames[slot],seconds=GetTimeframeSeconds(tf);
  datetime seed=iTime(Symbol(),tf,5),target=iTime(Symbol(),tf,2),fresh=iTime(Symbol(),tf,1);
  g_processing_time=seed+seconds;
  bool seeded=seed>0 && RefreshCustomAuxOwners(0,tf,seed) && RefreshCustomAuxOwners(1,tf,seed);
  Check("seed_"+IntegerToString(tf),seeded);
  bool continuous=true;
  for(int shift=4;shift>=2;shift--)
  {
   datetime candle=iTime(Symbol(),tf,shift);g_processing_time=candle+seconds;
   if(!RefreshCustomAuxOwners(0,tf,candle))continuous=false;
  }
  Check("continuous_control_"+IntegerToString(tf),continuous && g_pair_states[0].custom_aux[slot].lastClosed==target);
  g_processing_time=target+seconds;
  bool recovered=RefreshCustomAuxOwners(1,tf,target);
  Check("replay_catches_up_"+IntegerToString(tf),recovered && !g_pair_states[1].custom_aux[slot].recoveryRequired && g_pair_states[1].custom_aux[slot].lastClosed==target);
  Check("all_owner_fields_match_control_"+IntegerToString(tf),recovered && SameOwners(g_pair_states[0].custom_aux[slot],g_pair_states[1].custom_aux[slot]));
  CustomAuxLifecycle before=g_pair_states[1].custom_aux[slot];
  Check("duplicate_does_not_replay_"+IntegerToString(tf),RefreshCustomAuxOwners(1,tf,target) && SameOwners(before,g_pair_states[1].custom_aux[slot]));
#ifdef CUSTOM_RECOVERY_BASELINE
  Check("replay_is_context_only_"+IntegerToString(tf),false);
#else
  CustomOwnerView view;ReadCustomOwnerView(1,tf,"RE",DIR_BUY,target,view);
  Check("replay_is_context_only_"+IntegerToString(tf),view.recoveryOnly && !view.entryWindowOpen && !view.entryEligible && !view.executionAvailable && g_pair_states[1].custom_aux[slot].contextOnlyThrough==target && g_pair_states[1].custom_aux[slot].lastReplayBars==3);
#endif
  g_processing_time=fresh+seconds;
  bool resumed=RefreshCustomAuxOwners(1,tf,fresh);
  Check("next_genuine_bar_resumes_"+IntegerToString(tf),resumed && !g_pair_states[1].custom_aux[slot].recoveryRequired && g_pair_states[1].custom_aux[slot].lastClosed==fresh);
 }
 g_processing_time=TimeCurrent();datetime last=GetLatestClosedCandleTime(Symbol(),PERIOD_M1);
 g_pair_states[2].custom_aux[0].lastClosed=last-103;
 g_pair_states[2].custom_aux[0].reBuy.State=RE_STATE_CONFIRMED;g_pair_states[2].custom_aux[0].reBuy.IsValid=true;
 CustomAuxLifecycle prior=g_pair_states[2].custom_aux[0];
 bool missing=RefreshCustomAuxOwners(2,PERIOD_M1,last);
 Check("missing_exact_anchor_holds",!missing && g_pair_states[2].custom_aux[0].recoveryRequired);
 Check("failed_recovery_preserves_structural_owner",SameOwners(prior,g_pair_states[2].custom_aux[0]) && g_pair_states[2].custom_aux[0].reBuy.IsValid);
#ifndef CUSTOM_RECOVERY_BASELINE
 InitPairState(g_pair_states[2]);g_pair_states[2].actual_symbol=Symbol();
 g_pair_states[2].custom_aux[0].lastClosed=iTime(Symbol(),PERIOD_M1,3);
 g_pair_states[2].custom_aux[0].reBuy.LastUpdateCandleTime=last+60;
 g_pair_states[2].custom_aux[0].reBuy.State=RE_STATE_CONFIRMED;g_pair_states[2].custom_aux[0].reBuy.IsValid=true;
 prior=g_pair_states[2].custom_aux[0];
 bool future=RefreshCustomAuxOwners(2,PERIOD_M1,last);
 Check("owner_watermark_cannot_exceed_replay_anchor",!future && SameOwners(prior,g_pair_states[2].custom_aux[0]) && g_pair_states[2].custom_aux[0].recoveryReason=="WAIT_REPLAY_OWNER_ANCHOR");
 // A long backlog advances in bounded chunks while views remain unavailable.
 InitPairState(g_pair_states[2]);g_pair_states[2].actual_symbol=Symbol();
 datetime backlog=iTime(Symbol(),PERIOD_M1,300);
 g_pair_states[2].custom_aux[0].lastClosed=backlog;
 bool firstChunk=RefreshCustomAuxOwners(2,PERIOD_M1,last);
 Check("bounded_chunk_keeps_recovery_hold",!firstChunk && g_pair_states[2].custom_aux[0].recoveryRequired && g_pair_states[2].custom_aux[0].lastReplayBars==256 && g_pair_states[2].custom_aux[0].lastClosed==iTime(Symbol(),PERIOD_M1,44));
 bool secondChunk=RefreshCustomAuxOwners(2,PERIOD_M1,last);
 Check("next_chunk_resumes_without_replay",secondChunk && !g_pair_states[2].custom_aux[0].recoveryRequired && g_pair_states[2].custom_aux[0].lastReplayBars==299 && g_pair_states[2].custom_aux[0].lastClosed==last);
 InitPairState(g_pair_states[2]);g_pair_states[2].actual_symbol=Symbol();
 int insufficient=iBars(Symbol(),PERIOD_M1)-3;
 g_pair_states[2].custom_aux[0].lastClosed=iTime(Symbol(),PERIOD_M1,insufficient);
 g_pair_states[2].custom_aux[0].reBuy.State=RE_STATE_CONFIRMED;g_pair_states[2].custom_aux[0].reBuy.IsValid=true;
 prior=g_pair_states[2].custom_aux[0];
 bool warmup=RefreshCustomAuxOwners(2,PERIOD_M1,last);
 Check("missing_warmup_does_not_publish_partial_chunk",!warmup && g_pair_states[2].custom_aux[0].recoveryRequired && SameOwners(prior,g_pair_states[2].custom_aux[0]) && g_pair_states[2].custom_aux[0].lastReplayBars==0);
#endif
 Print("[CUSTOM-RECOVERY-SUMMARY] passed=",passed," failed=",failed);return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
