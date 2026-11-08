#ifndef BBMA_CUSTOM_SYMBOLS_V1
#define BBMA_CUSTOM_SYMBOLS_V1
// Configuration only. Broker resolution belongs to canonical FindActualSymbol.
enum ENUM_CUSTOM_SYMBOL_MODE {CUSTOM_CHART_ONLY=0,CUSTOM_MARKET_WATCH=1,CUSTOM_LIST=2};
struct CustomSymbolScope {string actual[];};
bool CustomContainsSymbol(string &items[],string actual)
{
 for(int i=0;i<ArraySize(items);i++)if(items[i]==actual)return true;
 return false;
}
bool CustomAppendResolved(string requested,string &items[],string &reason)
{
 requested=StringTrimLeft(StringTrimRight(requested));
 if(requested==""){reason="EMPTY_SYMBOL";return false;}
 string actual=FindActualSymbol(requested);
 if(actual==""){reason="SYMBOL_UNRESOLVED:"+requested;return false;}
 if(CustomContainsSymbol(items,actual))return true;
 int count=ArraySize(items);
 if(ArrayResize(items,count+1)!=count+1){reason="SYMBOL_ALLOCATION_FAILED";return false;}
 items[count]=actual;return true;
}
bool BuildCustomUniverse(int mode,string list,string chart,string &watch[],string &out[],string &reason)
{
 ArrayResize(out,0);reason="";string requested[],staged[];
 if(mode==CUSTOM_CHART_ONLY){ArrayResize(requested,1);requested[0]=chart;}
 else if(mode==CUSTOM_MARKET_WATCH)ArrayCopy(requested,watch);
 else if(mode==CUSTOM_LIST)
 {
  list=StringTrimLeft(StringTrimRight(list));
  if(list=="" || StringSubstr(list,StringLen(list)-1)==","){reason="INVALID_SYMBOL_LIST";return false;}
  StringSplit(list,44,requested);
 }
 else {reason="INVALID_SYMBOL_MODE";return false;}
 if(ArraySize(requested)==0){reason="EMPTY_UNIVERSE";return false;}
 for(int i=0;i<ArraySize(requested);i++)
  if(!CustomAppendResolved(requested[i],staged,reason))return false;
 if(ArrayCopy(out,staged)!=ArraySize(staged)){ArrayResize(out,0);reason="SYMBOL_COPY_FAILED";return false;}
 return true;
}
bool ResolveCustomSubset(string text,string &universe[],string &out[],string &reason)
{
 ArrayResize(out,0);reason="";text=StringTrimLeft(StringTrimRight(text));
 string upper=text;StringToUpper(upper);
 if(upper=="ALL")
 {
  if(ArraySize(universe)==0){reason="EMPTY_UNIVERSE";return false;}
  return ArrayCopy(out,universe)==ArraySize(universe);
 }
 string watch[],staged[];
 if(!BuildCustomUniverse(CUSTOM_LIST,text,"",watch,staged,reason))return false;
 for(int i=0;i<ArraySize(staged);i++)
  if(!CustomContainsSymbol(universe,staged[i])){reason="SYMBOL_OUTSIDE_UNIVERSE:"+staged[i];return false;}
 if(ArrayCopy(out,staged)!=ArraySize(staged)){ArrayResize(out,0);reason="SYMBOL_COPY_FAILED";return false;}
 return true;
}
#endif
