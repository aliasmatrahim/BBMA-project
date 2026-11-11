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
helper=fn('M10_CandleClosesBeyondMAPair')
code='enum ENUM_DIRECTION {DIR_NONE=0,DIR_BUY=1,DIR_SELL=-1};\n'+helper+'''
int main(){for(int d=-1;d<=1;d++)for(int c=0;c<=8;c++)for(int a=0;a<=8;a++)for(int b=0;b<=8;b++){
 bool expected=c>0 && a>0 && b>0 && ((d==1 && c>a && c>b)||(d==-1 && c<a && c<b));
 if(M10_CandleClosesBeyondMAPair(c,a,b,(ENUM_DIRECTION)d)!=expected)return 1;
}return 0;}
'''
with tempfile.TemporaryDirectory() as t:
 p=Path(t);(p/'test.cpp').write_text(code)
 subprocess.run(['g++','-std=c++11',str(p/'test.cpp'),'-o',str(p/'test')],check=True)
 subprocess.run([str(p/'test')],check=True)
print('M10_CLOSE_PAIR_EQUIVALENCE_PASS cases=2187; host numeric equivalence only')
assert fn('DetectCSD').count('M10_CandleClosesBeyondMAPair(')==2
assert 'iOpen(' not in fn('DetectCSD')
assert fn('DetectECSD').count('M10_CandleClosesBeyondMAPair(')==2
assert 'iOpen(' not in fn('DetectECSD')
