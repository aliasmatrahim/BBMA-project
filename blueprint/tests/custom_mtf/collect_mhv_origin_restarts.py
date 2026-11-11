from pathlib import Path
import json,hashlib,csv,re,zipfile,base64,datetime
r=Path(r'D:\BBMA\MT4_CustomMTF_302_Unit');repo=r/'ext611-stage';root=r/'evidence/sig06_mhv'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();lf=lambda p:hashlib.sha256(p.read_text().encode()).hexdigest()
source=repo/'blueprint/source/BBMA_EA.mq4';assert lf(source)=='a62672ae1874fcbf61c671af01da09ef45ffe6972abd998ec70c5f9a74c238cb'
inv=json.loads((root/'origin_inventory_v1/manifest.json').read_text());one=json.loads((root/'origin_replay_v3/manifest.json').read_text());multi=json.loads((root/'origin_multi_v4/manifest.json').read_text())
test=repo/'blueprint/tests/custom_mtf';bound={}
for m,name in [(inv,'CustomMHVOriginInventoryHarness'),(one,'CustomMHVOriginReplayHarness'),(multi,'CustomMHVOriginMultiReplayHarness')]:
 p=test/(name+'.mq4');assert lf(p)==m['harness_sha256_lf'] and sha(p.with_suffix('.ex4'))==m['binary_sha256'] and '0 errors, 0 warnings' in m['compile'];assert m['source_sha256_lf']==lf(source)
 bound[name]={'harness_sha256_lf':lf(p),'binary_sha256':sha(p.with_suffix('.ex4')),'compile':m['compile']}
for m in [one,multi]:
 assert lf(test/'CustomMHVOriginCodec.mqh')==m['codec_sha256_lf'] and lf(test/'CustomOwnerTestEquality.mqh')==m['equality_header_sha256_lf']
for p,h in inv['hst_hashes'].items():assert sha(Path(p))==h
cases={'15':{'records':one['records'],'anchor_chart_epoch':one['anchor_chart_epoch'],'status':'BOUNDED_PASS','snapshot':'origin_replay_v3/sig06_mhv_origin_checkpoint_v3_20261111.csv'}}
for tf,c in multi['cases'].items():
 assert c['status']=='BOUNDED_PASS',(tf,c['status'])
 cases[tf]={**c,'snapshot':'origin_multi_v4/sig06_mhv_origin_checkpoint_multi_v4_'+tf+'.csv'}
pids=set();steps=0
for tf,c in cases.items():
 for mode,rec in c['records'].items():
  expected=6 if mode=='produce' else 28
  assert any('mode='+mode+' checks='+str(expected)+' failed=0 ok=true' in row for row in rec['rows'])
  assert any('no_broker_orders PASS' in row for row in rec['rows'])
  assert rec['terminal_exit']==0;pids.add(rec['terminal_pid'])
 p=root/c['snapshot'];assert sha(p)==c['records']['produce']['snapshot_sha256']==c['records']['consume']['snapshot_sha256']
 with p.open() as f:rows=list(csv.reader(f,delimiter=';'))
 assert len(rows)==2553 and len({x[0] for x in rows})==2553,(tf,len(rows))
 for step in ['anchor']+['step'+str(x) for x in range(1,25)]:assert sum(x[0].startswith(step+'.') for x in rows)==102,(tf,step)
 c['snapshot_sha256']=sha(p);c['snapshot_rows']=len(rows);c['steps']=24;steps+=24
assert len(pids)==8
data=root/'origin_inventory_v1/sig06_mhv_origin_inputs_v1_20261111.csv'
assert sha(data)==inv['csv_files'][data.name]['sha256']
with data.open() as f:inputs=list(csv.DictReader(f,delimiter=';'))
assert len(inputs)==4200
boundaries={str(tf):[] for tf in [30,240,1440]};previous={}
for x in inputs:
 tf=x['tf'];time=int(x['time'])
 if tf in boundaries and tf in previous and x['gapReset']=='1' and len(boundaries[tf])<3:
  a=previous[tf];boundaries[tf].append({'previous_chart_epoch':a,'next_chart_epoch':time,'previous_chart_label':datetime.datetime.fromtimestamp(a,datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'),'next_chart_label':datetime.datetime.fromtimestamp(time,datetime.timezone.utc).strftime('%Y-%m-%d %H:%M'),'elapsed_seconds':time-a,'unobserved_nominal_bars':(time-a)//(int(tf)*60)-1,'classification':'UNAUTHENTICATED_BOUNDARY_NOT_ASSUMED_CLOSURE_OR_FILLED_BARS'})
 previous[tf]=time
red=json.loads((root/'origin_replay_v2/partial.json').read_text())
summary={'task':'SIG-06-MHV','status':'PARTIAL_BOUNDED_NATURAL_HISTORY_RESTART_PASS_SESSION_GLOBAL_ORIGIN_HOLD','source_sha256_lf':lf(source),'inventory_ready_bars':4200,'inventory_candidate_chains':57,'inventory_converged_candidates':23,'cases':cases,'source_bars_compared_after_reload':steps,'fields_per_state':102,'native_assertions':136,'distinct_terminal_processes':len(pids),'bindings':bound,'codec_sha256_lf':lf(test/'CustomMHVOriginCodec.mqh'),'hst_hashes_before_after_equal':True,'hst_hashes':inv['hst_hashes'],'remaining_boundary_examples':boundaries,'limits':'Four initial-state hypotheses do not exhaust all possible valid histories. No session/UTC authentication, no D1/H4/M30 origin acceptance, no custom executable availability. Prior SIG01-05 bounded acceptance unchanged.'}
(root/'natural_origin_restart_summary.json').write_text(json.dumps(summary,indent=2))
archive=root/'natural_origin_restart_evidence.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for folder in ['origin_inventory_v1','origin_replay_v3','origin_multi_v4']:
  for p in sorted((root/folder).glob('*')):
   if p.suffix.lower() in ['.csv','.json']:z.write(p,str(p.relative_to(root)).replace(chr(92),'/'))
 for name in ['partial.json','failed_bindings.json','CustomMHVOriginReplayHarness.mq4']:
  p=root/'origin_replay_v2'/name;assert p.exists();z.write(p,str(p.relative_to(root)).replace(chr(92),'/'))
 z.write(root/'natural_origin_restart_summary.json','natural_origin_restart_summary.json')
(root/'natural_origin_restart_evidence.base64').write_text(base64.b64encode(archive.read_bytes()).decode())
(root/'natural_origin_restart_archive.json').write_text(json.dumps({'sha256':sha(archive),'bytes':archive.stat().st_size,'base64_chars':len(base64.b64encode(archive.read_bytes()))},indent=2))
print(json.dumps({'verified':True,'cases':list(cases),'native_assertions':136,'replayed_source_bars':steps,'terminal_processes':len(pids),'archive_bytes':archive.stat().st_size,'remaining_boundaries':boundaries}),flush=True)
