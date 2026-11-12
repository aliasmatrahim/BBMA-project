#ifndef BBMA_CUSTOM_DISPATCH_V1
#define BBMA_CUSTOM_DISPATCH_V1
#include "CustomInputs.mqh"
#include "CustomFreshEvents.mqh"
#define CUSTOM_DISPATCH_REV "CUSTOM_DISPATCH_DRAFT_001_20261112"

// Diagnostic T05 results only. No M15 selection, reservation or execution authority.
struct CustomSlotEvaluation
{
 int slotId;
 int direction;
 bool satisfied;
 string reason;
 CustomWitness witness;
};
struct CustomEvaluationSnapshot
{
 string symbol;
 datetime observedAt;
 long batchTicket;
 string configRevision; // Exact admitted payload includes every slot formula and symbol scope.
 int resultCount;
 CustomSlotEvaluation results[CUSTOM_SLOT_COUNT*2];
};

bool CustomEvaluationConfigurationCurrent(string expectedRevision,string &reason)
{
 reason="";
 if(expectedRevision=="" || g_custom_config_payload!=expectedRevision)
 {reason="WAIT_CONFIGURATION_REVISION";return false;}
 // Bound counts before canonical identity serialization dereferences parsed atoms.
 for(int slot=0;slot<CUSTOM_SLOT_COUNT;slot++)
 {
  if(g_custom_slots[slot].slotId!=slot+1 ||
     g_custom_slots[slot].context.atomCount<0 || g_custom_slots[slot].context.atomCount>CUSTOM_MAX_ATOMS ||
     g_custom_slots[slot].trigger.atomCount<0 || g_custom_slots[slot].trigger.atomCount>CUSTOM_MAX_ATOMS)
  {reason="INVALID_SLOT_CONFIGURATION";return false;}
 }
 if(BuildCustomResolvedConfigurationPayload()!=expectedRevision)
 {reason="WAIT_CONFIGURATION_REVISION";return false;}
 return true;
}

bool DispatchCustomEvaluationSnapshot(string actualSymbol,string expectedRevision,
                                      const CustomClockState &clock,const CustomEventBatch &batch,
                                      const CustomOwnerFrame &source,
                                      CustomEvaluationSnapshot &snapshot,string &reason)
{
 ZeroMemory(snapshot);reason="";
 if(!CustomEvaluationConfigurationCurrent(expectedRevision,reason))return false;
 if(actualSymbol=="" || !CustomContainsSymbol(g_custom_universe,actualSymbol) ||
    batch.symbol!=actualSymbol || source.symbol!=actualSymbol)
 {reason="INVALID_SNAPSHOT_SYMBOL";return false;}
 if(clock.busy || clock.symbol!=actualSymbol || clock.ticket!=batch.ticket ||
    batch.ticket<=0 || batch.eventCount<1 || batch.eventCount>7 ||
    batch.observedAt<=0 || source.observedAt!=batch.observedAt ||
    source.viewCount<1 || source.viewCount>CUSTOM_OWNER_VIEW_CAP)
 {reason="WAIT_COMMITTED_SNAPSHOT";return false;}
 // Receipt belongs to the accepted batch, never an aborted or old observation.
 for(int observation=0;observation<7;observation++)
 {
  if(!batch.observations[observation].requested)continue;
  int tf=CustomTFIndex(batch.observations[observation].timeframe);
  if(tf<0 || !clock.primed[tf] ||
     clock.lastClosed[tf]!=batch.observations[observation].closedOpen ||
     clock.lastOpen[tf]!=batch.observations[observation].currentOpen)
  {reason="WAIT_COMMITTED_SNAPSHOT";return false;}
 }
 CustomEvaluationSnapshot staged;ZeroMemory(staged);
 staged.symbol=actualSymbol;staged.observedAt=batch.observedAt;
 staged.batchTicket=batch.ticket;staged.configRevision=expectedRevision;
 for(int slotIndex=0;slotIndex<CUSTOM_SLOT_COUNT;slotIndex++)
 {
  if(!g_custom_slots[slotIndex].enabled)continue;
  CustomSlotConfig slot=g_custom_slots[slotIndex];
  for(int side=0;side<2;side++)
  {
   int result=staged.resultCount++;
   int direction=(side==0?DIR_BUY:DIR_SELL);
   staged.results[result].slotId=slot.slotId;
   staged.results[result].direction=direction;
   if(!CustomSlotUsesSymbol(slotIndex,actualSymbol))
   {staged.results[result].reason="SLOT_SYMBOL_EXCLUDED";continue;}
   if(!CustomCheckUse(slot.context,g_custom_use,staged.results[result].reason) ||
      !CustomCheckUse(slot.trigger,g_custom_use,staged.results[result].reason))continue;
   staged.results[result].satisfied=EvaluateCustomSlot(slot,batch,source,direction,
                                     staged.results[result].witness,staged.results[result].reason);
  }
 }
 if(!CustomEvaluationConfigurationCurrent(expectedRevision,reason))return false;
 snapshot=staged;return true;
}
#endif
