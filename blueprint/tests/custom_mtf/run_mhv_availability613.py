from pathlib import Path
import json,hashlib,subprocess,shutil,re,sys
r=Path(r'D:\BBMA\MT4_CustomMTF_302_Unit');repo=r/'mhv613-stage';kind=sys.argv[1]
assert kind in ['red','green']
e=r/('evidence/sig06_mhv/availability613_'+kind);assert not e.exists();e.mkdir(parents=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();lf=lambda p:hashlib.sha256(p.read_text().encode()).hexdigest()
source=repo/'blueprint/source/BBMA_EA.mq4'
if kind=='red':assert lf(source)=='900744561bd5e5c5abaef754478a055fcf600bf178fe3174da2d484dd840f2e8'
h=repo/'blueprint/tests/custom_mtf/CustomMHVAvailabilityHarness.mq4';log=e/'compile.log'
subprocess.run([str(r/'metaeditor.exe'),'/compile:'+str(h),'/log:'+str(log)],timeout=60)
result=next(x for x in log.read_bytes().decode('utf-16').splitlines() if 'Result:' in x);assert '0 errors, 0 warnings' in result,result
shutil.copyfile(h.with_suffix('.ex4'),r/'MQL4/Experts'/h.with_suffix('.ex4').name);shutil.copyfile(h,e/h.name);shutil.copyfile(h.with_suffix('.ex4'),e/h.with_suffix('.ex4').name);shutil.copyfile(source,e/'BBMA_EA.mq4')
cfg=(r/'config/parser_green.ini').read_text().replace('CustomFormulaHarness',h.stem).replace('parser_green.html','availability613_'+kind+'.html');assert 'ExpertsTrades=false' in cfg
ini=e/'test.ini';ini.write_text(cfg);logs=r/'tester/logs';before={x:x.stat().st_size for x in logs.glob('*.log')}
p=subprocess.Popen([str(r/'terminal.exe'),'/portable',str(ini)],cwd=r);pid=p.pid;code=p.wait(timeout=120);assert code==0
rows=[]
for q in logs.glob('*.log'):
 with q.open('rb') as f:f.seek(before.get(q,0));rows.extend(x for x in f.read().decode(errors='replace').splitlines() if '[MHV-AVAILABLE' in x)
summaries=[x for x in rows if '-SUMMARY]' in x];assert len(summaries)==1,summaries
m=re.search(r'passed=(\d+) failed=(\d+)',summaries[0]);assert m
manifest={'mode':kind,'source_sha256_lf':lf(source),'harness_sha256_lf':lf(h),'binary_sha256':sha(h.with_suffix('.ex4')),'compile':result,'terminal_pid':pid,'terminal_exit':code,'passed':int(m[1]),'failed':int(m[2]),'rows':rows}
(e/'manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({k:v for k,v in manifest.items() if k!='rows'}),flush=True)
if kind=='red':assert int(m[2])>0
else:assert int(m[2])==0
