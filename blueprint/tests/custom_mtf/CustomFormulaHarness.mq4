#property strict
// Native unit harness: no detection, account changes or broker order functions.
#ifndef CUSTOM_TEST_BASELINE
#include "..\\..\\source\\custom_mtf\\CustomFormula.mqh"
#endif
int failed=0, passed=0;
void Check(string text,bool expected,int expectedAtoms)
{
   bool actual=false;
   int atoms=0;
#ifndef CUSTOM_TEST_BASELINE
   CustomFormula result; string reason;
   actual=ParseCustomFormula(text,result,reason);
   atoms=result.atomCount;
#endif
   bool ok=(actual==expected && (!actual || atoms==expectedAtoms));
   if(ok) passed++; else failed++;
   Print("[CUSTOM-PARSER] ",ok?"PASS":"FAIL"," text=",text," accepted=",actual," atoms=",atoms);
}
void CheckStructure(bool ok,string name)
{
   if(ok) passed++; else failed++;
   Print("[CUSTOM-STRUCTURE] ",ok?"PASS":"FAIL"," ",name);
}
#ifndef CUSTOM_TEST_BASELINE
void RunStructureCases()
{
   CustomFormula f; string reason;
   bool ok=ParseCustomFormula("D1:RE AND (H4:RE OR H1:RE)",f,reason);
   CheckStructure(ok && f.groupCount==2 && f.atomCount==3 &&
      f.atoms[0].group==0 && f.atoms[1].group==1 && f.atoms[2].group==1 &&
      f.atoms[0].timeframe==PERIOD_D1 && f.atoms[1].timeframe==PERIOD_H4 &&
      f.atoms[2].timeframe==PERIOD_H1 && f.atoms[0].signal=="RE","AND_OR_WITNESS_LAYOUT");
   ok=ParseCustomFormula("M1:MOM OR M5:MOM",f,reason);
   CheckStructure(ok && f.groupCount==1 && f.atomCount==2 &&
      f.atoms[0].group==0 && f.atoms[1].group==0,"BARE_OR_SINGLE_GROUP");
   ok=ParseCustomFormula("D1:RE",f,reason);
   CheckStructure(ok && f.atomCount==1 && f.groupCount==1,"REUSED_VALID");
   ok=ParseCustomFormula("D1:RE AND",f,reason);
   CheckStructure(!ok && f.atomCount==0 && f.groupCount==0 && reason!="","REUSED_INVALID_CLEARS_COUNTS");
   ok=ParseCustomFormula("M5:MOM",f,reason);
   CheckStructure(ok && f.atomCount==1 && f.groupCount==1 && reason=="" &&
      f.atoms[0].timeframe==PERIOD_M5 && f.atoms[0].signal=="MOM","REUSED_VALID_RESTORED");
   ok=ParseCustomFormula(" d1 : re1 ",f,reason);
   CheckStructure(ok && f.atoms[0].signal=="RE1" && f.atoms[0].timeframe==PERIOD_D1,"NORMALIZED_VALUES");
   ok=ParseCustomFormula("M1:RE1 AND M5:RE2 AND M15:RE3 AND M30:RE4 AND H1:EXT AND H4:MOM AND D1:MLV",f,reason);
   CheckStructure(ok && f.atomCount==7 && f.groupCount==7 &&
      f.atoms[0].timeframe==PERIOD_M1 && f.atoms[1].timeframe==PERIOD_M5 &&
      f.atoms[2].timeframe==PERIOD_M15 && f.atoms[3].timeframe==PERIOD_M30 &&
      f.atoms[4].timeframe==PERIOD_H1 && f.atoms[5].timeframe==PERIOD_H4 &&
      f.atoms[6].timeframe==PERIOD_D1 && f.atoms[6].group==6,"SEVEN_TIMEFRAME_VALUES");
}
#endif
int OnInit()
{
   Check("D1:RE AND H4:RE",true,2);
   Check("M15:MOM OR M5:MOM",true,2);
   Check("D1:RE AND (H4:RE OR H1:RE)",true,3);
   Check("  d1 : re  AND h4 : re1 ",true,2);
   Check("M1:RE1 AND M5:RE2 AND M15:RE3 AND M30:RE4 AND H1:EXT AND H4:MOM AND D1:MLV",true,7);
   Check("M1:RE1 AND M5:RE2 AND M15:RE3 AND M30:RE4 AND H1:EXT AND H4:MOM AND D1:MLV AND D1:MHV",false,0);
   Check("",false,0); Check(" ",false,0);
   Check("M2:MOM",false,0); Check("H1:UNKNOWN",false,0);
   Check("D1:RE AND",false,0); Check("OR M1:MOM",false,0);
   Check("(D1:RE OR (H4:RE OR H1:RE))",false,0);
   Check("D1:RE AND H4:RE OR H1:RE",false,0);
   Check("H1:RE AND H1:RE",false,0);
   Check("h1:re OR H1:RE",false,0);
   Check("NOT H1:RE",false,0); Check("D1;RE",false,0);
   Check("(H4:RE)",false,0); Check("H4:RE H1:RE",false,0);
   Check("H4:RE AND ()",false,0); Check("H4:RE OR",false,0);
   Check("H4:RE AND (H1:RE OR M15:MOM) AND M1:MOM",true,4);
#ifndef CUSTOM_TEST_BASELINE
   RunStructureCases();
#endif
   Print("[CUSTOM-PARSER-SUMMARY] passed=",passed," failed=",failed);
   int f=FileOpen("CUSTOM_PARSER_RESULT.txt",FILE_WRITE|FILE_TXT);
   if(f!=INVALID_HANDLE){FileWrite(f,"passed="+IntegerToString(passed)+" failed="+IntegerToString(failed));FileClose(f);}
   return failed==0 ? INIT_SUCCEEDED : INIT_FAILED;
}
void OnTick() {}
