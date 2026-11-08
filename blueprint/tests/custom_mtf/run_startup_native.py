"""Observe actual EA OnInit in the existing isolated offline Strategy Tester.

Records environmental blocks without weakening production gates. No real orders,
login, terminal primary restart or account configuration is performed.
"""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);a=p.parse_args()
root=a.root;repo=a.repo;source=repo/'blueprint/source/BBMA_EA.mq4';binary=source.with_suffix('.ex4')
assert 'V595_TESTER_TIMER_INIT_20261108' in source.read_text()
name='BBMA_Custom595_Startup';shutil.copyfile(binary,root/'MQL4/Experts'/(name+'.ex4'))
evidence=root/'evidence/startup595';evidence.mkdir(parents=True,exist_ok=True)
results=[]
base='PairList=GBPUSD\nMaxActivePair=1\nMMMode=2\nFixedLot=0.01\nInstanceID=82\nDebugLevel=4\nShowDashboard=false\n'
for case,extra,expected in [
 ('defaults','',True),
 ('changed_inputs','CustomSignals_M1=MOM, RE\n',True),
 ('invalid_formula','Custom1_Enable=true\nCustom1_Context=\nCustom1_Trigger=M1:MOM\n',False),
 ('unavailable','Custom1_Enable=true\nCustom1_Context=D1:RE\nCustom1_Trigger=M1:MOM\nCustomSignals_D1=RE\nCustomSignals_M1=MOM\n',False)]:
 defaults={'CustomSymbolMode':'0','CustomSymbolList':''}
 for tf in ['M1','M5','M15','M30','H1','H4','D1']:defaults['CustomTF_'+tf]='true';defaults['CustomSignals_'+tf]=''
 for slot in range(1,6):
  for key,value in [('Enable','false'),('Context',''),('Trigger',''),('Symbols','ALL')]:defaults[f'Custom{slot}_{key}']=value
 for line in (base+extra).splitlines():
  if '=' in line:key,value=line.split('=',1);defaults[key]=value
 preset=root/'tester'/('startup595_'+case+'.set');preset.write_text(''.join(key+'='+value+'\n' for key,value in defaults.items()))
 cfg=(root/'config/parser_green.ini').read_text().replace('CustomFormulaHarness',name).replace('parser_green.html','startup595_'+case+'.html')+'\nTestExpertParameters='+preset.name+'\n'
 f=evidence/(case+'.ini');f.write_text(cfg)
 logs=root/'tester/logs';before={x:x.stat().st_size for x in logs.glob('*.log')}
 subprocess.run([str(root/'terminal.exe'),'/portable',str(f)],cwd=root,timeout=90,check=True)
 rows=[]
 for log in logs.glob('*.log'):
  with log.open('rb') as stream:stream.seek(before.get(log,0));rows+=stream.read().decode(errors='replace').splitlines()
 (evidence/(case+'.log')).write_text('\n'.join(rows)+'\n')
 meaningful=[x for x in rows if any(t in x for t in ['[F7-BUILD]','[P3S1]','initialization','initialized','deinitialized','CUSTOM_SLOT','SYMBOL_UNRESOLVED','parameter validation','Failed to register EA timer'])]
 initialized=any('BBMA EA V595_TESTER_TIMER_INIT_20261108 initialized successfully' in x for x in rows) and not any('initialization failed' in x or 'Failed to register EA timer' in x for x in rows)
 rejected=any('Input parameter validation failed' in x for x in rows)
 reason_expected={'invalid_formula':'CUSTOM_SLOT_1:CONTEXT:UNKNOWN_TIMEFRAME@0','unavailable':'CUSTOM_SLOT_1:SIGNAL_UNAVAILABLE'}.get(case,'')
 precise_rejection=rejected and any(reason_expected in x for x in rows) if reason_expected else rejected
 status=('PASS' if initialized else 'VERIFICATION_REQUIRED') if expected else ('PASS' if precise_rejection and not initialized else 'FAIL')
 item={'case':case,'expected_init':expected,'initialized':initialized,'input_rejected':rejected,'status':status,'rows':meaningful};results.append(item)
 print(json.dumps(item),flush=True)
manifest={'build':'5.95','source_sha256_lf_utf8':hashlib.sha256(source.read_text().encode()).hexdigest(),'ex4_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'cases':results,'scope':'actual EA OnInit/offline Strategy Tester; not live terminal reattachment, recovery, profitability or custom execution'}
(evidence/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('STARTUP_OBSERVATIONS_SAVED',flush=True)
