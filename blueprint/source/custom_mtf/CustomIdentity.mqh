#ifndef BBMA_CUSTOM_IDENTITY_V1
#define BBMA_CUSTOM_IDENTITY_V1
#include "CustomSlot.mqh"
// Engineering configuration identity. Not a physical trigger/execution ID.
// Input: validated slots. Preserve group/alternative order; normalize syntax only.
string CustomFormulaIdentity(CustomFormula &formula)
{
 string value=IntegerToString(formula.groupCount)+":"+IntegerToString(formula.atomCount)+":";
 for(int i=0;i<formula.atomCount;i++)
  value+=IntegerToString(formula.atoms[i].group)+","+IntegerToString(formula.atoms[i].timeframe)+","+formula.atoms[i].signal+";";
 return value;
}
string BuildCustomConfigurationPayload(CustomSlotConfig &slots[],CustomUseMatrix &matrix)
{
 string value="CUSTOM_CONFIG_V1|"+string(CUSTOM_MTF_PARSER_REV)+"|"+string(CUSTOM_MTF_SLOT_REV)+"|";
 for(int i=0;i<7;i++)value+=(matrix.tfEnabled[i]?"1":"0");
 value+="|";
 for(int j=0;j<77;j++)value+=(matrix.signalEnabled[j]?"1":"0")+(matrix.available[j]?"1":"0");
 value+="|"+IntegerToString(ArraySize(slots))+"|";
 for(int k=0;k<ArraySize(slots);k++)
 {
  value+=IntegerToString(slots[k].slotId)+":"+(slots[k].enabled?"1":"0")+"|";
  if(!slots[k].enabled)continue;
  value+="C:"+CustomFormulaIdentity(slots[k].context)+"|T:"+CustomFormulaIdentity(slots[k].trigger)+"|";
 }
 return value;
}
#endif
