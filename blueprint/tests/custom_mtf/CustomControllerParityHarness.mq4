#property strict
input bool MonitorRequested=false;
input bool SeedPending=false;
int capturedOrderAttempts=0;
int CaptureOrderSend(string pair,int direction,double lot,double price,int slip,double sl,double tp,string comment,int magic,datetime expiry,color arrow){capturedOrderAttempts++;return -1;}
#define OrderSend CaptureOrderSend
#define OnInit CanonicalOnInit
#define OnDeinit CanonicalOnDeinit
#define OnTick CanonicalOnTick
#define OnTimer CanonicalOnTimer
#ifdef CONTROLLER_BASELINE605
#include "..\\..\\source\\BBMA_EA_ParityBaseline605.mq4"
#else
#include "..\\..\\source\\BBMA_EA.mq4"
#endif
#undef OrderSend
#undef OnInit
#undef OnDeinit
#undef OnTick
#undef OnTimer
#include "CustomOwnerTestEquality.mqh"
int cycles=0,validDecisions=0,diagnosticFrames=0,seeds=0,handovers=0;
int csaViews=0;bool csaOK=true;
bool seeded=false,seedTF[3];
ExtremeLifecycleData expectedBuy[3],expectedSell[3];
MLVData expectedMHVBuy[3],expectedMHVSell[3];
bool finished=false;datetime startAt=0,endAt=0,lastStamp=0;
void Emit(string key,string value){Print("[CUSTOM-PARITY] ",IntegerToString((int)lastStamp),"|",key,"|",IntegerToString(StringLen(value)),":",value);}
void TraceDecision(string key,BBMA_Decision &value)
{
 Emit(key+".Valid",IntegerToString((int)value.Valid));
 Emit(key+".Direction",IntegerToString((int)value.Direction));
 Emit(key+".SignalType",IntegerToString((int)value.SignalType));
 Emit(key+".PriorityTier",IntegerToString((int)value.PriorityTier));
 Emit(key+".ComponentCount",IntegerToString((int)value.ComponentCount));
 Emit(key+".Components[0].ComponentType",IntegerToString((int)value.Components[0].ComponentType));
 Emit(key+".Components[0].Direction",IntegerToString((int)value.Components[0].Direction));
 Emit(key+".Components[0].Timeframe",IntegerToString((int)value.Components[0].Timeframe));
 Emit(key+".Components[0].CandleTime",IntegerToString((int)value.Components[0].CandleTime));
 Emit(key+".Components[0].DecisionID",value.Components[0].DecisionID);
 Emit(key+".Components[1].ComponentType",IntegerToString((int)value.Components[1].ComponentType));
 Emit(key+".Components[1].Direction",IntegerToString((int)value.Components[1].Direction));
 Emit(key+".Components[1].Timeframe",IntegerToString((int)value.Components[1].Timeframe));
 Emit(key+".Components[1].CandleTime",IntegerToString((int)value.Components[1].CandleTime));
 Emit(key+".Components[1].DecisionID",value.Components[1].DecisionID);
 Emit(key+".Components[2].ComponentType",IntegerToString((int)value.Components[2].ComponentType));
 Emit(key+".Components[2].Direction",IntegerToString((int)value.Components[2].Direction));
 Emit(key+".Components[2].Timeframe",IntegerToString((int)value.Components[2].Timeframe));
 Emit(key+".Components[2].CandleTime",IntegerToString((int)value.Components[2].CandleTime));
 Emit(key+".Components[2].DecisionID",value.Components[2].DecisionID);
 Emit(key+".CandidateExpiry",IntegerToString((int)value.CandidateExpiry));
 Emit(key+".HasSLTPSourceComponent",IntegerToString((int)value.HasSLTPSourceComponent));
 Emit(key+".SLTPSourceComponent.ComponentType",IntegerToString((int)value.SLTPSourceComponent.ComponentType));
 Emit(key+".SLTPSourceComponent.Direction",IntegerToString((int)value.SLTPSourceComponent.Direction));
 Emit(key+".SLTPSourceComponent.Timeframe",IntegerToString((int)value.SLTPSourceComponent.Timeframe));
 Emit(key+".SLTPSourceComponent.CandleTime",IntegerToString((int)value.SLTPSourceComponent.CandleTime));
 Emit(key+".SLTPSourceComponent.DecisionID",value.SLTPSourceComponent.DecisionID);
 Emit(key+".PatternValid",IntegerToString((int)value.PatternValid));
 Emit(key+".SequenceValid",IntegerToString((int)value.SequenceValid));
 Emit(key+".ExpiryBar",IntegerToString((int)value.ExpiryBar));
 Emit(key+".CandleTime",IntegerToString((int)value.CandleTime));
 Emit(key+".EntryPrice",DoubleToString(value.EntryPrice,16));
 Emit(key+".StopLoss",DoubleToString(value.StopLoss,16));
 Emit(key+".TakeProfit",DoubleToString(value.TakeProfit,16));
 Emit(key+".StopLossPoints",DoubleToString(value.StopLossPoints,16));
 Emit(key+".Reason",value.Reason);
 Emit(key+".SourceSequence",value.SourceSequence);
 Emit(key+".DecisionID",value.DecisionID);
 Emit(key+".SequenceHash",value.SequenceHash);
 Emit(key+".CycleStartTime",IntegerToString((int)value.CycleStartTime));
 Emit(key+".SLTPSource",IntegerToString((int)value.SLTPSource));
 Emit(key+".Pair",value.Pair);
 Emit(key+".D1OwnerState",IntegerToString((int)value.D1OwnerState));
 Emit(key+".D1OwnerDirection",IntegerToString((int)value.D1OwnerDirection));
 Emit(key+".D1OwnerCandleTime",IntegerToString((int)value.D1OwnerCandleTime));
 Emit(key+".D1OwnerClose",DoubleToString(value.D1OwnerClose,16));
 Emit(key+".D1OwnerMA50Current",DoubleToString(value.D1OwnerMA50Current,16));
 Emit(key+".D1OwnerMA50Previous",DoubleToString(value.D1OwnerMA50Previous,16));
 Emit(key+".D1OwnerSnapshotValid",IntegerToString((int)value.D1OwnerSnapshotValid));
 Emit(key+".D1AuthorityMode",IntegerToString((int)value.D1AuthorityMode));
 Emit(key+".D1OpportunityFamily",IntegerToString((int)value.D1OpportunityFamily));
 Emit(key+".D1OpportunityDirection",IntegerToString((int)value.D1OpportunityDirection));
 Emit(key+".D1OpportunitySourceSignal",IntegerToString((int)value.D1OpportunitySourceSignal));
 Emit(key+".D1OpportunitySourceCandleTime",IntegerToString((int)value.D1OpportunitySourceCandleTime));
 Emit(key+".D1OpportunityActivationTime",IntegerToString((int)value.D1OpportunityActivationTime));
 Emit(key+".D1OpportunityCycleID",value.D1OpportunityCycleID);
 Emit(key+".D1OpportunitySnapshotValid",IntegerToString((int)value.D1OpportunitySnapshotValid));
 Emit(key+".NMJESnapshotPresent",IntegerToString((int)value.NMJESnapshotPresent));
 Emit(key+".NMJEJourneyID",value.NMJEJourneyID);
 Emit(key+".NMJEParentEventID",value.NMJEParentEventID);
 Emit(key+".NMJERelation",IntegerToString((int)value.NMJERelation));
 Emit(key+".NMJEStableRelation",IntegerToString((int)value.NMJEStableRelation));
 Emit(key+".NMJEStableRelationEvidenceID",value.NMJEStableRelationEvidenceID);
 Emit(key+".NMJEParentTransitioned",IntegerToString((int)value.NMJEParentTransitioned));
 Emit(key+".NMJEPreviousParentEventID",value.NMJEPreviousParentEventID);
 Emit(key+".NMJELineageClass",IntegerToString((int)value.NMJELineageClass));
 Emit(key+".NMJELineageRootEventID",value.NMJELineageRootEventID);
 Emit(key+".NMJEPreviousLineageRootEventID",value.NMJEPreviousLineageRootEventID);
 Emit(key+".NMJEMaturity",IntegerToString((int)value.NMJEMaturity));
 Emit(key+".NMJEStructureDensity.Present",IntegerToString((int)value.NMJEStructureDensity.Present));
 Emit(key+".NMJEStructureDensity.Valid",IntegerToString((int)value.NMJEStructureDensity.Valid));
 Emit(key+".NMJEStructureDensity.StageMask",IntegerToString((int)value.NMJEStructureDensity.StageMask));
 Emit(key+".NMJEStructureDensity.PrefixMask",IntegerToString((int)value.NMJEStructureDensity.PrefixMask));
 Emit(key+".NMJEStructureDensity.StageCount",IntegerToString((int)value.NMJEStructureDensity.StageCount));
 Emit(key+".NMJEStructureDensity.Reason",value.NMJEStructureDensity.Reason);
 Emit(key+".NMJEUpdateCandleTime",IntegerToString((int)value.NMJEUpdateCandleTime));
 Emit(key+".NMJEM5SnapshotPresent",IntegerToString((int)value.NMJEM5SnapshotPresent));
 Emit(key+".NMJEM5ShadowEventID",value.NMJEM5ShadowEventID);
 Emit(key+".NMJEM5ShadowClosedCandleTime",IntegerToString((int)value.NMJEM5ShadowClosedCandleTime));
 Emit(key+".NMJEM5SemanticResolved",IntegerToString((int)value.NMJEM5SemanticResolved));
 Emit(key+".NMJEM5DiagnosticRelation",IntegerToString((int)value.NMJEM5DiagnosticRelation));
 Emit(key+".NMJEM5DiagnosticReason",value.NMJEM5DiagnosticReason);
 Emit(key+".C044LifecycleManaged",IntegerToString((int)value.C044LifecycleManaged));
 Emit(key+".D1TPWLifecycleManaged",IntegerToString((int)value.D1TPWLifecycleManaged));
 Emit(key+".DecisionState",IntegerToString((int)value.DecisionState));
 Emit(key+".RejectionReason",IntegerToString((int)value.RejectionReason));
}
void TraceM09(string key,MLVData &value)
{
 Emit(key+".State",IntegerToString((int)value.State));
 Emit(key+".Direction",IntegerToString((int)value.Direction));
 Emit(key+".ParentExtremeDirection",IntegerToString((int)value.ParentExtremeDirection));
 Emit(key+".Timeframe",IntegerToString((int)value.Timeframe));
 Emit(key+".Reason",value.Reason);
 Emit(key+".ParentRawCandleTime",IntegerToString((int)value.ParentRawCandleTime));
 Emit(key+".ParentConfirmationCandleTime",IntegerToString((int)value.ParentConfirmationCandleTime));
 Emit(key+".TPWajibCandleTime",IntegerToString((int)value.TPWajibCandleTime));
 Emit(key+".ProvisionalBodyAnchor",DoubleToString(value.ProvisionalBodyAnchor,16));
 Emit(key+".FrozenMarkedBody",DoubleToString(value.FrozenMarkedBody,16));
 Emit(key+".PreviousClose",DoubleToString(value.PreviousClose,16));
 Emit(key+".StartBar",IntegerToString((int)value.StartBar));
 Emit(key+".StartCandleTime",IntegerToString((int)value.StartCandleTime));
 Emit(key+".LastUpdateBar",IntegerToString((int)value.LastUpdateBar));
 Emit(key+".LastUpdateCandleTime",IntegerToString((int)value.LastUpdateCandleTime));
 Emit(key+".ConfirmationBar",IntegerToString((int)value.ConfirmationBar));
 Emit(key+".ConfirmationCandleTime",IntegerToString((int)value.ConfirmationCandleTime));
 Emit(key+".ConfirmationClose",DoubleToString(value.ConfirmationClose,16));
 Emit(key+".RetestBar",IntegerToString((int)value.RetestBar));
 Emit(key+".RetestCandleTime",IntegerToString((int)value.RetestCandleTime));
 Emit(key+".DirectionTakeoverBar",IntegerToString((int)value.DirectionTakeoverBar));
 Emit(key+".DirectionTakeoverCandleTime",IntegerToString((int)value.DirectionTakeoverCandleTime));
 Emit(key+".VoidBar",IntegerToString((int)value.VoidBar));
 Emit(key+".VoidCandleTime",IntegerToString((int)value.VoidCandleTime));
 Emit(key+".SupersededBar",IntegerToString((int)value.SupersededBar));
 Emit(key+".SupersededCandleTime",IntegerToString((int)value.SupersededCandleTime));
 Emit(key+".InvalidationWindowOpen",IntegerToString((int)value.InvalidationWindowOpen));
 Emit(key+".IsValid",IntegerToString((int)value.IsValid));
 Emit(key+".SupersessionCandidateActive",IntegerToString((int)value.SupersessionCandidateActive));
 Emit(key+".SupersessionRawBar",IntegerToString((int)value.SupersessionRawBar));
 Emit(key+".SupersessionRawCandleTime",IntegerToString((int)value.SupersessionRawCandleTime));
}
void TraceM12(string key,ReEntryData &value)
{
 Emit(key+".Type",IntegerToString((int)value.Type));
 Emit(key+".State",IntegerToString((int)value.State));
 Emit(key+".Direction",IntegerToString((int)value.Direction));
 Emit(key+".Timeframe",IntegerToString((int)value.Timeframe));
 Emit(key+".EntryPrice",DoubleToString(value.EntryPrice,16));
 Emit(key+".StopLoss",DoubleToString(value.StopLoss,16));
 Emit(key+".TakeProfit",DoubleToString(value.TakeProfit,16));
 Emit(key+".StopLossPoints",DoubleToString(value.StopLossPoints,16));
 Emit(key+".MA5_Level",DoubleToString(value.MA5_Level,16));
 Emit(key+".MA10_Level",DoubleToString(value.MA10_Level,16));
 Emit(key+".MA50_Level",DoubleToString(value.MA50_Level,16));
 Emit(key+".MID_BB",DoubleToString(value.MID_BB,16));
 Emit(key+".EntryCandle",IntegerToString((int)value.EntryCandle));
 Emit(key+".ConfirmationCandle",IntegerToString((int)value.ConfirmationCandle));
 Emit(key+".StartBar",IntegerToString((int)value.StartBar));
 Emit(key+".StartCandleTime",IntegerToString((int)value.StartCandleTime));
 Emit(key+".LastUpdateBar",IntegerToString((int)value.LastUpdateBar));
 Emit(key+".LastUpdateCandleTime",IntegerToString((int)value.LastUpdateCandleTime));
 Emit(key+".ConfirmationBar",IntegerToString((int)value.ConfirmationBar));
 Emit(key+".ExpiryBar",IntegerToString((int)value.ExpiryBar));
 Emit(key+".ExpiryCandleTime",IntegerToString((int)value.ExpiryCandleTime));
 Emit(key+".MinCandlesRequired",IntegerToString((int)value.MinCandlesRequired));
 Emit(key+".QualifyingCandles",IntegerToString((int)value.QualifyingCandles));
 Emit(key+".Type1ContextState",IntegerToString((int)value.Type1ContextState));
 Emit(key+".Type1OwnerSignal",IntegerToString((int)value.Type1OwnerSignal));
 Emit(key+".Type1OwnerCandleTime",IntegerToString((int)value.Type1OwnerCandleTime));
 Emit(key+".Type1RangingStartCandleTime",IntegerToString((int)value.Type1RangingStartCandleTime));
 Emit(key+".Type1PreviousClose",DoubleToString(value.Type1PreviousClose,16));
 Emit(key+".IsValid",IntegerToString((int)value.IsValid));
 Emit(key+".StrengthScore",DoubleToString(value.StrengthScore,16));
 Emit(key+".Reason",value.Reason);
}
void TraceM08(string key,ExtremeLifecycleData &value)
{
 Emit(key+".Maturity",IntegerToString((int)value.Maturity));
 Emit(key+".Direction",IntegerToString((int)value.Direction));
 Emit(key+".Timeframe",IntegerToString((int)value.Timeframe));
 Emit(key+".RawBar",IntegerToString((int)value.RawBar));
 Emit(key+".RawCandleTime",IntegerToString((int)value.RawCandleTime));
 Emit(key+".ConfirmationBar",IntegerToString((int)value.ConfirmationBar));
 Emit(key+".ConfirmationCandleTime",IntegerToString((int)value.ConfirmationCandleTime));
 Emit(key+".ConfirmationClose",DoubleToString(value.ConfirmationClose,16));
 Emit(key+".LastUpdateBar",IntegerToString((int)value.LastUpdateBar));
 Emit(key+".LastUpdateCandleTime",IntegerToString((int)value.LastUpdateCandleTime));
 Emit(key+".PreviousClose",DoubleToString(value.PreviousClose,16));
 Emit(key+".ProvisionalBodyAnchor",DoubleToString(value.ProvisionalBodyAnchor,16));
 Emit(key+".FrozenBodyAnchor",DoubleToString(value.FrozenBodyAnchor,16));
 Emit(key+".RelevantMA5",DoubleToString(value.RelevantMA5,16));
 Emit(key+".RetestStartBar",IntegerToString((int)value.RetestStartBar));
 Emit(key+".RetestStartCandleTime",IntegerToString((int)value.RetestStartCandleTime));
 Emit(key+".RetestCompletionBar",IntegerToString((int)value.RetestCompletionBar));
 Emit(key+".RetestCompletionCandleTime",IntegerToString((int)value.RetestCompletionCandleTime));
 Emit(key+".IsValid",IntegerToString((int)value.IsValid));
 Emit(key+".Reason",value.Reason);
}
void TraceD1Owner(string key,D1MajorTrendOwner &value)
{
 Emit(key+".State",IntegerToString((int)value.State));
 Emit(key+".Direction",IntegerToString((int)value.Direction));
 Emit(key+".SourceCandleTime",IntegerToString((int)value.SourceCandleTime));
 Emit(key+".EpochStartCandleTime",IntegerToString((int)value.EpochStartCandleTime));
 Emit(key+".LastProcessedD1CandleTime",IntegerToString((int)value.LastProcessedD1CandleTime));
 Emit(key+".Close1",DoubleToString(value.Close1,16));
 Emit(key+".MA50_1",DoubleToString(value.MA50_1,16));
 Emit(key+".MA50_2",DoubleToString(value.MA50_2,16));
 Emit(key+".IsValid",IntegerToString((int)value.IsValid));
 Emit(key+".Reason",value.Reason);
}
void TraceH4Owner(string key,H4DirectionalOwner &value)
{
 Emit(key+".State",IntegerToString((int)value.State));
 Emit(key+".Direction",IntegerToString((int)value.Direction));
 Emit(key+".SourceSignal",IntegerToString((int)value.SourceSignal));
 Emit(key+".SourceCandleTime",IntegerToString((int)value.SourceCandleTime));
 Emit(key+".LastAdvanceSignal",IntegerToString((int)value.LastAdvanceSignal));
 Emit(key+".LastAdvanceCandleTime",IntegerToString((int)value.LastAdvanceCandleTime));
 Emit(key+".LastProcessedH4CandleTime",IntegerToString((int)value.LastProcessedH4CandleTime));
 Emit(key+".IsValid",IntegerToString((int)value.IsValid));
 Emit(key+".RecoveryComplete",IntegerToString((int)value.RecoveryComplete));
 Emit(key+".RecoveredFromCheckpoint",IntegerToString((int)value.RecoveredFromCheckpoint));
 Emit(key+".Reason",value.Reason);
}


// Trusted owner fixtures on actual closed source OHLC. Not a cold-start claim.
void SeedControllerOwners()
{
 seeded=true;g_processing_time=GetProcessingTime();int frames[3]={PERIOD_D1,PERIOD_H4,PERIOD_H1};
 for(int i=0;i<3;i++)
 {
  int tf=frames[i];datetime latest=GetLatestClosedCandleTime(Symbol(),tf);
  TimeframeData data;if(!ReadCustomAuxClosedData(Symbol(),tf,latest,data))continue;
  datetime rawTime=iTime(Symbol(),tf,data.barIndex+4),confirmationTime=iTime(Symbol(),tf,data.barIndex+3);
  datetime formationTime=iTime(Symbol(),tf,data.barIndex+2),previousSourceTime=iTime(Symbol(),tf,data.barIndex+1);
  if(rawTime<=0 || rawTime>=confirmationTime || confirmationTime>=formationTime || formationTime>=previousSourceTime || previousSourceTime>=latest)continue;
  BollingerBand band;ZeroMemory(band);band.TOP_BB=data.bollinger[0];band.MID_BB=data.bollinger[1];band.LOW_BB=data.bollinger[2];band.Width=band.TOP_BB-band.LOW_BB;
  ENUM_DIRECTION parentDir=data.close>data.open?DIR_BUY:DIR_SELL;
  if(data.close==data.open || IsExtremeLifecycleInvalidation(Symbol(),parentDir,data,band))continue;
  CustomAuxLifecycle owner;ZeroMemory(owner);
  ResetExtremeLifecycle(owner.extremeBuy,DIR_BUY,tf);ResetExtremeLifecycle(owner.extremeSell,DIR_SELL,tf);
  owner.extremeBuy.LastUpdateCandleTime=latest;owner.extremeSell.LastUpdateCandleTime=latest;
  ExtremeLifecycleData parent=parentDir==DIR_BUY?owner.extremeBuy:owner.extremeSell;
  parent.Maturity=EXT_MAT_REVERSAL_CONFIRMED;parent.IsValid=true;parent.RawCandleTime=rawTime;parent.ConfirmationCandleTime=confirmationTime;
  parent.LastUpdateBar=data.barIndex;parent.PreviousClose=data.close;
  if(parentDir==DIR_BUY)owner.extremeBuy=parent;else owner.extremeSell=parent;
  MLVData pending;ZeroMemory(pending);pending.Direction=parentDir==DIR_BUY?DIR_SELL:DIR_BUY;pending.ParentExtremeDirection=parentDir;
  pending.Timeframe=tf;pending.State=MLV_DIRECTION_TAKEN;pending.IsValid=true;pending.ParentRawCandleTime=parent.RawCandleTime;pending.ParentConfirmationCandleTime=parent.ConfirmationCandleTime;
  pending.StartCandleTime=formationTime;pending.ConfirmationCandleTime=formationTime;pending.LastUpdateCandleTime=previousSourceTime;pending.FrozenMarkedBody=data.close;pending.PreviousClose=data.close;
  pending.SupersessionCandidateActive=true;pending.SupersessionRawCandleTime=previousSourceTime;
  if(pending.Direction==DIR_BUY)owner.mhvBuy=pending;else owner.mhvSell=pending;
  StoreCustomCanonicalSource(0,tf,data,owner);g_pair_states[0].canonical_mhv_observed[i]=false;
  CustomAuxLifecycle control=owner;AdvanceMHVSourceOwners(Symbol(),data,band,control.extremeBuy,control.extremeSell,control.mhvBuy,control.mhvSell,false);
  if(SameExtremeLifecycleData(owner.extremeBuy,control.extremeBuy) && SameExtremeLifecycleData(owner.extremeSell,control.extremeSell))continue;
  expectedBuy[i]=control.extremeBuy;expectedSell[i]=control.extremeSell;expectedMHVBuy[i]=control.mhvBuy;expectedMHVSell[i]=control.mhvSell;seedTF[i]=true;seeds++;
 }
}
void VerifyControllerHandover()
{
 int frames[3]={PERIOD_D1,PERIOD_H4,PERIOD_H1};
 for(int i=0;i<3;i++)if(seedTF[i])
 {
  TimeframeData data;CustomAuxLifecycle owner;LoadCustomCanonicalSource(0,frames[i],data,owner);
  if(SameExtremeLifecycleData(owner.extremeBuy,expectedBuy[i]) && SameExtremeLifecycleData(owner.extremeSell,expectedSell[i]) && SameMLVData(owner.mhvBuy,expectedMHVBuy[i]) && SameMLVData(owner.mhvSell,expectedMHVSell[i]))handovers++;
 }
}

int OnInit()
{
 // Each comparison case starts from the same empty fixture checkpoint.
 // Guard this test-only cleanup to the isolated GBPUSD tester identity.
 if(!IsTesting() || Symbol()!="GBPUSD" || InstanceID!=82)return INIT_FAILED;
 PairState bootstrap;ZeroMemory(bootstrap);bootstrap.base_symbol="GBPUSD";
 string prefix=H4OwnerGVBase(bootstrap);
 Print("[CUSTOM-PARITY-INIT] checkpointBefore=",GlobalVariableCheck(prefix+"T")," prefix=",prefix);
 ClearH4OwnerCheckpoint(bootstrap);GlobalVariablesFlush();
 Print("[CUSTOM-PARITY-INIT] checkpointAfter=",GlobalVariableCheck(prefix+"T"));
 int status=CanonicalOnInit();if(status!=INIT_SUCCEEDED)return status;
 if(g_pair_count!=1 || !g_pair_canonical_scope[0])return INIT_FAILED;
 ZeroMemory(g_custom_use);ArrayResize(g_custom_pair_indices,MonitorRequested?1:0);
 if(MonitorRequested)
 {
  g_custom_pair_indices[0]=0;
  for(int tf=0;tf<7;tf++){g_custom_use.tfEnabled[tf]=true;g_custom_use.signalEnabled[tf*11+6]=true;g_custom_use.signalEnabled[tf*11+7]=true;g_custom_use.signalEnabled[tf*11+10]=true;g_custom_use.signalEnabled[tf*11+8]=true;g_custom_use.signalEnabled[tf*11+9]=true;}
 }
 startAt=StringToTime(TimeToString(TimeCurrent(),TIME_DATE))+7200;endAt=startAt+14400;
 return INIT_SUCCEEDED;
}
void Finish()
{
 if(finished)return;finished=true;
 bool ok=cycles>=16 && (!SeedPending || (seeds>0 && handovers==seeds)) && OrdersTotal()==0 && OrdersHistoryTotal()==0 && (!MonitorRequested || (diagnosticFrames>0 && csaViews>0)) && csaOK;
 Print("[CUSTOM-PARITY-SUMMARY] cycles=",cycles," valid=",validDecisions," frames=",diagnosticFrames," attempts=",capturedOrderAttempts," seeds=",seeds," handovers=",handovers," csaViews=",csaViews," csaOK=",csaOK," ok=",ok);
}
void OnTick()
{
 if(TimeCurrent()<startAt)return;
 if(TimeCurrent()>=endAt){Finish();ExpertRemove();return;}
 if(SeedPending && !seeded)SeedControllerOwners();
 if(cycles%2==0)CanonicalOnTick();else CanonicalOnTimer();
 datetime stamp=g_processed_candle_time[0];if(stamp<=0 || stamp==lastStamp)return;
 lastStamp=stamp;cycles++;if(SeedPending && cycles==1)VerifyControllerHandover();
 if(MonitorRequested && cycles<=3)
 {
  Print("[CUSTOM-PARITY-DIAG] now=",TimeCurrent()," processing=",g_processing_time," quote=",(datetime)MarketInfo(Symbol(),MODE_TIME)," frame=",g_custom_owner_frames[0].viewCount);
  for(int q=0;q<7;q++)Print("[CUSTOM-PARITY-DIAG] tf=",CustomTFValue(q)," open=",iTime(Symbol(),CustomTFValue(q),0)," closed=",iTime(Symbol(),CustomTFValue(q),1)," primed=",g_custom_clock_states[0].primed[q]," last=",g_custom_clock_states[0].lastClosed[q]," mom=",g_pair_states[0].m10_momentum[q].ready);
 }
 if(g_pair_states[0].last_decision.Valid)validDecisions++;
 if(g_custom_owner_frames[0].viewCount>0)diagnosticFrames++;
#ifndef CONTROLLER_BASELINE605
 if(MonitorRequested && g_custom_owner_frames[0].viewCount>0)
 {
  int found=0;
  for(int v=0;v<g_custom_owner_frames[0].viewCount;v++)
  {
   CustomOwnerView view=g_custom_owner_frames[0].views[v];if(view.signal!="CSA" && view.signal!="CSAK")continue;
   found++;csaViews++;
   datetime latest=iTime(Symbol(),view.timeframe,1);
   double close=iClose(Symbol(),view.timeframe,1),mid=iMA(Symbol(),view.timeframe,20,0,MODE_SMA,PRICE_CLOSE,1);
   bool expected=view.direction==DIR_BUY?close>mid:close<mid;
   if(view.signal=="CSAK")
   {
    int price=view.direction==DIR_BUY?PRICE_HIGH:PRICE_LOW;
    double ma5=iMA(Symbol(),view.timeframe,5,0,MODE_LWMA,price,1),ma10=iMA(Symbol(),view.timeframe,10,0,MODE_LWMA,price,1);
    expected=expected && (view.direction==DIR_BUY?(close>ma5 && close>ma10):(close<ma5 && close<ma10));
   }
   if(!view.readable || view.sourceBar!=latest || view.structuralValid!=expected || !view.recoveryOnly || view.entryWindowOpen || view.entryEligible || view.executionAvailable || close<=0 || mid<=0)csaOK=false;
   if(expected && (view.confirmation!=latest || StringLen(view.eventId)==0))csaOK=false;
   if(!expected && (view.confirmation!=0 || StringLen(view.eventId)>0))csaOK=false;
  }
  if(found!=28)csaOK=false;
 }
#endif
 TraceDecision("Decision",g_pair_states[0].last_decision);
 TraceD1Owner("D1Owner",g_pair_states[0].d1_major_trend_owner);
 TraceH4Owner("H4Owner",g_pair_states[0].h4_direction_owner);
 int frames[4]={PERIOD_D1,PERIOD_H4,PERIOD_H1,PERIOD_M15};
 for(int t=0;t<4;t++)
 {
  TimeframeData data;CustomAuxLifecycle owner;LoadCustomCanonicalSource(0,frames[t],data,owner);
  string key=IntegerToString(frames[t]);
  TraceM08(key+"/BUY/M08",owner.extremeBuy);TraceM08(key+"/SELL/M08",owner.extremeSell);
  TraceM09(key+"/BUY/M09",owner.mhvBuy);TraceM09(key+"/SELL/M09",owner.mhvSell);
  TraceM12(key+"/BUY/M12",owner.reBuy);TraceM12(key+"/SELL/M12",owner.reSell);
 }
 Emit("Clock",IntegerToString((int)g_processed_candle_time[0]));
}
void OnDeinit(const int reason){Finish();CanonicalOnDeinit(reason);}
void OnTimer(){}
