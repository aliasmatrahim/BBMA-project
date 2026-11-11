#ifndef BBMA_CUSTOM_SLOT_V1
#define BBMA_CUSTOM_SLOT_V1
#include "CustomFormula.mqh"
#define CUSTOM_MTF_SLOT_REV "CUSTOM_SLOT_001_20261108"
#define CUSTOM_SLOT_COUNT 5
struct CustomUseMatrix
{
 bool tfEnabled[7];
 bool signalEnabled[77];
 bool available[77];
};
struct CustomSlotConfig
{
 int slotId;
 bool enabled;
 string contextText;
 string triggerText;
 CustomFormula context;
 CustomFormula trigger;
};
int CustomTFValue(int index)
{
 int values[7]={PERIOD_M1,PERIOD_M5,PERIOD_M15,PERIOD_M30,PERIOD_H1,PERIOD_H4,PERIOD_D1};
 if(index<0 || index>=7)return 0;
 return values[index];
}
int CustomTFIndex(int tf)
{
 for(int i=0;i<7;i++)if(CustomTFValue(i)==tf)return i;
 return -1;
}
string CustomSignalValue(int index)
{
 string values[11]={"RE","RE1","RE2","RE3","RE4","EXT","MHV","MLV","CSA","CSAK","MOM"};
 if(index<0 || index>=11)return "";
 return values[index];
}
int CustomSignalIndex(string s)
{
 for(int i=0;i<11;i++)if(CustomSignalValue(i)==s)return i;
 return -1;
}
bool CustomCheckUse(CustomFormula &formula,CustomUseMatrix &matrix,string &reason)
{
 for(int i=0;i<formula.atomCount;i++)
 {
  int tf=CustomTFIndex(formula.atoms[i].timeframe);
  int sig=CustomSignalIndex(formula.atoms[i].signal);
  if(tf<0 || sig<0){reason="UNRESOLVED_ATOM";return false;}
  int cell=tf*11+sig;
  if(!matrix.tfEnabled[tf]){reason="TIMEFRAME_DISABLED";return false;}
  if(!matrix.signalEnabled[cell]){reason="SIGNAL_DISABLED";return false;}
  if(!matrix.available[cell]){reason="SIGNAL_UNAVAILABLE";return false;}
 }
 return true;
}
bool ValidateCustomSlot(CustomSlotConfig &slot,CustomUseMatrix &matrix,string &reason)
{
 slot.context.atomCount=0;slot.context.groupCount=0;
 slot.trigger.atomCount=0;slot.trigger.groupCount=0;reason="";
 if(slot.slotId<1 || slot.slotId>CUSTOM_SLOT_COUNT){reason="INVALID_SLOT_ID";return false;}
 if(!slot.enabled)return true;
 // Stage both fields locally: failed validation cannot expose a half-valid slot.
 CustomFormula context,trigger;
 if(!ParseCustomFormula(slot.contextText,context,reason)){reason="CONTEXT:"+reason;return false;}
 if(!ParseCustomFormula(slot.triggerText,trigger,reason)){reason="TRIGGER:"+reason;return false;}
 if(context.atomCount+trigger.atomCount>CUSTOM_MAX_ATOMS){reason="SLOT_TOO_MANY_ATOMS";return false;}
 if(!CustomCheckUse(context,matrix,reason) || !CustomCheckUse(trigger,matrix,reason))return false;
 slot.context=context;slot.trigger=trigger;
 return true;
}
#endif
