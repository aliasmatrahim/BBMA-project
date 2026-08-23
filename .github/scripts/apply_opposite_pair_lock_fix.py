from pathlib import Path

p = Path('blueprint/source/BBMA_EA.mq4')
s = p.read_text(encoding='utf-8')

old_header = 'Version 4.5.1 - P3-M2-07B.2 F1 Boundary Reconciliation'
new_header = 'Version 4.5.1 - P3-M2-11 Mode2 Diagnostic Trace'
if s.count(old_header) != 1:
    raise SystemExit(f'build header anchor count={s.count(old_header)}')
s = s.replace(old_header, new_header, 1)

old = '''   if(buyExtreme.ConfirmationCandleTime > sellExtreme.ConfirmationCandleTime)
      MarkExtremeLifecycleSuperseded(sellExtreme, data,
         "SELL Extreme superseded by newer reversal-confirmed opposite BUY Extreme");
   else if(sellExtreme.ConfirmationCandleTime > buyExtreme.ConfirmationCandleTime)
      MarkExtremeLifecycleSuperseded(buyExtreme, data,
         "BUY Extreme superseded by newer reversal-confirmed opposite SELL Extreme");
   // Equal confirmation time remains ambiguous; downstream conflict stays fail-closed.
'''
new = '''   if(buyExtreme.ConfirmationCandleTime > sellExtreme.ConfirmationCandleTime)
   {
      MarkExtremeLifecycleSuperseded(sellExtreme, data,
         "SELL Extreme superseded by newer reversal-confirmed opposite BUY Extreme");
      if(EntryMode == 2)
         Print("[P3M2][EXT_SUPERSEDE] TF=", data.timeframe,
               " Old=SELL New=BUY OldConfirm=", TimeToString(sellExtreme.ConfirmationCandleTime),
               " NewConfirm=", TimeToString(buyExtreme.ConfirmationCandleTime),
               " ProcessCandle=", TimeToString(data.candle_time));
   }
   else if(sellExtreme.ConfirmationCandleTime > buyExtreme.ConfirmationCandleTime)
   {
      MarkExtremeLifecycleSuperseded(buyExtreme, data,
         "BUY Extreme superseded by newer reversal-confirmed opposite SELL Extreme");
      if(EntryMode == 2)
         Print("[P3M2][EXT_SUPERSEDE] TF=", data.timeframe,
               " Old=BUY New=SELL OldConfirm=", TimeToString(buyExtreme.ConfirmationCandleTime),
               " NewConfirm=", TimeToString(sellExtreme.ConfirmationCandleTime),
               " ProcessCandle=", TimeToString(data.candle_time));
   }
   // Equal confirmation time remains ambiguous; downstream conflict stays fail-closed.
'''
if s.count(old) != 1:
    raise SystemExit(f'Extreme supersession trace anchor count={s.count(old)}')
s = s.replace(old, new, 1)

old = '''      if(IsExtremeReversalDirection(data, parentDirection))
      {
         InstallMHVSupersessionParent(mlv, parent, data);
         MarkCanonicalMLVSuperseded(
            mlv, data,
            "Old MHV/MLV cycle superseded by opposite reversal-confirmed Extreme");
         return true;
      }
'''
new = '''      if(IsExtremeReversalDirection(data, parentDirection))
      {
         InstallMHVSupersessionParent(mlv, parent, data);
         MarkCanonicalMLVSuperseded(
            mlv, data,
            "Old MHV/MLV cycle superseded by opposite reversal-confirmed Extreme");
         if(EntryMode == 2)
            Print("[P3M2][MLV_SUPERSEDE] MLVDir=", EnumToString(mlv.Direction),
                  " NewExtremeDir=", EnumToString(parentDirection),
                  " Raw=", TimeToString(mlv.SupersessionRawCandleTime),
                  " Confirm=", TimeToString(data.candle_time));
         return true;
      }
'''
if s.count(old) != 1:
    raise SystemExit(f'MLV confirmed supersession anchor count={s.count(old)}')
s = s.replace(old, new, 1)

old = '''   mlv.SupersessionCandidateActive = true;
   mlv.SupersessionRawBar = data.barIndex;
   mlv.SupersessionRawCandleTime = data.candle_time;
   return false;
'''
new = '''   mlv.SupersessionCandidateActive = true;
   mlv.SupersessionRawBar = data.barIndex;
   mlv.SupersessionRawCandleTime = data.candle_time;
   if(EntryMode == 2)
      Print("[P3M2][MLV_SUPER_CAND] MLVDir=", EnumToString(mlv.Direction),
            " ExtremeDir=", EnumToString(parentDirection),
            " Raw=", TimeToString(data.candle_time));
   return false;
'''
if s.count(old) != 1:
    raise SystemExit(f'MLV raw supersession anchor count={s.count(old)}')
s = s.replace(old, new, 1)

old = '''   if(EntryMode == 1 && (buyCount > 0 || sellCount > 0))
      Print("[P3M1][M15_COUNTS] Buy=", buyCount, " Sell=", sellCount,
            " Pool=", count, " Time=", TimeToString(g_processing_time));
'''
new = '''   if(EntryMode == 1 && (buyCount > 0 || sellCount > 0))
      Print("[P3M1][M15_COUNTS] Buy=", buyCount, " Sell=", sellCount,
            " Pool=", count, " Time=", TimeToString(g_processing_time));
   if(EntryMode == 2 && (buyCount > 0 || sellCount > 0))
      Print("[P3M2][M15_COUNTS] Buy=", buyCount, " Sell=", sellCount,
            " Pool=", count, " Time=", TimeToString(g_processing_time));
'''
if s.count(old) != 1:
    raise SystemExit(f'M15 counts anchor count={s.count(old)}')
s = s.replace(old, new, 1)

old = '''      if(EntryMode == 1)
         Print("[P3M1][M15_CONFLICT] Opposite eligible RE candidates; no winner selected");
      return;
'''
new = '''      if(EntryMode == 1)
         Print("[P3M1][M15_CONFLICT] Opposite eligible RE candidates; no winner selected");
      if(EntryMode == 2)
         Print("[P3M2][M15_CONFLICT] Opposite eligible Mode2 candidates; no winner selected");
      return;
'''
if s.count(old) != 1:
    raise SystemExit(f'M15 conflict anchor count={s.count(old)}')
s = s.replace(old, new, 1)

old = '''   if(EntryMode == 1)
      Print("[P3M1][M15_SELECT] Pair=", decision.Pair,
            " Signal=", EnumToString(decision.SignalType),
            " Dir=", EnumToString(decision.Direction),
            " Candle=", TimeToString(decision.CandleTime),
            " DecisionID=", decision.DecisionID);
'''
new = '''   if(EntryMode == 1)
      Print("[P3M1][M15_SELECT] Pair=", decision.Pair,
            " Signal=", EnumToString(decision.SignalType),
            " Dir=", EnumToString(decision.Direction),
            " Candle=", TimeToString(decision.CandleTime),
            " DecisionID=", decision.DecisionID);
   if(EntryMode == 2)
      Print("[P3M2][M15_SELECT] Pair=", decision.Pair,
            " Signal=", EnumToString(decision.SignalType),
            " Dir=", EnumToString(decision.Direction),
            " Candle=", TimeToString(decision.CandleTime),
            " Components=", decision.ComponentCount,
            " DecisionID=", decision.DecisionID);
'''
if s.count(old) != 1:
    raise SystemExit(f'M15 select anchor count={s.count(old)}')
s = s.replace(old, new, 1)

old = '''      if(EntryMode == 1)
         Print("[P3M1][M16_REJECT] DecisionID=", decision.DecisionID,
               " Reason=", EnumToString(decision.RejectionReason));
      return;
'''
new = '''      if(EntryMode == 1)
         Print("[P3M1][M16_REJECT] DecisionID=", decision.DecisionID,
               " Reason=", EnumToString(decision.RejectionReason));
      if(EntryMode == 2)
         Print("[P3M2][M16_REJECT] DecisionID=", decision.DecisionID,
               " Reason=", EnumToString(decision.RejectionReason));
      return;
'''
if s.count(old) != 1:
    raise SystemExit(f'M16 conflict reject anchor count={s.count(old)}')
s = s.replace(old, new, 1)

old = '''      else
      {
         decision.DecisionState = DEC_INVALIDATED;
         decision.RejectionReason = REJ_SEQUENCE_BREAK;
      }
      return;
   }
'''
new = '''      else
      {
         decision.DecisionState = DEC_INVALIDATED;
         decision.RejectionReason = REJ_SEQUENCE_BREAK;
      }
      if(EntryMode == 2)
         Print("[P3M2][M16_OWNER_REJECT] DecisionID=", decision.DecisionID,
               " State=", EnumToString(decision.DecisionState),
               " Reason=", EnumToString(decision.RejectionReason));
      return;
   }
'''
if s.count(old) != 1:
    raise SystemExit(f'M16 owner reject anchor count={s.count(old)}')
s = s.replace(old, new, 1)

old = '''   if(EntryMode == 1)
      Print("[P3M1][M16_PASS] DecisionID=", decision.DecisionID,
            " Signal=", EnumToString(decision.SignalType),
            " Candle=", TimeToString(decision.CandleTime));
'''
new = '''   if(EntryMode == 1)
      Print("[P3M1][M16_PASS] DecisionID=", decision.DecisionID,
            " Signal=", EnumToString(decision.SignalType),
            " Candle=", TimeToString(decision.CandleTime));
   if(EntryMode == 2)
      Print("[P3M2][M16_PASS] DecisionID=", decision.DecisionID,
            " Signal=", EnumToString(decision.SignalType),
            " Candle=", TimeToString(decision.CandleTime));
'''
if s.count(old) != 1:
    raise SystemExit(f'M16 pass anchor count={s.count(old)}')
s = s.replace(old, new, 1)

old = '''   if(EntryMode == 1)
      Print("[P3M1][PREFLIGHT_START] Pair=", pair,
            " DecisionID=", decision.DecisionID,
            " Signal=", EnumToString(decision.SignalType),
            " Dir=", EnumToString(decision.Direction),
            " ValidateCandle=", TimeToString(decision.CandleTime),
            " ProcessTime=", TimeToString(g_processing_time));
'''
new = '''   if(EntryMode == 1)
      Print("[P3M1][PREFLIGHT_START] Pair=", pair,
            " DecisionID=", decision.DecisionID,
            " Signal=", EnumToString(decision.SignalType),
            " Dir=", EnumToString(decision.Direction),
            " ValidateCandle=", TimeToString(decision.CandleTime),
            " ProcessTime=", TimeToString(g_processing_time));
   if(EntryMode == 2)
      Print("[P3M2][PREFLIGHT_START] Pair=", pair,
            " DecisionID=", decision.DecisionID,
            " Signal=", EnumToString(decision.SignalType),
            " Dir=", EnumToString(decision.Direction),
            " ValidateCandle=", TimeToString(decision.CandleTime),
            " ProcessTime=", TimeToString(g_processing_time));
'''
if s.count(old) != 1:
    raise SystemExit(f'preflight start anchor count={s.count(old)}')
s = s.replace(old, new, 1)

old = '''   if(EntryMode == 1)
      Print("[P3M1][PREFLIGHT_PASS] DecisionID=", decision.DecisionID,
            " Entry=", DoubleToString(decision.EntryPrice, snapshot.Digits),
            " SL=", DoubleToString(decision.StopLoss, snapshot.Digits),
            " TP=", DoubleToString(decision.TakeProfit, snapshot.Digits),
            " Lot=", DoubleToString(lot, snapshot.LotDigits));
'''
new = '''   if(EntryMode == 1)
      Print("[P3M1][PREFLIGHT_PASS] DecisionID=", decision.DecisionID,
            " Entry=", DoubleToString(decision.EntryPrice, snapshot.Digits),
            " SL=", DoubleToString(decision.StopLoss, snapshot.Digits),
            " TP=", DoubleToString(decision.TakeProfit, snapshot.Digits),
            " Lot=", DoubleToString(lot, snapshot.LotDigits));
   if(EntryMode == 2)
      Print("[P3M2][PREFLIGHT_PASS] DecisionID=", decision.DecisionID,
            " Entry=", DoubleToString(decision.EntryPrice, snapshot.Digits),
            " SL=", DoubleToString(decision.StopLoss, snapshot.Digits),
            " TP=", DoubleToString(decision.TakeProfit, snapshot.Digits),
            " Lot=", DoubleToString(lot, snapshot.LotDigits));
'''
if s.count(old) != 1:
    raise SystemExit(f'preflight pass anchor count={s.count(old)}')
s = s.replace(old, new, 1)

old = '''         if(EntryMode == 1)
            Print("[P3M1][EXEC] Ticket=", ticket,
                  " Pair=", pair,
                  " DecisionID=", decision.DecisionID,
                  " Signal=", EnumToString(decision.SignalType),
                  " Dir=", EnumToString(decision.Direction),
                  " ValidateCandle=", TimeToString(decision.CandleTime),
                  " OrderOpen=", TimeToString(OrderOpenTime()));
         return;
'''
new = '''         if(EntryMode == 1)
            Print("[P3M1][EXEC] Ticket=", ticket,
                  " Pair=", pair,
                  " DecisionID=", decision.DecisionID,
                  " Signal=", EnumToString(decision.SignalType),
                  " Dir=", EnumToString(decision.Direction),
                  " ValidateCandle=", TimeToString(decision.CandleTime),
                  " OrderOpen=", TimeToString(OrderOpenTime()));
         if(EntryMode == 2)
            Print("[P3M2][EXEC] Ticket=", ticket,
                  " Pair=", pair,
                  " DecisionID=", decision.DecisionID,
                  " Signal=", EnumToString(decision.SignalType),
                  " Dir=", EnumToString(decision.Direction),
                  " ValidateCandle=", TimeToString(decision.CandleTime),
                  " OrderOpen=", TimeToString(OrderOpenTime()));
         return;
'''
if s.count(old) != 1:
    raise SystemExit(f'exec trace anchor count={s.count(old)}')
s = s.replace(old, new, 1)

required = [
    '[P3M2][EXT_SUPERSEDE]', '[P3M2][MLV_SUPER_CAND]', '[P3M2][MLV_SUPERSEDE]',
    '[P3M2][M15_COUNTS]', '[P3M2][M15_CONFLICT]', '[P3M2][M15_SELECT]',
    '[P3M2][M16_OWNER_REJECT]', '[P3M2][M16_PASS]',
    '[P3M2][PREFLIGHT_START]', '[P3M2][PREFLIGHT_PASS]', '[P3M2][EXEC]'
]
for token in required:
    if token not in s:
        raise SystemExit('missing trace token: ' + token)
if s.count('{') != s.count('}'):
    raise SystemExit('brace imbalance')

p.write_text(s, encoding='utf-8')
print('P3-M2-11 Mode2 diagnostic trace patch applied')
