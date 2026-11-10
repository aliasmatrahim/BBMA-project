from pathlib import Path
import json,hashlib,gzip,base64
r=Path(r'D:\BBMA\MT4_CustomMTF_302_Unit');repo=r/'ext611-stage';e=r/'evidence/sig05_extreme'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lf=lambda p:hashlib.sha256(p.read_text().encode()).hexdigest()
state=json.loads((r/'ext611_regression_state.json').read_text());extra=json.loads((r/'ext611_extra_state.json').read_text());assert state['status']==extra['status']=='PASS'
source=repo/'blueprint/source/BBMA_EA.mq4';assert lf(source)==state['source_sha256_lf']=='a62672ae1874fcbf61c671af01da09ef45ffe6972abd998ec70c5f9a74c238cb'
manifests={}
for kind in [k for k in state['completed'] if k not in ['source','lifecycle','controller']]+['owner']:
 p=e/('custom611_'+kind)/'manifest.json';m=json.loads(p.read_text());assert m['passed'] and m['source_sha256_lf_utf8']==lf(source),(kind,m.get('passed'))
 for rel,h in m['headers'].items():assert lf(repo/rel)==h,rel
 for rel,h in m.get('test_headers',{}).items():assert lf(repo/rel)==h,rel
 manifests[kind]=m
latest={}
for kind,m in sorted(manifests.items(),key=lambda kv:(e/('custom611_'+kv[0])/'manifest.json').stat().st_mtime):
 for name,b in m['compiled'].items():latest[name]=dict(b,manifest=kind)
bindings={}
for name,b in latest.items():
 p=source if name=='BBMA_EA' else repo/'blueprint/tests/custom_mtf'/(name+'.mq4')
 assert lf(p)==b['source_sha256_lf_utf8'] and sha(p.with_suffix('.ex4'))==b['ex4_sha256'],name
 bindings[name]=b
custom={}
for kind,folder,name,expected in [('source','source_green','CustomExtremeSourceHarness','passed=141 failed=0'),('lifecycle','lifecycle','CustomExtremeLifecycleHarness','passed=716 failed=0 history=140')]:
 m=json.loads((e/folder/'manifest.json').read_text());assert m['source_sha256_lf']==lf(source)
 assert any(expected in x for x in m['rows']) and '0 errors, 0 warnings' in m['compile']
 p=repo/'blueprint/tests/custom_mtf'/(name+'.mq4');assert lf(p)==m['harness_sha256_lf'] and sha(p.with_suffix('.ex4'))==m['binary_sha256'],name
 bindings[name]={k:m[k] for k in ['harness_sha256_lf','binary_sha256','compile']};custom[kind]=m
c=json.loads((e/'controller611/manifest.json').read_text());assert c['source_sha256_lf']==lf(source) and c['candidate_monitor_parity'] and c['old_new_trace_row_counts_equal']
for name,b in c['compiled'].items():
 p=repo/'blueprint/tests/custom_mtf'/(name+'.mq4');assert lf(p)==b['harness_sha256_lf'] and sha(p.with_suffix('.ex4'))==b['binary_sha256'],name
 bindings[name]=b
traces={}
for case,rec in c['records'].items():
 p=Path(rec['trace_path']);assert sha(p)==rec['trace_sha256'] and rec['trace_rows']==12224 and rec['counts']['cycles']==16 and rec['counts']['attempts']==0
 if case=='on':assert rec['counts']['csaViews']==630 and rec['counts']['extViews']==180
 raw=p.read_bytes();z=gzip.compress(raw,mtime=0);out=e/(case+'_trace.txt.gz');out.write_bytes(z);(e/(case+'_trace.base64')).write_text(base64.b64encode(z).decode())
 traces[case]={'raw_sha256':sha(p),'gzip_sha256':sha(out),'rows':rec['trace_rows'],'bytes':len(raw),'gzip_bytes':len(z)}
baseline=json.loads((e/'baseline610_lifecycle/manifest.json').read_text());assert baseline['source_sha256_lf']=='ebe3e4155b0ae5211432957ed999e04b58bc0a043b40a23ce76d24257346baae' and any('passed=716 failed=0 history=140' in x for x in baseline['rows'])
p=repo/'blueprint/tests/custom_mtf/CustomExtremeLifecycleBaselineHarness.mq4';assert lf(p)==baseline['harness_sha256_lf'] and sha(p.with_suffix('.ex4'))==baseline['binary_sha256']
red={}
for label,path in [('M08_partial_source','source_red/manifest.json'),('handover_initial','handover_red/manifest.json'),('handover_revision','revision_handover_red/manifest.json'),('initial22_green','source22_green.json'),('lifecycle_clock_fixture','lifecycle_initial_clock_fixture_red.json')]:
 red[label]=json.loads((e/path).read_text())
bundle={'source_sha256_lf':lf(source),'state':state,'extra':extra,'bindings':bindings,'manifests':manifests,'custom':custom,'controller':c,'traces':traces,'baseline716':baseline,'red':red}
raw=json.dumps(bundle,indent=2).encode();z=gzip.compress(raw,mtime=0);(e/'ext611_evidence.json.gz').write_bytes(z);(e/'ext611_evidence.base64').write_text(base64.b64encode(z).decode())
summary={'verified':True,'source_sha256_lf':lf(source),'groups':{k:m['expected'] for k,m in manifests.items()},'custom_groups':{'source':141,'lifecycle':716},'baseline_lifecycle':716,'binding_count':len(bindings),'controller':c,'traces':traces,'archive_sha256':hashlib.sha256(z).hexdigest(),'archive_bytes':len(z)}
(e/'ext611_final_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps({'verified':True,'native_groups':len(manifests)+2,'bindings':len(bindings),'baseline_differences':c['old_new_difference_count'],'archive_bytes':len(z),'traces':traces}),flush=True)
