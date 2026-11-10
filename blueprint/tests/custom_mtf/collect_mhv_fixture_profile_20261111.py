from pathlib import Path
import json,hashlib,csv,zipfile,base64,py_compile
r=Path(r'D:\BBMA\MT4_CustomMTF_302_Unit'); repo=r/'ext611-stage';e=r/'evidence/sig06_mhv'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lf=lambda p:hashlib.sha256(p.read_text().encode()).hexdigest()
m=json.loads((e/'origin_ny_calendar_v7/manifest.json').read_text())
b=json.loads((e/'source_profile_binding_20261111/manifest.json').read_text())
old=json.loads((e/'m30_fixture_restart_summary_v5.json').read_text())
assert lf(repo/'blueprint/source/BBMA_EA.mq4')==m['source_sha256_lf']==old['source_sha256_lf']=='a62672ae1874fcbf61c671af01da09ef45ffe6972abd998ec70c5f9a74c238cb'
h=repo/'blueprint/tests/custom_mtf/CustomMHVNYFixtureCalendarReplayHarness.mq4'
assert lf(h)==m['harness_sha256_lf'] and sha(h.with_suffix('.ex4'))==m['binary_sha256']
assert lf(repo/'blueprint/tests/custom_mtf/CustomMHVOriginCodec.mqh')==m['codec_sha256_lf']
assert lf(repo/'blueprint/tests/custom_mtf/CustomOwnerTestEquality.mqh')==m['equality_header_sha256_lf']
assert '0 errors, 0 warnings' in m['compile']
assert b['profile_sha256']==m['calendar_policy']['profile_sha256'] and b['v3_manifest_sha256']==m['calendar_policy']['v3_manifest_sha256']
assert b['profile']['deploymentBrokerCanonical'] is False and b['profile']['canonicalStrategyRule'] is False
assert len(b['files'])==6 and all(x['source_tail_records_equal'] and x['source_header_equal'] for x in b['files'])
for path,digest in m['hst_hashes'].items(): assert sha(Path(path))==digest
pids=[];bridges=[]
for tf in ['240','1440']:
 c=m['cases'][tf];assert c['status']=='BOUNDED_PASS'
 for mode,n in [('produce',7),('consume',29)]:
  x=c['records'][mode];pids.append(x['terminal_pid'])
  assert x['terminal_exit']==0 and any('mode='+mode+' checks='+str(n)+' failed=0 ok=true' in row for row in x['rows'])
  assert any('no_broker_orders PASS' in row for row in x['rows'])
  assert x['reference_calendar_bridges'] and all(v['observed_M15_bars_skipped']==0 for v in x['reference_calendar_bridges'])
  bridges.extend(x['reference_calendar_bridges'])
 q=e/'origin_ny_calendar_v7'/('sig06_mhv_origin_checkpoint_ny_calendar_v7_'+tf+'.csv')
 assert sha(q)==c['snapshot_sha256']==c['records']['produce']['snapshot_sha256']==c['records']['consume']['snapshot_sha256']
 with q.open() as f: kv=list(csv.reader(f,delimiter=';'))
 assert len(kv)==2553 and len({v[0] for v in kv})==2553
 for step in ['anchor']+['step'+str(i) for i in range(1,25)]: assert sum(v[0].startswith(step+'.') for v in kv)==102
assert len(set(pids))==4
for name in ['run_mhv_ny_calendar_v7.py','run_mhv_m30_m15_v5.py','audit_m30_derivation_20261111.py','bind_hst_to_synthetic_profile_20261111.py']: py_compile.compile(str(r/name),doraise=True)
summary={'task':'SIG-06-MHV','status':'PARTIAL_FULL_ACCEPTANCE_HOLD','production_source_changed':False,'source_sha256_lf':m['source_sha256_lf'],'new_native_restart_assertions':106,'new_post_reload_bars':72,'reused_assertions':136,'combined_assertions':242,'combined_post_reload_bars':168,'fields_per_state':102,'all_seven_TF_bounded_proofs':True,'M30_adapter_MA_comparisons':200,'new_terminal_processes':6,'source_provenance':'M15/H1/H4/D1 exact synthetic v3 SHA; M1/M5 exact suffix payload plus identical header. M30 fixture derived from complete M15 pairs. No broker-session authentication.','source_binding':b,'NY_calendar_native':m,'prior_M30_summary':'m30_fixture_restart_summary_v5.json','review':'No material M30 adapter issue. NY test calls actual source engines directly; does not exercise production replay continuity admission. Original historical origin/session and T04B remain HOLD.','remaining':['Accepted same-feed historical session/boundary authority for production recovery','Source-proven owner epoch beyond four bounded stress hypotheses','Production replay admission and continuous/recovered parity across accepted non-nominal boundary'],'next':'Remain SIG06. Do not start MLV/Re-Entry, weaken recovery admission, or promote custom availability.','auto_entry':False,'all77_semantic_availability':False}
(e/'mhv611_fixture_profile_summary_20261111.json').write_text(json.dumps(summary,indent=2))
archive=e/'mhv611_fixture_profile_evidence_20261111.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for folder in ['m30_derivation_audit_20261111','origin_m30_m15_v5','hst_origin_candidates_20261111','source_profile_binding_20261111','origin_ny_calendar_v6','origin_ny_calendar_v7']:
  for q in sorted((e/folder).glob('*')):
   if q.is_file():z.write(q,str(q.relative_to(e)).replace(chr(92),'/'))
 for name in ['m30_fixture_restart_summary_v5.json','mhv611_fixture_profile_summary_20261111.json']:z.write(e/name,name)
 for name in ['run_mhv_ny_calendar_v7.py','run_mhv_m30_m15_v5.py','audit_m30_derivation_20261111.py','bind_hst_to_synthetic_profile_20261111.py']: z.write(r/name,'drivers/'+name)
 for name in ['CustomMHVNYFixtureCalendarReplayHarness.mq4','CustomMHVM30DerivedReplayHarness.mq4','CustomM30FromM15Fixture.mqh']: z.write(repo/'blueprint/tests/custom_mtf'/name,'harness/'+name)
(e/'mhv611_fixture_profile_evidence_20261111.base64').write_text(base64.b64encode(archive.read_bytes()).decode())
(e/'mhv611_fixture_profile_archive_20261111.json').write_text(json.dumps({'sha256':sha(archive),'bytes':archive.stat().st_size,'verified':True},indent=2))
print(json.dumps({'verified':True,'new_assertions':106,'combined_assertions':242,'post_reload_bars':168,'source_unchanged':True,'NY_terminal_pids':pids,'boundary_observations':len(bridges),'archive_bytes':archive.stat().st_size}),flush=True)
