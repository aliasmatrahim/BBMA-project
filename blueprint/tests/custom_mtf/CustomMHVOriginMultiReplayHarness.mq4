#property strict
input bool OriginReplayConsumer=false;
input int OriginSourceTF=15;
input int OriginCandidateEpoch=0;
input bool OriginCandidateIsBuy=true;
// Diagnostic inventory on installed history; no platform price fixtures or trading.
#define OnInit CanonicalOnInit
#define OnDeinit CanonicalOnDeinit
#define OnTick CanonicalOnTick
#define OnTimer CanonicalOnTimer
#include "..\\..\\source\\BBMA_EA.mq4"
#undef OnInit
#undef OnDeinit
#undef OnTick
#undef OnTimer
#include "CustomOwnerTestEquality.mqh"
struct OriginOwners {ExtremeLifecycleData buy;ExtremeLifecycleData sell;MLVData mhvBuy;MLVData mhvSell;};
void SeedHypothesis(OriginOwners &x,int tf,datetime before,double close,int scenario)
{
 ZeroMemory(x);ResetExtremeLifecycle(x.buy,DIR_BUY,tf);ResetExtremeLifecycle(x.sell,DIR_SELL,tf);ResetMLVState(x.mhvBuy,DIR_BUY,tf);ResetMLVState(x.mhvSell,DIR_SELL,tf);
 if(scenario==0)return;
 x.buy.Maturity=scenario==1?EXT_MAT_REVERSAL_CONFIRMED:(scenario==2?EXT_MAT_RAW:EXT_MAT_RETEST_READY);x.sell.Maturity=x.buy.Maturity;
 x.buy.IsValid=scenario!=2;x.sell.IsValid=x.buy.IsValid;
 x.buy.RawCandleTime=before-3*tf*60;x.sell.RawCandleTime=x.buy.RawCandleTime;
 x.buy.ConfirmationCandleTime=scenario==2?0:before-2*tf*60;x.sell.ConfirmationCandleTime=x.buy.ConfirmationCandleTime;
 x.buy.LastUpdateCandleTime=before;x.sell.LastUpdateCandleTime=before;x.buy.PreviousClose=close;x.sell.PreviousClose=close;
 x.buy.ProvisionalBodyAnchor=close;x.sell.ProvisionalBodyAnchor=close;x.buy.FrozenBodyAnchor=close;x.sell.FrozenBodyAnchor=close;
 x.mhvBuy.State=scenario==1?MLV_DIRECTION_TAKEN:(scenario==2?MLV_LOSS_DEVELOPING:MLV_RETEST_COMPLETE);x.mhvSell.State=x.mhvBuy.State;
 x.mhvBuy.IsValid=scenario!=2;x.mhvSell.IsValid=x.mhvBuy.IsValid;
 x.mhvBuy.ParentRawCandleTime=before-3*tf*60;x.mhvSell.ParentRawCandleTime=x.mhvBuy.ParentRawCandleTime;
 x.mhvBuy.ParentConfirmationCandleTime=before-2*tf*60;x.mhvSell.ParentConfirmationCandleTime=x.mhvBuy.ParentConfirmationCandleTime;
 x.mhvBuy.ConfirmationCandleTime=before-tf*60;x.mhvSell.ConfirmationCandleTime=x.mhvBuy.ConfirmationCandleTime;
 x.mhvBuy.LastUpdateCandleTime=before;x.mhvSell.LastUpdateCandleTime=before;x.mhvBuy.PreviousClose=close;x.mhvSell.PreviousClose=close;
 x.mhvBuy.ProvisionalBodyAnchor=close;x.mhvSell.ProvisionalBodyAnchor=close;x.mhvBuy.FrozenMarkedBody=close;x.mhvSell.FrozenMarkedBody=close;
 x.mhvBuy.ParentExtremeDirection=DIR_SELL;x.mhvSell.ParentExtremeDirection=DIR_BUY;x.mhvBuy.InvalidationWindowOpen=scenario!=1;x.mhvSell.InvalidationWindowOpen=x.mhvBuy.InvalidationWindowOpen;
}
bool SameOrigin(OriginOwners &a,OriginOwners &b)
{return SameExtremeLifecycleData(a.buy,b.buy) && SameExtremeLifecycleData(a.sell,b.sell) && SameMLVData(a.mhvBuy,b.mhvBuy) && SameMLVData(a.mhvSell,b.mhvSell);}
bool AdvanceOrigin(OriginOwners &x,TimeframeData &d,BollingerBand &bb,bool rawBuy,bool rawSell)
{
 UpdateExtremeLifecycle(x.buy,Symbol(),DIR_BUY,d,bb,rawBuy);UpdateExtremeLifecycle(x.sell,Symbol(),DIR_SELL,d,bb,rawSell);
 ResolveOppositeExtremeSupersession(x.buy,x.sell,d);
 return AdvanceMHVSourceOwners(Symbol(),d,bb,x.buy,x.sell,x.mhvBuy,x.mhvSell,false);
}
bool CandidateChain(MLVData &m,datetime reset)
{return reset>0 && IsCanonicalMLVMatureState(m.State) && m.IsValid && m.ParentRawCandleTime>reset && m.ParentConfirmationCandleTime>m.ParentRawCandleTime && m.TPWajibCandleTime>m.ParentConfirmationCandleTime && m.ConfirmationCandleTime>m.TPWajibCandleTime;}

#include "CustomMHVOriginCodec.mqh"
datetime OriginAnchor=0;
ENUM_DIRECTION OriginDirection=DIR_BUY;
int OriginTF=PERIOD_M15;
const int OriginSteps=24;
string OriginCheckpointFile="sig06_mhv_origin_checkpoint_v3_20261111.csv";
int checks=0,failures=0;
void OriginCheck(string label,bool ok){checks++;if(!ok)failures++;Print("[MHV-RESTART] ",label," ",ok?"PASS":"FAIL");}
bool OriginData(datetime stamp,TimeframeData &d,BollingerBand &bb,bool &rawBuy,bool &rawSell)
{
 GetDataForTimeframe(Symbol(),OriginTF,stamp,d);M10MomentumSnapshot m;
 if(!ReadM10MomentumSource(Symbol(),d,m))return false;
 ZeroMemory(bb);bb.TOP_BB=d.bollinger[0];bb.MID_BB=d.bollinger[1];bb.LOW_BB=d.bollinger[2];bb.Width=bb.TOP_BB-bb.LOW_BB;
 rawBuy=DetectExtreme(Symbol(),DIR_BUY,d,bb);rawSell=DetectExtreme(Symbol(),DIR_SELL,d,bb);return true;
}
bool ProduceOrigin()
{
 int oldest=(int)MathMin(600,iBars(Symbol(),OriginTF)-51);OriginOwners states[4],checkpoint;datetime previous=0,reset=0,firstReset=0;bool initialized=false,found=false;
 for(int sh=oldest;sh>=1;sh--)
 {
  datetime stamp=iTime(Symbol(),OriginTF,sh);if(OriginAnchor>0 && stamp>OriginAnchor)break;
  TimeframeData d;BollingerBand bb;bool rb=false,rs=false;if(!OriginData(stamp,d,bb,rb,rs)){initialized=false;previous=0;reset=0;firstReset=0;continue;}
  if(!initialized || stamp!=previous+OriginTF*60)
  {for(int k=0;k<4;k++)SeedHypothesis(states[k],OriginTF,stamp-OriginTF*60,d.close,k);initialized=true;reset=0;firstReset=0;}
  M10MomentumSnapshot m;if(!ReadM10MomentumSource(Symbol(),d,m))return false;
  if(m.buy || m.sell){reset=stamp;if(firstReset==0)firstReset=stamp;}
  for(int k=0;k<4;k++)if(!AdvanceOrigin(states[k],d,bb,rb,rs))return false;
  if(OriginAnchor==0)
  {
   bool same=SameOrigin(states[0],states[1]) && SameOrigin(states[0],states[2]) && SameOrigin(states[0],states[3]);
   bool sourceOrigins=firstReset>0 && states[0].buy.RawCandleTime>firstReset && states[0].sell.RawCandleTime>firstReset && states[0].mhvBuy.ParentRawCandleTime>firstReset && states[0].mhvSell.ParentRawCandleTime>firstReset;
   bool buyChain=CandidateChain(states[0].mhvBuy,reset),sellChain=CandidateChain(states[0].mhvSell,reset),room=true;
   if(same && sourceOrigins && (buyChain || sellChain))
   {
    for(int step=1;step<=OriginSteps;step++)if(iBarShift(Symbol(),OriginTF,stamp+step*OriginTF*60,true)<1)room=false;
    if(room){OriginAnchor=stamp;OriginDirection=buyChain?DIR_BUY:DIR_SELL;Print("[MHV-RESTART-SELECT] tf=",OriginTF," anchor=",(int)OriginAnchor," buy=",OriginDirection==DIR_BUY);}
   }
  }
  if(stamp==OriginAnchor)
  {
   bool same=SameOrigin(states[0],states[1]) && SameOrigin(states[0],states[2]) && SameOrigin(states[0],states[3]);
   OriginCheck("four_hypotheses_converge_at_anchor",same);
   MLVData selected=OriginDirection==DIR_BUY?states[0].mhvBuy:states[0].mhvSell;
   OriginCheck("natural_selected_parent_TPW_formation_after_Momentum",CandidateChain(selected,reset));
   OriginCheck("first_reset_precedes_both_M08_raws",firstReset>0 && states[0].buy.RawCandleTime>firstReset && states[0].sell.RawCandleTime>firstReset);
   OriginCheck("both_M09_parent_origins_after_first_reset",firstReset>0 && states[0].mhvBuy.ParentRawCandleTime>firstReset && states[0].mhvSell.ParentRawCandleTime>firstReset);
   Print("[MHV-RESTART-WITNESS] firstReset=",firstReset," lastMomentum=",reset," buyRaw=",states[0].buy.RawCandleTime," sellRaw=",states[0].sell.RawCandleTime," buyParentRaw=",states[0].mhvBuy.ParentRawCandleTime," sellParentRaw=",states[0].mhvSell.ParentRawCandleTime," reversal=",states[0].mhvBuy.ParentConfirmationCandleTime," tpw=",states[0].mhvBuy.TPWajibCandleTime," formation=",states[0].mhvBuy.ConfirmationCandleTime);
   if(!same || !CandidateChain(selected,reset))return false;
   checkpoint=states[0];found=true;break;
  }
  previous=stamp;
 }
 if(!found)return false;
 int h=FileOpen(OriginCheckpointFile,FILE_WRITE|FILE_CSV|FILE_ANSI,';');if(h==INVALID_HANDLE)return false;
 bool ok=FileWrite(h,"source","a62672ae1874fcbf61c671af01da09ef45ffe6972abd998ec70c5f9a74c238cb")>0 && FileWrite(h,"tf",IntegerToString(OriginTF))>0 && FileWrite(h,"anchor",IntegerToString((int)OriginAnchor))>0;
 ok=ok && WriteOriginSnapshot(h,"anchor",checkpoint);
 OriginOwners continuous=checkpoint;
 for(int step=1;step<=OriginSteps && ok;step++)
 {
  datetime stamp=OriginAnchor+step*OriginTF*60;TimeframeData d;BollingerBand bb;bool rb=false,rs=false;
  if(iBarShift(Symbol(),OriginTF,stamp,true)<1 || !OriginData(stamp,d,bb,rb,rs)){ok=false;break;}
  if(!AdvanceOrigin(continuous,d,bb,rb,rs)){ok=false;break;}
  ok=WriteOriginSnapshot(h,"step"+IntegerToString(step),continuous);
 }
 FileFlush(h);FileClose(h);OriginCheck("persist_anchor_and_24_continuous_states",ok);
 return ok;
}
bool ConsumeOrigin()
{
 int h=FileOpen(OriginCheckpointFile,FILE_READ|FILE_CSV|FILE_ANSI,';');if(h==INVALID_HANDLE)return false;
 string v;bool header=OriginReadKey(h,"source",v) && v=="a62672ae1874fcbf61c671af01da09ef45ffe6972abd998ec70c5f9a74c238cb";
 header=header && OriginReadKey(h,"tf",v) && StringToInteger(v)==OriginTF;
 header=header && OriginReadKey(h,"anchor",v) && (datetime)StringToInteger(v)==OriginAnchor;
 OriginCheck("fresh_terminal_snapshot_identity",header);if(!header){FileClose(h);return false;}
 OriginOwners recovered,expected;bool loaded=ReadOriginSnapshot(h,"anchor",recovered);OriginCheck("read_full_M08_M09_snapshot",loaded);
 if(!loaded){FileClose(h);return false;}
 for(int step=1;step<=OriginSteps;step++)
 {
  bool row=ReadOriginSnapshot(h,"step"+IntegerToString(step),expected);if(!row){FileClose(h);return false;}
  datetime stamp=OriginAnchor+step*OriginTF*60;TimeframeData d;BollingerBand bb;bool rb=false,rs=false;
  bool advanced=OriginData(stamp,d,bb,rb,rs) && AdvanceOrigin(recovered,d,bb,rb,rs);
  OriginCheck("recovered_equals_continuous_full_state_"+IntegerToString(step),advanced && SameOrigin(recovered,expected));
 }
 bool end=FileIsEnding(h);FileClose(h);OriginCheck("snapshot_has_no_extra_records",end);return failures==0;
}
int OnInit()
{
 OriginTF=OriginSourceTF;OriginAnchor=(datetime)OriginCandidateEpoch;OriginDirection=OriginCandidateIsBuy?DIR_BUY:DIR_SELL;OriginCheckpointFile="sig06_mhv_origin_checkpoint_multi_v4_"+IntegerToString(OriginTF)+".csv";
 g_pair_count=0;g_processing_time=TimeCurrent();bool ok=OriginReplayConsumer?ConsumeOrigin():ProduceOrigin();
 OriginCheck("no_broker_orders",OrdersTotal()==0 && OrdersHistoryTotal()==0);
 Print("[MHV-RESTART-SUMMARY] mode=",OriginReplayConsumer?"consume":"produce"," checks=",checks," failed=",failures," ok=",ok," acceptance=BOUNDED_ENGINEERING_ONLY");
 return ok && failures==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
void OnTimer(){}
void OnDeinit(const int reason){}
