#ifndef BBMA_CUSTOM_FORMULA_V1
#define BBMA_CUSTOM_FORMULA_V1
// Engineering configuration syntax only. No signal or execution authority.
#define CUSTOM_MTF_PARSER_REV "CUSTOM_MTF_PARSER_001_20261108"
#define CUSTOM_MAX_ATOMS 7
struct CustomAtom
{
   int timeframe;
   string signal;
   int group;
};
struct CustomFormula
{
   int atomCount;
   int groupCount;
   CustomAtom atoms[CUSTOM_MAX_ATOMS];
};
void CustomSkipSpace(string text,int &pos)
{
   while(pos<StringLen(text))
   {
      ushort c=StringGetCharacter(text,pos);
      if(c!=32 && c!=9 && c!=10 && c!=13) break;
      pos++;
   }
}
string CustomWord(string text,int &pos)
{
   CustomSkipSpace(text,pos);
   int start=pos;
   while(pos<StringLen(text))
   {
      ushort c=StringGetCharacter(text,pos);
      if(!((c>=65 && c<=90)||(c>=48 && c<=57)||c==95)) break;
      pos++;
   }
   return StringSubstr(text,start,pos-start);
}
int CustomTimeframe(string token)
{
   if(token=="M1") return PERIOD_M1;
   if(token=="M5") return PERIOD_M5;
   if(token=="M15") return PERIOD_M15;
   if(token=="M30") return PERIOD_M30;
   if(token=="H1") return PERIOD_H1;
   if(token=="H4") return PERIOD_H4;
   if(token=="D1") return PERIOD_D1;
   return 0;
}
bool CustomKnownSignal(string token)
{
   return token=="RE" || token=="RE1" || token=="RE2" || token=="RE3" ||
          token=="RE4" || token=="EXT" || token=="MHV" || token=="MLV" ||
          token=="CSA" || token=="CSAK" || token=="MOM";
}
bool CustomParseAtom(string text,int &pos,int group,CustomFormula &out,string &reason)
{
   int tf=CustomTimeframe(CustomWord(text,pos));
   if(tf==0){reason="UNKNOWN_TIMEFRAME@"+IntegerToString(pos);return false;}
   CustomSkipSpace(text,pos);
   if(pos>=StringLen(text) || StringGetCharacter(text,pos)!=58)
   {reason="EXPECTED_COLON@"+IntegerToString(pos);return false;}
   pos++;
   string signal=CustomWord(text,pos);
   if(!CustomKnownSignal(signal)){reason="UNKNOWN_SIGNAL@"+IntegerToString(pos);return false;}
   if(out.atomCount>=CUSTOM_MAX_ATOMS){reason="TOO_MANY_ATOMS";return false;}
   for(int i=0;i<out.atomCount;i++)
      if(out.atoms[i].timeframe==tf && out.atoms[i].signal==signal)
      {reason="DUPLICATE_ATOM@"+IntegerToString(pos);return false;}
   out.atoms[out.atomCount].timeframe=tf;
   out.atoms[out.atomCount].signal=signal;
   out.atoms[out.atomCount].group=group;
   out.atomCount++;
   return true;
}
bool CustomParseGroup(string text,int &pos,int group,CustomFormula &out,string &reason,bool &parenthesized)
{
   CustomSkipSpace(text,pos);
   parenthesized=(pos<StringLen(text) && StringGetCharacter(text,pos)==40);
   if(!parenthesized) return CustomParseAtom(text,pos,group,out,reason);
   pos++;
   if(!CustomParseAtom(text,pos,group,out,reason)) return false;
   int alternatives=1;
   while(true)
   {
      CustomSkipSpace(text,pos);
      if(pos>=StringLen(text)){reason="UNCLOSED_OR_GROUP";return false;}
      if(StringGetCharacter(text,pos)==41)
      {
         pos++;
         if(alternatives<2){reason="OR_GROUP_REQUIRES_ALTERNATIVE";return false;}
         return true;
      }
      if(CustomWord(text,pos)!="OR"){reason="EXPECTED_OR@"+IntegerToString(pos);return false;}
      if(!CustomParseAtom(text,pos,group,out,reason)) return false;
      alternatives++;
   }
}
bool ParseCustomFormula(string text,CustomFormula &out,string &reason)
{
   out.atomCount=0;out.groupCount=0;reason="";
   StringToUpper(text);
   int pos=0;bool parenthesized=false;
   if(!CustomParseGroup(text,pos,0,out,reason,parenthesized))
   {out.atomCount=0;out.groupCount=0;return false;}
   out.groupCount=1;
   string outerOperator="";
   while(true)
   {
      CustomSkipSpace(text,pos);
      if(pos==StringLen(text)) return true;
      string op=CustomWord(text,pos);
      if(op!="AND" && op!="OR")
      {reason="EXPECTED_OPERATOR@"+IntegerToString(pos);break;}
      if(outerOperator!="" && outerOperator!=op)
      {reason="MIXED_UNGROUPED_OPERATORS";break;}
      outerOperator=op;
      // Top-level OR is one alternative group, never combined with AND/nesting.
      if(op=="OR" && parenthesized){reason="NESTED_OR_NOT_SUPPORTED";break;}
      int group=(op=="OR" ? 0 : out.groupCount);
      bool nextParenthesized=false;
      if(!CustomParseGroup(text,pos,group,out,reason,nextParenthesized)) break;
      if(op=="OR" && nextParenthesized){reason="NESTED_OR_NOT_SUPPORTED";break;}
      if(op=="AND") out.groupCount++;
   }
   out.atomCount=0;out.groupCount=0;
   return false;
}
#endif
