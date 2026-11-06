from pathlib import Path
import re
s=(Path(__file__).resolve().parents[2]/'blueprint/source/BBMA_EA.mq4').read_text(encoding='utf-8-sig')
m=re.search(r'bool IsMHVRetestInteraction\(MLVData &mlv, TimeframeData &data\)\s*\{(.*?)\n\}',s,re.S)
assert m, 'production function missing'
f=m.group(1)
assert 'DIR_BUY || mlv.Direction == DIR_SELL' in f
expr=re.search(r'return \((data\.low <= mlv\.FrozenMarkedBody && data\.high >= mlv\.FrozenMarkedBody)\);',f)
assert expr, 'production range predicate missing'
# Evaluate the exact extracted C-style predicate with fixture values.
pred=expr.group(1).replace('data.low','low').replace('data.high','high').replace('mlv.FrozenMarkedBody','body').replace('&&','and')
cases=[(99,101,True),(100,101,True),(99,100,True),(101,102,False),(98,99,False)]
for direction in ('buy','sell'):
 for low,high,expected in cases:
  actual=eval(pred,{'__builtins__':{}},dict(low=low,high=high,body=100))
  assert actual==expected,(direction,low,high,expected,actual)
print('PASS 10 production-predicate boundary cases')
