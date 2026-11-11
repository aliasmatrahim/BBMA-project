#property strict
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
int OnInit()
{
 g_pair_count=0;g_processing_time=TimeCurrent();
 int inputFile=FileOpen("sig06_mhv_origin_inputs_v1_20261111.csv",FILE_WRITE|FILE_CSV|FILE_ANSI,';');
 int eventFile=FileOpen("sig06_mhv_origin_candidates_v1_20261111.csv",FILE_WRITE|FILE_CSV|FILE_ANSI,';');
 if(inputFile==INVALID_HANDLE || eventFile==INVALID_HANDLE)return INIT_FAILED;
 FileWrite(inputFile,"tf","time","shift","open","high","low","close","ma5High","ma10High","ma5Low","ma10Low","bbTop","bbMid","bbLow","momentumBuy","momentumSell","rawBuy","rawSell","gapReset","lastMomentum","converged","buyChain","sellChain");
 FileWrite(eventFile,"tf","direction","time","lastMomentum","raw","reversal","tpw","formation","frozenBody","hypothesesConverged","classification");
 int totalReady=0,totalCandidates=0;
 for(int t=0;t<7;t++)
 {
  int tf=CustomTFValue(t),seconds=GetTimeframeSeconds(tf),bars=iBars(Symbol(),tf),oldest=(int)MathMin(600,bars-51);
  int ready=0,unavailable=0,gaps=0,raws=0,momentums=0,convergenceBars=0,candidates=0,longest=0,segment=0;
  datetime previous=0,lastMomentum=0,first=0,last=0,lastBuy=0,lastSell=0;OriginOwners owners[4];bool initialized=false;
  for(int sh=oldest;sh>=1;sh--)
  {
   datetime stamp=iTime(Symbol(),tf,sh);TimeframeData d;GetDataForTimeframe(Symbol(),tf,stamp,d);M10MomentumSnapshot momentum;
   bool available=d.is_valid && d.is_closed && ReadM10MomentumSource(Symbol(),d,momentum);
   if(!available){unavailable++;initialized=false;previous=0;lastMomentum=0;segment=0;continue;}
   bool newSegment=!initialized || stamp!=previous+seconds;
   if(newSegment)
   {
    if(initialized)gaps++;for(int scenario=0;scenario<4;scenario++)SeedHypothesis(owners[scenario],tf,stamp-seconds,d.close,scenario);
    initialized=true;lastMomentum=0;lastBuy=0;lastSell=0;segment=0;
   }
   ready++;segment++;if(segment>longest)longest=segment;if(first==0)first=stamp;last=stamp;
   BollingerBand bb;ZeroMemory(bb);bb.TOP_BB=d.bollinger[0];bb.MID_BB=d.bollinger[1];bb.LOW_BB=d.bollinger[2];bb.Width=bb.TOP_BB-bb.LOW_BB;
   bool rb=DetectExtreme(Symbol(),DIR_BUY,d,bb),rs=DetectExtreme(Symbol(),DIR_SELL,d,bb);if(rb || rs)raws++;
   if(momentum.buy || momentum.sell){lastMomentum=stamp;momentums++;}
   bool advanced=true;for(int scenario=0;scenario<4;scenario++)if(!AdvanceOrigin(owners[scenario],d,bb,rb,rs))advanced=false;
   if(!advanced){unavailable++;initialized=false;previous=0;lastMomentum=0;segment=0;continue;}
   bool converged=SameOrigin(owners[0],owners[1]) && SameOrigin(owners[0],owners[2]) && SameOrigin(owners[0],owners[3]);if(converged)convergenceBars++;
   bool buy=CandidateChain(owners[0].mhvBuy,lastMomentum),sell=CandidateChain(owners[0].mhvSell,lastMomentum);
   FileWrite(inputFile,tf,(int)stamp,sh,DoubleToString(d.open,10),DoubleToString(d.high,10),DoubleToString(d.low,10),DoubleToString(d.close,10),DoubleToString(d.ma[0],10),DoubleToString(d.ma[1],10),DoubleToString(d.ma[2],10),DoubleToString(d.ma[3],10),DoubleToString(bb.TOP_BB,10),DoubleToString(bb.MID_BB,10),DoubleToString(bb.LOW_BB,10),(int)momentum.buy,(int)momentum.sell,(int)rb,(int)rs,(int)newSegment,(int)lastMomentum,(int)converged,(int)buy,(int)sell);
   for(int side=0;side<2;side++)
   {
    MLVData m=side==0?owners[0].mhvBuy:owners[0].mhvSell;bool chain=side==0?buy:sell;datetime seen=side==0?lastBuy:lastSell;
    if(!chain || m.ConfirmationCandleTime==seen)continue;
    if(side==0)lastBuy=m.ConfirmationCandleTime;else lastSell=m.ConfirmationCandleTime;candidates++;
    FileWrite(eventFile,tf,side==0?"BUY":"SELL",(int)stamp,(int)lastMomentum,(int)m.ParentRawCandleTime,(int)m.ParentConfirmationCandleTime,(int)m.TPWajibCandleTime,(int)m.ConfirmationCandleTime,DoubleToString(m.FrozenMarkedBody,10),(int)converged,"ENGINEERING_ORIGIN_CANDIDATE_NOT_AUTHENTICATED_EPOCH");
   }
   previous=stamp;
  }
  totalReady+=ready;totalCandidates+=candidates;
  Print("[MHV-ORIGIN-TF] tf=",tf," bars=",bars," scanned=",oldest," ready=",ready," unavailable=",unavailable," boundaries=",gaps," longest=",longest," raw=",raws," momentum=",momentums," convergedBars=",convergenceBars," candidateChains=",candidates," from=",(int)first," till=",(int)last);
 }
 FileClose(inputFile);FileClose(eventFile);
 Print("[MHV-ORIGIN-SUMMARY] frames=7 ready=",totalReady," candidates=",totalCandidates," orders=",OrdersTotal()," historyOrders=",OrdersHistoryTotal()," acceptance=NOT_PROMOTED");
 return totalReady>0 && OrdersTotal()==0 && OrdersHistoryTotal()==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
void OnTimer(){}
void OnDeinit(const int reason){}
