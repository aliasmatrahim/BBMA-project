"""Shared native runner for closed-bar, source owners and projections; isolated terminal only."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,struct
from datetime import datetime,timezone
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--kind',choices=['clock','owner','observer','producer','mhv','recovery','flow'],required=True);a=p.parse_args()
root=a.root;repo=a.repo;source=repo/'blueprint/source/BBMA_EA.mq4';tests=repo/'blueprint/tests/custom_mtf';e=root/'evidence'/('custom599_'+a.kind);e.mkdir(parents=True,exist_ok=True)
text=source.read_text();start=text.index('int GetTimeframeSeconds(');end=text.index('\nbool IsValidLotStep(',start);(tests/'CanonicalClockSecondsFixture.mqh').write_text(text[start:end])
name={'clock':'CustomClockHarness','owner':'CustomOwnerHarness','observer':'CustomObserverHarness','producer':'CustomProducerHarness','mhv':'CustomMHVViewHarness','recovery':'CustomRecoveryHarness','flow':'CustomFlowHarness'}[a.kind];h=tests/(name+'.mq4');compiled={}
for path in ([h] if a.kind in ('observer','producer','mhv','recovery') else [source,h]):
 log=e/(path.stem+'_compile.log');log.unlink(missing_ok=True);path.with_suffix('.ex4').unlink(missing_ok=True)
 subprocess.run([str(root/'metaeditor.exe'),'/compile:'+str(path),'/log:'+str(log)],timeout=60)
 s=log.read_bytes().decode('utf-16');line=next((x for x in s.splitlines() if 'Result:' in x),'NO_RESULT');print(line,flush=True);assert '0 errors, 0 warnings' in line,s
 compiled[path.stem]={'result':line,'source_sha256_lf_utf8':hashlib.sha256(path.read_text().encode()).hexdigest(),'ex4_sha256':hashlib.sha256(path.with_suffix('.ex4').read_bytes()).hexdigest()}
shutil.copyfile(h.with_suffix('.ex4'),root/'MQL4/Experts'/h.with_suffix('.ex4').name)
params={'StrategyID':'1','InstanceID':'0','DebugLevel':'4','ShowDashboard':'false','CustomSymbolMode':'0','CustomSymbolList':''}
for tf in ['M1','M5','M15','M30','H1','H4','D1']:params['CustomTF_'+tf]='true';params['CustomSignals_'+tf]=''
for slot in range(1,6):
 for key,value in [('Enable','false'),('Context',''),('Trigger',''),('Symbols','ALL')]:params[f'Custom{slot}_{key}']=value
if a.kind=='flow':
 # Subset mechanics acceptance only; do not certify market/session coverage.
 series={};inputs={}
 for tf in [1,5,30]:
  path=root/'history/MetaQuotes-Demo'/('GBPUSD'+str(tf)+'.hst');raw=path.read_bytes()
  assert struct.unpack_from('<i',raw)[0]==401 and struct.unpack_from('<i',raw,80)[0]==tf
  rows=list(struct.iter_unpack('<qddddqiq',raw[148:]));series[tf]={r[0] for r in rows if all(v>0 for v in r[1:5])}
  inputs[str(tf)]={'path':str(path),'sha256':hashlib.sha256(raw).hexdigest(),'period':tf,'rows':len(rows)}
 base=int(datetime(2026,8,4,tzinfo=timezone.utc).timestamp())
 windows=[hour for hour in range(23) if all(all(t in series[tf] for t in range(base+hour*3600-tf*60,base+hour*3600+7200,tf*60)) for tf in [1,5,30])]
 assert windows,'No complete contiguous two-hour source window on target date'
 hour=windows[0];params.update(PairList='GBPUSD',MaxActivePair='1',MMMode='2',FixedLot='0.01',InstanceID='82',DebugLevel='0',FlowStartHour=str(hour))
 preflight={'scope':'source-bar subset mechanics only; M30 is the previously declared derived OHLC fixture','date':'2026.08.04','start_hour':hour,'duration_seconds':7200,'complete_window_candidates':windows,'inputs':inputs,'omitted_M1_00_minutes':[i for i in range(5) if base+i*60 not in series[1]]}
 (e/'preflight.json').write_text(json.dumps(preflight,indent=2)+'\n');print('FLOW_HISTORY_PREFLIGHT '+json.dumps(preflight),flush=True)
preset=root/'tester'/('custom599_'+a.kind+'.set');preset.write_text(''.join(k+'='+v+'\n' for k,v in params.items()))
cfg=(root/'config/parser_green.ini').read_text().replace('CustomFormulaHarness',name).replace('parser_green.html',name+'599.html')+'\nTestExpertParameters='+preset.name+'\n';f=e/'tester.ini'
if a.kind=='flow':cfg=cfg.replace('TestPeriod=M15','TestPeriod=M1').replace('TestModel=0','TestModel=2').replace('TestFromDate=2026.08.03','TestFromDate=2026.08.04').replace('TestToDate=2026.08.04','TestToDate=2026.08.05')
f.write_text(cfg)
logs=root/'tester/logs';before={x:x.stat().st_size for x in logs.glob('*.log')}
subprocess.run([str(root/'terminal.exe'),'/portable',str(f)],cwd=root,timeout=90,check=True)
rows=[];marker={'clock':'[CUSTOM-CLOCK','owner':'[CUSTOM-OWNER','observer':'[CUSTOM-OBSERVER','producer':'[CUSTOM-PRODUCER','mhv':'[CUSTOM-MHV','recovery':'[CUSTOM-RECOVERY','flow':'[CUSTOM-FLOW'}[a.kind]
for log in logs.glob('*.log'):
 with log.open('rb') as stream:stream.seek(before.get(log,0));rows.extend(x for x in stream.read().decode(errors='replace').splitlines() if marker in x)
print('\n'.join(rows),flush=True);summary=[x for x in rows if '-SUMMARY]' in x];expected={'clock':'passed=14 failed=0','owner':'passed=10 failed=0','observer':'passed=4 failed=0','producer':'passed=22 failed=0','mhv':'passed=8 failed=0','recovery':'passed=27 failed=0','flow':'passed=12 failed=0'}[a.kind]
manifest={'build':'5.99','scope':{'clock':'closed-bar observation kernel','owner':'read-only canonical M08/M12 projection; no detector/controller invoked','observer':'actual observer with bar/quote fixtures; no trading controller invoked','producer':'actual M06/M08/M12 auxiliary producer in isolated tester; no trading controller invoked','mhv':'canonical M09 projection with owner fixtures; no detector/controller invoked','recovery':'actual M06/M08/M12 anchored replay vs continuous control; no trading controller invoked','flow':'actual canonical callbacks/M27 custom-only observer/producer path with moving M1 tester bars; monitor fixture, slots OFF'}[a.kind],'source_sha256_lf_utf8':hashlib.sha256(text.encode()).hexdigest(),'compiled':compiled,'rows':rows,'expected':expected,'passed':len(summary)==1 and expected in summary[0],'headers':{str(x.relative_to(repo)).replace(chr(92),'/'):hashlib.sha256(x.read_text().encode()).hexdigest() for x in (repo/'blueprint/source/custom_mtf').glob('*.mqh')}}
manifest['test_headers']={str(x.relative_to(repo)).replace(chr(92),'/'):hashlib.sha256(x.read_text().encode()).hexdigest() for x in tests.glob('CustomOwnerTestEquality.mqh')}
if a.kind=='flow':manifest['preflight']=preflight;manifest['tester']={'period':'M1','model':2,'from':'2026.08.04','to':'2026.08.05','duration_seconds':7200,'slots_enabled':False}
(e/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');assert manifest['passed'],summary;print('CLOCK_OWNER_NATIVE_PASS',flush=True)
