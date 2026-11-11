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
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[CUSTOM-MHV] ",name," ",ok?"PASS":"FAIL");}
int OnInit()
{
 datetime t=D'2026.08.03 09:00';g_pair_count=1;InitPairState(g_pair_states[0]);g_pair_states[0].actual_symbol="GBPUSD";
 g_pair_states[0].m15_data.timeframe=PERIOD_M15;g_pair_states[0].m15_data.is_valid=true;g_pair_states[0].m15_data.is_closed=true;g_pair_states[0].m15_data.barIndex=1;g_pair_states[0].m15_data.candle_time=t;
 MLVData owner;ZeroMemory(owner);owner.Timeframe=PERIOD_M15;owner.Direction=DIR_BUY;owner.IsValid=true;owner.State=MLV_FORMATION_ESTABLISHED;owner.LastUpdateCandleTime=t;owner.ConfirmationCandleTime=t-900;owner.FrozenMarkedBody=1.2;owner.StartCandleTime=t-1800;owner.ParentRawCandleTime=t-3600;
 g_pair_states[0].mlv_buy_state=owner;CustomOwnerView a,b;
 bool mhv=ReadCustomOwnerView(0,PERIOD_M15,"MHV",DIR_BUY,t,a);bool mlv=ReadCustomOwnerView(0,PERIOD_M15,"MLV",DIR_BUY,t,b);
 Check("mature_MHV_source_projection",mhv && a.structuralValid && a.readable && !a.entryEligible && !a.executionAvailable && StringLen(a.eventId)>0);
 Check("MLV_same_canonical_owner",mlv && b.structuralValid && b.eventId==a.eventId && b.signal=="MLV");
 g_pair_states[0].mlv_buy_state.State=MLV_LOSS_DEVELOPING;ReadCustomOwnerView(0,PERIOD_M15,"MHV",DIR_BUY,t,a);Check("unconfirmed_loss_not_mature",a.readable && !a.structuralValid);
 g_pair_states[0].mlv_buy_state.State=MLV_VOID;ReadCustomOwnerView(0,PERIOD_M15,"MLV",DIR_BUY,t,a);Check("void_owner_not_valid",a.readable && !a.structuralValid);
 Check("stale_owner_rejected",!ReadCustomOwnerView(0,PERIOD_M15,"MHV",DIR_BUY,t+900,a));
 Check("other_TF_stays_unavailable",!ReadCustomOwnerView(0,PERIOD_H1,"MHV",DIR_BUY,t,a));
 Check("no_new_direction_alias",!ReadCustomOwnerView(0,PERIOD_M15,"CSA",DIR_BUY,t,a));
 Check("projection_does_not_mutate",g_pair_states[0].mlv_buy_state.State==MLV_VOID && g_pair_states[0].mlv_buy_state.LastUpdateCandleTime==t);
 Print("[CUSTOM-MHV-SUMMARY] passed=",passed," failed=",failed);return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
