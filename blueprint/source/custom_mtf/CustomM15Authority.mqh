#ifndef BBMA_CUSTOM_M15_AUTHORITY_V1
#define BBMA_CUSTOM_M15_AUTHORITY_V1
#include "CustomDispatch.mqh"
#define CUSTOM_M15_AUTHORITY_REV "CUSTOM_M15_AUTHORITY_001_20261114"

struct CustomM15AuthorityReceipt
{
 string symbol;
 datetime observedAt;
 long batchTicket;
 string configRevision;
 bool selected;
 bool executionAuthority;
 bool m16RevalidationRequired;
 int direction;
 int primarySlotId;
 int matchingSlotCount;
 int matchingSlotIds[CUSTOM_SLOT_COUNT];
 string selectedAnchor;
 CustomWitness witness;
 D1MajorTrendOwner d1Owner;
 string reason;
};

datetime CustomM15PhysicalEventTime(const CustomOwnerView &view)
{
 if(view.entryEventTime>0)return view.entryEventTime;
 return view.sourceBar;
}

bool CustomM15BatchCommitted(const CustomClockState &clock,const CustomEventBatch &batch,
                             string &reason)
{
 reason="";
 if(clock.busy || clock.symbol!=batch.symbol || clock.ticket!=batch.ticket ||
    batch.symbol=="" || batch.ticket<=0 || batch.observedAt<=0 ||
    batch.eventCount<1 || batch.eventCount>7)
 {reason="WAIT_COMMITTED_BATCH";return false;}
 for(int index=0;index<7;index++)
 {
  if(!batch.observations[index].requested)continue;
  int tf=CustomTFIndex(batch.observations[index].timeframe);
  if(tf<0 || !clock.primed[tf] ||
     clock.lastClosed[tf]!=batch.observations[index].closedOpen ||
     clock.lastOpen[tf]!=batch.observations[index].currentOpen)
  {reason="WAIT_COMMITTED_BATCH";return false;}
 }
 return true;
}

bool CustomM15SnapshotBound(const CustomEvaluationSnapshot &evaluation,
                            const CustomEventBatch &batch,const CustomClockState &clock,
                            string expectedRevision,string &reason)
{
 reason="";
 if(!CustomEvaluationConfigurationCurrent(expectedRevision,reason))return false;
 if(!CustomM15BatchCommitted(clock,batch,reason))return false;
 if(evaluation.symbol!=batch.symbol || evaluation.observedAt!=batch.observedAt ||
    evaluation.batchTicket!=batch.ticket || evaluation.configRevision!=expectedRevision ||
    evaluation.resultCount<0 || evaluation.resultCount>CUSTOM_SLOT_COUNT*2)
 {reason="WAIT_CUSTOM_SNAPSHOT";return false;}
 bool seen[CUSTOM_SLOT_COUNT*2];ArrayInitialize(seen,false);
 for(int row=0;row<evaluation.resultCount;row++)
 {
  int slotId=evaluation.results[row].slotId;
  int direction=evaluation.results[row].direction;
  if(slotId<1 || slotId>CUSTOM_SLOT_COUNT ||
     (direction!=DIR_BUY && direction!=DIR_SELL))
  {reason="INVALID_CUSTOM_RESULT_KEY";return false;}
  int side=(direction==DIR_BUY?0:1);
  int key=(slotId-1)*2+side;
  if(seen[key]){reason="DUPLICATE_CUSTOM_RESULT_KEY";return false;}
  seen[key]=true;
 }
 return true;
}

bool CustomM15FreshAnchorCurrent(const CustomOwnerView &view,const CustomEventBatch &batch,
                                 int direction,string &reason)
{
 reason="";
 if(view.symbol!=batch.symbol || view.direction!=direction ||
    view.eventId=="" || view.sourceBar<=0 ||
    !CustomViewCurrent(view,batch,direction,true))
 {reason="WAIT_FRESH_TRIGGER_ANCHOR";return false;}
 datetime eventTime=CustomM15PhysicalEventTime(view);
 if(eventTime<=0 || eventTime>view.sourceBar)
 {reason="INVALID_FRESH_TRIGGER_TIME";return false;}
 for(int eventIndex=0;eventIndex<batch.eventCount;eventIndex++)
 {
  if(batch.events[eventIndex].timeframe!=view.timeframe ||
     batch.events[eventIndex].closedOpen!=view.sourceBar)continue;
  if(!batch.events[eventIndex].continuousBoundary)
  {reason="WAIT_CONTINUOUS_TRIGGER_BOUNDARY";return false;}
  return true;
 }
 reason="WAIT_FRESH_TRIGGER_BATCH_EVENT";return false;
}

bool CustomM15ValidateCandidate(const CustomSlotEvaluation &row,
                                const CustomEventBatch &batch,
                                CustomOwnerView &anchor,string &reason)
{
 ZeroMemory(anchor);reason="";
 if(!row.satisfied || row.witness.symbol!=batch.symbol ||
    row.witness.slotId!=row.slotId || row.witness.direction!=row.direction ||
    row.witness.observedAt!=batch.observedAt || row.witness.batchTicket!=batch.ticket ||
    row.witness.componentCount<1 || row.witness.componentCount>CUSTOM_MAX_ATOMS ||
    row.witness.anchorCount<1 || row.witness.anchorCount>CUSTOM_OWNER_VIEW_CAP ||
    row.witness.selectedAnchor=="")
 {reason="INVALID_CUSTOM_WITNESS";return false;}
 bool anchorListed=false;
 for(int item=0;item<row.witness.anchorCount;item++)
 {
  if(row.witness.freshAnchors[item]==""){reason="INVALID_FRESH_ANCHOR_LIST";return false;}
  for(int prior=0;prior<item;prior++)
   if(row.witness.freshAnchors[prior]==row.witness.freshAnchors[item])
   {reason="DUPLICATE_FRESH_ANCHOR";return false;}
  if(row.witness.freshAnchors[item]==row.witness.selectedAnchor)anchorListed=true;
 }
 if(!anchorListed){reason="SELECTED_ANCHOR_NOT_FRESH";return false;}
 bool selectedTriggerFound=false;
 for(int component=0;component<row.witness.componentCount;component++)
 {
  if(row.witness.components[component].group<0 ||
     row.witness.components[component].group>=CUSTOM_MAX_ATOMS)
  {reason="INVALID_WITNESS_GROUP";return false;}
  if(row.witness.components[component].owner.symbol!=batch.symbol ||
     row.witness.components[component].owner.direction!=row.direction ||
     row.witness.components[component].owner.eventId=="")
  {reason="INVALID_WITNESS_OWNER";return false;}
  if(!CustomViewCurrent(row.witness.components[component].owner,batch,row.direction,
                        row.witness.components[component].trigger))
  {reason="WAIT_CURRENT_WITNESS_OWNER";return false;}
  if(row.witness.components[component].trigger &&
     row.witness.components[component].owner.eventId==row.witness.selectedAnchor)
  {
   if(!CustomM15FreshAnchorCurrent(row.witness.components[component].owner,batch,
                                   row.direction,reason))return false;
   anchor=row.witness.components[component].owner;
   selectedTriggerFound=true;
  }
 }
 if(!selectedTriggerFound){reason="SELECTED_ANCHOR_NOT_IN_TRIGGER_WITNESS";return false;}
 return true;
}

bool CustomM15D1OwnerCurrent(const D1MajorTrendOwner &owner,datetime latestClosedD1,
                             int &direction,string &reason)
{
 direction=DIR_NONE;reason="WAIT_D1_OWNER";
 if(!owner.IsValid || latestClosedD1<=0 || owner.SourceCandleTime!=latestClosedD1 ||
    !MathIsValidNumber(owner.Close1) || !MathIsValidNumber(owner.MA50_1) ||
    !MathIsValidNumber(owner.MA50_2) || owner.Close1<=0 ||
    owner.MA50_1<=0 || owner.MA50_2<=0)return false;
 if(owner.State==D1_OWNER_BUY_CONFIRMED && owner.Direction==DIR_BUY)
 {direction=DIR_BUY;reason="";return true;}
 if(owner.State==D1_OWNER_SELL_CONFIRMED && owner.Direction==DIR_SELL)
 {direction=DIR_SELL;reason="";return true;}
 return false;
}

bool BuildCustomM15AuthorityReceipt(const CustomEvaluationSnapshot &evaluation,
                                    const CustomEventBatch &batch,
                                    const CustomClockState &clock,
                                    string expectedRevision,
                                    const D1MajorTrendOwner &d1Owner,
                                    datetime latestClosedD1,
                                    CustomM15AuthorityReceipt &receipt,string &reason)
{
 ZeroMemory(receipt);reason="";
 receipt.symbol=batch.symbol;
 receipt.observedAt=batch.observedAt;
 receipt.batchTicket=batch.ticket;
 receipt.executionAuthority=false;
 receipt.reason="WAIT_CUSTOM_M15_CANDIDATE";
 if(!CustomM15SnapshotBound(evaluation,batch,clock,expectedRevision,reason))
 {receipt.reason=reason;return false;}
 receipt.configRevision=evaluation.configRevision;
 int d1Direction=DIR_NONE;
 if(!CustomM15D1OwnerCurrent(d1Owner,latestClosedD1,d1Direction,reason))
 {receipt.reason=reason;return true;}
 receipt.d1Owner=d1Owner;

 int best=-1;
 CustomOwnerView bestAnchor;ZeroMemory(bestAnchor);
 bool sawBuy=false;bool sawSell=false;
 for(int rowIndex=0;rowIndex<evaluation.resultCount;rowIndex++)
 {
  if(!evaluation.results[rowIndex].satisfied)continue;
  int rowDirection=evaluation.results[rowIndex].direction;
  // Apply the M11 D1 direction filter before validating/arbitrating candidates.
  if(rowDirection!=d1Direction)continue;
  if(rowDirection==DIR_BUY)sawBuy=true;
  if(rowDirection==DIR_SELL)sawSell=true;
  CustomOwnerView anchor;string validationReason;
  if(!CustomM15ValidateCandidate(evaluation.results[rowIndex],batch,anchor,validationReason))
  {receipt.reason=validationReason;reason=validationReason;return false;}
  int rowSlotId=evaluation.results[rowIndex].slotId;
  int bestSlotId=(best<0?CUSTOM_SLOT_COUNT+1:evaluation.results[best].slotId);
  if(best<0 || CustomPreferredOwnerIdentity(anchor,bestAnchor,true) ||
     (anchor.eventId==bestAnchor.eventId && rowSlotId<bestSlotId))
  {
   best=rowIndex;bestAnchor=anchor;
  }
 }
 if(sawBuy && sawSell)
 {
  receipt.reason="CUSTOM_M15_DIRECTION_CONFLICT";
  reason=receipt.reason;
  return true;
 }
 if(best<0)
 {
  receipt.reason="WAIT_NO_D1_ALIGNED_CANDIDATE";
  reason=receipt.reason;
  return true;
 }

 receipt.direction=evaluation.results[best].direction;
 receipt.primarySlotId=evaluation.results[best].slotId;
 receipt.selectedAnchor=evaluation.results[best].witness.selectedAnchor;
 receipt.witness=evaluation.results[best].witness;
 receipt.d1Owner=d1Owner;
 for(int match=0;match<evaluation.resultCount;match++)
 {
  if(!evaluation.results[match].satisfied ||
     evaluation.results[match].direction!=receipt.direction ||
     evaluation.results[match].witness.selectedAnchor!=receipt.selectedAnchor)continue;
  int slotId=evaluation.results[match].slotId;
  int insertAt=receipt.matchingSlotCount;
  if(insertAt>=CUSTOM_SLOT_COUNT)
  {receipt.reason="MATCHING_SLOT_CAPACITY";reason=receipt.reason;return false;}
  while(insertAt>0 && receipt.matchingSlotIds[insertAt-1]>slotId)
  {
   receipt.matchingSlotIds[insertAt]=receipt.matchingSlotIds[insertAt-1];
   insertAt--;
  }
  receipt.matchingSlotIds[insertAt]=slotId;
  receipt.matchingSlotCount++;
 }
 if(receipt.matchingSlotCount<1)
 {receipt.reason="NO_MATCHING_SLOT_ATTRIBUTION";reason=receipt.reason;return false;}
 receipt.primarySlotId=receipt.matchingSlotIds[0];
 receipt.selected=true;
 receipt.executionAuthority=false;
 receipt.m16RevalidationRequired=true;
 receipt.reason="SELECTED_READ_ONLY";
 reason=receipt.reason;
 return true;
}
#endif
