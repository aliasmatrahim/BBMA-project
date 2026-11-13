#ifndef BBMA_CUSTOM_M15_AUTHORITY_V1
#define BBMA_CUSTOM_M15_AUTHORITY_V1
#include "CustomDispatch.mqh"
#define CUSTOM_M15_AUTHORITY_REV "CUSTOM_M15_AUTHORITY_DRAFT_001_20261114"

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
 const CustomWitness &witness=row.witness;
 if(!row.satisfied || witness.symbol!=batch.symbol || witness.slotId!=row.slotId ||
    witness.direction!=row.direction || witness.observedAt!=batch.observedAt ||
    witness.batchTicket!=batch.ticket || witness.componentCount<1 ||
    witness.componentCount>CUSTOM_MAX_ATOMS || witness.anchorCount<1 ||
    witness.anchorCount>CUSTOM_OWNER_VIEW_CAP || witness.selectedAnchor=="")
 {reason="INVALID_CUSTOM_WITNESS";return false;}
 bool anchorListed=false;
 for(int item=0;item<witness.anchorCount;item++)
 {
  if(witness.freshAnchors[item]==""){reason="INVALID_FRESH_ANCHOR_LIST";return false;}
  if(witness.freshAnchors[item]==witness.selectedAnchor)anchorListed=true;
 }
 if(!anchorListed){reason="SELECTED_ANCHOR_NOT_FRESH";return false;}
 bool selectedTriggerFound=false;
 for(int component=0;component<witness.componentCount;component++)
 {
  if(witness.components[component].group<0){reason="INVALID_WITNESS_GROUP";return false;}
  if(witness.components[component].owner.symbol!=batch.symbol ||
     witness.components[component].owner.direction!=row.direction ||
     witness.components[component].owner.eventId=="")
  {reason="INVALID_WITNESS_OWNER";return false;}
  if(!CustomViewCurrent(witness.components[component].owner,batch,row.direction,
                        witness.components[component].trigger))
  {reason="WAIT_CURRENT_WITNESS_OWNER";return false;}
  if(witness.components[component].trigger &&
     witness.components[component].owner.eventId==witness.selectedAnchor)
  {
   if(!CustomM15FreshAnchorCurrent(witness.components[component].owner,batch,
                                   row.direction,reason))return false;
   anchor=witness.components[component].owner;
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
 CustomOwnerView bestAnchor;
 ZeroMemory(bestAnchor);
 bool sawBuy=false;bool sawSell=false;
 for(int rowIndex=0;rowIndex<evaluation.resultCount;rowIndex++)
 {
  const CustomSlotEvaluation &row=evaluation.results[rowIndex];
  if(!row.satisfied)continue;
  CustomOwnerView anchor;string validationReason;
  if(!CustomM15ValidateCandidate(row,batch,anchor,validationReason))
  {receipt.reason=validationReason;reason=validationReason;return false;}
  if(row.direction==DIR_BUY)sawBuy=true;
  if(row.direction==DIR_SELL)sawSell=true;
  if(row.direction!=d1Direction)continue;
  if(best<0 || CustomPreferredOwnerIdentity(anchor,bestAnchor,true) ||
     (anchor.eventId==bestAnchor.eventId && row.slotId<evaluation.results[best].slotId))
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

 const CustomSlotEvaluation &winner=evaluation.results[best];
 receipt.selected=true;
 receipt.executionAuthority=false;
 receipt.m16RevalidationRequired=true;
 receipt.direction=winner.direction;
 receipt.primarySlotId=winner.slotId;
 receipt.selectedAnchor=winner.witness.selectedAnchor;
 receipt.witness=winner.witness;
 for(int match=0;match<evaluation.resultCount;match++)
 {
  if(!evaluation.results[match].satisfied ||
     evaluation.results[match].direction!=winner.direction ||
     evaluation.results[match].witness.selectedAnchor!=receipt.selectedAnchor)continue;
  bool duplicate=false;
  for(int prior=0;prior<receipt.matchingSlotCount;prior++)
   if(receipt.matchingSlotIds[prior]==evaluation.results[match].slotId){duplicate=true;break;}
  if(duplicate)continue;
  if(receipt.matchingSlotCount>=CUSTOM_SLOT_COUNT)
  {receipt.selected=false;receipt.reason="MATCHING_SLOT_CAPACITY";reason=receipt.reason;return false;}
  receipt.matchingSlotIds[receipt.matchingSlotCount++]=evaluation.results[match].slotId;
 }
 receipt.reason="SELECTED_READ_ONLY";
 reason=receipt.reason;
 return receipt.matchingSlotCount>0;
}
#endif
