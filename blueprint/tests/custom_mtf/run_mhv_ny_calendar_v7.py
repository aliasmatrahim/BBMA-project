from pathlib import Path
import json,hashlib,subprocess,shutil,re,struct,bisect,datetime
r=Path(r'D:\BBMA\MT4_CustomMTF_302_Unit');repo=r/'ext611-stage';e=r/'evidence/sig06_mhv/origin_ny_calendar_v7';assert not e.exists();e.mkdir(parents=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();lf=lambda p:hashlib.sha256(p.read_text().encode()).hexdigest()
source=repo/'blueprint/source/BBMA_EA.mq4';assert lf(source)=='a62672ae1874fcbf61c671af01da09ef45ffe6972abd998ec70c5f9a74c238cb'
inventory=json.loads((r/'evidence/sig06_mhv/origin_inventory_v1/manifest.json').read_text());hst=inventory['hst_hashes'];assert all(sha(Path(p))==v for p,v in hst.items())
dataset=Path(r'D:\BBMA\HistoricalData')
profile_path=dataset/'profiles/synthetic_ny_close_test_profile.json';profile=json.loads(profile_path.read_text(encoding='utf-8-sig'))
manifest_path=dataset/'exports/mt4/synthetic_ny_close_v3/MANIFEST.json';origin=json.loads(manifest_path.read_text(encoding='utf-8-sig'))
assert profile['status']=='APPROVED_FOR_ISOLATED_TESTER_REFERENCE_ONLY' and profile['deploymentBrokerCanonical'] is False and profile['canonicalStrategyRule'] is False
assert origin['profile']==profile['profileId']=='BBMA_SYNTHETIC_NY_CLOSE_TEST_V1'
gbp={int(x['period']):x for x in origin['files'] if x['pair']=='GBPUSD'}
for tf in [15,60,240,1440]:assert gbp[tf]['sha256']==hst[str(r/'history/MetaQuotes-Demo'/('GBPUSD'+str(tf)+'.hst'))]
fmt=struct.Struct('<qddddqiq');raw=(r/'history/MetaQuotes-Demo/GBPUSD15.hst').read_bytes();m15times=[x[0] for x in fmt.iter_unpack(raw[148:])]
policy={'profile_id':profile['profileId'],'profile_sha256':sha(profile_path),'v3_manifest_sha256':sha(manifest_path),'classification':'APPROVED_SYNTHETIC_REFERENCE_CALENDAR_ONLY_NOT_HISTORICAL_BROKER_SESSIONS','source_clock_mapping':profile['syntheticServerMapping'],'weekend_rule':'Only nominally adjacent bars or a sequence of Saturday/Sunday synthetic-wall-clock slots; any weekday omission is rejected','invariant':'No existing M15 source bar may lie inside an admitted weekend interval'}

h=repo/'blueprint/tests/custom_mtf/CustomMHVNYFixtureCalendarReplayHarness.mq4';log=e/'compile.log'
subprocess.run([str(r/'metaeditor.exe'),'/compile:'+str(h),'/log:'+str(log)],timeout=60)
result=next(x for x in log.read_bytes().decode('utf-16').splitlines() if 'Result:' in x);assert '0 errors, 0 warnings' in result,result
shutil.copyfile(h.with_suffix('.ex4'),r/'MQL4/Experts'/h.with_suffix('.ex4').name)
records={}
for tf in [240,1440]:
 records[str(tf)]={'status':'RUNNING','records':{}};case=records[str(tf)];snapshot=r/('tester/files/sig06_mhv_origin_checkpoint_ny_calendar_v7_'+str(tf)+'.csv');assert not snapshot.exists()
 anchor=0;buy=True
 for mode in ['produce','consume']:
  preset=r/'tester'/('origin_ny_calendar_v7_'+str(tf)+'_'+mode+'.set');preset.write_text('OriginReplayConsumer='+('true' if mode=='consume' else 'false')+'\nOriginSourceTF='+str(tf)+'\nOriginCandidateEpoch='+str(anchor)+'\nOriginCandidateIsBuy='+('true' if buy else 'false')+'\n')
  cfg=(r/'config/parser_green.ini').read_text().replace('CustomFormulaHarness',h.stem).replace('parser_green.html','mhv_ny_calendar_v7_'+str(tf)+'_'+mode+'.html')+'\nTestExpertParameters='+preset.name+'\n';assert 'ExpertsTrades=false' in cfg
  ini=e/(str(tf)+'_'+mode+'.ini');ini.write_text(cfg);logs=r/'tester/logs';before={x:x.stat().st_size for x in logs.glob('*.log')}
  proc=subprocess.Popen([str(r/'terminal.exe'),'/portable',str(ini)],cwd=r);pid=proc.pid;code=proc.wait(timeout=120);assert code==0,code
  rows=[]
  for p in logs.glob('*.log'):
   with p.open('rb') as f:f.seek(before.get(p,0));rows.extend(x for x in f.read().decode(errors='replace').splitlines() if '[MHV-RESTART' in x or '[MHV-NY-BRIDGE]' in x)
  case['records'][mode]={'terminal_pid':pid,'terminal_exit':code,'rows':rows};(e/'partial.json').write_text(json.dumps(records,indent=2))
  if mode=='produce':
   selects=[x for x in rows if '[MHV-RESTART-SELECT]' in x]
   if not selects:
    case['status']='NO_ELIGIBLE_ORIGIN_WITH_24_CONTIGUOUS_FUTURE_BARS';print(json.dumps({'tf':tf,'status':case['status'],'rows':rows[-2:]}),flush=True);break
   assert len(selects)==1,selects
   m=re.search(r'anchor=(\d+) buy=(true|false)',selects[0]);assert m,selects
   anchor=int(m[1]);buy=m[2]=='true';case['anchor_chart_epoch']=anchor;case['buy']=buy
  bridges=[]
  for row in rows:
   bm=re.search(r'\[MHV-NY-BRIDGE\] tf=(\d+) previous=(\d+) next=(\d+)',row)
   if not bm:continue
   prev,nxt=int(bm[2]),int(bm[3]);start=prev+tf*60
   assert bisect.bisect_left(m15times,nxt)==bisect.bisect_left(m15times,start),'Existing M15 quote bar would be skipped'
   assert all(datetime.datetime.fromtimestamp(t,datetime.timezone.utc).weekday()>=5 for t in range(start,nxt,tf*60))
   bridges.append({'previous_chart_epoch':prev,'next_chart_epoch':nxt,'omitted_fixture_slots':(nxt-prev)//(tf*60)-1,'observed_M15_bars_skipped':0})
  assert bridges,'Required reference-calendar boundary not exercised';case['records'][mode]['reference_calendar_bridges']=bridges
  assert any('mode='+mode in x and 'failed=0 ok=true acceptance=BOUNDED_ENGINEERING_ONLY' in x for x in rows),rows[-15:]
  assert snapshot.exists();case['records'][mode]['snapshot_sha256']=sha(snapshot)
  print(json.dumps({'tf':tf,'mode':mode,'terminal_pid':pid,'anchor':anchor,'summary':rows[-1]}),flush=True)
 if 'consume' in case['records']:
  assert case['records']['produce']['terminal_pid']!=case['records']['consume']['terminal_pid']
  assert case['records']['produce']['snapshot_sha256']==case['records']['consume']['snapshot_sha256'];case['status']='BOUNDED_PASS';case['snapshot_sha256']=sha(snapshot);case['snapshot_bytes']=snapshot.stat().st_size;shutil.copyfile(snapshot,e/snapshot.name)
 (e/'partial.json').write_text(json.dumps(records,indent=2))
assert all(sha(Path(p))==v for p,v in hst.items())
manifest={'classification':'BOUNDED_H4_D1_SYNTHETIC_PROFILE_CALENDAR_RESTART_NOT_BROKER_ACCEPTANCE','calendar_policy':policy,'source_sha256_lf':lf(source),'compile':result,'harness_sha256_lf':lf(h),'binary_sha256':sha(h.with_suffix('.ex4')),'codec_sha256_lf':lf(repo/'blueprint/tests/custom_mtf/CustomMHVOriginCodec.mqh'),'equality_header_sha256_lf':lf(repo/'blueprint/tests/custom_mtf/CustomOwnerTestEquality.mqh'),'hst_hashes_before_after_equal':True,'hst_hashes':hst,'steps_after_anchor':24,'cases':records,'scope':'First actual-history origin satisfying unchanged strict witness and24 future contiguous bars in each selected TF. Four initial-state stress hypotheses, not universal historical-state proof. No orders or global availability promotion.'}
(e/'manifest.json').write_text(json.dumps(manifest,indent=2));print('NATURAL_HISTORY_MULTI_RESTART_DIAGNOSTIC_COMPLETE',flush=True)
