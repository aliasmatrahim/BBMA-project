from pathlib import Path
import json,hashlib,subprocess,shutil,re
r=Path(r'D:\BBMA\MT4_CustomMTF_302_Unit');repo=r/'ext611-stage';e=r/'evidence/sig06_mhv/origin_multi_v4';assert not e.exists();e.mkdir(parents=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();lf=lambda p:hashlib.sha256(p.read_text().encode()).hexdigest()
source=repo/'blueprint/source/BBMA_EA.mq4';assert lf(source)=='a62672ae1874fcbf61c671af01da09ef45ffe6972abd998ec70c5f9a74c238cb'
inventory=json.loads((r/'evidence/sig06_mhv/origin_inventory_v1/manifest.json').read_text());hst=inventory['hst_hashes'];assert all(sha(Path(p))==v for p,v in hst.items())
h=repo/'blueprint/tests/custom_mtf/CustomMHVOriginMultiReplayHarness.mq4';log=e/'compile.log'
subprocess.run([str(r/'metaeditor.exe'),'/compile:'+str(h),'/log:'+str(log)],timeout=60)
result=next(x for x in log.read_bytes().decode('utf-16').splitlines() if 'Result:' in x);assert '0 errors, 0 warnings' in result,result
shutil.copyfile(h.with_suffix('.ex4'),r/'MQL4/Experts'/h.with_suffix('.ex4').name)
records={}
for tf in [1,5,60]:
 records[str(tf)]={'status':'RUNNING','records':{}};case=records[str(tf)];snapshot=r/('tester/files/sig06_mhv_origin_checkpoint_multi_v4_'+str(tf)+'.csv');assert not snapshot.exists()
 anchor=0;buy=True
 for mode in ['produce','consume']:
  preset=r/'tester'/('origin_multi_v4_'+str(tf)+'_'+mode+'.set');preset.write_text('OriginReplayConsumer='+('true' if mode=='consume' else 'false')+'\nOriginSourceTF='+str(tf)+'\nOriginCandidateEpoch='+str(anchor)+'\nOriginCandidateIsBuy='+('true' if buy else 'false')+'\n')
  cfg=(r/'config/parser_green.ini').read_text().replace('CustomFormulaHarness',h.stem).replace('parser_green.html','mhv_multi_v4_'+str(tf)+'_'+mode+'.html')+'\nTestExpertParameters='+preset.name+'\n';assert 'ExpertsTrades=false' in cfg
  ini=e/(str(tf)+'_'+mode+'.ini');ini.write_text(cfg);logs=r/'tester/logs';before={x:x.stat().st_size for x in logs.glob('*.log')}
  proc=subprocess.Popen([str(r/'terminal.exe'),'/portable',str(ini)],cwd=r);pid=proc.pid;code=proc.wait(timeout=120);assert code==0,code
  rows=[]
  for p in logs.glob('*.log'):
   with p.open('rb') as f:f.seek(before.get(p,0));rows.extend(x for x in f.read().decode(errors='replace').splitlines() if '[MHV-RESTART' in x)
  case['records'][mode]={'terminal_pid':pid,'terminal_exit':code,'rows':rows};(e/'partial.json').write_text(json.dumps(records,indent=2))
  if mode=='produce':
   selects=[x for x in rows if '[MHV-RESTART-SELECT]' in x]
   if not selects:
    case['status']='NO_ELIGIBLE_ORIGIN_WITH_24_CONTIGUOUS_FUTURE_BARS';print(json.dumps({'tf':tf,'status':case['status'],'rows':rows[-2:]}),flush=True);break
   assert len(selects)==1,selects
   m=re.search(r'anchor=(\d+) buy=(true|false)',selects[0]);assert m,selects
   anchor=int(m[1]);buy=m[2]=='true';case['anchor_chart_epoch']=anchor;case['buy']=buy
  assert any('mode='+mode in x and 'failed=0 ok=true acceptance=BOUNDED_ENGINEERING_ONLY' in x for x in rows),rows[-15:]
  assert snapshot.exists();case['records'][mode]['snapshot_sha256']=sha(snapshot)
  print(json.dumps({'tf':tf,'mode':mode,'terminal_pid':pid,'anchor':anchor,'summary':rows[-1]}),flush=True)
 if 'consume' in case['records']:
  assert case['records']['produce']['terminal_pid']!=case['records']['consume']['terminal_pid']
  assert case['records']['produce']['snapshot_sha256']==case['records']['consume']['snapshot_sha256'];case['status']='BOUNDED_PASS';case['snapshot_sha256']=sha(snapshot);case['snapshot_bytes']=snapshot.stat().st_size;shutil.copyfile(snapshot,e/snapshot.name)
 (e/'partial.json').write_text(json.dumps(records,indent=2))
assert all(sha(Path(p))==v for p,v in hst.items())
manifest={'classification':'BOUNDED_NATIVE_NATURAL_HISTORY_RESTART_CANDIDATES_NOT_GLOBAL_EPOCH_ACCEPTANCE','source_sha256_lf':lf(source),'compile':result,'harness_sha256_lf':lf(h),'binary_sha256':sha(h.with_suffix('.ex4')),'codec_sha256_lf':lf(repo/'blueprint/tests/custom_mtf/CustomMHVOriginCodec.mqh'),'equality_header_sha256_lf':lf(repo/'blueprint/tests/custom_mtf/CustomOwnerTestEquality.mqh'),'hst_hashes_before_after_equal':True,'hst_hashes':hst,'steps_after_anchor':24,'cases':records,'scope':'First actual-history origin satisfying unchanged strict witness and24 future contiguous bars in each selected TF. Four initial-state stress hypotheses, not universal historical-state proof. No orders or global availability promotion.'}
(e/'manifest.json').write_text(json.dumps(manifest,indent=2));print('NATURAL_HISTORY_MULTI_RESTART_DIAGNOSTIC_COMPLETE',flush=True)
