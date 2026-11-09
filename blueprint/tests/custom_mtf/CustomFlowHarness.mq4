#property strict
// Actual M27 callback/controller -> observer -> M06/M08/M12 -> owner views.
// Monitor fixture admission only; canonical/custom order admission stays OFF.
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
input bool FlowOnlyM09M1=false; // Prove M09-only request drives its shared producer.
input bool FlowExpectMomentum=false;
input bool FlowExpectHigher=false; // Capability expectation for the tested source revision.
input int FlowStartHour=2; // Chosen by read-only source-history preflight.
int passed=0,failed=0,ticks=0,advances[3],tickAdvances=0,timerAdvances=0,nonM15=0,simultaneous=0,frames=0;
bool initialized=false,printed=false,closedOK=true,duplicatesOK=true,orderOK=true,flagsOK=true,unavailableOK=true,canonicalExcluded=true;
datetime endAt=0,startAt=0;
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[CUSTOM-FLOW] ",name," ",ok?"PASS":"FAIL");}
int OnInit()
{
 int code=CanonicalOnInit();initialized=(code==INIT_SUCCEEDED);
 if(!initialized){Print("[CUSTOM-FLOW-INIT] failed code=",code);return code;}
 if(g_pair_count!=1 || g_pair_states[0].actual_symbol!=Symbol())return INIT_FAILED;
 g_pair_canonical_scope[0]=false;ArrayResize(g_custom_pair_indices,1);g_custom_pair_indices[0]=0;
 ZeroMemory(g_custom_use);
 int indexes[3]={0,1,3};
 for(int i=0;i<3;i++){int t=indexes[i];g_custom_use.tfEnabled[t]=true;g_custom_use.signalEnabled[t*11]=true;g_custom_use.signalEnabled[t*11+5]=true;}
 if(FlowOnlyM09M1){g_custom_use.signalEnabled[0]=false;g_custom_use.signalEnabled[5]=false;g_custom_use.signalEnabled[6]=true;g_custom_use.signalEnabled[7]=true;}
 g_custom_use.tfEnabled[4]=true;g_custom_use.signalEnabled[44]=true; // H1 custom-only producer is still unavailable.
 g_custom_use.signalEnabled[10]=true; // Shared M10 diagnostic snapshot expected only on supported revision.
 startAt=StringToTime(TimeToString(TimeCurrent(),TIME_DATE))+FlowStartHour*3600;endAt=startAt+7200;
 Print("[CUSTOM-FLOW-INIT] start=",startAt," connected=",IsConnected()," testing=",IsTesting()," chartTF=",Period()," quote=",(datetime)MarketInfo(Symbol(),MODE_TIME));
 return INIT_SUCCEEDED;
}
void Finish()
{
 if(printed)return;printed=true;
 Check("canonical_startup",initialized);
 Check("moving_M1_tester_schedule",ticks>=100 && Period()==PERIOD_M1 && TimeDay(startAt)==4 && TimeMonth(startAt)==8);
 Check("all_three_producers_advance",advances[0]>=100 && advances[1]>=20 && advances[2]>=3);
 Check("tick_and_timer_handlers_deliver",tickAdvances>0 && timerAdvances>0);
 Check("M1_without_waiting_M15",nonM15>=50);
 Check("simultaneous_frame_high_to_low",simultaneous>0 && orderOK);
 Check("only_matching_closed_snapshots",closedOK && frames>=100);
 Check("duplicate_tick_timer_state_stable",duplicatesOK && frames>=100);
 Check("M09_MOM_H1_capability_scope",unavailableOK && frames>=100);
 Check("no_entry_or_execution_authority",flagsOK && frames>=100);
 Check("custom_only_never_canonical_dispatch",canonicalExcluded && g_processed_candle_time[0]==0);
 Check("no_broker_orders",OrdersTotal()==0 && OrdersHistoryTotal()==0);
 Print("[CUSTOM-FLOW-DATA] ticks=",ticks," M1=",advances[0]," M5=",advances[1]," M30=",advances[2]," tickFirst=",tickAdvances," timerFirst=",timerAdvances," nonM15=",nonM15," simultaneous=",simultaneous," frames=",frames);
 Print("[CUSTOM-FLOW-SUMMARY] passed=",passed," failed=",failed);
}
void OnTick()
{
 if(TimeCurrent()<startAt)return;
 if(TimeCurrent()>=endAt){Finish();ExpertRemove();return;}
 ticks++;datetime before[3];ArrayInitialize(before,0);for(int p=0;p<3;p++)before[p]=g_pair_states[0].custom_aux[p].lastClosed;
 bool timerFirst=(ticks%2==0);if(timerFirst)CanonicalOnTimer();else CanonicalOnTick();
 bool changed[3];ArrayInitialize(changed,false);
 int tf[3]={PERIOD_M1,PERIOD_M5,PERIOD_M30};
 for(int i=0;i<3;i++)
 {
  datetime last=g_pair_states[0].custom_aux[i].lastClosed;changed[i]=(last>before[i]);
  if(changed[i])advances[i]++;
  if(last<=0 || last!=GetLatestClosedCandleTime(Symbol(),tf[i]) || g_pair_states[0].custom_aux[i].recoveryRequired)closedOK=false;
 }
 if(changed[0]){if(timerFirst)timerAdvances++;else tickAdvances++;if(before[0]>0 && TimeMinute(TimeCurrent())%15!=0)nonM15++;}
 if(before[0]>0 && changed[0] && changed[1] && changed[2])simultaneous++;
 CustomOwnerFrame frame=g_custom_owner_frames[0];
 if(frame.viewCount==16)
 {
  frames++;
  if(frame.views[0].timeframe!=PERIOD_H1 || frame.views[2].timeframe!=PERIOD_M30 || frame.views[6].timeframe!=PERIOD_M5 || frame.views[10].timeframe!=PERIOD_M1)orderOK=false;
  if(FlowExpectHigher)
  {
   if(!g_pair_states[0].h1_data.is_valid || g_pair_states[0].h1_data.candle_time!=GetLatestClosedCandleTime(Symbol(),PERIOD_H1))unavailableOK=false;
  }
  else if(frame.views[0].readable || frame.views[1].readable)unavailableOK=false;
  if(FlowOnlyM09M1 && (frame.views[10].signal!="MHV" || frame.views[12].signal!="MLV" ||
     g_pair_states[0].custom_aux[0].mhvBuy.Timeframe!=PERIOD_M1 || g_pair_states[0].custom_aux[0].mhvSell.Timeframe!=PERIOD_M1 ||
     g_pair_states[0].custom_aux[0].mhvBuy.Direction!=DIR_BUY || g_pair_states[0].custom_aux[0].mhvSell.Direction!=DIR_SELL))unavailableOK=false;
  if(frame.views[14].readable!=FlowExpectMomentum || frame.views[15].readable!=FlowExpectMomentum)unavailableOK=false;
  for(int v=0;v<frame.viewCount;v++)if(frame.views[v].entryEligible || frame.views[v].executionAvailable)flagsOK=false;
 }
 else if(ticks>1)closedOK=false;
 TimeframeData data[3];data[0]=g_pair_states[0].m1_data;data[1]=g_pair_states[0].m5_data;data[2]=g_pair_states[0].m30_data;
 for(int d=0;d<3;d++)if(!data[d].is_valid || !data[d].is_closed || data[d].barIndex!=1 || data[d].candle_time+GetTimeframeSeconds(tf[d])>TimeCurrent())closedOK=false;
 CustomAuxLifecycle snapshot[3];for(int s=0;s<3;s++)snapshot[s]=g_pair_states[0].custom_aux[s];
 datetime frameTime=frame.observedAt;CanonicalOnTick();CanonicalOnTimer();
 for(int copy=0;copy<3;copy++)if(!SameOwners(snapshot[copy],g_pair_states[0].custom_aux[copy]))duplicatesOK=false;
 if(g_custom_owner_frames[0].observedAt!=frameTime)duplicatesOK=false;
 if(g_processed_candle_time[0]!=0)canonicalExcluded=false;
 if(ticks<3)Print("[CUSTOM-FLOW-TICK] time=",TimeCurrent()," quote=",(datetime)MarketInfo(Symbol(),MODE_TIME)," processing=",g_processing_time," connected=",IsConnected()," frame=",frame.viewCount," lastM1=",g_pair_states[0].custom_aux[0].lastClosed," recovery=",g_pair_states[0].custom_aux[0].recoveryReason);
}
void OnDeinit(const int reason){Finish();CanonicalOnDeinit(reason);}
void OnTimer(){} // Native tester does not register EventSetTimer; handlers are delivered above.
