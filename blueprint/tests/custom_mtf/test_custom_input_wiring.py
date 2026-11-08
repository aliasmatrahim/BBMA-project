from pathlib import Path
s=Path('blueprint/source/BBMA_EA.mq4').read_text()
assert '#include "custom_mtf/CustomInputs.mqh"' in s, 'custom inputs not integrated'
start=s.index('bool ValidateInputParameters()');end=s.index('\n}',start)
b=s[start:end]
assert 'InitializeCustomInputs(' in b, 'custom initializer not wired'
assert s.index('ValidateInputParameters()',s.index('int OnInit()')) < s.index('InitializeEA()',s.index('int OnInit()'))
print('CUSTOM_INPUT_INIT_WIRING_PASS')
