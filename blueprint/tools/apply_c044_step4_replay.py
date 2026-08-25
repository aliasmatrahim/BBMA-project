from pathlib import Path

p = Path('blueprint/source/BBMA_EA.mq4')
s = p.read_text(encoding='utf-8')

if 'Version 4.5.5 - C044 Owner Event Evaluator Stage' not in s:
    raise SystemExit('unexpected baseline build')
if '#property version   "4.55"' not in s:
    raise SystemExit('unexpected baseline property version')
if 'bool           EnableC044Lifecycle                = false;' not in s:
    raise SystemExit('C044 gate not locked OFF on baseline')

baseline_order_close_count = s.count('OrderClose(')

def replace_once(old, new, label):
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, found {n}')
    s = s.replace(old, new, 1)

def find_function_span(text, name):
    marker = name + '('
    idx = text.find(marker)
    if idx < 0:
        raise SystemExit(f'function not found: {name}')
    start = text.rfind('\n', 0, idx) + 1
    brace = text.find('{', idx)
    if brace < 0:
        raise SystemExit(f'opening brace not found: {name}')
    depth = 0
    pos = brace
    in_string = False
    escaped = False
    while pos < len(text):
        ch = text[pos]
        if in_string:
            if escaped:
                escaped = False
            elif ch == '\\':
                escaped = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    end = pos + 1
                    while end < len(text) and text[end] in '\r\n':
                        end += 1
                    return start, end
        pos += 1
    raise SystemExit(f'closing brace not found: {name}')

def replace_function(name, new_text):
    global s
    start, end = find_function_span(s, name)
    s = s[:start] + new_text.rstrip() + '\n\n' + s[end:]

def remove_function(name):
    global s
    start, end = find_function_span(s, name)
    s = s[:start] + s[end:]

replace_once('Version 4.5.5 - C044 Owner Event Evaluator Stage',
             'Version 4.5.6 - C044 Deterministic Replay Stage',
             'header version')
replace_once('#property version   "4.55"', '#property version   "4.56"',
             'property version')

trade_anchor = '''   ENUM_C044_LIFECYCLE_STATE c044_state;\n   ENUM_C044_EXIT_REASON c044_exit_reason;\n   datetime             c044_exit_latched_candle;\n\n   ENUM_RECOVERY_STATE  recovery_state;\n'''
trade_block = '''   ENUM_C044_LIFECYCLE_STATE c044_state;\n   ENUM_C044_EXIT_REASON c044_exit_reason;\n   datetime             c044_exit_latched_candle;\n\n   // C044 Step4 deterministic replay seed. These are canonical owner snapshots\n   // captured at the runtime cursor and persisted with the lifecycle checkpoint.\n   bool                 c044_replay_seed_valid;\n   ReEntryData          c044_replay_reentry;\n   ExtremeLifecycleData c044_replay_extreme_buy;\n   ExtremeLifecycleData c044_replay_extreme_sell;\n\n   ENUM_RECOVERY_STATE  recovery_state;\n'''
replace_once(trade_anchor, trade_block, 'TradeInfo replay fields')

reset_func = r'''void ResetC044TradeState(TradeInfo &info)
{
   info.c044_lifecycle_managed = false;
   info.c044_owner_timeframe = 0;
   info.c044_owner_reentry_candle = 0;
   info.c044_epoch_anchor_candle = 0;
   info.c044_last_processed_owner_candle = 0;
   info.c044_state = C044_LIFE_NONE;
   info.c044_exit_reason = C044_EXIT_NONE;
   info.c044_exit_latched_candle = 0;
   info.c044_replay_seed_valid = false;
   ZeroMemory(info.c044_replay_reentry);
   ZeroMemory(info.c044_replay_extreme_buy);
   ZeroMemory(info.c044_replay_extreme_sell);
}'''
replace_function('ResetC044TradeState', reset_func)

capture_func = r'''bool CaptureC044ReplaySeed(TradeInfo &info, int pairIndex)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return false;
   if(info.direction != DIR_BUY && info.direction != DIR_SELL) return false;
   if(!IsValidC044OwnerTimeframe(info.c044_owner_timeframe)) return false;

   if(!GetC044OwnerReEntrySnapshot(pairIndex, info.c044_owner_timeframe,
                                   info.direction, info.c044_replay_reentry))
      return false;
   if(!GetC044OwnerExtremeSnapshot(pairIndex, info.c044_owner_timeframe,
                                   DIR_BUY, info.c044_replay_extreme_buy))
      return false;
   if(!GetC044OwnerExtremeSnapshot(pairIndex, info.c044_owner_timeframe,
                                   DIR_SELL, info.c044_replay_extreme_sell))
      return false;

   if(info.c044_replay_reentry.Direction != info.direction ||
      info.c044_replay_reentry.Timeframe != info.c044_owner_timeframe ||
      info.c044_replay_extreme_buy.Direction != DIR_BUY ||
      info.c044_replay_extreme_buy.Timeframe != info.c044_owner_timeframe ||
      info.c044_replay_extreme_sell.Direction != DIR_SELL ||
      info.c044_replay_extreme_sell.Timeframe != info.c044_owner_timeframe)
      return false;

   info.c044_replay_seed_valid = true;
   return true;
}'''

isvalid_end = s.find('bool InitializeC044TradeStateFromDecision(')
if isvalid_end < 0:
    raise SystemExit('initialize anchor missing')
s = s[:isvalid_end] + capture_func + '\n\n' + s[isvalid_end:]

init_func = r'''bool InitializeC044TradeStateFromDecision(TradeInfo &info, BBMA_Decision &decision)
{
   ResetC044TradeState(info);
   if(!decision.C044LifecycleManaged) return true;
   if(!decision.HasSLTPSourceComponent ||
      decision.SLTPSourceComponent.ComponentType != SIGNAL_RE_ENTRY ||
      decision.SLTPSourceComponent.Direction != decision.Direction ||
      !IsValidC044OwnerTimeframe(decision.SLTPSourceComponent.Timeframe) ||
      decision.SLTPSourceComponent.CandleTime <= 0)
      return false;

   int pairIndex = FindPairStateIndex(decision.Pair);
   if(pairIndex < 0)
   {
      for(int i = 0; i < g_pair_count; i++)
      {
         if(g_pair_states[i].actual_symbol == decision.Pair)
         {
            pairIndex = i;
            break;
         }
      }
   }
   if(pairIndex < 0) return false;

   string ownerPair = g_pair_states[pairIndex].actual_symbol;
   if(ownerPair == "") return false;
   datetime latestClosed = GetLatestClosedCandleTime(
      ownerPair, decision.SLTPSourceComponent.Timeframe);
   if(latestClosed <= 0 || latestClosed < decision.SLTPSourceComponent.CandleTime)
      return false;

   info.c044_lifecycle_managed = true;
   info.c044_owner_timeframe = decision.SLTPSourceComponent.Timeframe;
   info.c044_owner_reentry_candle = decision.SLTPSourceComponent.CandleTime;
   info.c044_epoch_anchor_candle = decision.SLTPSourceComponent.CandleTime;

   // Runtime ownership starts when the broker position exists. Closed owner
   // candles between the source Re-Entry and actual order creation are provenance,
   // not lifecycle events for a position that did not yet exist.
   info.c044_last_processed_owner_candle = latestClosed;
   info.c044_state = C044_LIFE_WAIT_OUTER_TEST;
   info.c044_exit_reason = C044_EXIT_NONE;
   info.c044_exit_latched_candle = 0;

   if(!CaptureC044ReplaySeed(info, pairIndex))
   {
      ResetC044TradeState(info);
      return false;
   }
   return true;
}'''
replace_function('InitializeC044TradeStateFromDecision', init_func)

checkpoint_marker = 'string C044CheckpointBase(TradeInfo &info)\n'
idx = s.find(checkpoint_marker)
if idx < 0:
    raise SystemExit('checkpoint base anchor missing')
# C044CheckpointBase itself stays unchanged; replay helpers are inserted after it.
start, end = find_function_span(s, 'C044CheckpointBase')
replay_helpers = r'''string C044ReplayGVBase(TradeInfo &info)
{
   return C044CheckpointBase(info) + "R|";
}

string C044ReplayGVKey(string base, string group, int index)
{
   return base + group + IntegerToString(index);
}

void ClearC044ReplaySeed(TradeInfo &info)
{
   if(info.ticket <= 0) return;
   string base = C044ReplayGVBase(info);
   if(GlobalVariableCheck(base + "V")) GlobalVariableDel(base + "V");
   for(int i = 0; i < 20; i++)
      if(GlobalVariableCheck(C044ReplayGVKey(base, "R", i)))
         GlobalVariableDel(C044ReplayGVKey(base, "R", i));
   for(int j = 0; j < 19; j++)
   {
      if(GlobalVariableCheck(C044ReplayGVKey(base, "B", j)))
         GlobalVariableDel(C044ReplayGVKey(base, "B", j));
      if(GlobalVariableCheck(C044ReplayGVKey(base, "S", j)))
         GlobalVariableDel(C044ReplayGVKey(base, "S", j));
   }
}

bool SaveC044ReplaySeed(TradeInfo &info)
{
   if(!info.c044_replay_seed_valid || info.ticket <= 0) return false;
   if(info.c044_replay_reentry.Direction != info.direction ||
      info.c044_replay_reentry.Timeframe != info.c044_owner_timeframe ||
      info.c044_replay_extreme_buy.Direction != DIR_BUY ||
      info.c044_replay_extreme_buy.Timeframe != info.c044_owner_timeframe ||
      info.c044_replay_extreme_sell.Direction != DIR_SELL ||
      info.c044_replay_extreme_sell.Timeframe != info.c044_owner_timeframe)
      return false;

   string base = C044ReplayGVBase(info);
   GlobalVariableSet(base + "V", 1.0);

   GlobalVariableSet(C044ReplayGVKey(base,"R",0),  (double)info.c044_replay_reentry.Type);
   GlobalVariableSet(C044ReplayGVKey(base,"R",1),  (double)info.c044_replay_reentry.State);
   GlobalVariableSet(C044ReplayGVKey(base,"R",2),  (double)info.c044_replay_reentry.Direction);
   GlobalVariableSet(C044ReplayGVKey(base,"R",3),  (double)info.c044_replay_reentry.Timeframe);
   GlobalVariableSet(C044ReplayGVKey(base,"R",4),  (double)info.c044_replay_reentry.StartBar);
   GlobalVariableSet(C044ReplayGVKey(base,"R",5),  (double)info.c044_replay_reentry.StartCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"R",6),  (double)info.c044_replay_reentry.LastUpdateBar);
   GlobalVariableSet(C044ReplayGVKey(base,"R",7),  (double)info.c044_replay_reentry.LastUpdateCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"R",8),  (double)info.c044_replay_reentry.ConfirmationBar);
   GlobalVariableSet(C044ReplayGVKey(base,"R",9),  (double)info.c044_replay_reentry.ConfirmationCandle);
   GlobalVariableSet(C044ReplayGVKey(base,"R",10), (double)info.c044_replay_reentry.ExpiryBar);
   GlobalVariableSet(C044ReplayGVKey(base,"R",11), (double)info.c044_replay_reentry.ExpiryCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"R",12), (double)info.c044_replay_reentry.MinCandlesRequired);
   GlobalVariableSet(C044ReplayGVKey(base,"R",13), (double)info.c044_replay_reentry.QualifyingCandles);
   GlobalVariableSet(C044ReplayGVKey(base,"R",14), (double)info.c044_replay_reentry.Type1ContextState);
   GlobalVariableSet(C044ReplayGVKey(base,"R",15), (double)info.c044_replay_reentry.Type1OwnerSignal);
   GlobalVariableSet(C044ReplayGVKey(base,"R",16), (double)info.c044_replay_reentry.Type1OwnerCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"R",17), (double)info.c044_replay_reentry.Type1RangingStartCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"R",18), info.c044_replay_reentry.Type1PreviousClose);
   GlobalVariableSet(C044ReplayGVKey(base,"R",19), info.c044_replay_reentry.IsValid ? 1.0 : 0.0);

   ExtremeLifecycleData buy = info.c044_replay_extreme_buy;
   ExtremeLifecycleData sell = info.c044_replay_extreme_sell;
   GlobalVariableSet(C044ReplayGVKey(base,"B",0),  (double)buy.Maturity);
   GlobalVariableSet(C044ReplayGVKey(base,"B",1),  (double)buy.Direction);
   GlobalVariableSet(C044ReplayGVKey(base,"B",2),  (double)buy.Timeframe);
   GlobalVariableSet(C044ReplayGVKey(base,"B",3),  (double)buy.RawBar);
   GlobalVariableSet(C044ReplayGVKey(base,"B",4),  (double)buy.RawCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"B",5),  (double)buy.ConfirmationBar);
   GlobalVariableSet(C044ReplayGVKey(base,"B",6),  (double)buy.ConfirmationCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"B",7),  buy.ConfirmationClose);
   GlobalVariableSet(C044ReplayGVKey(base,"B",8),  (double)buy.LastUpdateBar);
   GlobalVariableSet(C044ReplayGVKey(base,"B",9),  (double)buy.LastUpdateCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"B",10), buy.PreviousClose);
   GlobalVariableSet(C044ReplayGVKey(base,"B",11), buy.ProvisionalBodyAnchor);
   GlobalVariableSet(C044ReplayGVKey(base,"B",12), buy.FrozenBodyAnchor);
   GlobalVariableSet(C044ReplayGVKey(base,"B",13), buy.RelevantMA5);
   GlobalVariableSet(C044ReplayGVKey(base,"B",14), (double)buy.RetestStartBar);
   GlobalVariableSet(C044ReplayGVKey(base,"B",15), (double)buy.RetestStartCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"B",16), (double)buy.RetestCompletionBar);
   GlobalVariableSet(C044ReplayGVKey(base,"B",17), (double)buy.RetestCompletionCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"B",18), buy.IsValid ? 1.0 : 0.0);

   GlobalVariableSet(C044ReplayGVKey(base,"S",0),  (double)sell.Maturity);
   GlobalVariableSet(C044ReplayGVKey(base,"S",1),  (double)sell.Direction);
   GlobalVariableSet(C044ReplayGVKey(base,"S",2),  (double)sell.Timeframe);
   GlobalVariableSet(C044ReplayGVKey(base,"S",3),  (double)sell.RawBar);
   GlobalVariableSet(C044ReplayGVKey(base,"S",4),  (double)sell.RawCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"S",5),  (double)sell.ConfirmationBar);
   GlobalVariableSet(C044ReplayGVKey(base,"S",6),  (double)sell.ConfirmationCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"S",7),  sell.ConfirmationClose);
   GlobalVariableSet(C044ReplayGVKey(base,"S",8),  (double)sell.LastUpdateBar);
   GlobalVariableSet(C044ReplayGVKey(base,"S",9),  (double)sell.LastUpdateCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"S",10), sell.PreviousClose);
   GlobalVariableSet(C044ReplayGVKey(base,"S",11), sell.ProvisionalBodyAnchor);
   GlobalVariableSet(C044ReplayGVKey(base,"S",12), sell.FrozenBodyAnchor);
   GlobalVariableSet(C044ReplayGVKey(base,"S",13), sell.RelevantMA5);
   GlobalVariableSet(C044ReplayGVKey(base,"S",14), (double)sell.RetestStartBar);
   GlobalVariableSet(C044ReplayGVKey(base,"S",15), (double)sell.RetestStartCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"S",16), (double)sell.RetestCompletionBar);
   GlobalVariableSet(C044ReplayGVKey(base,"S",17), (double)sell.RetestCompletionCandleTime);
   GlobalVariableSet(C044ReplayGVKey(base,"S",18), sell.IsValid ? 1.0 : 0.0);
   return true;
}

bool ReadC044ReplayGV(string base, string group, int index, double &value)
{
   string key = C044ReplayGVKey(base, group, index);
   if(!GlobalVariableCheck(key)) return false;
   value = GlobalVariableGet(key);
   return true;
}

bool LoadC044ReplaySeed(TradeInfo &info)
{
   string base = C044ReplayGVBase(info);
   if(!GlobalVariableCheck(base + "V") ||
      (int)GlobalVariableGet(base + "V") != 1)
      return false;

   ZeroMemory(info.c044_replay_reentry);
   ZeroMemory(info.c044_replay_extreme_buy);
   ZeroMemory(info.c044_replay_extreme_sell);
   double v = 0.0;

   if(!ReadC044ReplayGV(base,"R",0,v)) return false; info.c044_replay_reentry.Type=(ENUM_RE_TYPE)((int)v);
   if(!ReadC044ReplayGV(base,"R",1,v)) return false; info.c044_replay_reentry.State=(ENUM_RE_STATE)((int)v);
   if(!ReadC044ReplayGV(base,"R",2,v)) return false; info.c044_replay_reentry.Direction=(ENUM_DIRECTION)((int)v);
   if(!ReadC044ReplayGV(base,"R",3,v)) return false; info.c044_replay_reentry.Timeframe=(int)v;
   if(!ReadC044ReplayGV(base,"R",4,v)) return false; info.c044_replay_reentry.StartBar=(int)v;
   if(!ReadC044ReplayGV(base,"R",5,v)) return false; info.c044_replay_reentry.StartCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"R",6,v)) return false; info.c044_replay_reentry.LastUpdateBar=(int)v;
   if(!ReadC044ReplayGV(base,"R",7,v)) return false; info.c044_replay_reentry.LastUpdateCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"R",8,v)) return false; info.c044_replay_reentry.ConfirmationBar=(int)v;
   if(!ReadC044ReplayGV(base,"R",9,v)) return false; info.c044_replay_reentry.ConfirmationCandle=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"R",10,v)) return false; info.c044_replay_reentry.ExpiryBar=(int)v;
   if(!ReadC044ReplayGV(base,"R",11,v)) return false; info.c044_replay_reentry.ExpiryCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"R",12,v)) return false; info.c044_replay_reentry.MinCandlesRequired=(int)v;
   if(!ReadC044ReplayGV(base,"R",13,v)) return false; info.c044_replay_reentry.QualifyingCandles=(int)v;
   if(!ReadC044ReplayGV(base,"R",14,v)) return false; info.c044_replay_reentry.Type1ContextState=(ENUM_TYPE1_CONTEXT_STATE)((int)v);
   if(!ReadC044ReplayGV(base,"R",15,v)) return false; info.c044_replay_reentry.Type1OwnerSignal=(ENUM_SIGNAL_TYPE)((int)v);
   if(!ReadC044ReplayGV(base,"R",16,v)) return false; info.c044_replay_reentry.Type1OwnerCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"R",17,v)) return false; info.c044_replay_reentry.Type1RangingStartCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"R",18,v)) return false; info.c044_replay_reentry.Type1PreviousClose=v;
   if(!ReadC044ReplayGV(base,"R",19,v)) return false; info.c044_replay_reentry.IsValid=(v > 0.5);

   if(!ReadC044ReplayGV(base,"B",0,v)) return false; info.c044_replay_extreme_buy.Maturity=(ENUM_EXTREME_MATURITY)((int)v);
   if(!ReadC044ReplayGV(base,"B",1,v)) return false; info.c044_replay_extreme_buy.Direction=(ENUM_DIRECTION)((int)v);
   if(!ReadC044ReplayGV(base,"B",2,v)) return false; info.c044_replay_extreme_buy.Timeframe=(int)v;
   if(!ReadC044ReplayGV(base,"B",3,v)) return false; info.c044_replay_extreme_buy.RawBar=(int)v;
   if(!ReadC044ReplayGV(base,"B",4,v)) return false; info.c044_replay_extreme_buy.RawCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"B",5,v)) return false; info.c044_replay_extreme_buy.ConfirmationBar=(int)v;
   if(!ReadC044ReplayGV(base,"B",6,v)) return false; info.c044_replay_extreme_buy.ConfirmationCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"B",7,v)) return false; info.c044_replay_extreme_buy.ConfirmationClose=v;
   if(!ReadC044ReplayGV(base,"B",8,v)) return false; info.c044_replay_extreme_buy.LastUpdateBar=(int)v;
   if(!ReadC044ReplayGV(base,"B",9,v)) return false; info.c044_replay_extreme_buy.LastUpdateCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"B",10,v)) return false; info.c044_replay_extreme_buy.PreviousClose=v;
   if(!ReadC044ReplayGV(base,"B",11,v)) return false; info.c044_replay_extreme_buy.ProvisionalBodyAnchor=v;
   if(!ReadC044ReplayGV(base,"B",12,v)) return false; info.c044_replay_extreme_buy.FrozenBodyAnchor=v;
   if(!ReadC044ReplayGV(base,"B",13,v)) return false; info.c044_replay_extreme_buy.RelevantMA5=v;
   if(!ReadC044ReplayGV(base,"B",14,v)) return false; info.c044_replay_extreme_buy.RetestStartBar=(int)v;
   if(!ReadC044ReplayGV(base,"B",15,v)) return false; info.c044_replay_extreme_buy.RetestStartCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"B",16,v)) return false; info.c044_replay_extreme_buy.RetestCompletionBar=(int)v;
   if(!ReadC044ReplayGV(base,"B",17,v)) return false; info.c044_replay_extreme_buy.RetestCompletionCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"B",18,v)) return false; info.c044_replay_extreme_buy.IsValid=(v > 0.5);

   if(!ReadC044ReplayGV(base,"S",0,v)) return false; info.c044_replay_extreme_sell.Maturity=(ENUM_EXTREME_MATURITY)((int)v);
   if(!ReadC044ReplayGV(base,"S",1,v)) return false; info.c044_replay_extreme_sell.Direction=(ENUM_DIRECTION)((int)v);
   if(!ReadC044ReplayGV(base,"S",2,v)) return false; info.c044_replay_extreme_sell.Timeframe=(int)v;
   if(!ReadC044ReplayGV(base,"S",3,v)) return false; info.c044_replay_extreme_sell.RawBar=(int)v;
   if(!ReadC044ReplayGV(base,"S",4,v)) return false; info.c044_replay_extreme_sell.RawCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"S",5,v)) return false; info.c044_replay_extreme_sell.ConfirmationBar=(int)v;
   if(!ReadC044ReplayGV(base,"S",6,v)) return false; info.c044_replay_extreme_sell.ConfirmationCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"S",7,v)) return false; info.c044_replay_extreme_sell.ConfirmationClose=v;
   if(!ReadC044ReplayGV(base,"S",8,v)) return false; info.c044_replay_extreme_sell.LastUpdateBar=(int)v;
   if(!ReadC044ReplayGV(base,"S",9,v)) return false; info.c044_replay_extreme_sell.LastUpdateCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"S",10,v)) return false; info.c044_replay_extreme_sell.PreviousClose=v;
   if(!ReadC044ReplayGV(base,"S",11,v)) return false; info.c044_replay_extreme_sell.ProvisionalBodyAnchor=v;
   if(!ReadC044ReplayGV(base,"S",12,v)) return false; info.c044_replay_extreme_sell.FrozenBodyAnchor=v;
   if(!ReadC044ReplayGV(base,"S",13,v)) return false; info.c044_replay_extreme_sell.RelevantMA5=v;
   if(!ReadC044ReplayGV(base,"S",14,v)) return false; info.c044_replay_extreme_sell.RetestStartBar=(int)v;
   if(!ReadC044ReplayGV(base,"S",15,v)) return false; info.c044_replay_extreme_sell.RetestStartCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"S",16,v)) return false; info.c044_replay_extreme_sell.RetestCompletionBar=(int)v;
   if(!ReadC044ReplayGV(base,"S",17,v)) return false; info.c044_replay_extreme_sell.RetestCompletionCandleTime=(datetime)((int)v);
   if(!ReadC044ReplayGV(base,"S",18,v)) return false; info.c044_replay_extreme_sell.IsValid=(v > 0.5);

   if(info.c044_replay_reentry.Direction != info.direction ||
      info.c044_replay_reentry.Timeframe != info.c044_owner_timeframe ||
      info.c044_replay_extreme_buy.Direction != DIR_BUY ||
      info.c044_replay_extreme_buy.Timeframe != info.c044_owner_timeframe ||
      info.c044_replay_extreme_sell.Direction != DIR_SELL ||
      info.c044_replay_extreme_sell.Timeframe != info.c044_owner_timeframe)
      return false;

   info.c044_replay_seed_valid = true;
   return true;
}'''
s = s[:end] + replay_helpers + '\n\n' + s[end:]

clear_func = r'''void ClearC044Checkpoint(TradeInfo &info)
{
   if(info.ticket <= 0) return;
   string base = C044CheckpointBase(info);
   string keys[10] = {"D","TF","OR","EP","LP","ST","XR","XL","OT","MG"};
   for(int i = 0; i < 10; i++)
      if(GlobalVariableCheck(base + keys[i])) GlobalVariableDel(base + keys[i]);
   ClearC044ReplaySeed(info);
}'''
replace_function('ClearC044Checkpoint', clear_func)

save_func = r'''bool SaveC044Checkpoint(TradeInfo &info)
{
   if(!info.c044_lifecycle_managed || info.ticket <= 0 ||
      info.magic_number <= 0 || info.open_time <= 0 ||
      (info.direction != DIR_BUY && info.direction != DIR_SELL) ||
      !IsValidC044OwnerTimeframe(info.c044_owner_timeframe) ||
      info.c044_owner_reentry_candle <= 0 || info.c044_epoch_anchor_candle <= 0 ||
      info.c044_last_processed_owner_candle <= 0 ||
      info.c044_state == C044_LIFE_NONE)
      return false;

   if(info.c044_state != C044_LIFE_FROZEN &&
      (!info.c044_replay_seed_valid || !SaveC044ReplaySeed(info)))
      return false;

   string base = C044CheckpointBase(info);
   GlobalVariableSet(base + "D",  (double)info.direction);
   GlobalVariableSet(base + "TF", (double)info.c044_owner_timeframe);
   GlobalVariableSet(base + "OR", (double)info.c044_owner_reentry_candle);
   GlobalVariableSet(base + "EP", (double)info.c044_epoch_anchor_candle);
   GlobalVariableSet(base + "LP", (double)info.c044_last_processed_owner_candle);
   GlobalVariableSet(base + "ST", (double)info.c044_state);
   GlobalVariableSet(base + "XR", (double)info.c044_exit_reason);
   GlobalVariableSet(base + "XL", (double)info.c044_exit_latched_candle);
   GlobalVariableSet(base + "OT", (double)info.open_time);
   GlobalVariableSet(base + "MG", (double)info.magic_number);
   GlobalVariablesFlush();

   string keys[10] = {"D","TF","OR","EP","LP","ST","XR","XL","OT","MG"};
   for(int i = 0; i < 10; i++)
      if(!GlobalVariableCheck(base + keys[i])) return false;
   return true;
}'''
replace_function('SaveC044Checkpoint', save_func)

load_func = r'''bool LoadC044Checkpoint(TradeInfo &info)
{
   if(info.ticket <= 0 || info.magic_number <= 0 || info.open_time <= 0) return false;
   string base = C044CheckpointBase(info);
   string keys[10] = {"D","TF","OR","EP","LP","ST","XR","XL","OT","MG"};
   for(int i = 0; i < 10; i++)
      if(!GlobalVariableCheck(base + keys[i])) return false;

   ENUM_DIRECTION direction = (ENUM_DIRECTION)((int)GlobalVariableGet(base + "D"));
   int timeframe = (int)GlobalVariableGet(base + "TF");
   datetime ownerRe = (datetime)((int)GlobalVariableGet(base + "OR"));
   datetime epoch = (datetime)((int)GlobalVariableGet(base + "EP"));
   datetime lastProcessed = (datetime)((int)GlobalVariableGet(base + "LP"));
   ENUM_C044_LIFECYCLE_STATE state =
      (ENUM_C044_LIFECYCLE_STATE)((int)GlobalVariableGet(base + "ST"));
   ENUM_C044_EXIT_REASON exitReason =
      (ENUM_C044_EXIT_REASON)((int)GlobalVariableGet(base + "XR"));
   datetime exitCandle = (datetime)((int)GlobalVariableGet(base + "XL"));
   datetime openTime = (datetime)((int)GlobalVariableGet(base + "OT"));
   int magic = (int)GlobalVariableGet(base + "MG");

   if(direction != info.direction || magic != info.magic_number || openTime != info.open_time)
      return false;
   if(!IsValidC044OwnerTimeframe(timeframe) || ownerRe <= 0 || epoch <= 0 ||
      lastProcessed <= 0)
      return false;
   if(state != C044_LIFE_WAIT_OUTER_TEST &&
      state != C044_LIFE_WAIT_NEXT_REENTRY &&
      state != C044_LIFE_EXIT_LATCHED && state != C044_LIFE_FROZEN)
      return false;
   if(state == C044_LIFE_EXIT_LATCHED &&
      (exitReason == C044_EXIT_NONE || exitCandle <= 0 ||
       exitCandle > lastProcessed))
      return false;
   if(state != C044_LIFE_EXIT_LATCHED &&
      (exitReason != C044_EXIT_NONE || exitCandle != 0))
      return false;

   info.c044_lifecycle_managed = true;
   info.c044_owner_timeframe = timeframe;
   info.c044_owner_reentry_candle = ownerRe;
   info.c044_epoch_anchor_candle = epoch;
   info.c044_last_processed_owner_candle = lastProcessed;
   info.c044_state = state;
   info.c044_exit_reason = exitReason;
   info.c044_exit_latched_candle = exitCandle;

   if(state == C044_LIFE_FROZEN)
   {
      info.c044_replay_seed_valid = false;
      return true;
   }
   return LoadC044ReplaySeed(info);
}'''
replace_function('LoadC044Checkpoint', load_func)

# Step4 no longer reads current global owner snapshots to infer missed events.
remove_function('IsC044SameDirectionReEntryEvent')
remove_function('IsC044OppositeExtremeSupersessionEvent')

process_func = r'''bool ProcessC044OwnerClosedCandle(TradeInfo &info, int pairIndex,
                                  datetime candleTime)
{
   if(!EnableC044Lifecycle || !info.c044_lifecycle_managed) return true;
   if(pairIndex < 0 || pairIndex >= g_pair_count || candleTime <= 0)
      return FreezeC044Lifecycle(info, "INVALID_OWNER_EVENT_IDENTITY");
   if(info.c044_state == C044_LIFE_EXIT_LATCHED ||
      info.c044_state == C044_LIFE_FROZEN)
      return true;
   if(!info.c044_replay_seed_valid)
      return FreezeC044Lifecycle(info, "REPLAY_SEED_MISSING");

   string pair = g_pair_states[pairIndex].actual_symbol;
   if(pair == "" || info.pair != pair ||
      !IsValidC044OwnerTimeframe(info.c044_owner_timeframe))
      return FreezeC044Lifecycle(info, "OWNER_EVENT_PAIR_OR_TF_MISMATCH");

   int shift = iBarShift(pair, info.c044_owner_timeframe, candleTime, true);
   if(shift < 1)
      return FreezeC044Lifecycle(info, "OWNER_EVENT_CANDLE_NOT_EXACT_CLOSED_BAR");

   TimeframeData data;
   InitTimeframeData(data);
   GetDataForTimeframe(pair, info.c044_owner_timeframe, candleTime, data);
   if(!data.is_valid || !data.is_closed || data.candle_time != candleTime ||
      data.barIndex != shift)
      return FreezeC044Lifecycle(info, "OWNER_EVENT_CLOSED_DATA_UNAVAILABLE");

   MovingAverage ma;
   BollingerBand band;
   BuildReEntryDirectionInputs(data, ma, band);

   // Deterministic replay uses the same canonical M08 and M12 state machines on
   // private C044 snapshots. No Extreme/Re-Entry formula is reimplemented here.
   bool rawBuy = DetectExtreme(pair, DIR_BUY, data, band);
   bool rawSell = DetectExtreme(pair, DIR_SELL, data, band);
   UpdateExtremeLifecycle(info.c044_replay_extreme_buy, pair, DIR_BUY,
                          data, band, rawBuy);
   UpdateExtremeLifecycle(info.c044_replay_extreme_sell, pair, DIR_SELL,
                          data, band, rawSell);
   ResolveOppositeExtremeSupersession(info.c044_replay_extreme_buy,
                                      info.c044_replay_extreme_sell, data);
   UpdateReEntryState(info.c044_replay_reentry, pair, info.direction, data);

   bool sameReEntryEvent =
      (info.c044_replay_reentry.State == RE_STATE_CONFIRMED &&
       info.c044_replay_reentry.IsValid &&
       info.c044_replay_reentry.Direction == info.direction &&
       info.c044_replay_reentry.Timeframe == info.c044_owner_timeframe &&
       info.c044_replay_reentry.ConfirmationCandle == candleTime &&
       candleTime > info.c044_epoch_anchor_candle);

   bool oppositeExtremeEvent = false;
   if(info.direction == DIR_BUY)
   {
      bool mature =
         (info.c044_replay_extreme_sell.Maturity == EXT_MAT_REVERSAL_CONFIRMED ||
          info.c044_replay_extreme_sell.Maturity == EXT_MAT_RETEST_PHASE ||
          info.c044_replay_extreme_sell.Maturity == EXT_MAT_RETEST_READY);
      oppositeExtremeEvent =
         (info.c044_replay_extreme_sell.IsValid && mature &&
          info.c044_replay_extreme_sell.ConfirmationCandleTime == candleTime &&
          candleTime > info.c044_epoch_anchor_candle);
   }
   else if(info.direction == DIR_SELL)
   {
      bool mature =
         (info.c044_replay_extreme_buy.Maturity == EXT_MAT_REVERSAL_CONFIRMED ||
          info.c044_replay_extreme_buy.Maturity == EXT_MAT_RETEST_PHASE ||
          info.c044_replay_extreme_buy.Maturity == EXT_MAT_RETEST_READY);
      oppositeExtremeEvent =
         (info.c044_replay_extreme_buy.IsValid && mature &&
          info.c044_replay_extreme_buy.ConfirmationCandleTime == candleTime &&
          candleTime > info.c044_epoch_anchor_candle);
   }

   info.c044_last_processed_owner_candle = candleTime;

   if(oppositeExtremeEvent)
   {
      if(!LatchC044Exit(info, C044_EXIT_CYCLE_SUPERSEDED, candleTime))
         return FreezeC044Lifecycle(info, "CYCLE_SUPERSESSION_LATCH_FAILED");
      return true;
   }

   if(info.c044_state == C044_LIFE_WAIT_NEXT_REENTRY)
   {
      if(sameReEntryEvent)
      {
         info.c044_owner_reentry_candle = candleTime;
         info.c044_epoch_anchor_candle = candleTime;
         info.c044_state = C044_LIFE_WAIT_OUTER_TEST;
         info.c044_exit_reason = C044_EXIT_NONE;
         info.c044_exit_latched_candle = 0;
      }
      if(!SaveC044Checkpoint(info))
         return FreezeC044Lifecycle(info, "WAIT_NEXT_REENTRY_CHECKPOINT_FAILED");
      return true;
   }

   if(info.c044_state != C044_LIFE_WAIT_OUTER_TEST)
      return FreezeC044Lifecycle(info, "UNEXPECTED_OWNER_EVENT_STATE");

   if(candleTime <= info.c044_epoch_anchor_candle)
   {
      if(!SaveC044Checkpoint(info))
         return FreezeC044Lifecycle(info, "EPOCH_BOUNDARY_CHECKPOINT_FAILED");
      return true;
   }

   if(!IsC044DirectionSideOuterBBTest(data, info.direction))
   {
      if(!SaveC044Checkpoint(info))
         return FreezeC044Lifecycle(info, "WAIT_OUTER_TEST_CHECKPOINT_FAILED");
      return true;
   }

   bool momentum = DetectCSM(pair, info.c044_owner_timeframe,
                             info.direction, shift);
   if(momentum)
   {
      info.c044_state = C044_LIFE_WAIT_NEXT_REENTRY;
      info.c044_exit_reason = C044_EXIT_NONE;
      info.c044_exit_latched_candle = 0;
      if(!SaveC044Checkpoint(info))
         return FreezeC044Lifecycle(info, "MOMENTUM_HOLD_CHECKPOINT_FAILED");
      return true;
   }

   if(!LatchC044Exit(info, C044_EXIT_FAILED_MOMENTUM, candleTime))
      return FreezeC044Lifecycle(info, "FAILED_MOMENTUM_LATCH_FAILED");
   return true;
}'''
replace_function('ProcessC044OwnerClosedCandle', process_func)

advance_func = r'''bool AdvanceC044OwnerEventOneCandle(TradeInfo &info, int pairIndex)
{
   if(!EnableC044Lifecycle || !info.c044_lifecycle_managed) return true;
   if(info.c044_state == C044_LIFE_EXIT_LATCHED ||
      info.c044_state == C044_LIFE_FROZEN)
      return true;
   if(info.c044_last_processed_owner_candle <= 0 ||
      !IsValidC044OwnerTimeframe(info.c044_owner_timeframe))
      return FreezeC044Lifecycle(info, "OWNER_EVENT_CURSOR_INVALID");
   if(!info.c044_replay_seed_valid)
      return FreezeC044Lifecycle(info, "REPLAY_SEED_MISSING");

   datetime latestClosed = GetLatestClosedCandleTime(
      info.pair, info.c044_owner_timeframe);
   if(latestClosed <= 0)
      return FreezeC044Lifecycle(info, "LATEST_OWNER_CANDLE_UNAVAILABLE");
   if(latestClosed <= info.c044_last_processed_owner_candle)
      return true;

   int latestShift = iBarShift(info.pair, info.c044_owner_timeframe,
                               latestClosed, true);
   int previousShift = iBarShift(info.pair, info.c044_owner_timeframe,
                                 info.c044_last_processed_owner_candle, true);
   if(latestShift < 1 || previousShift < 1 || previousShift <= latestShift)
      return FreezeC044Lifecycle(info, "OWNER_EVENT_CURSOR_NOT_IN_HISTORY");

   // Replay every missed closed owner candle from oldest to newest. Historical
   // data must be exact; any missing candle freezes the lifecycle rather than
   // guessing whether a Re-Entry, Extreme or failed Momentum occurred.
   for(int shift = previousShift - 1; shift >= latestShift; shift--)
   {
      datetime candleTime = iTime(info.pair, info.c044_owner_timeframe, shift);
      if(candleTime <= info.c044_last_processed_owner_candle)
         return FreezeC044Lifecycle(info, "REPLAY_CANDLE_ORDER_INVALID");
      if(!ProcessC044OwnerClosedCandle(info, pairIndex, candleTime))
         return false;
      if(info.c044_state == C044_LIFE_EXIT_LATCHED ||
         info.c044_state == C044_LIFE_FROZEN)
         return true;
   }

   if(info.c044_last_processed_owner_candle != latestClosed)
      return FreezeC044Lifecycle(info, "REPLAY_CURSOR_DID_NOT_REACH_LATEST");
   return true;
}'''
replace_function('AdvanceC044OwnerEventOneCandle', advance_func)

if s.count('OrderClose(') != baseline_order_close_count:
    raise SystemExit('OrderClose authority count changed')
if 'MULTI_CANDLE_OWNER_EVENT_GAP' in s:
    raise SystemExit('legacy multi-candle freeze path still present')
for marker in [
    'Version 4.5.6 - C044 Deterministic Replay Stage',
    '#property version   "4.56"',
    'CaptureC044ReplaySeed',
    'SaveC044ReplaySeed',
    'LoadC044ReplaySeed',
    'ResolveOppositeExtremeSupersession(info.c044_replay_extreme_buy',
    'for(int shift = previousShift - 1; shift >= latestShift; shift--)',
    'info.c044_last_processed_owner_candle = latestClosed;',
    'bool           EnableC044Lifecycle                = false;'
]:
    if marker not in s:
        raise SystemExit(f'missing Step4 marker: {marker}')

p.write_text(s, encoding='utf-8')
print('C044 Step4 deterministic replay patch applied')
