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
#ifdef CUSTOM_OWNER_BASELINE
struct CustomOwnerView {string symbol;string signal;string eventId;string reason;int timeframe;int direction;int ownerState;datetime sourceBar;datetime confirmation;datetime entryCandle;bool readable;bool structuralValid;bool entryEligible;bool executionAvailable;};
bool ReadCustomOwnerView(int index,int tf,string signal,ENUM_DIRECTION direction,datetime latest,CustomOwnerView &view){ZeroMemory(view);return false;}
#endif
int passed=0,failed=0;
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[CUSTOM-OWNER] ",name," ",ok?"PASS":"FAIL");}
int OnInit()
{
 datetime t=D'2026.08.03 09:00';g_pair_count=1;InitPairState(g_pair_states[0]);g_pair_states[0].actual_symbol="GBPUSD";
 g_pair_states[0].h1_data.timeframe=PERIOD_H1;g_pair_states[0].h1_data.is_valid=true;g_pair_states[0].h1_data.is_closed=true;g_pair_states[0].h1_data.barIndex=1;g_pair_states[0].h1_data.candle_time=t;
 ReEntryData re;ZeroMemory(re);re.Timeframe=PERIOD_H1;re.Direction=DIR_BUY;re.Type=RE_TYPE_1;re.State=RE_STATE_CONFIRMED;re.IsValid=true;re.EntryPrice=1.2;re.ConfirmationCandle=t-3600;re.EntryCandle=t;re.StartCandleTime=t-7200;re.LastUpdateCandleTime=t;
 g_pair_states[0].re_h1_buy_state=re;CustomOwnerView view;
 bool ok=ReadCustomOwnerView(0,PERIOD_H1,"RE",DIR_BUY,t,view);string firstId=view.eventId;
 Check("confirmed_RE_readable_not_executable",ok && view.readable && view.structuralValid && !view.entryEligible && !view.executionAvailable && StringLen(firstId)>0);
 g_pair_states[0].h1_data.candle_time=t+3600;g_pair_states[0].re_h1_buy_state.LastUpdateCandleTime=t+3600;
 ok=ReadCustomOwnerView(0,PERIOD_H1,"RE",DIR_BUY,t+3600,view);
 Check("structural_owner_outlives_entry_metadata",ok && view.structuralValid && !view.entryEligible && view.eventId==firstId && view.entryCandle==t);
 g_pair_states[0].re_h1_buy_state.State=RE_STATE_CANDIDATE;ok=ReadCustomOwnerView(0,PERIOD_H1,"RE",DIR_BUY,t+3600,view);Check("candidate_not_confirmed",ok && !view.structuralValid);
 g_pair_states[0].re_h1_buy_state.State=RE_STATE_CONFIRMED;g_pair_states[0].h1_data.is_valid=false;
 Check("warmup_data_not_ready",!ReadCustomOwnerView(0,PERIOD_H1,"RE",DIR_BUY,t+3600,view) && !view.readable);g_pair_states[0].h1_data.is_valid=true;
 Check("stale_owner_snapshot_rejected",!ReadCustomOwnerView(0,PERIOD_H1,"RE",DIR_BUY,t+7200,view));
 Check("unwired_TF_unavailable",!ReadCustomOwnerView(0,PERIOD_M1,"RE",DIR_BUY,t,view));
 ok=ReadCustomOwnerView(0,PERIOD_H1,"RE2",DIR_BUY,t+3600,view);Check("subtype_filter_preserved",ok && !view.structuralValid);
 g_pair_states[0].extreme_h1_buy_lifecycle.Timeframe=PERIOD_H1;g_pair_states[0].extreme_h1_buy_lifecycle.Direction=DIR_BUY;g_pair_states[0].extreme_h1_buy_lifecycle.IsValid=true;g_pair_states[0].extreme_h1_buy_lifecycle.LastUpdateCandleTime=t+3600;g_pair_states[0].extreme_h1_buy_lifecycle.Maturity=EXT_MAT_RAW;
 ok=ReadCustomOwnerView(0,PERIOD_H1,"EXT",DIR_BUY,t+3600,view);Check("raw_EXT_not_mature",ok && !view.structuralValid && !view.entryEligible);
 g_pair_states[0].extreme_h1_buy_lifecycle.Maturity=EXT_MAT_REVERSAL_CONFIRMED;g_pair_states[0].extreme_h1_buy_lifecycle.ConfirmationCandleTime=t;g_pair_states[0].extreme_h1_buy_lifecycle.ConfirmationClose=1.2;
 ok=ReadCustomOwnerView(0,PERIOD_H1,"EXT",DIR_BUY,t+3600,view);Check("mature_EXT_context_only",ok && view.structuralValid && !view.entryEligible && !view.executionAvailable);
 Check("canonical_owners_not_mutated",g_pair_states[0].re_h1_buy_state.EntryCandle==t && g_pair_states[0].re_h1_buy_state.State==RE_STATE_CONFIRMED && g_pair_states[0].extreme_h1_buy_lifecycle.Maturity==EXT_MAT_REVERSAL_CONFIRMED);
 Print("[CUSTOM-OWNER-SUMMARY] passed=",passed," failed=",failed);return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
