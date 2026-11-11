#property strict
// Broker catalog fixture; canonical resolver body is extracted by runner.
string catalog[];
int FixtureSymbolsTotal(bool selected){return ArraySize(catalog);}
string FixtureSymbolName(int i,bool selected){return catalog[i];}
bool FixtureSymbolSelect(string name,bool selected){return true;}
#include "CanonicalResolverFixture.mqh"
#include "..\\..\\source\\custom_mtf\\CustomInputs.mqh"
int passed=0,failed=0;
void Check(string name,bool value){if(value)passed++;else failed++;Print("[CONFIG-ID] ",name," ",value?"PASS":"FAIL");}
string Payload(CustomSlotConfig &slots[],CustomUseMatrix &matrix)
{
#ifdef CUSTOM_IDENTITY_BASELINE
 // Missing-capability adapter, not a failing production regression.
 return "";
#else
 return BuildCustomConfigurationPayload(slots,matrix);
#endif
}
int OnInit()
{
 StringSplit(Symbol()+",XAUUSD,EURUSD",44,catalog);
 CustomSlotConfig slots[5];CustomUseMatrix matrix;string reason;
 for(int i=0;i<7;i++)matrix.tfEnabled[i]=true;
 for(int j=0;j<77;j++){matrix.signalEnabled[j]=true;matrix.available[j]=true;}
 for(int k=0;k<5;k++){slots[k].slotId=k+1;slots[k].enabled=false;ValidateCustomSlot(slots[k],matrix,reason);}
 slots[0].enabled=true;slots[0].contextText="D1:RE";slots[0].triggerText="M1:MOM OR M5:MOM";
 Check("fixture_valid",ValidateCustomSlot(slots[0],matrix,reason));
 string a=Payload(slots,matrix);
 Check("nonempty",StringLen(a)>0);Check("repeat_stable",a!="" && a==Payload(slots,matrix));
 slots[0].contextText=" d1 : re ";slots[0].triggerText=" (m1:mom OR m5:mom) ";
 Check("normalized_fixture",ValidateCustomSlot(slots[0],matrix,reason));
 Check("whitespace_case_parenthesis_stable",a!="" && a==Payload(slots,matrix));
 slots[0].triggerText="M1:MOM AND M5:MOM";ValidateCustomSlot(slots[0],matrix,reason);
 Check("operator_changes_identity",a!=Payload(slots,matrix));
 slots[0].triggerText="M1:MOM OR M5:MOM";ValidateCustomSlot(slots[0],matrix,reason);
 matrix.tfEnabled[1]=false;Check("tf_changes_identity",a!=Payload(slots,matrix));matrix.tfEnabled[1]=true;
 matrix.signalEnabled[0]=false;Check("signal_changes_identity",a!=Payload(slots,matrix));matrix.signalEnabled[0]=true;
 matrix.available[0]=false;Check("availability_changes_identity",a!=Payload(slots,matrix));matrix.available[0]=true;
 slots[0].enabled=false;ValidateCustomSlot(slots[0],matrix,reason);Check("enable_changes_identity",a!=Payload(slots,matrix));
#ifndef CUSTOM_IDENTITY_BASELINE
 // Poison prior helper state; reinitialization must restore defaults exactly.
 bool first=InitializeCustomInputs(reason);string initial=g_custom_config_payload;
 g_custom_use.available[0]=true;g_custom_use.signalEnabled[0]=true;
 g_custom_slots[4].context.atomCount=7;g_custom_config_payload="STALE";g_custom_config_hash="STALE";
 bool second=InitializeCustomInputs(reason);
 Check("default_reinit_clean",first && second && initial!="" && initial==g_custom_config_payload && !g_custom_use.available[0] && !g_custom_use.signalEnabled[0] && g_custom_slots[4].context.atomCount==0 && g_custom_config_hash=="");
#endif
 Print("[CONFIG-ID-SUMMARY] passed=",passed," failed=",failed);
 return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
