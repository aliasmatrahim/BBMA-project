from pathlib import Path

base = Path('blueprint/tools/apply_c044_step4_replay.py')
code = base.read_text(encoding='utf-8')
old = "replace_function('AdvanceC044OwnerEventOneCandle', advance_func)"
new = r'''advance_start = s.find('bool AdvanceC044OwnerEventOneCandle(')
if advance_start < 0:
    raise SystemExit('AdvanceC044OwnerEventOneCandle start not found')
advance_end = s.find('void AdvanceC044OwnerEventsForPair(', advance_start)
if advance_end < 0:
    raise SystemExit('AdvanceC044OwnerEventsForPair boundary not found')
s = s[:advance_start] + advance_func.rstrip() + '\n\n' + s[advance_end:]'''
if code.count(old) != 1:
    raise SystemExit('Step4 patcher Advance replacement anchor mismatch')
code = code.replace(old, new, 1)
exec(compile(code, str(base), 'exec'))
