from pathlib import Path

SOURCE = Path('blueprint/source/BBMA_EA.mq4')
AUDIT = Path('blueprint/P3_M1_MODE1_OFFICIAL_BBMA_COMPLIANCE_AUDIT.md')
QUEUE = Path('blueprint/MASTER_QUEUE.md')
CURRENT = Path('blueprint/CURRENT.md')

s = SOURCE.read_text(encoding='utf-8')

required = {
    'EntryMode1 only standalone RE': 'if(EntryMode == 1)\n      return (candidate.SequenceType == SIGNAL_RE_ENTRY);',
    'standalone builder H1 only': 'if(reEntry.Timeframe != PERIOD_H1) return;',
    'standalone RE confirmed': 'if(reEntry.State != RE_STATE_CONFIRMED || !reEntry.IsValid) return;',
    'H4 owner recovery gate': 'if(!h4Owner.RecoveryComplete || !h4Owner.IsValid ||',
    'H4 owner direction gate': 'h4Owner.Direction != reEntry.Direction',
    'Type1 structural ranging': 'TYPE1_CTX_RANGING',
    'Type2 detector': 'bool DetectReEntry_Type2(',
    'Type3 detector': 'bool DetectReEntry_Type3(',
    'Type4 detector': 'bool DetectReEntry_Type4(',
    'Type3/4 precedence': 'Exact Type 3/4 precursor families own their setup before generic Type 1.',
    'M15 final authority': 'PriorityEngine_Atomic(allCandidates, allCandidateCount, decision, conflict);',
    'M16 owner invalidation': 'InvalidationEngine_Atomic(pairIndex, decision, conflict);',
    'M16 owner identity': 'IsDecisionComponentOwnerValid',
    'preflight only validated': 'if(decision.DecisionState == DEC_VALIDATED)\n      RunEntryPreflightAndExecute(decision, actual);',
    'F6 next candle metadata': 'reEntry.EntryCandle = (sourceTfSeconds > 0)',
}
missing = [name for name, token in required.items() if token not in s]
if missing:
    raise SystemExit('P3-M1 invariant(s) missing: ' + ', '.join(missing))

# Mode 1 must never directly admit combination or raw-signal families.
mode1_start = s.find('if(EntryMode == 1)')
mode2_start = s.find('if(EntryMode == 2)', mode1_start)
if mode1_start < 0 or mode2_start < 0:
    raise SystemExit('EntryMode branch boundaries unavailable')
mode1_block = s[mode1_start:mode2_start]
for forbidden in ['SIGNAL_REM', 'SIGNAL_RRE', 'SIGNAL_REE', 'SIGNAL_EXTREME', 'SIGNAL_MHV', 'SIGNAL_MLV', 'SIGNAL_CSD', 'SIGNAL_ECSD', 'SIGNAL_CSM']:
    if forbidden in mode1_block:
        raise SystemExit('Mode1 incorrectly admits ' + forbidden)

# Opposite eligible candidates must fail closed before execution.
if 'if(buyCount > 0 && sellCount > 0)' not in s or 'CONFLICT_DIRECTION_VIOLATION' not in s:
    raise SystemExit('M15 opposite-direction atomic conflict gate missing')

AUDIT.write_text('''# P3-M1 — Mode 1 Official BBMA Compliance Audit\n\nDate: 2026-08-22\nBranch: `blueprint-dev`\nStatus: **STATIC END-TO-END COMPLIANCE PASS — NATIVE METAEDITOR + RUNTIME MODE1 TRACE STILL REQUIRED**\n\n## Scope\nEntryMode 1 (`RE_ENTRY_ONLY`) was audited end-to-end against `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md` after integrated CORE-V2-F1 through F6 repairs.\n\nAudited path:\n`M06-M12 -> M13 -> M14 -> M15 -> M16 -> M17 -> M21 -> M19 -> M20 -> M22`\n\n## Static findings\n### 1. Candidate authority\nPASS. `EntryMode == 1` admits **only** `SIGNAL_RE_ENTRY`. REM/RRE/REE and raw Extreme/MHV/MLV/CSD/eCSD/CSM cannot become Mode-1 executable candidates.\n\n### 2. Re-Entry source/maturity\nPASS. Standalone candidate construction requires `RE_STATE_CONFIRMED`, valid direction, and specifically `PERIOD_H1`.\n\n### 3. Type 1\nPASS after F3. Type 1 uses prior BBMA direction/momentum ownership plus structural ranging/retrace before MA5/MA10 validation. MA touch alone is not sufficient; no generic fixed Type-1 TTL was reintroduced.\n\n### 4. Types 2–4\nPASS at static contract level.\n- Type 2 keeps the source-stated three-candle MA5/10 + Mid-BB confluence, with MA50 as the stronger/Most-Powerful form.\n- Type 3 requires CSM first, then retrace to MA5 or MA50.\n- Type 4 requires CSD first, then retrace to MA5/10.\n- Exact Type 3/4 precursor families are evaluated before generic Type 1 ownership.\n\n### 5. Higher-timeframe owner\nPASS after F4. Standalone H1 Re-Entry is blocked unless H4 recovery is complete and a valid same-direction H4 authoritative owner exists. There is no D1/EMA/candle-colour fallback.\n\n### 6. Timing\nPASS at static mapping after F6. The closed H1 Re-Entry candle validates; execution remains eligible in the immediately following live source-TF candle. No unsupported third-candle delay exists.\n\n### 7. M15/M16 authority\nPASS. M15 remains final atomic entry authority. If eligible BUY and SELL candidates coexist in the same decision pool, M15 creates an opposite-direction conflict rather than selecting an invented winner. M16 revalidates exact component owner identity/freshness before execution.\n\n### 8. Downstream execution boundary\nPASS at architecture level. Only `DEC_VALIDATED` decisions enter preflight. M17/M21/M19/M20/M22 cannot manufacture a new strategy signal family; they consume the strategy decision produced upstream.\n\n## Conclusion\nNo new Mode-1-specific Strategy-Core code defect is identified by static audit after F1-F6. Mode 1 is **statically source-compliant** at candidate/owner/timing architecture level.\n\nThis does not close live validation. Required runtime evidence remains:\n1. native MetaEditor **0 errors / 0 warnings** for integrated current source;\n2. Mode1 traces for Type1/2/3/4 H1 Re-Entry admission/rejection;\n3. H4 NO_OWNER block, same-direction owner admission and opposite-owner rejection;\n4. validation-candle time < actual `OrderOpenTime()` within the immediately following H1 candle;\n5. no raw/combination signal reaches execution while EntryMode=1.\n\n## Next engineering gate\nProceed to the queued **opposite-direction / same-pair cycle integrity audit**, because runtime observations have shown BUY and SELL positions coexisting on one pair. That issue is separate from this Mode-1 static candidate-authority PASS.\n''', encoding='utf-8')

q = QUEUE.read_text(encoding='utf-8')
old = '''#### P3-M1 — Mode 1 Official BBMA Compliance Audit\nPriority: CRITICAL / NEXT STRATEGY GATE AFTER CORE-V2 SPEC CLOSURE\nStatus: STATIC CORE COVERAGE PARTIAL; MODE-1-SPECIFIC END-TO-END/RUNTIME CLOSURE STILL QUEUED\n'''
new = '''#### P3-M1 — Mode 1 Official BBMA Compliance Audit\nPriority: CRITICAL / STRATEGY GATE\nStatus: **STATIC END-TO-END COMPLIANCE PASS — NATIVE METAEDITOR + RUNTIME MODE1 TRACE PENDING**\nAudit record: `blueprint/P3_M1_MODE1_OFFICIAL_BBMA_COMPLIANCE_AUDIT.md`\n'''
if old not in q:
    raise SystemExit('P3-M1 queue header not found')
q = q.replace(old, new, 1)
QUEUE.write_text(q, encoding='utf-8')

c = CURRENT.read_text(encoding='utf-8')
overlay = '''\n\n# 2026-08-22 P3-M1 Mode 1 Compliance Overlay\n- **Mode 1 static end-to-end BBMA compliance audit: PASS.**\n- EntryMode 1 admits only confirmed H1 Re-Entry, under recovered same-direction H4 authoritative ownership; F3 Type1 and existing Type2–4 semantics remain intact.\n- M15/M16 authority and F6 next-candle timing mapping pass static review.\n- Native MetaEditor and runtime Mode1 traces remain pending.\n- **Next engineering gate: opposite-direction / same-pair cycle integrity audit.**\n- Record: `blueprint/P3_M1_MODE1_OFFICIAL_BBMA_COMPLIANCE_AUDIT.md`.\n'''
if '# 2026-08-22 P3-M1 Mode 1 Compliance Overlay' not in c:
    c += overlay
CURRENT.write_text(c, encoding='utf-8')
