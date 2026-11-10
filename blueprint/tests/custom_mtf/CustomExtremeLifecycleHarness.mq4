#property strict
// Complete flat Momentum history for independently controlled M08 trajectories.
datetime ExtTime=0;int ExtTF=0;double ExtClose=100;
datetime ExtITime(string s,int tf,int shift){if(s=="EXT_FIX" && tf==ExtTF)return shift>=0 && shift<64?ExtTime+(1-shift)*tf*60:0;return iTime(s,tf,shift);}
int ExtIBars(string s,int tf){return s=="EXT_FIX"?64:iBars(s,tf);}
double ExtIClose(string s,int tf,int shift){return s=="EXT_FIX" && tf==ExtTF?ExtClose:iClose(s,tf,shift);}
#define iTime ExtITime
#define iBars ExtIBars
#define iClose ExtIClose
#define OnInit CanonicalOnInit
#define OnDeinit CanonicalOnDeinit
#define OnTick CanonicalOnTick
#define OnTimer CanonicalOnTimer
#include "..\\..\\source\\BBMA_EA.mq4"
#undef iTime
#undef iBars
#undef iClose
#undef OnInit
#undef OnDeinit
#undef OnTick
#undef OnTimer
#include "CustomOwnerTestEquality.mqh"
int passed=0,failed=0,history=0;
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[EXT-LIFE] ",name," ",ok?"PASS":"FAIL");}
void Step(TimeframeData &d,int tf,datetime time,ENUM_DIRECTION dir,double o,double c,double lo,double hi)
{
 InitTimeframeData(d);d.timeframe=tf;d.candle_time=time;d.barIndex=1;d.is_valid=true;d.is_closed=true;
 d.open=dir==DIR_SELL?o:200-o;d.close=dir==DIR_SELL?c:200-c;d.high=dir==DIR_SELL?hi:200-lo;d.low=dir==DIR_SELL?lo:200-hi;
 d.ma[0]=111;d.ma[1]=109;d.ma[2]=89;d.ma[3]=91;d.point=0.00001;ExtTime=time;ExtTF=tf;ExtClose=d.close;
}
int OnInit()
{
 g_pair_count=0;
 for(int t=0;t<7;t++)for(int side=0;side<2;side++)
 {
  int tf=CustomTFValue(t),sec=tf*60;ENUM_DIRECTION dir=side==0?DIR_SELL:DIR_BUY;string k=IntegerToString(tf)+"_"+IntegerToString(side)+"_";datetime start=D'2026.08.03 10:00';
  TimeframeData d;Step(d,tf,start,dir,105,104,103,106);BollingerBand bb;ZeroMemory(bb);bb.TOP_BB=110;bb.MID_BB=100;bb.LOW_BB=90;bb.Width=20;
  int a=dir==DIR_SELL?0:2,b=dir==DIR_SELL?1:3;double edge=dir==DIR_SELL?110:90,out=dir==DIR_SELL?111:89,inward=dir==DIR_SELL?109:91;
  d.ma[a]=edge;d.ma[b]=edge;Check(k+"MA_touch_not_raw",!DetectExtreme("EXT_FIX",dir,d,bb));
  d.ma[a]=out;d.ma[b]=inward;Check(k+"MA5_only_raw",DetectExtreme("EXT_FIX",dir,d,bb));
  d.ma[a]=inward;d.ma[b]=out;Check(k+"MA10_only_raw",DetectExtreme("EXT_FIX",dir,d,bb));
  d.ma[a]=inward;d.ma[b]=inward;Check(k+"inside_not_raw",!DetectExtreme("EXT_FIX",dir,d,bb));
  d.is_closed=false;Check(k+"live_flag_rejected",!DetectExtreme("EXT_FIX",dir,d,bb));d.is_closed=true;d.is_valid=false;Check(k+"invalid_rejected",!DetectExtreme("EXT_FIX",dir,d,bb));d.is_valid=true;
  ExtremeLifecycleData owner;ResetExtremeLifecycle(owner,dir,tf);Step(d,tf,start,dir,105,104,103,106);
  UpdateExtremeLifecycle(owner,"EXT_FIX",dir,d,bb,true);Signal signal;Check(k+"raw_not_component",owner.Maturity==EXT_MAT_RAW && !ExportReversalConfirmedExtremeSignal(owner,signal));
  ExtremeLifecycleData before=owner;UpdateExtremeLifecycle(owner,"EXT_FIX",dir,d,bb,true);Check(k+"same_candle_no_confirmation",SameExtremeLifecycleData(owner,before));
  Step(d,tf,start+sec,dir,104,102,101,105);UpdateExtremeLifecycle(owner,"EXT_FIX",dir,d,bb,true);Check(k+"first_reversal_component",owner.Maturity==EXT_MAT_REVERSAL_CONFIRMED && ExportReversalConfirmedExtremeSignal(owner,signal) && signal.CandleTime==d.candle_time && signal.Timeframe==tf && signal.Direction==dir);
  double expected=dir==DIR_SELL?104:96;Check(k+"body_not_wick_anchor",owner.ProvisionalBodyAnchor==expected);
  Step(d,tf,start+2*sec,dir,102,100,99,103);UpdateExtremeLifecycle(owner,"EXT_FIX",dir,d,bb,false);Check(k+"reversal_continues",owner.Maturity==EXT_MAT_REVERSAL_CONFIRMED && owner.ProvisionalBodyAnchor==expected);
  Step(d,tf,start+3*sec,dir,100,101,99,102);UpdateExtremeLifecycle(owner,"EXT_FIX",dir,d,bb,false);Check(k+"retest_freezes_excludes_trigger",owner.Maturity==EXT_MAT_RETEST_PHASE && owner.FrozenBodyAnchor==expected && owner.RetestStartCandleTime==d.candle_time);
  ExtremeLifecycleData bodyOwner=owner,maOwner=owner;
  Step(d,tf,start+4*sec,dir,101,102,100,104);UpdateExtremeLifecycle(bodyOwner,"EXT_FIX",dir,d,bb,false);Check(k+"body_only_touch_completes",bodyOwner.Maturity==EXT_MAT_RETEST_READY && bodyOwner.FrozenBodyAnchor==expected);
  Step(d,tf,start+4*sec,dir,101,102,100,103);d.ma[a]=dir==DIR_SELL?103:97;UpdateExtremeLifecycle(maOwner,"EXT_FIX",dir,d,bb,false);Check(k+"MA5_only_touch_completes",maOwner.Maturity==EXT_MAT_RETEST_READY && maOwner.FrozenBodyAnchor==expected);
  Step(d,tf,start+5*sec,dir,102,103,101,109);UpdateExtremeLifecycle(bodyOwner,"EXT_FIX",dir,d,bb,false);Check(k+"frozen_anchor_does_not_drift",bodyOwner.Maturity==EXT_MAT_RETEST_READY && bodyOwner.FrozenBodyAnchor==expected);
  Step(d,tf,start+5*sec,dir,109,111,108,112);UpdateExtremeLifecycle(owner,"EXT_FIX",dir,d,bb,false);Check(k+"void_before_touch",owner.Maturity==EXT_MAT_VOID && !owner.IsValid && !ExportReversalConfirmedExtremeSignal(owner,signal));
  Step(d,tf,start+6*sec,dir,105,104,103,106);UpdateExtremeLifecycle(owner,"EXT_FIX",dir,d,bb,true);Check(k+"new_raw_after_void",owner.Maturity==EXT_MAT_RAW && owner.RawCandleTime==d.candle_time);
  Step(d,tf,start+80*sec,dir,104,102,101,105);UpdateExtremeLifecycle(owner,"EXT_FIX",dir,d,bb,false);Check(k+"no_generic_TTL",owner.Maturity==EXT_MAT_REVERSAL_CONFIRMED && owner.IsValid);
  before=owner;Step(d,tf,start+79*sec,dir,104,102,101,105);UpdateExtremeLifecycle(owner,"EXT_FIX",dir,d,bb,false);Check(k+"old_candle_unchanged",SameExtremeLifecycleData(owner,before));
  ExtremeLifecycleData buy,sell;ResetExtremeLifecycle(buy,DIR_BUY,tf);ResetExtremeLifecycle(sell,DIR_SELL,tf);buy.Maturity=EXT_MAT_REVERSAL_CONFIRMED;buy.IsValid=true;buy.ConfirmationCandleTime=start;sell.Maturity=EXT_MAT_RAW;sell.ConfirmationCandleTime=0;
  ResolveOppositeExtremeSupersession(buy,sell,d);Check(k+"opposite_raw_no_supersession",buy.Maturity==EXT_MAT_REVERSAL_CONFIRMED);
  sell.Maturity=EXT_MAT_REVERSAL_CONFIRMED;sell.IsValid=true;sell.ConfirmationCandleTime=start+sec;ResolveOppositeExtremeSupersession(buy,sell,d);Check(k+"opposite_mature_supersedes",buy.Maturity==EXT_MAT_SUPERSEDED && !buy.IsValid && sell.IsValid);
 }
 g_processing_time=TimeCurrent();
 for(int t=0;t<7;t++)for(int sh=1;sh<=20;sh++)
 {
  int tf=CustomTFValue(t);TimeframeData d;InitTimeframeData(d);GetDataForTimeframe(Symbol(),tf,iTime(Symbol(),tf,sh),d);bool loaded=d.is_valid && d.is_closed;BollingerBand bb;ZeroMemory(bb);if(loaded)CalculateBollinger(Symbol(),tf,sh,bb);
  M10MomentumSnapshot m;bool ready=loaded && ReadM10MomentumSource(Symbol(),d,m);Check("history_ready_"+IntegerToString(tf)+"_"+IntegerToString(sh),ready);if(!ready)continue;
  bool buy=d.ma[2]<bb.LOW_BB || d.ma[3]<bb.LOW_BB,sell=d.ma[0]>bb.TOP_BB || d.ma[1]>bb.TOP_BB;
  Check("history_raw_"+IntegerToString(tf)+"_"+IntegerToString(sh),DetectExtreme(Symbol(),DIR_BUY,d,bb)==buy && DetectExtreme(Symbol(),DIR_SELL,d,bb)==sell);
  Check("history_canonical_invalidation_"+IntegerToString(tf)+"_"+IntegerToString(sh),IsExtremeMomentumInvalidation(Symbol(),d,bb)==(m.buy || m.sell) && IsExtremeLifecycleInvalidation(Symbol(),DIR_BUY,d,bb)==(d.close<bb.LOW_BB || m.buy || m.sell) && IsExtremeLifecycleInvalidation(Symbol(),DIR_SELL,d,bb)==(d.close>bb.TOP_BB || m.buy || m.sell));history++;
 }
 Check("history_140",history==140);Check("no_orders",OrdersTotal()==0);Print("[EXT-LIFE-SUMMARY] passed=",passed," failed=",failed," history=",history);return INIT_SUCCEEDED;
}
void OnTick(){}
void OnTimer(){}
void OnDeinit(const int reason){}
