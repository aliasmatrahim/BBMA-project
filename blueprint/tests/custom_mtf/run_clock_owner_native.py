"""Native closed-bar kernel and read-only owner projections; isolated terminal only."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--kind',choices=['clock','owner','observer'],required=True);a=p.parse_args()
root=a.root;repo=a.repo;source=repo/'blueprint/source/BBMA_EA.mq4';tests=repo/'blueprint/tests/custom_mtf';e=root/'evidence'/('custom597_'+a.kind);e.mkdir(parents=True,exist_ok=True)
text=source.read_text();start=text.index('int GetTimeframeSeconds(');end=text.index('\nbool IsValidLotStep(',start);(tests/'CanonicalClockSecondsFixture.mqh').write_text(text[start:end])
name={'clock':'CustomClockHarness','owner':'CustomOwnerHarness','observer':'CustomObserverHarness'}[a.kind];h=tests/(name+'.mq4');compiled={}
for path in ([h] if a.kind=='observer' else [source,h]):
 log=e/(path.stem+'_compile.log');log.unlink(missing_ok=True);path.with_suffix('.ex4').unlink(missing_ok=True)
 subprocess.run([str(root/'metaeditor.exe'),'/compile:'+str(path),'/log:'+str(log)],timeout=60)
 s=log.read_bytes().decode('utf-16');line=next((x for x in s.splitlines() if 'Result:' in x),'NO_RESULT');print(line,flush=True);assert '0 errors, 0 warnings' in line,s
 compiled[path.stem]={'result':line,'source_sha256_lf_utf8':hashlib.sha256(path.read_text().encode()).hexdigest(),'ex4_sha256':hashlib.sha256(path.with_suffix('.ex4').read_bytes()).hexdigest()}
shutil.copyfile(h.with_suffix('.ex4'),root/'MQL4/Experts'/h.with_suffix('.ex4').name)
params={'StrategyID':'1','InstanceID':'0','DebugLevel':'4','ShowDashboard':'false','CustomSymbolMode':'0','CustomSymbolList':''}
for tf in ['M1','M5','M15','M30','H1','H4','D1']:params['CustomTF_'+tf]='true';params['CustomSignals_'+tf]=''
for slot in range(1,6):
 for key,value in [('Enable','false'),('Context',''),('Trigger',''),('Symbols','ALL')]:params[f'Custom{slot}_{key}']=value
preset=root/'tester'/('custom597_'+a.kind+'.set');preset.write_text(''.join(k+'='+v+'\n' for k,v in params.items()))
cfg=(root/'config/parser_green.ini').read_text().replace('CustomFormulaHarness',name).replace('parser_green.html',name+'597.html')+'\nTestExpertParameters='+preset.name+'\n';f=e/'tester.ini';f.write_text(cfg)
logs=root/'tester/logs';before={x:x.stat().st_size for x in logs.glob('*.log')}
subprocess.run([str(root/'terminal.exe'),'/portable',str(f)],cwd=root,timeout=90,check=True)
rows=[];marker={'clock':'[CUSTOM-CLOCK','owner':'[CUSTOM-OWNER','observer':'[CUSTOM-OBSERVER'}[a.kind]
for log in logs.glob('*.log'):
 with log.open('rb') as stream:stream.seek(before.get(log,0));rows.extend(x for x in stream.read().decode(errors='replace').splitlines() if marker in x)
print('\n'.join(rows),flush=True);summary=[x for x in rows if '-SUMMARY]' in x];expected={'clock':'passed=14 failed=0','owner':'passed=10 failed=0','observer':'passed=4 failed=0'}[a.kind]
manifest={'build':'5.97','scope':{'clock':'closed-bar observation kernel','owner':'read-only canonical M08/M12 projection; no detector/controller invoked','observer':'actual observer with bar/quote fixtures; no detector or trading controller invoked'}[a.kind],'source_sha256_lf_utf8':hashlib.sha256(text.encode()).hexdigest(),'compiled':compiled,'rows':rows,'expected':expected,'passed':len(summary)==1 and expected in summary[0],'headers':{str(x.relative_to(repo)).replace(chr(92),'/'):hashlib.sha256(x.read_text().encode()).hexdigest() for x in (repo/'blueprint/source/custom_mtf').glob('*.mqh')}}
(e/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');assert manifest['passed'],summary;print('CLOCK_OWNER_NATIVE_PASS',flush=True)
