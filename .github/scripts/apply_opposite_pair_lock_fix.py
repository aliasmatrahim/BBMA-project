from pathlib import Path

SOURCE = Path('blueprint/source/BBMA_EA.mq4')
s = SOURCE.read_text(encoding='utf-8')

if 'P3-M2-07B Opposite Extreme Supersession' in s:
    print('P3-M2-07B already applied')
    raise SystemExit(0)

s = s.replace('Version 4.5.1 - PATCHED 2.1',
              'Version 4.5.1 - P3-M2-07B Opposite Extreme Supersession', 1)

old = '''enum ENUM_EXTREME_MATURITY
{
   EXT_MAT_NONE,
   EXT_MAT_RAW,
   EXT_MAT_REVERSAL_CONFIRMED,
   EXT_MAT_RETEST_PHASE,
   EXT_MAT_RETEST_READY,
   EXT_MAT_VOID
};'''
new = '''enum ENUM_EXTREME_MATURITY
{
   EXT_MAT_NONE,
   EXT_MAT_RAW,
   EXT_MAT_REVERSAL_CONFIRMED,
   EXT_MAT_RETEST_PHASE,
   EXT_MAT_RETEST_READY,
   EXT_MAT_VOID,
   EXT_MAT_SUPERSEDED
};'''
if s.count(old) != 1:
    raise SystemExit(f'Extreme enum anchor count={s.count(old)}')
s = s.replace(old, new, 1)

anchor = '''void MarkExtremeLifecycleVoid(ExtremeLifecycleData &extreme,
                              TimeframeData &data, string reason)
{
   extreme.Maturity = EXT_MAT_VOID;
   extreme.IsValid = false;
   extreme.LastUpdateBar = data.barIndex;
   extreme.LastUpdateCandleTime = data.candle_time;
   extreme.PreviousClose = data.close;
   extreme.Reason = reason;
}
'''
insert = anchor + '''
bool IsExtremeCycleOwnerMature(ExtremeLifecycleData &extreme)
{
   if(!extreme.IsValid || extreme.ConfirmationCandleTime <= 0) return false;
   return (extreme.Maturity == EXT_MAT_REVERSAL_CONFIRMED ||
           extreme.Maturity == EXT_MAT_RETEST_PHASE ||
           extreme.Maturity == EXT_MAT_RETEST_READY);
}

void MarkExtremeLifecycleSuperseded(ExtremeLifecycleData &extreme,
                                    TimeframeData &data, string reason)
{
   extreme.Maturity = EXT_MAT_SUPERSEDED;
   extreme.IsValid = false;
   extreme.LastUpdateBar = data.barIndex;
   extreme.LastUpdateCandleTime = data.candle_time;
   extreme.PreviousClose = data.close;
   extreme.Reason = reason;
}

void ResolveOppositeExtremeSupersession(ExtremeLifecycleData &buyExtreme,
                                        ExtremeLifecycleData &sellExtreme,
                                        TimeframeData &data)
{
   if(!data.is_valid || !data.is_closed || data.candle_time <= 0) return;
   if(buyExtreme.Timeframe != data.timeframe || sellExtreme.Timeframe != data.timeframe) return;

   bool buyMature = IsExtremeCycleOwnerMature(buyExtreme);
   bool sellMature = IsExtremeCycleOwnerMature(sellExtreme);
   if(!buyMature || !sellMature) return;

   if(buyExtreme.ConfirmationCandleTime > sellExtreme.ConfirmationCandleTime)
      MarkExtremeLifecycleSuperseded(sellExtreme, data,
         "SELL Extreme superseded by newer reversal-confirmed opposite BUY Extreme");
   else if(sellExtreme.ConfirmationCandleTime > buyExtreme.ConfirmationCandleTime)
      MarkExtremeLifecycleSuperseded(buyExtreme, data,
         "BUY Extreme superseded by newer reversal-confirmed opposite SELL Extreme");
   // Equal confirmation time remains ambiguous; downstream conflict stays fail-closed.
}
'''
if s.count(anchor) != 1:
    raise SystemExit(f'Void anchor count={s.count(anchor)}')
s = s.replace(anchor, insert, 1)

old = '''   if(extreme.Maturity == EXT_MAT_VOID)
   {
      if(!rawDetected || data.candle_time <= extreme.LastUpdateCandleTime)
         return EXT_MAT_VOID;
      ResetExtremeLifecycle(extreme, direction, data.timeframe);
   }
'''
new = '''   if(extreme.Maturity == EXT_MAT_VOID || extreme.Maturity == EXT_MAT_SUPERSEDED)
   {
      ENUM_EXTREME_MATURITY terminalState = extreme.Maturity;
      if(!rawDetected || data.candle_time <= extreme.LastUpdateCandleTime)
         return terminalState;
      ResetExtremeLifecycle(extreme, direction, data.timeframe);
   }
'''
if s.count(old) != 1:
    raise SystemExit(f'Terminal lifecycle anchor count={s.count(old)}')
s = s.replace(old, new, 1)

old = '''   UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_m15_sell_lifecycle,
                          actual, DIR_SELL, g_pair_states[pairIndex].m15_data,
                          m15Band, m15RawSellExtreme);

   for(int dirIdx = 0; dirIdx < 2; dirIdx++)
'''
new = '''   UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_m15_sell_lifecycle,
                          actual, DIR_SELL, g_pair_states[pairIndex].m15_data,
                          m15Band, m15RawSellExtreme);
   ResolveOppositeExtremeSupersession(g_pair_states[pairIndex].extreme_m15_buy_lifecycle,
                                      g_pair_states[pairIndex].extreme_m15_sell_lifecycle,
                                      g_pair_states[pairIndex].m15_data);

   bool h1RawBuyExtreme = DetectExtreme(actual, DIR_BUY, g_pair_states[pairIndex].h1_data, h1Band);
   bool h1RawSellExtreme = DetectExtreme(actual, DIR_SELL, g_pair_states[pairIndex].h1_data, h1Band);
   UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_h1_buy_lifecycle, actual, DIR_BUY,
                          g_pair_states[pairIndex].h1_data, h1Band, h1RawBuyExtreme);
   UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_h1_sell_lifecycle, actual, DIR_SELL,
                          g_pair_states[pairIndex].h1_data, h1Band, h1RawSellExtreme);
   ResolveOppositeExtremeSupersession(g_pair_states[pairIndex].extreme_h1_buy_lifecycle,
                                      g_pair_states[pairIndex].extreme_h1_sell_lifecycle,
                                      g_pair_states[pairIndex].h1_data);

   bool h4RawBuyExtreme = DetectExtreme(actual, DIR_BUY, g_pair_states[pairIndex].h4_data, h4Band);
   bool h4RawSellExtreme = DetectExtreme(actual, DIR_SELL, g_pair_states[pairIndex].h4_data, h4Band);
   UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_h4_buy_lifecycle, actual, DIR_BUY,
                          g_pair_states[pairIndex].h4_data, h4Band, h4RawBuyExtreme);
   UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_h4_sell_lifecycle, actual, DIR_SELL,
                          g_pair_states[pairIndex].h4_data, h4Band, h4RawSellExtreme);
   ResolveOppositeExtremeSupersession(g_pair_states[pairIndex].extreme_h4_buy_lifecycle,
                                      g_pair_states[pairIndex].extreme_h4_sell_lifecycle,
                                      g_pair_states[pairIndex].h4_data);

   Signal resolvedH1BuyExtreme, resolvedH1SellExtreme, resolvedH4BuyExtreme, resolvedH4SellExtreme;
   ZeroMemory(resolvedH1BuyExtreme); ZeroMemory(resolvedH1SellExtreme);
   ZeroMemory(resolvedH4BuyExtreme); ZeroMemory(resolvedH4SellExtreme);
   ExportReversalConfirmedExtremeSignal(g_pair_states[pairIndex].extreme_h1_buy_lifecycle, resolvedH1BuyExtreme);
   ExportReversalConfirmedExtremeSignal(g_pair_states[pairIndex].extreme_h1_sell_lifecycle, resolvedH1SellExtreme);
   ExportReversalConfirmedExtremeSignal(g_pair_states[pairIndex].extreme_h4_buy_lifecycle, resolvedH4BuyExtreme);
   ExportReversalConfirmedExtremeSignal(g_pair_states[pairIndex].extreme_h4_sell_lifecycle, resolvedH4SellExtreme);
   UpdatePersistentExtremeState(resolvedH1BuyExtreme, g_pair_states[pairIndex].extreme_h1_buy_state);
   UpdatePersistentExtremeState(resolvedH1SellExtreme, g_pair_states[pairIndex].extreme_h1_sell_state);
   UpdatePersistentExtremeState(resolvedH4BuyExtreme, g_pair_states[pairIndex].extreme_h4_buy_state);
   UpdatePersistentExtremeState(resolvedH4SellExtreme, g_pair_states[pairIndex].extreme_h4_sell_state);

   for(int dirIdx = 0; dirIdx < 2; dirIdx++)
'''
if s.count(old) != 1:
    raise SystemExit(f'Pre-loop anchor count={s.count(old)}')
s = s.replace(old, new, 1)

old = '''      Signal detectedH1Extreme, detectedH4Extreme;
      ZeroMemory(detectedH1Extreme); ZeroMemory(detectedH4Extreme);

      bool h1RawExtreme = DetectExtreme(actual, direction,
                                        g_pair_states[pairIndex].h1_data, h1Band);
      if(direction == DIR_BUY)
      {
         UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_h1_buy_lifecycle,
                                actual, direction,
                                g_pair_states[pairIndex].h1_data, h1Band, h1RawExtreme);
         ExportReversalConfirmedExtremeSignal(
            g_pair_states[pairIndex].extreme_h1_buy_lifecycle, detectedH1Extreme);
      }
      else
      {
         UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_h1_sell_lifecycle,
                                actual, direction,
                                g_pair_states[pairIndex].h1_data, h1Band, h1RawExtreme);
         ExportReversalConfirmedExtremeSignal(
            g_pair_states[pairIndex].extreme_h1_sell_lifecycle, detectedH1Extreme);
      }
'''
new = '''      Signal detectedH1Extreme, detectedH4Extreme;
      ZeroMemory(detectedH1Extreme); ZeroMemory(detectedH4Extreme);
      if(direction == DIR_BUY)
      {
         detectedH1Extreme = resolvedH1BuyExtreme;
         detectedH4Extreme = resolvedH4BuyExtreme;
      }
      else
      {
         detectedH1Extreme = resolvedH1SellExtreme;
         detectedH4Extreme = resolvedH4SellExtreme;
      }
'''
if s.count(old) != 1:
    raise SystemExit(f'H1 loop anchor count={s.count(old)}')
s = s.replace(old, new, 1)

old = '''      if(direction == DIR_BUY)
      {
         UpdatePersistentExtremeState(detectedH1Extreme,
                                      g_pair_states[pairIndex].extreme_h1_buy_state);
         h1ExtremeSnapshot = g_pair_states[pairIndex].extreme_h1_buy_state;
      }
      else
      {
         UpdatePersistentExtremeState(detectedH1Extreme,
                                      g_pair_states[pairIndex].extreme_h1_sell_state);
         h1ExtremeSnapshot = g_pair_states[pairIndex].extreme_h1_sell_state;
      }
'''
new = '''      if(direction == DIR_BUY)
         h1ExtremeSnapshot = g_pair_states[pairIndex].extreme_h1_buy_state;
      else
         h1ExtremeSnapshot = g_pair_states[pairIndex].extreme_h1_sell_state;
'''
if s.count(old) != 1:
    raise SystemExit(f'H1 persistence anchor count={s.count(old)}')
s = s.replace(old, new, 1)

old = '''      bool h4RawExtreme = DetectExtreme(actual, direction,
                                        g_pair_states[pairIndex].h4_data, h4Band);
      if(direction == DIR_BUY)
      {
         UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_h4_buy_lifecycle,
                                actual, direction,
                                g_pair_states[pairIndex].h4_data, h4Band, h4RawExtreme);
         ExportReversalConfirmedExtremeSignal(
            g_pair_states[pairIndex].extreme_h4_buy_lifecycle, detectedH4Extreme);
         UpdatePersistentExtremeState(detectedH4Extreme,
                                      g_pair_states[pairIndex].extreme_h4_buy_state);
         h4ExtremeSnapshot = g_pair_states[pairIndex].extreme_h4_buy_state;
      }
      else
      {
         UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_h4_sell_lifecycle,
                                actual, direction,
                                g_pair_states[pairIndex].h4_data, h4Band, h4RawExtreme);
         ExportReversalConfirmedExtremeSignal(
            g_pair_states[pairIndex].extreme_h4_sell_lifecycle, detectedH4Extreme);
         UpdatePersistentExtremeState(detectedH4Extreme,
                                      g_pair_states[pairIndex].extreme_h4_sell_state);
         h4ExtremeSnapshot = g_pair_states[pairIndex].extreme_h4_sell_state;
      }
      h4_extreme = h4ExtremeSnapshot;
'''
new = '''      if(direction == DIR_BUY)
         h4ExtremeSnapshot = g_pair_states[pairIndex].extreme_h4_buy_state;
      else
         h4ExtremeSnapshot = g_pair_states[pairIndex].extreme_h4_sell_state;
      h4_extreme = h4ExtremeSnapshot;
'''
if s.count(old) != 1:
    raise SystemExit(f'H4 loop anchor count={s.count(old)}')
s = s.replace(old, new, 1)

for token in ['EXT_MAT_SUPERSEDED', 'ResolveOppositeExtremeSupersession(', 'resolvedH1BuyExtreme', 'resolvedH4BuyExtreme']:
    if token not in s:
        raise SystemExit('missing token: ' + token)
if s.count('{') != s.count('}'):
    raise SystemExit('brace imbalance')

SOURCE.write_text(s, encoding='utf-8')
print('P3-M2-07B patch applied')
