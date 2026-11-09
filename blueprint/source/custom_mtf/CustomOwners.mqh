#ifndef BBMA_CUSTOM_OWNERS_V1
#define BBMA_CUSTOM_OWNERS_V1
// Read-only projection of canonical M08/M12 owners, never another lifecycle.
struct CustomOwnerView
{
 string symbol;string signal;string eventId;string reason;
 int timeframe;int direction;int ownerState;
 datetime sourceBar;datetime confirmation;datetime entryCandle;
 bool readable;bool structuralValid;bool recoveryOnly;bool entryWindowOpen;bool entryEligible;bool executionAvailable;
};
// Diagnostic counterpart of accepted Core 8.6 / PR301 EntryCandle equality.
// This does not change canonical candidates or grant custom eligibility.
bool CustomReEntryWindowOpen(ReEntryData &source,int tf,datetime currentOpen)
{
 if(source.State!=RE_STATE_CONFIRMED || !source.IsValid || source.Timeframe!=tf ||
    source.ConfirmationCandle<=0 || source.EntryCandle<=0 || currentOpen<=0)return false;
 int seconds=GetTimeframeSeconds(tf);
 return seconds>0 && source.EntryCandle==source.ConfirmationCandle+seconds && currentOpen==source.EntryCandle;
}
#define CUSTOM_OWNER_VIEW_CAP 154
struct CustomOwnerFrame {string symbol;datetime observedAt;int viewCount;CustomOwnerView views[CUSTOM_OWNER_VIEW_CAP];};
bool ProjectCustomReEntryView(string symbol,int tf,string signal,ENUM_DIRECTION direction,datetime latest,TimeframeData &data,ReEntryData &source,CustomOwnerView &view)
{
 view.recoveryOnly=false;view.entryWindowOpen=false;view.readable=false;view.structuralValid=false;view.entryEligible=false;view.executionAvailable=false;view.eventId="";
 view.ownerState=(int)source.State;view.entryCandle=source.EntryCandle;
 if(!data.is_valid || !data.is_closed || data.barIndex<1 || data.timeframe!=tf || data.candle_time!=latest || latest<=0)
 {view.reason="WAIT_OWNER_DATA";return false;}
 if(source.Timeframe!=tf || source.Direction!=direction || source.LastUpdateCandleTime!=latest)
 {view.reason="WAIT_OWNER_REFRESH";return false;}
 view.readable=true;view.sourceBar=latest;
 int requested=CustomSignalIndex(signal);
 if(requested>=1 && requested<=4 && (int)source.Type!=requested)
 {view.reason="RE_SUBTYPE_NOT_PRESENT";return true;}
 Signal exported;
 view.structuralValid=ExportConfirmedReEntrySignal(source,exported);
 if(view.structuralValid && exported.CandleTime>latest)view.structuralValid=false;
 if(view.structuralValid)
 {
  view.confirmation=exported.CandleTime;
  view.eventId=IntegerToString(StringLen(symbol))+":"+symbol+"|RE|"+IntegerToString(tf)+"|"+IntegerToString(direction)+"|"+IntegerToString(source.Type)+"|"+IntegerToString(source.StartCandleTime)+"|"+IntegerToString(source.ConfirmationCandle);
 }
 view.reason="READ_ONLY_M12_OWNER";
 // Entry-window diagnostic is assigned by the caller using actual current-bar identity.
 return true;
}
bool ProjectCustomExtremeView(string symbol,int tf,ENUM_DIRECTION direction,datetime latest,TimeframeData &data,ExtremeLifecycleData &source,CustomOwnerView &view)
{
 view.recoveryOnly=false;view.entryWindowOpen=false;view.readable=false;view.structuralValid=false;view.entryEligible=false;view.executionAvailable=false;view.eventId="";
 view.ownerState=(int)source.Maturity;view.entryCandle=source.RetestCompletionCandleTime;
 if(!data.is_valid || !data.is_closed || data.barIndex<1 || data.timeframe!=tf || data.candle_time!=latest || latest<=0)
 {view.reason="WAIT_OWNER_DATA";return false;}
 if(source.Timeframe!=tf || source.Direction!=direction || source.LastUpdateCandleTime!=latest)
 {view.reason="WAIT_OWNER_REFRESH";return false;}
 view.readable=true;view.sourceBar=latest;
 Signal exported;view.structuralValid=ExportReversalConfirmedExtremeSignal(source,exported);
 if(view.structuralValid && exported.CandleTime>latest)view.structuralValid=false;
 if(view.structuralValid)
 {
  view.confirmation=exported.CandleTime;
  view.eventId=IntegerToString(StringLen(symbol))+":"+symbol+"|EXT|"+IntegerToString(tf)+"|"+IntegerToString(direction)+"|"+IntegerToString(source.RawCandleTime)+"|"+IntegerToString(source.ConfirmationCandleTime);
 }
 view.reason="READ_ONLY_M08_OWNER";return true;
}
// MHV and MLV are views of the same canonical M09 owner, never independent signals.
bool ProjectCustomMHVView(string symbol,int tf,ENUM_DIRECTION direction,datetime latest,TimeframeData &data,MLVData &source,CustomOwnerView &view)
{
 view.recoveryOnly=false;view.entryWindowOpen=false;view.readable=false;view.structuralValid=false;
 view.entryEligible=false;view.executionAvailable=false;view.eventId="";
 view.ownerState=(int)source.State;
 if(CustomTFIndex(tf)<0){view.reason="TF_OWNER_UNWIRED";return false;}
 if(!data.is_valid || !data.is_closed || data.barIndex<1 || data.timeframe!=tf || data.candle_time!=latest || latest<=0)
 {view.reason="WAIT_OWNER_DATA";return false;}
 if(source.Timeframe!=tf || source.Direction!=direction || source.LastUpdateCandleTime!=latest)
 {view.reason="WAIT_OWNER_REFRESH";return false;}
 view.readable=true;view.sourceBar=latest;
 Signal exported;view.structuralValid=ExportSourceMHVSignal(source,exported);
 if(view.structuralValid && exported.CandleTime>latest)view.structuralValid=false;
 if(view.structuralValid)
 {
  view.confirmation=exported.CandleTime;
  view.eventId=IntegerToString(StringLen(symbol))+":"+symbol+"|MHV|"+IntegerToString(tf)+"|"+IntegerToString(direction)+"|"+IntegerToString(source.ParentRawCandleTime)+"|"+IntegerToString(source.StartCandleTime)+"|"+IntegerToString(source.ConfirmationCandleTime);
 }
 view.reason="READ_ONLY_M09_OWNER";return true;
}
#endif
