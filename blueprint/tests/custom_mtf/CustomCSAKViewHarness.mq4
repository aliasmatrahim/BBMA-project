#property strict
// Real M10/observer with controlled platform series; actual history is checked separately.
datetime fixtureNow=D'2026.08.03 10:00';int fixtureBars=40,openReads=0,closeReads=0;
double fixtureClose=102;int missingShift=-1;double fixtureHighMA=100,fixtureLowMA=100;int missingHighShift=-1;bool badChronology=false,mutateDuringRead=false;
bool IsCSAFixture(string s){return s=="CSA_A" || s=="CSA_B";}
datetime CSATime(string s,int tf,int shift)
{
 if(!IsCSAFixture(s))return iTime(s,tf,shift);
 if(shift<0 || shift>=fixtureBars)return 0;
 if(badChronology && shift==4)shift=3;
 return fixtureNow-shift*tf*60;
}
double CSAClose(string s,int tf,int shift)
{
 if(!IsCSAFixture(s))return iClose(s,tf,shift);
 closeReads++;if(mutateDuringRead && closeReads==21)fixtureClose=98;
 if(shift<0 || shift>=fixtureBars || shift==missingShift)return 0;
 if(shift==1)return s=="CSA_B"?98:fixtureClose;
 return 100;
}
int CSABars(string s,int tf){return IsCSAFixture(s)?fixtureBars:iBars(s,tf);}
double CSAOpen(string s,int tf,int shift){if(IsCSAFixture(s)){openReads++;return 300;}return iOpen(s,tf,shift);}
double CSAMarketInfo(string s,int mode){if(IsCSAFixture(s)&&mode==MODE_TIME)return (double)fixtureNow;return MarketInfo(s,mode);}
double CSAHigh(string s,int tf,int shift){if(IsCSAFixture(s))return shift==missingHighShift?0:110;return iHigh(s,tf,shift);}
double CSALow(string s,int tf,int shift){if(IsCSAFixture(s))return 90;return iLow(s,tf,shift);}
double CSAMA(string s,int tf,int period,int maShift,int method,int price,int shift)
{
 if(IsCSAFixture(s))return price==PRICE_HIGH?fixtureHighMA:fixtureLowMA;
 return iMA(s,tf,period,maShift,method,price,shift);
}
#define iHigh CSAHigh
#define iLow CSALow
#define iMA CSAMA
#define iTime CSATime
#define iClose CSAClose
#define iOpen CSAOpen
#define iBars CSABars
#define MarketInfo CSAMarketInfo
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
#undef iClose
#undef iOpen
#undef iBars
#undef MarketInfo
#undef iHigh
#undef iLow
#undef iMA
int passed=0,failed=0;
void Check(string label,bool ok){if(ok)passed++;else failed++;Print("[CUSTOM-CSAKVIEW] ",label," ",ok?"PASS":"FAIL");}
void ResetSources()
{
 for(int p=0;p<g_pair_count;p++)for(int i=0;i<14;i++){ZeroMemory(g_pair_states[p].m10_csak[i]);ZeroMemory(g_pair_states[p].m10_csa[i]);ZeroMemory(g_pair_states[p].m10_momentum[i]);}
 fixtureHighMA=100;fixtureLowMA=100;missingHighShift=-1;fixtureBars=40;fixtureClose=102;missingShift=-1;badChronology=false;mutateDuringRead=false;closeReads=0;openReads=0;
}
int OnInit()
{
 g_pair_count=3;for(int p=0;p<3;p++){InitPairState(g_pair_states[p]);g_pair_states[p].actual_symbol=p==0?"CSA_A":(p==1?"CSA_B":Symbol());}
 for(int t=0;t<7;t++)
 {
  ResetSources();int tf=CustomTFValue(t);string label=IntegerToString(tf)+"_";M10MomentumSnapshot s,other;
  Check(label+"ready_close_above_mid",ReadM10CSAKSnapshot("CSA_A",tf,1,s) && s.buy && !s.sell && s.inputCount==20 && MathAbs(s.currentBand.MID_BB-100.1)<0.000001);
  Check(label+"Open_never_read",openReads==0);
  datetime latest=CSATime("CSA_A",tf,1);CustomOwnerView buy,sell,repeat;
  Check(label+"buy_context_only",ReadCustomOwnerView(0,tf,"CSAK",DIR_BUY,latest,buy) && buy.readable && buy.structuralValid && buy.recoveryOnly && !buy.entryWindowOpen && !buy.entryEligible && !buy.executionAvailable && buy.confirmation==latest && StringLen(buy.eventId)>0);
  bool sellReadable=ReadCustomOwnerView(0,tf,"CSAK",DIR_SELL,latest,sell);
  Print("[CUSTOM-CSAKVIEW-DIAG] tf=",tf," return=",sellReadable," readable=",sell.readable," valid=",sell.structuralValid," confirmation=",(int)sell.confirmation," eventLen=",StringLen(sell.eventId)," emptyEquality=",sell.eventId=="");
  Check(label+"false_is_readable_not_unavailable",sellReadable && sell.readable && !sell.structuralValid && sell.confirmation==0 && StringLen(sell.eventId)==0);
  ReadM10CSAKSnapshot("CSA_A",tf,1,s);ReadCustomOwnerView(0,tf,"CSAK",DIR_BUY,latest,repeat);
  Check(label+"duplicate_identity_stable",repeat.eventId==buy.eventId && repeat.confirmation==buy.confirmation);
  Check(label+"stale_owner_rejected",!ReadCustomOwnerView(0,tf,"CSAK",DIR_BUY,latest-60,repeat));
  Check(label+"CSA_still_readable",ReadCustomOwnerView(0,tf,"CSA",DIR_BUY,latest,repeat) && repeat.structuralValid);
  Check(label+"second_symbol_independent",ReadM10CSAKSnapshot("CSA_B",tf,1,other) && !other.buy && other.sell && g_pair_states[0].m10_csak[t].buy);
  ReadCustomOwnerView(1,tf,"CSAK",DIR_SELL,latest,repeat);
  Check(label+"symbol_direction_identity_separate",repeat.eventId!=buy.eventId && repeat.symbol=="CSA_B");
  ReadM10CSAKSnapshot("CSA_A",tf,8,other);
  Check(label+"historical_does_not_evict_current",g_pair_states[0].m10_csak[t].sourceBar==latest && g_pair_states[0].m10_csak[t+7].sourceBar==CSATime("CSA_A",tf,8));
  fixtureClose=98;ReadM10CSAKSnapshot("CSA_A",tf,1,other);
  Check(label+"history_revision_reclassifies",!other.buy && other.sell && MathAbs(other.currentBand.MID_BB-99.9)<0.000001);
  fixtureClose=100;ReadM10CSAKSnapshot("CSA_A",tf,1,other);
  Check(label+"equality_valid_false",other.ready && !other.buy && !other.sell);
  ResetSources();fixtureBars=21;
  Check(label+"current20_sufficient",ReadM10CSAKSnapshot("CSA_A",tf,1,other) && other.buy);
  Check(label+"previous_MOM_candle_not_required",!ReadM10MomentumSnapshot("CSA_A",tf,1,s) && other.ready);
  ResetSources();ReadM10MomentumSnapshot("CSA_A",tf,1,s);closeReads=0;
  Check(label+"reuse_shared_M10_current_band",ReadM10CSAKSnapshot("CSA_A",tf,1,other) && other.currentBand.MID_BB==s.currentBand.MID_BB);
  ResetSources();fixtureBars=20;
  Check(label+"short_current_history_unavailable",!ReadM10CSAKSnapshot("CSA_A",tf,1,other));
  ResetSources();missingShift=9;
  Check(label+"missing_input_unavailable",!ReadM10CSAKSnapshot("CSA_A",tf,1,other));
  ResetSources();badChronology=true;
  Check(label+"unordered_input_unavailable",!ReadM10CSAKSnapshot("CSA_A",tf,1,other));
  ResetSources();mutateDuringRead=true;
  Check(label+"in_read_revision_not_cached",!ReadM10CSAKSnapshot("CSA_A",tf,1,other) && !g_pair_states[0].m10_csak[t].ready);
  ResetSources();
  Check(label+"live_negative_shift_rejected",!ReadM10CSAKSnapshot("CSA_A",tf,0,other) && !ReadM10CSAKSnapshot("CSA_A",tf,-1,other));
  ResetSources();fixtureHighMA=103;ReadM10CSAKSnapshot("CSA_A",tf,1,other);
  Check(label+"Mid_only_not_CSAK",other.ready && !other.buy && g_pair_states[0].m10_csa[t].buy);
  ResetSources();fixtureLowMA=97;fixtureClose=98;ReadM10CSAKSnapshot("CSA_A",tf,1,other);
  Check(label+"sell_Mid_only_not_CSAK",other.ready && !other.sell && g_pair_states[0].m10_csa[t].sell);
  ResetSources();missingHighShift=5;
  Check(label+"missing_high_unavailable",!ReadM10CSAKSnapshot("CSA_A",tf,1,other));
  ResetSources();fixtureHighMA=0;
  Check(label+"missing_MA_unavailable",!ReadM10CSAKSnapshot("CSA_A",tf,1,other));
  ResetSources();
  bool ready=true,equivalent=true;int positive=0;
  for(int shift=1;shift<=10;shift++)
  {
   M10MomentumSnapshot real;bool ok=ReadM10CSAKSnapshot(Symbol(),tf,shift,real);double mid=iMA(Symbol(),tf,20,0,MODE_SMA,PRICE_CLOSE,shift),close=iClose(Symbol(),tf,shift);
   if(!ok || mid<=0 || close<=0)ready=false;
   if(!ok || MathAbs(real.currentBand.MID_BB-mid)>0.0000001 || real.buy!=(close>mid && close>iMA(Symbol(),tf,5,0,MODE_LWMA,PRICE_HIGH,shift) && close>iMA(Symbol(),tf,10,0,MODE_LWMA,PRICE_HIGH,shift)) || real.sell!=(close<mid && close<iMA(Symbol(),tf,5,0,MODE_LWMA,PRICE_LOW,shift) && close<iMA(Symbol(),tf,10,0,MODE_LWMA,PRICE_LOW,shift)))equivalent=false;
   if(close>mid || close<mid)positive++;
  }
  Check(label+"actual_history_20_direction_comparisons",ready && equivalent);
  Print("[CUSTOM-CSAKVIEW-DATA] tf=",tf," comparisons=20 positives=",positive," M30_declared_fixture=",tf==PERIOD_M30);
 }
 ResetSources();ArrayResize(g_custom_pair_indices,1);g_custom_pair_indices[0]=0;ZeroMemory(g_custom_use);
 g_custom_use.tfEnabled[0]=true;g_custom_use.signalEnabled[9]=true;g_processing_time=fixtureNow;
 ObserveCustomClosedBars(0);
 Check("observer_prime_no_historical_trigger",g_custom_owner_frames[0].viewCount==0 && g_custom_clock_states[0].primed[0] && g_pair_states[0].m10_csak[0].ready);
 fixtureNow+=60;g_processing_time=fixtureNow;ObserveCustomClosedBars(0);
 Check("observer_CSA_only_publishes_closed_context",g_custom_owner_frames[0].viewCount==2 && g_custom_owner_frames[0].views[0].structuralValid && g_custom_owner_frames[0].views[0].sourceBar==fixtureNow-60 && !g_custom_owner_frames[0].views[0].entryEligible && g_pair_states[0].custom_aux[0].lastClosed==0);
 string id=g_custom_owner_frames[0].views[0].eventId;datetime observed=g_custom_owner_frames[0].observedAt;ObserveCustomClosedBars(0);
 Check("observer_duplicate_stable",g_custom_owner_frames[0].views[0].eventId==id && g_custom_owner_frames[0].observedAt==observed);
 fixtureNow+=60;g_processing_time=fixtureNow;missingShift=9;ObserveCustomClosedBars(0);
 Check("missing_data_batch_not_consumed",g_custom_owner_frames[0].viewCount==0 && g_custom_clock_states[0].lastClosed[0]==fixtureNow-120 && !g_custom_clock_states[0].busy);
 missingShift=-1;ObserveCustomClosedBars(0);
 Check("recovered_data_retries_same_bar_context_only",g_custom_owner_frames[0].viewCount==2 && g_custom_owner_frames[0].views[0].sourceBar==fixtureNow-60 && g_custom_owner_frames[0].views[0].recoveryOnly && !g_custom_owner_frames[0].views[0].entryWindowOpen);
 Check("invalid_direction_unavailable",!ReadCustomOwnerView(0,PERIOD_M1,"CSAK",DIR_NONE,fixtureNow-60,g_custom_owner_frames[0].views[0]));
 Check("no_orders",OrdersTotal()==0 && OrdersHistoryTotal()==0);
 Print("[CUSTOM-CSAKVIEW-SUMMARY] passed=",passed," failed=",failed);return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
