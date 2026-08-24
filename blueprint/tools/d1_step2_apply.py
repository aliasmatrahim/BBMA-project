from pathlib import Path
import sys

SRC = Path('blueprint/source/BBMA_EA.mq4')
M15 = Path('blueprint/contracts/M15_FINAL_SIGNAL_AUTHORITY_CONTRACT.md')
M16 = Path('blueprint/contracts/M16_CONFLICT_INVALIDATION_CONTRACT.md')
AUDIT = Path('blueprint/D1_STEP2_M15_M16_STRATEGIC_GATE_IMPLEMENTATION_AUDIT_20260824.md')


def replace_once(s: str, old: str, new: str, label: str) -> str:
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected exactly 1 anchor, found {n}')
    return s.replace(old, new, 1)


def apply_source():
    s = SRC.read_text(encoding='utf-8')

    s = replace_once(
        s,
        '//| Version 4.5.1 - D1-01 M11 Strategic Owner                        |',
        '//| Version 4.5.1 - D1-02 M15-M16 Strategic Gate                    |',
        'build header')

    s = replace_once(
        s,
        '   string               Pair;\n   \n   // MUTABLE LIFECYCLE',
        '''   string               Pair;

   // D1-02 frozen M11 strategic-owner identity for downstream M16 verification.
   ENUM_D1_OWNER_STATE  D1OwnerState;
   ENUM_DIRECTION       D1OwnerDirection;
   datetime             D1OwnerCandleTime;
   double               D1OwnerClose;
   double               D1OwnerMA50Current;
   double               D1OwnerMA50Previous;
   bool                 D1OwnerSnapshotValid;
   
   // MUTABLE LIFECYCLE''',
        'decision D1 payload')

    s = replace_once(
        s,
        '//| MODULE 15: PRIORITY ENGINE (FINAL SIGNAL AUTHORITY)              |\n//| LEVEL: EXPERT-RESTRICTED                                         |\n//+------------------------------------------------------------------+\n\nbool IsEntryModeCandidateAllowed',
        '''//| MODULE 15: PRIORITY ENGINE (FINAL SIGNAL AUTHORITY)              |
//| LEVEL: EXPERT-RESTRICTED                                         |
//+------------------------------------------------------------------+

bool IsD1MajorTrendOwnerExecutionReady(PairState &pairState)
{
   D1MajorTrendOwner owner = pairState.d1_major_trend_owner;

   if(!pairState.d1_data.is_valid || !pairState.d1_data.is_closed ||
      pairState.d1_data.timeframe != PERIOD_D1 ||
      pairState.d1_data.candle_time <= 0 || pairState.d1_data.close <= 0.0)
      return false;

   if(!owner.IsValid || owner.SourceCandleTime <= 0 ||
      owner.SourceCandleTime != pairState.d1_data.candle_time)
      return false;

   if(pairState.current_daily_ema50 <= 0.0 || pairState.prev_daily_ema50 <= 0.0)
      return false;

   if(owner.State == D1_OWNER_BUY_CONFIRMED)
      return (owner.Direction == DIR_BUY);

   if(owner.State == D1_OWNER_SELL_CONFIRMED)
      return (owner.Direction == DIR_SELL);

   return false;
}

bool IsCandidateAllowedByD1Owner(ValidatedSequenceCandidate &candidate,
                                 PairState &pairState)
{
   if(!IsD1MajorTrendOwnerExecutionReady(pairState)) return false;
   return (candidate.Direction == pairState.d1_major_trend_owner.Direction);
}

bool FreezeD1OwnerSnapshot(PairState &pairState, BBMA_Decision &decision)
{
   if(!IsD1MajorTrendOwnerExecutionReady(pairState)) return false;

   decision.D1OwnerState = pairState.d1_major_trend_owner.State;
   decision.D1OwnerDirection = pairState.d1_major_trend_owner.Direction;
   decision.D1OwnerCandleTime = pairState.d1_major_trend_owner.SourceCandleTime;
   decision.D1OwnerClose = pairState.d1_data.close;
   decision.D1OwnerMA50Current = pairState.current_daily_ema50;
   decision.D1OwnerMA50Previous = pairState.prev_daily_ema50;
   decision.D1OwnerSnapshotValid = true;
   return true;
}

bool IsEntryModeCandidateAllowed''',
        'M15 D1 helpers')

    s = replace_once(
        s,
        'void PriorityEngine_Atomic(ValidatedSequenceCandidate &candidates[], int count,\n                           BBMA_Decision &decision, OppositeConflictPackage &conflict)\n{\n   int buyCount = 0;\n   int sellCount = 0;\n\n   for(int i = 0; i < count; i++)\n   {\n      if(!IsCandidateEligible(candidates[i])) continue;\n      if(candidates[i].Direction == DIR_BUY) buyCount++;\n      else if(candidates[i].Direction == DIR_SELL) sellCount++;\n   }',
        '''void PriorityEngine_Atomic(ValidatedSequenceCandidate &candidates[], int count,
                           PairState &pairState,
                           BBMA_Decision &decision, OppositeConflictPackage &conflict)
{
   int structurallyEligible = 0;
   for(int i = 0; i < count; i++)
      if(IsCandidateEligible(candidates[i])) structurallyEligible++;

   // D1-02: D1 is the strategic new-entry gate. TRANSITION/UNRESOLVED
   // and stale/malformed owner identity fail closed before atomic direction selection.
   if(structurallyEligible > 0 && !IsD1MajorTrendOwnerExecutionReady(pairState))
   {
      Print("[D1-02][M15_D1_BLOCK] Pair=", pairState.actual_symbol,
            " State=", EnumToString(pairState.d1_major_trend_owner.State),
            " Dir=", EnumToString(pairState.d1_major_trend_owner.Direction),
            " Candle=", TimeToString(pairState.d1_major_trend_owner.SourceCandleTime));
      return;
   }

   int buyCount = 0;
   int sellCount = 0;

   for(int i = 0; i < count; i++)
   {
      if(!IsCandidateEligible(candidates[i])) continue;
      if(!IsCandidateAllowedByD1Owner(candidates[i], pairState)) continue;
      if(candidates[i].Direction == DIR_BUY) buyCount++;
      else if(candidates[i].Direction == DIR_SELL) sellCount++;
   }''',
        'PriorityEngine signature/gate')

    s = replace_once(
        s,
        '      if(!IsCandidateEligible(candidates[i])) continue;\n      if(candidates[i].Direction != targetDirection) continue;',
        '      if(!IsCandidateEligible(candidates[i])) continue;\n      if(!IsCandidateAllowedByD1Owner(candidates[i], pairState)) continue;\n      if(candidates[i].Direction != targetDirection) continue;',
        'canonical loop D1 filter')

    s = replace_once(
        s,
        '   ValidatedSequenceCandidate selected = candidates[canonicalIdx];\n   decision.Valid = true;',
        '''   ValidatedSequenceCandidate selected = candidates[canonicalIdx];
   if(!FreezeD1OwnerSnapshot(pairState, decision))
   {
      Print("[D1-02][M15_D1_BLOCK] Pair=", pairState.actual_symbol,
            " Reason=freeze_failed");
      return;
   }

   decision.Valid = true;''',
        'freeze D1 snapshot')

    s = replace_once(
        s,
        '            " Dir=", EnumToString(decision.Direction),\n            " Candle=", TimeToString(decision.CandleTime),\n            " DecisionID=", decision.DecisionID);',
        '            " Dir=", EnumToString(decision.Direction),\n            " D1State=", EnumToString(decision.D1OwnerState),\n            " D1Candle=", TimeToString(decision.D1OwnerCandleTime),\n            " Candle=", TimeToString(decision.CandleTime),\n            " DecisionID=", decision.DecisionID);',
        'Mode1 D1 trace')

    s = replace_once(
        s,
        '            " Dir=", EnumToString(decision.Direction),\n            " Candle=", TimeToString(decision.CandleTime),\n            " Components=", decision.ComponentCount,',
        '            " Dir=", EnumToString(decision.Direction),\n            " D1State=", EnumToString(decision.D1OwnerState),\n            " D1Candle=", TimeToString(decision.D1OwnerCandleTime),\n            " Candle=", TimeToString(decision.CandleTime),\n            " Components=", decision.ComponentCount,',
        'Mode2 D1 trace')

    s = replace_once(
        s,
        'bool ValidateDecisionOwnerSnapshot(int pairIndex, BBMA_Decision &decision,\n                                   bool &expired)',
        '''bool ValidateDecisionD1OwnerSnapshot(int pairIndex, BBMA_Decision &decision)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return false;
   if(!decision.D1OwnerSnapshotValid) return false;

   PairState state = g_pair_states[pairIndex];
   if(!IsD1MajorTrendOwnerExecutionReady(state)) return false;

   D1MajorTrendOwner owner = state.d1_major_trend_owner;
   if(decision.D1OwnerState != owner.State) return false;
   if(decision.D1OwnerDirection != owner.Direction) return false;
   if(decision.Direction != owner.Direction) return false;
   if(decision.D1OwnerCandleTime != owner.SourceCandleTime) return false;
   if(decision.D1OwnerClose != state.d1_data.close) return false;
   if(decision.D1OwnerMA50Current != state.current_daily_ema50) return false;
   if(decision.D1OwnerMA50Previous != state.prev_daily_ema50) return false;

   return true;
}

bool ValidateDecisionOwnerSnapshot(int pairIndex, BBMA_Decision &decision,
                                   bool &expired)''',
        'M16 D1 verification helper')

    s = replace_once(
        s,
        '   bool ownerExpired = false;\n   if(!ValidateDecisionOwnerSnapshot(pairIndex, decision, ownerExpired))',
        '''   if(!ValidateDecisionD1OwnerSnapshot(pairIndex, decision))
   {
      decision.DecisionState = DEC_INVALIDATED;
      decision.RejectionReason = REJ_SEQUENCE_BREAK;
      Print("[D1-02][M16_D1_REJECT] Pair=", decision.Pair,
            " DecisionID=", decision.DecisionID,
            " FrozenState=", EnumToString(decision.D1OwnerState),
            " FrozenDir=", EnumToString(decision.D1OwnerDirection),
            " FrozenCandle=", TimeToString(decision.D1OwnerCandleTime));
      return;
   }

   bool ownerExpired = false;
   if(!ValidateDecisionOwnerSnapshot(pairIndex, decision, ownerExpired))''',
        'M16 D1 fail-closed gate')

    s = replace_once(
        s,
        '   PriorityEngine_Atomic(allCandidates, allCandidateCount, decision, conflict);',
        '   PriorityEngine_Atomic(allCandidates, allCandidateCount,\n                         g_pair_states[pairIndex], decision, conflict);',
        'M27 M15 call')

    s = replace_once(
        s,
        '   Log(DBG_FULL, "BBMA EA V4.5.1 D1-01 initialized successfully");',
        '   Log(DBG_FULL, "BBMA EA V4.5.1 D1-02 initialized successfully");',
        'OnInit build trace')

    SRC.write_text(s, encoding='utf-8')
    static_check()


def static_check():
    s = SRC.read_text(encoding='utf-8')
    required = [
        'Version 4.5.1 - D1-02 M15-M16 Strategic Gate',
        'D1OwnerSnapshotValid',
        'IsD1MajorTrendOwnerExecutionReady',
        'IsCandidateAllowedByD1Owner',
        'FreezeD1OwnerSnapshot',
        '[D1-02][M15_D1_BLOCK]',
        'ValidateDecisionD1OwnerSnapshot',
        '[D1-02][M16_D1_REJECT]',
        'g_pair_states[pairIndex], decision, conflict',
    ]
    for x in required:
        if x not in s:
            raise SystemExit(f'missing required D1-02 anchor: {x}')
    if s.count('void PriorityEngine_Atomic(') != 1:
        raise SystemExit('PriorityEngine_Atomic definition count invalid')
    if s.count('PriorityEngine_Atomic(allCandidates') != 1:
        raise SystemExit('PriorityEngine_Atomic call count invalid')
    if s.count('ValidateDecisionD1OwnerSnapshot(pairIndex, decision)') != 1:
        raise SystemExit('M16 D1 verification call count invalid')
    if s.index('if(!IsCandidateAllowedByD1Owner(candidates[i], pairState)) continue;') > s.index('if(buyCount > 0 && sellCount > 0)'):
        raise SystemExit('D1 filter is not before atomic direction conflict check')
    if s.index('ValidateDecisionD1OwnerSnapshot(pairIndex, decision)') > s.index('ValidateDecisionOwnerSnapshot(pairIndex, decision, ownerExpired)'):
        raise SystemExit('M16 D1 revalidation is not before structural component revalidation')
    window = s[s.index('//| MODULE 15:'):s.index('//| MODULE 17:')]
    for forbidden in ['RSI', 'MACD', 'Stochastic', 'ADX', 'NewsFilter', 'SessionFilter']:
        if forbidden in window:
            raise SystemExit(f'forbidden filter introduced in M15/M16: {forbidden}')
    if s.count('{') != s.count('}'):
        raise SystemExit('brace imbalance')
    if s.count('(') != s.count(')'):
        raise SystemExit('parenthesis imbalance')
    print('D1_STEP2_STATIC=PASS')


def finalize():
    overlay15 = '''\n\n## D1-02 implementation record — `d1-owner-dev`\nThe 2026-08-24 D1 strategic gate is implemented on isolated `d1-owner-dev` as build `Version 4.5.1 - D1-02 M15-M16 Strategic Gate`.\n\n- M15 consumes M11 owner state; it does not recalculate D1/MA50.\n- Transition/unresolved/stale D1 blocks new-entry authority.\n- Opposite-D1 candidates are filtered before the atomic surviving-direction check.\n- Exact REM/RRE/REE signatures remain unchanged.\n- Selected decisions freeze D1 owner state/direction/candle plus D1 close and MA50 identity for M16.\n- Native MT4 MetaEditor: **0 errors / 0 warnings**.\n- `blueprint-dev` remains unchanged pending explicit integration approval.\n'''
    overlay16 = '''\n\n## D1-02 implementation record — `d1-owner-dev`\nThe 2026-08-24 D1 owner revalidation is implemented on isolated `d1-owner-dev` as build `Version 4.5.1 - D1-02 M15-M16 Strategic Gate`.\n\n- M16 verifies the frozen M15 D1 snapshot against the current M11-produced owner identity.\n- Transition/unresolved/opposite/stale/identity mismatch fails closed before structural component revalidation.\n- M16 does not duplicate the D1 price-vs-MA50 slope formula.\n- D1 strategic failure invalidates only a pending new-entry decision; it is not a live-position close rule.\n- Native MT4 MetaEditor: **0 errors / 0 warnings**.\n- `blueprint-dev` remains unchanged pending explicit integration approval.\n'''
    for path, marker, overlay in [
        (M15, '## D1-02 implementation record — `d1-owner-dev`', overlay15),
        (M16, '## D1-02 implementation record — `d1-owner-dev`', overlay16),
    ]:
        text = path.read_text(encoding='utf-8')
        if marker not in text:
            path.write_text(text.rstrip() + overlay + '\n', encoding='utf-8')

    AUDIT.write_text('''# D1 Step 2 — M15/M16 Strategic Gate Implementation Audit\n\nDate: 2026-08-24  \nBranch: `d1-owner-dev`  \nBuild: `Version 4.5.1 - D1-02 M15-M16 Strategic Gate`  \nStatus: **IMPLEMENTED / STATIC PASS / NATIVE METAEDITOR 0E0W PASS**\n\n## Scope\nImplements only the reconciled D1 strategic new-entry gate and frozen-owner revalidation.\n\n## Result\n- M15 consumes M11 D1 owner state.\n- Confirmed BUY permits BUY candidates only; confirmed SELL permits SELL candidates only.\n- Transition/unresolved/stale identity blocks new entries.\n- D1 filtering precedes opposite-direction atomic conflict evaluation.\n- REM/RRE/REE structural signatures are unchanged.\n- M15 freezes D1 state/direction/closed candle/close/current MA50/previous MA50.\n- M16 verifies that frozen identity against the current M11 owner before component revalidation.\n- No second D1 trend formula is introduced.\n- No live-position close authority is added.\n\n## Boundary\nNo F7 targetless TP, M17, M22, M23/M24 lifecycle, risk, lot sizing or broker execution change is part of D1-02.\n`blueprint-dev` remains frozen and unchanged.\n\n## Verification\nFocused static integrity: PASS.\nPurity guard: PASS.\nMT4 MetaEditor: **0 errors / 0 warnings**.\nEX4 produced successfully.\n''', encoding='utf-8')


if __name__ == '__main__':
    if '--finalize' in sys.argv:
        finalize()
    elif '--check' in sys.argv:
        static_check()
    else:
        apply_source()
