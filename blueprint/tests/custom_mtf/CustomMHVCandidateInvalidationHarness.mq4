#property strict
// Synthetic platform input; actual canonical M08/M09 engines and M10 classification.
datetime EraseNow=D'2026.08.03 10:00';int ErasePhase=1,EraseSide=1,EraseShape=1;bool EraseMissing=false;int EraseReads=0,EraseDropAt=0;bool EraseDropObserved=false;
bool EraseSymbol(string s){return s=="MHV_ERASURE";}
datetime EraseTime(string s,int tf,int shift){if(!EraseSymbol(s))return iTime(s,tf,shift);return shift>=0 && shift<64?EraseNow-shift*tf*60:0;}
int EraseBars(string s,int tf){return EraseSymbol(s)?64:iBars(s,tf);}
double EraseClose(string s,int tf,int shift)
{
 if(!EraseSymbol(s))return iClose(s,tf,shift);EraseReads++;
 if(EraseDropAt>0 && EraseReads>=EraseDropAt && shift==9){EraseDropObserved=true;return 0;}
 if(EraseMissing && shift==9)return 0;
 if(shift==1)return ErasePhase==1?(EraseSide==1?90:110):100;
 if(ErasePhase==2 && shift==2)return EraseSide==1?90:110;
 int priorShift=shift-(ErasePhase==2?1:0);return EraseShape==0?100:(priorShift%2==0?99:101);
}
double EraseOpen(string s,int tf,int shift)
{if(!EraseSymbol(s))return iOpen(s,tf,shift);return ErasePhase==1?(EraseSide==1?91:109):(EraseSide==1?101:99);}
double EraseHigh(string s,int tf,int shift){return EraseSymbol(s)?112:iHigh(s,tf,shift);}
double EraseLow(string s,int tf,int shift){return EraseSymbol(s)?88:iLow(s,tf,shift);}
double EraseMA(string s,int tf,int period,int offset,int method,int price,int shift)
{if(!EraseSymbol(s))return iMA(s,tf,period,offset,method,price,shift);return price==PRICE_HIGH?(period==5?101:101.5):(price==PRICE_LOW?(period==5?99:98.5):100);}
int EraseShift(string s,int tf,datetime stamp,bool exact=false){return EraseSymbol(s)?(int)((EraseNow-stamp)/(tf*60)):iBarShift(s,tf,stamp,exact);}
double EraseInfo(string s,int mode){if(!EraseSymbol(s))return MarketInfo(s,mode);if(mode==MODE_POINT)return 0.00001;if(mode==MODE_DIGITS)return 5;if(mode==MODE_TIME)return (double)(EraseNow+1);return 1;}
datetime EraseClock(){return EraseNow+1;}
datetime EraseClock(MqlDateTime &out){datetime now=EraseNow+1;TimeToStruct(now,out);return now;}
#define iTime EraseTime
#define iBars EraseBars
#define iClose EraseClose
#define iOpen EraseOpen
#define iHigh EraseHigh
#define iLow EraseLow
#define iMA EraseMA
#define iBarShift EraseShift
#define MarketInfo EraseInfo
#define TimeCurrent EraseClock
#define OnInit CanonicalOnInit
#define OnDeinit CanonicalOnDeinit
#define OnTick CanonicalOnTick
#define OnTimer CanonicalOnTimer
#include "..\\..\\source\\BBMA_EA.mq4"
#undef iTime
#undef iBars
#undef iClose
#undef iOpen
#undef iHigh
#undef iLow
#undef iMA
#undef iBarShift
#undef MarketInfo
#undef TimeCurrent
#undef OnInit
#undef OnDeinit
#undef OnTick
#undef OnTimer
#include "CustomOwnerTestEquality.mqh"
int passed=0,failed=0;
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[MHV-CANDIDATE] ",name," ",ok?"PASS":"FAIL");}
void Data(int tf,TimeframeData &d,BollingerBand &bb)
{
 GetDataForTimeframe("MHV_ERASURE",tf,EraseTime("MHV_ERASURE",tf,1),d);
 ZeroMemory(bb);bb.TOP_BB=d.bollinger[0];bb.MID_BB=d.bollinger[1];bb.LOW_BB=d.bollinger[2];bb.Width=bb.TOP_BB-bb.LOW_BB;
}
void Seed(int tf,ENUM_DIRECTION dir,ENUM_MLV_STATE stage,TimeframeData &d,MLVData &m,ExtremeLifecycleData &parent)
{
 ENUM_DIRECTION parentDir=dir==DIR_BUY?DIR_SELL:DIR_BUY;int sec=tf*60;
 ResetExtremeLifecycle(parent,parentDir,tf);parent.Maturity=EXT_MAT_RETEST_READY;parent.IsValid=true;
 parent.RawCandleTime=d.candle_time-8*sec;parent.ConfirmationCandleTime=d.candle_time-7*sec;parent.LastUpdateCandleTime=d.candle_time-sec;
 parent.PreviousClose=100;parent.ProvisionalBodyAnchor=100;parent.FrozenBodyAnchor=100;
 ResetMLVState(m,dir,tf);m.State=stage;m.IsValid=true;m.InvalidationWindowOpen=true;
 m.ParentRawCandleTime=parent.RawCandleTime;m.ParentConfirmationCandleTime=parent.ConfirmationCandleTime;
 m.TPWajibCandleTime=d.candle_time-6*sec;m.StartCandleTime=d.candle_time-5*sec;m.ConfirmationCandleTime=d.candle_time-4*sec;
 m.FrozenMarkedBody=100;m.PreviousClose=100;m.LastUpdateCandleTime=d.candle_time-sec;
 m.SupersessionCandidateActive=true;m.SupersessionRawCandleTime=d.candle_time-2*sec;m.SupersessionRawBar=3;
}
int OnInit()
{
 g_pair_count=0;
 for(int t=0;t<7;t++)for(int side=0;side<2;side++)for(int st=0;st<2;st++)for(int shape=0;shape<2;shape++)
 {
  int tf=CustomTFValue(t);ENUM_DIRECTION dir=side==0?DIR_BUY:DIR_SELL;ENUM_MLV_STATE stage=st==0?MLV_FORMATION_ESTABLISHED:MLV_RETEST_COMPLETE;
  EraseNow=D'2026.08.03 10:00';ErasePhase=1;EraseSide=side==0?1:-1;EraseShape=shape;EraseMissing=false;g_processing_time=EraseNow+1;
  TimeframeData d;BollingerBand bb;Data(tf,d,bb);M10MomentumSnapshot mom;bool ready=ReadM10MomentumSource("MHV_ERASURE",d,mom);
  bool continuing=dir==DIR_BUY?mom.sell:mom.buy;string key=IntegerToString(tf)+"_"+IntegerToString(side)+"_"+IntegerToString(st)+"_shape"+IntegerToString(shape);
  Check(key+"_fixture_ready_Momentum_class",ready && continuing==(shape==1));
  MLVData mlv;ExtremeLifecycleData parent;Seed(tf,dir,stage,d,mlv,parent);datetime oldRaw=mlv.SupersessionRawCandleTime;
  UpdateExtremeLifecycle(parent,"MHV_ERASURE",parent.Direction,d,bb,false);
  UpdateCanonicalMLVState(mlv,"MHV_ERASURE",dir,d,bb,parent,false,false);
  Check(key+"_MHV_becomes_VOID",mlv.State==MLV_VOID && !mlv.IsValid);
  bool candidate=mlv.SupersessionCandidateActive && mlv.SupersessionRawCandleTime==oldRaw;
  Check(key+"_candidate_matches_own_invalidation",shape==1?(!mlv.SupersessionCandidateActive && mlv.SupersessionRawCandleTime==0 && mlv.SupersessionRawBar==0):candidate);
  EraseNow+=tf*60;ErasePhase=2;g_processing_time=EraseNow+1;Data(tf,d,bb);
  bool nextReady=ReadM10MomentumSource("MHV_ERASURE",d,mom);Check(key+"_reversal_ready_non_Momentum",nextReady && !mom.buy && !mom.sell);
  UpdateExtremeLifecycle(parent,"MHV_ERASURE",parent.Direction,d,bb,false);
  UpdateCanonicalMLVState(mlv,"MHV_ERASURE",dir,d,bb,parent,false,false);
  bool installed=parent.Maturity==EXT_MAT_REVERSAL_CONFIRMED && parent.RawCandleTime==oldRaw && parent.ConfirmationCandleTime==d.candle_time;
  Check(key+"_invalid_raw_cannot_install_parent",shape==1?(!installed && mlv.State==MLV_VOID):(installed && mlv.State==MLV_SUPERSEDED));
 }
 for(int t=0;t<7;t++)for(int side=0;side<2;side++)
 {
  int tf=CustomTFValue(t);ENUM_DIRECTION dir=side==0?DIR_BUY:DIR_SELL;
  EraseNow=D'2026.08.03 10:00';ErasePhase=1;EraseSide=side==0?1:-1;EraseShape=1;EraseMissing=false;
  TimeframeData d;BollingerBand bb;Data(tf,d,bb);MLVData mlv;ExtremeLifecycleData parent;Seed(tf,dir,MLV_FORMATION_ESTABLISHED,d,mlv,parent);
  MLVData old=mlv;ExtremeLifecycleData oldParent=parent;EraseMissing=true;
  UpdateCanonicalMLVState(mlv,"MHV_ERASURE",dir,d,bb,parent,false,false);
  Check("unavailable_preserves_candidate_"+IntegerToString(tf)+"_"+IntegerToString(side),SameMLVData(mlv,old) && SameExtremeLifecycleData(parent,oldParent));EraseMissing=false;
 }
 for(int t=0;t<7;t++)for(int side=0;side<2;side++)
 {
  int tf=CustomTFValue(t);ENUM_DIRECTION dir=side==0?DIR_BUY:DIR_SELL;
  EraseNow=D'2026.08.03 10:00';ErasePhase=1;EraseSide=side==0?1:-1;EraseShape=1;EraseMissing=false;EraseDropAt=0;
  TimeframeData d;BollingerBand bb;Data(tf,d,bb);M10MomentumSnapshot probe;EraseReads=0;
  bool probeReady=ReadM10MomentumSource("MHV_ERASURE",d,probe);int initialReadCount=EraseReads;
  MLVData mlv;ExtremeLifecycleData parent;Seed(tf,dir,MLV_FORMATION_ESTABLISHED,d,mlv,parent);
  MLVData old=mlv;ExtremeLifecycleData oldParent=parent;
  EraseReads=0;EraseDropObserved=false;EraseDropAt=initialReadCount+1;
  UpdateCanonicalMLVState(mlv,"MHV_ERASURE",dir,d,bb,parent,false,false);
  Check("extra_read_revision_reached_"+IntegerToString(tf)+"_"+IntegerToString(side),probeReady && EraseDropObserved);
  Check("extra_read_revision_atomic_"+IntegerToString(tf)+"_"+IntegerToString(side),SameMLVData(mlv,old) && SameExtremeLifecycleData(parent,oldParent));
  EraseDropAt=0;
 }
 Check("no_orders",OrdersTotal()==0 && OrdersHistoryTotal()==0);
 Print("[MHV-CANDIDATE-SUMMARY] passed=",passed," failed=",failed);return INIT_SUCCEEDED;
}
void OnTick(){}
void OnTimer(){}
void OnDeinit(const int reason){}
