#ifndef CUSTOM_ORIGIN_TEST_CODEC
#define CUSTOM_ORIGIN_TEST_CODEC
// Test-only field codec. No production checkpoint or lifecycle rule.
string OriginHex(string value){uchar a[];int n=StringToCharArray(value,a,0,WHOLE_ARRAY,CP_UTF8);string out="";for(int i=0;i<n && a[i]!=0;i++)out+=StringFormat("%02X",(int)a[i]);return out;}
string OriginUnhex(string value){uchar a[];int n=StringLen(value)/2;ArrayResize(a,n+1);for(int i=0;i<n;i++){int hi=StringFind("0123456789ABCDEF",StringSubstr(value,2*i,1)),lo=StringFind("0123456789ABCDEF",StringSubstr(value,2*i+1,1));a[i]=(uchar)(16*hi+lo);}a[n]=0;return CharArrayToString(a,0,n,CP_UTF8);}
bool OriginReadKey(int h,string expected,string &value){if(FileIsEnding(h))return false;string key=FileReadString(h);value=FileReadString(h);return key==expected;}
bool WriteOriginExtremeLifecycleData(int h,string prefix,ExtremeLifecycleData &x)
{
 if(FileWrite(h,prefix+".Maturity",IntegerToString((int)x.Maturity))==0)return false;
 if(FileWrite(h,prefix+".Direction",IntegerToString((int)x.Direction))==0)return false;
 if(FileWrite(h,prefix+".Timeframe",IntegerToString((int)x.Timeframe))==0)return false;
 if(FileWrite(h,prefix+".RawBar",IntegerToString((int)x.RawBar))==0)return false;
 if(FileWrite(h,prefix+".RawCandleTime",IntegerToString((int)x.RawCandleTime))==0)return false;
 if(FileWrite(h,prefix+".ConfirmationBar",IntegerToString((int)x.ConfirmationBar))==0)return false;
 if(FileWrite(h,prefix+".ConfirmationCandleTime",IntegerToString((int)x.ConfirmationCandleTime))==0)return false;
 if(FileWrite(h,prefix+".ConfirmationClose",StringFormat("%.17g",x.ConfirmationClose))==0)return false;
 if(FileWrite(h,prefix+".LastUpdateBar",IntegerToString((int)x.LastUpdateBar))==0)return false;
 if(FileWrite(h,prefix+".LastUpdateCandleTime",IntegerToString((int)x.LastUpdateCandleTime))==0)return false;
 if(FileWrite(h,prefix+".PreviousClose",StringFormat("%.17g",x.PreviousClose))==0)return false;
 if(FileWrite(h,prefix+".ProvisionalBodyAnchor",StringFormat("%.17g",x.ProvisionalBodyAnchor))==0)return false;
 if(FileWrite(h,prefix+".FrozenBodyAnchor",StringFormat("%.17g",x.FrozenBodyAnchor))==0)return false;
 if(FileWrite(h,prefix+".RelevantMA5",StringFormat("%.17g",x.RelevantMA5))==0)return false;
 if(FileWrite(h,prefix+".RetestStartBar",IntegerToString((int)x.RetestStartBar))==0)return false;
 if(FileWrite(h,prefix+".RetestStartCandleTime",IntegerToString((int)x.RetestStartCandleTime))==0)return false;
 if(FileWrite(h,prefix+".RetestCompletionBar",IntegerToString((int)x.RetestCompletionBar))==0)return false;
 if(FileWrite(h,prefix+".RetestCompletionCandleTime",IntegerToString((int)x.RetestCompletionCandleTime))==0)return false;
 if(FileWrite(h,prefix+".IsValid",IntegerToString((int)x.IsValid))==0)return false;
 if(FileWrite(h,prefix+".Reason",OriginHex(x.Reason))==0)return false;
 return true;
}
bool ReadOriginExtremeLifecycleData(int h,string prefix,ExtremeLifecycleData &x)
{
 string value="";ZeroMemory(x);
 if(!OriginReadKey(h,prefix+".Maturity",value))return false;x.Maturity=(ENUM_EXTREME_MATURITY)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".Direction",value))return false;x.Direction=(ENUM_DIRECTION)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".Timeframe",value))return false;x.Timeframe=(int)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".RawBar",value))return false;x.RawBar=(int)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".RawCandleTime",value))return false;x.RawCandleTime=(datetime)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".ConfirmationBar",value))return false;x.ConfirmationBar=(int)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".ConfirmationCandleTime",value))return false;x.ConfirmationCandleTime=(datetime)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".ConfirmationClose",value))return false;x.ConfirmationClose=StringToDouble(value);
 if(!OriginReadKey(h,prefix+".LastUpdateBar",value))return false;x.LastUpdateBar=(int)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".LastUpdateCandleTime",value))return false;x.LastUpdateCandleTime=(datetime)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".PreviousClose",value))return false;x.PreviousClose=StringToDouble(value);
 if(!OriginReadKey(h,prefix+".ProvisionalBodyAnchor",value))return false;x.ProvisionalBodyAnchor=StringToDouble(value);
 if(!OriginReadKey(h,prefix+".FrozenBodyAnchor",value))return false;x.FrozenBodyAnchor=StringToDouble(value);
 if(!OriginReadKey(h,prefix+".RelevantMA5",value))return false;x.RelevantMA5=StringToDouble(value);
 if(!OriginReadKey(h,prefix+".RetestStartBar",value))return false;x.RetestStartBar=(int)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".RetestStartCandleTime",value))return false;x.RetestStartCandleTime=(datetime)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".RetestCompletionBar",value))return false;x.RetestCompletionBar=(int)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".RetestCompletionCandleTime",value))return false;x.RetestCompletionCandleTime=(datetime)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".IsValid",value))return false;x.IsValid=(StringToInteger(value)!=0);
 if(!OriginReadKey(h,prefix+".Reason",value))return false;x.Reason=OriginUnhex(value);
 return true;
}
bool WriteOriginMLVData(int h,string prefix,MLVData &x)
{
 if(FileWrite(h,prefix+".State",IntegerToString((int)x.State))==0)return false;
 if(FileWrite(h,prefix+".Direction",IntegerToString((int)x.Direction))==0)return false;
 if(FileWrite(h,prefix+".ParentExtremeDirection",IntegerToString((int)x.ParentExtremeDirection))==0)return false;
 if(FileWrite(h,prefix+".Timeframe",IntegerToString((int)x.Timeframe))==0)return false;
 if(FileWrite(h,prefix+".Reason",OriginHex(x.Reason))==0)return false;
 if(FileWrite(h,prefix+".ParentRawCandleTime",IntegerToString((int)x.ParentRawCandleTime))==0)return false;
 if(FileWrite(h,prefix+".ParentConfirmationCandleTime",IntegerToString((int)x.ParentConfirmationCandleTime))==0)return false;
 if(FileWrite(h,prefix+".TPWajibCandleTime",IntegerToString((int)x.TPWajibCandleTime))==0)return false;
 if(FileWrite(h,prefix+".ProvisionalBodyAnchor",StringFormat("%.17g",x.ProvisionalBodyAnchor))==0)return false;
 if(FileWrite(h,prefix+".FrozenMarkedBody",StringFormat("%.17g",x.FrozenMarkedBody))==0)return false;
 if(FileWrite(h,prefix+".PreviousClose",StringFormat("%.17g",x.PreviousClose))==0)return false;
 if(FileWrite(h,prefix+".StartBar",IntegerToString((int)x.StartBar))==0)return false;
 if(FileWrite(h,prefix+".StartCandleTime",IntegerToString((int)x.StartCandleTime))==0)return false;
 if(FileWrite(h,prefix+".LastUpdateBar",IntegerToString((int)x.LastUpdateBar))==0)return false;
 if(FileWrite(h,prefix+".LastUpdateCandleTime",IntegerToString((int)x.LastUpdateCandleTime))==0)return false;
 if(FileWrite(h,prefix+".ConfirmationBar",IntegerToString((int)x.ConfirmationBar))==0)return false;
 if(FileWrite(h,prefix+".ConfirmationCandleTime",IntegerToString((int)x.ConfirmationCandleTime))==0)return false;
 if(FileWrite(h,prefix+".ConfirmationClose",StringFormat("%.17g",x.ConfirmationClose))==0)return false;
 if(FileWrite(h,prefix+".RetestBar",IntegerToString((int)x.RetestBar))==0)return false;
 if(FileWrite(h,prefix+".RetestCandleTime",IntegerToString((int)x.RetestCandleTime))==0)return false;
 if(FileWrite(h,prefix+".DirectionTakeoverBar",IntegerToString((int)x.DirectionTakeoverBar))==0)return false;
 if(FileWrite(h,prefix+".DirectionTakeoverCandleTime",IntegerToString((int)x.DirectionTakeoverCandleTime))==0)return false;
 if(FileWrite(h,prefix+".VoidBar",IntegerToString((int)x.VoidBar))==0)return false;
 if(FileWrite(h,prefix+".VoidCandleTime",IntegerToString((int)x.VoidCandleTime))==0)return false;
 if(FileWrite(h,prefix+".SupersededBar",IntegerToString((int)x.SupersededBar))==0)return false;
 if(FileWrite(h,prefix+".SupersededCandleTime",IntegerToString((int)x.SupersededCandleTime))==0)return false;
 if(FileWrite(h,prefix+".InvalidationWindowOpen",IntegerToString((int)x.InvalidationWindowOpen))==0)return false;
 if(FileWrite(h,prefix+".IsValid",IntegerToString((int)x.IsValid))==0)return false;
 if(FileWrite(h,prefix+".SupersessionCandidateActive",IntegerToString((int)x.SupersessionCandidateActive))==0)return false;
 if(FileWrite(h,prefix+".SupersessionRawBar",IntegerToString((int)x.SupersessionRawBar))==0)return false;
 if(FileWrite(h,prefix+".SupersessionRawCandleTime",IntegerToString((int)x.SupersessionRawCandleTime))==0)return false;
 return true;
}
bool ReadOriginMLVData(int h,string prefix,MLVData &x)
{
 string value="";ZeroMemory(x);
 if(!OriginReadKey(h,prefix+".State",value))return false;x.State=(ENUM_MLV_STATE)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".Direction",value))return false;x.Direction=(ENUM_DIRECTION)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".ParentExtremeDirection",value))return false;x.ParentExtremeDirection=(ENUM_DIRECTION)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".Timeframe",value))return false;x.Timeframe=(int)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".Reason",value))return false;x.Reason=OriginUnhex(value);
 if(!OriginReadKey(h,prefix+".ParentRawCandleTime",value))return false;x.ParentRawCandleTime=(datetime)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".ParentConfirmationCandleTime",value))return false;x.ParentConfirmationCandleTime=(datetime)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".TPWajibCandleTime",value))return false;x.TPWajibCandleTime=(datetime)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".ProvisionalBodyAnchor",value))return false;x.ProvisionalBodyAnchor=StringToDouble(value);
 if(!OriginReadKey(h,prefix+".FrozenMarkedBody",value))return false;x.FrozenMarkedBody=StringToDouble(value);
 if(!OriginReadKey(h,prefix+".PreviousClose",value))return false;x.PreviousClose=StringToDouble(value);
 if(!OriginReadKey(h,prefix+".StartBar",value))return false;x.StartBar=(int)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".StartCandleTime",value))return false;x.StartCandleTime=(datetime)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".LastUpdateBar",value))return false;x.LastUpdateBar=(int)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".LastUpdateCandleTime",value))return false;x.LastUpdateCandleTime=(datetime)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".ConfirmationBar",value))return false;x.ConfirmationBar=(int)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".ConfirmationCandleTime",value))return false;x.ConfirmationCandleTime=(datetime)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".ConfirmationClose",value))return false;x.ConfirmationClose=StringToDouble(value);
 if(!OriginReadKey(h,prefix+".RetestBar",value))return false;x.RetestBar=(int)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".RetestCandleTime",value))return false;x.RetestCandleTime=(datetime)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".DirectionTakeoverBar",value))return false;x.DirectionTakeoverBar=(int)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".DirectionTakeoverCandleTime",value))return false;x.DirectionTakeoverCandleTime=(datetime)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".VoidBar",value))return false;x.VoidBar=(int)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".VoidCandleTime",value))return false;x.VoidCandleTime=(datetime)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".SupersededBar",value))return false;x.SupersededBar=(int)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".SupersededCandleTime",value))return false;x.SupersededCandleTime=(datetime)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".InvalidationWindowOpen",value))return false;x.InvalidationWindowOpen=(StringToInteger(value)!=0);
 if(!OriginReadKey(h,prefix+".IsValid",value))return false;x.IsValid=(StringToInteger(value)!=0);
 if(!OriginReadKey(h,prefix+".SupersessionCandidateActive",value))return false;x.SupersessionCandidateActive=(StringToInteger(value)!=0);
 if(!OriginReadKey(h,prefix+".SupersessionRawBar",value))return false;x.SupersessionRawBar=(int)StringToInteger(value);
 if(!OriginReadKey(h,prefix+".SupersessionRawCandleTime",value))return false;x.SupersessionRawCandleTime=(datetime)StringToInteger(value);
 return true;
}
bool WriteOriginSnapshot(int h,string prefix,OriginOwners &x){return WriteOriginExtremeLifecycleData(h,prefix+".buy",x.buy) && WriteOriginExtremeLifecycleData(h,prefix+".sell",x.sell) && WriteOriginMLVData(h,prefix+".mhvBuy",x.mhvBuy) && WriteOriginMLVData(h,prefix+".mhvSell",x.mhvSell);}
bool ReadOriginSnapshot(int h,string prefix,OriginOwners &x){return ReadOriginExtremeLifecycleData(h,prefix+".buy",x.buy) && ReadOriginExtremeLifecycleData(h,prefix+".sell",x.sell) && ReadOriginMLVData(h,prefix+".mhvBuy",x.mhvBuy) && ReadOriginMLVData(h,prefix+".mhvSell",x.mhvSell);}
#endif
