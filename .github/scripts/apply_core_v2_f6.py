from pathlib import Path

SOURCE = Path('blueprint/source/BBMA_EA.mq4')
AUDIT = Path('blueprint/CORE_V2_F6_TIMING_VERIFICATION_AUDIT.md')
QUEUE = Path('blueprint/MASTER_QUEUE.md')
CURRENT = Path('blueprint/CURRENT.md')

s = SOURCE.read_text(encoding='utf-8')

old = '''   reEntry.ConfirmationBar = data.barIndex;\n   reEntry.ConfirmationCandle = data.candle_time;\n   reEntry.EntryCandle = data.candle_time;\n   reEntry.EntryPrice = data.close;\n'''
new = '''   reEntry.ConfirmationBar = data.barIndex;\n   reEntry.ConfirmationCandle = data.candle_time;\n\n   // CORE-V2-F6 metadata correction only: the closed source-TF candle is the\n   // validation candle; execution is eligible in the immediately following\n   // source-TF candle.  No extra candle delay is introduced.\n   int sourceTfSeconds = GetTimeframeSeconds(data.timeframe);\n   reEntry.EntryCandle = (sourceTfSeconds > 0)\n                         ? data.candle_time + sourceTfSeconds\n                         : 0;\n   reEntry.EntryPrice = data.close;\n'''
if s.count(old) != 1:
    raise SystemExit(f'F6 confirmation metadata anchor expected once, found {s.count(old)}')
s = s.replace(old, new, 1)

required = [
    'datetime GetLatestClosedCandleTime(string pair, int timeframe)',
    'snapshot.M15_CandleTime = GetLatestClosedCandleTime(pair, PERIOD_M15);',
    'if(decision.DecisionState == DEC_VALIDATED)\n      RunEntryPreflightAndExecute(decision, actual);',
    'ProcessEntry(decision, pair, snapshot, lot);',
    'int ticket = OrderSend(pair, direction, lot, executionPrice, Slippage,',
    'reEntry.ConfirmationCandle = data.candle_time;',
    'reEntry.EntryCandle = (sourceTfSeconds > 0)',
]
for token in required:
    if token not in s:
        raise SystemExit(f'F6 invariant missing: {token}')

if 'reEntry.EntryCandle = data.candle_time;' in s:
    raise SystemExit('legacy confirmation==entry metadata remains')

SOURCE.write_text(s, encoding='utf-8')

AUDIT.write_text('''# CORE-V2-F6 — Re-Entry Validation-Candle / Entry-Candle Timing Verification\n\nDate: 2026-08-22\nStatus: **STATIC TIMING VERIFIED / METADATA CORRECTED — NO EXTRA ENTRY DELAY ADDED; NATIVE METAEDITOR + RUNTIME ORDER-TIME TRACE STILL REQUIRED**\nBranch: `blueprint-dev`\n\n## Question\nFinale teaches: first Re-Entry candle validates; the second candle is the entry candle. The Core audit required proof before adding any delay.\n\n## Static execution-path proof\nThe integrated EA already implements the intended timing structurally:\n1. `GetLatestClosedCandleTime()` only returns a candle after its full timeframe duration has elapsed.\n2. M27 processes a pair only when a new **closed M15 candle** becomes available.\n3. H1/H4/D1 Re-Entry detection therefore consumes closed source-TF data; `ConfirmReEntryState()` records that closed candle as `ConfirmationCandle`.\n4. After M13/M14/M15/M16 validation, the same M27 pass may call `RunEntryPreflightAndExecute()` immediately.\n5. M22 ultimately calls `OrderSend()` at the current live broker price. Because the validation candle is already closed, that live execution necessarily occurs in the immediately following source-TF candle (subject to normal processing/broker delay).\n\nTherefore the existing closed-candle architecture already maps the source wording as:\n`FIRST CLOSED RE CANDLE = VALIDATION -> IMMEDIATELY FOLLOWING LIVE CANDLE = ENTRY WINDOW`.\n\nAdding another mandatory full-candle wait would create a third-candle execution and would be an unsupported extra delay.\n\n## Metadata correction\n`ReEntryData.EntryCandle` previously equalled `ConfirmationCandle`, which was misleading even though runtime execution timing was already next-candle. F6 changes **metadata only**:\n- `ConfirmationCandle = data.candle_time`;\n- `EntryCandle = data.candle_time + source timeframe seconds`.\n\n`EntryCandle` is not consumed by strategy eligibility or execution authority elsewhere, so this correction does not alter signal qualification, ordering, SL/TP, lot, risk or OrderSend timing.\n\n## Classification\n- first validation / second entry wording: **DIRECT FINALE CLARIFICATION**;\n- proof that current architecture already satisfies it: **PROJECT STATIC EXECUTION-MAPPING VERIFICATION**;\n- EntryCandle timestamp correction: **OBSERVABILITY/METADATA REPAIR ONLY**.\n\n## Remaining verification\n1. Native MetaEditor compile: **0 errors / 0 warnings** for integrated F1-F6 source.\n2. Runtime trace must record at least one Re-Entry where `ConfirmationCandle < OrderOpenTime()` and `OrderOpenTime()` falls inside the immediately following source-TF candle.\n3. Do not add an extra full-candle delay unless runtime evidence contradicts this mapping.\n\nSource basis: `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md` F-07 and `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-11.\n''', encoding='utf-8')

q = QUEUE.read_text(encoding='utf-8')
old_q = '''#### CORE-V2-F6 — Re-Entry validation-candle / entry-candle timestamp audit\nPriority: MEDIUM\nStatus: VERIFY, NO CODE CHANGE YET\nEvidence required: Re-Entry confirmation candle time, M15 decision time, and actual `OrderOpenTime()`.\nGoal: prove whether current closed-candle processing already means “first Re-Entry candle validates, next candle executes.” Do not insert an extra full-candle delay without evidence.\n'''
new_q = '''#### CORE-V2-F6 — Re-Entry validation-candle / entry-candle timestamp audit\nPriority: MEDIUM\nStatus: **STATIC TIMING VERIFIED / METADATA REPAIRED — NATIVE METAEDITOR + RUNTIME ORDER-TIME TRACE PENDING**\nImplementation/audit record: `blueprint/CORE_V2_F6_TIMING_VERIFICATION_AUDIT.md`\nResolved mapping: the closed source-TF Re-Entry candle is the validation candle; M27 may execute during the immediately following live source-TF candle. No extra full-candle delay is added. `ReEntryData.EntryCandle` metadata now identifies that immediately following candle rather than duplicating `ConfirmationCandle`.\nRuntime closure evidence still required: `ConfirmationCandle`, processing/decision time and actual `OrderOpenTime()`.\n'''
if old_q not in q:
    raise SystemExit('F6 queue block not found')
q = q.replace(old_q, new_q, 1)
QUEUE.write_text(q, encoding='utf-8')

c = CURRENT.read_text(encoding='utf-8')
overlay = '''\n\n# 2026-08-22 CORE-V2-F6 Timing Verification Overlay\n- **CORE-V2-F6 static timing verification: PASS; metadata repair applied.**\n- Closed Re-Entry source candle is the validation candle; execution remains eligible in the immediately following live source-TF candle.\n- No additional full-candle delay was introduced.\n- `ReEntryData.EntryCandle` no longer duplicates `ConfirmationCandle`; it points to the immediately following source-TF candle for observability.\n- Native MetaEditor compile and runtime `OrderOpenTime()` evidence remain required for final runtime closure.\n- **Next Core action: rerun Strategy Core V2 static audit against integrated F1-F6 source.**\n'''
if '# 2026-08-22 CORE-V2-F6 Timing Verification Overlay' not in c:
    c += overlay
CURRENT.write_text(c, encoding='utf-8')
