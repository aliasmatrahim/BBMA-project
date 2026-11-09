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
#ifdef CUSTOM_M09TF_BASELINE
bool ExportSourceMHVSignal(MLVData &owner,Signal &signal){return ExportCanonicalMHVSignal(owner,signal);}
#endif
int passed=0,failed=0;
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[CUSTOM-MHVTF] ",name," ",ok?"PASS":"FAIL");}
void StepData(TimeframeData &data,int tf,datetime time,ENUM_DIRECTION direction,double open,double close,double low,double high)
{
 ZeroMemory(data);data.timeframe=tf;data.candle_time=time;data.barIndex=1;data.is_closed=true;data.is_valid=true;
 data.open=direction==DIR_BUY?open:3-open;data.close=direction==DIR_BUY?close:3-close;
 data.low=direction==DIR_BUY?low:3-high;data.high=direction==DIR_BUY?high:3-low;
 data.ma[0]=1.7;data.ma[1]=1.8;data.ma[2]=1.3;data.ma[3]=1.2;
}
int OnInit()
{
 for(int t=0;t<7;t++)for(int side=0;side<2;side++)
 {
  int tf=CustomTFValue(t),seconds=GetTimeframeSeconds(tf);ENUM_DIRECTION dir=side==0?DIR_BUY:DIR_SELL;
  string key=IntegerToString(tf)+"_"+IntegerToString(side);datetime start=D'2026.08.01 00:00';
  BollingerBand band;ZeroMemory(band);band.TOP_BB=2;band.MID_BB=1.5;band.LOW_BB=1;band.Width=1;
  ExtremeLifecycleData parent;ZeroMemory(parent);parent.Timeframe=tf;parent.Direction=dir==DIR_BUY?DIR_SELL:DIR_BUY;
  parent.IsValid=true;parent.Maturity=EXT_MAT_REVERSAL_CONFIRMED;parent.RawCandleTime=start-2*seconds;parent.ConfirmationCandleTime=start-seconds;
  MLVData owner;ZeroMemory(owner);TimeframeData data;
  StepData(data,tf,start,dir,1.45,1.5,1.4,1.6);
  UpdateCanonicalMLVState(owner,"M09_STRUCTURAL_FIXTURE",dir,data,band,parent,false);
  Check("parent_source_TF_"+key,owner.State==MLV_PARENT_READY && owner.Timeframe==tf && owner.ParentConfirmationCandleTime==parent.ConfirmationCandleTime);
  StepData(data,tf,start+seconds,dir,1.4,1.5,1.25,1.6);
  UpdateCanonicalMLVState(owner,"M09_STRUCTURAL_FIXTURE",dir,data,band,parent,false);
  Check("normal_TP_structure_"+key,owner.State==MLV_TP_COMPLETE && owner.TPWajibCandleTime==data.candle_time);
  StepData(data,tf,start+2*seconds,dir,1.4,1.35,1.3,1.5);
  UpdateCanonicalMLVState(owner,"M09_STRUCTURAL_FIXTURE",dir,data,band,parent,false);
  Check("loss_developing_"+key,owner.State==MLV_LOSS_DEVELOPING && !owner.IsValid);
  StepData(data,tf,start+3*seconds,dir,1.2,1.45,1.15,1.5);
  UpdateCanonicalMLVState(owner,"M09_STRUCTURAL_FIXTURE",dir,data,band,parent,false);
  Check("formation_established_"+key,owner.State==MLV_FORMATION_ESTABLISHED && owner.IsValid && owner.Timeframe==tf);
  double frozen=dir==DIR_BUY?1.35:1.65;
  Check("freeze_excludes_moveaway_body_"+key,MathAbs(owner.FrozenMarkedBody-frozen)<0.0000001);
  Signal signal;bool exported=ExportSourceMHVSignal(owner,signal);
  Check("source_export_identity_"+key,exported && signal.Timeframe==tf && signal.Direction==dir && signal.CandleTime==start+3*seconds);
  Check("canonical_export_remains_M15_"+key,ExportCanonicalMHVSignal(owner,signal)==(tf==PERIOD_M15));
  MLVData pending=owner;TimeframeData outside;
  StepData(outside,tf,start+4*seconds,dir,1.1,0.9,0.8,1.2);
  UpdateCanonicalMLVState(pending,"M09_STRUCTURAL_FIXTURE",dir,outside,band,parent,false);
  Check("outer_close_voids_pending_"+key,pending.State==MLV_VOID && !pending.IsValid);
  StepData(data,tf,start+4*seconds,dir,1.4,1.5,1.3,1.6);
  UpdateCanonicalMLVState(owner,"M09_STRUCTURAL_FIXTURE",dir,data,band,parent,false);
  Check("retest_frozen_reference_"+key,owner.State==MLV_RETEST_COMPLETE && MathAbs(owner.FrozenMarkedBody-frozen)<0.0000001);
  StepData(data,tf,start+5*seconds,dir,1.5,1.6,1.4,1.7);
  UpdateCanonicalMLVState(owner,"M09_STRUCTURAL_FIXTURE",dir,data,band,parent,true);
  Check("direction_takeover_"+key,owner.State==MLV_DIRECTION_TAKEN && owner.IsValid && !owner.InvalidationWindowOpen);
  StepData(data,tf,start+6*seconds,dir,1.1,0.9,0.8,1.2);
  UpdateCanonicalMLVState(owner,"M09_STRUCTURAL_FIXTURE",dir,data,band,parent,false);
  Check("completed_provenance_not_retro_void_"+key,owner.State==MLV_DIRECTION_TAKEN && owner.IsValid && MathAbs(owner.FrozenMarkedBody-frozen)<0.0000001);
  datetime stamp=owner.LastUpdateCandleTime;ENUM_MLV_STATE state=owner.State;
  UpdateCanonicalMLVState(owner,"M09_STRUCTURAL_FIXTURE",dir,data,band,parent,false);
  Check("duplicate_idempotent_"+key,owner.State==state && owner.LastUpdateCandleTime==stamp && MathAbs(owner.FrozenMarkedBody-frozen)<0.0000001);
  ExtremeLifecycleData newer=parent;newer.RawCandleTime=start+6*seconds;newer.ConfirmationCandleTime=start+7*seconds;
  StepData(data,tf,start+8*seconds,dir,1.45,1.5,1.4,1.6);
  UpdateCanonicalMLVState(owner,"M09_STRUCTURAL_FIXTURE",dir,data,band,newer,false);
  Check("new_parent_atomic_supersession_"+key,owner.State==MLV_SUPERSEDED && !owner.IsValid && owner.FrozenMarkedBody>0);
  StepData(data,tf,start+9*seconds,dir,1.45,1.5,1.4,1.6);
  UpdateCanonicalMLVState(owner,"M09_STRUCTURAL_FIXTURE",dir,data,band,newer,false);
  Check("next_cycle_attaches_exact_source_"+key,owner.State==MLV_PARENT_READY && owner.Timeframe==tf && owner.ParentConfirmationCandleTime==newer.ConfirmationCandleTime && owner.FrozenMarkedBody==0);
  MLVData wrong;ZeroMemory(wrong);ExtremeLifecycleData mismatch=parent;mismatch.Timeframe=tf==PERIOD_M15?PERIOD_H1:PERIOD_M15;
  StepData(data,tf,start,dir,1.45,1.5,1.4,1.6);
  UpdateCanonicalMLVState(wrong,"M09_STRUCTURAL_FIXTURE",dir,data,band,mismatch,false);
  Check("wrong_source_parent_rejected_"+key,wrong.State==MLV_NONE);
  ZeroMemory(wrong);mismatch=parent;mismatch.Direction=dir;
  UpdateCanonicalMLVState(wrong,"M09_STRUCTURAL_FIXTURE",dir,data,band,mismatch,false);
  Check("wrong_parent_direction_rejected_"+key,wrong.State==MLV_NONE);
  ZeroMemory(wrong);data.is_closed=false;
  UpdateCanonicalMLVState(wrong,"M09_STRUCTURAL_FIXTURE",dir,data,band,parent,false);
  Check("live_data_rejected_"+key,wrong.State==MLV_NONE);
 }
 Print("[CUSTOM-MHVTF-SUMMARY] passed=",passed," failed=",failed);return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
