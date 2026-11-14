#property strict
// Synthetic, read-only unit regression for the T05 evaluator and T06 M15 consumer.
// No live owner state, availability flag, trade request, or broker order is changed.
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
string revision="";
CustomEventBatch g_batch;
CustomClockState g_clockState;
CustomOwnerFrame g_frame;
CustomSlotConfig newSlot,oldSlot;
CustomWitness newWitness,oldWitness;
CustomEvaluationSnapshot g_evaluation;
D1MajorTrendOwner g_d1Owner;
string freshNew[2],freshOld[1];

void Check(string name,bool ok)
{
 if(ok)passed++;else failed++;
 Print("[T05-T06] ",name," ",ok?"PASS":"FAIL");
}

void SetView(CustomOwnerView &view,string signal,string eventId,int timeframe,int direction,
             datetime source,datetime confirmation,datetime physicalEvent,bool trigger)
{
 ZeroMemory(view);
 view.symbol="GBPUSD";
 view.signal=signal;
 view.concreteSignal=signal;
 view.eventId=eventId;
 view.timeframe=timeframe;
 view.direction=direction;
 view.ownerState=1;
 view.sourceBar=source;
 view.confirmation=confirmation;
 view.entryCandle=source+GetTimeframeSeconds(timeframe);
 view.entryEventTime=physicalEvent;
 view.readable=true;
 view.structuralValid=true;
 view.recoveryOnly=false;
 view.entryWindowOpen=trigger;
 view.entryEligible=trigger;
 view.executionAvailable=true;
}

void SetupBatch()
{
 ZeroMemory(g_batch);
 ZeroMemory(g_clockState);
 g_batch.symbol="GBPUSD";
 g_batch.observedAt=D'2026.08.03 10:00';
 g_batch.ticket=77;
 int tfs[7]={PERIOD_M1,PERIOD_M5,PERIOD_M15,PERIOD_M30,PERIOD_H1,PERIOD_H4,PERIOD_D1};
 for(int i=0;i<7;i++)
 {
  g_batch.observations[i].timeframe=tfs[i];
  g_batch.observations[i].requested=(i==0 || i==2 || i==4);
  g_batch.observations[i].barReady=true;
  g_batch.observations[i].currentOpen=g_batch.observedAt;
  g_batch.observations[i].closedOpen=g_batch.observedAt-GetTimeframeSeconds(tfs[i]);
  if(g_batch.observations[i].requested)
  {
   g_clockState.primed[i]=true;
   g_clockState.lastClosed[i]=g_batch.observations[i].closedOpen;
   g_clockState.lastOpen[i]=g_batch.observations[i].currentOpen;
  }
 }
 g_batch.eventCount=3;
 g_batch.events[0].timeframe=PERIOD_H1;
 g_batch.events[0].closedOpen=g_batch.observations[4].closedOpen;
 g_batch.events[0].currentOpen=g_batch.observedAt;
 g_batch.events[0].continuousBoundary=true;
 g_batch.events[1].timeframe=PERIOD_M15;
 g_batch.events[1].closedOpen=g_batch.observations[2].closedOpen;
 g_batch.events[1].currentOpen=g_batch.observedAt;
 g_batch.events[1].continuousBoundary=true;
 g_batch.events[2].timeframe=PERIOD_M1;
 g_batch.events[2].closedOpen=g_batch.observations[0].closedOpen;
 g_batch.events[2].currentOpen=g_batch.observedAt;
 g_batch.events[2].continuousBoundary=true;
 g_clockState.symbol=g_batch.symbol;
 g_clockState.ticket=g_batch.ticket;
 g_clockState.busy=false;
}

void SetupFrame()
{
 ZeroMemory(g_frame);
 g_frame.symbol=g_batch.symbol;
 g_frame.observedAt=g_batch.observedAt;
 g_frame.viewCount=4;
 SetView(g_frame.views[0],"RE1","CTX-M15",PERIOD_M15,DIR_BUY,
         g_batch.observations[2].closedOpen,g_batch.observations[2].closedOpen-900,0,false);
 SetView(g_frame.views[1],"EXT","TRIG-H1-OLD",PERIOD_H1,DIR_BUY,
         g_batch.observations[4].closedOpen,g_batch.observations[4].closedOpen-1800,
         g_batch.observations[4].closedOpen-60,true);
 SetView(g_frame.views[2],"RE1","TRIG-M1-OLD",PERIOD_M1,DIR_BUY,
         g_batch.observations[0].closedOpen,g_batch.observations[0].closedOpen-60,
         g_batch.observations[0].closedOpen-60,true);
 SetView(g_frame.views[3],"RE2","TRIG-M1-NEW",PERIOD_M1,DIR_BUY,
         g_batch.observations[0].closedOpen,g_batch.observations[0].closedOpen-60,
         g_batch.observations[0].closedOpen,true);
}

void SetRow(CustomSlotEvaluation &row,int slotId,int direction,CustomWitness &witness)
{
 ZeroMemory(row);
 row.slotId=slotId;
 row.direction=direction;
 row.satisfied=true;
 row.reason="SATISFIED";
 row.witness=witness;
 row.witness.slotId=slotId;
}

int OnInit()
{
 string reason="";
 bool initialized=InitializeCustomInputs(reason);
 Check("synthetic_configuration_initialized",initialized);
 if(!initialized){Print("[T05-T06-INIT] ",reason);return INIT_FAILED;}
 revision=g_custom_config_payload;
 SetupBatch();
 SetupFrame();

 CustomAtom alias;
 ZeroMemory(alias);
 alias.timeframe=PERIOD_M1;
 alias.signal="RE";
 bool allSubtypes=true;
 for(int subtype=1;subtype<=4;subtype++)
 {
  CustomOwnerView view;
  SetView(view,"RE"+IntegerToString(subtype),"RE-SUBTYPE-"+IntegerToString(subtype),
          PERIOD_M1,DIR_BUY,g_batch.observations[0].closedOpen,
          g_batch.observations[0].closedOpen-60,g_batch.observations[0].closedOpen,true);
  if(!CustomAtomMatchesView(alias,view))allSubtypes=false;
 }
 CustomOwnerView genericRe;
 SetView(genericRe,"RE","RE-GENERIC",PERIOD_M1,DIR_BUY,
         g_batch.observations[0].closedOpen,g_batch.observations[0].closedOpen-60,
         g_batch.observations[0].closedOpen,true);
 Check("RE_alias_resolves_only_subtypes_1_to_4",allSubtypes && !CustomAtomMatchesView(alias,genericRe));

 Check("trigger_order_uses_latest_physical_event",
       CustomPreferredOwnerIdentity(g_frame.views[3],g_frame.views[2],true));
 CustomOwnerView sameTimeH1,sameTimeM1;
 SetView(sameTimeH1,"EXT","H1-TIE",PERIOD_H1,DIR_BUY,
         g_batch.observations[4].closedOpen,g_batch.observations[4].closedOpen-60,
         g_batch.observations[4].closedOpen-60,true);
 SetView(sameTimeM1,"EXT","M1-TIE",PERIOD_M1,DIR_BUY,
         g_batch.observations[0].closedOpen,g_batch.observations[0].closedOpen-60,
         g_batch.observations[4].closedOpen-60,true);
 Check("trigger_tie_prefers_higher_timeframe",
       CustomPreferredOwnerIdentity(sameTimeH1,sameTimeM1,true));
 CustomOwnerView contextRecent,contextOld;
 SetView(contextRecent,"RE1","CTX-RECENT",PERIOD_M15,DIR_BUY,
         g_batch.observations[2].closedOpen,g_batch.observations[2].closedOpen-60,0,false);
 SetView(contextOld,"RE1","CTX-OLD",PERIOD_M15,DIR_BUY,
         g_batch.observations[2].closedOpen,g_batch.observations[2].closedOpen-120,0,false);
 Check("context_order_uses_latest_confirmation",
       CustomPreferredOwnerIdentity(contextRecent,contextOld,false));

 ZeroMemory(newSlot);
 newSlot.slotId=1;
 newSlot.enabled=true;
 bool parsedContext=ParseCustomFormula("M15:RE1 AND H1:EXT",newSlot.context,reason);
 bool parsedTrigger=ParseCustomFormula("M1:RE1 OR M1:RE2",newSlot.trigger,reason);
 Check("AND_OR_formula_parsed",parsedContext && parsedTrigger &&
       newSlot.context.groupCount==2 && newSlot.trigger.groupCount==1);
 freshNew[0]="TRIG-M1-OLD";
 freshNew[1]="TRIG-M1-NEW";
 bool evaluated=parsedContext && parsedTrigger &&
    EvaluateCustomSlotSnapshot(newSlot,g_batch,g_frame,freshNew,DIR_BUY,newWitness,reason);
 Check("T05_AND_context_OR_trigger_produces_witness",
       evaluated && newWitness.componentCount==3 && newWitness.anchorCount==2 &&
       newWitness.selectedAnchor=="TRIG-M1-NEW");
 if(!evaluated)Print("[T05-T06-T05-REASON] ",reason);

 // Build an older, valid H1 physical Trigger witness for T06 arbitration.
 ZeroMemory(oldSlot);
 oldSlot.slotId=3;
 oldSlot.enabled=true;
 bool oldParsed=ParseCustomFormula("M15:RE1",oldSlot.context,reason) &&
                ParseCustomFormula("H1:EXT",oldSlot.trigger,reason);
 freshOld[0]="TRIG-H1-OLD";
 bool oldEvaluated=oldParsed &&
    EvaluateCustomSlotSnapshot(oldSlot,g_batch,g_frame,freshOld,DIR_BUY,oldWitness,reason);
 Check("older_H1_trigger_witness_ready",
       oldEvaluated && oldWitness.selectedAnchor=="TRIG-H1-OLD");
 if(!oldEvaluated)Print("[T05-T06-OLD-REASON] ",reason);

 ZeroMemory(g_d1Owner);
 g_d1Owner.State=D1_OWNER_BUY_CONFIRMED;
 g_d1Owner.Direction=DIR_BUY;
 g_d1Owner.SourceCandleTime=D'2026.08.02 00:00';
 g_d1Owner.Close1=1.50000;
 g_d1Owner.MA50_1=1.40000;
 g_d1Owner.MA50_2=1.30000;
 g_d1Owner.IsValid=true;

 ZeroMemory(g_evaluation);
 g_evaluation.symbol=g_batch.symbol;
 g_evaluation.observedAt=g_batch.observedAt;
 g_evaluation.batchTicket=g_batch.ticket;
 g_evaluation.configRevision=revision;
 g_evaluation.resultCount=4;
 SetRow(g_evaluation.results[0],2,DIR_BUY,newWitness);
 SetRow(g_evaluation.results[1],1,DIR_BUY,newWitness);
 SetRow(g_evaluation.results[2],3,DIR_BUY,oldWitness);
 ZeroMemory(g_evaluation.results[3]);
 g_evaluation.results[3].slotId=4;
 g_evaluation.results[3].direction=DIR_SELL;
 g_evaluation.results[3].satisfied=true; // Deliberately malformed opposite side; D1 must filter it first.

 CustomM15AuthorityReceipt receipt;
 bool built=BuildCustomM15AuthorityReceipt(g_evaluation,g_batch,g_clockState,revision,g_d1Owner,
       g_d1Owner.SourceCandleTime,receipt,reason);
 Check("latest_physical_trigger_wins_and_opposite_D1_side_is_filtered",
       built && receipt.selected && receipt.selectedAnchor=="TRIG-M1-NEW");
 Check("same_anchor_primary_and_secondary_slots_are_stable",
       built && receipt.primarySlotId==1 && receipt.matchingSlotCount==2 &&
       receipt.matchingSlotIds[0]==1 && receipt.matchingSlotIds[1]==2);
 Check("selection_is_read_only_and_requires_M16",
       built && !receipt.executionAuthority && receipt.m16RevalidationRequired &&
       receipt.reason=="SELECTED_READ_ONLY");
 if(!built || !receipt.selected)Print("[T05-T06-SELECT-REASON] ",reason);

 D1MajorTrendOwner stale=g_d1Owner;
 stale.SourceCandleTime=g_d1Owner.SourceCandleTime-86400;
 bool staleResult=BuildCustomM15AuthorityReceipt(g_evaluation,g_batch,g_clockState,revision,
       stale,g_d1Owner.SourceCandleTime,receipt,reason);
 Check("stale_D1_fails_closed",staleResult && !receipt.selected && receipt.reason=="WAIT_D1_OWNER");

 string wrongRevision=revision+"STALE";
 bool revisionResult=BuildCustomM15AuthorityReceipt(g_evaluation,g_batch,g_clockState,wrongRevision,
       g_d1Owner,g_d1Owner.SourceCandleTime,receipt,reason);
 Check("stale_configuration_revision_fails_closed",
       !revisionResult && !receipt.selected && receipt.reason=="WAIT_CONFIGURATION_REVISION");

 g_batch.events[2].continuousBoundary=false;
 bool gapResult=BuildCustomM15AuthorityReceipt(g_evaluation,g_batch,g_clockState,revision,
       g_d1Owner,g_d1Owner.SourceCandleTime,receipt,reason);
 Check("recovery_gap_cannot_create_fresh_anchor",
       !gapResult && !receipt.selected && receipt.reason=="WAIT_CONTINUOUS_TRIGGER_BOUNDARY");
 g_batch.events[2].continuousBoundary=true;

 g_evaluation.results[1].slotId=2; // Duplicate (slot, direction) key must fail before arbitration.
 bool duplicateResult=BuildCustomM15AuthorityReceipt(g_evaluation,g_batch,g_clockState,revision,
       g_d1Owner,g_d1Owner.SourceCandleTime,receipt,reason);
 Check("duplicate_result_key_fails_closed",
       !duplicateResult && !receipt.selected && receipt.reason=="DUPLICATE_CUSTOM_RESULT_KEY");

 Check("no_broker_orders",OrdersTotal()==0 && OrdersHistoryTotal()==0);
 Print("[T05-T06-SUMMARY] passed=",passed," failed=",failed);
 return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}

void OnTick() {}
