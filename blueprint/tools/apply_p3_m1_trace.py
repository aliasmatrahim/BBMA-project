from pathlib import Path

p = Path('blueprint/source/BBMA_EA.mq4')
s = p.read_text(encoding='utf-8')
before = s


def rep(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    s = s.replace(old, new, 1)


rep('''void BuildConfirmedReEntryCandidate(ReEntryData &reEntry,
                                    H4DirectionalOwner &h4Owner,
                                    ValidatedSequenceCandidate &candidate)
{
   ZeroMemory(candidate);
''','''void BuildConfirmedReEntryCandidate(ReEntryData &reEntry,
                                    H4DirectionalOwner &h4Owner,
                                    ValidatedSequenceCandidate &candidate)
{
   ZeroMemory(candidate);

   if(EntryMode == 1 && reEntry.State == RE_STATE_CONFIRMED)
      Print("[P3M1][RE_EVAL] Type=", EnumToString(reEntry.Type),
            " Dir=", EnumToString(reEntry.Direction),
            " Valid=", reEntry.IsValid ? "Y" : "N",
            " Confirm=", TimeToString(reEntry.ConfirmationCandle),
            " H4State=", EnumToString(h4Owner.State),
            " H4Dir=", EnumToString(h4Owner.Direction),
            " H4Valid=", h4Owner.IsValid ? "Y" : "N",
            " H4Recovery=", h4Owner.RecoveryComplete ? "Y" : "N");
''','re_eval')

rep('''   candidate.PatternStrength = 0;
   candidate.Valid = true;
}
''','''   candidate.PatternStrength = 0;
   candidate.Valid = true;
   if(EntryMode == 1)
      Print("[P3M1][RE_ADMIT] Type=", EnumToString(reEntry.Type),
            " Dir=", EnumToString(reEntry.Direction),
            " Confirm=", TimeToString(reEntry.ConfirmationCandle),
            " Hash=", candidate.SequenceHash);
}
''','re_admit')

rep('''   if(buyCount > 0 && sellCount > 0)
   {
''','''   if(EntryMode == 1 && (buyCount > 0 || sellCount > 0))
      Print("[P3M1][M15_COUNTS] Buy=", buyCount, " Sell=", sellCount,
            " Pool=", count, " Time=", TimeToString(g_processing_time));

   if(buyCount > 0 && sellCount > 0)
   {
''','m15_counts')

rep('''      conflict.FrozenSnapshotTime = g_processing_time;
      return;
   }
''','''      conflict.FrozenSnapshotTime = g_processing_time;
      if(EntryMode == 1)
         Print("[P3M1][M15_CONFLICT] Opposite eligible RE candidates; no winner selected");
      return;
   }
''','m15_conflict')

rep('''   decision.DecisionID = GenerateDecisionID(decision.Pair, decision.CandleTime,
                                             decision.Direction,
                                             decision.SignalType,
                                             decision.SequenceHash);
}
''','''   decision.DecisionID = GenerateDecisionID(decision.Pair, decision.CandleTime,
                                             decision.Direction,
                                             decision.SignalType,
                                             decision.SequenceHash);
   if(EntryMode == 1)
      Print("[P3M1][M15_SELECT] Pair=", decision.Pair,
            " Signal=", EnumToString(decision.SignalType),
            " Dir=", EnumToString(decision.Direction),
            " Candle=", TimeToString(decision.CandleTime),
            " DecisionID=", decision.DecisionID);
}
''','m15_select')

rep('''      decision.DecisionState = DEC_INVALIDATED;
      decision.RejectionReason = REJ_OPPOSITE_SIGNAL;
      return;
''','''      decision.DecisionState = DEC_INVALIDATED;
      decision.RejectionReason = REJ_OPPOSITE_SIGNAL;
      if(EntryMode == 1)
         Print("[P3M1][M16_REJECT] DecisionID=", decision.DecisionID,
               " Reason=", EnumToString(decision.RejectionReason));
      return;
''','m16_reject')

rep('''   decision.DecisionState = DEC_VALIDATED;
   decision.RejectionReason = REJ_NONE;
}
''','''   decision.DecisionState = DEC_VALIDATED;
   decision.RejectionReason = REJ_NONE;
   if(EntryMode == 1)
      Print("[P3M1][M16_PASS] DecisionID=", decision.DecisionID,
            " Signal=", EnumToString(decision.SignalType),
            " Candle=", TimeToString(decision.CandleTime));
}
''','m16_pass')

rep('''bool RunEntryPreflightAndExecute(BBMA_Decision &decision, string pair)
{
   if(decision.DecisionState != DEC_VALIDATED) return false;
   if(pair == "" || decision.Pair != pair) return false;
''','''bool RunEntryPreflightAndExecute(BBMA_Decision &decision, string pair)
{
   if(decision.DecisionState != DEC_VALIDATED) return false;
   if(pair == "" || decision.Pair != pair) return false;
   if(EntryMode == 1)
      Print("[P3M1][PREFLIGHT_START] Pair=", pair,
            " DecisionID=", decision.DecisionID,
            " Signal=", EnumToString(decision.SignalType),
            " Dir=", EnumToString(decision.Direction),
            " ValidateCandle=", TimeToString(decision.CandleTime),
            " ProcessTime=", TimeToString(g_processing_time));
''','preflight_start')

rep('''   FinalPortfolioGuard(decision);
   if(decision.DecisionState != DEC_VALIDATED) return false;

   ProcessEntry(decision, pair, snapshot, lot);
''','''   FinalPortfolioGuard(decision);
   if(decision.DecisionState != DEC_VALIDATED)
   {
      if(EntryMode == 1)
         Print("[P3M1][PORTFOLIO_REJECT] DecisionID=", decision.DecisionID,
               " Reason=", EnumToString(decision.RejectionReason));
      return false;
   }

   if(EntryMode == 1)
      Print("[P3M1][PREFLIGHT_PASS] DecisionID=", decision.DecisionID,
            " Entry=", DoubleToString(decision.EntryPrice, snapshot.Digits),
            " SL=", DoubleToString(decision.StopLoss, snapshot.Digits),
            " TP=", DoubleToString(decision.TakeProfit, snapshot.Digits),
            " Lot=", DoubleToString(lot, snapshot.LotDigits));

   ProcessEntry(decision, pair, snapshot, lot);
''','preflight_pass')

rep('''         decision.DecisionState = DEC_EXECUTED;
         MarkDecisionExecuted(decision.DecisionID, ticket);
         decision.DecisionState = DEC_EXECUTED;
         decision.RejectionReason = REJ_NONE;
         return;
''','''         decision.DecisionState = DEC_EXECUTED;
         MarkDecisionExecuted(decision.DecisionID, ticket);
         decision.DecisionState = DEC_EXECUTED;
         decision.RejectionReason = REJ_NONE;
         if(EntryMode == 1)
            Print("[P3M1][EXEC] Ticket=", ticket,
                  " Pair=", pair,
                  " DecisionID=", decision.DecisionID,
                  " Signal=", EnumToString(decision.SignalType),
                  " Dir=", EnumToString(decision.Direction),
                  " ValidateCandle=", TimeToString(decision.CandleTime),
                  " OrderOpen=", TimeToString(OrderOpenTime()));
         return;
''','exec')

if s == before:
    raise SystemExit('No changes produced')
if s.count('{') != s.count('}'):
    raise SystemExit('Brace imbalance')
for anchor in [
    'bool IsEntryModeCandidateAllowed(',
    'void BuildConfirmedReEntryCandidate(',
    'void PriorityEngine_Atomic(',
    'void InvalidationEngine_Atomic(',
    'bool ResolveApprovedInitialSLTP(',
    'RiskStatus CheckRiskBeforeTrade(',
    'void ProcessEntry(',
    'bool RunEntryPreflightAndExecute(',
    'void ProcessPair(',
    'void OnTick()'
]:
    if before.count(anchor) != 1 or s.count(anchor) != 1:
        raise SystemExit('Anchor changed: ' + anchor)

p.write_text(s, encoding='utf-8')
Path('blueprint/P3_M1_RUNTIME_TRACE_PATCH.md').write_text(
    '# P3-M1 Runtime Trace Patch\n\n'
    'Status: TRACE-ONLY PATCH APPLIED; NATIVE METAEDITOR 0E0W REQUIRED BEFORE MERGE.\n\n'
    'Adds `[P3M1]` trace points for Re-Entry/H4 evaluation, M15 selection/conflict, M16 pass/reject, preflight/portfolio, and actual execution. No BBMA, SL/TP, lot, risk, portfolio, trade-lock, or execution predicate is changed.\n',
    encoding='utf-8'
)
