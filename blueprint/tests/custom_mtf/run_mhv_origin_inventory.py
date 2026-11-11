from pathlib import Path
import json,hashlib,subprocess,shutil,csv
r=Path(r'D:\BBMA\MT4_CustomMTF_302_Unit');repo=r/'ext611-stage';e=r/'evidence/sig06_mhv/origin_inventory_v1';assert not e.exists();e.mkdir(parents=True)
index=json.loads(Path(r'D:\MARKET_DATA_INDEX.json').read_text(encoding='utf-8-sig'));assert 'sources' in index
source=repo/'blueprint/source/BBMA_EA.mq4';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();lf=lambda p:hashlib.sha256(p.read_text().encode()).hexdigest()
assert lf(source)=='a62672ae1874fcbf61c671af01da09ef45ffe6972abd998ec70c5f9a74c238cb'
inputs={str(p):sha(p) for p in (r/'history').rglob('GBPUSD*.hst')}
assert inputs,'No existing GBPUSD HST'
h=repo/'blueprint/tests/custom_mtf/CustomMHVOriginInventoryHarness.mq4';log=e/'compile.log';log.unlink(missing_ok=True)
subprocess.run([str(r/'metaeditor.exe'),'/compile:'+str(h),'/log:'+str(log)],timeout=60)
result=next(x for x in log.read_bytes().decode('utf-16').splitlines() if 'Result:' in x);assert '0 errors, 0 warnings' in result,result
shutil.copyfile(h.with_suffix('.ex4'),r/'MQL4/Experts'/h.with_suffix('.ex4').name)
cfg=(r/'config/parser_green.ini').read_text().replace('CustomFormulaHarness',h.stem).replace('parser_green.html','mhv_origin_inventory_v1.html');assert 'ExpertsTrades=false' in cfg
ini=e/'run.ini';ini.write_text(cfg);logs=r/'tester/logs';before={x:x.stat().st_size for x in logs.glob('*.log')}
subprocess.run([str(r/'terminal.exe'),'/portable',str(ini)],cwd=r,timeout=240,check=True)
rows=[]
for p in logs.glob('*.log'):
 with p.open('rb') as f:f.seek(before.get(p,0));rows.extend(x for x in f.read().decode(errors='replace').splitlines() if '[MHV-ORIGIN' in x)
assert len([x for x in rows if '-TF]' in x])==7,rows
assert len([x for x in rows if '-SUMMARY]' in x and 'orders=0 historyOrders=0 acceptance=NOT_PROMOTED' in x])==1,rows
files={}
for name in ['sig06_mhv_origin_inputs_v1_20261111.csv','sig06_mhv_origin_candidates_v1_20261111.csv']:
 p=r/'tester/files'/name;assert p.exists(),str(p);shutil.copyfile(p,e/name);files[name]={'sha256':sha(p),'bytes':p.stat().st_size}
after={p:sha(Path(p)) for p in inputs};assert after==inputs,'HST changed: inspect evidence'
candidate_path=e/'sig06_mhv_origin_candidates_v1_20261111.csv'
with candidate_path.open() as f:candidates=list(csv.DictReader(f,delimiter=';'))
manifest={'task':'SIG-06-MHV/origin-inventory','classification':'ENGINEERING_DIAGNOSTIC_NOT_SOURCE_EPOCH_ACCEPTANCE','source_sha256_lf':lf(source),'compile':result,'harness_sha256_lf':lf(h),'binary_sha256':sha(h.with_suffix('.ex4')),'history_hst_hashes_before_after_equal':True,'hst_hashes':inputs,'rows':rows,'csv_files':files,'candidates':candidates,'scenario_count':4,'scope':'At most600 existing closed bars per7TF; never crosses a non-nominal boundary; initial states are stress hypotheses, not authenticated history. M30 remains derived fixture. No price IO fixtures, download, HST rewrite or orders. Candidate convergence is diagnostic only, not proof of all possible valid historical states or session authenticity.'}
(e/'manifest.json').write_text(json.dumps(manifest,indent=2));print('\n'.join(rows),flush=True);print(json.dumps({'candidate_rows':len(candidates),'converged_candidates':sum(x['hypothesesConverged']=='1' for x in candidates),'files':files}),flush=True)
