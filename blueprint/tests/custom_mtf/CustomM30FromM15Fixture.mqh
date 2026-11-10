#ifndef SIG06_M30_FROM_M15_FIXTURE
#define SIG06_M30_FROM_M15_FIXTURE
// Read-only test adapter: every closed M30 OHLC derives from two existing M15 bars.
struct Sig06M30Bar {datetime time;double open;double high;double low;double close;};
Sig06M30Bar Sig06M30Bars[];
double Sig06M30High[],Sig06M30Low[],Sig06M30Close[];
bool Sig06FixtureKey(string s,int tf){return s==Symbol() && tf==PERIOD_M30;}
bool Sig06LoadM30Fixture()
{
 int h=FileOpen("sig06_mhv_m30_from_m15_v5.csv",FILE_READ|FILE_CSV|FILE_ANSI,';');if(h==INVALID_HANDLE)return false;
 for(int k=0;k<7;k++)FileReadString(h);
 ArrayResize(Sig06M30Bars,1);int count=0;
 while(!FileIsEnding(h))
 {
  string ts=FileReadString(h);if(StringLen(ts)==0)break;datetime time=(datetime)StringToInteger(ts);
  double o=StringToDouble(FileReadString(h)),hi=StringToDouble(FileReadString(h)),lo=StringToDouble(FileReadString(h)),c=StringToDouble(FileReadString(h));
  datetime a=(datetime)StringToInteger(FileReadString(h)),b=(datetime)StringToInteger(FileReadString(h));
  if(time<=0 || time%1800!=0 || a!=time || b!=time+900 || o<=0 || lo<=0 || hi<MathMax(o,c) || lo>MathMin(o,c) || (count>0 && time>=Sig06M30Bars[count].time)){FileClose(h);return false;}
  count++;ArrayResize(Sig06M30Bars,count+1,4096);Sig06M30Bars[count].time=time;Sig06M30Bars[count].open=o;Sig06M30Bars[count].high=hi;Sig06M30Bars[count].low=lo;Sig06M30Bars[count].close=c;
 }
 FileClose(h);if(count<700)return false;
 datetime current=iTime(Symbol(),PERIOD_M15,0);Sig06M30Bars[0].time=current-current%1800;
 if(Sig06M30Bars[0].time<=Sig06M30Bars[1].time)return false;
 Sig06M30Bars[0].open=iOpen(Symbol(),PERIOD_M15,0);Sig06M30Bars[0].high=iHigh(Symbol(),PERIOD_M15,0);Sig06M30Bars[0].low=iLow(Symbol(),PERIOD_M15,0);Sig06M30Bars[0].close=iClose(Symbol(),PERIOD_M15,0);
 ArrayResize(Sig06M30High,count+1);ArrayResize(Sig06M30Low,count+1);ArrayResize(Sig06M30Close,count+1);
 ArraySetAsSeries(Sig06M30High,true);ArraySetAsSeries(Sig06M30Low,true);ArraySetAsSeries(Sig06M30Close,true);
 for(int i=0;i<=count;i++){Sig06M30High[i]=Sig06M30Bars[i].high;Sig06M30Low[i]=Sig06M30Bars[i].low;Sig06M30Close[i]=Sig06M30Bars[i].close;}
 Print("[M30-FIXTURE] complete_M15_pairs=",count," ready=true");return true;
}
bool Sig06VerifyMAArrayOrder()
{
 int n=(int)MathMin(1001,iBars(Symbol(),PERIOD_M15));if(n<100)return false;
 double hi[],lo[],cl[];ArrayResize(hi,n);ArrayResize(lo,n);ArrayResize(cl,n);ArraySetAsSeries(hi,true);ArraySetAsSeries(lo,true);ArraySetAsSeries(cl,true);
 for(int i=0;i<n;i++){hi[i]=iHigh(Symbol(),PERIOD_M15,i);lo[i]=iLow(Symbol(),PERIOD_M15,i);cl[i]=iClose(Symbol(),PERIOD_M15,i);}
 int errors=0,comparisons=0;
 for(int s=1;s<=20;s++)
 {
  comparisons+=5;
  if(MathAbs(iMAOnArray(hi,0,5,0,MODE_LWMA,s)-iMA(Symbol(),PERIOD_M15,5,0,MODE_LWMA,PRICE_HIGH,s))>1e-12)errors++;
  if(MathAbs(iMAOnArray(hi,0,10,0,MODE_LWMA,s)-iMA(Symbol(),PERIOD_M15,10,0,MODE_LWMA,PRICE_HIGH,s))>1e-12)errors++;
  if(MathAbs(iMAOnArray(lo,0,5,0,MODE_LWMA,s)-iMA(Symbol(),PERIOD_M15,5,0,MODE_LWMA,PRICE_LOW,s))>1e-12)errors++;
  if(MathAbs(iMAOnArray(lo,0,10,0,MODE_LWMA,s)-iMA(Symbol(),PERIOD_M15,10,0,MODE_LWMA,PRICE_LOW,s))>1e-12)errors++;
  if(MathAbs(iMAOnArray(cl,0,50,0,MODE_EMA,s)-iMA(Symbol(),PERIOD_M15,50,0,MODE_EMA,PRICE_CLOSE,s))>1e-12)errors++;
 }
 Print("[M30-FIXTURE-MA] comparisons=",comparisons," mismatches=",errors);return errors==0;
}
datetime Sig06DerivedTime(string s,int tf,int shift){if(!Sig06FixtureKey(s,tf))return iTime(s,tf,shift);return shift>=0 && shift<ArraySize(Sig06M30Bars)?Sig06M30Bars[shift].time:0;}
int Sig06DerivedBars(string s,int tf){return Sig06FixtureKey(s,tf)?ArraySize(Sig06M30Bars):iBars(s,tf);}
double Sig06DerivedOpen(string s,int tf,int shift){if(!Sig06FixtureKey(s,tf))return iOpen(s,tf,shift);return shift>=0 && shift<ArraySize(Sig06M30Bars)?Sig06M30Bars[shift].open:0;}
double Sig06DerivedHigh(string s,int tf,int shift){if(!Sig06FixtureKey(s,tf))return iHigh(s,tf,shift);return shift>=0 && shift<ArraySize(Sig06M30Bars)?Sig06M30Bars[shift].high:0;}
double Sig06DerivedLow(string s,int tf,int shift){if(!Sig06FixtureKey(s,tf))return iLow(s,tf,shift);return shift>=0 && shift<ArraySize(Sig06M30Bars)?Sig06M30Bars[shift].low:0;}
double Sig06DerivedClose(string s,int tf,int shift){if(!Sig06FixtureKey(s,tf))return iClose(s,tf,shift);return shift>=0 && shift<ArraySize(Sig06M30Bars)?Sig06M30Bars[shift].close:0;}
int Sig06DerivedShift(string s,int tf,datetime time,bool exact=false)
{
 if(!Sig06FixtureKey(s,tf))return iBarShift(s,tf,time,exact);
 for(int i=0;i<ArraySize(Sig06M30Bars);i++)if(Sig06M30Bars[i].time==time || (!exact && Sig06M30Bars[i].time<time))return i;
 return -1;
}
double Sig06DerivedMA(string s,int tf,int period,int offset,int method,int price,int shift)
{
 if(!Sig06FixtureKey(s,tf))return iMA(s,tf,period,offset,method,price,shift);
 if(price==PRICE_HIGH)return iMAOnArray(Sig06M30High,0,period,offset,method,shift);
 if(price==PRICE_LOW)return iMAOnArray(Sig06M30Low,0,period,offset,method,shift);
 if(price==PRICE_CLOSE)return iMAOnArray(Sig06M30Close,0,period,offset,method,shift);
 return 0;
}
#endif
