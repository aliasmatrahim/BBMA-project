#property strict
// Synthetic detector/consumer fixtures; no orders or canonical controller invoked.
double fixtureOpen=105,fixtureClose=102;
int openReads=0;
double ECSDOpen(string symbol,int tf,int shift){if(symbol=="ECSD_FIXTURE"){openReads++;return fixtureOpen;}return iOpen(symbol,tf,shift);}
double ECSDClose(string symbol,int tf,int shift){if(symbol=="ECSD_FIXTURE")return fixtureClose;return iClose(symbol,tf,shift);}
#define iOpen ECSDOpen
#define iClose ECSDClose
#define OnInit CanonicalOnInit
#define OnDeinit CanonicalOnDeinit
#define OnTick CanonicalOnTick
#define OnTimer CanonicalOnTimer
#include "..\\..\\source\\BBMA_EA.mq4"
#undef OnInit
#undef OnDeinit
#undef OnTick
#undef OnTimer
#undef iOpen
#undef iClose
int passed=0,failed=0;
void Check(string label,bool ok){if(ok)passed++;else failed++;Print("[CUSTOM-ECSD] ",label," ",ok?"PASS":"FAIL");}
int OnInit()
{
 double opens[5]={0,98,100,102,105};
 for(int t=0;t<7;t++)
 {
  int tf=CustomTFValue(t);string tag=IntegerToString(tf);MovingAverage ma;ZeroMemory(ma);
  ma.MA5_High=101;ma.MA10_High=101.5;ma.MA5_Low=99;ma.MA10_Low=98.5;
  openReads=0;fixtureClose=102;
  for(int i=0;i<5;i++){fixtureOpen=opens[i];Check(tag+"_buy_open_independent_"+IntegerToString(i),DetectECSD("ECSD_FIXTURE",tf,DIR_BUY,1,ma));}
  Check(tag+"_buy_no_open_access",openReads==0);
  openReads=0;fixtureClose=98;
  for(int j=0;j<5;j++){fixtureOpen=opens[j];Check(tag+"_sell_open_independent_"+IntegerToString(j),DetectECSD("ECSD_FIXTURE",tf,DIR_SELL,1,ma));}
  Check(tag+"_sell_no_open_access",openReads==0);
  fixtureClose=101;Check(tag+"_buy_equal_ma5_rejected",!DetectECSD("ECSD_FIXTURE",tf,DIR_BUY,1,ma));
  fixtureClose=101.5;Check(tag+"_buy_equal_ma10_rejected",!DetectECSD("ECSD_FIXTURE",tf,DIR_BUY,1,ma));
  fixtureClose=99;Check(tag+"_sell_equal_ma5_rejected",!DetectECSD("ECSD_FIXTURE",tf,DIR_SELL,1,ma));
  fixtureClose=98.5;Check(tag+"_sell_equal_ma10_rejected",!DetectECSD("ECSD_FIXTURE",tf,DIR_SELL,1,ma));
  fixtureClose=102;Check(tag+"_live_candle_rejected",!DetectECSD("ECSD_FIXTURE",tf,DIR_BUY,0,ma));
  Check(tag+"_negative_shift_rejected",!DetectECSD("ECSD_FIXTURE",tf,DIR_BUY,-1,ma));
  Check(tag+"_invalid_direction_rejected",!DetectECSD("ECSD_FIXTURE",tf,DIR_NONE,1,ma));
  fixtureClose=0;Check(tag+"_missing_close_rejected",!DetectECSD("ECSD_FIXTURE",tf,DIR_BUY,1,ma));
  fixtureClose=102;ma.MA5_High=0;Check(tag+"_missing_ma5_rejected",!DetectECSD("ECSD_FIXTURE",tf,DIR_BUY,1,ma));
  ma.MA5_High=101;ma.MA10_High=0;Check(tag+"_missing_ma10_rejected",!DetectECSD("ECSD_FIXTURE",tf,DIR_BUY,1,ma));ma.MA10_High=101.5;
  fixtureOpen=105;openReads=0;BollingerBand bb;ZeroMemory(bb);bb.MID_BB=100;
  Check(tag+"_CSD_close_only",DetectCSD("ECSD_FIXTURE",tf,DIR_BUY,1,ma,bb));
  Check(tag+"_CSD_control_no_open_access",openReads==0);
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
   double close=iClose(Symbol(),sourceTF,shift);
   if(close<=0 || current.MA5_High<=0 || current.MA10_High<=0 || current.MA5_Low<=0 || current.MA10_Low<=0 || iTime(Symbol(),sourceTF,shift)<=0)ready=false;
   bool buy=close>current.MA5_High && close>current.MA10_High;
   bool sell=close<current.MA5_Low && close<current.MA10_Low;
   if(DetectECSD(Symbol(),sourceTF,DIR_BUY,shift,current)!=buy || DetectECSD(Symbol(),sourceTF,DIR_SELL,shift,current)!=sell)equivalent=false;
   if(buy)positives++;if(sell)positives++;
  }
  Check(IntegerToString(sourceTF)+"_actual_history_ready",ready);
  Check(IntegerToString(sourceTF)+"_actual_20_closed_comparisons",equivalent && ready);
  Print("[CUSTOM-ECSD-DATA] tf=",sourceTF," comparisons=20 positives=",positives);
 }
 TimeframeData data;ZeroMemory(data);data.is_valid=true;data.is_closed=true;data.barIndex=1;data.timeframe=PERIOD_D1;data.candle_time=D'2026.08.03 00:00';
 data.ma[0]=101;data.ma[1]=101.5;data.ma[2]=99;data.ma[3]=98.5;data.bollinger[0]=200;data.bollinger[1]=103;data.bollinger[2]=50;
 fixtureOpen=105;fixtureClose=102;
 Check("D1_watch_delegates_closed_predicate",DetectD1OpportunityECSDWatch("ECSD_FIXTURE",data,DIR_BUY));
 data.timeframe=PERIOD_M15;
 Check("M12_precursor_delegates",DetectReEntryDirectionOwnerSignal("ECSD_FIXTURE",DIR_BUY,data)==SIGNAL_ECSD);
 data.timeframe=PERIOD_H4;
 ENUM_SIGNAL_TYPE signal=ClassifyH4AuthoritativeSignal("ECSD_FIXTURE",DIR_BUY,data);
 Check("M11_classification_delegates",signal==SIGNAL_ECSD);
 data.is_closed=false;
 Check("D1_watch_live_data_rejected",!DetectD1OpportunityECSDWatch("ECSD_FIXTURE",data,DIR_BUY));
 Check("M11_live_data_rejected",ClassifyH4AuthoritativeSignal("ECSD_FIXTURE",DIR_BUY,data)==SIGNAL_NONE);
 PairState state;InitPairState(state);
 ApplyH4AuthoritativeEvent(state,DIR_BUY,signal,D'2026.08.03 00:00',false);
 Check("M11_owner_identity",state.h4_direction_owner.SourceSignal==SIGNAL_ECSD && state.h4_direction_owner.Direction==DIR_BUY && state.h4_direction_owner.SourceCandleTime==D'2026.08.03 00:00');
 ApplyH4AuthoritativeEvent(state,DIR_BUY,signal,D'2026.08.03 00:00',false);
 Check("same_candle_owner_identity_stable",state.h4_direction_owner.SourceCandleTime==D'2026.08.03 00:00' && state.h4_direction_owner.Direction==DIR_BUY);
 Check("no_orders",OrdersTotal()==0 && OrdersHistoryTotal()==0);
 Print("[CUSTOM-ECSD-SUMMARY] passed=",passed," failed=",failed);
 return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
