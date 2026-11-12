#ifndef BBMA_CUSTOM_EVALUATOR_V1
#define BBMA_CUSTOM_EVALUATOR_V1
// Draft consumer of immutable owner snapshots. Include after canonical owner types.
// No scheduler or execution caller is connected while T05 remains HOLD.
#include "CustomClock.mqh"
#include "CustomOwners.mqh"
#define CUSTOM_EVALUATOR_REV "CUSTOM_EVALUATOR_DRAFT_001_20261112"

struct CustomWitnessComponent
{
 CustomOwnerView owner;
 bool trigger;
 int group;
};
struct CustomWitness
{
 string symbol;
 int slotId;
 int direction;
 datetime observedAt;
 long batchTicket;
 int componentCount;
 CustomWitnessComponent components[CUSTOM_MAX_ATOMS];
 int anchorCount;
 string freshAnchors[CUSTOM_OWNER_VIEW_CAP];
 string selectedAnchor;
};

bool CustomAtomMatchesView(const CustomAtom &atom,const CustomOwnerView &view)
{
 if(atom.timeframe!=view.timeframe)return false;
 // Wildcards must resolve to an explicit subtype supplied by the owner adapter.
 if(atom.signal=="RE")
 {
  int subtype=CustomSignalIndex(view.signal);
  return subtype>=1 && subtype<=4;
 }
 return atom.signal==view.signal;
}

bool CustomViewCurrent(const CustomOwnerView &view,const CustomEventBatch &batch,
                       int direction,bool trigger)
{
 if(view.symbol!=batch.symbol || view.direction!=direction ||
    !view.readable || !view.structuralValid || !view.executionAvailable ||
    view.eventId=="" || view.sourceBar<=0 || view.confirmation<=0 ||
    view.confirmation>view.sourceBar)return false;
 if(trigger && (view.recoveryOnly || !view.entryEligible || !view.entryWindowOpen))return false;
 for(int index=0;index<7;index++)
 {
  if(batch.observations[index].timeframe!=view.timeframe)continue;
  return batch.observations[index].requested && batch.observations[index].barReady &&
         batch.observations[index].closedOpen==view.sourceBar &&
         batch.observations[index].currentOpen>view.sourceBar &&
         batch.observations[index].currentOpen<=batch.observedAt;
 }
 return false;
}

bool CustomViewFresh(const CustomOwnerView &view,const CustomEventBatch &batch,
                     const string &freshOwnerIds[])
{
 bool declared=false;
 for(int index=0;index<ArraySize(freshOwnerIds);index++)
  if(freshOwnerIds[index]==view.eventId){declared=true;break;}
 if(!declared)return false;
 for(int eventIndex=0;eventIndex<batch.eventCount;eventIndex++)
  if(batch.events[eventIndex].timeframe==view.timeframe &&
     batch.events[eventIndex].closedOpen==view.sourceBar &&
     batch.events[eventIndex].continuousBoundary)return true;
 return false;
}

bool CustomEarlierIdentity(const CustomOwnerView &left,const CustomOwnerView &right)
{
 if(left.confirmation!=right.confirmation)return left.confirmation<right.confirmation;
 if(left.timeframe!=right.timeframe)return left.timeframe<right.timeframe;
 int signalOrder=StringCompare(left.signal,right.signal);
 if(signalOrder!=0)return signalOrder<0;
 return StringCompare(left.eventId,right.eventId)<0;
}

bool CustomAddFreshAnchor(CustomWitness &witness,string eventId)
{
 for(int index=0;index<witness.anchorCount;index++)
  if(witness.freshAnchors[index]==eventId)return true;
 if(witness.anchorCount>=CUSTOM_OWNER_VIEW_CAP)return false;
 witness.freshAnchors[witness.anchorCount++]=eventId;
 return true;
}

bool CustomEvaluateGroups(const CustomFormula &formula,const CustomEventBatch &batch,
                          const CustomOwnerFrame &frame,const string &freshOwnerIds[],
                          int direction,bool trigger,CustomWitness &witness,string &reason)
{
 if(formula.atomCount<1 || formula.atomCount>CUSTOM_MAX_ATOMS ||
    formula.groupCount<1 || formula.groupCount>formula.atomCount)
 {reason="INVALID_PARSED_FORMULA";return false;}
 for(int atomIndex=0;atomIndex<formula.atomCount;atomIndex++)
  if(formula.atoms[atomIndex].group<0 || formula.atoms[atomIndex].group>=formula.groupCount ||
     CustomTFIndex(formula.atoms[atomIndex].timeframe)<0 ||
     !CustomKnownSignal(formula.atoms[atomIndex].signal))
  {reason="INVALID_PARSED_ATOM";return false;}
 int firstComponent=witness.componentCount;
 int freshReplacement=-1;
 int freshReplacementComponent=-1;
 for(int group=0;group<formula.groupCount;group++)
 {
  int selected=-1;
  for(int atom=0;atom<formula.atomCount;atom++)
  {
   if(formula.atoms[atom].group!=group)continue;
   for(int viewIndex=0;viewIndex<frame.viewCount;viewIndex++)
   {
    if(!CustomAtomMatchesView(formula.atoms[atom],frame.views[viewIndex]) ||
       !CustomViewCurrent(frame.views[viewIndex],batch,direction,trigger))continue;
    if(selected<0 || StringCompare(frame.views[viewIndex].eventId,frame.views[selected].eventId)<0)
     selected=viewIndex;
    if(trigger && CustomViewFresh(frame.views[viewIndex],batch,freshOwnerIds))
    {
     if(!CustomAddFreshAnchor(witness,frame.views[viewIndex].eventId))
     {reason="ANCHOR_CAPACITY";return false;}
     if(freshReplacement<0 || CustomEarlierIdentity(frame.views[viewIndex],frame.views[freshReplacement]))
     {freshReplacement=viewIndex;freshReplacementComponent=firstComponent+group;}
    }
   }
  }
  if(selected<0){reason=trigger?"WAIT_TRIGGER":"WAIT_CONTEXT";return false;}
  if(witness.componentCount>=CUSTOM_MAX_ATOMS){reason="WITNESS_CAPACITY";return false;}
  int component=witness.componentCount++;
  witness.components[component].owner=frame.views[selected];
  witness.components[component].trigger=trigger;
  witness.components[component].group=group;
 }
 if(trigger)
 {
  if(freshReplacement<0){reason="WAIT_FRESH_TRIGGER";return false;}
  // Choose a satisfying witness containing the deterministic fresh anchor.
  // Other simultaneous alternatives remain in freshAnchors for later reservation.
  witness.components[freshReplacementComponent].owner=frame.views[freshReplacement];
  witness.selectedAnchor=frame.views[freshReplacement].eventId;
 }
 return true;
}

bool EvaluateCustomSlotSnapshot(const CustomSlotConfig &slot,const CustomEventBatch &batch,
                                const CustomOwnerFrame &frame,const string &freshOwnerIds[],
                                int direction,CustomWitness &witness,string &reason)
{
 ZeroMemory(witness);reason="";
 if(!slot.enabled){reason="SLOT_DISABLED";return false;}
 if(slot.slotId<1 || slot.slotId>CUSTOM_SLOT_COUNT ||
    (direction!=DIR_BUY && direction!=DIR_SELL))
 {reason="INVALID_SLOT_KEY";return false;}
 if(batch.symbol=="" || batch.ticket<=0 || batch.observedAt<=0 ||
    batch.eventCount<1 || batch.eventCount>7 || frame.symbol!=batch.symbol ||
    frame.observedAt!=batch.observedAt || frame.viewCount<1 || frame.viewCount>CUSTOM_OWNER_VIEW_CAP)
 {reason="WAIT_CURRENT_OWNER_FRAME";return false;}
 if(slot.context.atomCount+slot.trigger.atomCount>CUSTOM_MAX_ATOMS)
 {reason="SLOT_TOO_MANY_ATOMS";return false;}
 CustomWitness staged;ZeroMemory(staged);
 staged.symbol=batch.symbol;staged.slotId=slot.slotId;staged.direction=direction;
 staged.observedAt=batch.observedAt;staged.batchTicket=batch.ticket;
 if(!CustomEvaluateGroups(slot.context,batch,frame,freshOwnerIds,direction,false,staged,reason) ||
    !CustomEvaluateGroups(slot.trigger,batch,frame,freshOwnerIds,direction,true,staged,reason))return false;
 // Canonical ordering makes reservations independent of incoming frame order.
 for(int left=0;left<staged.anchorCount-1;left++)
  for(int right=left+1;right<staged.anchorCount;right++)
   if(StringCompare(staged.freshAnchors[left],staged.freshAnchors[right])>0)
   {string temporary=staged.freshAnchors[left];staged.freshAnchors[left]=staged.freshAnchors[right];staged.freshAnchors[right]=temporary;}
 witness=staged;return true;
}

bool CustomWitnessContainsSource(const CustomWitness &witness,const CustomAtom &source)
{
 if(witness.componentCount<1 || witness.componentCount>CUSTOM_MAX_ATOMS)return false;
 for(int component=0;component<witness.componentCount;component++)
  if(CustomAtomMatchesView(source,witness.components[component].owner))return true;
 return false;
}
#endif
