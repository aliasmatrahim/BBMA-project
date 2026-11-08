"""Native proof that adding custom PairState never enables canonical dispatch."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--baseline-source',type=Path,required=True);a=p.parse_args()
root=a.root;repo=a.repo;tests=repo/'blueprint/tests/custom_mtf';h=tests/'CustomScopeHarness.mq4';e=root/'evidence/scope596';e.mkdir(parents=True,exist_ok=True)
manifest={}
for phase,source in [('red',a.baseline_source),('green',repo/'blueprint/source/BBMA_EA.mq4')]:
 text=source.read_text();start=text.index('void OnTickMain()');end=text.index('\n//+---',start);body=text[start:end]
 (tests/'CanonicalDispatchFixture.mqh').write_text(body)
 log=e/(phase+'_compile.log');h.with_suffix('.ex4').unlink(missing_ok=True);log.unlink(missing_ok=True)
 subprocess.run([str(root/'metaeditor.exe'),'/compile:'+str(h),'/log:'+str(log)],timeout=60)
 output=log.read_bytes().decode('utf-16');assert '0 errors, 0 warnings' in output,output
 shutil.copyfile(h.with_suffix('.ex4'),root/'MQL4/Experts/CustomScopeHarness.ex4')
 cfg=(root/'config/parser_green.ini').read_text().replace('CustomFormulaHarness','CustomScopeHarness').replace('parser_green.html','scope_'+phase+'.html');f=e/(phase+'.ini');f.write_text(cfg)
 logs=root/'tester/logs';before={x:x.stat().st_size for x in logs.glob('*.log')}
 subprocess.run([str(root/'terminal.exe'),'/portable',str(f)],cwd=root,timeout=90,check=True)
 rows=[]
 for log_path in logs.glob('*.log'):
  with log_path.open('rb') as stream:stream.seek(before.get(log_path,0));rows.extend(x for x in stream.read().decode(errors='replace').splitlines() if '[SCOPE-ROUTING' in x)
 expected='passed=1 failed=2' if phase=='red' else 'passed=3 failed=0';summary=[x for x in rows if '-SUMMARY]' in x];print(phase,rows,flush=True)
 manifest[phase]={'source_sha256_lf_utf8':hashlib.sha256(text.encode()).hexdigest(),'dispatch_body_sha256_lf_utf8':hashlib.sha256(body.encode()).hexdigest(),'compile':next(x for x in output.splitlines() if 'Result:' in x),'rows':rows,'expected':expected}
 assert len(summary)==1 and expected in summary[0],summary
(e/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('SCOPE_NATIVE_PASS',flush=True)
