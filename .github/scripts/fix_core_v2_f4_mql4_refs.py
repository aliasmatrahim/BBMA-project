from pathlib import Path

p = Path('blueprint/source/BBMA_EA.mq4')
s = p.read_text(encoding='utf-8')


def replace_between(start, end, replacement, label):
    global s
    a = s.find(start)
    if a < 0:
        raise SystemExit(f'{label}: start not found')
    b = s.find(end, a)
    if b < 0:
        raise SystemExit(f'{label}: end not found')
    s = s[:a] + replacement + s[b + len(end):]

replace_between(
'''void SaveH4OwnerCheckpoint(PairState &state)
{
''',
'''ENUM_SIGNAL_TYPE ClassifyH4AuthoritativeSignal''',
'''void SaveH4OwnerCheckpoint(PairState &state)
{
   if(state.h4_direction_owner.State != H4_OWNER_ACTIVE ||
      !state.h4_direction_owner.IsValid ||
      (state.h4_direction_owner.Direction != DIR_BUY &&
       state.h4_direction_owner.Direction != DIR_SELL) ||
      state.h4_direction_owner.SourceCandleTime <= 0 ||
      (state.h4_direction_owner.SourceSignal != SIGNAL_ECSD &&
       state.h4_direction_owner.SourceSignal != SIGNAL_CSD &&
       state.h4_direction_owner.SourceSignal != SIGNAL_CSM))
   {
      ClearH4OwnerCheckpoint(state);
      return;
   }

   string base = H4OwnerGVBase(state);
   GlobalVariableSet(base + "D", (double)state.h4_direction_owner.Direction);
   GlobalVariableSet(base + "S", (double)state.h4_direction_owner.SourceSignal);
   GlobalVariableSet(base + "T", (double)state.h4_direction_owner.SourceCandleTime);
   GlobalVariablesFlush();
}

ENUM_SIGNAL_TYPE ClassifyH4AuthoritativeSignal''',
'SaveH4OwnerCheckpoint local reference removal')

replace_between(
'''void ApplyH4AuthoritativeEvent(PairState &state,
''',
'''bool VerifyH4OwnerCheckpoint''',
'''void ApplyH4AuthoritativeEvent(PairState &state,
                               ENUM_DIRECTION direction,
                               ENUM_SIGNAL_TYPE signalType,
                               datetime candleTime,
                               bool recovered)
{
   if(direction != DIR_BUY && direction != DIR_SELL) return;
   if(signalType != SIGNAL_ECSD && signalType != SIGNAL_CSD &&
      signalType != SIGNAL_CSM) return;
   if(candleTime <= 0) return;

   bool handover = (state.h4_direction_owner.State == H4_OWNER_ACTIVE &&
                    state.h4_direction_owner.IsValid &&
                    state.h4_direction_owner.Direction != DIR_NONE &&
                    state.h4_direction_owner.Direction != direction);

   state.h4_direction_owner.State = H4_OWNER_ACTIVE;
   state.h4_direction_owner.Direction = direction;
   state.h4_direction_owner.SourceSignal = signalType;
   state.h4_direction_owner.SourceCandleTime = candleTime;
   state.h4_direction_owner.LastAdvanceSignal = signalType;
   state.h4_direction_owner.LastAdvanceCandleTime = candleTime;
   state.h4_direction_owner.IsValid = true;
   state.h4_direction_owner.RecoveryComplete = true;
   state.h4_direction_owner.RecoveredFromCheckpoint = recovered;
   state.h4_direction_owner.Reason = handover
      ? "Atomic H4 owner handover by opposite source-valid direction/momentum"
      : "H4 authoritative directional owner established/advanced";
}

bool VerifyH4OwnerCheckpoint''',
'ApplyH4AuthoritativeEvent local reference removal')

replace_between(
'''void RecoverH4DirectionalOwnerForPair(int pairIndex)
{
''',
'''void RecoverH4DirectionalOwners()''',
'''void RecoverH4DirectionalOwnerForPair(int pairIndex)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;

   ResetH4DirectionalOwner(g_pair_states[pairIndex].h4_direction_owner,
                           H4_OWNER_RECOVERY_UNRESOLVED);

   if(!g_pair_states[pairIndex].pair_enabled ||
      g_pair_states[pairIndex].actual_symbol == "")
   {
      ResetH4DirectionalOwner(g_pair_states[pairIndex].h4_direction_owner,
                              H4_OWNER_NONE);
      g_pair_states[pairIndex].h4_direction_owner.Reason =
         "H4 recovery unavailable for disabled/unresolved pair";
      return;
   }

   bool checkpointValid = LoadVerifiedH4OwnerCheckpoint(g_pair_states[pairIndex]);
   int bars = iBars(g_pair_states[pairIndex].actual_symbol, PERIOD_H4);
   if(bars < 3)
   {
      if(!checkpointValid)
      {
         ResetH4DirectionalOwner(g_pair_states[pairIndex].h4_direction_owner,
                                 H4_OWNER_NONE);
         g_pair_states[pairIndex].h4_direction_owner.Reason =
            "Insufficient closed H4 history -> NO_OWNER";
      }
      g_pair_states[pairIndex].h4_direction_owner.RecoveryComplete = true;
      return;
   }

   int startShift = bars - 2;
   if(checkpointValid)
   {
      int checkpointShift = iBarShift(
         g_pair_states[pairIndex].actual_symbol, PERIOD_H4,
         g_pair_states[pairIndex].h4_direction_owner.SourceCandleTime, true);
      if(checkpointShift >= 1)
         startShift = checkpointShift - 1;
      else
      {
         ResetH4DirectionalOwner(g_pair_states[pairIndex].h4_direction_owner,
                                 H4_OWNER_NONE);
         checkpointValid = false;
         startShift = bars - 2;
      }
   }

   for(int shift = startShift; shift >= 1; shift--)
   {
      datetime candleTime =
         iTime(g_pair_states[pairIndex].actual_symbol, PERIOD_H4, shift);
      if(candleTime <= 0) continue;

      TimeframeData data;
      InitTimeframeData(data);
      GetDataForTimeframe(g_pair_states[pairIndex].actual_symbol,
                          PERIOD_H4, candleTime, data);
      if(!data.is_valid || !data.is_closed) continue;

      ApplyH4ReplayCandle(g_pair_states[pairIndex], data);
   }

   g_pair_states[pairIndex].h4_direction_owner.RecoveryComplete = true;
   if(g_pair_states[pairIndex].h4_direction_owner.State != H4_OWNER_ACTIVE ||
      !g_pair_states[pairIndex].h4_direction_owner.IsValid)
   {
      g_pair_states[pairIndex].h4_direction_owner.State = H4_OWNER_NONE;
      g_pair_states[pairIndex].h4_direction_owner.Direction = DIR_NONE;
      g_pair_states[pairIndex].h4_direction_owner.IsValid = false;
      g_pair_states[pairIndex].h4_direction_owner.Reason =
         "Closed-H4 replay could not prove authoritative owner -> NO_OWNER";
      ClearH4OwnerCheckpoint(g_pair_states[pairIndex]);
      return;
   }

   SaveH4OwnerCheckpoint(g_pair_states[pairIndex]);
}

void RecoverH4DirectionalOwners()''',
'RecoverH4DirectionalOwnerForPair local reference removal')

replace_between(
'''void UpdateRuntimeH4DirectionalOwner(int pairIndex)
{
''',
'''void NoteH4ReEntryInheritance''',
'''void UpdateRuntimeH4DirectionalOwner(int pairIndex)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;

   if(!g_pair_states[pairIndex].h4_direction_owner.RecoveryComplete) return;
   if(!g_pair_states[pairIndex].h4_data.is_valid ||
      !g_pair_states[pairIndex].h4_data.is_closed ||
      g_pair_states[pairIndex].h4_data.timeframe != PERIOD_H4 ||
      g_pair_states[pairIndex].h4_data.candle_time <= 0)
      return;
   if(g_pair_states[pairIndex].h4_data.candle_time ==
      g_pair_states[pairIndex].h4_direction_owner.LastProcessedH4CandleTime)
      return;

   ENUM_SIGNAL_TYPE buySignal = ClassifyH4AuthoritativeSignal(
      g_pair_states[pairIndex].actual_symbol, DIR_BUY,
      g_pair_states[pairIndex].h4_data);
   ENUM_SIGNAL_TYPE sellSignal = ClassifyH4AuthoritativeSignal(
      g_pair_states[pairIndex].actual_symbol, DIR_SELL,
      g_pair_states[pairIndex].h4_data);

   if(buySignal != SIGNAL_NONE && sellSignal != SIGNAL_NONE)
   {
      ResetH4DirectionalOwner(g_pair_states[pairIndex].h4_direction_owner,
                              H4_OWNER_NONE);
      g_pair_states[pairIndex].h4_direction_owner.LastProcessedH4CandleTime =
         g_pair_states[pairIndex].h4_data.candle_time;
      g_pair_states[pairIndex].h4_direction_owner.Reason =
         "Ambiguous simultaneous H4 BUY/SELL authoritative events -> NO_OWNER";
      ClearH4OwnerCheckpoint(g_pair_states[pairIndex]);
      return;
   }

   if(buySignal != SIGNAL_NONE)
      ApplyH4AuthoritativeEvent(g_pair_states[pairIndex], DIR_BUY, buySignal,
                                g_pair_states[pairIndex].h4_data.candle_time, false);
   else if(sellSignal != SIGNAL_NONE)
      ApplyH4AuthoritativeEvent(g_pair_states[pairIndex], DIR_SELL, sellSignal,
                                g_pair_states[pairIndex].h4_data.candle_time, false);

   g_pair_states[pairIndex].h4_direction_owner.LastProcessedH4CandleTime =
      g_pair_states[pairIndex].h4_data.candle_time;
   if(g_pair_states[pairIndex].h4_direction_owner.State == H4_OWNER_ACTIVE &&
      g_pair_states[pairIndex].h4_direction_owner.IsValid)
      SaveH4OwnerCheckpoint(g_pair_states[pairIndex]);
}

void NoteH4ReEntryInheritance''',
'UpdateRuntimeH4DirectionalOwner local reference removal')

replace_between(
'''void NoteH4ReEntryInheritance(int pairIndex, ReEntryData &reEntry)
{
''',
'''void RecoverExistingOrders()''',
'''void NoteH4ReEntryInheritance(int pairIndex, ReEntryData &reEntry)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;

   if(!g_pair_states[pairIndex].h4_direction_owner.RecoveryComplete ||
      !g_pair_states[pairIndex].h4_direction_owner.IsValid ||
      g_pair_states[pairIndex].h4_direction_owner.State != H4_OWNER_ACTIVE ||
      reEntry.State != RE_STATE_CONFIRMED || !reEntry.IsValid ||
      reEntry.Timeframe != PERIOD_H4 ||
      reEntry.Direction != g_pair_states[pairIndex].h4_direction_owner.Direction ||
      reEntry.ConfirmationCandle <= 0)
      return;

   g_pair_states[pairIndex].h4_direction_owner.LastAdvanceSignal = SIGNAL_RE_ENTRY;
   g_pair_states[pairIndex].h4_direction_owner.LastAdvanceCandleTime =
      reEntry.ConfirmationCandle;
   g_pair_states[pairIndex].h4_direction_owner.Reason =
      "Same-direction H4 Re-Entry inherited existing directional owner";
}

void RecoverExistingOrders()''',
'NoteH4ReEntryInheritance local reference removal')

bad = [
    'H4DirectionalOwner &owner =',
    'PairState &state = g_pair_states',
    'TimeframeData &data = state.h4_data',
]
for token in bad:
    if token in s:
        raise SystemExit(f'unsupported local MQL reference variable remains: {token}')

p.write_text(s, encoding='utf-8')

audit = Path('blueprint/CORE_V2_F4_IMPLEMENTATION_AUDIT.md')
a = audit.read_text(encoding='utf-8')
marker = '- source lexical brace/parenthesis/bracket sanity passes.\n'
addition = marker + '- post-static MQL4 compatibility repair removes unsupported local reference-variable aliases; references remain only in function parameters, as supported by MQL4.\n'
if marker not in a:
    raise SystemExit('F4 audit marker missing')
a = a.replace(marker, addition, 1)
audit.write_text(a, encoding='utf-8')
