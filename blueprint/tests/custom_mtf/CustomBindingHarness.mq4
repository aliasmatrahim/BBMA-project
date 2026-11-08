#property strict
// Identity helpers are extracted from current EA; no second production allocator.
#include "CanonicalPairIdentityFixture.mqh"
#ifndef CUSTOM_BINDING_BASELINE
#include "..\\..\\source\\custom_mtf\\CustomPairBinding.mqh"
#else
struct CustomPairBinding {string actual;int pairIndex;int pairId;int magic;bool append;};
bool BuildCustomPairBindingPlan(string &u[],string &a[],int &ids[],int &magics[],bool &ready[],int strategy,int instance,int capacity,CustomPairBinding &out[],string &reason)
{ArrayResize(out,0);reason="MISSING_CAPABILITY";return false;}
#endif
int passed=0,failed=0;
void Check(string name,bool ok){if(ok)passed++;else failed++;Print("[CUSTOM-BINDING] ",name," ",ok?"PASS":"FAIL");}
int OnInit()
{
 string pool[1]={"GBPUSD.a"};int ids[1]={14};int magics[1]={118214};bool ready[1]={true};
 string u[],reason;CustomPairBinding result[];
 StringSplit("GBPUSD.a,EURUSD.a",44,u);
 bool ok=BuildCustomPairBindingPlan(u,pool,ids,magics,ready,1,82,40,result,reason);
 Check("reuse_existing_actual",ok && ArraySize(result)==2 && result[0].pairIndex==0 && !result[0].append && result[0].pairId==14 && result[0].magic==118214);
 Check("append_new_separate_index",ok && ArraySize(result)==2 && result[1].pairIndex==1 && result[1].append && result[1].pairId==13 && result[1].magic==118213);
 Check("input_pool_untouched",pool[0]=="GBPUSD.a" && ids[0]==14 && magics[0]==118214 && ready[0]);
 ready[0]=false;Check("unready_reuse_rejected",!BuildCustomPairBindingPlan(u,pool,ids,magics,ready,1,82,40,result,reason) && ArraySize(result)==0);ready[0]=true;
 Check("combined_capacity_rejected",!BuildCustomPairBindingPlan(u,pool,ids,magics,ready,1,82,1,result,reason) && ArraySize(result)==0);
 StringSplit("GBPUSD.b",44,u);Check("suffix_pairid_collision_rejected",!BuildCustomPairBindingPlan(u,pool,ids,magics,ready,1,82,40,result,reason) && ArraySize(result)==0);
 StringSplit("EURUSD.a,EURUSD.a",44,u);Check("duplicate_actual_rejected",!BuildCustomPairBindingPlan(u,pool,ids,magics,ready,1,82,40,result,reason));
 StringSplit("",44,u);ArrayResize(u,0);Check("empty_universe_no_bindings",BuildCustomPairBindingPlan(u,pool,ids,magics,ready,1,82,40,result,reason) && ArraySize(result)==0);
 StringSplit("EURUSD.a",44,u);Check("invalid_deployment_identity",!BuildCustomPairBindingPlan(u,pool,ids,magics,ready,1,100,40,result,reason));
 magics[0]=0;Check("invalid_existing_identity",!BuildCustomPairBindingPlan(u,pool,ids,magics,ready,1,82,40,result,reason));magics[0]=118214;
 string emptyPool[];int emptyIds[],emptyMagics[];bool emptyReady[];
 StringSplit("GBPUSD.a,EURUSD.a",44,u);ok=BuildCustomPairBindingPlan(u,emptyPool,emptyIds,emptyMagics,emptyReady,1,82,40,result,reason);
 Check("empty_pool_distinct_slots",ok && ArraySize(result)==2 && result[0].pairIndex==0 && result[1].pairIndex==1);
 Print("[CUSTOM-BINDING-SUMMARY] passed=",passed," failed=",failed);
 return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
