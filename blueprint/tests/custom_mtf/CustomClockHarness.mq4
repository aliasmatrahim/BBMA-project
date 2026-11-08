#property strict
#include "CanonicalClockSecondsFixture.mqh"
#ifndef CUSTOM_CLOCK_BASELINE
#include "..\\..\\source\\custom_mtf\\CustomClock.mqh"
#else
struct CustomClosedObservation {int timeframe;datetime closedOpen;datetime currentOpen;bool requested;bool barReady;};
struct CustomClosedEvent {int timeframe;datetime closedOpen;datetime currentOpen;bool continuousBoundary;};
struct CustomEventBatch {string symbol;datetime observedAt;long ticket;int eventCount;CustomClosedEvent events[7];CustomClosedObservation observations[7];};
struct CustomClockState {string symbol;bool busy;long ticket;string pendingSymbol;bool primed[7];datetime lastClosed[7];datetime lastOpen[7];};
bool BeginCustomClosedBatch(string symbol,datetime now,datetime quote,CustomClosedObservation &obs[],CustomClockState &state,CustomEventBatch &batch,string &reason){batch.eventCount=0;reason="MISSING_CAPABILITY";return false;}
bool CompleteCustomClosedBatch(CustomClockState &state,CustomEventBatch &batch,bool accepted){return false;}
#endif
int passed=0,failed=0;
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[CUSTOM-CLOCK] ",name," ",ok?"PASS":"FAIL");}
void Observe(CustomClosedObservation &o[],datetime open,bool all)
{
 int tf[7]={1,5,15,30,60,240,1440};ArrayResize(o,7);
 for(int i=0;i<7;i++){o[i].timeframe=tf[i];o[i].closedOpen=open-GetTimeframeSeconds(tf[i]);o[i].currentOpen=open;o[i].requested=all || i==0;o[i].barReady=true;}
}
int OnInit()
{
 datetime t=D'2026.08.03 00:00';string reason;CustomClockState state;ZeroMemory(state);CustomEventBatch b,old;CustomClosedObservation o[];
 Observe(o,t,false);bool ok=BeginCustomClosedBatch("GBPUSD",t,t,o,state,b,reason);
 Check("restart_primes_without_replay",ok && b.eventCount==0);CompleteCustomClosedBatch(state,b,true);
 o[0].closedOpen=t;o[0].currentOpen=t+60;ok=BeginCustomClosedBatch("GBPUSD",t+60,t+60,o,state,b,reason);
 Check("M1_does_not_wait_M15",ok && b.eventCount==1 && b.events[0].timeframe==1 && b.events[0].continuousBoundary);
 old=b;CustomEventBatch nested;Check("reentrancy_blocked",!BeginCustomClosedBatch("GBPUSD",t+60,t+60,o,state,nested,reason));
 CompleteCustomClosedBatch(state,b,true);ok=BeginCustomClosedBatch("GBPUSD",t+60,t+60,o,state,b,reason);
 Check("duplicate_tick_timer_no_event",ok && b.eventCount==0);CompleteCustomClosedBatch(state,b,true);
 o[0].closedOpen=t+60;o[0].currentOpen=t+120;
 Check("missing_quote_wait",!BeginCustomClosedBatch("GBPUSD",t+120,0,o,state,b,reason));
 Check("stale_quote_cannot_create_close",!BeginCustomClosedBatch("GBPUSD",t+120,t+59,o,state,b,reason));
 o[0].barReady=false;Check("missing_history_wait",!BeginCustomClosedBatch("GBPUSD",t+120,t+120,o,state,b,reason));o[0].barReady=true;
 ok=BeginCustomClosedBatch("GBPUSD",t+120,t+120,o,state,b,reason);Check("wait_does_not_consume_event",ok && b.eventCount==1);CompleteCustomClosedBatch(state,b,false);
 ok=BeginCustomClosedBatch("GBPUSD",t+120,t+120,o,state,b,reason);Check("aborted_batch_retries",ok && b.eventCount==1);
 Check("old_completion_rejected",!CompleteCustomClosedBatch(state,old,true));CompleteCustomClosedBatch(state,b,true);
 CustomClockState allState;ZeroMemory(allState);Observe(o,t,true);BeginCustomClosedBatch("XAUUSD",t,t,o,allState,b,reason);CompleteCustomClosedBatch(allState,b,true);
 Observe(o,t+86400,true);ok=BeginCustomClosedBatch("XAUUSD",t+86400,t+86400,o,allState,b,reason);
 Check("seven_TF_high_to_low",ok && b.eventCount==7 && b.events[0].timeframe==1440 && b.events[1].timeframe==240 && b.events[2].timeframe==60 && b.events[3].timeframe==30 && b.events[4].timeframe==15 && b.events[5].timeframe==5 && b.events[6].timeframe==1);CompleteCustomClosedBatch(allState,b,true);
 Observe(o,t+86460,false);ok=BeginCustomClosedBatch("GBPUSD",t+86460,t+86460,o,state,b,reason);
 Check("reconnect_gap_not_fresh_anchor",ok && b.eventCount==1 && !b.events[0].continuousBoundary);CompleteCustomClosedBatch(state,b,true);
 Observe(o,t+86520,false);ok=BeginCustomClosedBatch("EURUSD",t+86520,t+86520,o,state,b,reason);Check("symbol_change_reprime",ok && b.eventCount==0);CompleteCustomClosedBatch(state,b,true);
 o[0].closedOpen=t;Check("clock_rollback_rejected",!BeginCustomClosedBatch("EURUSD",t+86520,t+86520,o,state,b,reason));
 Print("[CUSTOM-CLOCK-SUMMARY] passed=",passed," failed=",failed);return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
