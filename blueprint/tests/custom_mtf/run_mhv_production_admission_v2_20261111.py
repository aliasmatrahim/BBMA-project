from pathlib import Path
import json,hashlib,subprocess,shutil,re,zipfile,base64
r=Path(r'D:\BBMA\MT4_CustomMTF_302_Unit');repo=r/'ext611-stage';e=r/'evidence/sig06_mhv/production_admission_v2_20261111'
assert not e.exists();e.mkdir(parents=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lf=lambda p:hashlib.sha256(p.read_text().encode()).hexdigest()
# Existing registry is mandatory; no data download or new historical derivation.
index=Path(r'D:\MARKET_DATA_INDEX.json');json.loads(index.read_text(encoding='utf-8-sig'))
source=repo/'blueprint/source/BBMA_EA.mq4';assert lf(source)=='a62672ae1874fcbf61c671af01da09ef45ffe6972abd998ec70c5f9a74c238cb'
prior=json.loads((r/'evidence/sig06_mhv/origin_ny_calendar_v7/manifest.json').read_text());hst=prior['hst_hashes']
assert all(sha(Path(p))==digest for p,digest in hst.items())
snapshots={}
for tf in ['240','1440']:
 p=r/('tester/files/sig06_mhv_origin_checkpoint_ny_calendar_v7_'+tf+'.csv')
 assert sha(p)==prior['cases'][tf]['snapshot_sha256'];snapshots[str(p)]=sha(p)
h=repo/'blueprint/tests/custom_mtf/CustomMHVProductionAdmissionHarness.mq4';log=e/'compile.log'
subprocess.run([str(r/'metaeditor.exe'),'/compile:'+str(h),'/log:'+str(log)],timeout=60)
result=next(x for x in log.read_bytes().decode('utf-16').splitlines() if 'Result:' in x)
assert '0 errors, 0 warnings' in result,result
shutil.copyfile(h.with_suffix('.ex4'),r/'MQL4/Experts'/h.with_suffix('.ex4').name)
cfg=(r/'config/parser_green.ini').read_text().replace('CustomFormulaHarness',h.stem).replace('parser_green.html','mhv_production_admission_v2_20261111.html')
assert 'ExpertsTrades=false' in cfg
ini=e/'test.ini';ini.write_text(cfg);logs=r/'tester/logs';before={x:x.stat().st_size for x in logs.glob('*.log')}
proc=subprocess.Popen([str(r/'terminal.exe'),'/portable',str(ini)],cwd=r);pid=proc.pid;code=proc.wait(timeout=120);assert code==0,code
rows=[]
for p in logs.glob('*.log'):
 with p.open('rb') as f:f.seek(before.get(p,0));rows.extend(x for x in f.read().decode(errors='replace').splitlines() if '[MHV-ADMISSION' in x)
(e/'native_rows.json').write_text(json.dumps(rows,indent=2))
summaries=[x for x in rows if '[MHV-ADMISSION-SUMMARY]' in x];assert len(summaries)==1,summaries
match=re.search(r'cases=(\d+) passed=(\d+) failed=(\d+)',summaries[0]);assert match and match[1]=='24' and match[3]=='0',summaries
assert len([x for x in rows if '[MHV-ADMISSION-CASE]' in x])==24
assert all(sha(Path(p))==digest for p,digest in hst.items())
assert all(sha(Path(p))==digest for p,digest in snapshots.items())
manifest={'task':'SIG-06-MHV','classification':'ACTUAL_PRODUCTION_GAP_FAIL_FROZEN_PASS_NOT_RECOVERY_ACCEPTANCE','source_sha256_lf':lf(source),'compile':result,'harness_sha256_lf':lf(h),'binary_sha256':sha(h.with_suffix('.ex4')),'equality_sha256_lf':lf(repo/'blueprint/tests/custom_mtf/CustomOwnerTestEquality.mqh'),'codec_sha256_lf':lf(repo/'blueprint/tests/custom_mtf/CustomMHVOriginCodec.mqh'),'market_index_sha256':sha(index),'terminal_pid':pid,'terminal_exit':code,'cases':24,'boundaries':6,'native_assertions':int(match[2]),'failed':0,'hst_hashes_before_after_equal':True,'hst_hashes':hst,'snapshot_hashes_unchanged':snapshots,'rows':rows,'scope':'Real production ReplayCustomAuxOwnerSource, RefreshCustomRequestedOwners/canonical store and both MHV views; exact existing H4/D1 engine snapshots. Zero- and two-bar staged prefixes. Expected rejection and full structural/data rollback, initially held and previously unheld owners. Router catch-up targets current latest closed candle, not the historical gap. No new trusted epoch, broker-session or successful gap recovery claim.'}
(e/'manifest.json').write_text(json.dumps(manifest,indent=2))
archive=e/'evidence.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for name in ['manifest.json','native_rows.json','compile.log','test.ini']:z.write(e/name,name)
 z.write(h,h.name);z.write(Path(__file__),Path(__file__).name)
 for q in sorted((r/'evidence/sig06_mhv/production_admission_v1_20261111').glob('*')):
  if q.is_file():z.write(q,'initial_invalid_router_target/'+q.name)
(e/'evidence.base64').write_text(base64.b64encode(archive.read_bytes()).decode())
(e/'archive.json').write_text(json.dumps({'sha256':sha(archive),'bytes':archive.stat().st_size},indent=2))
print(json.dumps({'verified':True,'cases':24,'assertions':int(match[2]),'terminal_pid':pid,'exit':code,'compile':result,'source_unchanged':True,'archive_sha256':sha(archive)}),flush=True)
