"""Offline numerical/source comparison only. Never imported by EA or signal owners."""
from pathlib import Path
from itertools import product
import hashlib,json,re,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
source=(ROOT/'blueprint/source/BBMA_EA.mq4').read_text()
sha=hashlib.sha256(source.encode()).hexdigest()
assert sha=='0266fb3318348ae64b7bbbb52a1b30a0e79994df64979377cd14c1ba877c666e'
def fn(name):
    m=re.search(r'bool '+name+r'\s*\(',source);assert m,name
    start=source.index('{',m.start());i=start+1;depth=1
    while depth:
        depth+=(source[i]=='{')-(source[i]=='}');i+=1
    return source[m.start():i]
def calc(o,c,m,a,b,d):
    if d=='BUY':
        close=c>max(m,a,b)
        return {'A':o<=min(m,a,b) and close,'B':close,'C':o<m and close}
    close=c<min(m,a,b)
    return {'A':o>=max(m,a,b) and close,'B':close,'C':o>m and close}
# Explicit expected witnesses. Numbers are hypothetical geometry, not market OHLC.
cases=[
 ('cross_all',99,105,100,102,104,(True,True,True)),
 ('open_past_MAs_before_Mid',99.5,101,100,98,99,(False,True,True)),
 ('open_past_Mid',101,105,100,102,104,(False,True,False)),
 ('continuation_bull',105,106,100,102,104,(False,True,False)),
 ('bear_body_above_cluster',106,105,100,102,104,(False,True,False)),
 ('open_equals_Mid',100,105,100,102,104,(True,True,False)),
 ('open_equals_MA',98,101,100,98,99,(True,True,True)),
 ('close_equals_outer_required_line',99,104,100,102,104,(False,False,False))]
rows=[]
for d in ['BUY','SELL']:
    for label,o,c,m,a,b,expected in cases:
        if d=='SELL':o,c,m,a,b=[200-x for x in [o,c,m,a,b]]
        got=calc(o,c,m,a,b,d);assert tuple(got.values())==expected,(label,d,got)
        rows.append({'case':label,'side':d,'O':o,'C':c,'Mid':m,'MA5':a,'MA10':b,'result':got})
counts={'cases':0,'A_true':0,'B_true':0,'C_true':0,'A_not_C':0,'C_not_A':0}
for d in ['BUY','SELL']:
    for o,c,m,a,b in product(range(98,105),repeat=5):
        v=calc(o,c,m,a,b,d);counts['cases']+=1
        for k in 'ABC':counts[k+'_true']+=int(v[k])
        assert not v['A'] or v['B']
        assert not v['C'] or v['B']
        if v['A'] and not v['C']:assert o==m;counts['A_not_C']+=1
        if v['C'] and not v['A']:counts['C_not_A']+=1
        ordinary=(a>=m and b>=m) if d=='BUY' else (a<=m and b<=m)
        if ordinary and o!=m:assert v['A']==v['C']
# Actual source extraction verifies A against DetectCSD, with platform I/O stubs.
code='''#include <string>
#include <algorithm>
#include <iostream>
using string=std::string;
enum ENUM_DIRECTION{DIR_NONE=0,DIR_BUY=1,DIR_SELL=-1};
struct MovingAverage{double MA5_High,MA10_High,MA5_Low,MA10_Low,EMA50;};
struct BollingerBand{double MID_BB;};
double gOpen,gClose;
double iOpen(string,int,int){return gOpen;}
double iClose(string,int,int){return gClose;}
'''+ '\n'.join(fn(n) for n in ['CandleBodyCrossesLevel','M10_CandleBodyCrossesMAPair','DetectCSD'])+'''
int main(){int count=0;
for(int dir=-1;dir<=1;dir+=2)for(int o=98;o<=104;o++)for(int c=98;c<=104;c++)
for(int m=98;m<=104;m++)for(int a=98;a<=104;a++)for(int b=98;b<=104;b++){
gOpen=o;gClose=c;MovingAverage ma={(double)a,(double)b,(double)a,(double)b,100};BollingerBand bb={(double)m};
bool expected=dir==1?(o<=std::min(m,std::min(a,b))&&c>std::max(m,std::max(a,b))):(o>=std::max(m,std::max(a,b))&&c<std::min(m,std::min(a,b)));
if(DetectCSD("FIXTURE",15,(ENUM_DIRECTION)dir,1,ma,bb)!=expected){return 1;}
count++;
}std::cout<<count;return 0;}
'''
with tempfile.TemporaryDirectory() as tmp:
    p=Path(tmp);(p/'compare.cpp').write_text(code)
    compiled=subprocess.run(['g++','-std=c++11','-Wall','-Wextra',str(p/'compare.cpp'),'-o',str(p/'compare')],capture_output=True,text=True)
    assert compiled.returncode==0,compiled.stderr
    run=subprocess.run([str(p/'compare')],check=True,capture_output=True,text=True)
    assert run.stdout=='33614',run.stdout
result={'task':'C/T04-D three-formula source comparison','base_commit':'a149da67d578c19a94d12f6e0d14bd8d9ea8f865','source_sha256_lf':sha,'scope':'Offline hypothetical positive finite values; actual DetectCSD extracted into host C++ with I/O stubs. Not native MQL4/runtime/market/source-authority proof. B is bare close-side, with no silent colour/first-event rule.','witnesses':rows,'exhaustive_geometry':counts,'source_A_cpp_equivalence_cases':33614,'host_compile_returncode':compiled.returncode,'host_compile_warnings':compiled.stderr,'formula_C_source':'https://publikasi.uyelindo.ac.id/index.php/semmau/article/download/236/205/570 printed179','ruling':'A currently locked; B/C not admitted; founder numerical open/equality/event proof unresolved'}
(OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'witnesses':len(rows),'geometry':counts,'actual_source_A_equivalence':33614,'host_compile_warnings':compiled.stderr,'status':'PASS (offline scope only)'}))
