from pathlib import Path
import json,subprocess,hashlib,sys
r=Path(r'D:\BBMA\MT4_CustomMTF_302_Unit');repo=r/'mhv613-stage';e=r/'evidence/sig06_mhv/fix613_regression';e.mkdir(parents=True,exist_ok=True)
sha=hashlib.sha256((repo/'blueprint/source/BBMA_EA.mq4').read_text().encode()).hexdigest()
assert sha=='43470ff9795b18e44844bb815deceee778072a004b8815666e18e8ffa584d15c'
for folder,want in [('availability613_green',295),('status613_green',785)]:
 m=json.loads((e.parent/folder/'manifest.json').read_text());assert m['source_sha256_lf']==sha and m['passed']==want and m['failed']==0
sp=e/'state.json'
state=json.loads(sp.read_text());assert state['status']=='FAILED' and state['failed']=='momready' and state['completed']==['candidate'] and state['source_sha256_lf']==sha
(e/'state_initial_failure.json').write_text(json.dumps(state));state.pop('failed');state['status']='RUNNING'
for kind in ['momready','mhvtf','m09producer','m09replay','canonmhv','observerm09','producer','recovery','higher','flow','prefreeze','controller','controller_seeded']:
 state['running']=kind;sp.write_text(json.dumps(state));print('BEGIN613',kind,flush=True)
 if kind=='candidate':args=['python',str(r/'run_mhv_candidate613.py'),'green_v2']
 elif kind.startswith('controller'):
  args=['python',str(repo/'blueprint/tests/custom_mtf/run_controller_parity_native.py'),'--root',str(r),'--repo',str(repo),'--evidence-root',str(e),'--expected-source-sha',sha,'--baseline-build','612']
  if kind.endswith('seeded'):args.append('--seeded')
 else:args=['python',str(repo/'blueprint/tests/custom_mtf/run_clock_owner_native.py'),'--root',str(r),'--repo',str(repo),'--evidence-root',str(e/'canonical_fixture_retry' if kind=='momready' else e),'--kind',kind]
 log=e/((kind+'_canonical_fixture_retry' if kind=='momready' else kind)+'.log')
 with log.open('w',encoding='utf-8') as out:rc=subprocess.run(args,stdout=out,stderr=subprocess.STDOUT).returncode
 if rc:
  state['status']='FAILED';state['failed']=kind;sp.write_text(json.dumps(state));print(log.read_text()[-6000:],flush=True);sys.exit(rc)
 state['completed'].append(kind);sp.write_text(json.dumps(state));print('PASS613',kind,flush=True)
state['status']='PASS';state['running']=None;sp.write_text(json.dumps(state));print('MHV613_REGRESSION_PASS',flush=True)
