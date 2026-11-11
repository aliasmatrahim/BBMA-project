from pathlib import Path
import json,hashlib,subprocess,shutil
r=Path(r'D:\BBMA\MT4_CustomMTF_302_Unit');repo=r/'ext611-stage';e=r/'evidence/sig06_mhv/origin_replay_v3';assert not e.exists();e.mkdir(parents=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();lf=lambda p:hashlib.sha256(p.read_text().encode()).hexdigest()
source=repo/'blueprint/source/BBMA_EA.mq4';assert lf(source)=='a62672ae1874fcbf61c671af01da09ef45ffe6972abd998ec70c5f9a74c238cb'
inventory=json.loads((r/'evidence/sig06_mhv/origin_inventory_v1/manifest.json').read_text());hst=inventory['hst_hashes'];assert all(sha(Path(p))==v for p,v in hst.items())
h=repo/'blueprint/tests/custom_mtf/CustomMHVOriginReplayHarness.mq4';log=e/'compile.log'
subprocess.run([str(r/'metaeditor.exe'),'/compile:'+str(h),'/log:'+str(log)],timeout=60)
result=next(x for x in log.read_bytes().decode('utf-16').splitlines() if 'Result:' in x);assert '0 errors, 0 warnings' in result,result
shutil.copyfile(h.with_suffix('.ex4'),r/'MQL4/Experts'/h.with_suffix('.ex4').name)
records={};snapshot=r/'tester/files/sig06_mhv_origin_checkpoint_v3_20261111.csv';assert not snapshot.exists()
for mode in ['produce','consume']:
 preset=r/'tester'/('origin_v3_'+mode+'.set');preset.write_text('OriginReplayConsumer='+('true' if mode=='consume' else 'false')+'\n')
 cfg=(r/'config/parser_green.ini').read_text().replace('CustomFormulaHarness',h.stem).replace('parser_green.html','mhv_origin_v3_'+mode+'.html')+'\nTestExpertParameters='+preset.name+'\n'
 assert 'ExpertsTrades=false' in cfg
 ini=e/(mode+'.ini');ini.write_text(cfg);logs=r/'tester/logs';before={x:x.stat().st_size for x in logs.glob('*.log')}
 proc=subprocess.Popen([str(r/'terminal.exe'),'/portable',str(ini)],cwd=r);pid=proc.pid;code=proc.wait(timeout=120);assert code==0,code
 rows=[]
 for p in logs.glob('*.log'):
  with p.open('rb') as f:f.seek(before.get(p,0));rows.extend(x for x in f.read().decode(errors='replace').splitlines() if '[MHV-RESTART' in x)
 records[mode]={'terminal_pid':pid,'terminal_exit':code,'rows':rows}
 (e/'partial.json').write_text(json.dumps({'compile':result,'records':records},indent=2))
 assert any('mode='+mode in x and 'failed=0 ok=true acceptance=BOUNDED_ENGINEERING_ONLY' in x for x in rows),rows
 assert snapshot.exists();records[mode]['snapshot_sha256']=sha(snapshot)
 print(json.dumps({'mode':mode,'terminal_pid':pid,'summary':rows[-1],'snapshot_sha256':sha(snapshot)}),flush=True)
assert records['produce']['terminal_pid']!=records['consume']['terminal_pid']
assert records['produce']['snapshot_sha256']==records['consume']['snapshot_sha256']
assert all(sha(Path(p))==v for p,v in hst.items());shutil.copyfile(snapshot,e/snapshot.name)
manifest={'classification':'BOUNDED_M15_NATIVE_NATURAL_HISTORY_RESTART_CANDIDATE_NOT_GLOBAL_EPOCH_ACCEPTANCE','source_sha256_lf':lf(source),'compile':result,'harness_sha256_lf':lf(h),'binary_sha256':sha(h.with_suffix('.ex4')),'codec_sha256_lf':lf(repo/'blueprint/tests/custom_mtf/CustomMHVOriginCodec.mqh'),'equality_header_sha256_lf':lf(repo/'blueprint/tests/custom_mtf/CustomOwnerTestEquality.mqh'),'hst_hashes_before_after_equal':True,'hst_hashes':hst,'anchor_chart_epoch':1784912400,'timeframe':15,'steps_after_anchor':24,'records':records,'snapshot_sha256':sha(snapshot),'snapshot_bytes':snapshot.stat().st_size,'scope':'Four stress hypotheses converge on actual native history; M08/M09 source origins after the first source Momentum reset are asserted. Two separate terminal process starts serialize/reload all102 owner fields and compare24 consecutive source bars against uninterrupted control. No platform price fixture, artificial trusted parent, primary-terminal restart or orders. Sessions/UTC and universal unknown-state reconstruction remain unverified.'}
(e/'manifest.json').write_text(json.dumps(manifest,indent=2));print('NATURAL_HISTORY_M15_RESTART_BOUNDED_PASS',flush=True)
