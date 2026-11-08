"""Run pure configuration harnesses in the existing isolated G40 terminal.

Requires an already staged repo, offline terminal and config/parser_green.ini.
Never launches the primary terminal. No trading/account setup is performed.
"""
from pathlib import Path
import argparse, hashlib, json, re, shutil, subprocess

p=argparse.ArgumentParser()
p.add_argument('--root',type=Path,required=True)
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--only-reinit',action='store_true')
a=p.parse_args(); root=a.root; repo=a.repo
source=repo/'blueprint/source/BBMA_EA.mq4'; text=source.read_text()
tests=repo/'blueprint/tests/custom_mtf'; evidence=root/'evidence/config595';evidence.mkdir(parents=True,exist_ok=True)
start=text.index('string RemoveSuffix(');end=text.index('\ndouble GetPointSize(',start)
resolver=text[start:end]
(tests/'CanonicalNativeResolver.mqh').write_text(resolver)
(tests/'CanonicalResolverFixture.mqh').write_text(resolver.replace('SymbolsTotal(', 'FixtureSymbolsTotal(').replace('SymbolName(', 'FixtureSymbolName(').replace('SymbolSelect(', 'FixtureSymbolSelect('))
results={};compiled={}
def compile_file(path,name):
 log=evidence/(name+'_compile.log')
 log.unlink(missing_ok=True);path.with_suffix('.ex4').unlink(missing_ok=True)
 process=subprocess.run([str(root/'metaeditor.exe'),'/compile:'+str(path),'/log:'+str(log)],timeout=60)
 s=log.read_bytes().decode('utf-16');line=next((x for x in s.splitlines() if 'Result:' in x),'NO_RESULT')
 print(name,line,flush=True);assert '0 errors, 0 warnings' in line,s
 compiled[name]={'result':line,'compiler_process_exit':process.returncode,'source_sha256_lf_utf8':hashlib.sha256(path.read_text().encode()).hexdigest(),'ex4_sha256':hashlib.sha256(path.with_suffix('.ex4').read_bytes()).hexdigest()}
 return path.with_suffix('.ex4')
if not a.only_reinit:compile_file(source,'full595')
def run(name,params,marker,expected_reason=None):
 defaults={'ExpectedValid':'true','CustomSymbolMode':'0','CustomSymbolList':''}
 for tf in ['M1','M5','M15','M30','H1','H4','D1']:defaults['CustomTF_'+tf]='true';defaults['CustomSignals_'+tf]=''
 for slot in range(1,6):
  for key,value in [('Enable','false'),('Context',''),('Trigger',''),('Symbols','ALL')]:defaults[f'Custom{slot}_{key}']=value
 for line in params.splitlines():
  if '=' in line:key,value=line.split('=',1);defaults[key]=value
 preset=evidence/(name+'.set');preset.write_text(''.join(key+'='+value+'\n' for key,value in defaults.items()))
 # MT4 resolves preset basenames under tester, so preserve the exact tested preset there.
 shutil.copyfile(preset,root/'tester'/preset.name)
 cfg=(root/'config/parser_green.ini').read_text().replace('CustomFormulaHarness',current).replace('parser_green.html',name+'.html')+'\nTestExpertParameters='+preset.name+'\n'
 f=evidence/(name+'.ini');f.write_text(cfg)
 logs=root/'tester/logs';before={x:x.stat().st_size for x in logs.glob('*.log')}
 subprocess.run([str(root/'terminal.exe'),'/portable',str(f)],cwd=root,timeout=60,check=True)
 rows=[]
 for log in logs.glob('*.log'):
  with log.open('rb') as stream:stream.seek(before.get(log,0));rows.extend(x for x in stream.read().decode(errors='replace').splitlines() if marker in x)
 print(name,rows,flush=True);assert rows,'Missing fresh runtime marker'
 results[name]=rows
 if marker=='[CUSTOM-REINIT]':
  assert len(rows)==1 and 'passed=true' in rows[0]
  if expected_reason is not None:assert 'reason='+expected_reason+' clean=' in rows[0],rows
 else:assert len(rows)==1 and re.search(r'failed=0(?:\D|$)',rows[0])
for current,marker in [('CustomFormulaHarness','[CUSTOM-PARSER-SUMMARY]'),('CustomSlotHarness','[CUSTOM-SLOT-SUMMARY]'),('CustomIdentityHarness','[CONFIG-ID-SUMMARY]'),('CustomSymbolHarness','[CUSTOM-SYMBOL-SUMMARY]'),('CustomReinitHarness','[CUSTOM-REINIT]')]:
 if a.only_reinit and current!='CustomReinitHarness':continue
 binary=compile_file(tests/(current+'.mq4'),current);shutil.copyfile(binary,root/'MQL4/Experts'/binary.name)
 if current!='CustomReinitHarness':run(current,'',marker);continue
 for name,params,expected_reason in [
  ('defaults','ExpectedValid=true\n',''),
  ('spaced_signal_list','ExpectedValid=true\nCustomSignals_M1=MOM, RE\n',''),
  ('invalid_formula','ExpectedValid=false\nCustom1_Enable=true\nCustom1_Context=\nCustom1_Trigger=M1:MOM\n','CUSTOM_SLOT_1:CONTEXT:UNKNOWN_TIMEFRAME@0'),
  ('unavailable','ExpectedValid=false\nCustom1_Enable=true\nCustom1_Context=D1:RE\nCustom1_Trigger=M1:MOM\nCustomSignals_D1=RE\nCustomSignals_M1=MOM\n','CUSTOM_SLOT_1:SIGNAL_UNAVAILABLE'),
  ('bad_universe','ExpectedValid=false\nCustomSymbolMode=2\nCustomSymbolList=GOLDTYPO\n','SYMBOL_UNRESOLVED:GOLDTYPO'),
  ('explicit_universe','ExpectedValid=true\nCustomSymbolMode=2\nCustomSymbolList=GBPUSD, GBPUSD\n','')]:run(name,params,marker,expected_reason)
manifest={'build':'5.95','compiled':compiled,'runtime':results,'scope':'configuration helpers only; not full EA runtime/order execution'}
(evidence/('manifest_reinit.json' if a.only_reinit else 'manifest.json')).write_text(json.dumps(manifest,indent=2)+'\n');print('CONFIGURATION_NATIVE_PASS',flush=True)
