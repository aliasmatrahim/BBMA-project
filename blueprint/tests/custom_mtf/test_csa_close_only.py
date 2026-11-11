"""SIG-02 actual extracted M10 classifier: MidBB alone, never MA/Open/MOM gates."""
from pathlib import Path
import re, subprocess, tempfile

def test_csa_midbb_direction_boundaries():
    source=Path('blueprint/source/BBMA_EA.mq4').read_text()
    match=re.search(r'bool M10_CandleClosesBeyondMid\(',source)
    assert match, 'CSA MidBB classifier missing; owner currently unavailable'
    start=source.index('{',match.start());end=start+1;depth=1
    while depth:
        depth+=(source[end]=='{')-(source[end]=='}');end+=1
    code='''#include <cmath>
#include <initializer_list>
#include <limits>
enum ENUM_DIRECTION{DIR_NONE=0,DIR_BUY=1,DIR_SELL=-1};
bool MathIsValidNumber(double v){return std::isfinite(v);}
'''+source[match.start():end]+'''
int main(){
 for(int d=-1;d<=1;d++)for(int c=-1;c<=110;c++)for(int m=-1;m<=110;m++){
  bool expected=c>0&&m>0&&((d==1&&c>m)||(d==-1&&c<m));
  if(M10_CandleClosesBeyondMid(c,m,(ENUM_DIRECTION)d)!=expected)return 1;
 }
 double bad[]={std::numeric_limits<double>::infinity(),-std::numeric_limits<double>::infinity(),std::numeric_limits<double>::quiet_NaN()};
 for(double v:bad)for(int d:{-1,1})if(M10_CandleClosesBeyondMid(v,100,(ENUM_DIRECTION)d)||M10_CandleClosesBeyondMid(100,v,(ENUM_DIRECTION)d))return 2;
 return 0;
}
'''
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp);(p/'case.cpp').write_text(code)
        subprocess.run(['g++','-std=c++11',str(p/'case.cpp'),'-o',str(p/'case')],check=True)
        subprocess.run([str(p/'case')],check=True)
