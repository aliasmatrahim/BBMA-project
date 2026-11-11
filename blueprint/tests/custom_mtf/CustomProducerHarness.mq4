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
#ifdef CUSTOM_PRODUCER_BASELINE
bool RefreshCustomAuxOwners(int pairIndex,int tf,datetime latest){return false;}
bool CustomReEntryWindowOpen(ReEntryData &source,int tf,datetime currentOpen){return false;}
#endif
int passed=0,failed=0;
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[CUSTOM-PRODUCER] ",name," ",ok?"PASS":"FAIL");}
int OnInit()
{
 g_pair_count=2;for(int p=0;p<2;p++){InitPairState(g_pair_states[p]);g_pair_states[p].actual_symbol=Symbol();}
 g_processing_time=TimeCurrent();
 int frames[3]={PERIOD_M1,PERIOD_M5,PERIOD_M30};
 for(int i=0;i<3;i++)
 {
  int tf=frames[i];datetime latest=GetLatestClosedCandleTime(Symbol(),tf);
  bool first=RefreshCustomAuxOwners(0,tf,latest);
  bool again=RefreshCustomAuxOwners(0,tf,latest);
  Print("[CUSTOM-PRODUCER-DATA] TF=",tf," latest=",latest," bars=",iBars(Symbol(),tf)," first=",first," duplicate=",again);
  Check("producer_ready_and_duplicate_"+IntegerToString(tf),latest>0 && first && again);
#ifndef CUSTOM_PRODUCER_BASELINE
  // Selector acceptance uses a confirmed owner fixture, not a claimed market setup.
  ReEntryData projectedOwner;ZeroMemory(projectedOwner);projectedOwner.Timeframe=tf;projectedOwner.Direction=DIR_BUY;projectedOwner.Type=RE_TYPE_1;projectedOwner.State=RE_STATE_CONFIRMED;projectedOwner.IsValid=true;projectedOwner.EntryPrice=1.2;projectedOwner.ConfirmationCandle=latest;projectedOwner.EntryCandle=latest+GetTimeframeSeconds(tf);projectedOwner.LastUpdateCandleTime=latest;
  g_pair_states[0].custom_aux[i].reBuy=projectedOwner;CustomOwnerView projected;
  Check("aux_RE_projection_"+IntegerToString(tf),ReadCustomOwnerView(0,tf,"RE",DIR_BUY,latest,projected) && projected.structuralValid && !projected.entryEligible && !projected.executionAvailable);
#endif
 }
#ifndef CUSTOM_PRODUCER_BASELINE
 datetime observed=g_pair_states[0].custom_aux[0].lastClosed;
 Check("symbol_state_isolated",observed>0 && g_pair_states[1].custom_aux[0].lastClosed==0);
 g_pair_states[0].custom_aux[0].lastClosed=observed-120;
 ENUM_RE_STATE original=g_pair_states[0].custom_aux[0].reBuy.State;
 Check("gap_requires_recovery_without_expiry",!RefreshCustomAuxOwners(0,PERIOD_M1,observed) && g_pair_states[0].custom_aux[0].recoveryRequired && g_pair_states[0].custom_aux[0].reBuy.State==original);
 Check("gap_view_is_unavailable",!ReadCustomOwnerView(0,PERIOD_M1,"RE",DIR_BUY,observed,g_custom_owner_frames[0].views[0]) && g_custom_owner_frames[0].views[0].reason=="WAIT_OWNER_RECOVERY");
#endif
 Check("invalid_pair_rejected",!RefreshCustomAuxOwners(2,PERIOD_M1,TimeCurrent()-60));
 Check("canonical_tf_not_duplicated",!RefreshCustomAuxOwners(0,PERIOD_H1,TimeCurrent()-3600));
 Check("missing_bar_rejected",!RefreshCustomAuxOwners(0,PERIOD_M1,0));
 ReEntryData re;ZeroMemory(re);re.Timeframe=PERIOD_M1;re.State=RE_STATE_CONFIRMED;re.Direction=DIR_BUY;re.IsValid=true;re.ConfirmationCandle=D'2026.08.03 10:00';re.EntryCandle=re.ConfirmationCandle+60;
 Check("next_source_candle_window",CustomReEntryWindowOpen(re,PERIOD_M1,re.EntryCandle));
 Check("late_window_without_structural_expiry",!CustomReEntryWindowOpen(re,PERIOD_M1,re.EntryCandle+60) && re.IsValid && re.State==RE_STATE_CONFIRMED);
 for(int f=0;f<7;f++)
 {
  re.Timeframe=CustomTFValue(f);re.EntryCandle=re.ConfirmationCandle+GetTimeframeSeconds(re.Timeframe);
  Check("window_exact_source_TF_"+IntegerToString(re.Timeframe),CustomReEntryWindowOpen(re,re.Timeframe,re.EntryCandle) && !CustomReEntryWindowOpen(re,re.Timeframe,re.EntryCandle+GetTimeframeSeconds(re.Timeframe)) && re.IsValid);
 }
 re.Timeframe=PERIOD_M1;re.EntryCandle=0;Check("missing_entry_fails_closed",!CustomReEntryWindowOpen(re,PERIOD_M1,D'2026.08.03 10:01'));
 Print("[CUSTOM-PRODUCER-SUMMARY] passed=",passed," failed=",failed);return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
