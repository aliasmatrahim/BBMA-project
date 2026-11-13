#ifndef BBMA_CUSTOM_FRESH_EVENTS_V1
#define BBMA_CUSTOM_FRESH_EVENTS_V1
#include "CustomEvaluator.mqh"
#define CUSTOM_FRESH_EVENTS_REV "CUSTOM_FRESH_EVENTS_DRAFT_002_20261113"

// Read-only projections of M08/M12 source event metadata. They never grant execution availability.
bool CustomFreshReEntryEvent(const CustomOwnerView &view,const CustomEventBatch &batch)
{
 int subtype=CustomSignalIndex(view.signal);
 if(subtype<1 || subtype>4 || view.concreteSignal!=view.signal ||
    view.entryEventTime<=0 || view.entryEventTime!=view.confirmation ||
    !CustomViewCurrent(view,batch,view.direction,true))return false;
 for(int index=0;index<batch.eventCount;index++)
 {
  if(batch.events[index].timeframe!=view.timeframe)continue;
  return batch.events[index].continuousBoundary &&
         batch.events[index].closedOpen==view.entryEventTime &&
         batch.events[index].currentOpen==view.entryCandle &&
         batch.events[index].currentOpen<=batch.observedAt;
 }
 return false;
}

// A fresh EXT event requires the exact closed-bar retest-completion event. This physical
// event can be recorded while executionAvailable remains false; the evaluator still
// fails closed on owner availability and entry gates.
bool CustomFreshExtremeEvent(const CustomOwnerView &view,const CustomEventBatch &batch)
{
 if(CustomSignalIndex(view.signal)!=5 || view.concreteSignal!="EXT" ||
    !view.readable || !view.structuralValid || view.recoveryOnly ||
    view.ownerState!=(int)EXT_MAT_RETEST_READY || !view.entryEligible ||
    !view.entryWindowOpen || view.entryEventTime<=0 ||
    view.sourceBar!=view.entryEventTime || view.confirmation<=0 ||
    view.confirmation>view.sourceBar || view.eventId=="")return false;
 for(int index=0;index<batch.eventCount;index++)
 {
  if(batch.events[index].timeframe!=view.timeframe)continue;
  return batch.events[index].continuousBoundary &&
         batch.events[index].closedOpen==view.entryEventTime &&
         batch.events[index].currentOpen==view.entryCandle &&
         batch.events[index].currentOpen>view.entryEventTime &&
         batch.events[index].currentOpen<=batch.observedAt;
 }
 return false;
}

bool BuildCustomEvaluationInputs(const CustomEventBatch &batch,const CustomOwnerFrame &source,
                                 CustomOwnerFrame &frame,string &freshOwnerIds[],string &reason)
{
 ZeroMemory(frame);ArrayResize(freshOwnerIds,0);reason="";
 if(batch.symbol=="" || batch.ticket<=0 || batch.observedAt<=0 ||
    batch.eventCount<1 || batch.eventCount>7 || source.symbol!=batch.symbol ||
    source.observedAt!=batch.observedAt || source.viewCount<1 ||
    source.viewCount>CUSTOM_OWNER_VIEW_CAP)
 {reason="WAIT_CURRENT_OWNER_FRAME";return false;}
 CustomOwnerFrame staged=source;
 string fresh[];int freshCount=0;
 if(ArrayResize(fresh,source.viewCount)!=source.viewCount)
 {reason="FRESH_EVENT_ALLOCATION_FAILED";return false;}
 for(int index=0;index<source.viewCount;index++)
 {
  if(staged.views[index].symbol!=batch.symbol ||
     (staged.views[index].direction!=DIR_BUY && staged.views[index].direction!=DIR_SELL))
  {reason="INVALID_OWNER_KEY";return false;}
  int requested=CustomSignalIndex(staged.views[index].signal);
  if(requested<0 || CustomTFIndex(staged.views[index].timeframe)<0)
  {reason="UNRESOLVED_OWNER_TYPE";return false;}
  if(requested<=4 && staged.views[index].structuralValid)
  {
   int concrete=CustomSignalIndex(staged.views[index].concreteSignal);
   if(concrete<1 || concrete>4 || (requested!=0 && requested!=concrete))
   {reason="WAIT_CONCRETE_RE_OWNER";return false;}
   staged.views[index].signal=staged.views[index].concreteSignal;
  }
  if(!CustomFreshReEntryEvent(staged.views[index],batch) &&
     !CustomFreshExtremeEvent(staged.views[index],batch))continue;
  bool duplicate=false;
  for(int existing=0;existing<freshCount;existing++)
   if(fresh[existing]==staged.views[index].eventId){duplicate=true;break;}
  if(!duplicate)fresh[freshCount++]=staged.views[index].eventId;
 }
 if(ArrayResize(freshOwnerIds,freshCount)!=freshCount)
 {ArrayResize(freshOwnerIds,0);reason="FRESH_EVENT_ALLOCATION_FAILED";return false;}
 for(int item=0;item<freshCount;item++)freshOwnerIds[item]=fresh[item];
 frame=staged;return true;
}

// Scope/configuration revision and persistent consumption remain upstream owners.
// Non-RE trigger freshness stays unavailable until its source adapter is accepted.
bool EvaluateCustomSlot(const CustomSlotConfig &slot,const CustomEventBatch &batch,
                        const CustomOwnerFrame &source,int direction,
                        CustomWitness &witness,string &reason)
{
 ZeroMemory(witness);reason="";
 if(!slot.enabled){reason="SLOT_DISABLED";return false;}
 CustomOwnerFrame frame;string freshOwnerIds[];
 if(!BuildCustomEvaluationInputs(batch,source,frame,freshOwnerIds,reason))return false;
 return EvaluateCustomSlotSnapshot(slot,batch,frame,freshOwnerIds,direction,witness,reason);
}
#endif
