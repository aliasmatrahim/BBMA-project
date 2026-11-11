#property strict
// Accepted Close-only characterization: synthetic OHLC, actual canonical detector bodies.
double fixtureOpen=99,fixtureClose=102;
double DirectionFixtureOpen(string symbol,int tf,int shift){return fixtureOpen;}
double DirectionFixtureClose(string symbol,int tf,int shift){return fixtureClose;}
#define iOpen DirectionFixtureOpen
#define iClose DirectionFixtureClose
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
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[CUSTOM-DIRECTION] ",name," ",ok?"PASS":"FAIL");}
int OnInit()
{
 double opens[10]={99,100.5,99,99,99,101,99.5,101,101,99};
 double closes[10]={102,102,100.5,102,100,98,98,99.5,100,102};
 double ma5[10]={101,101,101,101,99.2,99,99,99,100.8,101};
 double ma10[10]={101.5,101.5,101.5,103,99.5,98.5,98.5,98.5,100.5,101.5};
 bool csd[10]={true,true,false,false,false,true,true,false,false,false};
 bool ecsd[10]={true,true,false,false,true,true,true,false,true,false};
 string names[10]={"buy_full_span","buy_open_above_mid","buy_mid_only","buy_incomplete_ma_pair","buy_close_at_mid","sell_full_span","sell_open_below_mid","sell_mid_only","sell_close_at_mid","invalid_direction"};
 for(int t=0;t<7;t++)for(int c=0;c<10;c++)
 {
  int tf=CustomTFValue(t);fixtureOpen=opens[c];fixtureClose=closes[c];
  ENUM_DIRECTION side=c==9?DIR_NONE:(c<5?DIR_BUY:DIR_SELL);
  MovingAverage ma;BollingerBand band;ZeroMemory(ma);ZeroMemory(band);
  ma.MA5_High=ma5[c];ma.MA10_High=ma10[c];ma.MA5_Low=ma5[c];ma.MA10_Low=ma10[c];band.MID_BB=100;
  string label=IntegerToString(tf)+"_"+names[c];
  Check(label+"_CSD",DetectCSD(Symbol(),tf,side,1,ma,band)==csd[c]);
  Check(label+"_eCSD",DetectECSD(Symbol(),tf,side,1,ma)==ecsd[c]);
 }
 Check("no_orders",OrdersTotal()==0 && OrdersHistoryTotal()==0);
 Print("[CUSTOM-DIRECTION-SUMMARY] passed=",passed," failed=",failed);
 return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
