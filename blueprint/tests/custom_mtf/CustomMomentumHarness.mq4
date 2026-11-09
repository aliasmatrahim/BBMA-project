#property strict
#define OnInit CanonicalOnInit
#define OnDeinit CanonicalOnDeinit
#define OnTick CanonicalOnTick
#define OnTimer CanonicalOnTimer
#include "..\\..\\source\\BBMA_EA.mq4"
#undef OnInit
#undef OnDeinit
#undef OnTick
#undef OnTimer
bool Frozen600DetectCSM(string pair, int timeframe, ENUM_DIRECTION direction, int shift)
{
   if(direction != DIR_BUY && direction != DIR_SELL) return false;
   if(shift < 1) return false;

   double close = iClose(pair, timeframe, shift);
   if(close <= 0) return false;

   BollingerBand currentBand, previousBand;
   ZeroMemory(currentBand);
   ZeroMemory(previousBand);
   CalculateBollinger(pair, timeframe, shift, currentBand);
   CalculateBollinger(pair, timeframe, shift + 1, previousBand);

   if(currentBand.TOP_BB <= 0 || currentBand.MID_BB <= 0 ||
      currentBand.LOW_BB <= 0 || currentBand.Width <= 0 ||
      previousBand.TOP_BB <= 0 || previousBand.MID_BB <= 0 ||
      previousBand.LOW_BB <= 0 || previousBand.Width <= 0)
      return false;

   bool bbExpanding = (currentBand.Width > previousBand.Width);

   if(direction == DIR_BUY)
   {
      bool bbDirectional = (currentBand.MID_BB > previousBand.MID_BB &&
                            currentBand.TOP_BB > previousBand.TOP_BB);
      return (bbExpanding && bbDirectional && close > currentBand.TOP_BB);
   }

   bool bbDirectional = (currentBand.MID_BB < previousBand.MID_BB &&
                         currentBand.LOW_BB < previousBand.LOW_BB);
   return (bbExpanding && bbDirectional && close < currentBand.LOW_BB);
}

int passed=0,failed=0;
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[CUSTOM-MOMENTUM] ",name," ",ok?"PASS":"FAIL");}
int OnInit()
{
 g_pair_count=2;for(int p=0;p<2;p++){InitPairState(g_pair_states[p]);g_pair_states[p].actual_symbol=p==0?Symbol():"UNAVAILABLE_SYMBOL_FIXTURE";}
 for(int t=0;t<7;t++)
 {
  int tf=CustomTFValue(t);bool equivalent=true;int positive=0;M10MomentumSnapshot snapshot;
  for(int shift=1;shift<=100;shift++)for(int side=0;side<2;side++)
  {
   ENUM_DIRECTION direction=side==0?DIR_BUY:DIR_SELL;
   bool original=Frozen600DetectCSM(Symbol(),tf,direction,shift);
   bool shared=DetectCSM(Symbol(),tf,direction,shift);
   if(shared!=original)equivalent=false;if(original)positive++;
  }
  Check("frozen600_equivalence_200_"+IntegerToString(tf),equivalent);
  bool ready=ReadM10MomentumSnapshot(Symbol(),tf,1,snapshot);
  datetime latest=iTime(Symbol(),tf,1);
  Check("ready_current_closed_snapshot_"+IntegerToString(tf),ready && snapshot.sourceBar==latest && snapshot.timeframe==tf && snapshot.symbol==Symbol());
  bool original=snapshot.buy;g_pair_states[0].m10_momentum[t].buy=!original;
  M10MomentumSnapshot duplicate;ReadM10MomentumSnapshot(Symbol(),tf,1,duplicate);
  Check("opposite_direction_reuses_same_calculation_"+IntegerToString(tf),duplicate.buy==!original && duplicate.sell==snapshot.sell);
  g_pair_states[0].m10_momentum[t]=snapshot;
  ReadM10MomentumSnapshot(Symbol(),tf,8,duplicate);
  Check("historical_query_does_not_evict_current_"+IntegerToString(tf),g_pair_states[0].m10_momentum[t].sourceBar==latest && g_pair_states[0].m10_momentum[t+7].sourceBar==iTime(Symbol(),tf,8));
  g_pair_states[0].m10_momentum[t].closes[3]+=1;g_pair_states[0].m10_momentum[t].buy=!original;
  ReadM10MomentumSnapshot(Symbol(),tf,1,duplicate);
  Check("changed_fingerprint_rebuilds_"+IntegerToString(tf),duplicate.buy==original && duplicate.closes[3]==snapshot.closes[3]);
  g_pair_states[0].m10_momentum[t].ready=false;g_pair_states[0].m10_momentum[t].buy=!original;
  ReadM10MomentumSnapshot(Symbol(),tf,1,duplicate);
  Check("unready_snapshot_retries_"+IntegerToString(tf),duplicate.ready && duplicate.buy==original);
  CustomOwnerView view;bool readable=ReadCustomOwnerView(0,tf,"MOM",DIR_BUY,latest,view);
  Check("diagnostic_only_projection_"+IntegerToString(tf),readable && view.readable && view.structuralValid==original && view.recoveryOnly && !view.entryWindowOpen && !view.entryEligible && !view.executionAvailable);
  Print("[CUSTOM-MOMENTUM-DATA] tf=",tf," comparisons=200 positive=",positive);
 }
 M10MomentumSnapshot missing;
 Check("missing_symbol_isolated",!ReadM10MomentumSnapshot(g_pair_states[1].actual_symbol,PERIOD_M1,1,missing) && !g_pair_states[1].m10_momentum[0].ready);
 Check("live_candle_rejected",!ReadM10MomentumSnapshot(Symbol(),PERIOD_M1,0,missing) && !DetectCSM(Symbol(),PERIOD_M1,DIR_BUY,0));
 Check("invalid_direction_rejected",!DetectCSM(Symbol(),PERIOD_M1,DIR_NONE,1));
 CustomOwnerView view;datetime latest=iTime(Symbol(),PERIOD_M1,1);
 Check("stale_projection_rejected",!ReadCustomOwnerView(0,PERIOD_M1,"MOM",DIR_BUY,latest-60,view));
 Check("CSA_CSAK_remain_unavailable",!ReadCustomOwnerView(0,PERIOD_M1,"CSA",DIR_BUY,latest,view) && !ReadCustomOwnerView(0,PERIOD_M1,"CSAK",DIR_BUY,latest,view));
 Check("no_orders",OrdersTotal()==0 && OrdersHistoryTotal()==0);
 Print("[CUSTOM-MOMENTUM-SUMMARY] passed=",passed," failed=",failed);return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
