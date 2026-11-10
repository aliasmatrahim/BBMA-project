from pathlib import Path
import subprocess,json,hashlib,shutil
r=Path(r'D:\BBMA\MT4_CustomMTF_302_Unit');repo=r/'ext611-stage';e=r/'evidence/sig05_extreme'
assert json.loads((r/'ext611_regression_state.json').read_text())['status']=='PASS'
sp=r/'ext611_extra_state.json';assert not sp.exists();state={'status':'RUNNING','completed':[]};sp.write_text(json.dumps(state))
args=['python',str(repo/'blueprint/tests/custom_mtf/run_clock_owner_native.py'),'--root',str(r),'--repo',str(repo),'--evidence-root',str(e),'--kind','owner']
with (e/'driver611_owner.log').open('w') as out:p=subprocess.run(args,stdout=out,stderr=subprocess.STDOUT)
assert p.returncode==0,(e/'driver611_owner.log').read_text()[-4000:]
state['completed'].append('owner');sp.write_text(json.dumps(state));print('OWNER10_PASS',flush=True)
src=r/'mom610-stage/blueprint/source/BBMA_EA.mq4';assert hashlib.sha256(src.read_text().encode()).hexdigest()=='ebe3e4155b0ae5211432957ed999e04b58bc0a043b40a23ce76d24257346baae'
dst=repo/'blueprint/source/BBMA_EA_ExtremeBaseline610.mq4';dst.write_text(src.read_text())
h=repo/'blueprint/tests/custom_mtf/CustomExtremeLifecycleBaselineHarness.mq4';h.write_text((repo/'blueprint/tests/custom_mtf/CustomExtremeLifecycleHarness.mq4').read_text().replace('BBMA_EA.mq4','BBMA_EA_ExtremeBaseline610.mq4'))
be=e/'baseline610_lifecycle';be.mkdir(exist_ok=True);log=be/'compile.log'
subprocess.run([str(r/'metaeditor.exe'),'/compile:'+str(h),'/log:'+str(log)],timeout=60)
result=next(x for x in log.read_bytes().decode('utf-16').splitlines() if 'Result:' in x);assert '0 errors, 0 warnings' in result,result
shutil.copyfile(h.with_suffix('.ex4'),r/'MQL4/Experts'/h.with_suffix('.ex4').name)
cfg=(r/'config/parser_green.ini').read_text().replace('CustomFormulaHarness',h.stem).replace('parser_green.html','extreme_baseline610_lifecycle.html');assert 'ExpertsTrades=false' in cfg
ini=be/'run.ini';ini.write_text(cfg);logs=r/'tester/logs';before={x:x.stat().st_size for x in logs.glob('*.log')}
subprocess.run([str(r/'terminal.exe'),'/portable',str(ini)],cwd=r,timeout=90,check=True)
rows=[]
for p in logs.glob('*.log'):
 with p.open('rb') as f:f.seek(before.get(p,0));rows.extend(x for x in f.read().decode(errors='replace').splitlines() if '[EXT-LIFE' in x)
assert any('passed=716 failed=0 history=140' in x for x in rows),rows[-15:]
manifest={'source_sha256_lf':hashlib.sha256(dst.read_text().encode()).hexdigest(),'harness_sha256_lf':hashlib.sha256(h.read_text().encode()).hexdigest(),'binary_sha256':hashlib.sha256(h.with_suffix('.ex4').read_bytes()).hexdigest(),'compile':result,'expected':'passed=716 failed=0 history=140','rows':rows,'scope':'Frozen6.10 actual M08 valid lifecycle/history suite with the same716 assertions and140 history samples; no source repair or orders.'}
(be/'manifest.json').write_text(json.dumps(manifest,indent=2));state['completed'].append('baseline610_lifecycle');state['status']='PASS';sp.write_text(json.dumps(state));print('EXT_EXTRA_PASS',flush=True)
