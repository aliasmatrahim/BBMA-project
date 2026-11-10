"""Approved eCSD Close-only behavior; extracted source, not native/runtime proof."""
from pathlib import Path
import re,subprocess,tempfile

def test_ecsd_close_only_and_closed_shift():
 s=Path('blueprint/source/BBMA_EA.mq4').read_text()
 def fn(name):
  m=re.search(r'bool '+name+r'\s*\(',s);assert m,name
  start=s.index('{',m.start());i=start+1;depth=1
  while depth:
   depth+=(s[i]=='{')-(s[i]=='}');i+=1
  return s[m.start():i]
 names=['CandleBodyCrossesLevel','M10_CandleBodyCrossesMAPair']
 if 'bool M10_CandleClosesBeyondMAPair(' in s:names+=['M10_CandleClosesBeyondMAPair']
 names+=['DetectECSD']
 code='''#include <string>
#include <iostream>
using string=std::string;
enum ENUM_DIRECTION{DIR_NONE=0,DIR_BUY=1,DIR_SELL=-1};
struct MovingAverage{double MA5_High,MA10_High,MA5_Low,MA10_Low,EMA50;};
double O,C;int openReads=0;
double iOpen(string,int,int){openReads++;return O;}
double iClose(string,int,int){return C;}
'''+ '\n'.join(fn(n) for n in names)+'''
int main(){MovingAverage ma={101,101.5,99,98.5,100};
O=105;C=102;if(!DetectECSD("FIXTURE",15,DIR_BUY,1,ma)){std::cerr<<"BUY close beyond both MAs rejected solely due Open";return 1;}
O=95;C=98;if(!DetectECSD("FIXTURE",15,DIR_SELL,1,ma)){std::cerr<<"SELL close beyond both MAs rejected solely due Open";return 2;}
for(int t: {1,5,15,30,60,240,1440})for(int o=-1;o<=110;o++){
 O=o;C=102;if(!DetectECSD("FIXTURE",t,DIR_BUY,1,ma))return 3;
 C=98;if(!DetectECSD("FIXTURE",t,DIR_SELL,1,ma))return 4;
}
if(openReads!=0){std::cerr<<"Open accessed by eCSD";return 5;}
C=101.5;if(DetectECSD("FIXTURE",15,DIR_BUY,1,ma))return 6;
C=98.5;if(DetectECSD("FIXTURE",15,DIR_SELL,1,ma))return 7;
C=102;if(DetectECSD("FIXTURE",15,DIR_BUY,0,ma)||DetectECSD("FIXTURE",15,DIR_BUY,-1,ma))return 8;
if(DetectECSD("FIXTURE",15,DIR_NONE,1,ma))return 9;
C=0;if(DetectECSD("FIXTURE",15,DIR_BUY,1,ma))return 10;
C=102;ma.MA5_High=0;if(DetectECSD("FIXTURE",15,DIR_BUY,1,ma))return 11;
return 0;}
'''
 with tempfile.TemporaryDirectory() as tmp:
  p=Path(tmp);(p/'test.cpp').write_text(code)
  subprocess.run(['g++','-std=c++11',str(p/'test.cpp'),'-o',str(p/'test')],check=True)
  run=subprocess.run([str(p/'test')],capture_output=True,text=True)
  assert run.returncode==0,run.stderr or f'case failure {run.returncode}'
