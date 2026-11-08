#property strict
// Broker bar/quote fixtures only; call the actual observer and owner projection.
datetime simulatedNow=D'2026.08.03 10:00';datetime simulatedQuote=simulatedNow;datetime m1Open=simulatedNow;
datetime ObserverTime(string symbol,int timeframe,int shift)
{
 if(shift>1)return 0;
 if(timeframe==PERIOD_M1)return shift==0?m1Open:m1Open-60;
 if(timeframe==PERIOD_H1)return shift==0?D'2026.08.03 10:00':D'2026.08.03 09:00';
 return 0;
}
double ObserverMarketInfo(string symbol,int mode){if(mode==MODE_TIME)return (double)simulatedQuote;return 0;}
#define iTime ObserverTime
#define MarketInfo ObserverMarketInfo
#define OnInit CanonicalOnInit
#define OnDeinit CanonicalOnDeinit
#define OnTick CanonicalOnTick
#define OnTimer CanonicalOnTimer
#include "..\\..\\source\\BBMA_EA.mq4"
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
 g_pair_count=1;InitPairState(g_pair_states[0]);g_pair_states[0].actual_symbol="GBPUSD";
 ArrayResize(g_custom_pair_indices,1);g_custom_pair_indices[0]=0;ZeroMemory(g_custom_use);
 g_custom_use.tfEnabled[0]=true;g_custom_use.tfEnabled[4]=true;g_custom_use.signalEnabled[10]=true;g_custom_use.signalEnabled[44]=true;
 g_pair_states[0].h1_data.timeframe=PERIOD_H1;g_pair_states[0].h1_data.barIndex=1;g_pair_states[0].h1_data.is_valid=true;g_pair_states[0].h1_data.is_closed=true;g_pair_states[0].h1_data.candle_time=simulatedNow-3600;
 ReEntryData re;ZeroMemory(re);re.Timeframe=PERIOD_H1;re.Direction=DIR_BUY;re.State=RE_STATE_CONFIRMED;re.Type=RE_TYPE_1;re.IsValid=true;re.EntryPrice=1.2;re.ConfirmationCandle=simulatedNow-7200;re.StartCandleTime=simulatedNow-10800;re.LastUpdateCandleTime=simulatedNow-3600;re.EntryCandle=simulatedNow-3600;g_pair_states[0].re_h1_buy_state=re;
 g_processing_time=simulatedNow;ObserveCustomClosedBars(0);Check("driver_primes_without_historical_frame",g_custom_owner_frames[0].viewCount==0 && g_custom_clock_states[0].primed[0]);
 simulatedNow+=60;simulatedQuote=simulatedNow;m1Open=simulatedNow;g_processing_time=simulatedNow;ObserveCustomClosedBars(0);
 bool frameReady=g_custom_owner_frames[0].viewCount==4;
 Check("M1_event_projects_current_H1_owner",frameReady && g_custom_owner_frames[0].observedAt==simulatedNow && g_custom_owner_frames[0].views[0].timeframe==PERIOD_H1 && g_custom_owner_frames[0].views[0].structuralValid && !g_custom_owner_frames[0].views[0].entryEligible && !g_custom_owner_frames[0].views[2].readable);
 datetime epoch=g_custom_owner_frames[0].observedAt;simulatedNow++;simulatedQuote=simulatedNow;g_processing_time=simulatedNow;ObserveCustomClosedBars(0);
 Check("duplicate_does_not_relabel_snapshot",g_custom_owner_frames[0].viewCount==4 && g_custom_owner_frames[0].observedAt==epoch);
 simulatedQuote=D'2026.08.03 09:59';ObserveCustomClosedBars(0);
 Check("stale_quote_hides_frame_without_consuming",g_custom_owner_frames[0].viewCount==0 && g_custom_clock_states[0].lastClosed[0]==D'2026.08.03 10:00' && !g_custom_clock_states[0].busy);
 Print("[CUSTOM-OBSERVER-SUMMARY] passed=",passed," failed=",failed);return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
