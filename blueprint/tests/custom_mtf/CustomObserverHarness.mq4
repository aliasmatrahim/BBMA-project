#property strict
input bool ObserverM09=false;
// Broker bar/quote fixtures only; call the actual observer and owner projection.
datetime simulatedNow=D'2026.08.03 10:00';datetime simulatedQuote=simulatedNow;datetime m1Open=simulatedNow;
datetime ObserverTime(string symbol,int timeframe,int shift)
{
 if(timeframe==PERIOD_M1 && shift>=0 && shift<51)return m1Open-shift*60;
 if(timeframe==PERIOD_H1 && shift>=0 && shift<51)return D'2026.08.03 10:00'-shift*3600;
 if(shift>1)return 0;
 if(timeframe==PERIOD_M1)return shift==0?m1Open:m1Open-60;
 if(timeframe==PERIOD_M15)return shift==0?D'2026.08.03 10:00':D'2026.08.03 09:45';
 if(timeframe==PERIOD_H1)return shift==0?D'2026.08.03 10:00':D'2026.08.03 09:00';
 return 0;
}
double ObserverMarketInfo(string symbol,int mode){if(mode==MODE_TIME)return (double)simulatedQuote;return 0;}
int ObserverBars(string symbol,int tf){return tf==PERIOD_M1 || tf==PERIOD_H1?51:iBars(symbol,tf);}
double ObserverClose(string symbol,int tf,int shift){return tf==PERIOD_M1 || tf==PERIOD_H1?1.5:iClose(symbol,tf,shift);}
double ObserverHigh(string symbol,int tf,int shift){return tf==PERIOD_M1?1.6:iHigh(symbol,tf,shift);}
double ObserverLow(string symbol,int tf,int shift){return tf==PERIOD_M1?1.4:iLow(symbol,tf,shift);}
double ObserverMA(string symbol,int tf,int period,int offset,int method,int price,int shift){if(tf==PERIOD_M1)return price==PRICE_HIGH?1.6:(price==PRICE_LOW?1.4:1.5);return iMA(symbol,tf,period,offset,method,price,shift);}
#define iBars ObserverBars
#define iClose ObserverClose
#define iHigh ObserverHigh
#define iLow ObserverLow
#define iMA ObserverMA
#define iTime ObserverTime
#define MarketInfo ObserverMarketInfo
#define OnInit CanonicalOnInit
#define OnDeinit CanonicalOnDeinit
#define OnTick CanonicalOnTick
#define OnTimer CanonicalOnTimer
#include "..\\..\\source\\BBMA_EA.mq4"
#undef iBars
#undef iClose
#undef iHigh
#undef iLow
#undef iMA
#undef iTime
#undef MarketInfo
#undef OnInit
#undef OnDeinit
#undef OnTick
#undef OnTimer
#ifdef CUSTOM_OBSERVER_BASELINE
#include "..\\..\\source\\custom_mtf\\CustomClock.mqh"
#include "..\\..\\source\\custom_mtf\\CustomOwners.mqh"
CustomClockState g_custom_clock_states[MAX_PAIRS];CustomOwnerFrame g_custom_owner_frames[MAX_PAIRS];
void ObserveCustomClosedBars(int index){}
#endif
int passed=0,failed=0;
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[CUSTOM-OBSERVER] ",name," ",ok?"PASS":"FAIL");}
int OnInit()
{
 ResetCustomSymbolInputs();
 ArrayResize(g_custom_universe,1);g_custom_universe[0]="GBPUSD";
 for(int slot=0;slot<CUSTOM_SLOT_COUNT;slot++)
 {
  g_custom_slots[slot].slotId=slot+1;g_custom_slots[slot].enabled=false;
  g_custom_slots[slot].context.atomCount=0;g_custom_slots[slot].context.groupCount=0;
  g_custom_slots[slot].trigger.atomCount=0;g_custom_slots[slot].trigger.groupCount=0;
 }
 g_pair_count=1;InitPairState(g_pair_states[0]);g_pair_states[0].actual_symbol="GBPUSD";g_pair_canonical_scope[0]=true; // Prevalidated canonical H1 owner fixture.
 ArrayResize(g_custom_pair_indices,1);g_custom_pair_indices[0]=0;ZeroMemory(g_custom_use);
 g_custom_use.tfEnabled[0]=true;g_custom_use.tfEnabled[4]=true;g_custom_use.signalEnabled[9]=true;g_custom_use.signalEnabled[44]=true;
 g_pair_states[0].h1_data.timeframe=PERIOD_H1;g_pair_states[0].h1_data.barIndex=1;g_pair_states[0].h1_data.is_valid=true;g_pair_states[0].h1_data.is_closed=true;g_pair_states[0].h1_data.candle_time=simulatedNow-3600;
 ReEntryData re;ZeroMemory(re);re.Timeframe=PERIOD_H1;re.Direction=DIR_BUY;re.State=RE_STATE_CONFIRMED;re.Type=RE_TYPE_1;re.IsValid=true;re.EntryPrice=1.2;re.ConfirmationCandle=simulatedNow-7200;re.StartCandleTime=simulatedNow-10800;re.LastUpdateCandleTime=simulatedNow-3600;re.EntryCandle=simulatedNow-3600;g_pair_states[0].re_h1_buy_state=re;
 if(ObserverM09)
 {
  g_custom_use.signalEnabled[44]=false;g_custom_use.signalEnabled[50]=true;
  TimeframeData data=g_pair_states[0].h1_data;data.open=1.4;data.close=1.5;data.low=1.3;data.high=1.7;data.point=0.00001;data.data_count=1001;
  data.ma[0]=1.7;data.ma[1]=1.8;data.ma[2]=1.3;data.ma[3]=1.2;data.ma[4]=1.5;data.bollinger[0]=2;data.bollinger[1]=1.5;data.bollinger[2]=1;
  CustomAuxLifecycle owner;ZeroMemory(owner);
  owner.extremeBuy.Direction=DIR_BUY;owner.extremeBuy.Timeframe=PERIOD_H1;owner.extremeBuy.Maturity=EXT_MAT_REVERSAL_CONFIRMED;owner.extremeBuy.IsValid=true;
  owner.extremeBuy.RawCandleTime=simulatedNow-4*3600;owner.extremeBuy.ConfirmationCandleTime=simulatedNow-3*3600;owner.extremeBuy.LastUpdateCandleTime=data.candle_time;
  owner.extremeSell=owner.extremeBuy;owner.extremeSell.Direction=DIR_SELL;
  owner.mhvBuy.Direction=DIR_BUY;owner.mhvBuy.ParentExtremeDirection=DIR_SELL;owner.mhvBuy.Timeframe=PERIOD_H1;owner.mhvBuy.State=MLV_DIRECTION_TAKEN;owner.mhvBuy.IsValid=true;
  owner.mhvBuy.ParentRawCandleTime=owner.extremeSell.RawCandleTime;owner.mhvBuy.ParentConfirmationCandleTime=owner.extremeSell.ConfirmationCandleTime;
  owner.mhvBuy.StartCandleTime=simulatedNow-3*3600;owner.mhvBuy.ConfirmationCandleTime=simulatedNow-2*3600;owner.mhvBuy.LastUpdateCandleTime=simulatedNow-2*3600;owner.mhvBuy.FrozenMarkedBody=1.2;owner.mhvBuy.PreviousClose=1.4;
  owner.mhvSell=owner.mhvBuy;owner.mhvSell.Direction=DIR_SELL;owner.mhvSell.ParentExtremeDirection=DIR_BUY;
  StoreCustomCanonicalSource(0,PERIOD_H1,data,owner);g_processed_candle_time[0]=simulatedNow-900;
 }
 g_custom_config_payload=BuildCustomResolvedConfigurationPayload();
 g_processing_time=simulatedNow;ObserveCustomClosedBars(0);Check("driver_primes_without_historical_frame",g_custom_owner_frames[0].viewCount==0 && g_custom_clock_states[0].primed[0]);
 simulatedNow+=60;simulatedQuote=simulatedNow;m1Open=simulatedNow;g_processing_time=simulatedNow;ObserveCustomClosedBars(0);
 bool frameReady=g_custom_owner_frames[0].viewCount==4;
 Check("M1_event_projects_current_H1_owner",frameReady && g_custom_owner_frames[0].observedAt==simulatedNow && g_custom_owner_frames[0].views[0].timeframe==PERIOD_H1 && g_custom_owner_frames[0].views[0].structuralValid && !g_custom_owner_frames[0].views[0].entryEligible && g_custom_owner_frames[0].views[2].readable && !g_custom_owner_frames[0].views[2].structuralValid && !g_custom_owner_frames[0].views[2].entryEligible);
 datetime epoch=g_custom_owner_frames[0].observedAt;simulatedNow++;simulatedQuote=simulatedNow;g_processing_time=simulatedNow;ObserveCustomClosedBars(0);
 Check("duplicate_clears_stale_frame_without_replay",g_custom_owner_frames[0].viewCount==0 && g_custom_clock_states[0].lastClosed[0]==epoch-60 && g_custom_clock_states[0].lastOpen[0]==epoch);
 simulatedQuote=D'2026.08.03 09:59';ObserveCustomClosedBars(0);
 Check("stale_quote_hides_frame_without_consuming",g_custom_owner_frames[0].viewCount==0 && g_custom_clock_states[0].lastClosed[0]==D'2026.08.03 10:00' && !g_custom_clock_states[0].busy);
 Print("[CUSTOM-OBSERVER-SUMMARY] passed=",passed," failed=",failed);return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}