#property strict
input bool UseFixtureBroker=true;
// Mock broker I/O only; validation, initialization and state binding remain production code.
double BindingBrokerInfo(string pair,int mode)
{
 if(!UseFixtureBroker)return MarketInfo(pair,mode);
 if(pair!="GBPUSD" && pair!="EURUSD")return 0;
 if(mode==MODE_POINT || mode==MODE_TICKSIZE)return 0.00001;
 if(mode==MODE_DIGITS)return 5;
 if(mode==MODE_TICKVALUE)return pair=="EURUSD"?2.0:1.0;
 if(mode==MODE_MINLOT || mode==MODE_LOTSTEP)return 0.01;
 if(mode==MODE_MAXLOT)return 100;
 return 0;
}
#define MarketInfo BindingBrokerInfo
// Include the actual EA but rename its event handlers: this harness never starts its controller.
#define OnInit CanonicalOnInit
#define OnDeinit CanonicalOnDeinit
#define OnTick CanonicalOnTick
#define OnTimer CanonicalOnTimer
#include "..\\..\\source\\BBMA_EA.mq4"
#undef OnInit
#undef OnDeinit
#undef OnTick
#undef OnTimer
#undef MarketInfo
int passed=0,failed=0;
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[STATE-BINDING] ",name," ",ok?"PASS":"FAIL");}
bool Bind(string &reason)
{
#ifdef CUSTOM_STATE_BASELINE
 reason="MISSING_CAPABILITY";return false;
#else
 return BindCustomPairStates(reason);
#endif
}
int OnInit()
{
 string reason;g_pair_count=1;InitPairState(g_pair_states[0]);
 g_pair_names[0]="GBPUSD";g_pair_states[0].base_symbol="GBPUSD";g_pair_states[0].actual_symbol="GBPUSD";
 g_pair_states[0].pair_id=14;g_pair_states[0].magic_number=GenerateMagicNumber(StrategyID,InstanceID,14);g_pair_states[0].pair_enabled=true;g_pair_states[0].broker_spec_valid=true;g_pair_states[0].tick_value=1.0;
 g_pair_states[0].re_m15_buy_state.EntryCandle=111;g_processed_candle_time[0]=222;
#ifndef CUSTOM_STATE_BASELINE
 g_pair_canonical_scope[0]=true;
#endif
 for(int s=0;s<5;s++)g_custom_slots[s].enabled=false;
 ArrayResize(g_custom_universe,1);g_custom_universe[0]="GBPUSD";
 bool ok=Bind(reason);Check("all_off_preserves_pool",ok && g_pair_count==1 && g_pair_states[0].re_m15_buy_state.EntryCandle==111 && g_processed_candle_time[0]==222);
 g_custom_slots[0].enabled=true;ok=Bind(reason);
#ifndef CUSTOM_STATE_BASELINE
 Check("reuse_exact_state",ok && ArraySize(g_custom_pair_indices)==1 && g_custom_pair_indices[0]==0 && g_pair_count==1 && g_pair_canonical_scope[0] && g_pair_states[0].re_m15_buy_state.EntryCandle==111);
#else
 Check("reuse_exact_state",ok);
#endif
 ArrayResize(g_custom_universe,2);g_custom_universe[1]="EURUSD";ok=Bind(reason);
#ifndef CUSTOM_STATE_BASELINE
 if(!UseFixtureBroker)
 {
  Check("real_nonchart_spec_rejected",!ok && reason=="CUSTOM_PAIR_BROKER_SPEC_NOT_READY:EURUSD");
  Check("real_failed_append_rolled_back",g_pair_count==1 && ArraySize(g_custom_pair_indices)==0 && StringLen(g_pair_states[1].actual_symbol)==0 && !g_pair_canonical_scope[1] && g_pair_states[0].re_m15_buy_state.EntryCandle==111 && g_processed_candle_time[0]==222);
  Print("[STATE-BINDING-SUMMARY] passed=",passed," failed=",failed);
  return failed==0?INIT_SUCCEEDED:INIT_FAILED;
 }
 Check("append_custom_state",ok && g_pair_count==2 && g_custom_pair_indices[1]==1 && g_pair_states[1].actual_symbol=="EURUSD" && g_pair_states[1].pair_id==13 && !g_pair_canonical_scope[1] && g_pair_states[1].tick_value==2.0 && g_pair_states[0].tick_value==1.0);
 if(ok)
 {
  g_pair_states[1].re_m15_buy_state.EntryCandle=333;g_processed_candle_time[1]=444;
  Check("state_isolation",g_pair_states[0].re_m15_buy_state.EntryCandle==111 && g_processed_candle_time[0]==222 && g_pair_states[1].re_m15_buy_state.EntryCandle==333 && g_processed_candle_time[1]==444);
  Check("repeat_reuses_without_reset",Bind(reason) && g_pair_count==2 && g_pair_states[1].re_m15_buy_state.EntryCandle==333 && g_processed_candle_time[1]==444);
 }
 else {Check("state_isolation",false);Check("repeat_reuses_without_reset",false);}
 g_custom_universe[1]="BROKER_UNAVAILABLE_CFD";
 bool failedBroker=!Bind(reason);Print("[STATE-DEBUG] failed=",failedBroker," reason=",reason," count=",g_pair_count," map=",ArraySize(g_custom_pair_indices)," empty_by_length=",StringLen(g_pair_states[2].actual_symbol)==0," empty_by_comparison=",g_pair_states[2].actual_symbol==""," scope2=",g_pair_canonical_scope[2]);
 Check("broker_failure_rolls_back_new_state",failedBroker && g_pair_count==2 && ArraySize(g_custom_pair_indices)==0 && StringLen(g_pair_states[2].actual_symbol)==0 && !g_pair_canonical_scope[2]);
 g_custom_universe[1]="GBPUSD.other";
 Check("collision_rejects_without_pool_growth",!Bind(reason) && g_pair_count==2 && ArraySize(g_custom_pair_indices)==0);
 Check("existing_states_retained_on_failure",g_pair_states[0].re_m15_buy_state.EntryCandle==111 && g_pair_states[1].re_m15_buy_state.EntryCandle==333);
#else
 Check("append_custom_state",ok);Check("state_isolation",false);Check("repeat_reuses_without_reset",false);
 Check("collision_rejects_without_pool_growth",false);Check("existing_states_retained_on_failure",false);
#endif
 Print("[STATE-BINDING-SUMMARY] passed=",passed," failed=",failed);
 return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
