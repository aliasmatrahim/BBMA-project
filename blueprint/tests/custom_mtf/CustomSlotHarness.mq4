#property strict
#ifndef CUSTOM_SLOT_BASELINE
#include "..\\..\\source\\custom_mtf\\CustomSlot.mqh"
#endif
int passed=0,failed=0;
void Check(int id,bool enabled,string context,string trigger,bool tfOn,bool signalOn,bool available,bool expected)
{
 bool actual=false;
#ifndef CUSTOM_SLOT_BASELINE
 CustomSlotConfig s;s.slotId=id;s.enabled=enabled;s.contextText=context;s.triggerText=trigger;
 CustomUseMatrix m;
 for(int i=0;i<7;i++)m.tfEnabled[i]=tfOn;
 for(int j=0;j<77;j++){m.signalEnabled[j]=signalOn;m.available[j]=available;}
 string reason;actual=ValidateCustomSlot(s,m,reason);
#endif
 if(actual==expected)passed++;else failed++;
 Print("[CUSTOM-SLOT] ",actual==expected?"PASS":"FAIL"," slot=",id," expected=",expected," actual=",actual);
}
int OnInit()
{
 Check(1,true,"D1:RE AND H4:RE","M1:MOM",true,true,true,true);
 Check(5,true,"D1:RE AND H4:RE","M1:RE1 AND M5:RE2 AND M15:RE3 AND M30:RE4 AND H1:EXT",true,true,true,true);
 Check(1,true,"D1:RE AND H4:RE","M1:RE1 AND M5:RE2 AND M15:RE3 AND M30:RE4 AND H1:EXT AND H4:MOM",true,true,true,false);
 Check(0,true,"D1:RE","M1:MOM",true,true,true,false);
 Check(6,true,"D1:RE","M1:MOM",true,true,true,false);
 Check(3,false,"","",false,false,false,true);
 Check(2,true,"","M1:MOM",true,true,true,false);
 Check(2,true,"D1:RE","",true,true,true,false);
 Check(2,true,"D1:RE","M1:MOM",false,true,true,false);
 Check(2,true,"D1:RE","M1:MOM",true,false,true,false);
 Check(2,true,"D1:RE","M1:MOM",true,true,false,false);
 Print("[CUSTOM-SLOT-SUMMARY] passed=",passed," failed=",failed);
 return failed==0?INIT_SUCCEEDED:INIT_FAILED;
}
void OnTick(){}
