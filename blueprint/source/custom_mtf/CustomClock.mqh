#ifndef BBMA_CUSTOM_CLOCK_V1
#define BBMA_CUSTOM_CLOCK_V1
#include "CustomSlot.mqh"
// Engineering event observation only; not owner maturity or execution consumption.
struct CustomClosedObservation {int timeframe;datetime closedOpen;datetime currentOpen;bool requested;bool barReady;};
struct CustomClosedEvent {int timeframe;datetime closedOpen;datetime currentOpen;bool continuousBoundary;};
struct CustomEventBatch {string symbol;datetime observedAt;long ticket;int eventCount;CustomClosedEvent events[7];CustomClosedObservation observations[7];};
struct CustomClockState {string symbol;bool busy;long ticket;string pendingSymbol;bool primed[7];datetime lastClosed[7];datetime lastOpen[7];};
bool BeginCustomClosedBatch(string symbol,datetime now,datetime quote,CustomClosedObservation &obs[],CustomClockState &state,CustomEventBatch &batch,string &reason)
{
 ZeroMemory(batch);reason="";
 if(state.busy){reason="CUSTOM_CLOCK_BUSY";return false;}
 if(StringLen(symbol)==0 || now<=0 || quote<=0 || quote>now){reason="WAIT_QUOTE";return false;}
 if(ArraySize(obs)!=7){reason="INVALID_CLOCK_OBSERVATIONS";return false;}
 bool seen[7];ArrayInitialize(seen,false);int requested=0;
 for(int i=0;i<7;i++)
 {
  int index=CustomTFIndex(obs[i].timeframe);
  if(index<0 || seen[index]){reason="INVALID_CLOCK_TIMEFRAME";return false;}
  seen[index]=true;
  if(!obs[i].requested)continue;
  requested++;
  int seconds=GetTimeframeSeconds(obs[i].timeframe);
  if(!obs[i].barReady || obs[i].closedOpen<=0 || obs[i].currentOpen<=0)
  {reason="WAIT_CLOSED_BAR_HISTORY";return false;}
  if(obs[i].currentOpen>now || obs[i].closedOpen>=obs[i].currentOpen || obs[i].closedOpen+seconds>now)
  {reason="BAR_NOT_CLOSED";return false;}
  if(quote<obs[i].currentOpen){reason="WAIT_QUOTE";return false;}
  if(state.symbol==symbol && state.primed[index] &&
     (obs[i].closedOpen<state.lastClosed[index] || obs[i].currentOpen<state.lastOpen[index]))
  {reason="CLOCK_ROLLBACK";return false;}
 }
 if(requested==0){reason="NO_REQUESTED_TIMEFRAME";return false;}
 batch.symbol=symbol;batch.observedAt=now;
 for(int copy=0;copy<7;copy++)batch.observations[copy]=obs[copy];
 // Canonical TF indices ascend; publish simultaneous closes high -> low.
 for(int tfIndex=6;tfIndex>=0;tfIndex--)
  for(int cell=0;cell<7;cell++)
  {
   if(!obs[cell].requested || CustomTFIndex(obs[cell].timeframe)!=tfIndex)continue;
   if(state.symbol!=symbol || !state.primed[tfIndex] || obs[cell].closedOpen==state.lastClosed[tfIndex])continue;
   int event=batch.eventCount++;
   batch.events[event].timeframe=obs[cell].timeframe;
   batch.events[event].closedOpen=obs[cell].closedOpen;batch.events[event].currentOpen=obs[cell].currentOpen;
   // Conservative continuity metadata, not a source entry-window rule.
   batch.events[event].continuousBoundary=(state.lastOpen[tfIndex]==obs[cell].closedOpen &&
                  obs[cell].closedOpen+GetTimeframeSeconds(obs[cell].timeframe)==obs[cell].currentOpen);
  }
 state.ticket++;batch.ticket=state.ticket;state.pendingSymbol=symbol;state.busy=true;
 return true;
}
bool CompleteCustomClosedBatch(CustomClockState &state,CustomEventBatch &batch,bool accepted)
{
 if(!state.busy || state.ticket!=batch.ticket || state.pendingSymbol!=batch.symbol)return false;
 if(accepted)
 {
  if(state.symbol!=batch.symbol)
  {ArrayInitialize(state.primed,false);ArrayInitialize(state.lastClosed,0);ArrayInitialize(state.lastOpen,0);}
  state.symbol=batch.symbol;
  for(int i=0;i<7;i++)
  {
   if(!batch.observations[i].requested)continue;
   int index=CustomTFIndex(batch.observations[i].timeframe);
   state.primed[index]=true;state.lastClosed[index]=batch.observations[i].closedOpen;state.lastOpen[index]=batch.observations[i].currentOpen;
  }
 }
 state.pendingSymbol="";state.busy=false;return true;
}
#endif
