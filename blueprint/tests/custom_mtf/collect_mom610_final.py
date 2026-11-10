from pathlib import Path
import json,hashlib,gzip,base64
r=Path(r'D:\BBMA\MT4_CustomMTF_302_Unit');repo=r/'mom610-stage';e=r/'evidence/sig04_mom'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lf=lambda p:hashlib.sha256(p.read_text().encode()).hexdigest()
state=json.loads((r/'mom610_regression_state.json').read_text());assert state['status']=='PASS',state
source=repo/'blueprint/source/BBMA_EA.mq4';assert lf(source)==state['source_sha256_lf']
manifests={}
for kind in ['momready']+state['completed']:
 if kind=='controller':continue
 p=e/('custom610_'+kind)/'manifest.json';m=json.loads(p.read_text());assert m['passed'] and m['source_sha256_lf_utf8']==lf(source),(kind,m.get('passed'))
 for rel,h in m['headers'].items():assert lf(repo/rel)==h,rel
 for rel,h in m.get('test_headers',{}).items():assert lf(repo/rel)==h,rel
 manifests[kind]=m
c=json.loads((e/'controller610/manifest.json').read_text());assert c['candidate_monitor_parity'] and c['old_new_trace_row_counts_equal']
assert c['source_sha256_lf']==lf(source)
latest={}
for kind,m in sorted(manifests.items(),key=lambda kv:(e/('custom610_'+kv[0])/'manifest.json').stat().st_mtime):
 for name,b in m['compiled'].items():latest[name]=dict(b,manifest=kind)
bindings={}
for name,b in latest.items():
 p=source if name=='BBMA_EA' else repo/'blueprint/tests/custom_mtf'/(name+'.mq4')
 assert lf(p)==b['source_sha256_lf_utf8'],name
 assert sha(p.with_suffix('.ex4'))==b['ex4_sha256'],name
 bindings[name]=b
for name,b in c['compiled'].items():
 p=repo/'blueprint/tests/custom_mtf'/(name+'.mq4')
 assert lf(p)==b['harness_sha256_lf'] and sha(p.with_suffix('.ex4'))==b['binary_sha256'],name
 bindings[name]=b
traces={}
for case,rec in c['records'].items():
 p=Path(rec['trace_path']);assert sha(p)==rec['trace_sha256']
 assert rec['trace_rows']==12224 and rec['counts']['cycles']==16 and rec['counts']['attempts']==0
 if case=='on':assert rec['counts']['csaViews']==630
 raw=p.read_bytes();z=gzip.compress(raw,mtime=0);out=e/(case+'_trace.txt.gz');out.write_bytes(z)
 (e/(case+'_trace.base64')).write_text(base64.b64encode(z).decode())
 traces[case]={'raw_sha256':sha(p),'gzip_sha256':sha(out),'rows':rec['trace_rows'],'bytes':len(raw),'gzip_bytes':len(z)}
red={}
for label,path in [('missing_close','gap_red/manifest.json'),('readiness_baseline','readiness_red/manifest.json'),('retry','recovery_retry_red.json'),('review_edges','review_edges_red.json'),('incomplete_fixture','canonmhv_incomplete_fixture_red.json')]:
 p=e/path
 assert p.exists(),str(p)
 red[label]=json.loads(p.read_text())
bundle={'source_sha256_lf':lf(source),'regression_state':state,'bindings':bindings,'manifests':manifests,'controller':c,'traces':traces,'red':red}
raw=json.dumps(bundle,indent=2).encode();z=gzip.compress(raw,mtime=0);(e/'mom610_evidence.json.gz').write_bytes(z);(e/'mom610_evidence.base64').write_text(base64.b64encode(z).decode())
summary={'verified':True,'source_sha256_lf':lf(source),'groups':{k:m['expected'] for k,m in manifests.items()},'binding_count':len(bindings),'controller':c,'traces':traces,'archive_sha256':hashlib.sha256(z).hexdigest(),'archive_bytes':len(z)}
(e/'mom610_final_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps({'verified':True,'groups':len(manifests),'bindings':len(bindings),'baseline_differences':c['old_new_difference_count'],'archive_bytes':len(z),'traces':traces}),flush=True)
