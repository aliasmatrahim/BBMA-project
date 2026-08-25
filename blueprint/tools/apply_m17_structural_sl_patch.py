from pathlib import Path
import re

SOURCE = Path("blueprint/source/BBMA_EA.mq4")
text = SOURCE.read_text(encoding="utf-8")

if "M17-SLRANGE-01" in text:
    raise SystemExit("M17-SLRANGE-01 already present; refusing duplicate patch")

for old, new in [
    ("Version 4.5.1 - D1O-07 Canonical LTF Dedup",
     "Version 4.5.2 - M17 Structural SL Normalization"),
    ('#property version   "4.51"', '#property version   "4.52"'),
]:
    if old not in text:
        raise SystemExit(f"required baseline marker missing: {old}")
    text = text.replace(old, new, 1)

helper_block = r'''// M17-SLRANGE-01: resolve the exact M12 Re-Entry lifecycle that owns
// the approved SLTP source component. This does not redetect Re-Entry.
bool ResolveMatchingReEntryLifecycle(string pair, ComponentIdentity &source,
                                     ReEntryData &reEntry)
{
   ZeroMemory(reEntry);

   int pairIndex = FindPairStateIndex(pair);
   if(pairIndex < 0)
   {
      for(int i = 0; i < g_pair_count; i++)
      {
         if(g_pair_states[i].actual_symbol == pair)
         {
            pairIndex = i;
            break;
         }
      }
   }
   if(pairIndex < 0 || pairIndex >= g_pair_count) return false;

   if(source.Timeframe == PERIOD_H1 && source.Direction == DIR_BUY)
      reEntry = g_pair_states[pairIndex].re_h1_buy_state;
   else if(source.Timeframe == PERIOD_H1 && source.Direction == DIR_SELL)
      reEntry = g_pair_states[pairIndex].re_h1_sell_state;
   else if(source.Timeframe == PERIOD_H4 && source.Direction == DIR_BUY)
      reEntry = g_pair_states[pairIndex].re_h4_buy_state;
   else if(source.Timeframe == PERIOD_H4 && source.Direction == DIR_SELL)
      reEntry = g_pair_states[pairIndex].re_h4_sell_state;
   else if(source.Timeframe == PERIOD_D1 && source.Direction == DIR_BUY)
      reEntry = g_pair_states[pairIndex].re_d1_buy_state;
   else if(source.Timeframe == PERIOD_D1 && source.Direction == DIR_SELL)
      reEntry = g_pair_states[pairIndex].re_d1_sell_state;
   else if(source.Timeframe == PERIOD_M15 && source.Direction == DIR_BUY)
      reEntry = g_pair_states[pairIndex].re_m15_buy_state;
   else if(source.Timeframe == PERIOD_M15 && source.Direction == DIR_SELL)
      reEntry = g_pair_states[pairIndex].re_m15_sell_state;
   else
      return false;

   if(reEntry.State != RE_STATE_CONFIRMED || !reEntry.IsValid) return false;
   if(reEntry.Direction != source.Direction || reEntry.Timeframe != source.Timeframe)
      return false;
   if(reEntry.ConfirmationCandle != source.CandleTime) return false;
   if(reEntry.StartCandleTime <= 0 || reEntry.ConfirmationCandle <= 0) return false;
   if(reEntry.StartCandleTime > reEntry.ConfirmationCandle) return false;
   return true;
}

// M17-SLRANGE-01: reconstruct only the source-owned lifecycle window
// StartCandleTime..ConfirmationCandle inclusive. No arbitrary swing lookback.
bool ResolveSourceOwnedStructuralAnchor(string pair, ComponentIdentity &source,
                                        ENUM_DIRECTION direction, double &anchor,
                                        datetime &startTime,
                                        datetime &confirmationTime,
                                        double &confirmationWick)
{
   anchor = 0.0;
   startTime = 0;
   confirmationTime = 0;
   confirmationWick = 0.0;

   ReEntryData reEntry;
   if(!ResolveMatchingReEntryLifecycle(pair, source, reEntry)) return false;

   startTime = reEntry.StartCandleTime;
   confirmationTime = reEntry.ConfirmationCandle;

   int startShift = iBarShift(pair, source.Timeframe, startTime, true);
   int confirmationShift = iBarShift(pair, source.Timeframe,
                                     confirmationTime, true);
   if(startShift < 1 || confirmationShift < 1) return false;
   if(startShift < confirmationShift) return false;
   if(iTime(pair, source.Timeframe, startShift) != startTime) return false;
   if(iTime(pair, source.Timeframe, confirmationShift) != confirmationTime)
      return false;

   int tfSeconds = GetTimeframeSeconds(source.Timeframe);
   if(tfSeconds <= 0) return false;

   for(int shift = confirmationShift; shift <= startShift; shift++)
   {
      datetime barTime = iTime(pair, source.Timeframe, shift);
      if(barTime <= 0 || barTime < startTime || barTime > confirmationTime)
         return false;
      if(!IsCandleClosed(barTime, tfSeconds)) return false;

      double low = iLow(pair, source.Timeframe, shift);
      double high = iHigh(pair, source.Timeframe, shift);
      if(low <= 0.0 || high <= 0.0 || high < low) return false;

      if(direction == DIR_BUY)
      {
         if(anchor <= 0.0 || low < anchor) anchor = low;
      }
      else if(direction == DIR_SELL)
      {
         if(anchor <= 0.0 || high > anchor) anchor = high;
      }
      else
         return false;
   }

   if(direction == DIR_BUY)
      confirmationWick = iLow(pair, source.Timeframe, confirmationShift);
   else if(direction == DIR_SELL)
      confirmationWick = iHigh(pair, source.Timeframe, confirmationShift);
   else
      return false;

   return (anchor > 0.0 && confirmationWick > 0.0);
}

'''

pattern = re.compile(
    r"bool ResolveSourceOwnedWickAnchor\(string pair, ComponentIdentity &source,\n"
    r"\s*ENUM_DIRECTION direction, double &anchor\)\n\{.*?\n\}\n\n"
    r"(?=bool ResolveApprovedBBDestination)",
    re.S,
)
text, count = pattern.subn(helper_block, text, count=1)
if count != 1:
    raise SystemExit(f"expected one ResolveSourceOwnedWickAnchor block, got {count}")

old_resolve = '''   double wickAnchor = 0.0;
   double destination = 0.0;
   if(!ResolveSourceOwnedWickAnchor(decision.Pair,
                                    decision.SLTPSourceComponent,
                                    decision.Direction,
                                    wickAnchor))
      return false;
'''
new_resolve = '''   double structuralAnchor = 0.0;
   datetime structuralStart = 0;
   datetime structuralConfirmation = 0;
   double confirmationWick = 0.0;
   double destination = 0.0;
   if(!ResolveSourceOwnedStructuralAnchor(decision.Pair,
                                          decision.SLTPSourceComponent,
                                          decision.Direction,
                                          structuralAnchor,
                                          structuralStart,
                                          structuralConfirmation,
                                          confirmationWick))
      return false;
'''
if old_resolve not in text:
    raise SystemExit("old wick resolver call block not found")
text = text.replace(old_resolve, new_resolve, 1)

old_sl = '''   double safetyBuffer = snapshot.Point;
   double structuralSL = (decision.Direction == DIR_BUY)
      ? wickAnchor - safetyBuffer
      : wickAnchor + safetyBuffer;
'''
new_sl = '''   double safetyBuffer = snapshot.Point;
   double structuralSL = (decision.Direction == DIR_BUY)
      ? structuralAnchor - safetyBuffer
      : structuralAnchor + safetyBuffer;

   // M17-SLRANGE-01: direction-aware broker hard-SL normalization.
   // BUY closes on Bid, aligned with Bid-chart structure: no spread buffer.
   // SELL closes on Ask: add the approved frozen rounded spread buffer.
   double brokerSL = structuralSL;
   double rawSpreadPips = 0.0;
   double roundedSpreadBufferPips = 0.0;
   if(decision.Direction == DIR_SELL)
   {
      double pipValue = GetPipValue(decision.Pair);
      if(pipValue <= 0.0 || snapshot.CurrentSpreadPrice < 0.0) return false;

      rawSpreadPips = snapshot.CurrentSpreadPrice / pipValue;
      roundedSpreadBufferPips = MathCeil(rawSpreadPips - 0.000000001);
      if(roundedSpreadBufferPips < 2.0)
         roundedSpreadBufferPips = 2.0;

      brokerSL += roundedSpreadBufferPips * pipValue;
   }
'''
if old_sl not in text:
    raise SystemExit("old structural SL block not found")
text = text.replace(old_sl, new_sl, 1)

old_ticks = "   double slTicks = structuralSL / snapshot.TickSize_Price;"
if old_ticks not in text:
    raise SystemExit("old slTicks expression not found")
text = text.replace(old_ticks,
                    "   double slTicks = brokerSL / snapshot.TickSize_Price;", 1)

old_assign = '''   decision.StopLoss = normalizedSL;
   decision.TakeProfit = normalizedTP;
   decision.SLTPSource = decision.SLTPSourceComponent.ComponentType;
   return true;
}'''
new_assign = '''   decision.StopLoss = normalizedSL;
   decision.TakeProfit = normalizedTP;
   decision.SLTPSource = decision.SLTPSourceComponent.ComponentType;

   if(DebugLevel >= DBG_TRADE)
   {
      Print("[M17-SL][STRUCT] Pair=", decision.Pair,
            " Dir=", EnumToString(decision.Direction),
            " TF=", IntegerToString(decision.SLTPSourceComponent.Timeframe),
            " Start=", TimeToString(structuralStart),
            " Confirm=", TimeToString(structuralConfirmation),
            " StructuralAnchor=", DoubleToString(structuralAnchor, snapshot.Digits),
            " ConfirmationWick=", DoubleToString(confirmationWick, snapshot.Digits),
            " RawSpreadPips=", DoubleToString(rawSpreadPips, 4),
            " SpreadBufferPips=", DoubleToString(roundedSpreadBufferPips, 1),
            " StructuralSL=", DoubleToString(structuralSL, snapshot.Digits),
            " FinalBrokerSL=", DoubleToString(decision.StopLoss, snapshot.Digits),
            " TP=", DoubleToString(decision.TakeProfit, snapshot.Digits));
   }
   return true;
}'''
if old_assign not in text:
    raise SystemExit("M17 final assignment block not found")
text = text.replace(old_assign, new_assign, 1)

lot_reject = '''      decision.DecisionState = DEC_REJECTED;
      decision.RejectionReason = REJ_INVALID_LOT;
      return false;
   }
'''
if lot_reject not in text:
    raise SystemExit("invalid-lot rejection block not found")
lot_telemetry = lot_reject + '''
   if(DebugLevel >= DBG_TRADE)
   {
      Print("[M17-SL][LOT] Pair=", pair,
            " Dir=", EnumToString(decision.Direction),
            " Entry=", DoubleToString(decision.EntryPrice, snapshot.Digits),
            " FinalSL=", DoubleToString(decision.StopLoss, snapshot.Digits),
            " FinalTP=", DoubleToString(decision.TakeProfit, snapshot.Digits),
            " FinalLot=", DoubleToString(lot, snapshot.LotDigits));
   }
'''
text = text.replace(lot_reject, lot_telemetry, 1)

must = [
    "Version 4.5.2 - M17 Structural SL Normalization",
    '#property version   "4.52"',
    "ResolveMatchingReEntryLifecycle",
    "ResolveSourceOwnedStructuralAnchor",
    "reEntry.StartCandleTime",
    "reEntry.ConfirmationCandle",
    "MathCeil(rawSpreadPips - 0.000000001)",
    "if(roundedSpreadBufferPips < 2.0)",
    "brokerSL += roundedSpreadBufferPips * pipValue",
    "double slTicks = brokerSL / snapshot.TickSize_Price",
    "[M17-SL][STRUCT]",
    "[M17-SL][LOT]",
]
missing = [marker for marker in must if marker not in text]
if missing:
    raise SystemExit(f"post-patch markers missing: {missing}")

for stale in ["ResolveSourceOwnedWickAnchor(", "? wickAnchor - safetyBuffer",
              ": wickAnchor + safetyBuffer"]:
    if stale in text:
        raise SystemExit(f"stale old mapping remains: {stale}")

SOURCE.write_text(text, encoding="utf-8", newline="\n")
print("M17 structural-range patch materialized successfully")
