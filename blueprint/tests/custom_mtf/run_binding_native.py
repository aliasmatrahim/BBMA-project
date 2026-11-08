"""Exercise production binding code in the existing isolated terminal only."""
from pathlib import Path
import argparse,hashlib,json,re,shutil,subprocess
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--kind',choices=['plan','state'],required=True);p.add_argument('--baseline',action='store_true');p.add_argument('--real-broker',action='store_true');a=p.parse_args()
root=a.root;repo=a.repo;tests=repo/'blueprint/tests/custom_mtf';source=repo/'blueprint/source/BBMA_EA.mq4';text=source.read_text()
phase='red' if a.baseline else 'green';tag='binding_'+a.kind+'_'+phase+('_real' if a.real_broker else '');e=root/'evidence'/tag;e.mkdir(parents=True,exist_ok=True)
if a.kind=='plan':
 start=text.index('string RemoveSuffix(');end=text.index('\nstring FindActualSymbol(',start)
 start_id=text.index('int GeneratePairID(');end_id=text.index('\ndatetime GetTodayStart(',start_id)
 names={'MAGIC_BASE','PAIR_ID_MIN','PAIR_ID_MAX','STRATEGY_ID_MIN','STRATEGY_ID_MAX','INSTANCE_ID_MIN','INSTANCE_ID_MAX'}
 constants='\n'.join(x for x in text.splitlines() if x.startswith('#define ') and x.split()[1] in names)
 (tests/'CanonicalPairIdentityFixture.mqh').write_text(constants+'\n'+text[start:end]+text[start_id:end_id])
name='CustomBindingHarness' if a.kind=='plan' else 'CustomStateBindingHarness';h=tests/(name+'.mq4')
if a.baseline:
 target=tests/(name+'Red.mq4');macro='CUSTOM_BINDING_BASELINE' if a.kind=='plan' else 'CUSTOM_STATE_BASELINE';target.write_text('#define '+macro+'\n'+h.read_text());h=target
compiled={}
for path in ([source,h] if a.kind=='state' and not a.baseline and not a.real_broker else [h]):
 log=e/(path.stem+'_compile.log');path.with_suffix('.ex4').unlink(missing_ok=True);log.unlink(missing_ok=True)
 process=subprocess.run([str(root/'metaeditor.exe'),'/compile:'+str(path),'/log:'+str(log)],timeout=60)
 s=log.read_bytes().decode('utf-16');line=next((x for x in s.splitlines() if 'Result:' in x),'NO_RESULT');print(line,flush=True);assert '0 errors, 0 warnings' in line,s
 compiled[path.stem]={'result':line,'compiler_exit':process.returncode,'source_sha256_lf_utf8':hashlib.sha256(path.read_text().encode()).hexdigest(),'ex4_sha256':hashlib.sha256(path.with_suffix('.ex4').read_bytes()).hexdigest()}
shutil.copyfile(h.with_suffix('.ex4'),root/'MQL4/Experts'/h.with_suffix('.ex4').name)
params={'UseFixtureBroker':'false' if a.real_broker else 'true','StrategyID':'1','InstanceID':'0','DebugLevel':'4','ShowDashboard':'false','CustomSymbolMode':'0','CustomSymbolList':''}
for slot in range(1,6):
 for key,value in [('Enable','false'),('Context',''),('Trigger',''),('Symbols','ALL')]:params[f'Custom{slot}_{key}']=value
for tf in ['M1','M5','M15','M30','H1','H4','D1']:params['CustomTF_'+tf]='true';params['CustomSignals_'+tf]=''
preset=root/'tester'/(tag+'.set');preset.write_text(''.join(k+'='+v+'\n' for k,v in params.items()))
cfg=(root/'config/parser_green.ini').read_text().replace('CustomFormulaHarness',h.stem).replace('parser_green.html',tag+'.html')+'\nTestExpertParameters='+preset.name+'\n';f=e/'tester.ini';f.write_text(cfg)
logs=root/'tester/logs';before={x:x.stat().st_size for x in logs.glob('*.log')}
subprocess.run([str(root/'terminal.exe'),'/portable',str(f)],cwd=root,timeout=120,check=True)
rows=[]
for log in logs.glob('*.log'):
 with log.open('rb') as stream:stream.seek(before.get(log,0));rows.extend(stream.read().decode(errors='replace').splitlines())
marker='[CUSTOM-BINDING' if a.kind=='plan' else '[STATE-BINDING';selected=[x for x in rows if marker in x];print('\n'.join(selected),flush=True)
summary=[x for x in selected if '-SUMMARY]' in x];assert len(summary)==1,summary
expected=('passed=7 failed=4' if a.kind=='plan' else 'passed=0 failed=7') if a.baseline else ('passed=11 failed=0' if a.kind=='plan' else ('passed=4 failed=0' if a.real_broker else 'passed=8 failed=0'))
manifest={'scope':'binding planner' if a.kind=='plan' else ('actual broker API rejection/rollback; controller not started' if a.real_broker else 'actual PairState binding with broker-I/O fixtures; EA callbacks renamed; no trading controller called'),'phase':phase,'compiled':compiled,'rows':selected,'expected':expected,'passed':expected in summary[0],'source_sha256_lf_utf8':hashlib.sha256(source.read_text().encode()).hexdigest(),'headers':{str(x.relative_to(repo)).replace(chr(92),'/'):hashlib.sha256(x.read_text().encode()).hexdigest() for x in (repo/'blueprint/source/custom_mtf').glob('*.mqh')}}
(e/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');assert manifest['passed'],summary;print('BINDING_NATIVE_PASS',flush=True)
