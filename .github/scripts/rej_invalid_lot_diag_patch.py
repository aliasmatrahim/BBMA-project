from pathlib import Path
import hashlib

SRC = Path('blueprint/source/BBMA_EA.mq4')
CONTRACT = Path('blueprint/contracts/M21_MONEY_MANAGEMENT_CONTRACT.md')

src = SRC.read_text(encoding='utf-8')
if 'Version 4.5.1 - D1O-07 Canonical LTF Dedup' not in src:
    raise RuntimeError('unexpected EA baseline')
if 'P2-LOTDIAG-01' in src:
    print('REJ_INVALID_LOT_DIAG_ALREADY_APPLIED=PASS')
    raise SystemExit(0)

calc_start = src.find('double CalculateLotSize(BBMA_Decision &decision, RiskValidationSnapshot &snapshot, bool &valid)')
module22 = src.find('//+------------------------------------------------------------------+\n//| MODULE 22: ORDER EXECUTION ENGINE', calc_start)
if calc_start < 0 or module22 < 0:
    raise RuntimeError('CalculateLotSize block anchors missing')
calc_before = src[calc_start:module22]
calc_hash_before = hashlib.sha256(calc_before.encode('utf-8')).hexdigest()

helper = r'''// P2-LOTDIAG-01: observability-only explanation for an already-failed M21 lot result.
// IMPORTANT: CalculateLotSize() remains the sole sizing authority and is unchanged.
// This helper never queries live broker/account state, changes lot, clamps values,
// or changes rejection semantics. It only reads the same frozen decision/snapshot.
string DiagnoseInvalidLotReason(BBMA_Decision &decision,
                                RiskValidationSnapshot &snapshot,
                                double &rawLot,
                                double &normalizedLot,
                                double &effectiveMaxLot)
{
   rawLot = 0.0;
   normalizedLot = 0.0;
   effectiveMaxLot = 0.0;

   if(decision.DecisionState != DEC_VALIDATED || decision.Pair == "" ||
      decision.EntryPrice <= 0 || decision.StopLoss <= 0)
      return "INVALID_DECISION";

   if(snapshot.Point <= 0 || snapshot.TickSize_Price <= 0 || snapshot.TickValue <= 0 ||
      snapshot.LotStep <= 0 || snapshot.MinLot <= 0 ||
      snapshot.MaxLot < snapshot.MinLot || snapshot.LotDigits < 0 || snapshot.Equity <= 0)
      return "BROKER_SNAPSHOT_INVALID";

   double payloadTolerance = snapshot.Point * 0.5;
   if(MathAbs(snapshot.EntryPrice - decision.EntryPrice) > payloadTolerance ||
      MathAbs(snapshot.StopLoss - decision.StopLoss) > payloadTolerance)
      return "PAYLOAD_MISMATCH";

   if(MMMode == 1)
   {
      if(AutoLotPercent <= 0 || MaxAutoLot <= 0)
         return "MM_CONFIG_INVALID";

      double slDistance = MathAbs(decision.EntryPrice - decision.StopLoss);
      if(slDistance <= 0)
         return "SL_DISTANCE_INVALID";

      double riskPerLot = slDistance * snapshot.TickValue / snapshot.TickSize_Price;
      if(riskPerLot <= 0)
         return "RISK_PER_LOT_INVALID";

      double riskAmount = snapshot.Equity * (AutoLotPercent / 100.0);
      if(riskAmount <= 0)
         return "RISK_AMOUNT_INVALID";

      rawLot = riskAmount / riskPerLot;
      normalizedLot = NormalizeLotDownFromSnapshot(rawLot, snapshot);
      effectiveMaxLot = MathMin(snapshot.MaxLot, MaxAutoLot);

      if(normalizedLot < snapshot.MinLot)
         return "BELOW_MIN";
      if(effectiveMaxLot < snapshot.MinLot)
         return "MAXAUTOLOT_BELOW_MIN";
      if(normalizedLot > effectiveMaxLot)
         return "ABOVE_MAX";
      if(!IsValidSnapshotLotStep(normalizedLot, snapshot))
         return "STEP_MISMATCH";

      return "AUTOLOT_FAILURE_UNCLASSIFIED";
   }

   if(MMMode == 2)
   {
      rawLot = FixedLot;
      normalizedLot = FixedLot;
      effectiveMaxLot = snapshot.MaxLot;

      if(FixedLot <= 0 || FixedLot < snapshot.MinLot || FixedLot > snapshot.MaxLot)
         return "FIXEDLOT_INVALID";
      if(!IsValidSnapshotLotStep(FixedLot, snapshot))
         return "STEP_MISMATCH";

      return "FIXEDLOT_FAILURE_UNCLASSIFIED";
   }

   return "MMMODE_INVALID";
}

void PrintInvalidLotDiagnostic(BBMA_Decision &decision,
                               RiskValidationSnapshot &snapshot,
                               string reasonTag,
                               double rawLot,
                               double normalizedLot,
                               double effectiveMaxLot)
{
   double slDistance = MathAbs(decision.EntryPrice - decision.StopLoss);

   Print("[LOT_DIAG][REJ_INVALID_LOT] Pair=", decision.Pair,
         " Reason=", reasonTag,
         " MMMode=", IntegerToString(MMMode),
         " RawLot=", DoubleToString(rawLot, 8),
         " NormalizedLot=", DoubleToString(normalizedLot, 8),
         " MinLot=", DoubleToString(snapshot.MinLot, 8),
         " MaxLot=", DoubleToString(snapshot.MaxLot, 8),
         " EffectiveMaxLot=", DoubleToString(effectiveMaxLot, 8),
         " LotStep=", DoubleToString(snapshot.LotStep, 8),
         " LotDigits=", IntegerToString(snapshot.LotDigits),
         " TickValue=", DoubleToString(snapshot.TickValue, 8),
         " TickSize=", DoubleToString(snapshot.TickSize_Price, 8),
         " Point=", DoubleToString(snapshot.Point, 10),
         " SLDistance=", DoubleToString(slDistance, 10),
         " Entry=", DoubleToString(decision.EntryPrice, snapshot.Digits),
         " SL=", DoubleToString(decision.StopLoss, snapshot.Digits),
         " Equity=", DoubleToString(snapshot.Equity, 2),
         " AutoPct=", DoubleToString(AutoLotPercent, 4),
         " MaxAutoLot=", DoubleToString(MaxAutoLot, 8),
         " FixedLot=", DoubleToString(FixedLot, 8));
}

'''

src = src[:calc_start] + helper + src[calc_start:]

old_caller = '''   bool lotValid = true;\n   double lot = CalculateLotSize(decision, snapshot, lotValid);\n   if(!lotValid || lot <= 0)\n   {\n      decision.DecisionState = DEC_REJECTED;\n      decision.RejectionReason = REJ_INVALID_LOT;\n      return false;\n   }'''
new_caller = '''   bool lotValid = true;\n   double lot = CalculateLotSize(decision, snapshot, lotValid);\n   if(!lotValid || lot <= 0)\n   {\n      double rawLotDiagnostic = 0.0;\n      double normalizedLotDiagnostic = 0.0;\n      double effectiveMaxLotDiagnostic = 0.0;\n      string lotReasonTag = DiagnoseInvalidLotReason(\n         decision, snapshot, rawLotDiagnostic, normalizedLotDiagnostic,\n         effectiveMaxLotDiagnostic);\n      PrintInvalidLotDiagnostic(decision, snapshot, lotReasonTag,\n                                rawLotDiagnostic, normalizedLotDiagnostic,\n                                effectiveMaxLotDiagnostic);\n\n      decision.DecisionState = DEC_REJECTED;\n      decision.RejectionReason = REJ_INVALID_LOT;\n      return false;\n   }'''
if old_caller not in src:
    raise RuntimeError('preflight invalid-lot caller anchor missing')
src = src.replace(old_caller, new_caller, 1)

# Hard semantic guard: the sizing-authority function body must remain byte-for-byte unchanged.
new_calc_start = src.find('double CalculateLotSize(BBMA_Decision &decision, RiskValidationSnapshot &snapshot, bool &valid)')
new_module22 = src.find('//+------------------------------------------------------------------+\n//| MODULE 22: ORDER EXECUTION ENGINE', new_calc_start)
calc_after = src[new_calc_start:new_module22]
if calc_after != calc_before:
    raise RuntimeError('CalculateLotSize changed; observability-only contract violated')
calc_hash_after = hashlib.sha256(calc_after.encode('utf-8')).hexdigest()
if calc_hash_after != calc_hash_before:
    raise RuntimeError('CalculateLotSize hash drift')

for needle in [
    '"BROKER_SNAPSHOT_INVALID"', '"BELOW_MIN"', '"ABOVE_MAX"',
    '"STEP_MISMATCH"', '"MAXAUTOLOT_BELOW_MIN"', '"FIXEDLOT_INVALID"',
    '[LOT_DIAG][REJ_INVALID_LOT]',
    'decision.RejectionReason = REJ_INVALID_LOT;'
]:
    if needle not in src:
        raise RuntimeError('missing diagnostic guard: ' + needle)

SRC.write_text(src, encoding='utf-8', newline='\n')

contract = CONTRACT.read_text(encoding='utf-8')
marker = '## Diagnostics boundary — P2-LOTDIAG-01'
if marker not in contract:
    anchor = '## Failure behavior\n'
    if anchor not in contract:
        raise RuntimeError('M21 contract failure-behavior anchor missing')
    block = '''## Diagnostics boundary — P2-LOTDIAG-01\n\n`REJ_INVALID_LOT` remains the downstream rejection enum. Observability may attach a reason tag and frozen-snapshot values **after** M21 has already failed, but diagnostics MUST NOT alter sizing or admission.\n\nApproved diagnostic tags include at minimum:\n- `BROKER_SNAPSHOT_INVALID`;\n- `BELOW_MIN`;\n- `ABOVE_MAX`;\n- `STEP_MISMATCH`;\n- `MAXAUTOLOT_BELOW_MIN`;\n- `FIXEDLOT_INVALID`.\n\nAdditional explanatory tags may distinguish invalid decision payload, payload mismatch, invalid MM configuration, invalid SL distance/risk-per-lot/risk amount, unknown MMMode, or an otherwise-unclassified failure.\n\nDiagnostic capture may include `rawLot`, normalized lot, `MinLot`, `MaxLot`, effective maximum lot, `LotStep`, `LotDigits`, `TickValue`, `TickSize_Price`, point size, SL distance, Entry, SL, frozen Equity, AutoLotPercent, MaxAutoLot, FixedLot and MMMode.\n\nHard guard: diagnostics consume only the already-frozen decision/snapshot and user inputs. They may not re-query live broker/account state, clamp/normalize a rejected trade into acceptance, change `CalculateLotSize()`, or replace `REJ_INVALID_LOT` with a new trading decision.\n\n'''
    contract = contract.replace(anchor, block + anchor, 1)
    CONTRACT.write_text(contract, encoding='utf-8', newline='\n')

print('REJ_INVALID_LOT_DIAG_PATCH=PASS')
print('CALCULATE_LOT_SIZE_SHA256=' + calc_hash_after)
