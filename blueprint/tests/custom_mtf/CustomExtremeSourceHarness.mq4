#property strict
// Actual engines; only platform series/specification calls are fixtures.
datetime GapNow=D'2026.08.03 10:00';int GapCase=1,GapReads=0,GapMutationAt=22;bool GapRevised=false,GapNeutral=false;
bool GapSymbol(string s){return s=="MOM_GAP";}
datetime GapTime(string s,int tf,int shift)
{
 if(!GapSymbol(s))return iTime(s,tf,shift);
 int bars=GapCase==2?21:64;if(shift<0 || shift>=bars)return 0;
 if(GapCase==3 && shift==4)shift=3;
 return GapNow-shift*tf*60;
}
int GapBars(string s,int tf){return GapSymbol(s)?(GapCase==2?21:64):iBars(s,tf);}
double GapClose(string s,int tf,int shift)
{
 if(!GapSymbol(s))return iClose(s,tf,shift);
 if(GapNeutral)return 100;
 GapReads++;if(GapCase==5 && GapReads>=GapMutationAt && shift==9)return 0;
 if(GapCase==4 && GapReads==GapMutationAt)GapRevised=true;
 if(shift==1)return 110;
 if(GapCase==1 && shift==9)return 0;
 if(shift==21 && GapRevised)return 103;
 return shift%2==0?99:101;
}
double GapOpen(string s,int tf,int shift){return GapSymbol(s)?111:iOpen(s,tf,shift);}
double GapHigh(string s,int tf,int shift){return GapSymbol(s)?112:iHigh(s,tf,shift);}
double GapLow(string s,int tf,int shift){return GapSymbol(s)?98:iLow(s,tf,shift);}
double GapMA(string s,int tf,int period,int offset,int method,int price,int shift)
{if(!GapSymbol(s))return iMA(s,tf,period,offset,method,price,shift);return price==PRICE_HIGH?(period==5?101:101.5):(price==PRICE_LOW?(period==5?99:98.5):100);}
int GapShift(string s,int tf,datetime time,bool exact=false)
{if(!GapSymbol(s))return iBarShift(s,tf,time,exact);return (int)((GapNow-time)/(tf*60));}
double GapInfo(string s,int mode)
{if(!GapSymbol(s))return MarketInfo(s,mode);if(mode==MODE_POINT)return 0.00001;if(mode==MODE_DIGITS)return 5;if(mode==MODE_TIME)return (double)(GapNow+1);return 1;}
datetime GapServerTime(){return GapNow+1;}
datetime GapServerTime(MqlDateTime &out){datetime now=GapNow+1;TimeToStruct(now,out);return now;}
#define iTime GapTime
#define iBars GapBars
#define iClose GapClose
#define iOpen GapOpen
#define iHigh GapHigh
#define iLow GapLow
#define iMA GapMA
#define iBarShift GapShift
#define MarketInfo GapInfo
#define TimeCurrent GapServerTime
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
void Check(string label,bool ok){if(ok)passed++;else failed++;Print("[EXT-SOURCE] ",label," ",ok?"PASS":"FAIL");}
void ResetGap(int kind)
{
 GapCase=kind;GapReads=0;GapRevised=false;GapNeutral=false;GapMutationAt=22;g_processing_time=GapNow+1;
 g_pair_count=1;InitPairState(g_pair_states[0]);g_pair_states[0].actual_symbol="MOM_GAP";g_pair_states[0].pair_enabled=true;g_pair_names[0]="MOM_GAP";
 g_processed_candle_time[0]=0;
}
void DataFixture(int tf,TimeframeData &d)
{
 InitTimeframeData(d);d.timeframe=tf;d.barIndex=1;d.candle_time=GapNow-tf*60;d.is_valid=true;d.is_closed=true;
 d.open=111;d.high=112;d.low=98;d.close=110;d.point=0.00001;d.data_count=64;
 d.ma[0]=101;d.ma[1]=101.5;d.ma[2]=99;d.ma[3]=98.5;d.ma[4]=100;
 d.bollinger[0]=106;d.bollinger[1]=100;d.bollinger[2]=94;
}
int OnInit()
{
 for(int t=0;t<7;t++)for(int c=1;c<=4;c++)
 {
  int tf=CustomTFValue(t);string key=IntegerToString(tf)+"_case"+IntegerToString(c);ResetGap(1);
  TimeframeData data;DataFixture(tf,data);BollingerBand bb;ZeroMemory(bb);CalculateBollinger("MOM_GAP",tf,1,bb);
  ResetGap(c);M10MomentumSnapshot m;bool ready=ReadM10MomentumSource("MOM_GAP",data,m);
  Check("canonical_source_unavailable_"+key,!ready && !m.buy && !m.sell);
  ResetGap(c);Check("unavailable_is_not_M08_Momentum_"+key,!IsExtremeMomentumInvalidation("MOM_GAP",data,bb));
  ResetGap(c);ExtremeLifecycleData owner;ResetExtremeLifecycle(owner,DIR_SELL,PERIOD_H4);owner.Maturity=EXT_MAT_REVERSAL_CONFIRMED;owner.IsValid=true;owner.RawCandleTime=data.candle_time-2*tf*60;owner.ConfirmationCandleTime=data.candle_time-tf*60;owner.LastUpdateCandleTime=owner.ConfirmationCandleTime;owner.PreviousClose=109;owner.ProvisionalBodyAnchor=108;
  ExtremeLifecycleData old=owner;UpdateExtremeLifecycle(owner,"MOM_GAP",DIR_BUY,data,bb,false);
  Check("unavailable_M08_no_owner_reset_or_void_"+key,SameExtremeLifecycleData(owner,old));
 }
 for(int t=0;t<7;t++)for(int c=0;c<3;c++)
 {
  int tf=CustomTFValue(t);ResetGap(0);TimeframeData data;DataFixture(tf,data);BollingerBand bb;ZeroMemory(bb);bb.TOP_BB=106;bb.MID_BB=100;bb.LOW_BB=94;bb.Width=12;
  if(c==0)data.barIndex=0;if(c==1)data.candle_time-=tf*60;if(c==2)data.close=109;
  ExtremeLifecycleData owner;ResetExtremeLifecycle(owner,DIR_SELL,PERIOD_H4);owner.Maturity=EXT_MAT_RAW;owner.RawCandleTime=data.candle_time-tf*60;ExtremeLifecycleData old=owner;
  UpdateExtremeLifecycle(owner,"MOM_GAP",DIR_BUY,data,bb,true);Check("source_identity_defers_"+IntegerToString(tf)+"_"+IntegerToString(c),SameExtremeLifecycleData(owner,old));
 }
 for(int t=0;t<7;t++)for(int c=1;c<=4;c++)
 {
  int tf=CustomTFValue(t);ResetGap(c);TimeframeData data;DataFixture(tf,data);BollingerBand bb;ZeroMemory(bb);bb.TOP_BB=106;bb.MID_BB=100;bb.LOW_BB=94;bb.Width=12;
  MLVData mlv;ResetMLVState(mlv,DIR_BUY,tf);mlv.State=MLV_FORMATION_ESTABLISHED;mlv.IsValid=true;mlv.SupersessionCandidateActive=true;mlv.SupersessionRawCandleTime=data.candle_time-tf*60;mlv.ConfirmationCandleTime=data.candle_time-2*tf*60;MLVData oldMLV=mlv;
  ExtremeLifecycleData parent;ResetExtremeLifecycle(parent,DIR_BUY,tf);ExtremeLifecycleData oldParent=parent;
  bool available=true;bool promoted=TryAdvanceMHVSupersessionCandidate(mlv,"MOM_GAP",data,bb,parent,available,false);
  Check("unavailable_extreme_handover_atomic_"+IntegerToString(tf)+"_"+IntegerToString(c),!available && !promoted && SameMLVData(mlv,oldMLV) && SameExtremeLifecycleData(parent,oldParent));
 }
 for(int t=0;t<7;t++)
 {
  int tf=CustomTFValue(t);ResetGap(5);GapMutationAt=163;TimeframeData data;DataFixture(tf,data);BollingerBand bb;ZeroMemory(bb);bb.TOP_BB=106;bb.MID_BB=100;bb.LOW_BB=94;bb.Width=12;
  MLVData mlv;ResetMLVState(mlv,DIR_BUY,tf);mlv.State=MLV_DIRECTION_TAKEN;mlv.IsValid=true;mlv.SupersessionCandidateActive=true;mlv.SupersessionRawCandleTime=data.candle_time-tf*60;mlv.ConfirmationCandleTime=data.candle_time-2*tf*60;mlv.LastUpdateCandleTime=data.candle_time-tf*60;mlv.PreviousClose=109;mlv.InvalidationWindowOpen=false;MLVData oldMLV=mlv;
  ExtremeLifecycleData parent;ResetExtremeLifecycle(parent,DIR_BUY,tf);ExtremeLifecycleData oldParent=parent;
  UpdateCanonicalMLVState(mlv,"MOM_GAP",DIR_BUY,data,bb,parent,false,false);
  Check("source_revision_M09_extreme_handover_atomic_"+IntegerToString(tf),SameMLVData(mlv,oldMLV) && SameExtremeLifecycleData(parent,oldParent));
 }
 Check("no_orders",OrdersTotal()==0);Print("[EXT-SOURCE-SUMMARY] passed=",passed," failed=",failed);return INIT_SUCCEEDED;
}
void OnTick(){}
void OnTimer(){}
void OnDeinit(const int reason){}
