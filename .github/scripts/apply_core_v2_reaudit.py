from pathlib import Path

SOURCE = Path('blueprint/source/BBMA_EA.mq4')
AUDIT = Path('blueprint/P3_CORE_V2_STRATEGY_REAUDIT_20260822.md')
QUEUE = Path('blueprint/MASTER_QUEUE.md')
CURRENT = Path('blueprint/CURRENT.md')

s = SOURCE.read_text(encoding='utf-8')

required = {
    'F1 canonical MHV state': 'MLV_FORMATION_ESTABLISHED',
    'F1 frozen marked body': 'FrozenMarkedBody',
    'F2 reversal maturity': 'EXT_MAT_REVERSAL_CONFIRMED',
    'F2 retest ready': 'EXT_MAT_RETEST_READY',
    'F3 Type1 ranging': 'TYPE1_CTX_RANGING',
    'F4 H4 owner': 'H4_OWNER_ACTIVE',
    'F4 standalone owner gate': 'h4Owner.Direction != reEntry.Direction',
    'F5 reachable flat geometry': 'bool topHorizontal',
    'F5 three-line horizontal': 'bool lowHorizontal',
    'F6 next-candle metadata': 'reEntry.EntryCandle = (sourceTfSeconds > 0)',
    'M10 CSM': 'bool DetectCSM(string pair, int timeframe, ENUM_DIRECTION direction, int shift)',
    'Mode1 standalone candidate': 'BuildConfirmedReEntryCandidate(',
    'REM/RRE/REE builder': 'BuildPossibleCombinations(rem, rre, ree',
    'M15 atomic authority': 'PriorityEngine_Atomic(allCandidates, allCandidateCount, decision, conflict);',
    'M16 atomic invalidation': 'InvalidationEngine_Atomic(pairIndex, decision, conflict);',
}
missing = [name for name, token in required.items() if token not in s]
if missing:
    raise SystemExit('Core re-audit invariant(s) missing: ' + ', '.join(missing))

if 'reEntry.EntryCandle = data.candle_time;' in s:
    raise SystemExit('F6 legacy confirmation==entry metadata still present')
if 'else if(widthRatio >= 0.9 && widthRatio <= 1.1)' in s:
    raise SystemExit('F5 legacy unreachable BB_FLAT branch still present')

AUDIT.write_text('''# P3 Strategy Core V2 — Integrated Static Re-Audit after F1–F6\n\nDate: 2026-08-22\nBranch: `blueprint-dev`\nStatus: **STATIC CORE RE-AUDIT PASS — NATIVE METAEDITOR COMPILE + RUNTIME TRACES STILL REQUIRED; F7 REMAINS SOURCE-GOVERNANCE ONLY**\n\n## Scope\nRe-audit of the current integrated source after implementing/resolving CORE-V2-F1 through CORE-V2-F6. Baseline remains `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`. This is a static strategy-semantic audit, not a claim of live MT4 closure.\n\n## Re-audit result by original finding\n| ID | Area | Re-audit result |\n|---|---|---|\n| CV2-01 | M06 indicator/data producer | **MATCH — unchanged** |\n| CV2-02 | M07 flat/horizontal BB | **FIXED by F5 / static PASS** |\n| CV2-03 | Extreme component maturity | **FIXED by F2 / static PASS** |\n| CV2-04 | MHV outer-BB invalidation | **FIXED by F1 / static PASS** |\n| CV2-05 | MHV body/retest construction | **FIXED by F1 canonical lifecycle / static PASS** |\n| CV2-06 | duplicate MHV/MLV semantics | **CANONICALIZED by F1 / static PASS** |\n| CV2-07 | M10 CSM/eCSD/CSD | **MATCH — unchanged** |\n| CV2-08 | M11 EMA helper | **DORMANT / not used as final Core gate** |\n| CV2-09 | Re-Entry Type 1 context | **FIXED by F3 / static PASS** |\n| CV2-10 | Re-Entry Types 2–4 | **MATCH — unchanged** |\n| CV2-11 | first validation / second entry timing | **STATIC VERIFIED by F6; no extra delay; runtime OrderOpenTime trace pending** |\n| CV2-12 | standalone H1 higher-TF context | **FIXED by F4 H4 owner / static PASS** |\n| CV2-13 | REM/RRE/REE signatures | **MATCH — preserved** |\n| CV2-14 | M15 EntryMode/candidate authority | **MATCH — preserved** |\n| CV2-15 | M16 owner-aware invalidation/freshness | **MATCH at architecture level; upstream F1/F2/F3 defects now statically resolved** |\n| CV2-16 | M17 SL/TP provenance | **UNCHANGED: OUTSIDE CORE / F7 SOURCE-GOVERNANCE DECISION, not a proven Core code bug** |\n\n## Integrated invariants confirmed\n- F1 canonical MHV/MLV owner-state markers and frozen marked-body lifecycle are present.\n- F2 Extreme reversal-confirmed and retest-ready maturity stages are present.\n- F3 Type 1 structural ranging state is present.\n- F4 recovered H4 authoritative owner and same-direction standalone H1 gate are present.\n- F5 `BB_FLAT` is reachable via geometric three-line horizontal classification; legacy unreachable near-unity branch is gone.\n- F6 validation/entry metadata no longer identifies the same candle; runtime still executes without an added full-candle wait.\n- M10 directional Momentum remains independently defined; F5 did not add a new trading filter.\n- Exact REM/RRE/REE combination builder remains in place.\n- M15 remains sole atomic final signal authority and M16 remains atomic invalidation/freshness authority.\n\n## Static conclusion\nNo remaining **known Strategy-Core semantic code defect** from CV2-01 through CV2-15 is open at static level. The integrated F1–F6 code must still pass native MetaEditor compilation and targeted runtime lifecycle/timing traces before live closure.\n\nCV2-16/F7 is intentionally not converted into a code defect: current executable SL/TP provenance remains project policy (`FORUM_SUPPORTED` / `EA_SAFETY`) unless governance chooses to require stronger Strategy-Core source certification.\n\n## Next gate\nProceed to **P3-M1 — Mode 1 Official BBMA Compliance Audit** end-to-end. Do not add strategy filters or alter source semantics unless that audit produces evidence-backed deviations.\n''', encoding='utf-8')

q = QUEUE.read_text(encoding='utf-8')
marker = '## Priority queue\n'
if marker not in q:
    raise SystemExit('MASTER_QUEUE priority marker missing')
summary = '''\n### CORE-V2 integrated re-audit after F1–F6\nStatus: **STATIC RE-AUDIT PASS — METAEDITOR/RUNTIME EVIDENCE PENDING**\nRecord: `blueprint/P3_CORE_V2_STRATEGY_REAUDIT_20260822.md`\nResult: original CV2-01..CV2-15 findings are either MATCH/DORMANT or statically resolved by F1–F6. CV2-16 remains F7 source-governance only, not a proven Strategy-Core code defect.\nNext strategy gate: **P3-M1 Mode 1 Official BBMA Compliance Audit**.\n\n'''
if '### CORE-V2 integrated re-audit after F1–F6' not in q:
    q = q.replace(marker, marker + summary, 1)
QUEUE.write_text(q, encoding='utf-8')

c = CURRENT.read_text(encoding='utf-8')
overlay = '''\n\n# 2026-08-22 Strategy Core V2 Integrated Re-Audit Overlay\n- **Integrated F1–F6 static Strategy-Core re-audit: PASS.**\n- Original CV2-01..CV2-15 findings are now MATCH/DORMANT or statically resolved; native MetaEditor compile and runtime traces remain pending.\n- CV2-16/F7 remains a source-governance decision only and is not treated as a proven Core code defect.\n- **Next strategy gate: P3-M1 Mode 1 Official BBMA Compliance Audit.**\n- Audit record: `blueprint/P3_CORE_V2_STRATEGY_REAUDIT_20260822.md`.\n'''
if '# 2026-08-22 Strategy Core V2 Integrated Re-Audit Overlay' not in c:
    c += overlay
CURRENT.write_text(c, encoding='utf-8')
