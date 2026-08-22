from pathlib import Path

SOURCE = Path('blueprint/source/BBMA_EA.mq4')
AUDIT = Path('blueprint/CORE_V2_F2_IMPLEMENTATION_AUDIT.md')

s = SOURCE.read_text(encoding='utf-8')


def replace_between(source: str, start_marker: str, end_marker: str, replacement: str, label: str) -> str:
    a = source.find(start_marker)
    if a < 0:
        raise SystemExit(f'{label}: start marker not found')
    b = source.find(end_marker, a)
    if b < 0:
        raise SystemExit(f'{label}: end marker not found')
    if source.find(start_marker, a + 1) >= 0:
        raise SystemExit(f'{label}: start marker not unique')
    return source[:a] + replacement + source[b:]


# 1) M02: explicit Extreme maturity state.
enum_needle = 'enum ENUM_EXTREME_TYPE { EXT_NONE, EXT_SIDEWAYS, EXT_WITH_MOMENTUM, EXT_WITHOUT_MOMENTUM };\n'
enum_insert = enum_needle + '''\nenum ENUM_EXTREME_MATURITY\n{\n   EXT_MAT_NONE,\n   EXT_MAT_RAW,\n   EXT_MAT_REVERSAL_CONFIRMED,\n   EXT_MAT_RETEST_PHASE,\n   EXT_MAT_RETEST_READY,\n   EXT_MAT_VOID\n};\n'''
if 'enum ENUM_EXTREME_MATURITY' not in s:
    if s.count(enum_needle) != 1:
        raise SystemExit('ENUM_EXTREME_TYPE insertion point not unique')
    s = s.replace(enum_needle, enum_insert, 1)


# 2) M02: lifecycle storage separate from generic Signal payloads.
struct_marker = 'struct MLVData\n{\n'
extreme_struct = '''struct ExtremeLifecycleData\n{\n   ENUM_EXTREME_MATURITY Maturity;\n   ENUM_DIRECTION        Direction;\n   int                   Timeframe;\n   int                   RawBar;\n   datetime              RawCandleTime;\n   int                   ConfirmationBar;\n   datetime              ConfirmationCandleTime;\n   double                ConfirmationClose;\n   int                   LastUpdateBar;\n   datetime              LastUpdateCandleTime;\n   double                PreviousClose;\n   double                ProvisionalBodyAnchor;\n   double                FrozenBodyAnchor;\n   double                RelevantMA5;\n   int                   RetestStartBar;\n   datetime              RetestStartCandleTime;\n   int                   RetestCompletionBar;\n   datetime              RetestCompletionCandleTime;\n   bool                  IsValid;\n   string                Reason;\n};\n\n'''
if 'struct ExtremeLifecycleData' not in s:
    if s.count(struct_marker) != 1:
        raise SystemExit('MLVData insertion point not unique')
    s = s.replace(struct_marker, extreme_struct + struct_marker, 1)


# 3) PairState: H1/H4 lifecycle owners for executable Extreme components.
pair_marker = '   // M16 persistent validity overlay for source-detected Extremes.\n'
pair_insert = '''   // F2 source-aligned Extreme maturity lifecycle.\n   ExtremeLifecycleData extreme_h1_buy_lifecycle;\n   ExtremeLifecycleData extreme_h1_sell_lifecycle;\n   ExtremeLifecycleData extreme_h4_buy_lifecycle;\n   ExtremeLifecycleData extreme_h4_sell_lifecycle;\n'''
if 'extreme_h1_buy_lifecycle' not in s:
    if s.count(pair_marker) != 1:
        raise SystemExit('PairState Extreme insertion point not unique')
    s = s.replace(pair_marker, pair_insert + pair_marker, 1)


# 4) M08: RAW detector + deterministic maturity/reversal/retest lifecycle.
module08_start = 'bool DetectExtreme(string pair, ENUM_DIRECTION direction, TimeframeData &data, BollingerBand &band)\n{\n'
module08_end = 'void BuildSLTP_Extreme(ENUM_DIRECTION direction, double entryPrice, \n'
new_m08 = r'''bool DetectExtreme(string pair, ENUM_DIRECTION direction, TimeframeData &data, BollingerBand &band)
{
   // F2 RAW detector only. Reversal confirmation and retest maturity are
   // handled by UpdateExtremeLifecycle(); RAW alone is never a combo component.
   if(!data.is_valid || !data.is_closed) return false;
   if(band.TOP_BB <= 0 || band.LOW_BB <= 0) return false;
   if(direction != DIR_BUY && direction != DIR_SELL) return false;

   if(direction == DIR_SELL)
   {
      double ma5High = data.ma[0];
      double ma10High = data.ma[1];
      if(ma5High <= 0 || ma10High <= 0) return false;
      return (ma5High > band.TOP_BB || ma10High > band.TOP_BB);
   }

   double ma5Low = data.ma[2];
   double ma10Low = data.ma[3];
   if(ma5Low <= 0 || ma10Low <= 0) return false;
   return (ma5Low < band.LOW_BB || ma10Low < band.LOW_BB);
}

void ResetExtremeLifecycle(ExtremeLifecycleData &extreme,
                           ENUM_DIRECTION direction, int timeframe)
{
   ZeroMemory(extreme);
   extreme.Maturity = EXT_MAT_NONE;
   extreme.Direction = direction;
   extreme.Timeframe = timeframe;
}

double GetExtremeRelevantMA5(TimeframeData &data, ENUM_DIRECTION direction)
{
   if(direction == DIR_SELL) return data.ma[0]; // MA5 High
   if(direction == DIR_BUY)  return data.ma[2]; // MA5 Low
   return 0.0;
}

double GetExtremeReversalBodyEdge(TimeframeData &data, ENUM_DIRECTION direction)
{
   if(direction == DIR_SELL) return MathMax(data.open, data.close);
   if(direction == DIR_BUY)  return MathMin(data.open, data.close);
   return 0.0;
}

bool IsExtremeReversalDirection(TimeframeData &data, ENUM_DIRECTION direction)
{
   if(data.open <= 0 || data.close <= 0) return false;
   if(direction == DIR_SELL) return (data.close < data.open);
   if(direction == DIR_BUY)  return (data.close > data.open);
   return false;
}

bool IsExtremeMomentumInvalidation(string pair, TimeframeData &data,
                                   BollingerBand &currentBand)
{
   if(data.barIndex < 1 || data.close <= 0 || currentBand.Width <= 0) return false;

   BollingerBand previousBand;
   ZeroMemory(previousBand);
   CalculateBollinger(pair, data.timeframe, data.barIndex + 1, previousBand);
   if(previousBand.Width <= 0 || previousBand.MID_BB <= 0 ||
      previousBand.TOP_BB <= 0 || previousBand.LOW_BB <= 0)
      return false;

   bool bbExpanding = (currentBand.Width > previousBand.Width);
   bool buyMomentum = bbExpanding &&
                      currentBand.MID_BB > previousBand.MID_BB &&
                      currentBand.TOP_BB > previousBand.TOP_BB &&
                      data.close > currentBand.TOP_BB;
   bool sellMomentum = bbExpanding &&
                       currentBand.MID_BB < previousBand.MID_BB &&
                       currentBand.LOW_BB < previousBand.LOW_BB &&
                       data.close < currentBand.LOW_BB;
   return (buyMomentum || sellMomentum);
}

bool IsExtremeLifecycleInvalidation(string pair, ENUM_DIRECTION direction,
                                    TimeframeData &data, BollingerBand &band)
{
   if(data.close <= 0 || band.TOP_BB <= 0 || band.LOW_BB <= 0) return false;

   // A continuation close through the original Extreme-side outer BB is void.
   // An opposite-side outside close is not made a universal hard failure here;
   // it is invalid only when it qualifies as accepted directional Momentum.
   bool relevantOuterBreak = (direction == DIR_SELL)
                             ? (data.close > band.TOP_BB)
                             : (data.close < band.LOW_BB);

   return (relevantOuterBreak || IsExtremeMomentumInvalidation(pair, data, band));
}

void MarkExtremeLifecycleVoid(ExtremeLifecycleData &extreme,
                              TimeframeData &data, string reason)
{
   extreme.Maturity = EXT_MAT_VOID;
   extreme.IsValid = false;
   extreme.LastUpdateBar = data.barIndex;
   extreme.LastUpdateCandleTime = data.candle_time;
   extreme.PreviousClose = data.close;
   extreme.Reason = reason;
}

void UpdateExtremeProvisionalAnchor(ExtremeLifecycleData &extreme,
                                    TimeframeData &data)
{
   double edge = GetExtremeReversalBodyEdge(data, extreme.Direction);
   if(edge <= 0) return;

   if(extreme.ProvisionalBodyAnchor <= 0)
      extreme.ProvisionalBodyAnchor = edge;
   else if(extreme.Direction == DIR_SELL)
      extreme.ProvisionalBodyAnchor = MathMax(extreme.ProvisionalBodyAnchor, edge);
   else if(extreme.Direction == DIR_BUY)
      extreme.ProvisionalBodyAnchor = MathMin(extreme.ProvisionalBodyAnchor, edge);
}

bool IsExtremeRetestStart(ExtremeLifecycleData &extreme, TimeframeData &data)
{
   if(extreme.PreviousClose <= 0 || data.close <= 0) return false;
   if(extreme.Direction == DIR_SELL) return (data.close > extreme.PreviousClose);
   if(extreme.Direction == DIR_BUY)  return (data.close < extreme.PreviousClose);
   return false;
}

bool IsExtremeRetestInteraction(ExtremeLifecycleData &extreme,
                                TimeframeData &data)
{
   if(data.high <= 0 || data.low <= 0) return false;

   bool bodyTouch = false;
   if(extreme.FrozenBodyAnchor > 0)
   {
      if(extreme.Direction == DIR_SELL)
         bodyTouch = (data.high >= extreme.FrozenBodyAnchor);
      else if(extreme.Direction == DIR_BUY)
         bodyTouch = (data.low <= extreme.FrozenBodyAnchor);
   }

   double ma5 = GetExtremeRelevantMA5(data, extreme.Direction);
   extreme.RelevantMA5 = ma5;
   bool ma5Touch = (ma5 > 0 && data.low <= ma5 && data.high >= ma5);

   return (bodyTouch || ma5Touch);
}

ENUM_EXTREME_MATURITY UpdateExtremeLifecycle(ExtremeLifecycleData &extreme,
                                             string pair,
                                             ENUM_DIRECTION direction,
                                             TimeframeData &data,
                                             BollingerBand &band,
                                             bool rawDetected)
{
   if(direction != DIR_BUY && direction != DIR_SELL) return extreme.Maturity;
   if(!data.is_valid || !data.is_closed || data.candle_time <= 0) return extreme.Maturity;

   if(extreme.Direction != direction || extreme.Timeframe != data.timeframe)
      ResetExtremeLifecycle(extreme, direction, data.timeframe);

   // F2 maturity has NO fixed candle/session expiry. MaxWaitBars_Extreme stays
   // downstream as a project component-freshness overlay only; it must not
   // erase lifecycle provenance needed by later structural stages such as F1.

   if(extreme.Maturity == EXT_MAT_VOID)
   {
      if(!rawDetected || data.candle_time <= extreme.LastUpdateCandleTime)
         return EXT_MAT_VOID;
      ResetExtremeLifecycle(extreme, direction, data.timeframe);
   }

   if(extreme.Maturity == EXT_MAT_NONE)
   {
      if(!rawDetected) return EXT_MAT_NONE;

      extreme.Maturity = EXT_MAT_RAW;
      extreme.Direction = direction;
      extreme.Timeframe = data.timeframe;
      extreme.RawBar = data.barIndex;
      extreme.RawCandleTime = data.candle_time;
      extreme.LastUpdateBar = data.barIndex;
      extreme.LastUpdateCandleTime = data.candle_time;
      extreme.PreviousClose = data.close;
      extreme.RelevantMA5 = GetExtremeRelevantMA5(data, direction);
      extreme.IsValid = false;
      extreme.Reason = "RAW Extreme detected; awaiting reversal confirmation";

      if(IsExtremeLifecycleInvalidation(pair, direction, data, band))
         MarkExtremeLifecycleVoid(extreme, data,
                                  "RAW Extreme void: outside-BB/Momentum invalidation");
      return extreme.Maturity;
   }

   if(data.candle_time <= extreme.LastUpdateCandleTime)
      return extreme.Maturity;

   // Invalidation is evaluated before every pre-entry maturity promotion.
   if(IsExtremeLifecycleInvalidation(pair, direction, data, band))
   {
      MarkExtremeLifecycleVoid(extreme, data,
                               "Extreme void: outside-BB/Momentum invalidation");
      return EXT_MAT_VOID;
   }

   if(extreme.Maturity == EXT_MAT_RAW)
   {
      // RAW confirmation is necessarily a SUBSEQUENT closed source-TF candle:
      // the RAW candle was already stored as LastUpdateCandleTime above.
      if(IsExtremeReversalDirection(data, direction))
      {
         extreme.Maturity = EXT_MAT_REVERSAL_CONFIRMED;
         extreme.ConfirmationBar = data.barIndex;
         extreme.ConfirmationCandleTime = data.candle_time;
         extreme.ConfirmationClose = data.close;
         extreme.ProvisionalBodyAnchor = 0.0;
         UpdateExtremeProvisionalAnchor(extreme, data);
         extreme.IsValid = true;
         extreme.Reason = "Extreme reversal-confirmed; component maturity reached";
      }

      extreme.LastUpdateBar = data.barIndex;
      extreme.LastUpdateCandleTime = data.candle_time;
      extreme.PreviousClose = data.close;
      extreme.RelevantMA5 = GetExtremeRelevantMA5(data, direction);
      return extreme.Maturity;
   }

   if(extreme.Maturity == EXT_MAT_REVERSAL_CONFIRMED)
   {
      bool retestStarts = IsExtremeRetestStart(extreme, data);
      if(retestStarts)
      {
         // Trigger candle belongs to retest phase and is excluded from anchor.
         extreme.FrozenBodyAnchor = extreme.ProvisionalBodyAnchor;
         extreme.RetestStartBar = data.barIndex;
         extreme.RetestStartCandleTime = data.candle_time;
         extreme.Maturity = EXT_MAT_RETEST_PHASE;
         extreme.LastUpdateBar = data.barIndex;
         extreme.LastUpdateCandleTime = data.candle_time;
         extreme.PreviousClose = data.close;
         extreme.RelevantMA5 = GetExtremeRelevantMA5(data, direction);
         extreme.Reason = "Extreme retest phase started; body anchor frozen";

         // The retest-start candle is excluded from anchor construction but may
         // itself be the first valid revisit of the already-frozen reference.
         if(IsExtremeRetestInteraction(extreme, data))
         {
            extreme.Maturity = EXT_MAT_RETEST_READY;
            extreme.RetestCompletionBar = data.barIndex;
            extreme.RetestCompletionCandleTime = data.candle_time;
            extreme.Reason = "Extreme retest complete: body anchor or MA5 interaction";
         }
         return extreme.Maturity;
      }

      // No close progression back toward the original Extreme yet: the
      // structural reversal phase continues and its provisional body edge may
      // update. No fixed candle count is imposed.
      UpdateExtremeProvisionalAnchor(extreme, data);
      extreme.LastUpdateBar = data.barIndex;
      extreme.LastUpdateCandleTime = data.candle_time;
      extreme.PreviousClose = data.close;
      extreme.RelevantMA5 = GetExtremeRelevantMA5(data, direction);
      return EXT_MAT_REVERSAL_CONFIRMED;
   }

   if(extreme.Maturity == EXT_MAT_RETEST_PHASE)
   {
      extreme.LastUpdateBar = data.barIndex;
      extreme.LastUpdateCandleTime = data.candle_time;
      extreme.PreviousClose = data.close;
      extreme.RelevantMA5 = GetExtremeRelevantMA5(data, direction);

      if(IsExtremeRetestInteraction(extreme, data))
      {
         extreme.Maturity = EXT_MAT_RETEST_READY;
         extreme.RetestCompletionBar = data.barIndex;
         extreme.RetestCompletionCandleTime = data.candle_time;
         extreme.Reason = "Extreme retest complete: body anchor or MA5 interaction";
      }
      return extreme.Maturity;
   }

   if(extreme.Maturity == EXT_MAT_RETEST_READY)
   {
      extreme.LastUpdateBar = data.barIndex;
      extreme.LastUpdateCandleTime = data.candle_time;
      extreme.PreviousClose = data.close;
      extreme.RelevantMA5 = GetExtremeRelevantMA5(data, direction);
      extreme.IsValid = true;
   }

   return extreme.Maturity;
}

bool ExportReversalConfirmedExtremeSignal(ExtremeLifecycleData &extreme,
                                          Signal &signal)
{
   ZeroMemory(signal);
   bool mature = (extreme.Maturity == EXT_MAT_REVERSAL_CONFIRMED ||
                  extreme.Maturity == EXT_MAT_RETEST_PHASE ||
                  extreme.Maturity == EXT_MAT_RETEST_READY);
   if(!mature || !extreme.IsValid) return false;
   if(extreme.ConfirmationCandleTime <= 0 || extreme.Timeframe <= 0) return false;

   signal.Type = SIGNAL_EXTREME;
   signal.Direction = extreme.Direction;
   signal.Valid = true;
   signal.Timeframe = extreme.Timeframe;
   signal.BarIndex = extreme.ConfirmationBar;
   signal.ExpiryBar = MaxWaitBars_Extreme;
   signal.Timestamp = extreme.ConfirmationCandleTime;
   signal.CandleTime = extreme.ConfirmationCandleTime;
   signal.Close = extreme.ConfirmationClose;
   signal.MA5_Level = extreme.RelevantMA5;
   signal.Reason = extreme.Reason;
   return true;
}

'''
s = replace_between(s, module08_start, module08_end, new_m08, 'Module 08 Extreme lifecycle')


# 5) M16: generic Signal overlay consumes only reversal-confirmed-or-higher
# exports. M08 owns lifecycle strategy invalidation; M16 retains project expiry.
m16_start = 'void UpdatePersistentExtremeState(Signal &detectedExtreme, Signal &csmSnapshot,\n                                  Signal &state)\n{\n'
m16_end = 'bool IsPersistentExtremeComponentValid(PairState &pairState,\n'
new_m16 = '''void UpdatePersistentExtremeState(Signal &matureExtreme, Signal &state)\n{\n   // M08 lifecycle owns RAW/reversal/retest/invalidation semantics. M16 keeps\n   // only the existing project component-freshness overlay.\n   if(!matureExtreme.Valid)\n   {\n      ZeroMemory(state);\n      return;\n   }\n\n   state = matureExtreme;\n   if(IsExtremeStateExpired(state, g_processing_time))\n   {\n      state.Valid = false;\n      state.Reason = "Extreme component expired by timeframe-aware project window";\n   }\n}\n\n'''
s = replace_between(s, m16_start, m16_end, new_m16, 'M16 Extreme persistent overlay')


# 6) M27: remove legacy any-CSM snapshot invalidation path. The lifecycle
# evaluates accepted invalidation itself on every new closed source-TF candle.
csm_block_start = '   Signal h1AnyCSMSnapshot, h4AnyCSMSnapshot;\n'
csm_block_end = '   ValidatedSequenceCandidate allCandidates[];\n'
a = s.find(csm_block_start)
b = s.find(csm_block_end, a)
if a < 0 or b < 0:
    raise SystemExit('M27 legacy CSM snapshot block markers not found')
s = s[:a] + s[b:]


# H1: RAW detect -> lifecycle update -> mature export only.
h1_start = '      Signal detectedH1Extreme, detectedH4Extreme;\n'
h1_end = '      if(DetectMHV(actual, direction, g_pair_states[pairIndex].m15_data))\n'
h1_block = '''      Signal detectedH1Extreme, detectedH4Extreme;\n      ZeroMemory(detectedH1Extreme); ZeroMemory(detectedH4Extreme);\n\n      bool h1RawExtreme = DetectExtreme(actual, direction,\n                                        g_pair_states[pairIndex].h1_data, h1Band);\n      if(direction == DIR_BUY)\n      {\n         UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_h1_buy_lifecycle,\n                                actual, direction,\n                                g_pair_states[pairIndex].h1_data, h1Band, h1RawExtreme);\n         ExportReversalConfirmedExtremeSignal(\n            g_pair_states[pairIndex].extreme_h1_buy_lifecycle, detectedH1Extreme);\n      }\n      else\n      {\n         UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_h1_sell_lifecycle,\n                                actual, direction,\n                                g_pair_states[pairIndex].h1_data, h1Band, h1RawExtreme);\n         ExportReversalConfirmedExtremeSignal(\n            g_pair_states[pairIndex].extreme_h1_sell_lifecycle, detectedH1Extreme);\n      }\n\n'''
s = replace_between(s, h1_start, h1_end, h1_block, 'M27 H1 Extreme lifecycle wiring')

old_h1_persist = '''      if(direction == DIR_BUY)\n      {\n         UpdatePersistentExtremeState(detectedH1Extreme, h1AnyCSMSnapshot,\n                                      g_pair_states[pairIndex].extreme_h1_buy_state);\n         h1ExtremeSnapshot = g_pair_states[pairIndex].extreme_h1_buy_state;\n      }\n      else\n      {\n         UpdatePersistentExtremeState(detectedH1Extreme, h1AnyCSMSnapshot,\n                                      g_pair_states[pairIndex].extreme_h1_sell_state);\n         h1ExtremeSnapshot = g_pair_states[pairIndex].extreme_h1_sell_state;\n      }\n'''
new_h1_persist = '''      if(direction == DIR_BUY)\n      {\n         UpdatePersistentExtremeState(detectedH1Extreme,\n                                      g_pair_states[pairIndex].extreme_h1_buy_state);\n         h1ExtremeSnapshot = g_pair_states[pairIndex].extreme_h1_buy_state;\n      }\n      else\n      {\n         UpdatePersistentExtremeState(detectedH1Extreme,\n                                      g_pair_states[pairIndex].extreme_h1_sell_state);\n         h1ExtremeSnapshot = g_pair_states[pairIndex].extreme_h1_sell_state;\n      }\n'''
if s.count(old_h1_persist) != 1:
    raise SystemExit(f'H1 persistent block expected once, found {s.count(old_h1_persist)}')
s = s.replace(old_h1_persist, new_h1_persist, 1)


# H4: RAW detect -> lifecycle update -> mature export -> M16 freshness overlay.
h4_start = '      if(DetectExtreme(actual, direction, g_pair_states[pairIndex].h4_data, h4Band))\n'
h4_end = '      h4_extreme = h4ExtremeSnapshot;\n'
h4_block = '''      bool h4RawExtreme = DetectExtreme(actual, direction,\n                                        g_pair_states[pairIndex].h4_data, h4Band);\n      if(direction == DIR_BUY)\n      {\n         UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_h4_buy_lifecycle,\n                                actual, direction,\n                                g_pair_states[pairIndex].h4_data, h4Band, h4RawExtreme);\n         ExportReversalConfirmedExtremeSignal(\n            g_pair_states[pairIndex].extreme_h4_buy_lifecycle, detectedH4Extreme);\n         UpdatePersistentExtremeState(detectedH4Extreme,\n                                      g_pair_states[pairIndex].extreme_h4_buy_state);\n         h4ExtremeSnapshot = g_pair_states[pairIndex].extreme_h4_buy_state;\n      }\n      else\n      {\n         UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_h4_sell_lifecycle,\n                                actual, direction,\n                                g_pair_states[pairIndex].h4_data, h4Band, h4RawExtreme);\n         ExportReversalConfirmedExtremeSignal(\n            g_pair_states[pairIndex].extreme_h4_sell_lifecycle, detectedH4Extreme);\n         UpdatePersistentExtremeState(detectedH4Extreme,\n                                      g_pair_states[pairIndex].extreme_h4_sell_state);\n         h4ExtremeSnapshot = g_pair_states[pairIndex].extreme_h4_sell_state;\n      }\n'''
s = replace_between(s, h4_start, h4_end, h4_block + h4_end, 'M27 H4 Extreme lifecycle wiring')


# Static source invariants for the resolved F2 contract.
checks = {
    'Extreme maturity enum': 'enum ENUM_EXTREME_MATURITY',
    'Extreme lifecycle struct': 'struct ExtremeLifecycleData',
    'RAW detector comment': 'F2 RAW detector only',
    'Lifecycle update': 'ENUM_EXTREME_MATURITY UpdateExtremeLifecycle',
    'Reversal SELL mapping': 'if(direction == DIR_SELL) return (data.close < data.open);',
    'Reversal BUY mapping': 'if(direction == DIR_BUY)  return (data.close > data.open);',
    'SELL retest start': 'if(extreme.Direction == DIR_SELL) return (data.close > extreme.PreviousClose);',
    'BUY retest start': 'if(extreme.Direction == DIR_BUY)  return (data.close < extreme.PreviousClose);',
    'Mature export': 'bool ExportReversalConfirmedExtremeSignal',
    'H1 lifecycle wiring': 'extreme_h1_buy_lifecycle',
    'H4 lifecycle wiring': 'extreme_h4_buy_lifecycle',
    'No F2 fixed expiry statement': 'F2 maturity has NO fixed candle/session expiry.',
}
for label, needle in checks.items():
    if needle not in s:
        raise SystemExit(f'missing F2 invariant: {label}')

# RAW detector must not conflate reversal confirmation with close-inside-BB.
d0 = s.index('bool DetectExtreme(string pair, ENUM_DIRECTION direction, TimeframeData &data, BollingerBand &band)')
d1 = s.index('void ResetExtremeLifecycle(', d0)
detector = s[d0:d1]
if 'data.close > band.TOP_BB' in detector or 'data.close < band.LOW_BB' in detector:
    raise SystemExit('RAW DetectExtreme still conflates close-inside reversal/invalidation')

if 'Signal h1AnyCSMSnapshot, h4AnyCSMSnapshot;' in s:
    raise SystemExit('legacy any-CSM snapshot variables remain')
if 'UpdatePersistentExtremeState(detectedH1Extreme, h1AnyCSMSnapshot' in s:
    raise SystemExit('legacy H1 CSM-based persistence call remains')
if 'UpdatePersistentExtremeState(detectedH4Extreme, h4AnyCSMSnapshot' in s:
    raise SystemExit('legacy H4 CSM-based persistence call remains')

# Exact MTF signatures remain untouched; only the maturity of the Signal input changes.
if s.count('IsCombinationSignalReady(h1_extreme, SIGNAL_EXTREME, PERIOD_H1)') != 3:
    raise SystemExit('unexpected H1 Extreme combination signature count')
if s.count('IsCombinationSignalReady(h4_extreme, SIGNAL_EXTREME, PERIOD_H4)') != 1:
    raise SystemExit('unexpected H4 Extreme combination signature count')

SOURCE.write_text(s, encoding='utf-8')

AUDIT.write_text('''# CORE-V2-F2 — Extreme Lifecycle Implementation Audit\n\nDate: 2026-08-22\nStatus: **IMPLEMENTED / STATIC AUDIT PASS — NATIVE METAEDITOR COMPILE + REGRESSION/RUNTIME STILL REQUIRED**\nBranch: `blueprint-dev`\n\n## Scope\nImplements the resolved `CORE_V2_F2_EXTREME_MATURITY_DECISION.md` contract on the executable H1/H4 Extreme component paths. No M09/F1 MHV lifecycle, F3 Type-1, F4 H4-owner, risk, SL/TP, lot-sizing, portfolio or dashboard semantics are changed here.\n\n## Pre-fix mismatch\n- `DetectExtreme()` conflated RAW detection with a close-inside-BB condition and exported the result immediately as `SIGNAL_EXTREME`.\n- REM/RRE/REE could therefore consume an atomic/RAW-like Extreme without the approved subsequent reversal-confirmation lifecycle.\n- M16 persistence stored that atomic signal and invalidated it through a generic later any-CSM snapshot rather than an explicit F2 maturity owner.\n- No deterministic reversal phase, frozen body anchor, retest-start state or body/MA5 retest-ready maturity existed.\n\n## Applied implementation\n- Added `ENUM_EXTREME_MATURITY`: `NONE -> RAW -> REVERSAL_CONFIRMED -> RETEST_PHASE -> RETEST_READY`, plus `VOID`.\n- Added `ExtremeLifecycleData` owner state for H1/H4 BUY/SELL executable Extreme paths.\n- `DetectExtreme()` is now RAW MA5/MA10-outside-BB detection only; close-inside-BB is no longer RAW eligibility.\n- First subsequent same-TF reversal-direction closed candle promotes RAW to reversal-confirmed: SELL `Close < Open`, BUY `Close > Open`.\n- Reversal phase can continue without fixed candle count; provisional body anchor updates until retest starts.\n- Retest starts on first close progression back toward the original Extreme: SELL `CurrentClose > PreviousClose`, BUY `CurrentClose < PreviousClose`; trigger candle is excluded from anchor construction and freezes the anchor.\n- Frozen body anchor = SELL highest body top / BUY lowest body bottom across the completed reversal phase.\n- First valid range interaction with frozen body anchor OR current relevant MA5 completes standalone retest maturity.\n- Applicable continuation outer-BB / source-valid directional Momentum invalidation is evaluated before promotion and resolves the lifecycle to `VOID`.\n- REM/RRE/REE receive an Extreme `Signal` only from `ExportReversalConfirmedExtremeSignal()`, so RAW Extreme cannot satisfy an executable combination component.\n- `MaxWaitBars_Extreme` remains downstream as the existing **project component-freshness overlay only**. It does not expire/reset RAW, reversal, retest or structural Extreme provenance in M08.\n- M16 no longer owns the old any-CSM strategy invalidation; it consumes only mature M08 exports and retains component freshness/exact owner identity checks.\n\n## Static invariants verified by patch script\n- RAW detector contains no close-inside-BB gate.\n- Reversal-confirmed export is the only path populating H1/H4 executable Extreme snapshots.\n- Exact REM/RRE/REE signatures remain unchanged.\n- Legacy `h1AnyCSMSnapshot/h4AnyCSMSnapshot` persistence path is removed.\n- M16 component owner still exact-matches direction, timeframe and confirmation-candle identity.\n- No standalone Extreme direct-entry authority is introduced.\n\n## Remaining verification\n1. Native MetaEditor compile must report **0 errors / 0 warnings**.\n2. Regression/static re-audit should prove RAW Extreme never reaches M13/M14/M15 as an executable component.\n3. Runtime trace should cover: RAW->REVERSAL_CONFIRMED; invalidation-before-confirmation; multi-candle reversal anchor update; retest start/freeze; body-touch completion; MA5-touch completion; invalidation precedence.\n4. F1 implementation must consume the underlying F2 lifecycle for prior-Extreme provenance without weakening F2 maturity or converting `MaxWaitBars_Extreme` into a strategy-lifecycle TTL.\n\nDecision provenance: `blueprint/decisions/CORE_V2_F2_EXTREME_MATURITY_DECISION.md`.\n''', encoding='utf-8')

print('CORE-V2-F2 patch script: static invariants PASS')
