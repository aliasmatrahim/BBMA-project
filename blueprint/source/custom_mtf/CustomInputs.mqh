#ifndef BBMA_CUSTOM_INPUTS_V1
#define BBMA_CUSTOM_INPUTS_V1
#include "CustomIdentity.mqh"
// Configuration admission only. Custom execution availability defaults closed.
input bool CustomTF_M1=true;
input string CustomSignals_M1=""; // enabled shortforms, comma separated
input bool CustomTF_M5=true;
input string CustomSignals_M5=""; // enabled shortforms, comma separated
input bool CustomTF_M15=true;
input string CustomSignals_M15=""; // enabled shortforms, comma separated
input bool CustomTF_M30=true;
input string CustomSignals_M30=""; // enabled shortforms, comma separated
input bool CustomTF_H1=true;
input string CustomSignals_H1=""; // enabled shortforms, comma separated
input bool CustomTF_H4=true;
input string CustomSignals_H4=""; // enabled shortforms, comma separated
input bool CustomTF_D1=true;
input string CustomSignals_D1=""; // enabled shortforms, comma separated
input bool Custom1_Enable=false;
input string Custom1_Context="";
input string Custom1_Trigger="";
input bool Custom2_Enable=false;
input string Custom2_Context="";
input string Custom2_Trigger="";
input bool Custom3_Enable=false;
input string Custom3_Context="";
input string Custom3_Trigger="";
input bool Custom4_Enable=false;
input string Custom4_Context="";
input string Custom4_Trigger="";
input bool Custom5_Enable=false;
input string Custom5_Context="";
input string Custom5_Trigger="";
CustomSlotConfig g_custom_slots[CUSTOM_SLOT_COUNT];
CustomUseMatrix g_custom_use;
string g_custom_config_payload="";
string g_custom_config_hash="";
bool CustomInputTFEnabled(int index)
{
 if(index==0)return CustomTF_M1;
 if(index==1)return CustomTF_M5;
 if(index==2)return CustomTF_M15;
 if(index==3)return CustomTF_M30;
 if(index==4)return CustomTF_H1;
 if(index==5)return CustomTF_H4;
 if(index==6)return CustomTF_D1;
 return false;
}
string CustomInputSignalList(int index)
{
 if(index==0)return CustomSignals_M1;
 if(index==1)return CustomSignals_M5;
 if(index==2)return CustomSignals_M15;
 if(index==3)return CustomSignals_M30;
 if(index==4)return CustomSignals_H1;
 if(index==5)return CustomSignals_H4;
 if(index==6)return CustomSignals_D1;
 return "";
}
bool InitializeCustomInputs(string &reason)
{
 reason="";g_custom_config_payload="";g_custom_config_hash="";
 for(int reset=0;reset<CUSTOM_SLOT_COUNT;reset++)
 {
  g_custom_slots[reset].context.atomCount=0;g_custom_slots[reset].context.groupCount=0;
  g_custom_slots[reset].trigger.atomCount=0;g_custom_slots[reset].trigger.groupCount=0;
 }
 for(int i=0;i<7;i++)
 {
  g_custom_use.tfEnabled[i]=CustomInputTFEnabled(i);
  for(int j=0;j<11;j++){g_custom_use.signalEnabled[i*11+j]=false;g_custom_use.available[i*11+j]=false;}
  string list=CustomInputSignalList(i);StringToUpper(list);
  StringTrimLeft(list);StringTrimRight(list);
  if(list=="")continue;
  string tokens[];int count=StringSplit(list,44,tokens);
  for(int k=0;k<count;k++)
  {
   string token=tokens[k];StringTrimLeft(token);StringTrimRight(token);
   int signal=CustomSignalIndex(token);
   if(signal<0){reason="INVALID_SIGNAL_LIST:"+IntegerToString(i);return false;}
   g_custom_use.signalEnabled[i*11+signal]=true;
  }
 }
 g_custom_slots[0].slotId=1;g_custom_slots[0].enabled=Custom1_Enable;
 g_custom_slots[0].contextText=Custom1_Context;g_custom_slots[0].triggerText=Custom1_Trigger;
 g_custom_slots[1].slotId=2;g_custom_slots[1].enabled=Custom2_Enable;
 g_custom_slots[1].contextText=Custom2_Context;g_custom_slots[1].triggerText=Custom2_Trigger;
 g_custom_slots[2].slotId=3;g_custom_slots[2].enabled=Custom3_Enable;
 g_custom_slots[2].contextText=Custom3_Context;g_custom_slots[2].triggerText=Custom3_Trigger;
 g_custom_slots[3].slotId=4;g_custom_slots[3].enabled=Custom4_Enable;
 g_custom_slots[3].contextText=Custom4_Context;g_custom_slots[3].triggerText=Custom4_Trigger;
 g_custom_slots[4].slotId=5;g_custom_slots[4].enabled=Custom5_Enable;
 g_custom_slots[4].contextText=Custom5_Context;g_custom_slots[4].triggerText=Custom5_Trigger;
 for(int n=0;n<CUSTOM_SLOT_COUNT;n++)
 {
  if(!ValidateCustomSlot(g_custom_slots[n],g_custom_use,reason))
  {reason="CUSTOM_SLOT_"+IntegerToString(n+1)+":"+reason;return false;}
 }
 g_custom_config_payload=BuildCustomConfigurationPayload(g_custom_slots,g_custom_use);
 return true;
}
#endif
