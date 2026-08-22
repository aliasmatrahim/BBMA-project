from pathlib import Path
import re

SOURCE = Path('blueprint/source/BBMA_EA.mq4')
AUDIT = Path('blueprint/CORE_V2_F3_IMPLEMENTATION_AUDIT.md')
QUEUE = Path('blueprint/MASTER_QUEUE.md')
CURRENT = Path('blueprint/CURRENT.md')

s = SOURCE.read_text(encoding='utf-8')


def replace_once(old: str, new: str, label: str):
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'{label}: expected 1 occurrence, found {count}')
    s = s.replace(old, new, 1)


def replace_between(start: str, end: str, replacement: str, label: str):
    global s
    a = s.find(start)
    if a < 0:
        raise SystemExit(f'{label}: start marker not found')
    b = s.find(end, a)
    if b < 0:
        raise SystemExit(f'{label}: end marker not found')
    if s.find(start, a + 1) >= 0:
        raise SystemExit(f'{label}: start marker not unique')
    s = s[:a] + replacement + s[b:]


# ---------------------------------------------------------------------------
# M02 — minimal Type-1 context state carried inside existing ReEntryData.
# ---------------------------------------------------------------------------
replace_once(
    'enum ENUM_RE_STATE { RE_STATE_NONE, RE_STATE_CANDIDATE, RE_STATE_CONFIRMED, RE_STATE_EXPIRED };\n',
    '''enum ENUM_RE_STATE { RE_STATE_NONE, RE_STATE_CANDIDATE, RE_STATE_CONFIRMED, RE_STATE_EXPIRED };\n\nenum ENUM_TYPE1_CONTEXT_STATE\n{\n   TYPE1_CTX_NONE,\n   TYPE1_CTX_DIRECTION_OWNER,\n   TYPE1_CTX_RANGING\n};\n''',
    'Type1 context enum'
)

old_tail = '''   int                  MinCandlesRequired;\n   int                  QualifyingCandles;\n   bool                 IsValid;\n   double               StrengthScore;\n   string               Reason;\n};\n'''
new_tail = '''   int                  MinCandlesRequired;\n   int                  QualifyingCandles;\n\n   ENUM_TYPE1_CONTEXT_STATE Type1ContextState;\n   ENUM_SIGNAL_TYPE     Type1OwnerSignal;\n   datetime             Type1OwnerCandleTime;\n   datetime             Type1RangingStartCandleTime;\n   double               Type1PreviousClose;\n\n   bool                 IsValid;\n   double               StrengthScore;\n   string               Reason;\n};\n'''
replace_once(old_tail, new_tail, 'ReEntryData Type1 context fields')

# ---------------------------------------------------------------------------
# M12 — replace only the Re-Entry module. F1/F2 code and later modules remain.
# ---------------------------------------------------------------------------
module12_start = '''//+------------------------------------------------------------------+\n//| MODULE 12: RE-ENTRY ENGINE                                       |\n//| LEVEL: INTERMEDIATE+                                             |\n//+------------------------------------------------------------------+\n'''
module13_start = '''//+------------------------------------------------------------------+\n//| MODULE 13: COMBINATION ENGINE (COLLECT ONLY)                     |\n//| LEVEL: INTERMEDIATE+                                             |\n//+------------------------------------------------------------------+\n'''

new_m12 = r'''//+------------------------------------------------------------------+
//| MODULE 12: RE-ENTRY ENGINE                                       |
//| LEVEL: INTERMEDIATE+                                             |
//+------------------------------------------------------------------+

bool GetReEntryMACluster(TimeframeData &data, ENUM_DIRECTION direction,
                         double &ma5, double &ma10)
{
   ma5 = 0;
   ma10 = 0;

   if(direction == DIR_BUY)
   {
      ma5 = data.ma[2];
      ma10 = data.ma[3];
   }
   else if(direction == DIR_SELL)
   {
      ma5 = data.ma[0];
      ma10 = data.ma[1];
   }
   else return false;

   return (ma5 > 0 && ma10 > 0);
}

bool HasReEntryMAClusterTouch(TimeframeData &data, ENUM_DIRECTION direction)
{
   double ma5, ma10;
   if(!GetReEntryMACluster(data, direction, ma5, ma10)) return false;
   if(data.close <= 0 || data.high <= 0 || data.low <= 0) return false;

   if(direction == DIR_BUY)
   {
      return (data.low <= MathMax(ma5, ma10) &&
              data.close >= ma5 && data.close >= ma10);
   }

   return (data.high >= MathMin(ma5, ma10) &&
           data.close <= ma5 && data.close <= ma10);
}

bool HasReEntryMA5OrMA50Touch(TimeframeData &data, ENUM_DIRECTION direction)
{
   double ma5, ma10;
   if(!GetReEntryMACluster(data, direction, ma5, ma10)) return false;
   if(data.ma[4] <= 0 || data.close <= 0 || data.high <= 0 || data.low <= 0) return false;

   if(direction == DIR_BUY)
   {
      bool ma5Touch = (data.low <= ma5 && data.close >= ma5);
      bool ma50Touch = (data.low <= data.ma[4] && data.close >= data.ma[4]);
      return (ma5Touch || ma50Touch);
   }

   bool ma5Touch = (data.high >= ma5 && data.close <= ma5);
   bool ma50Touch = (data.high >= data.ma[4] && data.close <= data.ma[4]);
   return (ma5Touch || ma50Touch);
}

void BuildReEntryDirectionInputs(TimeframeData &data, MovingAverage &ma,
                                 BollingerBand &band)
{
   ma.MA5_High = data.ma[0];
   ma.MA10_High = data.ma[1];
   ma.MA5_Low = data.ma[2];
   ma.MA10_Low = data.ma[3];
   ma.EMA50 = data.ma[4];

   ZeroMemory(band);
   band.TOP_BB = data.bollinger[0];
   band.MID_BB = data.bollinger[1];
   band.LOW_BB = data.bollinger[2];
   band.Width = band.TOP_BB - band.LOW_BB;
}

ENUM_SIGNAL_TYPE DetectReEntryDirectionOwnerSignal(string pair,
                                                    ENUM_DIRECTION direction,
                                                    TimeframeData &data)
{
   if(direction != DIR_BUY && direction != DIR_SELL) return SIGNAL_NONE;
   if(!data.is_valid || !data.is_closed || data.barIndex < 1) return SIGNAL_NONE;

   MovingAverage ma;
   BollingerBand band;
   BuildReEntryDirectionInputs(data, ma, band);

   // Momentum is the strongest same-candle classification. CSD is checked
   // before eCSD because a CSD candle also contains the eCSD MA crossing.
   if(DetectCSM(pair, data.timeframe, direction, data.barIndex)) return SIGNAL_CSM;
   if(DetectCSD(pair, data.timeframe, direction, data.barIndex, ma, band)) return SIGNAL_CSD;
   if(DetectECSD(pair, data.timeframe, direction, data.barIndex, ma)) return SIGNAL_ECSD;
   return SIGNAL_NONE;
}

bool DetectReEntry_Type2(string pair, ENUM_DIRECTION direction, TimeframeData &data,
                         bool &mostPowerful)
{
   mostPowerful = false;
   if(!EnableRE_Type2) return false;
   if(!data.is_valid || !data.is_closed || data.bollinger[1] <= 0) return false;

   double ma5, ma10;
   if(!GetReEntryMACluster(data, direction, ma5, ma10)) return false;

   bool powerful = IsNear(ma5, data.bollinger[1], pair) &&
                   IsNear(ma10, data.bollinger[1], pair);
   if(!powerful) return false;

   mostPowerful = (data.ma[4] > 0 && IsNear(data.ma[4], data.bollinger[1], pair));
   return true;
}

bool DetectReEntry_Type3(string pair, ENUM_DIRECTION direction, TimeframeData &data)
{
   if(!EnableRE_Type3) return false;
   if(!data.is_valid || !data.is_closed) return false;
   return DetectCSM(pair, data.timeframe, direction, data.barIndex);
}

bool DetectReEntry_Type4(string pair, ENUM_DIRECTION direction, TimeframeData &data)
{
   if(!EnableRE_Type4) return false;
   if(!data.is_valid || !data.is_closed) return false;

   MovingAverage ma;
   BollingerBand band;
   BuildReEntryDirectionInputs(data, ma, band);
   return DetectCSD(pair, data.timeframe, direction, data.barIndex, ma, band);
}

void ResetReEntryState(ReEntryData &reEntry, ENUM_DIRECTION direction, int timeframe)
{
   ZeroMemory(reEntry);
   reEntry.Type = RE_NONE;
   reEntry.State = RE_STATE_NONE;
   reEntry.Direction = direction;
   reEntry.Timeframe = timeframe;
   reEntry.Type1ContextState = TYPE1_CTX_NONE;
   reEntry.Type1OwnerSignal = SIGNAL_NONE;
}

bool IsReEntryIntrinsicExpired(ReEntryData &reEntry, datetime currentCandleTime)
{
   // CORE-V2-F3: Type 1 has structural owner lifetime, not a generic candle TTL.
   if(reEntry.Type == RE_TYPE_1) return false;
   if(reEntry.StartCandleTime <= 0 || reEntry.ExpiryCandleTime <= 0) return false;
   return (currentCandleTime > reEntry.ExpiryCandleTime);
}

void SetReEntrySnapshotLevels(ReEntryData &reEntry, TimeframeData &data)
{
   double ma5, ma10;
   GetReEntryMACluster(data, reEntry.Direction, ma5, ma10);
   reEntry.MA5_Level = ma5;
   reEntry.MA10_Level = ma10;
   reEntry.MA50_Level = data.ma[4];
   reEntry.MID_BB = data.bollinger[1];
}

void ConfirmReEntryState(ReEntryData &reEntry, TimeframeData &data, string reason)
{
   reEntry.State = RE_STATE_CONFIRMED;
   reEntry.ConfirmationBar = data.barIndex;
   reEntry.ConfirmationCandle = data.candle_time;
   reEntry.EntryCandle = data.candle_time;
   reEntry.EntryPrice = data.close;
   reEntry.IsValid = true;
   reEntry.LastUpdateBar = data.barIndex;
   reEntry.LastUpdateCandleTime = data.candle_time;
   SetReEntrySnapshotLevels(reEntry, data);
   reEntry.Reason = reason;
}

string ReEntryOwnerSignalName(ENUM_SIGNAL_TYPE type)
{
   if(type == SIGNAL_ECSD) return "eCSD";
   if(type == SIGNAL_CSD) return "CSD";
   if(type == SIGNAL_CSM) return "CSM";
   return "NONE";
}

void AdoptType1DirectionOwner(ReEntryData &reEntry, ENUM_DIRECTION direction,
                              TimeframeData &data, ENUM_SIGNAL_TYPE ownerSignal)
{
   ResetReEntryState(reEntry, direction, data.timeframe);
   reEntry.Type1ContextState = TYPE1_CTX_DIRECTION_OWNER;
   reEntry.Type1OwnerSignal = ownerSignal;
   reEntry.Type1OwnerCandleTime = data.candle_time;
   reEntry.Type1PreviousClose = data.close;
   reEntry.LastUpdateBar = data.barIndex;
   reEntry.LastUpdateCandleTime = data.candle_time;
   reEntry.Reason = "Type1 owner established by source-valid " +
                    ReEntryOwnerSignalName(ownerSignal) +
                    "; awaiting structural pause/retrace";
}

bool IsType1MAClusterCloseSideFailure(TimeframeData &data,
                                      ENUM_DIRECTION direction)
{
   double ma5, ma10;
   if(!GetReEntryMACluster(data, direction, ma5, ma10)) return true;
   if(data.close <= 0) return true;

   // Penetration of one MA is not automatically failure. The pending setup
   // fails only when price closes clear through the full MA5/MA10 cluster.
   if(direction == DIR_BUY)
      return (data.close < MathMin(ma5, ma10));
   if(direction == DIR_SELL)
      return (data.close > MathMax(ma5, ma10));
   return true;
}

bool IsType1StructuralRetraceEvidence(ReEntryData &reEntry,
                                      TimeframeData &data,
                                      ENUM_DIRECTION direction)
{
   if(reEntry.Type1PreviousClose <= 0 || data.close <= 0) return false;

   // A valid MA-cluster interaction is itself structural retrace evidence.
   // Otherwise use direction-only close progression toward the cluster; no
   // pip/ATR/EMA threshold or fixed candle count is introduced.
   if(HasReEntryMAClusterTouch(data, direction)) return true;
   if(direction == DIR_BUY)  return (data.close < reEntry.Type1PreviousClose);
   if(direction == DIR_SELL) return (data.close > reEntry.Type1PreviousClose);
   return false;
}

void BeginType1RangingCandidate(ReEntryData &reEntry,
                                ENUM_DIRECTION direction,
                                TimeframeData &data)
{
   reEntry.Type = RE_TYPE_1;
   reEntry.State = RE_STATE_CANDIDATE;
   reEntry.Direction = direction;
   reEntry.Timeframe = data.timeframe;
   reEntry.StartBar = data.barIndex;
   reEntry.StartCandleTime = data.candle_time;
   reEntry.LastUpdateBar = data.barIndex;
   reEntry.LastUpdateCandleTime = data.candle_time;
   reEntry.EntryPrice = 0;
   reEntry.EntryCandle = 0;
   reEntry.ConfirmationBar = 0;
   reEntry.ConfirmationCandle = 0;
   reEntry.ExpiryBar = 0;
   reEntry.ExpiryCandleTime = 0;
   reEntry.MinCandlesRequired = 0;
   reEntry.QualifyingCandles = 0;
   reEntry.IsValid = false;
   reEntry.Type1ContextState = TYPE1_CTX_RANGING;
   reEntry.Type1RangingStartCandleTime = data.candle_time;
   reEntry.Type1PreviousClose = data.close;
   SetReEntrySnapshotLevels(reEntry, data);
   reEntry.Reason = "Type1 structural ranging/retrace established; awaiting MA5/10 validation";
}

void StartSpecificReEntryCandidate(ReEntryData &reEntry,
                                   ENUM_RE_TYPE type,
                                   ENUM_DIRECTION direction,
                                   TimeframeData &data,
                                   bool mostPowerful)
{
   ResetReEntryState(reEntry, direction, data.timeframe);
   reEntry.Type = type;
   reEntry.State = RE_STATE_CANDIDATE;
   reEntry.StartBar = data.barIndex;
   reEntry.StartCandleTime = data.candle_time;
   reEntry.LastUpdateBar = data.barIndex;
   reEntry.LastUpdateCandleTime = data.candle_time;
   reEntry.ExpiryBar = MaxWaitBars_ReEntry;
   reEntry.ExpiryCandleTime =
      reEntry.StartCandleTime + MaxWaitBars_ReEntry * data.timeframe * 60;
   reEntry.QualifyingCandles = 1;
   SetReEntrySnapshotLevels(reEntry, data);

   if(type == RE_TYPE_2)
   {
      reEntry.MinCandlesRequired = 3;
      reEntry.Reason = mostPowerful
                       ? "Type2 candidate: MA5/10 + MID BB + MA50 collision (1/3)"
                       : "Type2 candidate: MA5/10 + MID BB collision (1/3)";
   }
   else if(type == RE_TYPE_3_CSM)
   {
      reEntry.MinCandlesRequired = 1;
      reEntry.Reason = "Type3 candidate: CSM formed; awaiting retrace to MA5 or MA50";
   }
   else if(type == RE_TYPE_4_CSD)
   {
      reEntry.MinCandlesRequired = 1;
      reEntry.Reason = "Type4 candidate: CSD formed; awaiting retrace to MA5/10";
   }
}

bool TryStartSpecificReEntry(ReEntryData &reEntry, string pair,
                             ENUM_DIRECTION direction, TimeframeData &data)
{
   // Exact Type 3/4 precursor families own their setup before generic Type 1.
   if(DetectReEntry_Type3(pair, direction, data))
   {
      StartSpecificReEntryCandidate(reEntry, RE_TYPE_3_CSM, direction, data, false);
      return true;
   }

   if(DetectReEntry_Type4(pair, direction, data))
   {
      StartSpecificReEntryCandidate(reEntry, RE_TYPE_4_CSD, direction, data, false);
      return true;
   }

   bool mostPowerful = false;
   if(DetectReEntry_Type2(pair, direction, data, mostPowerful))
   {
      StartSpecificReEntryCandidate(reEntry, RE_TYPE_2, direction, data, mostPowerful);
      return true;
   }

   return false;
}

void ResetType1AndAdoptCurrentOwner(ReEntryData &reEntry,
                                    ENUM_DIRECTION direction,
                                    TimeframeData &data,
                                    ENUM_SIGNAL_TYPE sameDirectionSignal)
{
   ResetReEntryState(reEntry, direction, data.timeframe);
   if(sameDirectionSignal != SIGNAL_NONE)
      AdoptType1DirectionOwner(reEntry, direction, data, sameDirectionSignal);
}

ENUM_RE_STATE UpdateReEntryState(ReEntryData &reEntry, string pair,
                                 ENUM_DIRECTION direction, TimeframeData &data)
{
   if(direction != DIR_BUY && direction != DIR_SELL) return RE_STATE_NONE;
   if(!data.is_valid || !data.is_closed || data.candle_time <= 0) return reEntry.State;

   if(reEntry.Direction != direction || reEntry.Timeframe != data.timeframe)
      ResetReEntryState(reEntry, direction, data.timeframe);

   // Do not process the same closed source-TF candle twice.
   if(reEntry.LastUpdateCandleTime > 0 &&
      data.candle_time <= reEntry.LastUpdateCandleTime)
      return reEntry.State;

   ENUM_DIRECTION oppositeDirection =
      (direction == DIR_BUY) ? DIR_SELL : DIR_BUY;
   ENUM_SIGNAL_TYPE sameSignal =
      DetectReEntryDirectionOwnerSignal(pair, direction, data);
   ENUM_SIGNAL_TYPE oppositeSignal =
      DetectReEntryDirectionOwnerSignal(pair, oppositeDirection, data);

   // Opposite source-valid direction/momentum atomically removes the old
   // Type-1 directional context. The opposite-direction state is managed by
   // its own ReEntryData owner in the parallel direction pass.
   if(oppositeSignal != SIGNAL_NONE &&
      (reEntry.Type == RE_TYPE_1 ||
       reEntry.Type1ContextState != TYPE1_CTX_NONE))
   {
      ResetReEntryState(reEntry, direction, data.timeframe);
      return RE_STATE_NONE;
   }

   if((reEntry.State == RE_STATE_CANDIDATE || reEntry.State == RE_STATE_CONFIRMED) &&
      IsReEntryIntrinsicExpired(reEntry, data.candle_time))
   {
      reEntry.State = RE_STATE_EXPIRED;
      reEntry.IsValid = false;
      reEntry.Reason = "MaxWaitBars_ReEntry expired";
      reEntry.LastUpdateBar = data.barIndex;
      reEntry.LastUpdateCandleTime = data.candle_time;
      return RE_STATE_EXPIRED;
   }

   // Confirmed Type 1 remains structurally valid only while its owner survives.
   if(reEntry.State == RE_STATE_CONFIRMED && reEntry.Type == RE_TYPE_1)
   {
      if(IsType1MAClusterCloseSideFailure(data, direction))
      {
         ResetReEntryState(reEntry, direction, data.timeframe);
         return RE_STATE_NONE;
      }

      if(sameSignal == SIGNAL_CSM || sameSignal == SIGNAL_CSD)
      {
         // Exact Type 3/4 may take ownership immediately on their precursor.
         if(TryStartSpecificReEntry(reEntry, pair, direction, data))
            return reEntry.State;
         ResetType1AndAdoptCurrentOwner(reEntry, direction, data, sameSignal);
         return reEntry.State;
      }

      if(sameSignal == SIGNAL_ECSD)
      {
         ResetType1AndAdoptCurrentOwner(reEntry, direction, data, sameSignal);
         return reEntry.State;
      }

      reEntry.IsValid = true;
      reEntry.LastUpdateBar = data.barIndex;
      reEntry.LastUpdateCandleTime = data.candle_time;
      reEntry.Type1PreviousClose = data.close;
      return RE_STATE_CONFIRMED;
   }

   if(reEntry.State == RE_STATE_EXPIRED)
   {
      ResetReEntryState(reEntry, direction, data.timeframe);
      // Continue on the same candle so a fresh structural owner is not lost.
   }

   if(reEntry.State == RE_STATE_NONE)
   {
      // Specific source-defined Re-Entry families own before generic Type 1.
      if(TryStartSpecificReEntry(reEntry, pair, direction, data))
         return reEntry.State;

      if(!EnableRE_Type1)
      {
         reEntry.LastUpdateBar = data.barIndex;
         reEntry.LastUpdateCandleTime = data.candle_time;
         return RE_STATE_NONE;
      }

      if(sameSignal != SIGNAL_NONE)
      {
         // eCSD/CSD/CSM is prior-move evidence only for Type 1; it is never
         // itself a Type-1 entry. Type3/4 were already given exact ownership.
         AdoptType1DirectionOwner(reEntry, direction, data, sameSignal);
         return RE_STATE_NONE;
      }

      if(reEntry.Type1ContextState != TYPE1_CTX_DIRECTION_OWNER)
      {
         reEntry.LastUpdateBar = data.barIndex;
         reEntry.LastUpdateCandleTime = data.candle_time;
         return RE_STATE_NONE;
      }

      if(IsType1MAClusterCloseSideFailure(data, direction))
      {
         ResetReEntryState(reEntry, direction, data.timeframe);
         return RE_STATE_NONE;
      }

      if(!IsType1StructuralRetraceEvidence(reEntry, data, direction))
      {
         reEntry.Type1PreviousClose = data.close;
         reEntry.LastUpdateBar = data.barIndex;
         reEntry.LastUpdateCandleTime = data.candle_time;
         return RE_STATE_NONE;
      }

      BeginType1RangingCandidate(reEntry, direction, data);

      // No fixed minimum candle count: if this structurally proven retrace
      // candle also reaches MA5/MA10 and closes on the valid side, it may
      // complete Type 1 immediately. This is not an MA-touch-only shortcut
      // because an earlier source-valid direction owner was mandatory.
      if(HasReEntryMAClusterTouch(data, direction))
      {
         ConfirmReEntryState(
            reEntry, data,
            (direction == DIR_BUY)
            ? "Type1 confirmed: prior BBMA direction -> structural ranging -> MA5/10 Low support retest"
            : "Type1 confirmed: prior BBMA direction -> structural ranging -> MA5/10 High resistance retest");
         return RE_STATE_CONFIRMED;
      }

      return RE_STATE_CANDIDATE;
   }

   if(reEntry.State == RE_STATE_CANDIDATE)
   {
      if(reEntry.Type == RE_TYPE_1)
      {
         // Structural invalidation / ownership transfer has priority.
         if(IsType1MAClusterCloseSideFailure(data, direction))
         {
            ResetReEntryState(reEntry, direction, data.timeframe);
            return RE_STATE_NONE;
         }

         if(sameSignal == SIGNAL_CSM || sameSignal == SIGNAL_CSD)
         {
            if(TryStartSpecificReEntry(reEntry, pair, direction, data))
               return reEntry.State;
            ResetType1AndAdoptCurrentOwner(reEntry, direction, data, sameSignal);
            return reEntry.State;
         }

         if(sameSignal == SIGNAL_ECSD)
         {
            ResetType1AndAdoptCurrentOwner(reEntry, direction, data, sameSignal);
            return reEntry.State;
         }

         if(HasReEntryMAClusterTouch(data, direction))
         {
            ConfirmReEntryState(
               reEntry, data,
               (direction == DIR_BUY)
               ? "Type1 confirmed: structural ranging retest at MA5/10 Low support"
               : "Type1 confirmed: structural ranging retest at MA5/10 High resistance");
            return RE_STATE_CONFIRMED;
         }

         // No fixed expiry and no invented minimum count. Keep the candidate
         // only while no structural invalidation/supersession has occurred.
         reEntry.Type1PreviousClose = data.close;
         reEntry.LastUpdateBar = data.barIndex;
         reEntry.LastUpdateCandleTime = data.candle_time;
         SetReEntrySnapshotLevels(reEntry, data);
         reEntry.Reason = "Type1 structural ranging active; awaiting MA5/10 support/resistance validation";
         return RE_STATE_CANDIDATE;
      }

      reEntry.LastUpdateBar = data.barIndex;
      reEntry.LastUpdateCandleTime = data.candle_time;
      SetReEntrySnapshotLevels(reEntry, data);

      if(reEntry.Type == RE_TYPE_2)
      {
         bool mostPowerful = false;
         if(!DetectReEntry_Type2(pair, direction, data, mostPowerful))
         {
            ResetReEntryState(reEntry, direction, data.timeframe);
            return RE_STATE_NONE;
         }

         reEntry.QualifyingCandles++;
         if(reEntry.QualifyingCandles < reEntry.MinCandlesRequired)
         {
            reEntry.Reason = mostPowerful
               ? "Type2 candidate: MA5/10 + MID BB + MA50 collision"
               : "Type2 candidate: MA5/10 + MID BB collision";
            return RE_STATE_CANDIDATE;
         }

         if(!HasReEntryMAClusterTouch(data, direction)) return RE_STATE_CANDIDATE;

         ConfirmReEntryState(reEntry, data,
            mostPowerful
            ? "Type2 confirmed: 3-candle MA5/10 + MID BB + MA50 confluence"
            : "Type2 confirmed: 3-candle MA5/10 + MID BB confluence");
         return RE_STATE_CONFIRMED;
      }

      if(reEntry.Type == RE_TYPE_3_CSM)
      {
         if(!HasReEntryMA5OrMA50Touch(data, direction)) return RE_STATE_CANDIDATE;

         ConfirmReEntryState(reEntry, data,
            "Type3 confirmed: post-CSM retrace to MA5 or MA50");
         return RE_STATE_CONFIRMED;
      }

      if(reEntry.Type == RE_TYPE_4_CSD)
      {
         if(!HasReEntryMAClusterTouch(data, direction)) return RE_STATE_CANDIDATE;

         ConfirmReEntryState(reEntry, data,
            "Type4 confirmed: post-CSD retrace to MA5/10");
         return RE_STATE_CONFIRMED;
      }

      return RE_STATE_CANDIDATE;
   }

   if(reEntry.State == RE_STATE_CONFIRMED)
   {
      reEntry.IsValid = true;
      reEntry.LastUpdateBar = data.barIndex;
      reEntry.LastUpdateCandleTime = data.candle_time;
   }

   return reEntry.State;
}

bool ExportConfirmedReEntrySignal(ReEntryData &reEntry, Signal &signal)
{
   ZeroMemory(signal);
   if(reEntry.State != RE_STATE_CONFIRMED || !reEntry.IsValid) return false;
   if(reEntry.ConfirmationCandle <= 0 || reEntry.EntryPrice <= 0) return false;

   signal.Type = SIGNAL_RE_ENTRY;
   signal.Direction = reEntry.Direction;
   signal.Valid = true;
   signal.Timeframe = reEntry.Timeframe;
   signal.Reason = reEntry.Reason;
   signal.BarIndex = reEntry.ConfirmationBar;
   signal.ExpiryBar = reEntry.ExpiryBar;
   signal.EntryPrice = reEntry.EntryPrice;
   signal.MA5_Level = reEntry.MA5_Level;
   signal.MA10_Level = reEntry.MA10_Level;
   signal.MA50_Level = reEntry.MA50_Level;
   signal.MID_BB = reEntry.MID_BB;
   signal.Timestamp = reEntry.ConfirmationCandle;
   signal.CandleTime = reEntry.ConfirmationCandle;
   signal.Close = reEntry.EntryPrice;
   return true;
}

void BuildReEntrySignal(ENUM_RE_TYPE type, ENUM_DIRECTION direction, double entryPrice,
                        double &sl, double &tp, double &slPoints)
{
   double point = GetPointSize(Symbol());
   double slDistance = MaxSLPips * point / 10;

   if(direction == DIR_BUY)
   {
      sl = entryPrice - slDistance;
      tp = entryPrice + slDistance * MinRRRatio;
   }
   else if(direction == DIR_SELL)
   {
      sl = entryPrice + slDistance;
      tp = entryPrice - slDistance * MinRRRatio;
   }
   slPoints = MathAbs(entryPrice - sl);
}

'''
replace_between(module12_start, module13_start, new_m12, 'Module 12 F3 replacement')

# ---------------------------------------------------------------------------
# Static regression: contract-specific invariants only.
# ---------------------------------------------------------------------------
if 'bool DetectReEntry_Type1(' in s:
    raise SystemExit('legacy MA-touch-only DetectReEntry_Type1 remains')
if s.count('TYPE1_CTX_DIRECTION_OWNER') < 3 or s.count('TYPE1_CTX_RANGING') < 3:
    raise SystemExit('Type1 structural context state wiring incomplete')
if 'if(reEntry.Type == RE_TYPE_1) return false;' not in s:
    raise SystemExit('Type1 fixed-expiry bypass missing')
if 'reEntry.ExpiryCandleTime = 0;' not in s:
    raise SystemExit('Type1 candidate still lacks explicit no-TTL mapping')
if s.find('DetectReEntry_Type3(pair, direction, data)') > s.find('DetectReEntry_Type2(pair, direction, data, mostPowerful)'):
    raise SystemExit('specific Type3 ownership must precede Type2/generic Type1 start')
if 'DetectReEntryDirectionOwnerSignal(pair, oppositeDirection, data)' not in s:
    raise SystemExit('opposite direction/momentum invalidation wiring missing')
if 'IsType1MAClusterCloseSideFailure' not in s:
    raise SystemExit('Type1 MA-cluster structural invalidation missing')
if 'IsType1StructuralRetraceEvidence' not in s:
    raise SystemExit('Type1 structural pause/retrace evidence missing')
if 'HasReEntryMAClusterTouch(data, direction)' not in s:
    raise SystemExit('Type1 MA5/10 final validation missing')

# Exact downstream entry/combo architecture must survive.
for required in [
    'candidate.SequenceType = SIGNAL_RE_ENTRY;',
    'return (candidate.SequenceType == SIGNAL_RE_ENTRY);',
    'BuildPossibleCombinations(rem, rre, ree, h4_reEntry, extreme, mlv,',
    'IsCombinationMLVReady(m15_mlv)',
]:
    if required not in s:
        raise SystemExit(f'downstream architecture drift: {required}')

# Lexical delimiter sanity after stripping comments/strings.
def strip_cpp(src: str) -> str:
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.S)
    src = re.sub(r'//.*', '', src)
    src = re.sub(r'"(?:\\.|[^"\\])*"', '""', src)
    return src

clean = strip_cpp(s)
for op, cl in [('(', ')'), ('{', '}'), ('[', ']')]:
    depth = 0
    for ch in clean:
        if ch == op:
            depth += 1
        elif ch == cl:
            depth -= 1
            if depth < 0:
                raise SystemExit(f'unbalanced {op}{cl}: early close')
    if depth != 0:
        raise SystemExit(f'unbalanced {op}{cl}: depth {depth}')

SOURCE.write_text(s, encoding='utf-8')

AUDIT.write_text('''# CORE-V2-F3 — Re-Entry Type 1 Structural Context Implementation Audit\n\nDate: 2026-08-22\nStatus: **IMPLEMENTED / STATIC REGRESSION PASS — NATIVE METAEDITOR COMPILE + RUNTIME TRACE STILL REQUIRED**\nBranch: `blueprint-dev`\n\n## Scope\nImplements the resolved `CORE_V2_F3_TYPE1_CONTEXT_DECISION.md` contract in M12 while preserving F1 MHV/MLV, F2 Extreme maturity, exact REM/RRE/REE signatures, risk, execution and dashboard semantics.\n\n## Removed mismatch\n- Removed the old `DetectReEntry_Type1()` MA5/MA10-touch-only shortcut.\n- Type 1 is no longer confirmed atomically from a single MA-cluster touch with no prior BBMA owner.\n- Removed generic `MaxWaitBars_ReEntry` expiry from Type 1 strategy lifetime only; Type 2/3/4 retain their existing project freshness behavior pending their own reviews.\n- Exact Type 3 (`CSM`) and Type 4 (`CSD`) precursor families are evaluated before generic Type 1 ownership, preventing Type 1 from stealing their setup.\n\n## Implemented Type 1 lifecycle\n`SOURCE-VALID SAME-TF eCSD/CSD/CSM OWNER -> STRUCTURAL MOMENTUM PAUSE / RETRACE TOWARD MA5/10 -> TYPE1 RANGING OWNER -> MA5/MA10 INTERACTION + VALID CLOSE-SIDE -> TYPE1 CONFIRMED`.\n\n### Prior move owner\n- Same-timeframe source-valid `eCSD`, `CSD`, or `CSM` is required before Type 1 ranging can exist.\n- The direction event is stored as structural owner/provenance only; it does not itself create a Type 1 entry.\n- EMA slope, ATR, fixed pip displacement and arbitrary candle-count movement are not used.\n\n### Structural pause/ranging\n- One candle that merely fails CSM is not enough.\n- Ranging/retrace starts only after the prior owner when a later closed candle provides actual retrace evidence toward the relevant MA cluster: direction-only close progression toward the cluster, or a valid cluster interaction itself.\n- No pip/ATR threshold and no mandatory BB_FLAT gate is introduced.\n- No fixed minimum candle count is used; if the structurally proven retrace candle also reaches the MA5/10 cluster and closes on the permitted side, it may complete Type 1 on that candle.\n\n### Validation and invalidation\n- Final BUY validation uses MA5/MA10 Low support interaction with close back/on the valid BUY side; SELL mirrors at MA5/MA10 High resistance.\n- A pending/confirmed Type 1 is cleared when price closes clear through the full MA5/MA10 cluster against the intended direction. Penetration of only one MA is not automatically treated as failure.\n- Opposite source-valid eCSD/CSD/CSM removes the old Type 1 direction owner.\n- Same-direction CSM/CSD during Type 1 transfers to exact Type 3/4 ownership when enabled; otherwise the old ranging state is reset and the new direction/momentum event becomes fresh prior-move provenance. Same-direction eCSD similarly refreshes the direction owner rather than validating stale Type 1.\n\n### Structural lifetime\n- Type 1 candidate and confirmed owner use `ExpiryCandleTime = 0`; `IsReEntryIntrinsicExpired()` explicitly bypasses `RE_TYPE_1`.\n- Type 1 therefore has no generic N-candle/session/day expiry. Its validity ends through structural invalidation/supersession.\n- Type 2/3/4 behavior is intentionally left outside F3 scope.\n\n## Static regression invariants\n- no MA-touch-only `DetectReEntry_Type1()` remains;\n- Type1 direction-owner and ranging states are present;\n- exact Type3/Type4 precursors have ownership precedence over generic Type1;\n- opposite direction/momentum invalidation and MA-cluster close-side failure are wired;\n- Type1 fixed TTL is disabled without globally changing Type2/3/4;\n- downstream standalone H1 `SIGNAL_RE_ENTRY` and REM/RRE/REE architecture remains present;\n- full-source brace/parenthesis/bracket lexical sanity passes.\n\n## Remaining verification\n1. Native MetaEditor compile must report **0 errors / 0 warnings**.\n2. Runtime traces should cover: no-owner MA touch rejection; eCSD->pause->touch confirmation; CSD/CSM owner cases; one non-CSM candle without retrace rejection; direct structural retrace+touch completion without fixed count; MA-cluster close-side failure; same-direction CSM reset/Type3 transfer; same-direction CSD Type4 transfer; opposite direction invalidation; long-lived Type1 with no timer expiry.\n3. F4 H4 parent-owner implementation must gate standalone H1 Re-Entry without weakening this same-TF Type1 lifecycle.\n\nDecision provenance: `blueprint/decisions/CORE_V2_F3_TYPE1_CONTEXT_DECISION.md`.\n''', encoding='utf-8')

# Tracking updates are deliberately narrow.
q = QUEUE.read_text(encoding='utf-8')
old_status = 'Status: **SPECIFICATION PHILOSOPHY RESOLVED — USER APPROVED; CODE PATCH/AUDIT STILL PENDING**'
new_status = 'Status: **CODE IMPLEMENTED / STATIC REGRESSION PASS — NATIVE METAEDITOR COMPILE + RUNTIME TRACE PENDING**'
if q.count(old_status) != 1:
    raise SystemExit(f'F3 queue status expected once, found {q.count(old_status)}')
q = q.replace(old_status, new_status, 1)
q = q.replace(
    'Next action for F3: patch/audit M12 only after the remaining higher-priority Core specification closures are reconciled; do not alter code during specification review.',
    'Next action for F3: native MetaEditor compile and runtime Type1 lifecycle traces; static implementation/regression is complete.',
    1
)
QUEUE.write_text(q, encoding='utf-8')

c = CURRENT.read_text(encoding='utf-8')
c = c.replace(
    '**Strategy Core V2:** F1 MHV/MLV and F2 Extreme maturity are implemented with static regression PASS; F3 Re-Entry Type 1 and F4 standalone H1/H4 parent-owner remain specification-resolved with code patch/audit pending. Native MetaEditor compile/runtime traces remain pending for the new F1/F2 code.',
    '**Strategy Core V2:** F1 MHV/MLV, F2 Extreme maturity and F3 Re-Entry Type 1 are implemented with static regression PASS; F4 standalone H1/H4 parent-owner remains specification-resolved with code patch/audit pending. Native MetaEditor compile/runtime traces remain pending for the new F1/F2/F3 code.',
    1
)
c = c.replace(
    '**Implement/audit CORE-V2-F3 Re-Entry Type 1 next, then CORE-V2-F4 H4 parent-owner; preserve the implemented F1/F2 lifecycle contracts.**',
    '**Implement/audit CORE-V2-F4 H4 parent-owner next; preserve the implemented F1/F2/F3 lifecycle contracts.**',
    1
)
CURRENT.write_text(c, encoding='utf-8')

print('CORE-V2-F3 patch and static regression prepared successfully')
