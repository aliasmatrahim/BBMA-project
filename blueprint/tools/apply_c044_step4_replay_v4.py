from pathlib import Path

base = Path('blueprint/tools/apply_c044_step4_replay.py')
code = base.read_text(encoding='utf-8')
start = code.find('def find_function_span(text, name):')
end = code.find('def replace_function(name, new_text):', start)
if start < 0 or end < 0:
    raise SystemExit('base patcher parser boundary not found')

bounded = r'''def find_function_span(text, name):
    starts = {
        'ResetC044TradeState': 'void ResetC044TradeState(',
        'C044CheckpointBase': 'string C044CheckpointBase(',
        'ClearC044Checkpoint': 'void ClearC044Checkpoint(',
        'SaveC044Checkpoint': 'bool SaveC044Checkpoint(',
        'LoadC044Checkpoint': 'bool LoadC044Checkpoint(',
        'InitializeC044TradeStateFromDecision': 'bool InitializeC044TradeStateFromDecision(',
        'IsC044SameDirectionReEntryEvent': 'bool IsC044SameDirectionReEntryEvent(',
        'IsC044OppositeExtremeSupersessionEvent': 'bool IsC044OppositeExtremeSupersessionEvent(',
        'ProcessC044OwnerClosedCandle': 'bool ProcessC044OwnerClosedCandle(',
        'AdvanceC044OwnerEventOneCandle': 'bool AdvanceC044OwnerEventOneCandle(',
    }
    nexts = {
        'ResetC044TradeState': 'bool IsValidC044OwnerTimeframe(',
        'C044CheckpointBase': 'void ClearC044Checkpoint(',
        'ClearC044Checkpoint': 'bool SaveC044Checkpoint(',
        'SaveC044Checkpoint': 'bool LoadC044Checkpoint(',
        'LoadC044Checkpoint': 'string H4OwnerGVBase(',
        'InitializeC044TradeStateFromDecision': 'string C044CheckpointBase(',
        'IsC044SameDirectionReEntryEvent': 'bool IsC044OppositeExtremeSupersessionEvent(',
        'IsC044OppositeExtremeSupersessionEvent': 'bool IsC044DirectionSideOuterBBTest(',
        'ProcessC044OwnerClosedCandle': 'bool AdvanceC044OwnerEventOneCandle(',
        'AdvanceC044OwnerEventOneCandle': 'void AdvanceC044OwnerEventsForPair(',
    }
    if name not in starts:
        raise SystemExit(f'no deterministic boundary registered for: {name}')
    a = text.find(starts[name])
    if a < 0:
        raise SystemExit(f'function start not found: {name}')
    b = text.find(nexts[name], a + len(starts[name]))
    if b < 0:
        raise SystemExit(f'function next boundary not found: {name}')
    return a, b

'''
code = code[:start] + bounded + code[end:]
exec(compile(code, str(base), 'exec'))
