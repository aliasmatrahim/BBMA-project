from pathlib import Path
import re

SRC = Path('blueprint/source/BBMA_EA.mq4')
s = SRC.read_text(encoding='utf-8')

BASE_BLOB = '2285b90b82c4512b50279bb3546f9801dbc652a3'


def one(old: str, new: str, label: str):
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 occurrence, found {n}')
    s = s.replace(old, new, 1)


def block(start: str, end: str, transform, label: str):
    global s
    i = s.find(start)
    if i < 0:
        raise SystemExit(f'{label}: start anchor missing')
    j = s.find(end, i)
    if j < 0:
        raise SystemExit(f'{label}: end anchor missing')
    old = s[i:j]
    new = transform(old)
    if old == new:
        raise SystemExit(f'{label}: transform made no change')
    s = s[:i] + new + s[j:]


# Build identity.
one('Version 4.5.7 - N1.1 NMJE Coverage Overlay',
    'Version 4.5.8 - D1 TP-Wajib Lifecycle Stage', 'header version')
one('#property version   "4.57"', '#property version   "4.58"', 'property version')

# Separate fail-safe feature gate. It remains OFF until broker/demo validation.
one('bool           EnableC044Lifecycle                = false;\n',
    'bool           EnableC044Lifecycle                = false;\n'
    '// D1 EXTREME_TPW staged lifecycle. Keep OFF until native/static gates and\n'
    '// broker/demo restart + close-idempotency validation are complete.\n'
    'bool           EnableD1TPWLifecycle               = false;\n',
    'D1 TPW gate')

# Decision payload gets an explicit lifecycle owner distinct from C044.
one('   bool                 C044LifecycleManaged;\n   ENUM_DECISION_STATE  DecisionState;',
    '   bool                 C044LifecycleManaged;\n'
    '   bool                 D1TPWLifecycleManaged;\n'
    '   ENUM_DECISION_STATE  DecisionState;',
    'decision lifecycle flag')

# Trade registry gets an independent D1 TPW checkpoint/latch state.
one('   ExtremeLifecycleData c044_replay_extreme_sell;\n\n   ENUM_RECOVERY_STATE  recovery_state;',
    '   ExtremeLifecycleData c044_replay_extreme_sell;\n\n'
    '   // D1 Extreme TP-Wajib lifecycle. Independent of C044.\n'
    '   bool                 d1_tpw_lifecycle_managed;\n'
    '   datetime             d1_tpw_extreme_candle;\n'
    '   datetime             d1_tpw_last_processed_d1_candle;\n'
    '   bool                 d1_tpw_exit_latched;\n'
    '   datetime             d1_tpw_exit_latched_candle;\n'
    '   bool                 d1_tpw_frozen;\n\n'
    '   ENUM_RECOVERY_STATE  recovery_state;',
    'trade TPW fields')

# One canonical TPW candle predicate, reused by journey and live lifecycle.
pattern = re.compile(r'bool D1OpportunityTPWCompletedSince\(string pair, ExtremeLifecycleData &extreme,\n\s*TimeframeData &latestClosedD1\)\n\{.*?\n\}\n\nvoid InstallD1OpportunityJourney', re.S)
m = pattern.search(s)
if not m:
    raise SystemExit('D1OpportunityTPWCompletedSince block missing')
replacement = r'''bool IsD1TPWCompletionAtShift(string pair, ENUM_DIRECTION direction, int shift)
{
   if(pair == "" || shift < 1) return false;
   double high = iHigh(pair, PERIOD_D1, shift);
   double low = iLow(pair, PERIOD_D1, shift);
   if(high <= 0.0 || low <= 0.0 || high < low) return false;

   if(direction == DIR_SELL)
   {
      double ma5Low = BBMALowMA(pair, PERIOD_D1, MA5_LOW_PERIOD, shift);
      double ma10Low = BBMALowMA(pair, PERIOD_D1, MA10_LOW_PERIOD, shift);
      if(ma5Low <= 0.0 || ma10Low <= 0.0) return false;
      return (low <= ma5Low || low <= ma10Low);
   }

   if(direction == DIR_BUY)
   {
      double ma5High = BBMAHighMA(pair, PERIOD_D1, MA5_HIGH_PERIOD, shift);
      double ma10High = BBMAHighMA(pair, PERIOD_D1, MA10_HIGH_PERIOD, shift);
      if(ma5High <= 0.0 || ma10High <= 0.0) return false;
      return (high >= ma5High || high >= ma10High);
   }

   return false;
}

bool D1OpportunityTPWCompletedSince(string pair, ExtremeLifecycleData &extreme,
                                    TimeframeData &latestClosedD1)
{
   if(!D1OpportunityExtremeMature(extreme)) return true;
   if(!latestClosedD1.is_valid || !latestClosedD1.is_closed ||
      latestClosedD1.timeframe != PERIOD_D1 || latestClosedD1.barIndex < 1)
      return true;

   int confirmationShift = iBarShift(pair, PERIOD_D1,
                                     extreme.ConfirmationCandleTime, true);
   int latestShift = latestClosedD1.barIndex;
   if(confirmationShift < 1 || latestShift < 1) return true;
   if(confirmationShift < latestShift) return true;
   if(confirmationShift == latestShift) return false;

   for(int shift = confirmationShift - 1; shift >= latestShift; shift--)
   {
      datetime barTime = iTime(pair, PERIOD_D1, shift);
      if(barTime <= 0) return true; // fail closed on incomplete history

      double high = iHigh(pair, PERIOD_D1, shift);
      double low = iLow(pair, PERIOD_D1, shift);
      if(high <= 0.0 || low <= 0.0 || high < low) return true;

      // Invalid MA history is fail-closed for opportunity activation.
      if(extreme.Direction == DIR_SELL)
      {
         double ma5Low = BBMALowMA(pair, PERIOD_D1, MA5_LOW_PERIOD, shift);
         double ma10Low = BBMALowMA(pair, PERIOD_D1, MA10_LOW_PERIOD, shift);
         if(ma5Low <= 0.0 || ma10Low <= 0.0) return true;
      }
      else if(extreme.Direction == DIR_BUY)
      {
         double ma5High = BBMAHighMA(pair, PERIOD_D1, MA5_HIGH_PERIOD, shift);
         double ma10High = BBMAHighMA(pair, PERIOD_D1, MA10_HIGH_PERIOD, shift);
         if(ma5High <= 0.0 || ma10High <= 0.0) return true;
      }
      else return true;

      if(IsD1TPWCompletionAtShift(pair, extreme.Direction, shift)) return true;
   }
   return false;
}

void InstallD1OpportunityJourney'''
s = s[:m.start()] + replacement + s[m.end():]

# M17: source identity is independent of feature gate; gate OFF fails closed instead
# of silently reverting EXTREME_TPW to the LTF Re-Entry outer-BB TP.
insert_before = 'bool ResolveApprovedInitialSLTP(BBMA_Decision &decision,\n                                RiskValidationSnapshot &snapshot)\n'
helper = r'''bool IsD1TPWLifecycleIdentity(BBMA_Decision &decision)
{
   return (decision.D1AuthorityMode == D1_AUTH_OPPORTUNITY &&
           decision.D1OpportunitySnapshotValid &&
           decision.D1OpportunityFamily == D1_OPP_EXTREME_TPW &&
           decision.D1OpportunitySourceSignal == SIGNAL_EXTREME &&
           decision.D1OpportunityDirection == decision.Direction &&
           decision.D1OpportunitySourceCandleTime > 0 &&
           decision.D1OpportunityCycleID != "");
}

bool IsTargetlessLifecycleDecision(BBMA_Decision &decision)
{
   return (decision.C044LifecycleManaged || decision.D1TPWLifecycleManaged);
}

'''
one(insert_before, helper + insert_before, 'M17 helper insertion')


def transform_resolver(b: str) -> str:
    anchor = ('   if(!IsApprovedSLTPSourceComponent(decision,\n'
              '                                     decision.SLTPSourceComponent))\n'
              '      return false;\n')
    if b.count(anchor) != 1:
        raise SystemExit('resolver source anchor mismatch')
    b = b.replace(anchor, anchor +
        '\n   bool d1TPWLifecycle = IsD1TPWLifecycleIdentity(decision);\n'
        '   if(d1TPWLifecycle && !EnableD1TPWLifecycle)\n'
        '      return false; // never execute EXTREME_TPW with the legacy RE outer-BB TP\n'
        '   d1TPWLifecycle = d1TPWLifecycle && EnableD1TPWLifecycle;\n'
        '   bool c044Lifecycle = EnableC044Lifecycle && !d1TPWLifecycle;\n'
        '   bool targetlessLifecycle = (d1TPWLifecycle || c044Lifecycle);\n', 1)
    n = b.count('if(!EnableC044Lifecycle)')
    if n != 2:
        raise SystemExit(f'resolver expected 2 C044 destination guards, found {n}')
    b = b.replace('if(!EnableC044Lifecycle)', 'if(!targetlessLifecycle)')
    old = ('   decision.StopLoss = normalizedSL;\n'
           '   decision.TakeProfit = EnableC044Lifecycle ? 0.0 : normalizedTP;\n'
           '   decision.SLTPSource = decision.SLTPSourceComponent.ComponentType;\n'
           '   decision.C044LifecycleManaged = EnableC044Lifecycle;')
    new = ('   decision.StopLoss = normalizedSL;\n'
           '   decision.TakeProfit = targetlessLifecycle ? 0.0 : normalizedTP;\n'
           '   decision.SLTPSource = decision.SLTPSourceComponent.ComponentType;\n'
           '   decision.D1TPWLifecycleManaged = d1TPWLifecycle;\n'
           '   decision.C044LifecycleManaged = c044Lifecycle;')
    if b.count(old) != 1:
        raise SystemExit('resolver assignment block mismatch')
    b = b.replace(old, new, 1)
    oldlog = '            " C044=", decision.C044LifecycleManaged ? "Y" : "N");'
    newlog = ('            " C044=", decision.C044LifecycleManaged ? "Y" : "N",\n'
              '            " D1TPW=", decision.D1TPWLifecycleManaged ? "Y" : "N");')
    if b.count(oldlog) != 1:
        raise SystemExit('resolver log block mismatch')
    return b.replace(oldlog, newlog, 1)

block('bool ResolveApprovedInitialSLTP(BBMA_Decision &decision,\n',
      'double GetDirectionalClosePrice(', transform_resolver, 'M17 resolver')

# General targetless validation applies equally to C044 and D1 TPW.
def transform_m17_validation(b: str) -> str:
    b2 = b.replace('if(decision.C044LifecycleManaged)',
                   'if(IsTargetlessLifecycleDecision(decision))')
    if b2 == b:
        raise SystemExit('M17 validation targetless replacements missing')
    b2 = b2.replace('// C044 targetless lifecycle has no deterministic reward coordinate.',
                    '// Targetless lifecycle has no deterministic reward coordinate.')
    return b2

block('bool HasSourceResolvedSLTP(BBMA_Decision &decision)\n',
      '//+------------------------------------------------------------------+\n//| MODULE 18:',
      transform_m17_validation, 'M17 validation')

# Closed registry cleanup must clear either lifecycle checkpoint.
one('         if(g_monitored_trades[i].c044_lifecycle_managed)\n            ClearC044Checkpoint(g_monitored_trades[i]);\n',
    '         if(g_monitored_trades[i].c044_lifecycle_managed)\n            ClearC044Checkpoint(g_monitored_trades[i]);\n'
    '         if(g_monitored_trades[i].d1_tpw_lifecycle_managed)\n            ClearD1TPWCheckpoint(g_monitored_trades[i]);\n',
    'registry checkpoint cleanup')

# ProcessEntry accepts either targetless lifecycle and initializes exactly one.
def transform_process_entry(b: str) -> str:
    old = ('   bool tpPayloadValid = decision.C044LifecycleManaged\n'
           '      ? (decision.TakeProfit == 0.0)\n'
           '      : (decision.TakeProfit > 0.0);\n\n'
           '   if(decision.C044LifecycleManaged &&')
    new = ('   bool targetlessLifecycle = IsTargetlessLifecycleDecision(decision);\n'
           '   bool tpPayloadValid = targetlessLifecycle\n'
           '      ? (decision.TakeProfit == 0.0)\n'
           '      : (decision.TakeProfit > 0.0);\n\n'
           '   if(targetlessLifecycle &&')
    if b.count(old) != 1:
        raise SystemExit('ProcessEntry payload block mismatch')
    b = b.replace(old, new, 1)

    old = ('         ResetC044TradeState(info);\n'
           '         bool c044StateReady = true;\n'
           '         if(decision.C044LifecycleManaged)\n'
           '            c044StateReady = InitializeC044TradeStateFromDecision(info, decision);')
    new = ('         ResetC044TradeState(info);\n'
           '         ResetD1TPWTradeState(info);\n'
           '         bool lifecycleStateReady = true;\n'
           '         if(decision.D1TPWLifecycleManaged)\n'
           '            lifecycleStateReady = InitializeD1TPWTradeStateFromDecision(info, decision);\n'
           '         else if(decision.C044LifecycleManaged)\n'
           '            lifecycleStateReady = InitializeC044TradeStateFromDecision(info, decision);')
    if b.count(old) != 1:
        raise SystemExit('ProcessEntry lifecycle init mismatch')
    b = b.replace(old, new, 1)

    old = ('         info.execution_hash = persistedHashMatch ? persistedExecutionHash : "";\n'
           '         info.recovery_state = c044StateReady ? REC_NORMAL : REC_IDENTITY_MISSING_FROZEN;\n'
           '         if(info.c044_lifecycle_managed && c044StateReady && !SaveC044Checkpoint(info))\n'
           '         {\n'
           '            info.recovery_state = REC_IDENTITY_MISSING_FROZEN;\n'
           '            Log(DBG_ERROR, "C044 checkpoint persist failed ticket=" + IntegerToString(ticket));\n'
           '         }')
    new = ('         info.execution_hash = persistedHashMatch ? persistedExecutionHash : "";\n'
           '         info.recovery_state = lifecycleStateReady ? REC_NORMAL : REC_IDENTITY_MISSING_FROZEN;\n'
           '         if(info.d1_tpw_lifecycle_managed && lifecycleStateReady &&\n'
           '            !SaveD1TPWCheckpoint(info))\n'
           '         {\n'
           '            info.recovery_state = REC_IDENTITY_MISSING_FROZEN;\n'
           '            Log(DBG_ERROR, "D1TPW checkpoint persist failed ticket=" + IntegerToString(ticket));\n'
           '         }\n'
           '         else if(info.c044_lifecycle_managed && lifecycleStateReady &&\n'
           '                 !SaveC044Checkpoint(info))\n'
           '         {\n'
           '            info.recovery_state = REC_IDENTITY_MISSING_FROZEN;\n'
           '            Log(DBG_ERROR, "C044 checkpoint persist failed ticket=" + IntegerToString(ticket));\n'
           '         }')
    if b.count(old) != 1:
        raise SystemExit('ProcessEntry checkpoint block mismatch')
    return b.replace(old, new, 1)

block('void ProcessEntry(BBMA_Decision &decision, string pair,\n',
      '//+------------------------------------------------------------------+\n//| MODULE 23:',
      transform_process_entry, 'ProcessEntry')

# M23 D1 TPW event/close owner. Uses the same canonical TPW candle predicate.
d1_m23 = r'''
// D1TPW-01: lifecycle evidence is consumed on the M15 processing clock only.
// The D1 Extreme remains TP semantic owner; M23 only latches/executes full close.
bool FreezeD1TPWLifecycle(TradeInfo &info, string reason)
{
   if(!info.d1_tpw_lifecycle_managed) return false;
   info.d1_tpw_frozen = true;
   info.d1_tpw_exit_latched = false;
   info.d1_tpw_exit_latched_candle = 0;
   info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
   if(!SaveD1TPWCheckpoint(info))
      Log(DBG_ERROR, "D1TPW freeze checkpoint failed ticket=" + IntegerToString(info.ticket));
   Log(DBG_ERROR, "D1TPW lifecycle frozen ticket=" + IntegerToString(info.ticket) +
       " pair=" + info.pair + " reason=" + reason);
   return false;
}

bool LatchD1TPWExit(TradeInfo &info, datetime candleTime)
{
   if(!EnableD1TPWLifecycle || !info.d1_tpw_lifecycle_managed ||
      info.d1_tpw_frozen || candleTime <= 0)
      return false;
   if(info.d1_tpw_exit_latched)
      return (info.d1_tpw_exit_latched_candle == candleTime);

   info.d1_tpw_exit_latched = true;
   info.d1_tpw_exit_latched_candle = candleTime;
   if(!SaveD1TPWCheckpoint(info))
      return FreezeD1TPWLifecycle(info, "EXIT_LATCH_CHECKPOINT_FAILED");
   return true;
}

bool ProcessD1TPWClosedCandle(TradeInfo &info, int pairIndex, datetime candleTime)
{
   if(!EnableD1TPWLifecycle || !info.d1_tpw_lifecycle_managed) return true;
   if(info.d1_tpw_frozen || info.d1_tpw_exit_latched) return true;
   if(pairIndex < 0 || pairIndex >= g_pair_count || candleTime <= 0 ||
      info.d1_tpw_extreme_candle <= 0 || candleTime <= info.d1_tpw_extreme_candle)
      return FreezeD1TPWLifecycle(info, "INVALID_D1_EVENT_IDENTITY");

   string pair = g_pair_states[pairIndex].actual_symbol;
   if(pair == "" || pair != info.pair)
      return FreezeD1TPWLifecycle(info, "PAIR_MISMATCH");

   int shift = iBarShift(pair, PERIOD_D1, candleTime, true);
   if(shift < 1 || iTime(pair, PERIOD_D1, shift) != candleTime)
      return FreezeD1TPWLifecycle(info, "D1_CANDLE_NOT_EXACT_CLOSED_BAR");

   int tfSeconds = GetTimeframeSeconds(PERIOD_D1);
   if(tfSeconds <= 0 || !IsCandleClosed(candleTime, tfSeconds))
      return FreezeD1TPWLifecycle(info, "D1_CANDLE_NOT_CLOSED");

   double high = iHigh(pair, PERIOD_D1, shift);
   double low = iLow(pair, PERIOD_D1, shift);
   if(high <= 0.0 || low <= 0.0 || high < low)
      return FreezeD1TPWLifecycle(info, "D1_PRICE_HISTORY_INVALID");

   // Validate MA history explicitly; IsD1TPWCompletionAtShift(false) alone
   // cannot distinguish 'not reached' from unavailable MA history.
   if(info.direction == DIR_SELL)
   {
      if(BBMALowMA(pair, PERIOD_D1, MA5_LOW_PERIOD, shift) <= 0.0 ||
         BBMALowMA(pair, PERIOD_D1, MA10_LOW_PERIOD, shift) <= 0.0)
         return FreezeD1TPWLifecycle(info, "D1_TPW_MA_HISTORY_INVALID");
   }
   else if(info.direction == DIR_BUY)
   {
      if(BBMAHighMA(pair, PERIOD_D1, MA5_HIGH_PERIOD, shift) <= 0.0 ||
         BBMAHighMA(pair, PERIOD_D1, MA10_HIGH_PERIOD, shift) <= 0.0)
         return FreezeD1TPWLifecycle(info, "D1_TPW_MA_HISTORY_INVALID");
   }
   else
      return FreezeD1TPWLifecycle(info, "DIRECTION_INVALID");

   info.d1_tpw_last_processed_d1_candle = candleTime;
   if(IsD1TPWCompletionAtShift(pair, info.direction, shift))
      return LatchD1TPWExit(info, candleTime);

   if(!SaveD1TPWCheckpoint(info))
      return FreezeD1TPWLifecycle(info, "D1_CURSOR_CHECKPOINT_FAILED");
   return true;
}

bool AdvanceD1TPWLifecycleForTrade(TradeInfo &info, int pairIndex)
{
   if(!EnableD1TPWLifecycle || !info.d1_tpw_lifecycle_managed) return true;
   if(info.d1_tpw_frozen || info.d1_tpw_exit_latched) return true;
   if(info.d1_tpw_last_processed_d1_candle <= 0)
      return FreezeD1TPWLifecycle(info, "D1_CURSOR_INVALID");

   datetime latestClosed = GetLatestClosedCandleTime(info.pair, PERIOD_D1);
   if(latestClosed <= 0)
      return FreezeD1TPWLifecycle(info, "LATEST_D1_UNAVAILABLE");
   if(latestClosed <= info.d1_tpw_last_processed_d1_candle) return true;

   int latestShift = iBarShift(info.pair, PERIOD_D1, latestClosed, true);
   int previousShift = iBarShift(info.pair, PERIOD_D1,
                                 info.d1_tpw_last_processed_d1_candle, true);
   if(latestShift < 1 || previousShift < 1 || previousShift <= latestShift)
      return FreezeD1TPWLifecycle(info, "D1_CURSOR_NOT_IN_HISTORY");

   for(int shift = previousShift - 1; shift >= latestShift; shift--)
   {
      datetime candleTime = iTime(info.pair, PERIOD_D1, shift);
      if(candleTime <= 0)
         return FreezeD1TPWLifecycle(info, "MISSED_D1_CANDLE_UNAVAILABLE");
      if(!ProcessD1TPWClosedCandle(info, pairIndex, candleTime)) return false;
      if(info.d1_tpw_exit_latched || info.d1_tpw_frozen) break;
   }
   return true;
}

void AdvanceD1TPWLifecycleForPair(int pairIndex)
{
   if(!EnableD1TPWLifecycle || pairIndex < 0 || pairIndex >= g_pair_count) return;
   string pair = g_pair_states[pairIndex].actual_symbol;
   for(int i = 0; i < g_monitored_count; i++)
   {
      if(!g_monitored_trades[i].d1_tpw_lifecycle_managed ||
         g_monitored_trades[i].pair != pair)
         continue;
      if(g_monitored_trades[i].recovery_state != REC_NORMAL &&
         g_monitored_trades[i].recovery_state != REC_PARTIAL_INFERRED)
         continue;
      AdvanceD1TPWLifecycleForTrade(g_monitored_trades[i], pairIndex);
   }
}

bool ExecuteLatchedD1TPWClose(TradeInfo &info)
{
   if(!EnableD1TPWLifecycle || !info.d1_tpw_lifecycle_managed ||
      info.d1_tpw_frozen || !info.d1_tpw_exit_latched ||
      info.d1_tpw_exit_latched_candle <= 0)
      return false;
   if(info.ticket <= 0 || info.pair == "" || info.magic_number <= 0) return false;
   if(!OrderSelect(info.ticket, SELECT_BY_TICKET) || OrderCloseTime() != 0) return false;
   if(OrderSymbol() != info.pair || OrderMagicNumber() != info.magic_number) return false;

   double closePrice = (info.direction == DIR_BUY)
      ? MarketInfo(info.pair, MODE_BID)
      : (info.direction == DIR_SELL ? MarketInfo(info.pair, MODE_ASK) : 0.0);
   if(closePrice <= 0.0) return false;

   ResetLastError();
   if(OrderClose(info.ticket, OrderLots(), closePrice, Slippage))
   {
      ClearD1TPWCheckpoint(info);
      return true;
   }

   int error = GetLastError();
   Log(DBG_ERROR, "D1TPW close failed ticket=" + IntegerToString(info.ticket) +
       " error=" + IntegerToString(error));
   return false;
}

'''
one('void ManagePositions()\n{', d1_m23 + 'void ManagePositions()\n{', 'M23 D1TPW insertion')

# M20 emergency stays first; D1TPW close gets precedence over C044 and is exclusive.
one('      // C044 close execution is dormant while the internal feature gate is OFF.\n'
    '      // M20 emergency handling above retains precedence.\n'
    '      if(EnableC044Lifecycle && g_monitored_trades[i].c044_lifecycle_managed &&',
    '      // M20 emergency handling above retains precedence. D1 TPW and C044\n'
    '      // are mutually exclusive normal strategy lifecycle owners.\n'
    '      if(EnableD1TPWLifecycle && g_monitored_trades[i].d1_tpw_lifecycle_managed &&\n'
    '         g_monitored_trades[i].d1_tpw_exit_latched &&\n'
    '         !g_monitored_trades[i].d1_tpw_frozen)\n'
    '      {\n'
    '         ExecuteLatchedD1TPWClose(g_monitored_trades[i]);\n'
    '         continue;\n'
    '      }\n\n'
    '      // C044 close execution is dormant while its internal feature gate is OFF.\n'
    '      if(EnableC044Lifecycle && g_monitored_trades[i].c044_lifecycle_managed &&',
    'M23 close precedence')

# M24 dedicated checkpoint/recovery implementation.
d1_m24 = r'''void ResetD1TPWTradeState(TradeInfo &info)
{
   info.d1_tpw_lifecycle_managed = false;
   info.d1_tpw_extreme_candle = 0;
   info.d1_tpw_last_processed_d1_candle = 0;
   info.d1_tpw_exit_latched = false;
   info.d1_tpw_exit_latched_candle = 0;
   info.d1_tpw_frozen = false;
}

string D1TPWCheckpointBase(TradeInfo &info)
{
   return "D1TPW|S" + IntegerToString(StrategyID) + "|I" +
          IntegerToString(InstanceID) + "|T" + IntegerToString(info.ticket) + "|";
}

bool D1TPWCheckpointExists(TradeInfo &info)
{
   if(info.ticket <= 0) return false;
   string base = D1TPWCheckpointBase(info);
   string keys[8] = {"D","X","LP","L","XL","F","OT","MG"};
   for(int i = 0; i < 8; i++)
      if(!GlobalVariableCheck(base + keys[i])) return false;
   return true;
}

void ClearD1TPWCheckpoint(TradeInfo &info)
{
   if(info.ticket <= 0) return;
   string base = D1TPWCheckpointBase(info);
   string keys[8] = {"D","X","LP","L","XL","F","OT","MG"};
   for(int i = 0; i < 8; i++)
      if(GlobalVariableCheck(base + keys[i])) GlobalVariableDel(base + keys[i]);
   GlobalVariablesFlush();
}

bool SaveD1TPWCheckpoint(TradeInfo &info)
{
   if(!info.d1_tpw_lifecycle_managed || info.ticket <= 0 ||
      info.magic_number <= 0 || info.open_time <= 0 ||
      (info.direction != DIR_BUY && info.direction != DIR_SELL) ||
      info.d1_tpw_extreme_candle <= 0 ||
      info.d1_tpw_last_processed_d1_candle < info.d1_tpw_extreme_candle)
      return false;

   string base = D1TPWCheckpointBase(info);
   GlobalVariableSet(base + "D", (double)info.direction);
   GlobalVariableSet(base + "X", (double)info.d1_tpw_extreme_candle);
   GlobalVariableSet(base + "LP", (double)info.d1_tpw_last_processed_d1_candle);
   GlobalVariableSet(base + "L", info.d1_tpw_exit_latched ? 1.0 : 0.0);
   GlobalVariableSet(base + "XL", (double)info.d1_tpw_exit_latched_candle);
   GlobalVariableSet(base + "F", info.d1_tpw_frozen ? 1.0 : 0.0);
   GlobalVariableSet(base + "OT", (double)info.open_time);
   GlobalVariableSet(base + "MG", (double)info.magic_number);
   GlobalVariablesFlush();
   return D1TPWCheckpointExists(info);
}

bool LoadD1TPWCheckpoint(TradeInfo &info)
{
   if(info.ticket <= 0 || info.magic_number <= 0 || info.open_time <= 0) return false;
   if(!D1TPWCheckpointExists(info)) return false;

   string base = D1TPWCheckpointBase(info);
   ENUM_DIRECTION direction = (ENUM_DIRECTION)((int)GlobalVariableGet(base + "D"));
   datetime extremeCandle = (datetime)((int)GlobalVariableGet(base + "X"));
   datetime lastProcessed = (datetime)((int)GlobalVariableGet(base + "LP"));
   bool latched = (GlobalVariableGet(base + "L") > 0.5);
   datetime exitCandle = (datetime)((int)GlobalVariableGet(base + "XL"));
   bool frozen = (GlobalVariableGet(base + "F") > 0.5);
   datetime openTime = (datetime)((int)GlobalVariableGet(base + "OT"));
   int magic = (int)GlobalVariableGet(base + "MG");

   if(direction != info.direction || magic != info.magic_number ||
      openTime != info.open_time || extremeCandle <= 0 ||
      lastProcessed < extremeCandle || (latched && exitCandle <= 0) ||
      (!latched && exitCandle != 0))
      return false;

   int extremeShift = iBarShift(info.pair, PERIOD_D1, extremeCandle, true);
   int cursorShift = iBarShift(info.pair, PERIOD_D1, lastProcessed, true);
   if(extremeShift < 1 || cursorShift < 1 ||
      iTime(info.pair, PERIOD_D1, extremeShift) != extremeCandle ||
      iTime(info.pair, PERIOD_D1, cursorShift) != lastProcessed)
      return false;

   ResetD1TPWTradeState(info);
   info.d1_tpw_lifecycle_managed = true;
   info.d1_tpw_extreme_candle = extremeCandle;
   info.d1_tpw_last_processed_d1_candle = lastProcessed;
   info.d1_tpw_exit_latched = latched;
   info.d1_tpw_exit_latched_candle = exitCandle;
   info.d1_tpw_frozen = frozen;
   return true;
}

bool InitializeD1TPWTradeStateFromDecision(TradeInfo &info, BBMA_Decision &decision)
{
   ResetD1TPWTradeState(info);
   if(!decision.D1TPWLifecycleManaged) return true;
   if(!EnableD1TPWLifecycle || !IsD1TPWLifecycleIdentity(decision) ||
      decision.D1OpportunitySourceCandleTime <= 0 ||
      decision.D1OpportunityDirection != decision.Direction)
      return false;

   int pairIndex = FindPairStateIndex(decision.Pair);
   if(pairIndex < 0 || pairIndex >= g_pair_count) return false;
   string pair = g_pair_states[pairIndex].actual_symbol;
   if(pair == "" || pair != decision.Pair) return false;

   int extremeShift = iBarShift(pair, PERIOD_D1,
                                decision.D1OpportunitySourceCandleTime, true);
   if(extremeShift < 1 ||
      iTime(pair, PERIOD_D1, extremeShift) != decision.D1OpportunitySourceCandleTime)
      return false;

   datetime latestClosed = GetLatestClosedCandleTime(pair, PERIOD_D1);
   if(latestClosed <= 0 || latestClosed < decision.D1OpportunitySourceCandleTime)
      return false;

   info.d1_tpw_lifecycle_managed = true;
   info.d1_tpw_extreme_candle = decision.D1OpportunitySourceCandleTime;
   // Position-management events start when the broker position exists; any
   // earlier D1 candles were already part of opportunity eligibility/provenance.
   info.d1_tpw_last_processed_d1_candle = latestClosed;
   info.d1_tpw_exit_latched = false;
   info.d1_tpw_exit_latched_candle = 0;
   info.d1_tpw_frozen = false;
   return true;
}

'''
one('void ResetC044TradeState(TradeInfo &info)\n{',
    d1_m24 + 'void ResetC044TradeState(TradeInfo &info)\n{',
    'M24 D1TPW insertion')

# Allow recovery code to distinguish targetless lifecycle checkpoint families.
one('string C044ReplayGVBase(TradeInfo &info)\n{',
    'bool C044CheckpointExists(TradeInfo &info)\n'
    '{\n'
    '   if(info.ticket <= 0) return false;\n'
    '   string base = C044CheckpointBase(info);\n'
    '   string keys[10] = {"D","TF","OR","EP","LP","ST","XR","XL","OT","MG"};\n'
    '   for(int i = 0; i < 10; i++)\n'
    '      if(!GlobalVariableCheck(base + keys[i])) return false;\n'
    '   return true;\n'
    '}\n\n'
    'string C044ReplayGVBase(TradeInfo &info)\n{',
    'C044 checkpoint exists helper')

# Recovery: targetless order must have exactly one valid checkpoint family.
def transform_recovery(b: str) -> str:
    start = b.find('      ResetC044TradeState(info);\n')
    end = b.find('      info.partial_closed = false;\n', start)
    if start < 0 or end < 0:
        raise SystemExit('recovery state block anchors missing')
    old = b[start:end]
    new = r'''      ResetC044TradeState(info);
      ResetD1TPWTradeState(info);
      bool targetless = (info.initial_take_profit == 0.0);
      bool c044Checkpoint = targetless && C044CheckpointExists(info);
      bool d1TPWCheckpoint = targetless && D1TPWCheckpointExists(info);
      bool checkpointAmbiguous = (c044Checkpoint && d1TPWCheckpoint);
      bool targetlessRecovered = false;
      if(targetless && !checkpointAmbiguous)
      {
         if(d1TPWCheckpoint)
            targetlessRecovered = LoadD1TPWCheckpoint(info);
         else if(c044Checkpoint)
            targetlessRecovered = LoadC044Checkpoint(info);
      }

      bool geometryValid = (info.initial_entry_price > 0 &&
                            info.initial_stop_loss > 0);
      if(geometryValid && liveDirection == DIR_BUY)
         geometryValid = (info.initial_stop_loss < info.initial_entry_price &&
                          (targetless ? targetlessRecovered
                                      : info.initial_entry_price < info.initial_take_profit));
      else if(geometryValid && liveDirection == DIR_SELL)
         geometryValid = (info.initial_stop_loss > info.initial_entry_price &&
                          (targetless ? targetlessRecovered
                                      : info.initial_take_profit < info.initial_entry_price));

      string recoveryCause = "";
      double currentLot = OrderLots();
      if(targetless && checkpointAmbiguous)
      {
         info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
         recoveryCause = "TARGETLESS_CHECKPOINT_AMBIGUOUS";
      }
      else if(targetless && targetlessRecovered && info.d1_tpw_lifecycle_managed &&
              info.d1_tpw_frozen)
      {
         info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
         recoveryCause = "D1TPW_CHECKPOINT_FROZEN";
      }
      else if(targetless && targetlessRecovered && info.c044_lifecycle_managed &&
              info.c044_state == C044_LIFE_FROZEN)
      {
         info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
         recoveryCause = "C044_CHECKPOINT_FROZEN";
      }
      else if(targetless && !targetlessRecovered)
      {
         info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
         recoveryCause = "TARGETLESS_CHECKPOINT_MISSING_OR_INVALID";
      }
      else if(targetless && !fullMetadata)
      {
         info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
         recoveryCause = "TARGETLESS_FULL_METADATA_REQUIRED";
      }
      else if(!geometryValid)
      {
         info.recovery_state = REC_RECOVERY_INVALID;
         recoveryCause = "INVALID_GEOMETRY";
      }
      else if(currentLot <= 0)
      {
         info.recovery_state = REC_RECOVERY_INVALID;
         recoveryCause = "NONPOSITIVE_LIVE_LOT";
      }
      else if(!IsValidLotStep(currentLot, pair))
      {
         info.recovery_state = REC_RECOVERY_INVALID;
         recoveryCause = "INVALID_LIVE_LOT_STEP";
      }
      else if(fullMetadata && intendedLot > 0 && currentLot > intendedLot + 0.0000001)
      {
         info.recovery_state = REC_CORRUPTED;
         recoveryCause = "LIVE_LOT_ABOVE_INTENDED";
      }
      else if(fullMetadata && intendedLot > 0 && currentLot < intendedLot - 0.0000001)
      {
         info.recovery_state = REC_PARTIAL_INFERRED;
         info.remaining_lot = currentLot;
         recoveryCause = "LIVE_LOT_BELOW_INTENDED";
      }
      else if(fullMetadata)
      {
         info.recovery_state = REC_NORMAL;
         recoveryCause = "FULL_METADATA_MATCH";
      }
      else if(hasExecutionHash)
      {
         info.recovery_state = REC_IDENTITY_HASH_ONLY;
         recoveryCause = "EXECUTION_HASH_ONLY";
      }
      else
      {
         info.recovery_state = REC_IDENTITY_MISSING_FROZEN;
         recoveryCause = "MISSING_EXECUTION_HASH";
      }

'''
    return b[:start] + new + b[end:]

block('void RecoverExistingOrders()\n',
      '//+------------------------------------------------------------------+\n//| MODULE 25:',
      transform_recovery, 'Recovery targetless split')

# Advance TPW lifecycle on the same closed-M15 processing cycle as C044 evidence.
one('   AdvanceC044OwnerEventsForPair(pairIndex);\n\n   // D1O-02: all D1/H4/H1/M15 owners are now current.',
    '   AdvanceC044OwnerEventsForPair(pairIndex);\n'
    '   AdvanceD1TPWLifecycleForPair(pairIndex);\n\n'
    '   // D1O-02: all D1/H4/H1/M15 owners are now current.',
    'M15 TPW lifecycle clock')

# Static staging guard: source feature remains OFF until runtime activation review.
if 'bool           EnableD1TPWLifecycle               = false;' not in s:
    raise SystemExit('D1 TPW gate not OFF after patch')
if 'decision.D1TPWLifecycleManaged = d1TPWLifecycle;' not in s:
    raise SystemExit('M17 D1 TPW payload missing')
if 'AdvanceD1TPWLifecycleForPair(pairIndex);' not in s:
    raise SystemExit('M15 TPW lifecycle call missing')
if 'D1TPWCheckpointExists' not in s or 'ExecuteLatchedD1TPWClose' not in s:
    raise SystemExit('D1 TPW recovery/close machinery missing')
if 'Version 4.5.8 - D1 TP-Wajib Lifecycle Stage' not in s:
    raise SystemExit('build marker missing')

SRC.write_text(s, encoding='utf-8', newline='\n')
print('D1 TP-Wajib lifecycle v4.58 patch applied')
