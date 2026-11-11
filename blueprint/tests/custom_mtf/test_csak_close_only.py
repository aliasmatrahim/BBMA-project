"""Catches the rejected Open restriction, missing-line acceptance and live-bar reads."""
from pathlib import Path
import re, subprocess, tempfile

def test_csak_closed_price_beyond_all_three_lines():
 s=Path('blueprint/source/BBMA_EA.mq4').read_text()
 def fn(name):
  m=re.search(r'bool '+name+r'\s*\(',s);assert m,name
  start=s.index('{',m.start());end=start+1;depth=1
  while depth:
   depth+=(s[end]=='{')-(s[end]=='}');end+=1
  return s[m.start():end]
 names=[n for n in ['CandleBodyCrossesLevel','M10_CandleBodyCrossesMAPair','M10_CandleClosesBeyondMAPair','M10_CandleClosesBeyondMid'] if 'bool '+n+'(' in s]+['DetectCSD']
 code='''#include <string>
#include <cmath>
#include <iostream>
using string=std::string;
enum ENUM_DIRECTION{DIR_NONE=0,DIR_BUY=1,DIR_SELL=-1};
struct MovingAverage{double MA5_High,MA10_High,MA5_Low,MA10_Low,EMA50;};
struct BollingerBand{double TOP_BB,MID_BB,LOW_BB,Width;};
double O,C;int opens=0;
double iOpen(string,int,int){opens++;return O;}
double iClose(string,int,int){return C;}
bool MathIsValidNumber(double v){return std::isfinite(v);}
'''+ '\n'.join(fn(n) for n in names)+'''
int main(){MovingAverage ma={101,101.5,99,98.5,100};BollingerBand bb={200,100,50,150};
 O=105;C=102;
 if(!DetectCSD("FIXTURE",15,DIR_BUY,1,ma,bb)){std::cerr<<"CSAK Close beyond MA5/MA10/Mid rejected solely due Open";return 1;}
 O=95;C=98;if(!DetectCSD("FIXTURE",15,DIR_SELL,1,ma,bb))return 2;
 for(int tf:{1,5,15,30,60,240,1440})for(int o=-1;o<=110;o++){
  O=o;C=102;if(!DetectCSD("FIXTURE",tf,DIR_BUY,1,ma,bb))return 3;
  C=98;if(!DetectCSD("FIXTURE",tf,DIR_SELL,1,ma,bb))return 4;
 }
 if(opens!=0)return 5;
 C=101.5;if(DetectCSD("FIXTURE",15,DIR_BUY,1,ma,bb))return 6;
 C=98.5;if(DetectCSD("FIXTURE",15,DIR_SELL,1,ma,bb))return 7;
 C=102;bb.MID_BB=102;if(DetectCSD("FIXTURE",15,DIR_BUY,1,ma,bb))return 8;
 C=98;bb.MID_BB=98;if(DetectCSD("FIXTURE",15,DIR_SELL,1,ma,bb))return 9;
 C=102;bb.MID_BB=103;if(DetectCSD("FIXTURE",15,DIR_BUY,1,ma,bb))return 10;
 C=98;bb.MID_BB=97;if(DetectCSD("FIXTURE",15,DIR_SELL,1,ma,bb))return 11;
 bb.MID_BB=100;C=102;
 if(DetectCSD("FIXTURE",15,DIR_BUY,0,ma,bb)||DetectCSD("FIXTURE",15,DIR_BUY,-1,ma,bb)||DetectCSD("FIXTURE",15,DIR_NONE,1,ma,bb))return 12;
 return 0;}
'''
 with tempfile.TemporaryDirectory() as tmp:
  p=Path(tmp);(p/'case.cpp').write_text(code)
  subprocess.run(['g++','-std=c++11',str(p/'case.cpp'),'-o',str(p/'case')],check=True)
  run=subprocess.run([str(p/'case')],capture_output=True,text=True)
  assert run.returncode==0,run.stderr or f'case failure {run.returncode}'
