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
void Check(string label,bool ok){if(ok)passed++;else failed++;Print("[MOM-READY] ",label," ",ok?"PASS":"FAIL");}
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
  int tf=CustomTFValue(t);string tag=IntegerToString(tf)+"_case"+IntegerToString(c)+"_";
  ResetGap(c);M10MomentumSnapshot m;bool ready=ReadM10MomentumSnapshot("MOM_GAP",tf,1,m);
  Check(tag+"unavailable_has_no_classification",!ready && !m.buy && !m.sell && !g_pair_states[0].m10_momentum[t].ready);
  ResetGap(c);Check(tag+"raw_rejects_unavailable",!DetectCSM("MOM_GAP",tf,DIR_BUY,1));
  ResetGap(c);TimeframeData data;DataFixture(tf,data);
  Check(tag+"M12_no_weaker_fallback",DetectReEntryDirectionOwnerSignal("MOM_GAP",DIR_BUY,data)==SIGNAL_NONE);
  ResetGap(c);DataFixture(tf,data);ReEntryData re;ResetReEntryState(re,DIR_BUY,tf);re.State=RE_STATE_CANDIDATE;re.Type=RE_TYPE_1;re.LastUpdateCandleTime=data.candle_time-tf*60;re.Reason="retained";ReEntryData oldRE=re;
  UpdateReEntryState(re,"MOM_GAP",DIR_BUY,data);Check(tag+"M12_owner_unchanged",SameReEntryData(re,oldRE));
  ResetGap(c);DataFixture(tf,data);MLVData mlv;ResetMLVState(mlv,DIR_BUY,tf);mlv.State=MLV_TP_COMPLETE;mlv.LastUpdateCandleTime=data.candle_time-tf*60;mlv.PreviousClose=99;mlv.Reason="retained";MLVData oldMLV=mlv;
  ExtremeLifecycleData parent;ResetExtremeLifecycle(parent,DIR_SELL,tf);parent.IsValid=true;parent.Maturity=EXT_MAT_REVERSAL_CONFIRMED;
  BollingerBand bb;ZeroMemory(bb);bb.TOP_BB=106;bb.MID_BB=100;bb.LOW_BB=94;bb.Width=12;
  UpdateCanonicalMLVState(mlv,"MOM_GAP",DIR_BUY,data,bb,parent,false,false);Check(tag+"M09_owner_unchanged",SameMLVData(mlv,oldMLV));
 }
 for(int c=1;c<=4;c++)
 {
  string tag="H4_case"+IntegerToString(c)+"_";ResetGap(c);TimeframeData data;DataFixture(PERIOD_H4,data);
  Check(tag+"no_weaker_fallback",ClassifyH4AuthoritativeSignal("MOM_GAP",DIR_BUY,data)==SIGNAL_NONE);
  ResetGap(c);DataFixture(PERIOD_H4,data);g_pair_states[0].h4_data=data;g_pair_states[0].h4_direction_owner.RecoveryComplete=true;datetime before=g_pair_states[0].h4_direction_owner.LastProcessedH4CandleTime;
  UpdateRuntimeH4DirectionalOwner(0);Check(tag+"runtime_cursor_unchanged",g_pair_states[0].h4_direction_owner.LastProcessedH4CandleTime==before && g_pair_states[0].h4_direction_owner.State!=H4_OWNER_ACTIVE);ClearH4OwnerCheckpoint(g_pair_states[0]);
  ResetGap(c);DataFixture(PERIOD_H4,data);ApplyH4ReplayCandle(g_pair_states[0],data);Check(tag+"replay_cursor_unchanged",g_pair_states[0].h4_direction_owner.LastProcessedH4CandleTime==0 && g_pair_states[0].h4_direction_owner.State!=H4_OWNER_ACTIVE);
 }
 for(int c=1;c<=3;c++)
 {
  ResetGap(c);ProcessPair(0);Check("pair_cycle_case"+IntegerToString(c)+"_not_consumed",g_processed_candle_time[0]==0 && !g_pair_states[0].is_processing);
 }
 for(int c=1;c<=4;c++)
 {
  ResetGap(c);if(c==4)GapMutationAt=83;
  TradeInfo info;ZeroMemory(info);info.c044_shadow_replay=true;info.c044_lifecycle_managed=true;info.c044_replay_seed_valid=true;info.pair="MOM_GAP";info.direction=DIR_BUY;info.c044_owner_timeframe=PERIOD_H1;info.c044_state=C044_LIFE_MOMENTUM_PENDING;info.c044_epoch_anchor_candle=GapNow-7200;info.c044_last_processed_owner_candle=GapNow-7200;
  datetime before=info.c044_last_processed_owner_candle;ProcessC044OwnerClosedCandle(info,0,GapNow-3600);
  Check("C044_case"+IntegerToString(c)+"_freeze_no_exit_no_cursor",info.c044_state==C044_LIFE_FROZEN && info.c044_exit_reason==C044_EXIT_NONE && info.c044_exit_latched_candle==0 && info.c044_last_processed_owner_candle==before);
 }
 ResetGap(0);TimeframeData readyH4;DataFixture(PERIOD_H4,readyH4);g_pair_states[0].h4_data=readyH4;
 UpdateRuntimeH4DirectionalOwner(0);
 Check("H4_recovery_retries_when_data_ready",g_pair_states[0].h4_direction_owner.RecoveryComplete && g_pair_states[0].h4_direction_owner.LastProcessedH4CandleTime==readyH4.candle_time);ClearH4OwnerCheckpoint(g_pair_states[0]);
 ResetGap(1);ProcessPair(0);GapCase=0;GapReads=0;ProcessPair(0);
 Check("M15_cycle_retries_same_identity_after_recovery",g_processed_candle_time[0]==GapNow-900 && !g_pair_states[0].is_processing);ClearH4OwnerCheckpoint(g_pair_states[0]);
 ResetGap(1);string base=H4OwnerGVBase(g_pair_states[0]);GlobalVariableSet(base+"D",(double)DIR_BUY);GlobalVariableSet(base+"S",(double)SIGNAL_CSM);GlobalVariableSet(base+"T",(double)(GapNow-14400));
 bool unavailable=false;bool loaded=LoadVerifiedH4OwnerCheckpoint(g_pair_states[0],unavailable);
 Check("unavailable_H4_checkpoint_retained",!loaded && GlobalVariableCheck(base+"D") && GlobalVariableCheck(base+"S") && GlobalVariableCheck(base+"T"));
 GapCase=2;RecoverH4DirectionalOwnerForPair(0);
 Check("unwarmed_H4_recovery_is_unresolved",!g_pair_states[0].h4_direction_owner.RecoveryComplete && GlobalVariableCheck(base+"T"));
 GlobalVariableSet(base+"D",(double)DIR_NONE);LoadVerifiedH4OwnerCheckpoint(g_pair_states[0],unavailable);
 Check("proven_invalid_H4_checkpoint_cleared",!GlobalVariableCheck(base+"D") && !GlobalVariableCheck(base+"S") && !GlobalVariableCheck(base+"T"));ClearH4OwnerCheckpoint(g_pair_states[0]);
 ResetGap(0);GapNeutral=true;base=H4OwnerGVBase(g_pair_states[0]);GlobalVariableSet(base+"D",(double)DIR_BUY);GlobalVariableSet(base+"S",(double)SIGNAL_CSM);GlobalVariableSet(base+"T",(double)(GapNow-100*14400));
 RecoverH4DirectionalOwnerForPair(0);
 Check("full_recovery_preserves_unavailable_checkpoint",!g_pair_states[0].h4_direction_owner.RecoveryComplete && g_pair_states[0].h4_direction_owner.State==H4_OWNER_RECOVERY_UNRESOLVED && GlobalVariableCheck(base+"T"));ClearH4OwnerCheckpoint(g_pair_states[0]);
 ResetGap(5);GapMutationAt=163;TimeframeData atomicData;DataFixture(PERIOD_M1,atomicData);CustomAuxLifecycle atomicOwner;ZeroMemory(atomicOwner);
 ResetExtremeLifecycle(atomicOwner.extremeBuy,DIR_BUY,PERIOD_M1);atomicOwner.extremeBuy.Maturity=EXT_MAT_REVERSAL_CONFIRMED;atomicOwner.extremeBuy.IsValid=true;
 ResetExtremeLifecycle(atomicOwner.extremeSell,DIR_SELL,PERIOD_M1);atomicOwner.extremeSell.Maturity=EXT_MAT_REVERSAL_CONFIRMED;atomicOwner.extremeSell.IsValid=true;
 CustomAuxLifecycle atomicBefore=atomicOwner;bool atomicOK=AdvanceCustomAuxLifecycle("MOM_GAP",atomicData,atomicOwner);
 Check("aux_second_read_failure_is_atomic",!atomicOK && SameOwners(atomicOwner,atomicBefore));
 Check("no_orders",OrdersTotal()==0 && OrdersHistoryTotal()==0);
 Print("[MOM-READY-SUMMARY] passed=",passed," failed=",failed);
 return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
