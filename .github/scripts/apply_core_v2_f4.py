from pathlib import Path
import re

SOURCE = Path('blueprint/source/BBMA_EA.mq4')
AUDIT = Path('blueprint/CORE_V2_F4_IMPLEMENTATION_AUDIT.md')
QUEUE = Path('blueprint/MASTER_QUEUE.md')
CURRENT = Path('blueprint/CURRENT.md')

s = SOURCE.read_text(encoding='utf-8')


def replace_once(old: str, new: str, label: str):
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 occurrence, found {count}')
    s = s.replace(old, new, 1)


# ---------------------------------------------------------------------------
# M02/M03 — explicit H4 directional owner state.
# ---------------------------------------------------------------------------
anchor_enum = '''enum ENUM_TYPE1_CONTEXT_STATE
{
   TYPE1_CTX_NONE,
   TYPE1_CTX_DIRECTION_OWNER,
   TYPE1_CTX_RANGING
};
'''
owner_enum = anchor_enum + '''
enum ENUM_H4_OWNER_STATE
{
   H4_OWNER_RECOVERY_UNRESOLVED,
   H4_OWNER_NONE,
   H4_OWNER_ACTIVE
};
'''
replace_once(anchor_enum, owner_enum, 'H4 owner enum')

reentry_end = '''   bool                 IsValid;
   double               StrengthScore;
   string               Reason;
};

struct SignalMemory
'''
owner_struct = '''   bool                 IsValid;
   double               StrengthScore;
   string               Reason;
};

struct H4DirectionalOwner
{
   ENUM_H4_OWNER_STATE  State;
   ENUM_DIRECTION       Direction;
   ENUM_SIGNAL_TYPE     SourceSignal;
   datetime             SourceCandleTime;
   ENUM_SIGNAL_TYPE     LastAdvanceSignal;
   datetime             LastAdvanceCandleTime;
   datetime             LastProcessedH4CandleTime;
   bool                 IsValid;
   bool                 RecoveryComplete;
   bool                 RecoveredFromCheckpoint;
   string               Reason;
};

struct SignalMemory
'''
replace_once(reentry_end, owner_struct, 'H4 owner struct')

pair_anchor = '''   ReEntryData          re_d1_buy_state;
   ReEntryData          re_d1_sell_state;
   double               prev_ema50;
'''
pair_new = '''   ReEntryData          re_d1_buy_state;
   ReEntryData          re_d1_sell_state;
   H4DirectionalOwner   h4_direction_owner;
   double               prev_ema50;
'''
replace_once(pair_anchor, pair_new, 'PairState H4 owner field')

init_anchor = '''   state.re_d1_sell_state.State = RE_STATE_NONE;
   state.re_d1_sell_state.Direction = DIR_SELL;
   state.re_d1_sell_state.Timeframe = PERIOD_D1;
}
'''
init_new = '''   state.re_d1_sell_state.State = RE_STATE_NONE;
   state.re_d1_sell_state.Direction = DIR_SELL;
   state.re_d1_sell_state.Timeframe = PERIOD_D1;

   state.h4_direction_owner.State = H4_OWNER_RECOVERY_UNRESOLVED;
   state.h4_direction_owner.Direction = DIR_NONE;
   state.h4_direction_owner.SourceSignal = SIGNAL_NONE;
   state.h4_direction_owner.LastAdvanceSignal = SIGNAL_NONE;
   state.h4_direction_owner.IsValid = false;
   state.h4_direction_owner.RecoveryComplete = false;
   state.h4_direction_owner.RecoveredFromCheckpoint = false;
}
'''
replace_once(init_anchor, init_new, 'InitPairState H4 owner initialization')

# ---------------------------------------------------------------------------
# M15 — standalone H1 Re-Entry candidate requires compatible recovered H4 owner.
# ---------------------------------------------------------------------------
old_sig = '''void BuildConfirmedReEntryCandidate(ReEntryData &reEntry,
                                    ValidatedSequenceCandidate &candidate)
{
'''
new_sig = '''void BuildConfirmedReEntryCandidate(ReEntryData &reEntry,
                                    H4DirectionalOwner &h4Owner,
                                    ValidatedSequenceCandidate &candidate)
{
'''
replace_once(old_sig, new_sig, 'BuildConfirmedReEntryCandidate signature')

old_gate = '''   if(reEntry.Direction != DIR_BUY && reEntry.Direction != DIR_SELL) return;
   if(reEntry.Timeframe != PERIOD_H1) return;
   if(reEntry.ConfirmationCandle <= 0) return;
'''
new_gate = '''   if(reEntry.Direction != DIR_BUY && reEntry.Direction != DIR_SELL) return;
   if(reEntry.Timeframe != PERIOD_H1) return;

   // CORE-V2-F4: standalone H1 Re-Entry is executable only under the
   // immediate H4 authoritative directional owner. No D1/EMA/current-candle
   // fallback is permitted when H4 is NO_OWNER or recovery is unresolved.
   if(!h4Owner.RecoveryComplete || !h4Owner.IsValid ||
      h4Owner.State != H4_OWNER_ACTIVE ||
      h4Owner.Direction != reEntry.Direction)
      return;

   if(reEntry.ConfirmationCandle <= 0) return;
'''
replace_once(old_gate, new_gate, 'standalone H1 H4 owner gate')

# ---------------------------------------------------------------------------
# M24 — checkpoint, provenance verification, deterministic closed-H4 replay,
# runtime owner/handover, and fail-safe NO_OWNER.
# ---------------------------------------------------------------------------
recover_marker = '''void RecoverExistingOrders()
{
'''
owner_functions = r'''string H4OwnerGVBase(PairState &state)
{
   return "F4H4|" + IntegerToString(StrategyID) + "|" +
          IntegerToString(InstanceID) + "|" + state.base_symbol + "|";
}

void ResetH4DirectionalOwner(H4DirectionalOwner &owner,
                             ENUM_H4_OWNER_STATE state)
{
   ZeroMemory(owner);
   owner.State = state;
   owner.Direction = DIR_NONE;
   owner.SourceSignal = SIGNAL_NONE;
   owner.LastAdvanceSignal = SIGNAL_NONE;
   owner.IsValid = false;
   owner.RecoveryComplete = (state != H4_OWNER_RECOVERY_UNRESOLVED);
   owner.RecoveredFromCheckpoint = false;
}

void ClearH4OwnerCheckpoint(PairState &state)
{
   string base = H4OwnerGVBase(state);
   if(GlobalVariableCheck(base + "D")) GlobalVariableDel(base + "D");
   if(GlobalVariableCheck(base + "S")) GlobalVariableDel(base + "S");
   if(GlobalVariableCheck(base + "T")) GlobalVariableDel(base + "T");
}

void SaveH4OwnerCheckpoint(PairState &state)
{
   H4DirectionalOwner &owner = state.h4_direction_owner;
   if(owner.State != H4_OWNER_ACTIVE || !owner.IsValid ||
      (owner.Direction != DIR_BUY && owner.Direction != DIR_SELL) ||
      owner.SourceCandleTime <= 0 ||
      (owner.SourceSignal != SIGNAL_ECSD &&
       owner.SourceSignal != SIGNAL_CSD &&
       owner.SourceSignal != SIGNAL_CSM))
   {
      ClearH4OwnerCheckpoint(state);
      return;
   }

   string base = H4OwnerGVBase(state);
   GlobalVariableSet(base + "D", (double)owner.Direction);
   GlobalVariableSet(base + "S", (double)owner.SourceSignal);
   GlobalVariableSet(base + "T", (double)owner.SourceCandleTime);
   GlobalVariablesFlush();
}

ENUM_SIGNAL_TYPE ClassifyH4AuthoritativeSignal(string pair,
                                                ENUM_DIRECTION direction,
                                                TimeframeData &data)
{
   if(direction != DIR_BUY && direction != DIR_SELL) return SIGNAL_NONE;
   if(!data.is_valid || !data.is_closed || data.timeframe != PERIOD_H4 ||
      data.barIndex < 1 || data.candle_time <= 0)
      return SIGNAL_NONE;

   MovingAverage ma;
   BollingerBand band;
   BuildReEntryDirectionInputs(data, ma, band);

   // One canonical same-candle classification: Momentum > CSD > eCSD.
   if(DetectCSM(pair, PERIOD_H4, direction, data.barIndex))
      return SIGNAL_CSM;
   if(DetectCSD(pair, PERIOD_H4, direction, data.barIndex, ma, band))
      return SIGNAL_CSD;
   if(DetectECSD(pair, PERIOD_H4, direction, data.barIndex, ma))
      return SIGNAL_ECSD;
   return SIGNAL_NONE;
}

void ApplyH4AuthoritativeEvent(PairState &state,
                               ENUM_DIRECTION direction,
                               ENUM_SIGNAL_TYPE signalType,
                               datetime candleTime,
                               bool recovered)
{
   H4DirectionalOwner &owner = state.h4_direction_owner;
   if(direction != DIR_BUY && direction != DIR_SELL) return;
   if(signalType != SIGNAL_ECSD && signalType != SIGNAL_CSD &&
      signalType != SIGNAL_CSM) return;
   if(candleTime <= 0) return;

   bool handover = (owner.State == H4_OWNER_ACTIVE && owner.IsValid &&
                    owner.Direction != DIR_NONE && owner.Direction != direction);

   owner.State = H4_OWNER_ACTIVE;
   owner.Direction = direction;
   owner.SourceSignal = signalType;
   owner.SourceCandleTime = candleTime;
   owner.LastAdvanceSignal = signalType;
   owner.LastAdvanceCandleTime = candleTime;
   owner.IsValid = true;
   owner.RecoveryComplete = true;
   owner.RecoveredFromCheckpoint = recovered;
   owner.Reason = handover
                  ? "Atomic H4 owner handover by opposite source-valid direction/momentum"
                  : "H4 authoritative directional owner established/advanced";
}

bool VerifyH4OwnerCheckpoint(PairState &state,
                             ENUM_DIRECTION direction,
                             ENUM_SIGNAL_TYPE signalType,
                             datetime candleTime)
{
   if(direction != DIR_BUY && direction != DIR_SELL) return false;
   if(signalType != SIGNAL_ECSD && signalType != SIGNAL_CSD &&
      signalType != SIGNAL_CSM) return false;
   if(candleTime <= 0 || state.actual_symbol == "") return false;

   int shift = iBarShift(state.actual_symbol, PERIOD_H4, candleTime, true);
   if(shift < 1) return false; // checkpoint must reference a CLOSED H4 candle.

   TimeframeData data;
   InitTimeframeData(data);
   GetDataForTimeframe(state.actual_symbol, PERIOD_H4, candleTime, data);
   if(!data.is_valid || !data.is_closed) return false;

   ENUM_SIGNAL_TYPE verified =
      ClassifyH4AuthoritativeSignal(state.actual_symbol, direction, data);
   return (verified == signalType);
}

bool LoadVerifiedH4OwnerCheckpoint(PairState &state)
{
   string base = H4OwnerGVBase(state);
   if(!GlobalVariableCheck(base + "D") ||
      !GlobalVariableCheck(base + "S") ||
      !GlobalVariableCheck(base + "T"))
      return false;

   ENUM_DIRECTION direction =
      (ENUM_DIRECTION)((int)GlobalVariableGet(base + "D"));
   ENUM_SIGNAL_TYPE signalType =
      (ENUM_SIGNAL_TYPE)((int)GlobalVariableGet(base + "S"));
   datetime candleTime = (datetime)((int)GlobalVariableGet(base + "T"));

   if(!VerifyH4OwnerCheckpoint(state, direction, signalType, candleTime))
   {
      ClearH4OwnerCheckpoint(state);
      return false;
   }

   ResetH4DirectionalOwner(state.h4_direction_owner, H4_OWNER_ACTIVE);
   ApplyH4AuthoritativeEvent(state, direction, signalType, candleTime, true);
   state.h4_direction_owner.RecoveredFromCheckpoint = true;
   return true;
}

void ApplyH4ReplayCandle(PairState &state, TimeframeData &data)
{
   ENUM_SIGNAL_TYPE buySignal =
      ClassifyH4AuthoritativeSignal(state.actual_symbol, DIR_BUY, data);
   ENUM_SIGNAL_TYPE sellSignal =
      ClassifyH4AuthoritativeSignal(state.actual_symbol, DIR_SELL, data);

   // Simultaneous opposite authoritative classifications are fail-closed.
   if(buySignal != SIGNAL_NONE && sellSignal != SIGNAL_NONE)
   {
      ResetH4DirectionalOwner(state.h4_direction_owner, H4_OWNER_NONE);
      state.h4_direction_owner.LastProcessedH4CandleTime = data.candle_time;
      state.h4_direction_owner.Reason =
         "Ambiguous simultaneous H4 BUY/SELL authoritative events -> NO_OWNER";
      ClearH4OwnerCheckpoint(state);
      return;
   }

   if(buySignal != SIGNAL_NONE)
      ApplyH4AuthoritativeEvent(state, DIR_BUY, buySignal, data.candle_time, true);
   else if(sellSignal != SIGNAL_NONE)
      ApplyH4AuthoritativeEvent(state, DIR_SELL, sellSignal, data.candle_time, true);
   // Neutral H4 candle intentionally preserves inherited owner.

   state.h4_direction_owner.LastProcessedH4CandleTime = data.candle_time;
}

void RecoverH4DirectionalOwnerForPair(int pairIndex)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;
   PairState &state = g_pair_states[pairIndex];
   ResetH4DirectionalOwner(state.h4_direction_owner,
                           H4_OWNER_RECOVERY_UNRESOLVED);

   if(!state.pair_enabled || state.actual_symbol == "")
   {
      ResetH4DirectionalOwner(state.h4_direction_owner, H4_OWNER_NONE);
      state.h4_direction_owner.Reason = "H4 recovery unavailable for disabled/unresolved pair";
      return;
   }

   bool checkpointValid = LoadVerifiedH4OwnerCheckpoint(state);
   int bars = iBars(state.actual_symbol, PERIOD_H4);
   if(bars < 3)
   {
      if(!checkpointValid)
      {
         ResetH4DirectionalOwner(state.h4_direction_owner, H4_OWNER_NONE);
         state.h4_direction_owner.Reason = "Insufficient closed H4 history -> NO_OWNER";
      }
      state.h4_direction_owner.RecoveryComplete = true;
      return;
   }

   int startShift = bars - 2; // replay all available closed H4 history by default.
   if(checkpointValid)
   {
      int checkpointShift = iBarShift(state.actual_symbol, PERIOD_H4,
                                      state.h4_direction_owner.SourceCandleTime, true);
      if(checkpointShift >= 1)
         startShift = checkpointShift - 1;
      else
      {
         ResetH4DirectionalOwner(state.h4_direction_owner, H4_OWNER_NONE);
         checkpointValid = false;
         startShift = bars - 2;
      }
   }

   for(int shift = startShift; shift >= 1; shift--)
   {
      datetime candleTime = iTime(state.actual_symbol, PERIOD_H4, shift);
      if(candleTime <= 0) continue;

      TimeframeData data;
      InitTimeframeData(data);
      GetDataForTimeframe(state.actual_symbol, PERIOD_H4, candleTime, data);
      if(!data.is_valid || !data.is_closed) continue;

      ApplyH4ReplayCandle(state, data);
   }

   state.h4_direction_owner.RecoveryComplete = true;
   if(state.h4_direction_owner.State != H4_OWNER_ACTIVE ||
      !state.h4_direction_owner.IsValid)
   {
      state.h4_direction_owner.State = H4_OWNER_NONE;
      state.h4_direction_owner.Direction = DIR_NONE;
      state.h4_direction_owner.IsValid = false;
      state.h4_direction_owner.Reason =
         "Closed-H4 replay could not prove authoritative owner -> NO_OWNER";
      ClearH4OwnerCheckpoint(state);
      return;
   }

   SaveH4OwnerCheckpoint(state);
}

void RecoverH4DirectionalOwners()
{
   for(int i = 0; i < g_pair_count; i++)
      RecoverH4DirectionalOwnerForPair(i);
}

void UpdateRuntimeH4DirectionalOwner(int pairIndex)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;
   PairState &state = g_pair_states[pairIndex];
   TimeframeData &data = state.h4_data;

   if(!state.h4_direction_owner.RecoveryComplete) return;
   if(!data.is_valid || !data.is_closed || data.timeframe != PERIOD_H4 ||
      data.candle_time <= 0)
      return;
   if(data.candle_time == state.h4_direction_owner.LastProcessedH4CandleTime)
      return;

   ENUM_SIGNAL_TYPE buySignal =
      ClassifyH4AuthoritativeSignal(state.actual_symbol, DIR_BUY, data);
   ENUM_SIGNAL_TYPE sellSignal =
      ClassifyH4AuthoritativeSignal(state.actual_symbol, DIR_SELL, data);

   if(buySignal != SIGNAL_NONE && sellSignal != SIGNAL_NONE)
   {
      ResetH4DirectionalOwner(state.h4_direction_owner, H4_OWNER_NONE);
      state.h4_direction_owner.LastProcessedH4CandleTime = data.candle_time;
      state.h4_direction_owner.Reason =
         "Ambiguous simultaneous H4 BUY/SELL authoritative events -> NO_OWNER";
      ClearH4OwnerCheckpoint(state);
      return;
   }

   if(buySignal != SIGNAL_NONE)
      ApplyH4AuthoritativeEvent(state, DIR_BUY, buySignal, data.candle_time, false);
   else if(sellSignal != SIGNAL_NONE)
      ApplyH4AuthoritativeEvent(state, DIR_SELL, sellSignal, data.candle_time, false);
   // Else neutral candle: preserve inherited owner exactly as specified.

   state.h4_direction_owner.LastProcessedH4CandleTime = data.candle_time;
   if(state.h4_direction_owner.State == H4_OWNER_ACTIVE &&
      state.h4_direction_owner.IsValid)
      SaveH4OwnerCheckpoint(state);
}

void NoteH4ReEntryInheritance(int pairIndex, ReEntryData &reEntry)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;
   H4DirectionalOwner &owner = g_pair_states[pairIndex].h4_direction_owner;

   if(!owner.RecoveryComplete || !owner.IsValid ||
      owner.State != H4_OWNER_ACTIVE ||
      reEntry.State != RE_STATE_CONFIRMED || !reEntry.IsValid ||
      reEntry.Timeframe != PERIOD_H4 ||
      reEntry.Direction != owner.Direction ||
      reEntry.ConfirmationCandle <= 0)
      return;

   owner.LastAdvanceSignal = SIGNAL_RE_ENTRY;
   owner.LastAdvanceCandleTime = reEntry.ConfirmationCandle;
   owner.Reason = "Same-direction H4 Re-Entry inherited existing directional owner";
}

void RecoverExistingOrders()
{
'''
replace_once(recover_marker, owner_functions, 'M24 H4 recovery/owner functions')

# ---------------------------------------------------------------------------
# M26 initialization: recover H4 context after pair/magic identity validation.
# ---------------------------------------------------------------------------
init_recovery_old = '''   g_dashboard_needs_update = true;

   RebuildExecutionHistory();
   RecoverExistingOrders();
'''
init_recovery_new = '''   g_dashboard_needs_update = true;

   // CORE-V2-F4: reconstruct H4 directional context before any standalone H1
   // Re-Entry can be admitted. Failure resolves per-pair to NO_OWNER.
   RecoverH4DirectionalOwners();

   RebuildExecutionHistory();
   RecoverExistingOrders();
'''
replace_once(init_recovery_old, init_recovery_new, 'InitializeEA H4 owner recovery')

# ---------------------------------------------------------------------------
# M27 runtime: update H4 owner once per newly observed closed H4 candle, then
# use that owner to gate only standalone H1 Re-Entry candidate construction.
# ---------------------------------------------------------------------------
data_anchor = '''   GetDataForTimeframe(actual, PERIOD_M15, g_pair_states[pairIndex].tf_snapshot.M15_CandleTime,
                       g_pair_states[pairIndex].m15_data);

   BollingerBand h1Band, h1PrevBand, h4Band, h4PrevBand, m15Band;
'''
data_new = '''   GetDataForTimeframe(actual, PERIOD_M15, g_pair_states[pairIndex].tf_snapshot.M15_CandleTime,
                       g_pair_states[pairIndex].m15_data);

   // H4 owner is persistent across neutral H4 candles and changes only on
   // source-valid authoritative H4 direction/momentum events.
   UpdateRuntimeH4DirectionalOwner(pairIndex);

   BollingerBand h1Band, h1PrevBand, h4Band, h4PrevBand, m15Band;
'''
replace_once(data_anchor, data_new, 'M27 runtime H4 owner update')

# Explicitly record same-direction H4 Re-Entry as inherited lifecycle progress.
buy_re_anchor = '''         h1ReEntrySnapshot = g_pair_states[pairIndex].re_h1_buy_state;
         h4ReEntryState = g_pair_states[pairIndex].re_h4_buy_state;
         d1ReEntryState = g_pair_states[pairIndex].re_d1_buy_state;
'''
buy_re_new = '''         h1ReEntrySnapshot = g_pair_states[pairIndex].re_h1_buy_state;
         h4ReEntryState = g_pair_states[pairIndex].re_h4_buy_state;
         d1ReEntryState = g_pair_states[pairIndex].re_d1_buy_state;
         NoteH4ReEntryInheritance(pairIndex, h4ReEntryState);
'''
replace_once(buy_re_anchor, buy_re_new, 'BUY H4 ReEntry inheritance')

sell_re_anchor = '''         h1ReEntrySnapshot = g_pair_states[pairIndex].re_h1_sell_state;
         h4ReEntryState = g_pair_states[pairIndex].re_h4_sell_state;
         d1ReEntryState = g_pair_states[pairIndex].re_d1_sell_state;
'''
sell_re_new = '''         h1ReEntrySnapshot = g_pair_states[pairIndex].re_h1_sell_state;
         h4ReEntryState = g_pair_states[pairIndex].re_h4_sell_state;
         d1ReEntryState = g_pair_states[pairIndex].re_d1_sell_state;
         NoteH4ReEntryInheritance(pairIndex, h4ReEntryState);
'''
replace_once(sell_re_anchor, sell_re_new, 'SELL H4 ReEntry inheritance')

old_call = '''      BuildConfirmedReEntryCandidate(reEntry, reEntryCandidate);
'''
new_call = '''      BuildConfirmedReEntryCandidate(
         reEntry, g_pair_states[pairIndex].h4_direction_owner, reEntryCandidate);
'''
replace_once(old_call, new_call, 'standalone H1 candidate H4 owner call')

# ---------------------------------------------------------------------------
# Static regression: contract-specific invariants.
# ---------------------------------------------------------------------------
required = [
    'enum ENUM_H4_OWNER_STATE',
    'H4DirectionalOwner   h4_direction_owner;',
    'VerifyH4OwnerCheckpoint',
    'RecoverH4DirectionalOwners();',
    'UpdateRuntimeH4DirectionalOwner(pairIndex);',
    'H4_OWNER_ACTIVE',
    'GlobalVariableSet(base + "D"',
    'owner.Direction != reEntry.Direction',
    'NoteH4ReEntryInheritance(pairIndex, h4ReEntryState);',
]
for token in required:
    if token not in s:
        raise SystemExit(f'F4 invariant missing: {token}')

if s.count('RecoverH4DirectionalOwners();') != 1:
    raise SystemExit('H4 recovery must be invoked exactly once during initialization')
if s.count('UpdateRuntimeH4DirectionalOwner(pairIndex);') != 1:
    raise SystemExit('runtime H4 owner update must have one M27 call site')
if 'h4Owner.Direction != reEntry.Direction' not in s:
    raise SystemExit('standalone H1 direction compatibility gate missing')
if 'H4_OWNER_RECOVERY_UNRESOLVED' not in s or 'H4_OWNER_NONE' not in s:
    raise SystemExit('fail-safe H4 no-owner/recovery states missing')
if 'DetectECSD(pair, PERIOD_H4' not in s or 'DetectCSD(pair, PERIOD_H4' not in s or 'DetectCSM(pair, PERIOD_H4' not in s:
    raise SystemExit('source-valid H4 owner producers incomplete')

# Basic lexical balance, ignoring comments/strings approximately.
def strip_cpp(text):
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    text = re.sub(r'//.*', '', text)
    text = re.sub(r'"(?:\\.|[^"\\])*"', '""', text)
    return text

clean = strip_cpp(s)
for a, b, name in [('{','}','brace'), ('(',')','paren'), ('[',']','bracket')]:
    if clean.count(a) != clean.count(b):
        raise SystemExit(f'lexical {name} imbalance: {clean.count(a)} vs {clean.count(b)}')

SOURCE.write_text(s, encoding='utf-8')

AUDIT.write_text('''# CORE-V2-F4 — H4 Parent/Directional Owner Implementation Audit

Date: 2026-08-22
Status: **IMPLEMENTED / STATIC REGRESSION PASS — NATIVE METAEDITOR COMPILE + RUNTIME TRACE STILL REQUIRED**
Branch: `blueprint-dev`

## Scope
Implements the resolved `CORE_V2_F4_H1_RE_HTF_CONTEXT_DECISION.md` contract without changing REM/RRE/REE signatures or weakening F1/F2/F3 semantics.

## Implemented owner contract
- Standalone H1 Re-Entry now requires an active, recovered, same-direction H4 authoritative owner.
- H4 eCSD, CSD and CSM/Momentum can establish/advance directional ownership; classification precedence is CSM > CSD > eCSD for one closed H4 candle.
- A valid opposite authoritative event performs atomic handover. BUY and SELL owners are never simultaneously authoritative.
- A neutral H4 candle preserves the inherited owner; owner age alone does not expire it.
- Raw H4 Extreme/MHV do not establish the directional owner.
- D1, EMA50/Mid-BB, candle colour and absence-of-opposite are not fallback owners.
- Same-direction H4 Re-Entry is recorded as inherited lifecycle progress but does not manufacture direction from NO_OWNER.

## Standalone H1 execution gate
`BuildConfirmedReEntryCandidate()` receives the pair's H4 owner and rejects standalone H1 Re-Entry candidate construction unless recovery is complete, state is `H4_OWNER_ACTIVE`, owner is valid, and directions match. Combination signatures are untouched.

## Recovery
- Terminal Global Variables persist the latest independently verifiable H4 owner-producing event: direction, source family and closed-H4 candle time.
- Checkpoints are verified by exact closed-H4 timestamp plus re-running the same eCSD/CSD/CSM classifier at the provenance candle.
- Invalid/missing checkpoints are not trusted.
- Recovery replays closed H4 history chronologically, applying the same owner/handover rules used at runtime.
- If history cannot prove an owner, the pair resolves to `H4_OWNER_NONE`; standalone H1 execution remains blocked.
- Ambiguous simultaneous BUY/SELL authoritative classification is fail-closed to `NO_OWNER`.

## Static invariants
- explicit H4 owner/recovery/no-owner states exist;
- one per-pair owner exists, not separate simultaneous BUY/SELL owners;
- checkpoint verification and closed-H4 replay are wired before strategy execution;
- runtime update uses closed H4 data and preserves neutral-candle inheritance;
- standalone H1 Re-Entry checks H4 direction compatibility;
- no generic H4 owner TTL or D1/EMA fallback is introduced;
- same-direction H4 Re-Entry can inherit but cannot establish a no-owner direction;
- source lexical brace/parenthesis/bracket sanity passes.

## Remaining verification
1. Native MetaEditor compile must report **0 errors / 0 warnings** for the F1-F4 integrated source.
2. Runtime traces: fresh start with no provable history -> NO_OWNER block; eCSD establishes owner; neutral H4 preserves owner; same-direction H1 Re-Entry admitted; opposite H1 blocked; opposite H4 eCSD/CSD/CSM atomic handover; same-direction H4 Re-Entry inheritance; restart with valid checkpoint + replay; corrupt checkpoint fallback replay; insufficient history -> NO_OWNER.
3. Re-run Strategy Core V2 audit after F5/F6 closure.

Decision provenance: `blueprint/decisions/CORE_V2_F4_H1_RE_HTF_CONTEXT_DECISION.md`.
''', encoding='utf-8')

q = QUEUE.read_text(encoding='utf-8')
old_status = 'Status: **SPECIFICATION RESOLVED — USER APPROVED; CODE PATCH/AUDIT STILL PENDING**'
if old_status not in q:
    raise SystemExit('F4 queue status marker not found')
q = q.replace(old_status,
              'Status: **CODE IMPLEMENTED / STATIC REGRESSION PASS — NATIVE METAEDITOR COMPILE + RUNTIME TRACE PENDING**',
              1)
q = q.replace('Next action for F4: patch/audit H4 owner consumption and M24 recovery after the specification gates are closed.',
              'Next action for F4: native MetaEditor compile and H4 owner/recovery runtime traces; static implementation/regression is complete.',
              1)
QUEUE.write_text(q, encoding='utf-8')

c = CURRENT.read_text(encoding='utf-8')
c = c.replace(
    '- **Strategy Core V2:** F1 MHV/MLV and F2 Extreme maturity are implemented with static regression PASS; F3 Re-Entry Type 1 and F4 standalone H1/H4 parent-owner remain specification-resolved with code patch/audit pending. Native MetaEditor compile/runtime traces remain pending for the new F1/F2 code.',
    '- **Strategy Core V2:** F1 MHV/MLV, F2 Extreme maturity, F3 Re-Entry Type 1, and F4 standalone H1/H4 parent-owner are implemented with static regression PASS. Native MetaEditor compile/runtime traces remain pending for the integrated F1-F4 code.'
)
c = c.replace(
    '**Implement/audit CORE-V2-F3 Re-Entry Type 1 next, then CORE-V2-F4 H4 parent-owner; preserve the implemented F1/F2 lifecycle contracts.**',
    '**Proceed to CORE-V2-F5 BB-flat classification repair and CORE-V2-F6 timing verification, then re-run the Strategy Core audit; preserve the implemented F1-F4 lifecycle/owner contracts.**'
)
CURRENT.write_text(c, encoding='utf-8')
