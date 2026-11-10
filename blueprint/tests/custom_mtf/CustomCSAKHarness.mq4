#property strict
// Synthetic detector/consumer fixtures; no orders or canonical controller invoked.
double fixtureOpen=105,fixtureClose=102;
int openReads=0;
double CSAKOpen(string symbol,int tf,int shift){if(symbol=="CSAK_FIXTURE"){openReads++;return fixtureOpen;}return iOpen(symbol,tf,shift);}
double CSAKClose(string symbol,int tf,int shift){if(symbol=="CSAK_FIXTURE")return fixtureClose;return iClose(symbol,tf,shift);}
datetime CSAKSourceNow=D'2026.08.03 00:00';
datetime CSAKTime(string symbol,int tf,int shift){if(symbol=="CSAK_FIXTURE")return shift>=0 && shift<64?CSAKSourceNow-shift*tf*60:0;return iTime(symbol,tf,shift);}
int CSAKBars(string symbol,int tf){return symbol=="CSAK_FIXTURE"?64:iBars(symbol,tf);}
#define iTime CSAKTime
#define iBars CSAKBars
#define iOpen CSAKOpen
#define iClose CSAKClose
#define OnInit CanonicalOnInit
#define OnDeinit CanonicalOnDeinit
#define OnTick CanonicalOnTick
#define OnTimer CanonicalOnTimer
#include "..\\..\\source\\BBMA_EA.mq4"
#undef OnInit
#undef OnDeinit
#undef OnTick
#undef OnTimer
#undef iTime
#undef iBars
#undef iOpen
#undef iClose
int passed=0,failed=0;
void Check(string label,bool ok){if(ok)passed++;else failed++;Print("[CUSTOM-CSAK] ",label," ",ok?"PASS":"FAIL");}
int OnInit()
{
 double opens[5]={0,98,100,102,105};
 for(int t=0;t<7;t++)
 {
  int tf=CustomTFValue(t);string tag=IntegerToString(tf);MovingAverage ma;ZeroMemory(ma);
  BollingerBand bb;ZeroMemory(bb);bb.MID_BB=100;
  ma.MA5_High=101;ma.MA10_High=101.5;ma.MA5_Low=99;ma.MA10_Low=98.5;
  openReads=0;fixtureClose=102;
  for(int i=0;i<5;i++){fixtureOpen=opens[i];Check(tag+"_buy_open_independent_"+IntegerToString(i),DetectCSD("CSAK_FIXTURE",tf,DIR_BUY,1,ma,bb));}
  Check(tag+"_buy_no_open_access",openReads==0);
  openReads=0;fixtureClose=98;
  for(int j=0;j<5;j++){fixtureOpen=opens[j];Check(tag+"_sell_open_independent_"+IntegerToString(j),DetectCSD("CSAK_FIXTURE",tf,DIR_SELL,1,ma,bb));}
  Check(tag+"_sell_no_open_access",openReads==0);
  fixtureClose=101;Check(tag+"_buy_equal_ma5_rejected",!DetectCSD("CSAK_FIXTURE",tf,DIR_BUY,1,ma,bb));
  fixtureClose=101.5;Check(tag+"_buy_equal_ma10_rejected",!DetectCSD("CSAK_FIXTURE",tf,DIR_BUY,1,ma,bb));
  fixtureClose=99;Check(tag+"_sell_equal_ma5_rejected",!DetectCSD("CSAK_FIXTURE",tf,DIR_SELL,1,ma,bb));
  fixtureClose=98.5;Check(tag+"_sell_equal_ma10_rejected",!DetectCSD("CSAK_FIXTURE",tf,DIR_SELL,1,ma,bb));
  fixtureClose=102;Check(tag+"_live_candle_rejected",!DetectCSD("CSAK_FIXTURE",tf,DIR_BUY,0,ma,bb));
  Check(tag+"_negative_shift_rejected",!DetectCSD("CSAK_FIXTURE",tf,DIR_BUY,-1,ma,bb));
  Check(tag+"_invalid_direction_rejected",!DetectCSD("CSAK_FIXTURE",tf,DIR_NONE,1,ma,bb));
  fixtureClose=0;Check(tag+"_missing_close_rejected",!DetectCSD("CSAK_FIXTURE",tf,DIR_BUY,1,ma,bb));
  fixtureClose=102;ma.MA5_High=0;Check(tag+"_missing_ma5_rejected",!DetectCSD("CSAK_FIXTURE",tf,DIR_BUY,1,ma,bb));
  ma.MA5_High=101;ma.MA10_High=0;Check(tag+"_missing_ma10_rejected",!DetectCSD("CSAK_FIXTURE",tf,DIR_BUY,1,ma,bb));ma.MA10_High=101.5;
  fixtureOpen=105;openReads=0;
  
  
  fixtureClose=102;bb.MID_BB=102;Check(tag+"_buy_equal_mid_rejected",!DetectCSD("CSAK_FIXTURE",tf,DIR_BUY,1,ma,bb));
  bb.MID_BB=103;Check(tag+"_buy_MA_only_not_CSAK",!DetectCSD("CSAK_FIXTURE",tf,DIR_BUY,1,ma,bb));
  fixtureClose=98;bb.MID_BB=98;Check(tag+"_sell_equal_mid_rejected",!DetectCSD("CSAK_FIXTURE",tf,DIR_SELL,1,ma,bb));
  bb.MID_BB=97;Check(tag+"_sell_MA_only_not_CSAK",!DetectCSD("CSAK_FIXTURE",tf,DIR_SELL,1,ma,bb));
  fixtureClose=102;bb.MID_BB=0;Check(tag+"_missing_mid_rejected",!DetectCSD("CSAK_FIXTURE",tf,DIR_BUY,1,ma,bb));

 }
 for(int realTF=0;realTF<7;realTF++)
 {
  int sourceTF=CustomTFValue(realTF);bool ready=true,equivalent=true;int positives=0;
  for(int shift=1;shift<=10;shift++)
  {
   MovingAverage current;ZeroMemory(current);
   current.MA5_High=iMA(Symbol(),sourceTF,5,0,MODE_LWMA,PRICE_HIGH,shift);
   current.MA10_High=iMA(Symbol(),sourceTF,10,0,MODE_LWMA,PRICE_HIGH,shift);
   current.MA5_Low=iMA(Symbol(),sourceTF,5,0,MODE_LWMA,PRICE_LOW,shift);
   current.MA10_Low=iMA(Symbol(),sourceTF,10,0,MODE_LWMA,PRICE_LOW,shift);
   double close=iClose(Symbol(),sourceTF,shift);BollingerBand band;ZeroMemory(band);band.MID_BB=iMA(Symbol(),sourceTF,20,0,MODE_SMA,PRICE_CLOSE,shift);
   if(close<=0 || current.MA5_High<=0 || current.MA10_High<=0 || current.MA5_Low<=0 || current.MA10_Low<=0 || iTime(Symbol(),sourceTF,shift)<=0)ready=false;
   bool buy=close>current.MA5_High && close>current.MA10_High && close>band.MID_BB;
   bool sell=close<current.MA5_Low && close<current.MA10_Low && close<band.MID_BB;
   if(DetectCSD(Symbol(),sourceTF,DIR_BUY,shift,current,band)!=buy || DetectCSD(Symbol(),sourceTF,DIR_SELL,shift,current,band)!=sell)equivalent=false;
   if(buy)positives++;if(sell)positives++;
  }
  Check(IntegerToString(sourceTF)+"_actual_history_ready",ready);
  Check(IntegerToString(sourceTF)+"_actual_20_closed_comparisons",equivalent && ready);
  Print("[CUSTOM-CSAK-DATA] tf=",sourceTF," comparisons=20 positives=",positives);
 }
 TimeframeData data;ZeroMemory(data);data.is_valid=true;data.is_closed=true;data.barIndex=1;data.timeframe=PERIOD_D1;data.candle_time=CSAKTime("CSAK_FIXTURE",PERIOD_D1,1);data.close=102;
 data.ma[0]=101;data.ma[1]=101.5;data.ma[2]=99;data.ma[3]=98.5;data.bollinger[0]=200;data.bollinger[1]=100;data.bollinger[2]=50;
 fixtureOpen=105;fixtureClose=102;BollingerBand d1Band;ZeroMemory(d1Band);d1Band.MID_BB=100;
 Check("D1_watch_delegates_closed_predicate",DetectD1OpportunityCSD("CSAK_FIXTURE",data,d1Band,DIR_BUY));
 data.timeframe=PERIOD_M15;data.candle_time=CSAKTime("CSAK_FIXTURE",PERIOD_M15,1);
 Check("M12_precursor_delegates",DetectReEntryDirectionOwnerSignal("CSAK_FIXTURE",DIR_BUY,data)==SIGNAL_CSD);
 data.timeframe=PERIOD_H4;data.candle_time=CSAKTime("CSAK_FIXTURE",PERIOD_H4,1);
 ENUM_SIGNAL_TYPE signal=ClassifyH4AuthoritativeSignal("CSAK_FIXTURE",DIR_BUY,data);
 Check("M11_classification_delegates",signal==SIGNAL_CSD);
 data.is_closed=false;
 Check("D1_watch_live_data_rejected",!DetectD1OpportunityCSD("CSAK_FIXTURE",data,d1Band,DIR_BUY));
 Check("M11_live_data_rejected",ClassifyH4AuthoritativeSignal("CSAK_FIXTURE",DIR_BUY,data)==SIGNAL_NONE);
 PairState state;InitPairState(state);
 ApplyH4AuthoritativeEvent(state,DIR_BUY,signal,data.candle_time,false);
 Check("M11_owner_identity",state.h4_direction_owner.SourceSignal==SIGNAL_CSD && state.h4_direction_owner.Direction==DIR_BUY && state.h4_direction_owner.SourceCandleTime==data.candle_time);
 ApplyH4AuthoritativeEvent(state,DIR_BUY,signal,data.candle_time,false);
 Check("same_candle_owner_identity_stable",state.h4_direction_owner.SourceCandleTime==data.candle_time && state.h4_direction_owner.Direction==DIR_BUY);
 Check("no_orders",OrdersTotal()==0 && OrdersHistoryTotal()==0);
 Print("[CUSTOM-CSAK-SUMMARY] passed=",passed," failed=",failed);
 return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
