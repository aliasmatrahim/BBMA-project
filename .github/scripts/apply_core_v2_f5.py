from pathlib import Path
import re

SOURCE = Path('blueprint/source/BBMA_EA.mq4')
AUDIT = Path('blueprint/CORE_V2_F5_IMPLEMENTATION_AUDIT.md')
QUEUE = Path('blueprint/MASTER_QUEUE.md')
CURRENT = Path('blueprint/CURRENT.md')

s = SOURCE.read_text(encoding='utf-8')


def replace_once(old: str, new: str, label: str):
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 occurrence, found {count}')
    s = s.replace(old, new, 1)


old_detector = '''ENUM_BB_STATE DetectBBState(BollingerBand &current, BollingerBand &previous)\n{\n   if(current.Width <= 0 || previous.Width <= 0) return BB_NONE;\n   \n   double widthRatio = current.Width / previous.Width;\n   \n   if(widthRatio < 0.9)\n      return BB_SQUEEZE;\n   else if(widthRatio > 1.1)\n      return BB_EXPANDING;\n   else if(widthRatio >= 0.9 && widthRatio <= 1.1)\n      return BB_CONTRACTING;\n   return BB_FLAT;\n}\n'''

new_detector = '''ENUM_BB_STATE DetectBBState(BollingerBand &current, BollingerBand &previous,\n                            double horizontalTolerance)\n{\n   if(current.Width <= 0 || previous.Width <= 0) return BB_NONE;\n   if(current.TOP_BB <= 0 || current.MID_BB <= 0 || current.LOW_BB <= 0 ||\n      previous.TOP_BB <= 0 || previous.MID_BB <= 0 || previous.LOW_BB <= 0)\n      return BB_NONE;\n\n   // CORE-V2-F5: flat/horizontal is a geometric BB-line state, not the\n   // leftover branch of width-ratio classification.  Tolerance is exactly one\n   // broker point supplied by BuildBBShapeState(), used only as numerical\n   // equality tolerance rather than a trading/strategy threshold.\n   if(horizontalTolerance > 0)\n   {\n      bool topHorizontal =\n         (MathAbs(current.TOP_BB - previous.TOP_BB) <= horizontalTolerance);\n      bool midHorizontal =\n         (MathAbs(current.MID_BB - previous.MID_BB) <= horizontalTolerance);\n      bool lowHorizontal =\n         (MathAbs(current.LOW_BB - previous.LOW_BB) <= horizontalTolerance);\n\n      if(topHorizontal && midHorizontal && lowHorizontal)\n         return BB_FLAT;\n   }\n\n   double widthRatio = current.Width / previous.Width;\n\n   // Preserve the pre-existing project shape thresholds outside the repaired\n   // flat branch; F5 does not redefine squeeze/expansion strategy semantics.\n   if(widthRatio < 0.9)\n      return BB_SQUEEZE;\n   if(widthRatio > 1.1)\n      return BB_EXPANDING;\n\n   return BB_CONTRACTING;\n}\n'''
replace_once(old_detector, new_detector, 'M07 DetectBBState')

old_call = '''   current.State = DetectBBState(current, previous);\n   return (current.State != BB_NONE);\n'''
new_call = '''   double pointTolerance = GetPointSize(pair);\n   if(pointTolerance <= 0)\n   {\n      current.State = BB_NONE;\n      return false;\n   }\n\n   current.State = DetectBBState(current, previous, pointTolerance);\n   return (current.State != BB_NONE);\n'''
replace_once(old_call, new_call, 'BuildBBShapeState point-tolerance wiring')

# Contract-specific static regression.
required = [
    'ENUM_BB_STATE DetectBBState(BollingerBand &current, BollingerBand &previous,',
    'bool topHorizontal',
    'bool midHorizontal',
    'bool lowHorizontal',
    'return BB_FLAT;',
    'double pointTolerance = GetPointSize(pair);',
    'DetectBBState(current, previous, pointTolerance)',
    'bool DetectCSM(string pair, int timeframe, ENUM_DIRECTION direction, int shift)',
    'H4DirectionalOwner   h4_direction_owner;',
    'MLV_FORMATION_ESTABLISHED',
    'EXT_MAT_REVERSAL_CONFIRMED',
    'TYPE1_CTX_RANGING',
]
for token in required:
    if token not in s:
        raise SystemExit(f'F5 invariant missing: {token}')

if 'else if(widthRatio >= 0.9 && widthRatio <= 1.1)' in s:
    raise SystemExit('legacy all-covering near-unity BB branch remains')
if s.count('DetectBBState(current, previous, pointTolerance)') != 1:
    raise SystemExit('M07 BB-state call-site count mismatch')

# F5 is a support-state repair only; do not couple M10 CSM to BB_FLAT.
m10_a = s.find('bool DetectCSM(string pair, int timeframe, ENUM_DIRECTION direction, int shift)')
m10_b = s.find('bool CandleBodyCrossesLevel', m10_a)
if m10_a < 0 or m10_b < 0:
    raise SystemExit('M10 DetectCSM boundary unavailable')
if 'BB_FLAT' in s[m10_a:m10_b]:
    raise SystemExit('F5 must not add a BB_FLAT trading gate to source-aligned DetectCSM')

# Basic lexical balance, ignoring comments/strings approximately.
def strip_cpp(text):
    text = re.sub(r'/\\*.*?\\*/', '', text, flags=re.S)
    text = re.sub(r'//.*', '', text)
    text = re.sub(r'"(?:\\\\.|[^"\\\\])*"', '""', text)
    return text

clean = strip_cpp(s)
for a, b, name in [('{','}','brace'), ('(',')','paren'), ('[',']','bracket')]:
    if clean.count(a) != clean.count(b):
        raise SystemExit(f'lexical {name} imbalance: {clean.count(a)} vs {clean.count(b)}')

SOURCE.write_text(s, encoding='utf-8')

AUDIT.write_text('''# CORE-V2-F5 — M07 Flat/Horizontal Bollinger-Band State Repair\n\nDate: 2026-08-22\nStatus: **IMPLEMENTED / STATIC REGRESSION PASS — NATIVE METAEDITOR COMPILE + RUNTIME TRACE STILL REQUIRED**\nBranch: `blueprint-dev`\n\n## Scope\nRepairs CV2-02 only: `BB_FLAT` was unreachable because every valid positive width ratio was already consumed by squeeze/expanding/contracting branches.\n\n## Source rule preserved\nThe accepted Strategy Core says an outside-BB close under a flat/horizontal BB is not directional Momentum/CSM. The source does not provide a numeric flatness formula. F5 therefore implements only a minimal geometric state mapping and does **not** add a new trading filter.\n\n## Deterministic mapping\n- `BB_FLAT` is now a real geometric state: Top BB, Mid BB and Low BB must each remain horizontal versus the immediately previous closed source-TF candle within **one broker point**.\n- One broker point is used only as numerical equality tolerance; it is not a pip/ATR/volatility threshold and does not become an entry rule.\n- The existing project shape thresholds are otherwise preserved: width ratio `< 0.9` -> `BB_SQUEEZE`; `> 1.1` -> `BB_EXPANDING`; remaining non-flat valid states -> `BB_CONTRACTING`.\n- Invalid/zero point or invalid BB geometry fails to `BB_NONE`.\n\n## Important boundary\nM10 `DetectCSM()` is intentionally unchanged. It already independently requires outside close + width expansion + directional BB movement. F5 repairs M07 state semantics so later modules can safely consume `BB_FLAT`; it does not claim that M07 is the current CSM authority.\n\n## Static regression\n- the old all-covering `0.9..1.1 -> BB_CONTRACTING` branch is removed;\n- `BB_FLAT` is reachable before width-ratio classification;\n- Top/Mid/Low horizontal checks are all required;\n- M10 contains no newly introduced `BB_FLAT` gate;\n- F1/F2/F3/F4 structural markers remain present;\n- source lexical brace/parenthesis/bracket sanity passes.\n\n## Evidence classification\n- flat/horizontal BB distinction and its Momentum meaning: **DIRECT / STRONGLY CORROBORATED SOURCE PRINCIPLE**;\n- exact one-broker-point three-line horizontal predicate: **MINIMAL PROJECT NUMERICAL MAPPING**, not a verbatim Oma Ally formula.\n\n## Remaining verification\n1. Native MetaEditor compile must report **0 errors / 0 warnings** for integrated F1-F5 source.\n2. Runtime trace should show at least one `BB_FLAT` classification on genuinely horizontal closed BB geometry and confirm non-flat near-equal-width sloping BB is not mislabeled flat.\n3. Proceed to CORE-V2-F6 timing verification before re-running the full Strategy Core audit.\n''', encoding='utf-8')

q = QUEUE.read_text(encoding='utf-8')
old_f5 = '''#### CORE-V2-F5 — M07 flat/horizontal BB state\nPriority: MEDIUM\nStatus: QUEUED\nSource: `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-02\nCurrent issue: `BB_FLAT` is effectively unreachable in the current ratio branching. M10 CSM remains independently source-aligned, so this is not currently a proven entry leak, but the state classification must be repaired before other modules depend on it.\n'''
new_f5 = '''#### CORE-V2-F5 — M07 flat/horizontal BB state\nPriority: MEDIUM\nStatus: **CODE IMPLEMENTED / STATIC REGRESSION PASS — NATIVE METAEDITOR COMPILE + RUNTIME TRACE PENDING**\nSource: `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-02\nImplementation record: `blueprint/CORE_V2_F5_IMPLEMENTATION_AUDIT.md`\nResolved mapping: `BB_FLAT` is now a reachable geometric three-line horizontal state using one broker point only as numerical equality tolerance. Existing squeeze/expanding width thresholds are preserved; remaining non-flat valid near-width states remain contracting. M10 CSM remains independently source-aligned and was not changed by F5.\nNext action for F5: native MetaEditor compile and focused runtime BB-shape trace; proceed to F6 timing verification before full Core re-audit.\n'''
if old_f5 not in q:
    raise SystemExit('F5 queue block not found')
q = q.replace(old_f5, new_f5, 1)
QUEUE.write_text(q, encoding='utf-8')

c = CURRENT.read_text(encoding='utf-8')
append = '''\n\n# 2026-08-22 CORE-V2-F5 Implementation Overlay\n- **CORE-V2-F5 M07 BB-flat classification: CODE IMPLEMENTED / STATIC REGRESSION PASS.**\n- `BB_FLAT` is no longer an unreachable leftover branch; it is a geometric Top/Mid/Low horizontal state with one broker point used only as numerical equality tolerance.\n- M10 CSM logic is unchanged; F5 is a Core-support state repair, not a new execution filter.\n- F1-F5 integrated native MetaEditor compile/runtime verification remains pending.\n- **Highest-priority next Core gate: CORE-V2-F6 Re-Entry validation/entry timing verification, then rerun Strategy Core V2 audit.**\n'''
if '# 2026-08-22 CORE-V2-F5 Implementation Overlay' not in c:
    c += append
CURRENT.write_text(c, encoding='utf-8')
