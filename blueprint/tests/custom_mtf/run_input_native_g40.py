from pathlib import Path
import subprocess
r=Path(r'D:\BBMA\MT4_CustomMTF_302_Unit')
h='#property strict\n#include "..\\\\..\\\\m10-stage\\\\blueprint\\\\source\\\\custom_mtf\\\\CustomInputs.mqh"\ninput bool ExpectedValid=true;\nint OnInit(){string reason;bool v=InitializeCustomInputs(reason);Print("[INPUT_ADMISSION] expected=",ExpectedValid," actual=",v," reason=",reason," passed=",v==ExpectedValid);return v==ExpectedValid?INIT_SUCCEEDED:INIT_FAILED;}\nvoid OnTick(){}\n'
(r/'MQL4/Experts/CustomInputHarness.mq4').write_text(h)
log=r/'evidence/input_runtime_compile.log'
subprocess.run([str(r/'metaeditor.exe'),'/compile:'+str(r/'MQL4/Experts/CustomInputHarness.mq4'),'/log:'+str(log)],timeout=60)
s=log.read_bytes().decode('utf-16');print(s,flush=True);assert '0 errors, 0 warnings' in s
for name,params in [('default','ExpectedValid=true\n'),('invalid','ExpectedValid=false\nCustom1_Enable=true\nCustom1_Context=\nCustom1_Trigger=M1:MOM\n'),('unavailable','ExpectedValid=false\nCustom1_Enable=true\nCustom1_Context=D1:RE\nCustom1_Trigger=M1:MOM\nCustomSignals_D1=RE\nCustomSignals_M1=MOM\n')]:
 (r/'tester'/('input_'+name+'.set')).write_text(params)
 cfg=(r/'config/parser_green.ini').read_text().replace('CustomFormulaHarness','CustomInputHarness').replace('parser_green.html','input_'+name+'.html')+'\nTestExpertParameters=input_'+name+'.set\n'
 f=r/'config'/('input_'+name+'.ini');f.write_text(cfg)
 p=subprocess.Popen([str(r/'terminal.exe'),'/portable',str(f)],cwd=r);print(name,p.pid,flush=True);p.wait(timeout=60)
print('INPUT_MATRIX_FINISHED',flush=True)
