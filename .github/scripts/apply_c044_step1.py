from pathlib import Path

p = Path('blueprint/source/BBMA_EA.mq4')
s = p.read_text(encoding='utf-8')
original = s


def replace_once(old: str, new: str, label: str) -> None:
    global s
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, found {n}')
    s = s.replace(old, new, 1)


def replace_function(start_marker: str, end_marker: str, replacement: str, label: str) -> None:
    global s
    a = s.find(start_marker)
    if a < 0:
        raise SystemExit(f'{label}: start marker missing')
    b = s.find(end_marker, a)
    if b < 0:
        raise SystemExit(f'{label}: end marker missing')
    if s.find(start_marker, a + 1) >= 0:
        raise SystemExit(f'{label}: start marker not unique')
    s = s[:a] + replacement.rstrip() + '\n\n' + s[b:]


replace_once('Version 4.5.2 - M17 Structural SL Normalization',
             'Version 4.5.3 - C044 Targetless Payload Stage',
             'header version')
replace_once('#property version   "4.52"',
             '#property version   "4.53"',
             'property version')

replace_once('bool           EnableRE_Type4                     = true;\n',
             'bool           EnableRE_Type4                     = true;\n'
             '// C044 staged implementation gate. Keep OFF until M23/M24 lifecycle\n'
             '// close + restart reconstruction are implemented and verified.\n'
             'bool           EnableC044Lifecycle                = false;\n',
             'C044 feature gate')

replace_once('   // MUTABLE LIFECYCLE\n   ENUM_DECISION_STATE  DecisionState;\n',
             '   // MUTABLE LIFECYCLE\n'
             '   bool                 C044LifecycleManaged;\n'
             '   ENUM_DECISION_STATE  DecisionState;\n',
             'decision lifecycle flag')

resolve_fn = r'''bool ResolveApprovedInitialSLTP(BBMA_Decision &decision,
                                RiskValidationSnapshot &snapshot)
{
   if(!IsApprovedSLTPSourceComponent(decision,
                                     decision.SLTPSourceComponent))
      return false;

   double structuralAnchor = 0.0;
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

   // C044 is intentionally fail-safe gated OFF until M23/M24 lifecycle support
   // is complete. While OFF, preserve the v4.52 static destination exactly.
   if(!EnableC044Lifecycle)
   {
      if(!ResolveApprovedBBDestination(decision.Pair,
                                       decision.SLTPSourceComponent,
                                       decision.Direction,
                                       destination))
         return false;

      if(decision.Direction == DIR_BUY && destination <= decision.EntryPrice)
         return false;
      if(decision.Direction == DIR_SELL && destination >= decision.EntryPrice)
         return false;
   }

   if(snapshot.Point <= 0.0 || decision.EntryPrice <= 0.0) return false;

   double safetyBuffer = snapshot.Point;
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

   if(snapshot.TickSize_Price <= 0.0 || snapshot.Digits < 0) return false;

   double slTicks = brokerSL / snapshot.TickSize_Price;
   double normalizedSL = 0.0;
   if(decision.Direction == DIR_BUY)
      normalizedSL = MathFloor(slTicks + 0.000000001) * snapshot.TickSize_Price;
   else if(decision.Direction == DIR_SELL)
      normalizedSL = MathCeil(slTicks - 0.000000001) * snapshot.TickSize_Price;
   else
      return false;

   normalizedSL = NormalizeDouble(normalizedSL, snapshot.Digits);
   if(normalizedSL <= 0.0) return false;

   double normalizedTP = 0.0;
   if(!EnableC044Lifecycle)
   {
      double tpTicks = destination / snapshot.TickSize_Price;
      if(decision.Direction == DIR_BUY)
         normalizedTP = MathFloor(tpTicks + 0.000000001) * snapshot.TickSize_Price;
      else if(decision.Direction == DIR_SELL)
         normalizedTP = MathCeil(tpTicks - 0.000000001) * snapshot.TickSize_Price;
      else
         return false;

      normalizedTP = NormalizeDouble(normalizedTP, snapshot.Digits);
      if(normalizedTP <= 0.0) return false;
   }

   decision.StopLoss = normalizedSL;
   decision.TakeProfit = EnableC044Lifecycle ? 0.0 : normalizedTP;
   decision.SLTPSource = decision.SLTPSourceComponent.ComponentType;
   decision.C044LifecycleManaged = EnableC044Lifecycle;

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
            " TP=", DoubleToString(decision.TakeProfit, snapshot.Digits),
            " C044=", decision.C044LifecycleManaged ? "Y" : "N");
   }
   return true;
}'''
replace_function('bool ResolveApprovedInitialSLTP(BBMA_Decision &decision,',
                 'double GetDirectionalClosePrice(RiskValidationSnapshot &snapshot, ENUM_DIRECTION direction)',
                 resolve_fn,
                 'ResolveApprovedInitialSLTP')

has_fn = r'''bool HasSourceResolvedSLTP(BBMA_Decision &decision)
{
   if(decision.SLTPSource == SIGNAL_NONE) return false;
   if(decision.C044LifecycleManaged)
      return (decision.StopLoss > 0.0 && decision.TakeProfit == 0.0);
   return (decision.StopLoss > 0.0 && decision.TakeProfit > 0.0);
}'''
replace_function('bool HasSourceResolvedSLTP(BBMA_Decision &decision)',
                 'bool ValidateDirectionalSLTPGeometry(BBMA_Decision &decision)',
                 has_fn,
                 'HasSourceResolvedSLTP')

geom_fn = r'''bool ValidateDirectionalSLTPGeometry(BBMA_Decision &decision)
{
   if(decision.C044LifecycleManaged)
   {
      if(decision.TakeProfit != 0.0) return false;
      if(decision.Direction == DIR_BUY)
         return (decision.StopLoss < decision.EntryPrice);
      if(decision.Direction == DIR_SELL)
         return (decision.StopLoss > decision.EntryPrice);
      return false;
   }

   if(decision.Direction == DIR_BUY)
      return (decision.StopLoss < decision.EntryPrice &&
              decision.TakeProfit > decision.EntryPrice);

   if(decision.Direction == DIR_SELL)
      return (decision.StopLoss > decision.EntryPrice &&
              decision.TakeProfit < decision.EntryPrice);

   return false;
}'''
replace_function('bool ValidateDirectionalSLTPGeometry(BBMA_Decision &decision)',
                 'bool ValidateSLTP(BBMA_Decision &decision, RiskValidationSnapshot &snapshot,',
                 geom_fn,
                 'ValidateDirectionalSLTPGeometry')

validate_fn = r'''bool ValidateSLTP(BBMA_Decision &decision, RiskValidationSnapshot &snapshot,
                  ENUM_REJECTION_REASON &rejection)
{
   rejection = REJ_NONE;

   if(decision.EntryPrice <= 0.0 || snapshot.EntryPrice <= 0.0)
   {
      rejection = REJ_MARKET_PRICE_INVALID;
      return false;
   }

   if(!HasSourceResolvedSLTP(decision))
   {
      rejection = REJ_SLTP_UNRESOLVED;
      return false;
   }

   if(decision.StopLoss <= 0.0)
   {
      rejection = REJ_INVALID_SL;
      return false;
   }

   if(decision.C044LifecycleManaged)
   {
      if(decision.TakeProfit != 0.0)
      {
         rejection = REJ_INVALID_TP;
         return false;
      }

      if(!ValidateDirectionalSLTPGeometry(decision))
      {
         rejection = REJ_INVALID_SL;
         return false;
      }

      double slDistance = MathAbs(decision.EntryPrice - decision.StopLoss);
      if(slDistance <= 0.0)
      {
         rejection = REJ_INVALID_SL;
         return false;
      }

      double pipPrice = GetPipValue(decision.Pair);
      if(MaxSLPips > 0.0 && pipPrice > 0.0 && slDistance > MaxSLPips * pipPrice)
      {
         rejection = REJ_INVALID_SL;
         return false;
      }

      // C044 targetless lifecycle has no deterministic reward coordinate.
      // Never manufacture one merely to satisfy an explicitly enabled MinRR.
      if(MinRRRatio > 0.0)
      {
         rejection = REJ_INVALID_RR;
         return false;
      }

      double closePrice = GetDirectionalClosePrice(snapshot, decision.Direction);
      double minDistance = snapshot.StopLevel * snapshot.Point;
      if(closePrice <= 0.0)
      {
         rejection = REJ_MARKET_PRICE_INVALID;
         return false;
      }
      if(minDistance > 0.0 && MathAbs(decision.StopLoss - closePrice) < minDistance)
      {
         rejection = REJ_INVALID_SL;
         return false;
      }

      decision.StopLossPoints = slDistance / snapshot.Point;
      return true;
   }

   if(decision.TakeProfit <= 0.0)
   {
      rejection = REJ_INVALID_TP;
      return false;
   }

   if(!ValidateDirectionalSLTPGeometry(decision))
   {
      rejection = (decision.StopLoss == decision.EntryPrice)
         ? REJ_INVALID_SL : REJ_INVALID_TP;
      return false;
   }

   double slDistance = MathAbs(decision.EntryPrice - decision.StopLoss);
   double tpDistance = MathAbs(decision.TakeProfit - decision.EntryPrice);
   if(slDistance <= 0.0 || tpDistance <= 0.0)
   {
      rejection = (slDistance <= 0.0) ? REJ_INVALID_SL : REJ_INVALID_TP;
      return false;
   }

   double pipPrice = GetPipValue(decision.Pair);
   if(MaxSLPips > 0.0 && pipPrice > 0.0)
   {
      double maxSLPrice = MaxSLPips * pipPrice;
      if(slDistance > maxSLPrice)
      {
         rejection = REJ_INVALID_SL;
         return false;
      }
   }

   if(MinRRRatio > 0.0 && (tpDistance / slDistance) < MinRRRatio)
   {
      rejection = REJ_INVALID_RR;
      return false;
   }

   double closePrice = GetDirectionalClosePrice(snapshot, decision.Direction);
   double minDistance = snapshot.StopLevel * snapshot.Point;
   if(closePrice <= 0.0)
   {
      rejection = REJ_MARKET_PRICE_INVALID;
      return false;
   }

   if(minDistance > 0.0)
   {
      if(MathAbs(decision.StopLoss - closePrice) < minDistance)
      {
         rejection = REJ_INVALID_SL;
         return false;
      }
      if(MathAbs(decision.TakeProfit - closePrice) < minDistance)
      {
         rejection = REJ_INVALID_TP;
         return false;
      }
   }

   decision.StopLossPoints = slDistance / snapshot.Point;
   return true;
}'''
replace_function('bool ValidateSLTP(BBMA_Decision &decision, RiskValidationSnapshot &snapshot,',
                 'bool ValidateStopLevel(double price, string pair, ENUM_DIRECTION direction)',
                 validate_fn,
                 'ValidateSLTP')

replace_once('if(MaxRetry <= 0 || pair == "" || lot <= 0 || stopLoss <= 0 || takeProfit <= 0 ||\n      magicNumber <= 0 || decisionID == "")',
             'if(MaxRetry <= 0 || pair == "" || lot <= 0 || stopLoss <= 0 || takeProfit < 0.0 ||\n      magicNumber <= 0 || decisionID == "")',
             'M22 retry TP zero support')

old_guard = '''   if(pair == "" || decision.Pair != pair || decision.DecisionID == "" ||\n      decision.Direction == DIR_NONE || decision.EntryPrice <= 0 ||\n      decision.StopLoss <= 0 || decision.TakeProfit <= 0)\n   {\n'''
new_guard = '''   bool tpPayloadValid = decision.C044LifecycleManaged\n      ? (decision.TakeProfit == 0.0)\n      : (decision.TakeProfit > 0.0);\n\n   if(pair == "" || decision.Pair != pair || decision.DecisionID == "" ||\n      decision.Direction == DIR_NONE || decision.EntryPrice <= 0 ||\n      decision.StopLoss <= 0 || !tpPayloadValid)\n   {\n'''
replace_once(old_guard, new_guard, 'M22 ProcessEntry payload guard')

required = [
    'bool           EnableC044Lifecycle                = false;',
    'bool                 C044LifecycleManaged;',
    'decision.TakeProfit = EnableC044Lifecycle ? 0.0 : normalizedTP;',
    'takeProfit < 0.0',
    'bool tpPayloadValid = decision.C044LifecycleManaged',
]
for token in required:
    if token not in s:
        raise SystemExit(f'missing required token: {token}')

if s.count('OrderClose(') != original.count('OrderClose('):
    raise SystemExit('Step1 must not add M23/M20 close authority')
if 'EnableC044Lifecycle                = true;' in s:
    raise SystemExit('C044 gate must remain OFF in Step1')

p.write_text(s, encoding='utf-8')

Path('blueprint/C044_STEP1_TARGETLESS_PAYLOAD_IMPLEMENTATION_AUDIT_20260826.md').write_text('''# C044 Step 1 — Targetless Payload Implementation Audit — 2026-08-26

Branch: `d1-owner-dev`

## Status
**IMPLEMENTED / STATIC INTEGRITY PASS / FAIL-SAFE FEATURE GATE OFF / NATIVE COMPILE PENDING**

## Scope
Stage the minimum M17/M22 plumbing required by the approved C044 targetless lifecycle architecture without enabling incomplete lifecycle execution.

## Implemented
- source build identifier advanced to `4.53 - C044 Targetless Payload Stage`;
- added internal locked `EnableC044Lifecycle=false` gate;
- added `BBMA_Decision.C044LifecycleManaged` payload classification;
- M17 can resolve the existing approved structural hard SL while producing `TP=0` only when the C044 gate is enabled;
- current static outer-BB TP path is preserved while the gate is OFF;
- M17 targetless validation accepts SL-only geometry, rejects `MinRRRatio>0`, and does not manufacture reward distance;
- M22 transport/pre-send guards can carry `TP=0` only when the decision is explicitly C044 lifecycle-managed;
- no M23 lifecycle close logic, M24 recovery semantics, entry eligibility, detector ownership, SL formula, lot sizing, risk percentage or emergency-close authority is changed in this step.

## Safety boundary
The C044 feature gate remains OFF because enabling targetless orders before M23/M24 lifecycle close and recovery are implemented would create live positions without the approved normal lifecycle exit. Current runtime behavior therefore remains the pre-C044 static-TP policy until the later atomic activation gate.

## Static checks
- exact pre-step source Git blob verified: `4ccd444a96a34b494653143a7560516a4147b5bc`;
- one C044 gate and one decision payload flag;
- targetless M17 path present;
- MinRR fail-closed rule present;
- M22 TP=0 transport path present;
- no new `OrderClose()` authority added;
- `git diff --check` required before commit.

## Next step
Implement immutable owner/lifecycle evidence + M23 C044 close latching and M24 restart reconstruction, then enable C044 only after cross-module static regression and native MetaEditor 0E0W.
''', encoding='utf-8')
