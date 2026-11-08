from pathlib import Path
import re,subprocess,tempfile
s=Path('blueprint/source/BBMA_EA.mq4').read_text()
def fn(name):
 m=re.search(r'bool '+name+r'\s*\(',s)
 assert m, name+' missing'
 start=s.index('{',m.start());depth=1;i=start+1
 while depth:
  depth+=(s[i]=='{')-(s[i]=='}');i+=1
 return s[m.start():i]
helper=fn('M10_CandleBodyCrossesMAPair')
for name in ('DetectCSD','DetectECSD'):
 b=fn(name)
 assert b.count('M10_CandleBodyCrossesMAPair(')==2
 assert 'CandleBodyCrossesLevel(open, close, ma.' not in b
code='enum ENUM_DIRECTION {DIR_NONE=0,DIR_BUY=1,DIR_SELL=-1};\n'+fn('CandleBodyCrossesLevel')+'\n'+helper+'''
int main(){for(int d=-1;d<=1;d++)for(int o=0;o<=8;o++)for(int c=0;c<=8;c++)for(int a=0;a<=8;a++)for(int b=0;b<=8;b++){
 bool expected=CandleBodyCrossesLevel(o,c,a,(ENUM_DIRECTION)d)&&CandleBodyCrossesLevel(o,c,b,(ENUM_DIRECTION)d);
 if(M10_CandleBodyCrossesMAPair(o,c,a,b,(ENUM_DIRECTION)d)!=expected)return 1;
}return 0;}
'''
with tempfile.TemporaryDirectory() as t:
 p=Path(t);(p/'test.cpp').write_text(code)
 subprocess.run(['g++','-std=c++11',str(p/'test.cpp'),'-o',str(p/'test')],check=True)
 subprocess.run([str(p/'test')],check=True)
print('M10_SHARED_PAIR_EQUIVALENCE_PASS cases=19683; numeric C++ equivalence only, not native MQL4 runtime')
