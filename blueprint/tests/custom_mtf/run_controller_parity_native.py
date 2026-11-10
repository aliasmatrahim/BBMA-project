"""Actual canonical controller comparison; test-only OrderSend capture, no live orders."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,re
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--expected-source-sha',default='0266fb3318348ae64b7bbbb52a1b30a0e79994df64979377cd14c1ba877c666e');p.add_argument('--baseline-build',choices=['605','606','607','608','609','610','611'],default='605');p.add_argument('--evidence-root',type=Path);p.add_argument('--seeded',action='store_true');a=p.parse_args()
root=a.root;repo=a.repo;test=repo/'blueprint/tests/custom_mtf';build=re.search(r'#property version\s+"([^"]+)"',(repo/'blueprint/source/BBMA_EA.mq4').read_text()).group(1);tag=build.replace('.','');e=(a.evidence_root or root/'evidence')/('controller'+tag+('_seeded' if a.seeded else ''));e.mkdir(parents=True,exist_ok=True)
source=repo/'blueprint/source/BBMA_EA.mq4';source_hash=hashlib.sha256(source.read_text().encode()).hexdigest()
assert source_hash==a.expected_source_sha
baseline_paths={'611':'ext611-stage/blueprint/source/BBMA_EA.mq4','610':'mom610-stage/blueprint/source/BBMA_EA.mq4','609':'csak609-stage/blueprint/source/BBMA_EA.mq4','608':'csa608-stage/blueprint/source/BBMA_EA.mq4','605':'evidence/stage606_baseline/blueprint/source/BBMA_EA.mq4','606':'597-stage/blueprint/source/BBMA_EA.mq4','607':'ecsd607-stage/blueprint/source/BBMA_EA.mq4'}
baseline_fences={'611':'a62672ae1874fcbf61c671af01da09ef45ffe6972abd998ec70c5f9a74c238cb','610':'ebe3e4155b0ae5211432957ed999e04b58bc0a043b40a23ce76d24257346baae','609':'d74f41d0c85e8ec5e4afdd58728c4cfcaae5765adc128f4aefa849edbfb04c25','608':'f317317f2ba7145990b66340aea6022a385e464e72da4e01be2d71f1c12e7e9c','605':'4247b5aa6babc62d7680fcb71e8859a74452638ba60c9c0fa084fae7f6f78415','606':'0266fb3318348ae64b7bbbb52a1b30a0e79994df64979377cd14c1ba877c666e','607':'3c2745e4fd9d0d84c66c6e5442388f0d8de05ccb211fff81bd4ed38a2e310b44'}
baseline_path=root/baseline_paths[a.baseline_build];baseline=baseline_path.read_text();assert hashlib.sha256(baseline.encode()).hexdigest()==baseline_fences[a.baseline_build]
(repo/'blueprint/source/BBMA_EA_ParityBaseline605.mq4').write_text(baseline)
h=test/'CustomControllerParityHarness.mq4';hb=test/'CustomControllerBaselineHarness.mq4';hb.write_text('#define CONTROLLER_BASELINE605\n'+h.read_text())
compiled={}
for path in [h,hb]:
 log=e/(path.stem+'_compile.log');log.unlink(missing_ok=True);path.with_suffix('.ex4').unlink(missing_ok=True)
 subprocess.run([str(root/'metaeditor.exe'),'/compile:'+str(path),'/log:'+str(log)],timeout=60)
 line=next((x for x in log.read_bytes().decode('utf-16').splitlines() if 'Result:' in x),'NO_RESULT');assert '0 errors, 0 warnings' in line,log.read_bytes().decode('utf-16')
 compiled[path.stem]={'result':line,'harness_sha256_lf':hashlib.sha256(path.read_text().encode()).hexdigest(),'binary_sha256':hashlib.sha256(path.with_suffix('.ex4').read_bytes()).hexdigest()}
 shutil.copyfile(path.with_suffix('.ex4'),root/'MQL4/Experts'/path.with_suffix('.ex4').name)
records={};payloads={}
for case,name,monitor in [('off',h.stem,'false'),('on',h.stem,'true'),('baseline'+a.baseline_build,hb.stem,'false')]:
 params={'PairList':'GBPUSD','MaxActivePair':'1','MMMode':'2','FixedLot':'0.01','InstanceID':'82','DebugLevel':'0','ShowDashboard':'false','MonitorRequested':monitor,'SeedPending':'true' if a.seeded else 'false','CustomSymbolMode':'0','CustomSymbolList':''}
 for tf in ['M1','M5','M15','M30','H1','H4','D1']:params['CustomTF_'+tf]='true';params['CustomSignals_'+tf]=''
 for slot in range(1,6):
  for key,value in [('Enable','false'),('Context',''),('Trigger',''),('Symbols','ALL')]:params[f'Custom{slot}_{key}']=value
 preset=root/'tester'/('controller'+tag+'_'+case+'.set');preset.write_text(''.join(k+'='+v+'\n' for k,v in params.items()))
 cfg=(root/'config/parser_green.ini').read_text().replace('CustomFormulaHarness',name).replace('parser_green.html',case+tag+'.html').replace('TestPeriod=M15','TestPeriod=M1').replace('TestModel=0','TestModel=2').replace('TestFromDate=2026.08.03','TestFromDate=2026.08.04').replace('TestToDate=2026.08.04','TestToDate=2026.08.05')+'\nTestExpertParameters='+preset.name+'\n'
 assert 'ExpertsTrades=false' in cfg
 ini=e/(case+'.ini');ini.write_text(cfg);logs=root/'tester/logs';before={x:x.stat().st_size for x in logs.glob('*.log')}
 subprocess.run([str(root/'terminal.exe'),'/portable',str(ini)],cwd=root,timeout=150,check=True)
 rows=[]
 for log in logs.glob('*.log'):
  with log.open('rb') as stream:stream.seek(before.get(log,0));rows.extend(stream.read().decode(errors='replace').splitlines())
 summaries=[x for x in rows if '[CUSTOM-PARITY-SUMMARY]' in x];assert len(summaries)==1,summaries
 summary=summaries[0];observed_ok=('ok=true' in summary or 'ok=1' in summary);assert observed_ok==(not(a.seeded and a.baseline_build=='605' and case=='baseline605')),summary
 isolation=[x for x in rows if '[CUSTOM-PARITY-INIT]' in x];assert len(isolation)==2 and ('checkpointAfter=false' in isolation[1] or 'checkpointAfter=0' in isolation[1]),isolation
 payload=[x.split('[CUSTOM-PARITY] ',1)[1] for x in rows if '[CUSTOM-PARITY] ' in x]
 assert len(payload)>1000
 trace=e/(case+'_trace.txt');trace.write_text('\n'.join(payload)+'\n');payloads[case]=payload
 counts={k:int(v) for k,v in re.findall(r'(cycles|valid|frames|attempts|seeds|handovers|csaViews|extViews)=(\d+)',summary)}
 records[case]={'initial_checkpoint_isolation':isolation,'summary':summary,'counts':counts,'trace_path':str(trace),'trace_rows':len(payload),'trace_sha256':hashlib.sha256(trace.read_bytes()).hexdigest()}
 print(json.dumps({'case':case,**counts,'rows':len(payload)}),flush=True)
off=payloads['off'];on=payloads['on'];base=payloads['baseline'+a.baseline_build]
parity=(off==on);differences=[{'off':x,'on':y} for x,y in zip(off,on) if x!=y][:10]
old_diff=[{'baseline'+a.baseline_build:x,'candidate':y} for x,y in zip(base,off) if x!=y]
manifest={'build':build,'seeded_trusted_owner_fixtures':a.seeded,'source_sha256_lf':source_hash,'baseline_build':a.baseline_build,'baseline_source_sha256_lf':hashlib.sha256(baseline.encode()).hexdigest(),'compiled':compiled,'records':records,'candidate_monitor_parity':parity,'candidate_differences_first10':differences,'old_new_trace_row_counts_equal':len(base)==len(off),'old_new_difference_count':len(old_diff),'old_new_differences_first20':old_diff[:20],'scope':'Actual OnTick/OnTimer -> M27 -> ProcessPair on GBPUSD M1 delivery model2 with canonical M15 clock, Aug4 2026 02:00-06:00 chart time; fresh initialized owners unless seeded_trusted_owner_fixtures=true (explicit pending handover fixtures, not historical formation), M30 derived fixture; no wall-clock timer, arbitrary cold-start/session or positive-entry claim. Test-only OrderSend capture replaces broker send; all custom slots OFF. Full scalar owner/decision traces are compared, not only hashes.'}
(e/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
assert parity and len(base)==len(off),manifest['candidate_differences_first10']
print('CONTROLLER'+tag+'_PARITY_PASS',flush=True)
