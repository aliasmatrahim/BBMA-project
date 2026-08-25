#!/usr/bin/env python3
from pathlib import Path

SRC = Path('blueprint/source/BBMA_EA.mq4')
text = SRC.read_text(encoding='utf-8')

EXPECTED_BUILD = 'Version 4.5.1 - N2-13 Closed Outcome Shadow'
if EXPECTED_BUILD not in text:
    raise SystemExit('Unexpected BBMA_EA baseline build')


def function_block(src: str, signature: str) -> str:
    start = src.index(signature)
    brace = src.index('{', start)
    depth = 0
    for i in range(brace, len(src)):
        c = src[i]
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return src[start:i + 1]
    raise RuntimeError(f'unclosed function: {signature}')


def replace_once(old: str, new: str, label: str) -> None:
    global text
    n = text.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 anchor, found {n}')
    text = text.replace(old, new, 1)


protected = {
    'BuildPossibleCombinations': function_block(text, 'void BuildPossibleCombinations('),
    'ValidateSequence': function_block(text, 'void ValidateSequence('),
    'RunEntryPreflightAndExecute': function_block(text, 'bool RunEntryPreflightAndExecute('),
    'CheckRiskBeforeTrade': function_block(text, 'RiskStatus CheckRiskBeforeTrade('),
}

# Build identity.
replace_once(
    'Version 4.5.1 - N2-13 Closed Outcome Shadow',
    'Version 4.5.1 - D1O-02 Opportunity Execution',
    'build header')
replace_once(
    'BBMA EA V4.5.1 N2-13 initialized successfully',
    'BBMA EA V4.5.1 D1O-02 initialized successfully',
    'init build log')

# D1 opportunity / authority enums.
anchor = '''enum ENUM_D1_OWNER_STATE
{
   D1_OWNER_UNRESOLVED,
   D1_OWNER_BUY_CONFIRMED,
   D1_OWNER_SELL_CONFIRMED,
   D1_TRANSITION
};
'''
insert = anchor + '''
// D1O-02: user-approved D1 BBMA opportunity execution extension.
enum ENUM_D1_OPPORTUNITY_FAMILY
{
   D1_OPP_NONE,
   D1_OPP_EXTREME_TPW,
   D1_OPP_CSD,
   D1_OPP_RE_ENTRY,
   D1_OPP_MOMENTUM_RETRACE
};

enum ENUM_D1_AUTHORITY_MODE
{
   D1_AUTH_NONE,
   D1_AUTH_STRATEGIC_OWNER,
   D1_AUTH_OPPORTUNITY
};
'''
replace_once(anchor, insert, 'D1 opportunity enums')

# D1 opportunity state.
anchor = '''struct D1MajorTrendOwner
{
   ENUM_D1_OWNER_STATE  State;
   ENUM_DIRECTION       Direction;
   datetime             SourceCandleTime;
   datetime             LastProcessedD1CandleTime;
   double               Close1;
   double               MA50_1;
   double               MA50_2;
   bool                 IsValid;
   string               Reason;
};
'''
insert = anchor + '''
struct D1OpportunityJourney
{
   ENUM_D1_OPPORTUNITY_FAMILY Family;
   ENUM_DIRECTION             Direction;
   ENUM_SIGNAL_TYPE           SourceSignal;
   datetime                   SourceCandleTime;
   datetime                   ActivationTime;
   datetime                   LastProcessedD1CandleTime;
   string                     CycleID;
   bool                       Active;
   bool                       Tactical;
   bool                       TPWCompleted;
   string                     Reason;
};
'''
replace_once(anchor, insert, 'D1 opportunity struct')

# Freeze the selected authority into the decision payload.
anchor = '''   double               D1OwnerMA50Previous;
   bool                 D1OwnerSnapshotValid;
   
   // MUTABLE LIFECYCLE
'''
insert = '''   double               D1OwnerMA50Previous;
   bool                 D1OwnerSnapshotValid;

   // D1O-02 selected D1 authority identity. Legacy candidates stay strategic;
   // only Mode-2 opportunity candidates use D1_AUTH_OPPORTUNITY.
   ENUM_D1_AUTHORITY_MODE       D1AuthorityMode;
   ENUM_D1_OPPORTUNITY_FAMILY   D1OpportunityFamily;
   ENUM_DIRECTION               D1OpportunityDirection;
   ENUM_SIGNAL_TYPE             D1OpportunitySourceSignal;
   datetime                     D1OpportunitySourceCandleTime;
   datetime                     D1OpportunityActivationTime;
   string                       D1OpportunityCycleID;
   bool                         D1OpportunitySnapshotValid;
   
   // MUTABLE LIFECYCLE
'''
replace_once(anchor, insert, 'decision opportunity snapshot')

# Candidate metadata.
anchor = '''   int                  SequenceCompleteness;
   double               PatternStrength;
};

struct PairState
'''
insert = '''   int                  SequenceCompleteness;
   double               PatternStrength;

   // D1O-02 authority metadata; zero/false for all legacy candidates.
   bool                         UsesD1Opportunity;
   ENUM_D1_OPPORTUNITY_FAMILY   D1OpportunityFamily;
   ENUM_DIRECTION               D1OpportunityDirection;
   ENUM_SIGNAL_TYPE             D1OpportunitySourceSignal;
   datetime                     D1OpportunitySourceCandleTime;
   datetime                     D1OpportunityActivationTime;
   string                       D1OpportunityCycleID;
};

struct PairState
'''
replace_once(anchor, insert, 'candidate opportunity metadata')

# Pair state owners: M15 RE, D1 Extreme lifecycle, D1 opportunity.
replace_once(
'''   ReEntryData          re_d1_buy_state;
   ReEntryData          re_d1_sell_state;
   H4DirectionalOwner   h4_direction_owner;
   D1MajorTrendOwner    d1_major_trend_owner;
''',
'''   ReEntryData          re_d1_buy_state;
   ReEntryData          re_d1_sell_state;
   ReEntryData          re_m15_buy_state;
   ReEntryData          re_m15_sell_state;
   H4DirectionalOwner   h4_direction_owner;
   D1MajorTrendOwner    d1_major_trend_owner;
   D1OpportunityJourney d1_opportunity;
''', 'PairState opportunity owners')

replace_once(
'''   ExtremeLifecycleData extreme_h4_buy_lifecycle;
   ExtremeLifecycleData extreme_h4_sell_lifecycle;
   // F1 uses the F2 Extreme maturity engine as same-TF M15 parent provenance.
''',
'''   ExtremeLifecycleData extreme_h4_buy_lifecycle;
   ExtremeLifecycleData extreme_h4_sell_lifecycle;
   ExtremeLifecycleData extreme_d1_buy_lifecycle;
   ExtremeLifecycleData extreme_d1_sell_lifecycle;
   // F1 uses the F2 Extreme maturity engine as same-TF M15 parent provenance.
''', 'PairState D1 extreme lifecycle')

# Init new pair state fields.
replace_once(
'''   state.extreme_m15_sell_lifecycle.Maturity = EXT_MAT_NONE;
   state.extreme_m15_sell_lifecycle.Direction = DIR_SELL;
   state.extreme_m15_sell_lifecycle.Timeframe = PERIOD_M15;

   state.re_h1_buy_state.State = RE_STATE_NONE;
''',
'''   state.extreme_m15_sell_lifecycle.Maturity = EXT_MAT_NONE;
   state.extreme_m15_sell_lifecycle.Direction = DIR_SELL;
   state.extreme_m15_sell_lifecycle.Timeframe = PERIOD_M15;

   state.extreme_d1_buy_lifecycle.Maturity = EXT_MAT_NONE;
   state.extreme_d1_buy_lifecycle.Direction = DIR_BUY;
   state.extreme_d1_buy_lifecycle.Timeframe = PERIOD_D1;
   state.extreme_d1_sell_lifecycle.Maturity = EXT_MAT_NONE;
   state.extreme_d1_sell_lifecycle.Direction = DIR_SELL;
   state.extreme_d1_sell_lifecycle.Timeframe = PERIOD_D1;

   state.re_h1_buy_state.State = RE_STATE_NONE;
''', 'init D1 extremes')

replace_once(
'''   state.re_d1_sell_state.State = RE_STATE_NONE;
   state.re_d1_sell_state.Direction = DIR_SELL;
   state.re_d1_sell_state.Timeframe = PERIOD_D1;

   state.h4_direction_owner.State = H4_OWNER_RECOVERY_UNRESOLVED;
''',
'''   state.re_d1_sell_state.State = RE_STATE_NONE;
   state.re_d1_sell_state.Direction = DIR_SELL;
   state.re_d1_sell_state.Timeframe = PERIOD_D1;
   state.re_m15_buy_state.State = RE_STATE_NONE;
   state.re_m15_buy_state.Direction = DIR_BUY;
   state.re_m15_buy_state.Timeframe = PERIOD_M15;
   state.re_m15_sell_state.State = RE_STATE_NONE;
   state.re_m15_sell_state.Direction = DIR_SELL;
   state.re_m15_sell_state.Timeframe = PERIOD_M15;

   state.h4_direction_owner.State = H4_OWNER_RECOVERY_UNRESOLVED;
''', 'init M15 RE owners')

replace_once(
'''   state.d1_major_trend_owner.IsValid = false;
   state.d1_major_trend_owner.Reason = "D1 owner not evaluated";
}
''',
'''   state.d1_major_trend_owner.IsValid = false;
   state.d1_major_trend_owner.Reason = "D1 owner not evaluated";

   state.d1_opportunity.Family = D1_OPP_NONE;
   state.d1_opportunity.Direction = DIR_NONE;
   state.d1_opportunity.SourceSignal = SIGNAL_NONE;
   state.d1_opportunity.Active = false;
   state.d1_opportunity.Tactical = false;
   state.d1_opportunity.TPWCompleted = false;
   state.d1_opportunity.Reason = "D1 opportunity not evaluated";
}
''', 'init D1 opportunity')

# D1 opportunity owner logic. MHV/eCSD stay WATCH ONLY and never install an active family.
module12_anchor = '''//+------------------------------------------------------------------+
//| MODULE 12: RE-ENTRY ENGINE                                       |
//| LEVEL: INTERMEDIATE+                                             |
//+------------------------------------------------------------------+
'''
opportunity_logic = r'''
//+------------------------------------------------------------------+
//| MODULE 11J: D1 BBMA OPPORTUNITY JOURNEY (EXECUTION CONTEXT)     |
//| LEVEL: EXPERT-RESTRICTED                                         |
//+------------------------------------------------------------------+

string D1OpportunityFamilyText(ENUM_D1_OPPORTUNITY_FAMILY family)
{
   if(family == D1_OPP_EXTREME_TPW) return "EXT_TPW";
   if(family == D1_OPP_CSD) return "CSD";
   if(family == D1_OPP_RE_ENTRY) return "RE";
   if(family == D1_OPP_MOMENTUM_RETRACE) return "MOM_RE";
   return "NONE";
}

string D1AuthorityModeText(ENUM_D1_AUTHORITY_MODE mode)
{
   if(mode == D1_AUTH_STRATEGIC_OWNER) return "STRAT";
   if(mode == D1_AUTH_OPPORTUNITY) return "OPP";
   return "NONE";
}

void ResetD1OpportunityJourney(D1OpportunityJourney &journey, string reason)
{
   ZeroMemory(journey);
   journey.Family = D1_OPP_NONE;
   journey.Direction = DIR_NONE;
   journey.SourceSignal = SIGNAL_NONE;
   journey.Active = false;
   journey.Tactical = false;
   journey.TPWCompleted = false;
   journey.Reason = reason;
}

bool D1OpportunityIsConfirmedRE(ReEntryData &reEntry)
{
   return (reEntry.State == RE_STATE_CONFIRMED && reEntry.IsValid &&
           (reEntry.Direction == DIR_BUY || reEntry.Direction == DIR_SELL) &&
           reEntry.Timeframe == PERIOD_D1 && reEntry.ConfirmationCandle > 0);
}

bool SelectConfirmedD1OpportunityRE(ReEntryData &buyState, ReEntryData &sellState,
                                    ReEntryData &selected, bool &ambiguous)
{
   ZeroMemory(selected);
   bool buyValid = D1OpportunityIsConfirmedRE(buyState);
   bool sellValid = D1OpportunityIsConfirmedRE(sellState);
   ambiguous = (buyValid && sellValid);
   if(ambiguous || (!buyValid && !sellValid)) return false;
   selected = buyValid ? buyState : sellState;
   return true;
}

bool D1OpportunityExtremeMature(ExtremeLifecycleData &extreme)
{
   if(!extreme.IsValid || extreme.Timeframe != PERIOD_D1 ||
      extreme.ConfirmationCandleTime <= 0) return false;
   return (extreme.Maturity == EXT_MAT_REVERSAL_CONFIRMED ||
           extreme.Maturity == EXT_MAT_RETEST_PHASE ||
           extreme.Maturity == EXT_MAT_RETEST_READY);
}

bool SelectMatureD1OpportunityExtreme(ExtremeLifecycleData &buyState,
                                      ExtremeLifecycleData &sellState,
                                      ExtremeLifecycleData &selected,
                                      bool &ambiguous)
{
   ZeroMemory(selected);
   bool buyValid = D1OpportunityExtremeMature(buyState);
   bool sellValid = D1OpportunityExtremeMature(sellState);
   ambiguous = false;
   if(!buyValid && !sellValid) return false;
   if(buyValid && sellValid)
   {
      if(buyState.ConfirmationCandleTime == sellState.ConfirmationCandleTime)
      {
         ambiguous = true;
         return false;
      }
      selected = (buyState.ConfirmationCandleTime > sellState.ConfirmationCandleTime)
                 ? buyState : sellState;
      return true;
   }
   selected = buyValid ? buyState : sellState;
   return true;
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
      double high = iHigh(pair, PERIOD_D1, shift);
      double low = iLow(pair, PERIOD_D1, shift);
      if(high <= 0 || low <= 0) return true; // fail closed on incomplete history

      if(extreme.Direction == DIR_SELL)
      {
         double ma5Low = BBMALowMA(pair, PERIOD_D1, MA5_LOW_PERIOD, shift);
         double ma10Low = BBMALowMA(pair, PERIOD_D1, MA10_LOW_PERIOD, shift);
         if(ma5Low <= 0 || ma10Low <= 0) return true;
         if(low <= ma5Low || low <= ma10Low) return true;
      }
      else if(extreme.Direction == DIR_BUY)
      {
         double ma5High = BBMAHighMA(pair, PERIOD_D1, MA5_HIGH_PERIOD, shift);
         double ma10High = BBMAHighMA(pair, PERIOD_D1, MA10_HIGH_PERIOD, shift);
         if(ma5High <= 0 || ma10High <= 0) return true;
         if(high >= ma5High || high >= ma10High) return true;
      }
      else return true;
   }
   return false;
}

void InstallD1OpportunityJourney(D1OpportunityJourney &journey, string pair,
                                 ENUM_D1_OPPORTUNITY_FAMILY family,
                                 ENUM_DIRECTION direction,
                                 ENUM_SIGNAL_TYPE sourceSignal,
                                 datetime sourceCandleTime,
                                 datetime activationTime,
                                 bool tactical,
                                 string reason)
{
   ResetD1OpportunityJourney(journey, reason);
   journey.Family = family;
   journey.Direction = direction;
   journey.SourceSignal = sourceSignal;
   journey.SourceCandleTime = sourceCandleTime;
   journey.ActivationTime = activationTime;
   journey.Active = true;
   journey.Tactical = tactical;
   journey.TPWCompleted = false;
   journey.CycleID = SHORT_HASH(pair + "|D1OPP|" + IntegerToString((int)family) + "|" +
                                IntegerToString((int)direction) + "|" +
                                IntegerToString((int)sourceCandleTime), 16);
   journey.Reason = reason;
}

bool DetectD1OpportunityCSD(string pair, TimeframeData &data,
                            BollingerBand &band, ENUM_DIRECTION direction)
{
   if(!data.is_valid || !data.is_closed || data.barIndex < 1) return false;
   MovingAverage ma;
   ma.MA5_High = data.ma[0];
   ma.MA10_High = data.ma[1];
   ma.MA5_Low = data.ma[2];
   ma.MA10_Low = data.ma[3];
   ma.EMA50 = data.ma[4];
   return DetectCSD(pair, PERIOD_D1, direction, data.barIndex, ma, band);
}

bool DetectD1OpportunityECSDWatch(string pair, TimeframeData &data,
                                  ENUM_DIRECTION direction)
{
   if(!data.is_valid || !data.is_closed || data.barIndex < 1) return false;
   MovingAverage ma;
   ma.MA5_High = data.ma[0];
   ma.MA10_High = data.ma[1];
   ma.MA5_Low = data.ma[2];
   ma.MA10_Low = data.ma[3];
   ma.EMA50 = data.ma[4];
   return DetectECSD(pair, PERIOD_D1, direction, data.barIndex, ma);
}

void UpdateD1OpportunityJourney(int pairIndex, BollingerBand &d1Band)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;
   string pair = g_pair_states[pairIndex].actual_symbol;
   TimeframeData d1 = g_pair_states[pairIndex].d1_data;
   D1OpportunityJourney previous = g_pair_states[pairIndex].d1_opportunity;
   D1OpportunityJourney next = previous;

   if(!d1.is_valid || !d1.is_closed || d1.timeframe != PERIOD_D1 ||
      d1.candle_time <= 0 || d1.barIndex < 1)
   {
      ResetD1OpportunityJourney(next, "Invalid closed D1 opportunity snapshot");
      g_pair_states[pairIndex].d1_opportunity = next;
      return;
   }

   // Existing family remains structurally owned until invalidated or superseded.
   if(next.Active && next.Family == D1_OPP_RE_ENTRY)
   {
      ReEntryData owner = (next.Direction == DIR_BUY)
                          ? g_pair_states[pairIndex].re_d1_buy_state
                          : g_pair_states[pairIndex].re_d1_sell_state;
      if(!D1OpportunityIsConfirmedRE(owner) ||
         owner.ConfirmationCandle != next.SourceCandleTime)
      {
         next.Active = false;
         next.Reason = "D1 Re-Entry opportunity owner no longer valid";
      }
   }

   if(next.Active && next.Family == D1_OPP_EXTREME_TPW)
   {
      ExtremeLifecycleData owner = (next.Direction == DIR_BUY)
                                   ? g_pair_states[pairIndex].extreme_d1_buy_lifecycle
                                   : g_pair_states[pairIndex].extreme_d1_sell_lifecycle;
      if(!D1OpportunityExtremeMature(owner) ||
         owner.ConfirmationCandleTime != next.SourceCandleTime)
      {
         next.Active = false;
         next.Reason = "D1 Extreme opportunity owner no longer valid";
      }
      else if(D1OpportunityTPWCompletedSince(pair, owner, d1))
      {
         next.Active = false;
         next.TPWCompleted = true;
         next.Reason = "D1 Extreme normal TP-Wajib structurally completed";
      }
   }

   // A confirmed strategic reversal retires a stale normal directional family.
   if(next.Active && !next.Tactical &&
      (g_pair_states[pairIndex].d1_major_trend_owner.State == D1_OWNER_BUY_CONFIRMED ||
       g_pair_states[pairIndex].d1_major_trend_owner.State == D1_OWNER_SELL_CONFIRMED) &&
      g_pair_states[pairIndex].d1_major_trend_owner.IsValid &&
      g_pair_states[pairIndex].d1_major_trend_owner.Direction != next.Direction &&
      g_pair_states[pairIndex].d1_major_trend_owner.SourceCandleTime >= next.SourceCandleTime)
   {
      next.Active = false;
      next.Reason = "Strategic owner reversed against prior D1 opportunity";
   }

   datetime baselineSource = next.SourceCandleTime;
   bool installed = false;

   // Strongest active family: confirmed D1 Re-Entry.
   ReEntryData d1RE;
   bool reAmbiguous = false;
   if(SelectConfirmedD1OpportunityRE(g_pair_states[pairIndex].re_d1_buy_state,
                                     g_pair_states[pairIndex].re_d1_sell_state,
                                     d1RE, reAmbiguous))
   {
      if(d1RE.ConfirmationCandle >= baselineSource)
      {
         datetime activation = (d1RE.EntryCandle > 0)
                               ? d1RE.EntryCandle
                               : d1RE.ConfirmationCandle + GetTimeframeSeconds(PERIOD_D1);
         InstallD1OpportunityJourney(next, pair, D1_OPP_RE_ENTRY,
                                     d1RE.Direction, SIGNAL_RE_ENTRY,
                                     d1RE.ConfirmationCandle, activation, false,
                                     "Confirmed D1 Re-Entry opportunity");
         installed = true;
      }
   }
   else if(reAmbiguous)
   {
      next.Active = false;
      next.Reason = "Ambiguous opposite confirmed D1 Re-Entry owners";
   }

   // Momentum outranks CSD on the same D1 source candle. It opens a wait-for-RE window.
   if(!installed && !reAmbiguous)
   {
      bool csmBuy = DetectCSM(pair, PERIOD_D1, DIR_BUY, d1.barIndex);
      bool csmSell = DetectCSM(pair, PERIOD_D1, DIR_SELL, d1.barIndex);
      if(csmBuy != csmSell && d1.candle_time >= baselineSource)
      {
         ENUM_DIRECTION dir = csmBuy ? DIR_BUY : DIR_SELL;
         InstallD1OpportunityJourney(next, pair, D1_OPP_MOMENTUM_RETRACE,
                                     dir, SIGNAL_CSM, d1.candle_time,
                                     d1.candle_time + GetTimeframeSeconds(PERIOD_D1),
                                     false,
                                     "D1 Momentum/CSM continuation; wait for fresh LTF Re-Entry");
         installed = true;
      }
   }

   if(!installed && !reAmbiguous)
   {
      bool csdBuy = DetectD1OpportunityCSD(pair, d1, d1Band, DIR_BUY);
      bool csdSell = DetectD1OpportunityCSD(pair, d1, d1Band, DIR_SELL);
      if(csdBuy != csdSell && d1.candle_time >= baselineSource)
      {
         ENUM_DIRECTION dir = csdBuy ? DIR_BUY : DIR_SELL;
         InstallD1OpportunityJourney(next, pair, D1_OPP_CSD,
                                     dir, SIGNAL_CSD, d1.candle_time,
                                     d1.candle_time + GetTimeframeSeconds(PERIOD_D1),
                                     false, "Confirmed D1 CSD opportunity");
         installed = true;
      }
   }

   // eCSD is intentionally WATCH ONLY. It may be logged but never installs a family.
   bool ecsdWatchBuy = DetectD1OpportunityECSDWatch(pair, d1, DIR_BUY);
   bool ecsdWatchSell = DetectD1OpportunityECSDWatch(pair, d1, DIR_SELL);
   if(DebugLevel >= DBG_SIGNAL && ecsdWatchBuy != ecsdWatchSell)
      Print("[D1-OPP-WATCH] ", pair, " eCSD=", ecsdWatchBuy ? "B" : "S",
            " Action=WATCH_ONLY");

   if(!installed && !reAmbiguous)
   {
      ExtremeLifecycleData extreme;
      bool extremeAmbiguous = false;
      if(SelectMatureD1OpportunityExtreme(
            g_pair_states[pairIndex].extreme_d1_buy_lifecycle,
            g_pair_states[pairIndex].extreme_d1_sell_lifecycle,
            extreme, extremeAmbiguous))
      {
         if(extreme.ConfirmationCandleTime >= baselineSource &&
            !D1OpportunityTPWCompletedSince(pair, extreme, d1))
         {
            InstallD1OpportunityJourney(next, pair, D1_OPP_EXTREME_TPW,
                                        extreme.Direction, SIGNAL_EXTREME,
                                        extreme.ConfirmationCandleTime,
                                        extreme.ConfirmationCandleTime + GetTimeframeSeconds(PERIOD_D1),
                                        true,
                                        "Reversal-confirmed D1 Extreme with active TP-Wajib path");
            installed = true;
         }
      }
      else if(extremeAmbiguous)
      {
         next.Active = false;
         next.Reason = "Ambiguous opposite mature D1 Extremes";
      }
   }

   next.LastProcessedD1CandleTime = d1.candle_time;
   g_pair_states[pairIndex].d1_opportunity = next;

   bool changed = (previous.Family != next.Family ||
                   previous.Direction != next.Direction ||
                   previous.SourceCandleTime != next.SourceCandleTime ||
                   previous.Active != next.Active ||
                   previous.TPWCompleted != next.TPWCompleted);
   if(changed || DebugLevel >= DBG_SIGNAL)
   {
      Print("[D1-OPP] ", pair,
            " F=", D1OpportunityFamilyText(next.Family),
            " DIR=", (next.Direction == DIR_BUY ? "B" : (next.Direction == DIR_SELL ? "S" : "-")),
            " ACTIVE=", next.Active ? "Y" : "N",
            " TACT=", next.Tactical ? "Y" : "N",
            " SRC=", TimeToString(next.SourceCandleTime),
            " ACT=", TimeToString(next.ActivationTime),
            " CYCLE=", next.CycleID,
            " R=", next.Reason);
   }
}

'''
replace_once(module12_anchor, opportunity_logic + module12_anchor, 'M11J opportunity engine')

# M15 authority rules.
old = '''bool IsCandidateAllowedByD1Owner(ValidatedSequenceCandidate &candidate,
                                 PairState &pairState)
{
   if(!IsD1MajorTrendOwnerExecutionReady(pairState)) return false;
   return (candidate.Direction == pairState.d1_major_trend_owner.Direction);
}
'''
new = '''bool IsD1OpportunityCandidateAuthorityReady(ValidatedSequenceCandidate &candidate,
                                               PairState &pairState)
{
   if(!candidate.UsesD1Opportunity) return false;
   D1OpportunityJourney opportunity = pairState.d1_opportunity;
   if(!opportunity.Active || opportunity.CycleID == "") return false;
   if(candidate.D1OpportunityCycleID != opportunity.CycleID) return false;
   if(candidate.D1OpportunityFamily != opportunity.Family) return false;
   if(candidate.D1OpportunityDirection != opportunity.Direction) return false;
   if(candidate.Direction != opportunity.Direction) return false;
   if(candidate.D1OpportunitySourceCandleTime != opportunity.SourceCandleTime) return false;
   if(candidate.D1OpportunityActivationTime != opportunity.ActivationTime) return false;

   // Tactical Extreme/TPW may oppose MA50 or run during a valid transition,
   // but unresolved/malformed D1 strategic context still fails closed.
   if(opportunity.Family == D1_OPP_EXTREME_TPW)
   {
      D1MajorTrendOwner owner = pairState.d1_major_trend_owner;
      return (owner.IsValid && owner.SourceCandleTime > 0 &&
              owner.Close1 > 0.0 && owner.MA50_1 > 0.0 && owner.MA50_2 > 0.0 &&
              owner.State != D1_OWNER_UNRESOLVED);
   }

   if(!IsD1MajorTrendOwnerExecutionReady(pairState)) return false;
   return (candidate.Direction == pairState.d1_major_trend_owner.Direction);
}

bool IsCandidateAllowedByD1Owner(ValidatedSequenceCandidate &candidate,
                                 PairState &pairState)
{
   if(candidate.UsesD1Opportunity)
      return IsD1OpportunityCandidateAuthorityReady(candidate, pairState);

   if(!IsD1MajorTrendOwnerExecutionReady(pairState)) return false;
   return (candidate.Direction == pairState.d1_major_trend_owner.Direction);
}
'''
replace_once(old, new, 'M15 opportunity authority rule')

# Legacy freeze remains intact, tagged as strategic; add opportunity freeze.
replace_once(
'''   decision.D1OwnerMA50Previous = owner.MA50_2;
   decision.D1OwnerSnapshotValid = true;
   return true;
}

bool IsEntryModeCandidateAllowed''',
'''   decision.D1OwnerMA50Previous = owner.MA50_2;
   decision.D1OwnerSnapshotValid = true;
   decision.D1AuthorityMode = D1_AUTH_STRATEGIC_OWNER;
   decision.D1OpportunitySnapshotValid = false;
   return true;
}

bool FreezeD1OpportunitySnapshot(PairState &pairState,
                                 ValidatedSequenceCandidate &selected,
                                 BBMA_Decision &decision)
{
   if(!IsD1OpportunityCandidateAuthorityReady(selected, pairState)) return false;

   D1MajorTrendOwner owner = pairState.d1_major_trend_owner;
   if(!owner.IsValid || owner.SourceCandleTime <= 0 ||
      owner.Close1 <= 0.0 || owner.MA50_1 <= 0.0 || owner.MA50_2 <= 0.0)
      return false;

   decision.D1OwnerState = owner.State;
   decision.D1OwnerDirection = owner.Direction;
   decision.D1OwnerCandleTime = owner.SourceCandleTime;
   decision.D1OwnerClose = owner.Close1;
   decision.D1OwnerMA50Current = owner.MA50_1;
   decision.D1OwnerMA50Previous = owner.MA50_2;
   decision.D1OwnerSnapshotValid = true;

   decision.D1AuthorityMode = D1_AUTH_OPPORTUNITY;
   decision.D1OpportunityFamily = selected.D1OpportunityFamily;
   decision.D1OpportunityDirection = selected.D1OpportunityDirection;
   decision.D1OpportunitySourceSignal = selected.D1OpportunitySourceSignal;
   decision.D1OpportunitySourceCandleTime = selected.D1OpportunitySourceCandleTime;
   decision.D1OpportunityActivationTime = selected.D1OpportunityActivationTime;
   decision.D1OpportunityCycleID = selected.D1OpportunityCycleID;
   decision.D1OpportunitySnapshotValid = true;
   return true;
}

bool IsEntryModeCandidateAllowed''', 'freeze opportunity authority')

# Build a single canonical LTF opportunity cluster. H1 is preferred structural source;
# a simultaneously fresh M15 RE is included in the same identity, not double-traded.
anchor = '''void AppendValidatedCandidate(ValidatedSequenceCandidate &candidate,
                              ValidatedSequenceCandidate &candidates[], int &count)
{
   if(!candidate.Valid) return;
   ArrayResize(candidates, count + 1);
   candidates[count] = candidate;
   count++;
}
'''
insert = anchor + r'''

bool IsH4OpportunityAlignmentReady(PairState &state, ENUM_DIRECTION direction)
{
   return (state.h4_direction_owner.RecoveryComplete &&
           state.h4_direction_owner.IsValid &&
           state.h4_direction_owner.State == H4_OWNER_ACTIVE &&
           state.h4_direction_owner.Direction == direction);
}

datetime OpportunityReEntryReadyTime(ReEntryData &reEntry)
{
   if(reEntry.ConfirmationCandle <= 0 || reEntry.Timeframe <= 0) return 0;
   int tfSeconds = GetTimeframeSeconds(reEntry.Timeframe);
   if(tfSeconds <= 0) return 0;
   return reEntry.ConfirmationCandle + tfSeconds;
}

bool IsFreshOpportunityReEntry(ReEntryData &reEntry,
                               ENUM_DIRECTION direction,
                               int expectedTimeframe,
                               datetime activationTime)
{
   if(reEntry.State != RE_STATE_CONFIRMED || !reEntry.IsValid) return false;
   if(reEntry.Direction != direction || reEntry.Timeframe != expectedTimeframe) return false;
   if(reEntry.ConfirmationCandle <= 0 || activationTime <= 0) return false;
   if(reEntry.ExpiryCandleTime > 0 && g_processing_time > reEntry.ExpiryCandleTime) return false;
   return (OpportunityReEntryReadyTime(reEntry) > activationTime);
}

void SetOpportunityREComponent(ComponentIdentity &component, ReEntryData &reEntry)
{
   ZeroMemory(component);
   component.ComponentType = SIGNAL_RE_ENTRY;
   component.Direction = reEntry.Direction;
   component.Timeframe = reEntry.Timeframe;
   component.CandleTime = reEntry.ConfirmationCandle;
}

datetime MinPositiveExpiry(datetime a, datetime b)
{
   if(a <= 0) return b;
   if(b <= 0) return a;
   return MathMin(a, b);
}

void BuildD1OpportunityCandidate(int pairIndex,
                                 ValidatedSequenceCandidate &candidate)
{
   ZeroMemory(candidate);
   if(EntryMode != MODE_2_ALL_VALIDATED_BBMA) return;
   if(pairIndex < 0 || pairIndex >= g_pair_count) return;

   PairState state = g_pair_states[pairIndex];
   D1OpportunityJourney opportunity = state.d1_opportunity;
   if(!opportunity.Active || opportunity.Family == D1_OPP_NONE ||
      opportunity.CycleID == "" || opportunity.ActivationTime <= 0 ||
      (opportunity.Direction != DIR_BUY && opportunity.Direction != DIR_SELL))
      return;

   ReEntryData h1 = (opportunity.Direction == DIR_BUY)
                     ? state.re_h1_buy_state : state.re_h1_sell_state;
   ReEntryData m15 = (opportunity.Direction == DIR_BUY)
                      ? state.re_m15_buy_state : state.re_m15_sell_state;

   bool h1Fresh = IsFreshOpportunityReEntry(h1, opportunity.Direction,
                                             PERIOD_H1, opportunity.ActivationTime);
   bool m15Fresh = IsFreshOpportunityReEntry(m15, opportunity.Direction,
                                              PERIOD_M15, opportunity.ActivationTime);
   bool h4Aligned = IsH4OpportunityAlignmentReady(state, opportunity.Direction);

   if(opportunity.Family == D1_OPP_EXTREME_TPW)
   {
      // Stronger tactical confirmation: H4 owner + H1 confirmed RE are mandatory.
      if(!h4Aligned || !h1Fresh) return;
   }
   else
   {
      // Normal families are strategic-owner aligned. M15-only requires H4 support.
      if(!IsD1MajorTrendOwnerExecutionReady(state) ||
         state.d1_major_trend_owner.Direction != opportunity.Direction)
         return;
      if(!h1Fresh && !(m15Fresh && h4Aligned)) return;
   }

   int componentCount = 0;
   datetime expiry = 0;
   string ltfIdentity = "";

   if(h1Fresh)
   {
      SetOpportunityREComponent(candidate.Components[componentCount], h1);
      componentCount++;
      expiry = MinPositiveExpiry(expiry, h1.ExpiryCandleTime);
      ltfIdentity += "|H1:" + IntegerToString((int)h1.ConfirmationCandle);
   }

   // Same-cycle M15 is folded into the same cluster when H4 confirms lineage.
   if(m15Fresh && h4Aligned)
   {
      SetOpportunityREComponent(candidate.Components[componentCount], m15);
      componentCount++;
      expiry = MinPositiveExpiry(expiry, m15.ExpiryCandleTime);
      ltfIdentity += "|M15:" + IntegerToString((int)m15.ConfirmationCandle);
   }

   if(componentCount <= 0 || componentCount > 2) return;

   candidate.SequenceType = SIGNAL_RE_ENTRY;
   candidate.Direction = opportunity.Direction;
   candidate.ComponentCount = componentCount;
   candidate.SequenceStartTime = opportunity.SourceCandleTime;
   candidate.SequenceHash = SHORT_HASH("D1OPP|" + opportunity.CycleID + "|" +
                                      IntegerToString((int)opportunity.Family) + ltfIdentity, 16);
   candidate.Expiry = expiry;
   candidate.SLTPSource = SIGNAL_RE_ENTRY;
   candidate.PriorityTier = TIER_NONE;
   candidate.RequirementCompleteness = componentCount;
   candidate.SequenceCompleteness = componentCount;
   candidate.PatternStrength = 0;
   candidate.Valid = true;

   candidate.UsesD1Opportunity = true;
   candidate.D1OpportunityFamily = opportunity.Family;
   candidate.D1OpportunityDirection = opportunity.Direction;
   candidate.D1OpportunitySourceSignal = opportunity.SourceSignal;
   candidate.D1OpportunitySourceCandleTime = opportunity.SourceCandleTime;
   candidate.D1OpportunityActivationTime = opportunity.ActivationTime;
   candidate.D1OpportunityCycleID = opportunity.CycleID;
}
'''
replace_once(anchor, insert, 'D1 opportunity candidate builder')

# Opportunity RE source can be H1 or M15. If both are in one cluster, H1 owns SL/TP.
old = '''bool ResolveSelectedSLTPSourceComponent(ValidatedSequenceCandidate &selected,
                                        ComponentIdentity &source)
{
   ZeroMemory(source);

   int expectedTf = 0;
   if(selected.SequenceType == SIGNAL_RE_ENTRY)
      expectedTf = PERIOD_H1;
   else if(selected.SequenceType == SIGNAL_REM)
      expectedTf = PERIOD_H4;
   else if(selected.SequenceType == SIGNAL_RRE ||
           selected.SequenceType == SIGNAL_REE)
      expectedTf = PERIOD_D1;
   else
      return false;

   for(int i = 0; i < selected.ComponentCount; i++)
   {
      ComponentIdentity component = selected.Components[i];
      if(component.ComponentType != SIGNAL_RE_ENTRY) continue;
      if(component.Timeframe != expectedTf) continue;
      if(component.Direction != selected.Direction) continue;
      if(component.CandleTime <= 0) continue;

      source = component;
      return true;
   }

   return false;
}
'''
new = '''bool ResolveSelectedSLTPSourceComponent(ValidatedSequenceCandidate &selected,
                                        ComponentIdentity &source)
{
   ZeroMemory(source);

   if(selected.SequenceType == SIGNAL_RE_ENTRY && selected.UsesD1Opportunity)
   {
      // H1 is the structural source preference when H1+M15 are one cluster.
      for(int pass = 0; pass < 2; pass++)
      {
         int preferredTf = (pass == 0) ? PERIOD_H1 : PERIOD_M15;
         for(int i = 0; i < selected.ComponentCount; i++)
         {
            ComponentIdentity component = selected.Components[i];
            if(component.ComponentType != SIGNAL_RE_ENTRY) continue;
            if(component.Timeframe != preferredTf) continue;
            if(component.Direction != selected.Direction || component.CandleTime <= 0) continue;
            source = component;
            return true;
         }
      }
      return false;
   }

   int expectedTf = 0;
   if(selected.SequenceType == SIGNAL_RE_ENTRY)
      expectedTf = PERIOD_H1;
   else if(selected.SequenceType == SIGNAL_REM)
      expectedTf = PERIOD_H4;
   else if(selected.SequenceType == SIGNAL_RRE ||
           selected.SequenceType == SIGNAL_REE)
      expectedTf = PERIOD_D1;
   else
      return false;

   for(int i = 0; i < selected.ComponentCount; i++)
   {
      ComponentIdentity component = selected.Components[i];
      if(component.ComponentType != SIGNAL_RE_ENTRY) continue;
      if(component.Timeframe != expectedTf) continue;
      if(component.Direction != selected.Direction) continue;
      if(component.CandleTime <= 0) continue;
      source = component;
      return true;
   }
   return false;
}
'''
replace_once(old, new, 'opportunity SLTP source selector')

# Remove the old global strategic-only pre-block. Per-candidate authority now fails closed.
old = '''   // D1-02: D1 is the strategic new-entry gate. TRANSITION/UNRESOLVED
   // and stale/malformed owner identity fail closed before atomic direction selection.
   if(structurallyEligible > 0 && !IsD1MajorTrendOwnerExecutionReady(pairState))
   {
      Print("[D1-03][M15_D1_BLOCK] Pair=", pairState.actual_symbol,
            " State=", EnumToString(pairState.d1_major_trend_owner.State),
            " Dir=", EnumToString(pairState.d1_major_trend_owner.Direction),
            " Candle=", TimeToString(pairState.d1_major_trend_owner.SourceCandleTime));
      return;
   }

'''
new = '''   // D1O-02: authority is evaluated per candidate. Legacy candidates remain
   // MA50-strategic gated; only explicit Mode-2 D1 opportunity candidates may
   // use the separately frozen opportunity authority.
'''
replace_once(old, new, 'remove global strategic preblock')

# Freeze selected authority atomically.
old = '''   ValidatedSequenceCandidate selected = candidates[canonicalIdx];
   if(!FreezeD1OwnerSnapshot(pairState, decision))
   {
      Print("[D1-03][M15_D1_BLOCK] Pair=", pairState.actual_symbol,
            " Reason=freeze_failed");
      return;
   }

   decision.Valid = true;
'''
new = '''   ValidatedSequenceCandidate selected = candidates[canonicalIdx];
   bool authorityFrozen = selected.UsesD1Opportunity
                          ? FreezeD1OpportunitySnapshot(pairState, selected, decision)
                          : FreezeD1OwnerSnapshot(pairState, decision);
   if(!authorityFrozen)
   {
      Print("[D1O][M15_D1_BLOCK] Pair=", pairState.actual_symbol,
            " Reason=authority_freeze_failed");
      return;
   }

   decision.Valid = true;
'''
replace_once(old, new, 'M15 selected authority freeze')

# M16 must validate M15 Re-Entry components for opportunity clusters.
replace_once(
'''   else if(component.Timeframe == PERIOD_D1 && component.Direction == DIR_SELL)
      reEntry = pairState.re_d1_sell_state;
   else
      return false;
''',
'''   else if(component.Timeframe == PERIOD_D1 && component.Direction == DIR_SELL)
      reEntry = pairState.re_d1_sell_state;
   else if(component.Timeframe == PERIOD_M15 && component.Direction == DIR_BUY)
      reEntry = pairState.re_m15_buy_state;
   else if(component.Timeframe == PERIOD_M15 && component.Direction == DIR_SELL)
      reEntry = pairState.re_m15_sell_state;
   else
      return false;
''', 'M16 M15 RE owner validation')

# Add D1 opportunity snapshot validation and dispatch.
anchor = '''bool ValidateDecisionOwnerSnapshot(int pairIndex, BBMA_Decision &decision,
                                   bool &expired)
'''
insert = r'''bool ValidateDecisionD1OpportunitySnapshot(int pairIndex, BBMA_Decision &decision)
{
   if(pairIndex < 0 || pairIndex >= g_pair_count) return false;
   if(decision.D1AuthorityMode != D1_AUTH_OPPORTUNITY ||
      !decision.D1OpportunitySnapshotValid || !decision.D1OwnerSnapshotValid)
      return false;

   PairState state = g_pair_states[pairIndex];
   D1OpportunityJourney opportunity = state.d1_opportunity;
   if(!opportunity.Active || opportunity.CycleID == "") return false;
   if(decision.D1OpportunityFamily != opportunity.Family) return false;
   if(decision.D1OpportunityDirection != opportunity.Direction) return false;
   if(decision.D1OpportunitySourceSignal != opportunity.SourceSignal) return false;
   if(decision.D1OpportunitySourceCandleTime != opportunity.SourceCandleTime) return false;
   if(decision.D1OpportunityActivationTime != opportunity.ActivationTime) return false;
   if(decision.D1OpportunityCycleID != opportunity.CycleID) return false;
   if(decision.Direction != opportunity.Direction) return false;

   D1MajorTrendOwner owner = state.d1_major_trend_owner;
   if(!owner.IsValid || owner.SourceCandleTime <= 0 ||
      owner.Close1 <= 0.0 || owner.MA50_1 <= 0.0 || owner.MA50_2 <= 0.0)
      return false;
   if(decision.D1OwnerState != owner.State ||
      decision.D1OwnerDirection != owner.Direction ||
      decision.D1OwnerCandleTime != owner.SourceCandleTime ||
      decision.D1OwnerClose != owner.Close1 ||
      decision.D1OwnerMA50Current != owner.MA50_1 ||
      decision.D1OwnerMA50Previous != owner.MA50_2)
      return false;

   if(opportunity.Family != D1_OPP_EXTREME_TPW)
   {
      if(!IsD1MajorTrendOwnerExecutionReady(state)) return false;
      if(decision.Direction != owner.Direction) return false;
   }
   else if(owner.State == D1_OWNER_UNRESOLVED)
      return false;

   return true;
}

bool ValidateDecisionD1AuthoritySnapshot(int pairIndex, BBMA_Decision &decision)
{
   if(decision.D1AuthorityMode == D1_AUTH_OPPORTUNITY)
      return ValidateDecisionD1OpportunitySnapshot(pairIndex, decision);
   if(decision.D1AuthorityMode == D1_AUTH_STRATEGIC_OWNER)
      return ValidateDecisionD1OwnerSnapshot(pairIndex, decision);
   return false;
}

'''
replace_once(anchor, insert + anchor, 'M16 D1 opportunity snapshot validator')
replace_once(
'''   if(!ValidateDecisionD1OwnerSnapshot(pairIndex, decision))
   {
      decision.DecisionState = DEC_INVALIDATED;
      decision.RejectionReason = REJ_SEQUENCE_BREAK;
      Print("[D1-03][M16_D1_REJECT] Pair=", decision.Pair,
            " DecisionID=", decision.DecisionID,
            " FrozenState=", EnumToString(decision.D1OwnerState),
            " FrozenDir=", EnumToString(decision.D1OwnerDirection),
            " FrozenCandle=", TimeToString(decision.D1OwnerCandleTime));
      return;
   }
''',
'''   if(!ValidateDecisionD1AuthoritySnapshot(pairIndex, decision))
   {
      decision.DecisionState = DEC_INVALIDATED;
      decision.RejectionReason = REJ_SEQUENCE_BREAK;
      Print("[D1O][M16_D1_REJECT] Pair=", decision.Pair,
            " DecisionID=", decision.DecisionID,
            " Authority=", D1AuthorityModeText(decision.D1AuthorityMode),
            " Opp=", D1OpportunityFamilyText(decision.D1OpportunityFamily),
            " FrozenState=", EnumToString(decision.D1OwnerState),
            " FrozenDir=", EnumToString(decision.D1OwnerDirection),
            " FrozenCandle=", TimeToString(decision.D1OwnerCandleTime));
      return;
   }
''', 'M16 authority dispatch')

# M17 accepts M15 structural Re-Entry only for an explicitly frozen opportunity decision.
old = '''   if(decision.SignalType == SIGNAL_RE_ENTRY)
      return (source.Timeframe == PERIOD_H1);

   if(decision.SignalType == SIGNAL_REM)
'''
new = '''   if(decision.SignalType == SIGNAL_RE_ENTRY)
   {
      if(decision.D1AuthorityMode == D1_AUTH_OPPORTUNITY &&
         decision.D1OpportunitySnapshotValid)
         return (source.Timeframe == PERIOD_H1 || source.Timeframe == PERIOD_M15);
      return (source.Timeframe == PERIOD_H1);
   }

   if(decision.SignalType == SIGNAL_REM)
'''
replace_once(old, new, 'M17 opportunity RE source TF')

# Enrich N2 decision telemetry without changing existing parser prefix/identity fields.
replace_once(
'''         " J=", journeyId,
         " DID=", decisionToken,
         " DIDH=", decisionHash);
''',
'''         " J=", journeyId,
         " DID=", decisionToken,
         " DIDH=", decisionHash,
         " AUTH=", D1AuthorityModeText(decision.D1AuthorityMode),
         " OFAM=", D1OpportunityFamilyText(decision.D1OpportunityFamily),
         " OC=", (decision.D1OpportunityCycleID == "" ? "-" : decision.D1OpportunityCycleID));
''', 'N2 opportunity telemetry')

# Orchestration: add D1 band, D1 Extreme lifecycle, M15 RE owners, then one opportunity candidate.
replace_once(
'''   BollingerBand h1Band, h1PrevBand, h4Band, h4PrevBand, m15Band;
   ZeroMemory(h1Band); ZeroMemory(h1PrevBand);
   ZeroMemory(h4Band); ZeroMemory(h4PrevBand); ZeroMemory(m15Band);

   h1Band.TOP_BB =''',
'''   BollingerBand d1Band, h1Band, h1PrevBand, h4Band, h4PrevBand, m15Band;
   ZeroMemory(d1Band); ZeroMemory(h1Band); ZeroMemory(h1PrevBand);
   ZeroMemory(h4Band); ZeroMemory(h4PrevBand); ZeroMemory(m15Band);

   d1Band.TOP_BB = g_pair_states[pairIndex].d1_data.bollinger[0];
   d1Band.MID_BB = g_pair_states[pairIndex].d1_data.bollinger[1];
   d1Band.LOW_BB = g_pair_states[pairIndex].d1_data.bollinger[2];
   d1Band.Width = d1Band.TOP_BB - d1Band.LOW_BB;
   d1Band.State = BB_NONE;

   h1Band.TOP_BB =''', 'ProcessPair D1 band')

# D1 Extreme lifecycle is now an owned D1 opportunity source.
anchor = '''   // F1 parent provenance: M15 Extreme maturity uses the already-resolved F2
   // lifecycle. RAW Extreme alone cannot parent canonical MHV/MLV.
'''
insert = r'''   // D1O-02: D1 Extreme is a tactical opportunity source only after the
   // existing F2 reversal-confirmation maturity. RAW never authorizes entry.
   bool d1RawBuyExtreme = DetectExtreme(actual, DIR_BUY,
                                         g_pair_states[pairIndex].d1_data, d1Band);
   bool d1RawSellExtreme = DetectExtreme(actual, DIR_SELL,
                                          g_pair_states[pairIndex].d1_data, d1Band);
   UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_d1_buy_lifecycle,
                          actual, DIR_BUY, g_pair_states[pairIndex].d1_data,
                          d1Band, d1RawBuyExtreme);
   UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_d1_sell_lifecycle,
                          actual, DIR_SELL, g_pair_states[pairIndex].d1_data,
                          d1Band, d1RawSellExtreme);
   ResolveOppositeExtremeSupersession(g_pair_states[pairIndex].extreme_d1_buy_lifecycle,
                                      g_pair_states[pairIndex].extreme_d1_sell_lifecycle,
                                      g_pair_states[pairIndex].d1_data);

'''
replace_once(anchor, insert + anchor, 'ProcessPair D1 Extreme lifecycle')

# M15 RE state uses the already-generic M12 owner. It is not a raw M15 direction shortcut.
replace_once(
'''         UpdateReEntryState(g_pair_states[pairIndex].re_d1_buy_state, actual, direction,
                            g_pair_states[pairIndex].d1_data);
         h1ReEntrySnapshot = g_pair_states[pairIndex].re_h1_buy_state;
''',
'''         UpdateReEntryState(g_pair_states[pairIndex].re_d1_buy_state, actual, direction,
                            g_pair_states[pairIndex].d1_data);
         UpdateReEntryState(g_pair_states[pairIndex].re_m15_buy_state, actual, direction,
                            g_pair_states[pairIndex].m15_data);
         h1ReEntrySnapshot = g_pair_states[pairIndex].re_h1_buy_state;
''', 'ProcessPair BUY M15 RE')
replace_once(
'''         UpdateReEntryState(g_pair_states[pairIndex].re_d1_sell_state, actual, direction,
                            g_pair_states[pairIndex].d1_data);
         h1ReEntrySnapshot = g_pair_states[pairIndex].re_h1_sell_state;
''',
'''         UpdateReEntryState(g_pair_states[pairIndex].re_d1_sell_state, actual, direction,
                            g_pair_states[pairIndex].d1_data);
         UpdateReEntryState(g_pair_states[pairIndex].re_m15_sell_state, actual, direction,
                            g_pair_states[pairIndex].m15_data);
         h1ReEntrySnapshot = g_pair_states[pairIndex].re_h1_sell_state;
''', 'ProcessPair SELL M15 RE')

replace_once(
'''   // N1-03 NMJE shadow observation: all BUY/SELL owner states are current.
   // Intentionally read-only and excluded from allCandidates / M15 authority.
   UpdateNestedJourneyObservation(pairIndex);
''',
'''   // D1O-02: all D1/H4/H1/M15 owners are now current. Materialize one
   // canonical Mode-2 opportunity cluster at most; M15 remains final authority.
   UpdateD1OpportunityJourney(pairIndex, d1Band);
   ValidatedSequenceCandidate d1OpportunityCandidate;
   BuildD1OpportunityCandidate(pairIndex, d1OpportunityCandidate);
   AppendValidatedCandidate(d1OpportunityCandidate, allCandidates, allCandidateCount);

   // N1/N2 relationship observation remains descriptive; D1O execution uses
   // the separately owned/frozen D1 opportunity identity, not NESTED_RELATION.
   UpdateNestedJourneyObservation(pairIndex);
''', 'ProcessPair opportunity hook')

# Diagnostics: show opportunity + M15 RE without changing dashboard trade logic.
replace_once(
'''         " D1=", D10RE(g_pair_states[pairIndex].re_d1_buy_state.State), "/",
                     D10RE(g_pair_states[pairIndex].re_d1_sell_state.State));
''',
'''         " D1=", D10RE(g_pair_states[pairIndex].re_d1_buy_state.State), "/",
                     D10RE(g_pair_states[pairIndex].re_d1_sell_state.State),
         " M15=", D10RE(g_pair_states[pairIndex].re_m15_buy_state.State), "/",
                      D10RE(g_pair_states[pairIndex].re_m15_sell_state.State),
         " OPP=", D1OpportunityFamilyText(g_pair_states[pairIndex].d1_opportunity.Family), "/",
                    D10Dir(g_pair_states[pairIndex].d1_opportunity.Direction), "/",
                    (g_pair_states[pairIndex].d1_opportunity.Active ? "Y" : "N"));
''', 'D1O diagnostics')

# Static behavior guards.
for name, before in protected.items():
    after = function_block(text, {
        'BuildPossibleCombinations': 'void BuildPossibleCombinations(',
        'ValidateSequence': 'void ValidateSequence(',
        'RunEntryPreflightAndExecute': 'bool RunEntryPreflightAndExecute(',
        'CheckRiskBeforeTrade': 'RiskStatus CheckRiskBeforeTrade(',
    }[name])
    if after != before:
        raise SystemExit(f'protected function changed unexpectedly: {name}')

for required in (
    'set.Comp1.Timeframe == PERIOD_H4',
    'set.Comp2.Timeframe == PERIOD_H1',
    'set.Comp3.Timeframe == PERIOD_M15',
    'set.Comp1.Timeframe == PERIOD_D1',
    'D1_OPP_EXTREME_TPW',
    'D1_OPP_MOMENTUM_RETRACE',
    'EntryMode != MODE_2_ALL_VALIDATED_BBMA',
    're_m15_buy_state',
    're_m15_sell_state',
    'ValidateDecisionD1AuthoritySnapshot',
):
    if required not in text:
        raise SystemExit(f'missing required D1O guard: {required}')

# Existing safety caps are deliberately untouched.
for exact in (
    'input int      MaxTradePerPair                    = 2;',
    'input int      MaxTotalTrade                      = 10;',
    'input int      MaxActivePair                      = 7;',
):
    if exact not in text:
        raise SystemExit(f'portfolio cap changed unexpectedly: {exact}')

SRC.write_text(text, encoding='utf-8')
print('D1O-02 opportunity execution patch applied with static guards PASS')
