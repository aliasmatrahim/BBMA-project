from pathlib import Path

p = Path('blueprint/source/BBMA_EA.mq4')
s = p.read_text(encoding='utf-8')

block = '''   if(DebugLevel >= DBG_TRADE)\n   {\n      Print("[M17-SL][LOT] Pair=", pair,\n            " Dir=", EnumToString(decision.Direction),\n            " Entry=", DoubleToString(decision.EntryPrice, snapshot.Digits),\n            " FinalSL=", DoubleToString(decision.StopLoss, snapshot.Digits),\n            " FinalTP=", DoubleToString(decision.TakeProfit, snapshot.Digits),\n            " FinalLot=", DoubleToString(lot, snapshot.LotDigits));\n   }\n\n'''

if block not in s:
    raise SystemExit('protected-flow telemetry block not found exactly once')
if s.count(block) != 1:
    raise SystemExit(f'unexpected protected-flow telemetry count: {s.count(block)}')

s = s.replace(block, '', 1)
if '[M17-SL][LOT]' in s:
    raise SystemExit('M17-SL LOT marker still present after removal')

# Preserve approved M17 structural change.
for marker in [
    'Version 4.5.2 - M17 Structural SL Normalization',
    'M17-SLRANGE-01',
    'ResolveSourceOwnedStructuralAnchor',
    'MathCeil(rawSpreadPips - 0.000000001)',
    'brokerSL += roundedSpreadBufferPips * pipValue',
    '[M17-SL][STRUCT]',
]:
    if marker not in s:
        raise SystemExit(f'required M17 marker lost: {marker}')

p.write_text(s, encoding='utf-8', newline='\n')
print('Removed non-essential telemetry from protected preflight flow')
