from pathlib import Path
import json,hashlib,re,difflib,zipfile,base64,py_compile
r=Path(r'D:\BBMA\MT4_CustomMTF_302_Unit');repo=r/'mhv612-stage';e=r/'evidence/sig06_mhv';out=e/'fix612_final';assert not out.exists();out.mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();lf=lambda p:hashlib.sha256(p.read_text().encode()).hexdigest()
source=repo/'blueprint/source/BBMA_EA.mq4';expected='900744561bd5e5c5abaef754478a055fcf600bf178fe3174da2d484dd840f2e8';assert lf(source)==expected
state=json.loads((e/'fix612_regression/state.json').read_text());assert state['status']=='PASS' and len(state['completed'])==22,state
candidates={}
for kind in ['red','green','red_v2','green_v2']:
 p=e/('candidate612_'+kind);m=json.loads((p/'manifest.json').read_text());candidates[kind]=m
 assert '0 errors, 0 warnings' in m['compile'] and m['terminal_exit']==0
 assert lf(p/'BBMA_EA.mq4')==m['source_sha256_lf']
 harness=next(x for x in p.glob('*.mq4') if x.name!='BBMA_EA.mq4')
 assert lf(harness)==m['harness_sha256_lf'] and sha(harness.with_suffix('.ex4'))==m['binary_sha256']
assert (candidates['red']['passed'],candidates['red']['failed'])==(239,56)
assert (candidates['green']['passed'],candidates['green']['failed'])==(295,0)
assert (candidates['red_v2']['passed'],candidates['red_v2']['failed'])==(239,84)
assert (candidates['green_v2']['passed'],candidates['green_v2']['failed'])==(323,0)
assert candidates['green_v2']['source_sha256_lf']==expected
old=(r/'ext611-stage/blueprint/source/BBMA_EA.mq4').read_text();new=source.read_text()
def functions(s):
 masked=re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*.*?\*/',lambda m:re.sub(r'[^\n]',' ',m[0]),s,flags=re.S)
 result={}
 for m in re.finditer(r'^[A-Za-z_]\w*\s+([A-Za-z_]\w*)\([^;{}]*\)\s*\{',masked,re.M):
  a=masked.index('{',m.start());b=a;depth=1
  while depth:
   b+=1
   if masked[b]=='{':depth+=1
   if masked[b]=='}':depth-=1
  assert m[1] not in result,m[1]
  result[m[1]]=s[m.start():b+1]
 return result
before=functions(old);after=functions(new);changed=sorted(k for k in before if k in after and before[k]!=after[k]);added=sorted(set(after)-set(before));deleted=sorted(set(before)-set(after))
assert changed==['TryAdvanceMHVSupersessionCandidate','UpdateCanonicalMLVState'] and added==['ClearMHVSupersessionCandidate'] and not deleted,(changed,added,deleted)
assert new.splitlines()[2].startswith('//| Version 6.1.2')
(out/'production.diff').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='6.11',tofile='6.12')))
groups={};last_binaries={}
for kind in state['completed']:
 folder=('source_green' if kind=='source' else 'lifecycle' if kind=='lifecycle' else 'controller612_seeded' if kind=='controller_seeded' else 'controller612' if kind=='controller' else 'custom612_'+kind)
 p=e/'fix612_regression'/folder;m=json.loads((p/'manifest.json').read_text());groups[kind]=m
 actual=m.get('source_sha256_lf',m.get('source_sha256_lf_utf8'));assert actual==expected,(kind,actual)
 if kind in ['controller','controller_seeded']:
  assert m['candidate_monitor_parity'] and m['old_new_trace_row_counts_equal']
  assert m['baseline_source_sha256_lf']=='a62672ae1874fcbf61c671af01da09ef45ffe6972abd998ec70c5f9a74c238cb'
  for case,v in m['records'].items():
   q=Path(v['trace_path']);assert sha(q)==v['trace_sha256'] and v['counts']['attempts']==0
 else:
  if 'passed' in m:assert m['passed']
  assert all('FAIL' not in row for row in m['rows']),kind
 for name,v in m.get('compiled',{}).items():
  assert '0 errors, 0 warnings' in v['result']
  path=repo/'blueprint/source/BBMA_EA.mq4' if name=='BBMA_EA' else repo/'blueprint/tests/custom_mtf'/(name+'.mq4')
  assert lf(path)==v.get('source_sha256_lf_utf8',v.get('harness_sha256_lf'))
  last_binaries[str(path.with_suffix('.ex4'))]=v.get('ex4_sha256',v.get('binary_sha256'))
 for rel,digest in m.get('headers',{}).items():assert lf(repo/rel)==digest
 for rel,digest in m.get('test_headers',{}).items():assert lf(repo/rel)==digest
for path,digest in last_binaries.items():assert sha(Path(path))==digest,path
inventory=json.loads((e/'origin_inventory_v1/manifest.json').read_text())
for path,digest in inventory['hst_hashes'].items():assert sha(Path(path))==digest
for p in [r/'run_mhv_candidate612_v2.py',r/'run_mhv612_regression.py',repo/'blueprint/tests/custom_mtf/run_controller_parity_native.py']:py_compile.compile(str(p),doraise=True)
summary={'task':'SIG-06-MHV','bug_status':'BOUNDED_FIX_VERIFIED','full_signal_status':'PARTIAL_HISTORICAL_SESSION_EPOCH_RECOVERY_HOLD','source_sha256_lf':expected,'build':'6.12','revision':'MHV_CANDIDATE_INVALIDATION_001_20261111','changed_functions':changed,'added_functions':added,'native_candidate_assertions':323,'initial_RED':{'passed':239,'failed':56},'expanded_RED':{'passed':239,'failed':84},'native_groups_completed':state['completed'],'native_group_count':len(groups),'HST_hashes_unchanged':True,'final_binary_bindings':last_binaries,'candidates':candidates,'regression':groups,'cloud':'6 available test functions and import assertions PASS on exact900744 source; pytest module unavailable on cloud/G40; no full repository pytest claim','remaining':'Accepted same-feed production historical sessions/boundary and source-proven epoch, then successful production recovery parity; no next signal or availability promotion'}
(out/'summary.json').write_text(json.dumps(summary,indent=2))
archive=out/'evidence.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 z.write(out/'summary.json','summary.json');z.write(out/'production.diff','production.diff')
 for folder in ['candidate612_red','candidate612_green','candidate612_red_v2','candidate612_green_v2','fix612_regression']:
  for p in sorted((e/folder).rglob('*')):
   if p.is_file() and p.suffix in ['.json','.log','.ini','.txt'] and not p.name.endswith('.base64'):z.write(p,str(p.relative_to(e)).replace(chr(92),'/'))
 data=Path(__file__);z.write(data,'collect_mhv612.py')
encoded=base64.b64encode(archive.read_bytes()).decode()
for i in range((len(encoded)+79999)//80000):(out/('part'+str(i)+'.b64')).write_text(encoded[i*80000:(i+1)*80000])
meta={'sha256':sha(archive),'bytes':archive.stat().st_size,'base64_chars':len(encoded),'parts':(len(encoded)+79999)//80000,'verified':True}
(out/'archive.json').write_text(json.dumps(meta,indent=2))
print(json.dumps({'verified':True,'candidate_assertions':323,'groups':len(groups),'changed_functions':changed,'binary_bindings':len(last_binaries),'archive':meta,'controller_differences':{k:groups[k]['old_new_difference_count'] for k in ['controller','controller_seeded']}}),flush=True)
