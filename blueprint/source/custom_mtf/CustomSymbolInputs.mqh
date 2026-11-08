#ifndef BBMA_CUSTOM_SYMBOL_INPUTS_V1
#define BBMA_CUSTOM_SYMBOL_INPUTS_V1
#include "CustomSymbols.mqh"
input ENUM_CUSTOM_SYMBOL_MODE CustomSymbolMode=CUSTOM_CHART_ONLY;
input string CustomSymbolList="";
input string Custom1_Symbols="ALL";
input string Custom2_Symbols="ALL";
input string Custom3_Symbols="ALL";
input string Custom4_Symbols="ALL";
input string Custom5_Symbols="ALL";
string g_custom_universe[];
CustomSymbolScope g_custom_slot_symbols[CUSTOM_SLOT_COUNT];
void ResetCustomSymbolInputs()
{
 ArrayResize(g_custom_universe,0);
 for(int i=0;i<CUSTOM_SLOT_COUNT;i++)ArrayResize(g_custom_slot_symbols[i].actual,0);
}
string CustomInputSymbolList(int index)
{
 if(index==0)return Custom1_Symbols;
 if(index==1)return Custom2_Symbols;
 if(index==2)return Custom3_Symbols;
 if(index==3)return Custom4_Symbols;
 if(index==4)return Custom5_Symbols;
 return "";
}
bool InitializeCustomSymbolInputs(string &reason)
{
 ResetCustomSymbolInputs();string watch[],universe[];
 // Snapshot before FindActualSymbol can select additional symbols.
 if(CustomSymbolMode==CUSTOM_MARKET_WATCH)
 {
  int count=SymbolsTotal(true);ArrayResize(watch,count);
  for(int i=0;i<count;i++)watch[i]=SymbolName(i,true);
 }
 if(!BuildCustomUniverse(CustomSymbolMode,CustomSymbolList,Symbol(),watch,universe,reason))return false;
 CustomSymbolScope staged[CUSTOM_SLOT_COUNT];
 for(int j=0;j<CUSTOM_SLOT_COUNT;j++)
 {
  if(!g_custom_slots[j].enabled)continue;
  if(!ResolveCustomSubset(CustomInputSymbolList(j),universe,staged[j].actual,reason))
  {reason="CUSTOM_SLOT_"+IntegerToString(j+1)+":"+reason;return false;}
 }
 if(ArrayCopy(g_custom_universe,universe)!=ArraySize(universe)){reason="UNIVERSE_COPY_FAILED";ResetCustomSymbolInputs();return false;}
 for(int k=0;k<CUSTOM_SLOT_COUNT;k++)
  if(ArrayCopy(g_custom_slot_symbols[k].actual,staged[k].actual)!=ArraySize(staged[k].actual))
  {reason="SUBSET_COPY_FAILED";ResetCustomSymbolInputs();return false;}
 return true;
}
bool CustomSlotUsesSymbol(int slotIndex,string actualSymbol)
{
 if(slotIndex<0 || slotIndex>=CUSTOM_SLOT_COUNT || !g_custom_slots[slotIndex].enabled)return false;
 return CustomContainsSymbol(g_custom_slot_symbols[slotIndex].actual,actualSymbol);
}
string CustomResolvedSymbolIdentity(string &symbols[])
{
 string result=IntegerToString(ArraySize(symbols))+":";
 for(int i=0;i<ArraySize(symbols);i++)result+=IntegerToString(StringLen(symbols[i]))+":"+symbols[i];
 return result;
}
#endif
