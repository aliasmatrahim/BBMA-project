#!/usr/bin/env python3
"""Apply NMJE N3 Step-1 M09 single-writer hardening to BBMA_EA.mq4.

Design invariant:
- M08 is the sole writer of ExtremeLifecycleData.
- M09 may consume canonical M08 Extreme state and mutate only MLVData.
- No BBMA strategy rule is added or changed.

This tool is intentionally fail-closed: every expected source block must match
exactly once, otherwise no output file is written.
"""
from pathlib import Path
import sys

TARGET = Path("blueprint/source/BBMA_EA.mq4")

OLD_INSTALL = r'''void InstallMHVSupersessionParent(MLVData &mlv,
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

'''

OLD_TRY = r'''bool TryAdvanceMHVSupersessionCandidate(MLVData &mlv, string pair,
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
         if(EntryMode == 2)
            Print("[P3M2][MLV_SUPERSEDE] MLVDir=", EnumToString(mlv.Direction),
                  " NewExtremeDir=", EnumToString(parentDirection),
                  " Raw=", TimeToString(mlv.SupersessionRawCandleTime),
                  " Confirm=", TimeToString(data.candle_time));
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
   if(EntryMode == 2)
      Print("[P3M2][MLV_SUPER_CAND] MLVDir=", EnumToString(mlv.Direction),
            " ExtremeDir=", EnumToString(parentDirection),
            " Raw=", TimeToString(data.candle_time));
   return false;
}

'''

NEW_TRY = r'''bool TryAdvanceMHVSupersessionFromCanonicalParent(MLVData &mlv,
                                                   TimeframeData &data,
                                                   ExtremeLifecycleData &parent)
{
   // N3 single-writer invariant: M09 NEVER detects, resets, promotes or mutates
   // ExtremeLifecycleData. M08 owns the canonical parent lifecycle completely.
   if(!IsMHVParentExtremeMature(parent)) return false;
   if(parent.ConfirmationCandleTime <= 0) return false;

   datetime boundary = mlv.ParentConfirmationCandleTime;
   if(boundary <= 0) boundary = mlv.ConfirmationCandleTime;
   if(boundary <= 0) boundary = mlv.VoidCandleTime;
   if(boundary <= 0 || parent.ConfirmationCandleTime <= boundary) return false;

   MarkCanonicalMLVSuperseded(
      mlv, data,
      "Old MHV/MLV cycle superseded by newer canonical M08 reversal-confirmed parent Extreme");
   if(EntryMode == 2)
      Print("[P3M2][MLV_SUPERSEDE] MLVDir=", EnumToString(mlv.Direction),
            " NewExtremeDir=", EnumToString(parent.Direction),
            " NewConfirm=", TimeToString(parent.ConfirmationCandleTime),
            " ProcessCandle=", TimeToString(data.candle_time));
   return true;
}

'''

REPLACEMENTS = [
    (OLD_INSTALL, ""),
    (OLD_TRY, NEW_TRY),
    ("TryAdvanceMHVSupersessionCandidate(mlv, pair, data, band, parent)",
     "TryAdvanceMHVSupersessionFromCanonicalParent(mlv, data, parent)"),
]

FORBIDDEN_AFTER = [
    "InstallMHVSupersessionParent(",
    "TryAdvanceMHVSupersessionCandidate(",
]


def replace_exact(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected exactly one match, found {count}: {old[:80]!r}")
    return text.replace(old, new, 1)


def main() -> int:
    if not TARGET.exists():
        print(f"ERROR: target not found: {TARGET}", file=sys.stderr)
        return 2
    original = TARGET.read_text(encoding="utf-8")
    updated = original
    try:
        for old, new in REPLACEMENTS:
            # function-call replacement can occur multiple times by design.
            if old.startswith("TryAdvanceMHVSupersessionCandidate(mlv"):
                count = updated.count(old)
                if count < 1:
                    raise RuntimeError("no M09 supersession call sites found")
                updated = updated.replace(old, new)
            else:
                updated = replace_exact(updated, old, new)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3

    for token in FORBIDDEN_AFTER:
        if token in updated:
            print(f"ERROR: forbidden M09 Extreme-writer token remains: {token}", file=sys.stderr)
            return 4

    if "TryAdvanceMHVSupersessionFromCanonicalParent(" not in updated:
        print("ERROR: canonical-parent supersession helper missing", file=sys.stderr)
        return 5

    # Guard against accidental strategy-surface changes.
    for invariant in [
        "bool IsMHVTPWajibCompleted(",
        "bool IsMHVContinuationInvalidation(",
        "bool IsMHVLossPhaseEligible(",
        "bool IsMHVRetestInteraction(",
        "ENUM_MLV_STATE UpdateCanonicalMLVState(",
    ]:
        if invariant not in updated:
            print(f"ERROR: expected M09 invariant missing: {invariant}", file=sys.stderr)
            return 6

    TARGET.write_text(updated, encoding="utf-8")
    print("PASS: M09 single-writer hardening applied")
    print("PASS: M09 no longer installs/promotes/mutates canonical Extreme parent")
    print("NEXT: run static guard + MetaEditor compile before merge")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
