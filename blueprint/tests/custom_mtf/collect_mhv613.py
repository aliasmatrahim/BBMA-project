from pathlib import Path
import json,hashlib,tarfile,io,base64,py_compile
r=Path(r'D:\BBMA\MT4_CustomMTF_302_Unit');repo=r/'mhv613-stage';e=r/'evidence/sig06_mhv';reg=e/'fix613_regression';o=e/'fix613_final'
sha=lambda b:hashlib.sha256(b).hexdigest()
lf=lambda p:sha(p.read_text().encode())
expected='43470ff9795b18e44844bb815deceee778072a004b8815666e18e8ffa584d15c'
base='900744561bd5e5c5abaef754478a055fcf600bf178fe3174da2d484dd840f2e8'
source=repo/'blueprint/source/BBMA_EA.mq4';assert lf(source)==expected
assert lf(r/'mhv612-stage/blueprint/source/BBMA_EA.mq4')==base
state=json.loads((reg/'state.json').read_text());assert state['status']=='PASS' and len(state['completed'])==14 and state['source_sha256_lf']==expected,state
payload={};aliases={}
def include(p,logical):
 b=p.read_bytes();k=sha(b);payload[k]=b;aliases[logical]=k
def unit(folder,passed,failed,source_hash):
 p=e/folder;m=json.loads((p/'manifest.json').read_text())
 assert (m['passed'],m['failed'])==(passed,failed) and m['source_sha256_lf']==source_hash and m['terminal_exit']==0 and '0 errors, 0 warnings' in m['compile'],folder
 assert lf(p/'BBMA_EA.mq4')==source_hash
 h=next(x for x in p.glob('*.mq4') if x.name!='BBMA_EA.mq4')
 assert lf(h)==m['harness_sha256_lf'] and sha(h.with_suffix('.ex4').read_bytes())==m['binary_sha256']
 for name in ['manifest.json','compile.log','test.ini']:include(p/name,folder+'/'+name)
 return {k:v for k,v in m.items() if k!='rows'}
units={'red':unit('availability613_red',197,98,base),'caller':unit('availability613_green',295,0,expected),'inner':unit('status613_green',785,0,expected),'candidate':unit('candidate613_green_v2',323,0,expected)}
old=reg/'custom613_momready/manifest.json'
red=json.loads(old.read_text());assert not red['passed'] and len([v for v in red['rows'] if v.rstrip().endswith(' FAIL')])==1
include(old,'initial_momready_red/manifest.json');include(reg/'state_initial_failure.json','initial_momready_red/state.json')
groups={};last={}
for kind in state['completed']:
 if kind=='candidate':continue
 if kind.startswith('controller'):p=reg/('controller613_seeded' if kind.endswith('seeded') else 'controller613')
 elif kind=='momready':p=reg/'canonical_fixture_retry/custom613_momready'
 else:p=reg/('custom613_'+kind)
 m=json.loads((p/'manifest.json').read_text())
 assert m.get('source_sha256_lf',m.get('source_sha256_lf_utf8'))==expected,kind
 include(p/'manifest.json',kind+'/manifest.json')
 for q in p.glob('*_compile.log'):include(q,kind+'/'+q.name)
 for name,v in m.get('compiled',{}).items():
  assert '0 errors, 0 warnings' in v['result']
  q=source if name=='BBMA_EA' else repo/'blueprint/tests/custom_mtf'/(name+'.mq4')
  assert lf(q)==v.get('source_sha256_lf_utf8',v.get('harness_sha256_lf')),(kind,name)
  last[str(q.with_suffix('.ex4'))]=v.get('ex4_sha256',v.get('binary_sha256'))
 for rel,v in list(m.get('headers',{}).items())+list(m.get('test_headers',{}).items()):assert lf(repo/rel)==v,(kind,rel)
 if kind.startswith('controller'):
  assert m['candidate_monitor_parity'] and m['old_new_trace_row_counts_equal'] and m['baseline_source_sha256_lf']==base
  for case,v in m['records'].items():
   q=Path(v['trace_path']);assert sha(q.read_bytes())==v['trace_sha256'] and v['counts']['attempts']==0
   include(q,kind+'/'+case+'_trace.txt')
  groups[kind]={k:m[k] for k in ['old_new_difference_count','old_new_differences_first20','candidate_monitor_parity','records']}
 else:
  assert m['passed'],kind
  groups[kind]={'passed':True,'expected':m['expected']}
assert str(source.with_suffix('.ex4')) in last
for p,v in last.items():assert sha(Path(p).read_bytes())==v,p
hst=json.loads((e/'origin_inventory_v1/manifest.json').read_text())['hst_hashes']
assert all(sha(Path(p).read_bytes())==v for p,v in hst.items())
for p in ['run_mhv_availability613.py','run_mhv_status613.py','run_mhv_candidate613.py','run_mhv613_regression.py','resume_mhv613_regression.py']:py_compile.compile(str(r/p),doraise=True)
profile=Path(r'D:\BBMA\HistoricalData\profiles\broker_profile.json')
broker=json.loads(profile.read_text(encoding='utf-8-sig'));assert broker['status']=='UNRESOLVED'
o.mkdir(exist_ok=False)
summary={'verified':True,'task':'SIG-06-MHV','build':'6.13','source_sha256_lf':expected,'baseline_sha256_lf':base,'units':units,'native_groups_completed':state['completed'],'regression':groups,'final_binary_bindings':last,'hst_hashes':hst,'broker_profile':broker,'remaining':'Full historical session/epoch/successful production gap recovery HOLD; no later signal or execution promotion.'}
(o/'summary.json').write_text(json.dumps(summary,indent=2))
with tarfile.open(o/'evidence.tar.xz','w:xz',preset=6) as z:
 def add(name,b):
  info=tarfile.TarInfo(name);info.size=len(b);z.addfile(info,io.BytesIO(b))
 add('summary.json',(o/'summary.json').read_bytes());add('file_index.json',json.dumps(aliases,indent=2).encode())
 for key,b in payload.items():add('objects/'+key,b)
with tarfile.open(o/'evidence.tar.xz','r:xz') as z:
 idx=json.loads(z.extractfile('file_index.json').read());assert idx==aliases
 for k in set(idx.values()):assert sha(z.extractfile('objects/'+k).read())==k
b=(o/'evidence.tar.xz').read_bytes();encoded=base64.b64encode(b).decode()
for i in range((len(encoded)+49999)//50000):(o/('part'+str(i)+'.b64')).write_text(encoded[i*50000:(i+1)*50000])
meta={'sha256':sha(b),'bytes':len(b),'base64_chars':len(encoded),'parts':(len(encoded)+49999)//50000,'chunk_chars':50000,'roundtrip_verified':True,'files':len(aliases),'unique_objects':len(payload)}
(o/'archive.json').write_text(json.dumps(meta,indent=2))
print(json.dumps({'verified':True,'groups':len(state['completed']),'binary_bindings':len(last),'archive':meta,'controller_diffs':{k:groups[k]['old_new_difference_count'] for k in ['controller','controller_seeded']}}),flush=True)
