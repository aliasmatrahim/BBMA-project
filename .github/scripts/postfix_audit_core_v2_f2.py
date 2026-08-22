from pathlib import Path

SOURCE = Path('blueprint/source/BBMA_EA.mq4')
AUDIT = Path('blueprint/CORE_V2_F2_IMPLEMENTATION_AUDIT.md')

s = SOURCE.read_text(encoding='utf-8')

# Remove the one accidental duplicate assignment introduced by the first patch.
dup = '      h4_extreme = h4ExtremeSnapshot;\n      h4_extreme = h4ExtremeSnapshot;\n'
if dup in s:
    s = s.replace(dup, '      h4_extreme = h4ExtremeSnapshot;\n', 1)

# Keep ownership comments aligned with the actual F2 split.
old_comment = '''   // M16 persistent validity overlay for source-detected Extremes.\n   // M08 remains the detector; M16 owns temporal invalidation/expiry only.\n'''
new_comment = '''   // M16 executable-component freshness/identity overlay for mature Extremes.\n   // M08 owns RAW/reversal/retest maturity and strategy invalidation.\n'''
if old_comment in s:
    s = s.replace(old_comment, new_comment, 1)


def block(start: str, end: str) -> str:
    a = s.find(start)
    if a < 0:
        raise SystemExit(f'missing block start: {start}')
    b = s.find(end, a)
    if b < 0:
        raise SystemExit(f'missing block end: {end}')
    return s[a:b]

# F2 static regression invariants.
if s.count('signal.Type = SIGNAL_EXTREME;') != 1:
    raise SystemExit('SIGNAL_EXTREME must have exactly one executable export assignment')
if s.count('DetectExtreme(') != 3:
    raise SystemExit('DetectExtreme must be definition + H1 RAW call + H4 RAW call only')
if s.count('ENUM_EXTREME_MATURITY UpdateExtremeLifecycle(') != 1:
    raise SystemExit('UpdateExtremeLifecycle definition count drift')
if s.count('UpdateExtremeLifecycle(g_pair_states') != 4:
    raise SystemExit('UpdateExtremeLifecycle expected H1 BUY/SELL + H4 BUY/SELL call sites')
if s.count('bool ExportReversalConfirmedExtremeSignal(') != 1:
    raise SystemExit('mature Extreme exporter definition count drift')
if s.count('ExportReversalConfirmedExtremeSignal(\n            g_pair_states') != 4:
    raise SystemExit('mature Extreme exporter expected H1 BUY/SELL + H4 BUY/SELL call sites')
if s.count('IsCombinationSignalReady(h1_extreme, SIGNAL_EXTREME, PERIOD_H1)') != 3:
    raise SystemExit('H1 Extreme combination signature drift')
if s.count('IsCombinationSignalReady(h4_extreme, SIGNAL_EXTREME, PERIOD_H4)') != 1:
    raise SystemExit('H4 Extreme combination signature drift')
if 'h1AnyCSMSnapshot' in s or 'h4AnyCSMSnapshot' in s:
    raise SystemExit('legacy generic any-CSM Extreme invalidation path remains')
if s.count('      h4_extreme = h4ExtremeSnapshot;\n') != 1:
    raise SystemExit('H4 Extreme snapshot assignment must occur exactly once')

raw_detector = block(
    'bool DetectExtreme(string pair, ENUM_DIRECTION direction, TimeframeData &data, BollingerBand &band)\n{',
    'void ResetExtremeLifecycle('
)
if 'data.close > band.TOP_BB' in raw_detector or 'data.close < band.LOW_BB' in raw_detector:
    raise SystemExit('RAW detector still contains close-inside/close-outside maturity gating')

lifecycle = block(
    'ENUM_EXTREME_MATURITY UpdateExtremeLifecycle(',
    'bool ExportReversalConfirmedExtremeSignal('
)
# MaxWaitBars_Extreme may appear in explanatory comments, but must not be used
# as executable lifecycle expiry/reset logic inside M08.
if 'MaxWaitBars_Extreme *' in lifecycle or 'IsExtremeStateExpired' in lifecycle:
    raise SystemExit('MaxWaitBars_Extreme leaked into F2 strategy lifecycle')
for required in [
    'if(direction == DIR_SELL) return (data.close < data.open);',
    'if(direction == DIR_BUY)  return (data.close > data.open);',
    'if(extreme.Direction == DIR_SELL) return (data.close > extreme.PreviousClose);',
    'if(extreme.Direction == DIR_BUY)  return (data.close < extreme.PreviousClose);',
    'extreme.FrozenBodyAnchor = extreme.ProvisionalBodyAnchor;',
    'if(IsExtremeLifecycleInvalidation(pair, direction, data, band))',
]:
    if required not in s:
        raise SystemExit(f'missing resolved F2 predicate: {required}')

# Basic lexical delimiter audit (ignores strings and comments) to catch accidental
# structural damage before native MetaEditor compilation.
def strip_noncode(text: str) -> str:
    out = []
    i = 0
    n = len(text)
    state = 'code'
    while i < n:
        c = text[i]
        nxt = text[i + 1] if i + 1 < n else ''
        if state == 'code':
            if c == '"':
                state = 'string'; out.append(' ')
            elif c == '/' and nxt == '/':
                state = 'line'; out.extend('  '); i += 1
            elif c == '/' and nxt == '*':
                state = 'block'; out.extend('  '); i += 1
            else:
                out.append(c)
        elif state == 'string':
            if c == '\\' and nxt:
                out.extend('  '); i += 1
            elif c == '"':
                state = 'code'; out.append(' ')
            else:
                out.append('\n' if c == '\n' else ' ')
        elif state == 'line':
            if c == '\n':
                state = 'code'; out.append('\n')
            else:
                out.append(' ')
        elif state == 'block':
            if c == '*' and nxt == '/':
                state = 'code'; out.extend('  '); i += 1
            else:
                out.append('\n' if c == '\n' else ' ')
        i += 1
    if state in ('string', 'block'):
        raise SystemExit(f'unterminated lexical state: {state}')
    return ''.join(out)

code = strip_noncode(s)
for op, cl, name in [('{', '}', 'brace'), ('(', ')', 'paren'), ('[', ']', 'bracket')]:
    depth = 0
    for ch in code:
        if ch == op:
            depth += 1
        elif ch == cl:
            depth -= 1
            if depth < 0:
                raise SystemExit(f'unbalanced {name}: premature close')
    if depth != 0:
        raise SystemExit(f'unbalanced {name}: final depth {depth}')

SOURCE.write_text(s, encoding='utf-8')

text = AUDIT.read_text(encoding='utf-8')
text = text.replace(
    'Status: **IMPLEMENTED / STATIC AUDIT PASS — NATIVE METAEDITOR COMPILE + REGRESSION/RUNTIME STILL REQUIRED**',
    'Status: **IMPLEMENTED / STATIC REGRESSION PASS — NATIVE METAEDITOR COMPILE + RUNTIME TRACE STILL REQUIRED**'
)
text = text.replace(
    '## Remaining verification\n1. Native MetaEditor compile must report **0 errors / 0 warnings**.\n2. Regression/static re-audit should prove RAW Extreme never reaches M13/M14/M15 as an executable component.\n3. Runtime trace should cover:',
    '## Static regression closure\nPost-implementation re-audit additionally verified:\n- the full source has balanced braces/parentheses/brackets after stripping comments/strings;\n- only one `SIGNAL_EXTREME` executable export assignment exists, inside the reversal-confirmed exporter;\n- `DetectExtreme()` has only the definition plus H1/H4 RAW call sites;\n- `MaxWaitBars_Extreme` is not used as executable expiry/reset logic inside `UpdateExtremeLifecycle()`;\n- H1/H4 exact combination signatures remain unchanged;\n- duplicate H4 snapshot assignment from the first patch pass was removed.\n\n## Remaining verification\n1. Native MetaEditor compile must report **0 errors / 0 warnings**.\n2. Runtime trace should cover:'
)
text = text.replace(
    '4. F1 implementation must consume the underlying F2 lifecycle',
    '3. F1 implementation must consume the underlying F2 lifecycle'
)
AUDIT.write_text(text, encoding='utf-8')

print('CORE-V2-F2 post-fix/static regression: PASS')
