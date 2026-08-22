from pathlib import Path

SOURCE = Path('blueprint/source/BBMA_EA.mq4')
AUDIT = Path('blueprint/CORE_V2_F1_IMPLEMENTATION_AUDIT.md')
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
# M02 — one canonical MHV/MLV state model.
# ---------------------------------------------------------------------------
replace_once(
    'enum ENUM_MLV_STATE { MLV_NONE, MLV_CANDIDATE, MLV_CONFIRMED, MLV_VOID, MLV_EXPIRED };\n',
    '''enum ENUM_MLV_STATE\n{\n   MLV_NONE,\n   MLV_PARENT_READY,\n   MLV_TP_COMPLETE,\n   MLV_LOSS_DEVELOPING,\n   MLV_FORMATION_ESTABLISHED,\n   MLV_RETEST_COMPLETE,\n   MLV_DIRECTION_TAKEN,\n   MLV_VOID,\n   MLV_SUPERSEDED\n};\n''',
    'canonical MLV enum'
)

struct_start = 'struct MLVData\n{\n'
struct_end = 'struct ReEntryData\n{\n'
canonical_struct = '''struct MLVData\n{\n   ENUM_MLV_STATE       State;\n   ENUM_DIRECTION       Direction;\n   ENUM_DIRECTION       ParentExtremeDirection;\n   int                  Timeframe;\n   string               Reason;\n\n   datetime             ParentRawCandleTime;\n   datetime             ParentConfirmationCandleTime;\n   datetime             TPWajibCandleTime;\n\n   double               ProvisionalBodyAnchor;\n   double               FrozenMarkedBody;\n   double               PreviousClose;\n\n   int                  StartBar;\n   datetime             StartCandleTime;\n   int                  LastUpdateBar;\n   datetime             LastUpdateCandleTime;\n\n   int                  ConfirmationBar;\n   datetime             ConfirmationCandleTime;\n   double               ConfirmationClose;\n\n   int                  RetestBar;\n   datetime             RetestCandleTime;\n   int                  DirectionTakeoverBar;\n   datetime             DirectionTakeoverCandleTime;\n\n   int                  VoidBar;\n   datetime             VoidCandleTime;\n   int                  SupersededBar;\n   datetime             SupersededCandleTime;\n\n   bool                 InvalidationWindowOpen;\n   bool                 IsValid;\n\n   bool                 SupersessionCandidateActive;\n   int                  SupersessionRawBar;\n   datetime             SupersessionRawCandleTime;\n};\n\n'''
replace_between(struct_start, struct_end, canonical_struct, 'canonical MLVData')

pair_marker = '''   ExtremeLifecycleData extreme_h4_buy_lifecycle;\n   ExtremeLifecycleData extreme_h4_sell_lifecycle;\n'''
pair_insert = pair_marker + '''   // F1 uses the F2 Extreme maturity engine as same-TF M15 parent provenance.\n   ExtremeLifecycleData extreme_m15_buy_lifecycle;\n   ExtremeLifecycleData extreme_m15_sell_lifecycle;\n'''
replace_once(pair_marker, pair_insert, 'M15 Extreme lifecycle owner fields')

init_old = '''   state.mlv_buy_state.State = MLV_NONE;\n   state.mlv_buy_state.Direction = DIR_BUY;\n   state.mlv_sell_state.State = MLV_NONE;\n   state.mlv_sell_state.Direction = DIR_SELL;\n'''
init_new = '''   state.mlv_buy_state.State = MLV_NONE;\n   state.mlv_buy_state.Direction = DIR_BUY;\n   state.mlv_buy_state.ParentExtremeDirection = DIR_SELL;\n   state.mlv_buy_state.Timeframe = PERIOD_M15;\n   state.mlv_sell_state.State = MLV_NONE;\n   state.mlv_sell_state.Direction = DIR_SELL;\n   state.mlv_sell_state.ParentExtremeDirection = DIR_BUY;\n   state.mlv_sell_state.Timeframe = PERIOD_M15;\n\n   state.extreme_m15_buy_lifecycle.Maturity = EXT_MAT_NONE;\n   state.extreme_m15_buy_lifecycle.Direction = DIR_BUY;\n   state.extreme_m15_buy_lifecycle.Timeframe = PERIOD_M15;\n   state.extreme_m15_sell_lifecycle.Maturity = EXT_MAT_NONE;\n   state.extreme_m15_sell_lifecycle.Direction = DIR_SELL;\n   state.extreme_m15_sell_lifecycle.Timeframe = PERIOD_M15;\n'''
replace_once(init_old, init_new, 'InitPairState MHV/M15 Extreme initialization')

# ---------------------------------------------------------------------------
# M09 — canonical source-aligned lifecycle. Removes one-candle DetectMHV,
# synthetic neckline/double-top formula, fixed-pip tolerance and MLV TTL.
# ---------------------------------------------------------------------------
module09_start = '''//+------------------------------------------------------------------+\n//| MODULE 09: MHV & MLV STATE ENGINE                                |\n//| LEVEL: INTERMEDIATE+                                             |\n//+------------------------------------------------------------------+\n'''
module10_start = '''//+------------------------------------------------------------------+\n//| MODULE 10: CSM, CSD, eCSD                                        |\n//| LEVEL: INTERMEDIATE                                              |\n//+------------------------------------------------------------------+\n'''

new_m09 = r'''//+------------------------------------------------------------------+
//| MODULE 09: MHV & MLV CANONICAL LIFECYCLE ENGINE                  |
//| LEVEL: INTERMEDIATE+                                             |
//+------------------------------------------------------------------+

ENUM_DIRECTION GetMHVParentExtremeDirection(ENUM_DIRECTION mhvDirection)
{
   if(mhvDirection == DIR_BUY) return DIR_SELL;
   if(mhvDirection == DIR_SELL) return DIR_BUY;
   return DIR_NONE;
}

bool IsMHVParentExtremeMature(ExtremeLifecycleData &parent)
{
   if(!parent.IsValid) return false;
   if(parent.ConfirmationCandleTime <= 0 || parent.Timeframe != PERIOD_M15)
      return false;

   return (parent.Maturity == EXT_MAT_REVERSAL_CONFIRMED ||
           parent.Maturity == EXT_MAT_RETEST_PHASE ||
           parent.Maturity == EXT_MAT_RETEST_READY);
}

bool IsCanonicalMLVMatureState(ENUM_MLV_STATE state)
{
   return (state == MLV_FORMATION_ESTABLISHED ||
           state == MLV_RETEST_COMPLETE ||
           state == MLV_DIRECTION_TAKEN);
}

void ResetMLVState(MLVData &mlv, ENUM_DIRECTION direction)
{
   ZeroMemory(mlv);
   mlv.State = MLV_NONE;
   mlv.Direction = direction;
   mlv.ParentExtremeDirection = GetMHVParentExtremeDirection(direction);
   mlv.Timeframe = PERIOD_M15;
}

void AttachCanonicalMHVParent(MLVData &mlv, ENUM_DIRECTION direction,
                              ExtremeLifecycleData &parent,
                              TimeframeData &data)
{
   ResetMLVState(mlv, direction);
   mlv.State = MLV_PARENT_READY;
   mlv.ParentRawCandleTime = parent.RawCandleTime;
   mlv.ParentConfirmationCandleTime = parent.ConfirmationCandleTime;
   mlv.LastUpdateBar = data.barIndex;
   mlv.LastUpdateCandleTime = data.candle_time;
   mlv.PreviousClose = data.close;
   mlv.IsValid = false;
   mlv.Reason = "Canonical MHV parent attached: reversal-confirmed M15 Extreme";
}

void MarkCanonicalMLVVoid(MLVData &mlv, TimeframeData &data, string reason)
{
   mlv.State = MLV_VOID;
   mlv.IsValid = false;
   mlv.InvalidationWindowOpen = false;
   mlv.VoidBar = data.barIndex;
   mlv.VoidCandleTime = data.candle_time;
   mlv.LastUpdateBar = data.barIndex;
   mlv.LastUpdateCandleTime = data.candle_time;
   mlv.PreviousClose = data.close;
   mlv.Reason = reason;
}

void MarkCanonicalMLVSuperseded(MLVData &mlv, TimeframeData &data, string reason)
{
   mlv.State = MLV_SUPERSEDED;
   mlv.IsValid = false;
   mlv.InvalidationWindowOpen = false;
   mlv.SupersededBar = data.barIndex;
   mlv.SupersededCandleTime = data.candle_time;
   mlv.LastUpdateBar = data.barIndex;
   mlv.LastUpdateCandleTime = data.candle_time;
   mlv.PreviousClose = data.close;
   mlv.Reason = reason;
}

bool IsMHVTPWajibCompleted(TimeframeData &data, ENUM_DIRECTION parentDirection)
{
   if(data.high <= 0 || data.low <= 0) return false;

   if(parentDirection == DIR_SELL)
   {
      double ma5Low = data.ma[2];
      double ma10Low = data.ma[3];
      if(ma5Low <= 0 || ma10Low <= 0) return false;
      return (data.low <= ma5Low || data.low <= ma10Low);
   }

   if(parentDirection == DIR_BUY)
   {
      double ma5High = data.ma[0];
      double ma10High = data.ma[1];
      if(ma5High <= 0 || ma10High <= 0) return false;
      return (data.high >= ma5High || data.high >= ma10High);
   }

   return false;
}

bool IsMHVContinuationInvalidation(string pair, ENUM_DIRECTION mhvDirection,
                                   TimeframeData &data, BollingerBand &band)
{
   if(data.close <= 0 || band.TOP_BB <= 0 || band.LOW_BB <= 0) return false;

   // Bottom-side BUY MHV follows a prior SELL Extreme/TP move: a fresh
   // downside outer-BB close / SELL CSM means prior momentum continued.
   if(mhvDirection == DIR_BUY)
   {
      if(data.close < band.LOW_BB) return true;
      return DetectCSM(pair, data.timeframe, DIR_SELL, data.barIndex);
   }

   // Top-side SELL MHV mirrors the rule after a prior BUY Extreme/TP move.
   if(mhvDirection == DIR_SELL)
   {
      if(data.close > band.TOP_BB) return true;
      return DetectCSM(pair, data.timeframe, DIR_BUY, data.barIndex);
   }

   return false;
}

bool IsMHVLossPhaseEligible(string pair, ENUM_DIRECTION mhvDirection,
                            TimeframeData &data, BollingerBand &band)
{
   if(data.close <= 0 || band.TOP_BB <= 0 || band.LOW_BB <= 0) return false;
   if(data.close < band.LOW_BB || data.close > band.TOP_BB) return false;

   ENUM_DIRECTION priorMoveDirection = GetMHVParentExtremeDirection(mhvDirection);
   if(priorMoveDirection == DIR_NONE) return false;
   if(DetectCSM(pair, data.timeframe, priorMoveDirection, data.barIndex)) return false;
   return true;
}

double GetMHVBodyEdge(TimeframeData &data, ENUM_DIRECTION mhvDirection)
{
   if(data.open <= 0 || data.close <= 0) return 0.0;
   if(mhvDirection == DIR_BUY)  return MathMin(data.open, data.close); // bottom body
   if(mhvDirection == DIR_SELL) return MathMax(data.open, data.close); // top body
   return 0.0;
}

void UpdateMHVProvisionalBody(MLVData &mlv, TimeframeData &data)
{
   double edge = GetMHVBodyEdge(data, mlv.Direction);
   if(edge <= 0) return;

   if(mlv.ProvisionalBodyAnchor <= 0)
      mlv.ProvisionalBodyAnchor = edge;
   else if(mlv.Direction == DIR_BUY)
      mlv.ProvisionalBodyAnchor = MathMin(mlv.ProvisionalBodyAnchor, edge);
   else if(mlv.Direction == DIR_SELL)
      mlv.ProvisionalBodyAnchor = MathMax(mlv.ProvisionalBodyAnchor, edge);
}

bool IsMHVFormationMoveAway(MLVData &mlv, TimeframeData &data)
{
   if(mlv.PreviousClose <= 0 || data.close <= 0) return false;
   if(mlv.Direction == DIR_BUY)  return (data.close > mlv.PreviousClose);
   if(mlv.Direction == DIR_SELL) return (data.close < mlv.PreviousClose);
   return false;
}

bool IsMHVRetestInteraction(MLVData &mlv, TimeframeData &data)
{
   if(mlv.FrozenMarkedBody <= 0 || data.high <= 0 || data.low <= 0) return false;
   if(mlv.Direction == DIR_BUY)  return (data.low <= mlv.FrozenMarkedBody);
   if(mlv.Direction == DIR_SELL) return (data.high >= mlv.FrozenMarkedBody);
   return false;
}

void InstallMHVSupersessionParent(MLVData &mlv,
                                  ExtremeLifecycleData &parent,
                                  TimeframeData &data)
{
   ENUM_DIRECTION parentDirection = GetMHVParentExtremeDirection(mlv.Direction);
   int rawBar = mlv.SupersessionRawBar;
   datetime rawTime = mlv.SupersessionRawCandleTime;

   ResetExtremeLifecycle(parent, parentDirection, data.timeframe);
   parent.Maturity = EXT_MAT_REVERSAL_CONFIRMED;
   parent.Direction = parentDirection;
   parent.Timeframe = data.timeframe;
   parent.RawBar = rawBar;
   parent.RawCandleTime = rawTime;
   parent.ConfirmationBar = data.barIndex;
   parent.ConfirmationCandleTime = data.candle_time;
   parent.ConfirmationClose = data.close;
   parent.LastUpdateBar = data.barIndex;
   parent.LastUpdateCandleTime = data.candle_time;
   parent.PreviousClose = data.close;
   parent.ProvisionalBodyAnchor = GetExtremeReversalBodyEdge(data, parentDirection);
   parent.RelevantMA5 = GetExtremeRelevantMA5(data, parentDirection);
   parent.IsValid = true;
   parent.Reason = "Reversal-confirmed M15 Extreme installed by F1 cycle supersession";
}

bool TryAdvanceMHVSupersessionCandidate(MLVData &mlv, string pair,
                                        TimeframeData &data, BollingerBand &band,
                                        ExtremeLifecycleData &parent)
{
   ENUM_DIRECTION parentDirection = GetMHVParentExtremeDirection(mlv.Direction);
   if(parentDirection == DIR_NONE) return false;

   if(mlv.SupersessionCandidateActive)
   {
      if(data.candle_time <= mlv.SupersessionRawCandleTime) return false;

      if(IsExtremeLifecycleInvalidation(pair, parentDirection, data, band))
      {
         mlv.SupersessionCandidateActive = false;
         mlv.SupersessionRawBar = 0;
         mlv.SupersessionRawCandleTime = 0;
         return false;
      }

      if(IsExtremeReversalDirection(data, parentDirection))
      {
         InstallMHVSupersessionParent(mlv, parent, data);
         MarkCanonicalMLVSuperseded(
            mlv, data,
            "Old MHV/MLV cycle superseded by opposite reversal-confirmed Extreme");
         return true;
      }
      return false;
   }

   datetime boundary = mlv.ConfirmationCandleTime;
   if(boundary <= 0) boundary = mlv.VoidCandleTime;
   if(boundary <= 0 || data.candle_time <= boundary) return false;

   bool rawDetected = DetectExtreme(pair, parentDirection, data, band);
   if(!rawDetected) return false;

   // Opposite RAW Extreme is only a new-cycle candidate. It cannot erase the
   // old MHV provenance until the later reversal-confirmation candle arrives.
   if(IsExtremeLifecycleInvalidation(pair, parentDirection, data, band))
      return false;

   mlv.SupersessionCandidateActive = true;
   mlv.SupersessionRawBar = data.barIndex;
   mlv.SupersessionRawCandleTime = data.candle_time;
   return false;
}

ENUM_MLV_STATE UpdateCanonicalMLVState(MLVData &mlv, string pair,
                                       ENUM_DIRECTION direction,
                                       TimeframeData &data,
                                       BollingerBand &band,
                                       ExtremeLifecycleData &parent,
                                       bool sameDirectionSignal)
{
   if(!EnableMLVStateEngine) return MLV_NONE;
   if(direction != DIR_BUY && direction != DIR_SELL) return MLV_NONE;
   if(!data.is_valid || !data.is_closed || data.candle_time <= 0) return mlv.State;

   if(mlv.Direction != direction || mlv.Timeframe != data.timeframe)
      ResetMLVState(mlv, direction);

   bool parentMature = IsMHVParentExtremeMature(parent);

   if(mlv.State == MLV_NONE)
   {
      if(!parentMature) return MLV_NONE;
      AttachCanonicalMHVParent(mlv, direction, parent, data);
      return mlv.State;
   }

   // A newly installed reversal-confirmed parent is a new cycle. Preserve the
   // atomic supersession transition for one processing step, then attach it.
   if(parentMature && parent.ConfirmationCandleTime > 0 &&
      parent.ConfirmationCandleTime != mlv.ParentConfirmationCandleTime)
   {
      if(mlv.State == MLV_SUPERSEDED || mlv.State == MLV_VOID)
      {
         AttachCanonicalMHVParent(mlv, direction, parent, data);
         return mlv.State;
      }

      MarkCanonicalMLVSuperseded(
         mlv, data,
         "MHV/MLV provenance superseded by a newer reversal-confirmed parent Extreme");
      return mlv.State;
   }

   if(data.candle_time <= mlv.LastUpdateCandleTime)
      return mlv.State;

   // Before formation, parent validity is mandatory. After formation, the
   // frozen parent identity is historical provenance and is not retroactively
   // erased by later same-cycle progression.
   if(!parentMature && !IsCanonicalMLVMatureState(mlv.State) &&
      mlv.State != MLV_VOID && mlv.State != MLV_SUPERSEDED)
   {
      MarkCanonicalMLVVoid(mlv, data,
                           "Canonical MHV void: parent Extreme lost validity before formation");
      return mlv.State;
   }

   if(mlv.State == MLV_PARENT_READY)
   {
      if(data.candle_time <= mlv.ParentConfirmationCandleTime) return mlv.State;

      if(IsMHVTPWajibCompleted(data, mlv.ParentExtremeDirection))
      {
         mlv.State = MLV_TP_COMPLETE;
         mlv.TPWajibCandleTime = data.candle_time;
         mlv.LastUpdateBar = data.barIndex;
         mlv.LastUpdateCandleTime = data.candle_time;
         mlv.PreviousClose = data.close;
         mlv.Reason = "Normal TP-Wajib structurally completed; awaiting loss of prior momentum";
      }
      else
      {
         mlv.LastUpdateBar = data.barIndex;
         mlv.LastUpdateCandleTime = data.candle_time;
         mlv.PreviousClose = data.close;
      }
      return mlv.State;
   }

   if(mlv.State == MLV_TP_COMPLETE)
   {
      // Continuing Momentum after TP means loss-of-momentum has not started.
      // No fixed candle count or timer is used; wait for an actual inside-BB,
      // non-CSM structural pause to begin the MHV formation phase.
      if(IsMHVLossPhaseEligible(pair, direction, data, band))
      {
         mlv.State = MLV_LOSS_DEVELOPING;
         mlv.StartBar = data.barIndex;
         mlv.StartCandleTime = data.candle_time;
         mlv.ProvisionalBodyAnchor = 0.0;
         UpdateMHVProvisionalBody(mlv, data);
         mlv.InvalidationWindowOpen = true;
         mlv.Reason = "Post-TP structural loss of prior momentum developing";
      }

      mlv.LastUpdateBar = data.barIndex;
      mlv.LastUpdateCandleTime = data.candle_time;
      mlv.PreviousClose = data.close;
      return mlv.State;
   }

   if(mlv.State == MLV_LOSS_DEVELOPING)
   {
      // Invalidation has priority over formation promotion.
      if(IsMHVContinuationInvalidation(pair, direction, data, band))
      {
         MarkCanonicalMLVVoid(
            mlv, data,
            "Canonical MHV void: prior Momentum/outer-BB continuation resumed before formation");
         return mlv.State;
      }

      bool moveAway = IsMHVFormationMoveAway(mlv, data);
      if(moveAway && mlv.ProvisionalBodyAnchor > 0)
      {
         // The move-away trigger candle confirms formation but is excluded from
         // the accumulated most-extreme body reference.
         mlv.FrozenMarkedBody = mlv.ProvisionalBodyAnchor;
         mlv.State = MLV_FORMATION_ESTABLISHED;
         mlv.ConfirmationBar = data.barIndex;
         mlv.ConfirmationCandleTime = data.candle_time;
         mlv.ConfirmationClose = data.close;
         mlv.IsValid = true;
         mlv.InvalidationWindowOpen = true;
         mlv.LastUpdateBar = data.barIndex;
         mlv.LastUpdateCandleTime = data.candle_time;
         mlv.PreviousClose = data.close;
         mlv.Reason = "Canonical MHV/MLV formation established; marked body frozen";
         return mlv.State;
      }

      UpdateMHVProvisionalBody(mlv, data);
      mlv.LastUpdateBar = data.barIndex;
      mlv.LastUpdateCandleTime = data.candle_time;
      mlv.PreviousClose = data.close;
      return mlv.State;
   }

   if(mlv.State == MLV_FORMATION_ESTABLISHED ||
      mlv.State == MLV_RETEST_COMPLETE)
   {
      if(mlv.InvalidationWindowOpen &&
         IsMHVContinuationInvalidation(pair, direction, data, band))
      {
         MarkCanonicalMLVVoid(
            mlv, data,
            "Canonical MHV void: outer-BB/Momentum invalidation before direction takeover");
         return mlv.State;
      }

      if(TryAdvanceMHVSupersessionCandidate(mlv, pair, data, band, parent))
         return mlv.State;

      if(mlv.State == MLV_FORMATION_ESTABLISHED &&
         data.candle_time > mlv.ConfirmationCandleTime &&
         IsMHVRetestInteraction(mlv, data))
      {
         mlv.State = MLV_RETEST_COMPLETE;
         mlv.RetestBar = data.barIndex;
         mlv.RetestCandleTime = data.candle_time;
         mlv.Reason = "Canonical MHV/MLV retest complete at frozen marked body";
      }

      // eCSD/CSD is the normal next stage, not MHV invalidation. It may take
      // ownership only on a later closed candle after formation exists.
      if(sameDirectionSignal && data.candle_time > mlv.ConfirmationCandleTime)
      {
         mlv.State = MLV_DIRECTION_TAKEN;
         mlv.DirectionTakeoverBar = data.barIndex;
         mlv.DirectionTakeoverCandleTime = data.candle_time;
         mlv.InvalidationWindowOpen = false;
         mlv.IsValid = true;
         mlv.Reason = "Same-cycle eCSD/CSD direction takeover; MHV provenance retained";
      }

      mlv.LastUpdateBar = data.barIndex;
      mlv.LastUpdateCandleTime = data.candle_time;
      mlv.PreviousClose = data.close;
      return mlv.State;
   }

   if(mlv.State == MLV_DIRECTION_TAKEN)
   {
      // Later same-cycle RE/CSM/Momentum must not retroactively void MHV.
      mlv.InvalidationWindowOpen = false;
      mlv.IsValid = true;

      if(TryAdvanceMHVSupersessionCandidate(mlv, pair, data, band, parent))
         return mlv.State;

      mlv.LastUpdateBar = data.barIndex;
      mlv.LastUpdateCandleTime = data.candle_time;
      mlv.PreviousClose = data.close;
      return mlv.State;
   }

   if(mlv.State == MLV_VOID)
   {
      // VOID remains non-authoritative. A later RAW opposite-cycle Extreme is
      // only a candidate; a reversal-confirmed Extreme installs the new parent.
      TryAdvanceMHVSupersessionCandidate(mlv, pair, data, band, parent);
      mlv.LastUpdateBar = data.barIndex;
      mlv.LastUpdateCandleTime = data.candle_time;
      mlv.PreviousClose = data.close;
      return mlv.State;
   }

   if(mlv.State == MLV_SUPERSEDED)
   {
      mlv.IsValid = false;
      mlv.InvalidationWindowOpen = false;
      mlv.LastUpdateBar = data.barIndex;
      mlv.LastUpdateCandleTime = data.candle_time;
      mlv.PreviousClose = data.close;
   }

   return mlv.State;
}

bool ExportCanonicalMHVSignal(MLVData &mlv, Signal &signal)
{
   ZeroMemory(signal);
   if(!IsCanonicalMLVMatureState(mlv.State) || !mlv.IsValid) return false;
   if(mlv.Direction != DIR_BUY && mlv.Direction != DIR_SELL) return false;
   if(mlv.Timeframe != PERIOD_M15 || mlv.ConfirmationCandleTime <= 0) return false;
   if(mlv.FrozenMarkedBody <= 0) return false;

   signal.Type = SIGNAL_MHV;
   signal.Direction = mlv.Direction;
   signal.Valid = true;
   signal.Timeframe = mlv.Timeframe;
   signal.BarIndex = mlv.ConfirmationBar;
   signal.Timestamp = mlv.ConfirmationCandleTime;
   signal.CandleTime = mlv.ConfirmationCandleTime;
   signal.Close = mlv.ConfirmationClose;
   signal.Reason = mlv.Reason;
   return true;
}

'''
replace_between(module09_start, module10_start, new_m09, 'M09 canonical lifecycle replacement')

# ---------------------------------------------------------------------------
# M13 — REM consumes the canonical formation-established M15 MHV/MLV owner.
# ---------------------------------------------------------------------------
comb_start = '''bool IsCombinationMLVReady(MLVData &mlv)\n{\n'''
comb_end = '''void SetCombinationComponent(ComponentIdentity &component, ENUM_SIGNAL_TYPE type,\n'''
comb_new = '''bool IsCombinationMLVReady(MLVData &mlv)\n{\n   return (IsCanonicalMLVMatureState(mlv.State) &&\n           mlv.IsValid &&\n           mlv.Direction != DIR_NONE &&\n           mlv.Timeframe == PERIOD_M15 &&\n           mlv.FrozenMarkedBody > 0 &&\n           mlv.ConfirmationCandleTime > 0);\n}\n\n'''
replace_between(comb_start, comb_end, comb_new, 'M13 canonical MLV readiness')

# ---------------------------------------------------------------------------
# M16 — exact owner identity, no MHV strategy TTL.
# ---------------------------------------------------------------------------
m16_start = '''bool IsPersistentMLVComponentValid(PairState &pairState,\n                                   ComponentIdentity &component,\n                                   bool &expired)\n{\n'''
m16_end = '''bool IsPersistentReEntryComponentValid(PairState &pairState,\n'''
m16_new = '''bool IsPersistentMLVComponentValid(PairState &pairState,\n                                   ComponentIdentity &component,\n                                   bool &expired)\n{\n   expired = false;\n   if(component.Timeframe != PERIOD_M15) return false;\n\n   MLVData mlv;\n   ZeroMemory(mlv);\n   if(component.Direction == DIR_BUY) mlv = pairState.mlv_buy_state;\n   else if(component.Direction == DIR_SELL) mlv = pairState.mlv_sell_state;\n   else return false;\n\n   // F1 lifecycle has no generic candle/session/day expiry. Exact formation\n   // identity stays valid until structural VOID or atomic cycle supersession.\n   return (IsCanonicalMLVMatureState(mlv.State) &&\n           mlv.IsValid &&\n           mlv.Timeframe == PERIOD_M15 &&\n           mlv.FrozenMarkedBody > 0 &&\n           mlv.Direction == component.Direction &&\n           mlv.ConfirmationCandleTime == component.CandleTime);\n}\n\n'''
replace_between(m16_start, m16_end, m16_new, 'M16 canonical MLV owner validation')

# ---------------------------------------------------------------------------
# M27 — materialize M15 F2 parent provenance before the direction loop, remove
# legacy one-candle MHV and route both MHV/MLV aliases through M09 owner state.
# ---------------------------------------------------------------------------
loop_marker = '''   ValidatedSequenceCandidate allCandidates[];\n   int allCandidateCount = 0;\n\n   for(int dirIdx = 0; dirIdx < 2; dirIdx++)\n'''
loop_insert = '''   ValidatedSequenceCandidate allCandidates[];\n   int allCandidateCount = 0;\n\n   // F1 parent provenance: M15 Extreme maturity uses the already-resolved F2\n   // lifecycle. RAW Extreme alone cannot parent canonical MHV/MLV.\n   bool m15RawBuyExtreme = DetectExtreme(actual, DIR_BUY,\n                                          g_pair_states[pairIndex].m15_data, m15Band);\n   bool m15RawSellExtreme = DetectExtreme(actual, DIR_SELL,\n                                           g_pair_states[pairIndex].m15_data, m15Band);\n   UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_m15_buy_lifecycle,\n                          actual, DIR_BUY, g_pair_states[pairIndex].m15_data,\n                          m15Band, m15RawBuyExtreme);\n   UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_m15_sell_lifecycle,\n                          actual, DIR_SELL, g_pair_states[pairIndex].m15_data,\n                          m15Band, m15RawSellExtreme);\n\n   for(int dirIdx = 0; dirIdx < 2; dirIdx++)\n'''
replace_once(loop_marker, loop_insert, 'M27 M15 Extreme parent preprocessing')

legacy_mhv = '''      if(DetectMHV(actual, direction, g_pair_states[pairIndex].m15_data))\n      {\n         m15MHVSnapshot.Type = SIGNAL_MHV;\n         m15MHVSnapshot.Direction = direction;\n         m15MHVSnapshot.Valid = true;\n         m15MHVSnapshot.Timeframe = PERIOD_M15;\n         m15MHVSnapshot.BarIndex = g_pair_states[pairIndex].m15_data.barIndex;\n         m15MHVSnapshot.CandleTime = g_pair_states[pairIndex].m15_data.candle_time;\n         m15MHVSnapshot.Timestamp = m15MHVSnapshot.CandleTime;\n         m15MHVSnapshot.Close = g_pair_states[pairIndex].m15_data.close;\n      }\n\n'''
replace_once(legacy_mhv, '', 'remove legacy DetectMHV call')

buy_old = '''         DetectMLV_State(g_pair_states[pairIndex].mlv_buy_state, actual, direction,\n                         g_pair_states[pairIndex].m15_data);\n         mlvSnapshot = g_pair_states[pairIndex].mlv_buy_state;\n'''
buy_new = '''         UpdateCanonicalMLVState(\n            g_pair_states[pairIndex].mlv_buy_state, actual, DIR_BUY,\n            g_pair_states[pairIndex].m15_data, m15Band,\n            g_pair_states[pairIndex].extreme_m15_sell_lifecycle,\n            (m15CSDSnapshot.Valid || m15ECSDSnapshot.Valid));\n         mlvSnapshot = g_pair_states[pairIndex].mlv_buy_state;\n         ExportCanonicalMHVSignal(g_pair_states[pairIndex].mlv_buy_state,\n                                  m15MHVSnapshot);\n'''
replace_once(buy_old, buy_new, 'M27 BUY canonical MHV owner route')

sell_old = '''         DetectMLV_State(g_pair_states[pairIndex].mlv_sell_state, actual, direction,\n                         g_pair_states[pairIndex].m15_data);\n         mlvSnapshot = g_pair_states[pairIndex].mlv_sell_state;\n'''
sell_new = '''         UpdateCanonicalMLVState(\n            g_pair_states[pairIndex].mlv_sell_state, actual, DIR_SELL,\n            g_pair_states[pairIndex].m15_data, m15Band,\n            g_pair_states[pairIndex].extreme_m15_buy_lifecycle,\n            (m15CSDSnapshot.Valid || m15ECSDSnapshot.Valid));\n         mlvSnapshot = g_pair_states[pairIndex].mlv_sell_state;\n         ExportCanonicalMHVSignal(g_pair_states[pairIndex].mlv_sell_state,\n                                  m15MHVSnapshot);\n'''
replace_once(sell_old, sell_new, 'M27 SELL canonical MHV owner route')

# Parameter remains for backward .set compatibility only; it is not strategy TTL.
s = s.replace(
    'input int      MaxWaitBars_MLV                    = 5;          // MaxWaitBars_MLV',
    'input int      MaxWaitBars_MLV                    = 5;          // Legacy compatibility only; canonical MHV/MLV has no strategy TTL'
)

# ---------------------------------------------------------------------------
# Static invariants before writing.
# ---------------------------------------------------------------------------
for forbidden in [
    'DetectMHV(',
    'DetectMLV_State(',
    'MLV_CANDIDATE',
    'MLV_CONFIRMED',
    'MLV_EXPIRED',
    '.Neckline',
    'DoubleTop',
    'DoubleBottom',
]:
    if forbidden in s:
        raise SystemExit(f'legacy/unsupported MHV semantic remains: {forbidden}')

if s.count('ENUM_MLV_STATE UpdateCanonicalMLVState(') != 1:
    raise SystemExit('canonical MHV lifecycle definition count drift')
if s.count('UpdateCanonicalMLVState(\n            g_pair_states') != 2:
    raise SystemExit('canonical MHV lifecycle must have BUY/SELL M15 call sites')
if s.count('bool ExportCanonicalMHVSignal(') != 1:
    raise SystemExit('canonical MHV exporter definition count drift')
if s.count('ExportCanonicalMHVSignal(g_pair_states') != 2:
    raise SystemExit('canonical MHV exporter must have BUY/SELL call sites')
if s.count('extreme_m15_buy_lifecycle') < 3 or s.count('extreme_m15_sell_lifecycle') < 3:
    raise SystemExit('M15 F2 parent lifecycle wiring incomplete')
if 'mlv.ExpiryCandleTime' in s:
    raise SystemExit('canonical MHV owner still has generic expiry logic')

required = [
    'MLV_PARENT_READY',
    'MLV_TP_COMPLETE',
    'MLV_LOSS_DEVELOPING',
    'MLV_FORMATION_ESTABLISHED',
    'MLV_RETEST_COMPLETE',
    'MLV_DIRECTION_TAKEN',
    'MLV_SUPERSEDED',
    'data.low <= ma5Low || data.low <= ma10Low',
    'data.high >= ma5High || data.high >= ma10High',
    'return MathMin(data.open, data.close); // bottom body',
    'return MathMax(data.open, data.close); // top body',
    'return (data.close > mlv.PreviousClose);',
    'return (data.close < mlv.PreviousClose);',
    'return (data.low <= mlv.FrozenMarkedBody);',
    'return (data.high >= mlv.FrozenMarkedBody);',
    'sameDirectionSignal && data.candle_time > mlv.ConfirmationCandleTime',
    'Old MHV/MLV cycle superseded by opposite reversal-confirmed Extreme',
]
for token in required:
    if token not in s:
        raise SystemExit(f'missing resolved F1 invariant: {token}')

# M13 exact REM signature must remain unchanged.
for token in [
    'IsCombinationSignalReady(h4_reEntry, SIGNAL_RE_ENTRY, PERIOD_H4)',
    'IsCombinationSignalReady(h1_extreme, SIGNAL_EXTREME, PERIOD_H1)',
    'SetCombinationComponent(rem.Comp3, SIGNAL_MLV, m15_mlv.Direction,',
]:
    if token not in s:
        raise SystemExit(f'REM signature drift: {token}')

# Basic lexical structure audit before native MetaEditor compile.
def strip_noncode(text: str) -> str:
    out = []
    i = 0
    n = len(text)
    state = 'code'
    while i < n:
        c = text[i]
        nxt = text[i + 1] if i + 1 < n else ''
        if state == 'code':
            if c == '"':
                state = 'string'; out.append(' ')
            elif c == '/' and nxt == '/':
                state = 'line'; out.extend('  '); i += 1
            elif c == '/' and nxt == '*':
                state = 'block'; out.extend('  '); i += 1
            else:
                out.append(c)
        elif state == 'string':
            if c == '\\' and nxt:
                out.extend('  '); i += 1
            elif c == '"':
                state = 'code'; out.append(' ')
            else:
                out.append('\n' if c == '\n' else ' ')
        elif state == 'line':
            if c == '\n':
                state = 'code'; out.append('\n')
            else:
                out.append(' ')
        elif state == 'block':
            if c == '*' and nxt == '/':
                state = 'code'; out.extend('  '); i += 1
            else:
                out.append('\n' if c == '\n' else ' ')
        i += 1
    if state in ('string', 'block'):
        raise SystemExit(f'unterminated lexical state: {state}')
    return ''.join(out)

code = strip_noncode(s)
for op, cl, name in [('{', '}', 'brace'), ('(', ')', 'paren'), ('[', ']', 'bracket')]:
    depth = 0
    for ch in code:
        if ch == op:
            depth += 1
        elif ch == cl:
            depth -= 1
            if depth < 0:
                raise SystemExit(f'unbalanced {name}: premature close')
    if depth != 0:
        raise SystemExit(f'unbalanced {name}: final depth {depth}')

SOURCE.write_text(s, encoding='utf-8')

AUDIT.write_text('''# CORE-V2-F1 — Canonical MHV/MLV Lifecycle Implementation Audit\n\nDate: 2026-08-22\nStatus: **IMPLEMENTED / STATIC REGRESSION PASS — NATIVE METAEDITOR COMPILE + RUNTIME TRACE STILL REQUIRED**\nBranch: `blueprint-dev`\n\n## Scope\nImplements the resolved `CORE_V2_F1_MHV_MLV_LIFECYCLE_DECISION.md` contract in M09 and executable REM ownership paths. F2 remains the Extreme maturity authority used for same-timeframe M15 parent provenance. F3 Type-1 and F4 H4 parent-owner semantics are not changed by this patch.\n\n## Removed legacy divergence\n- Removed the independent one-candle `DetectMHV()` path.\n- Removed synthetic fixed-pip double-top/double-bottom candidate logic, generated neckline confirmation and `MaxWaitBars_MLV` strategy expiry.\n- MHV and MLV now resolve from one canonical `MLVData` owner lifecycle; `SIGNAL_MHV` is only an alias export of that owner, while REM consumes the same canonical owner identity as `SIGNAL_MLV`.\n\n## Implemented lifecycle\n`REVERSAL-CONFIRMED SAME-TF EXTREME -> NORMAL TP-WAJIB COMPLETE -> POST-TP LOSS OF PRIOR MOMENTUM -> MOST-EXTREME BODY -> FIRST CLOSED MOVE AWAY -> FORMATION ESTABLISHED + BODY FROZEN -> OPTIONAL LATER BODY RETEST -> SAME-CYCLE eCSD/CSD DIRECTION TAKEOVER -> HISTORICAL PROVENANCE UNTIL OPPOSITE REVERSAL-CONFIRMED EXTREME SUPERSESSION`.\n\n### Parent and TP provenance\n- M15 BUY MHV uses a prior reversal-confirmed M15 SELL Extreme; M15 SELL MHV mirrors from a prior reversal-confirmed M15 BUY Extreme.\n- RAW Extreme cannot parent MHV.\n- TP-Wajib is structural market evidence, not broker-order state: prior SELL Extreme reaches current opposite MA5/MA10 Low area; prior BUY Extreme reaches current opposite MA5/MA10 High area.\n- The TP-completion candle only records TP completion; the later loss-of-momentum structure must develop separately.\n\n### Loss / formation / marked body\n- Loss-of-momentum starts only inside the relevant outer BB without source-valid continuation CSM.\n- One ordinary candle does not itself establish MHV: a provisional body is first accumulated, then a later closed move-away establishes formation.\n- BUY/bottom MHV tracks lowest `min(Open,Close)` and establishes on first later `Close > PreviousClose`.\n- SELL/top MHV tracks highest `max(Open,Close)` and establishes on first later `Close < PreviousClose`.\n- Move-away trigger candle is excluded from body accumulation and the marked body freezes immediately at formation.\n\n### Retest / direction progression\n- Later BUY MHV retest completes on `Low <= FrozenMarkedBody`; SELL on `High >= FrozenMarkedBody`.\n- Retest is not required merely for REM component maturity.\n- Same-cycle eCSD/CSD on a later closed candle advances ownership to `MLV_DIRECTION_TAKEN`; it does not void completed MHV provenance.\n- Once direction takes ownership, the MHV outer-BB/Momentum invalidation window is closed.\n\n### Invalidation and supersession\n- While loss/formation/retest is the active stage, relevant outer-BB continuation / prior-direction CSM has priority and resolves the setup to `MLV_VOID`.\n- No generic candle/session/day TTL exists for canonical MHV validity.\n- A later opposite-cycle RAW Extreme is candidate-only. It cannot erase the old MHV.\n- Only the subsequent reversal-confirmation candle atomically installs the new M15 Extreme parent and resolves old MHV provenance to `MLV_SUPERSEDED`.\n- Superseded/void MHV cannot satisfy new REM ownership.\n\n## REM maturity contract\n`IsCombinationMLVReady()` and M16 owner validation accept only canonical formation-established-or-later states with a frozen marked body and exact formation-candle identity. The exact REM signature remains `H4 Re-Entry + H1 Extreme + M15 MHV/MLV`.\n\n## Static regression invariants\n- no `DetectMHV()` or legacy `DetectMLV_State()` remains;\n- no synthetic MHV neckline/double-top/double-bottom rule remains;\n- no `MLV_CANDIDATE`, `MLV_CONFIRMED`, `MLV_EXPIRED` legacy state remains;\n- no MHV `ExpiryCandleTime` strategy TTL remains;\n- M15 F2 Extreme lifecycle owners exist for both directions;\n- canonical BUY/SELL MHV lifecycle call sites and alias exports are unique;\n- exact REM signature remains unchanged;\n- full-source brace/parenthesis/bracket lexical sanity passes.\n\n## Remaining verification\n1. Native MetaEditor compile must report **0 errors / 0 warnings**.\n2. Runtime traces should cover: parent RAW rejection; parent reversal confirmation; TP-Wajib completion; continued Momentum delaying loss state; loss-state invalidation; multi-candle body accumulation; move-away/freeze; formation export into REM; later retest; eCSD/CSD takeover; RAW supersession candidate without handover; reversal-confirmed atomic supersession; stale REM rejection after supersession.\n3. F3/F4 implementation must preserve this canonical MHV owner and F2 provenance.\n\nDecision provenance: `blueprint/decisions/CORE_V2_F1_MHV_MLV_LIFECYCLE_DECISION.md`.\n''', encoding='utf-8')

# Reconcile queue statuses after successful source/static patch.
q = QUEUE.read_text(encoding='utf-8')
q = q.replace(
    'Status: **SPECIFICATION RESOLVED — BEST-RECOMMENDATION REVIEW COMPLETE; CODE PATCH/AUDIT STILL PENDING**',
    'Status: **CODE IMPLEMENTED / STATIC REGRESSION PASS — NATIVE METAEDITOR COMPILE + RUNTIME TRACE PENDING**',
    1
)
q = q.replace(
    'Status: **SPECIFICATION RESOLVED — USER APPROVED; CODE PATCH/AUDIT STILL PENDING**',
    'Status: **CODE IMPLEMENTED / STATIC REGRESSION PASS — NATIVE METAEDITOR COMPILE + RUNTIME TRACE PENDING**',
    1
)
q = q.replace(
    'Next action for F1: migrate/remove duplicate MHV detector semantics, implement/audit one canonical M09 lifecycle, verify REM stale-provenance rejection, then compile/regression/runtime-test. No EA code was changed during specification review.',
    'Next action for F1: native MetaEditor compile and runtime lifecycle traces; static implementation/regression is complete.'
)
q = q.replace(
    'Next action for F2: patch/audit the Extreme lifecycle and REM/REE component maturity against the resolved contract; no code was changed during specification review.',
    'Next action for F2: native MetaEditor compile and runtime lifecycle traces; static implementation/regression is complete.'
)
QUEUE.write_text(q, encoding='utf-8')

c = CURRENT.read_text(encoding='utf-8')
c = c.replace(
    'Strategy Core V2 specification:** CORE-V2-F1 MHV/MLV, F2 Extreme maturity, F3 Re-Entry Type 1 and F4 standalone H1/H4 parent-owner contracts are resolved at specification level; their code patch/audit work remains pending.',
    'Strategy Core V2:** F1 MHV/MLV and F2 Extreme maturity are implemented with static regression PASS; F3 Re-Entry Type 1 and F4 standalone H1/H4 parent-owner remain specification-resolved with code patch/audit pending. Native MetaEditor compile/runtime traces remain pending for the new F1/F2 code.'
)
c = c.replace(
    '**Implement/audit the resolved CORE-V2-F1/F2/F3/F4 contracts in dependency-safe order.**',
    '**Implement/audit CORE-V2-F3 Re-Entry Type 1 next, then CORE-V2-F4 H4 parent-owner; preserve the implemented F1/F2 lifecycle contracts.**'
)
CURRENT.write_text(c, encoding='utf-8')

print('CORE-V2-F1 canonical MHV/MLV implementation + static regression: PASS')
