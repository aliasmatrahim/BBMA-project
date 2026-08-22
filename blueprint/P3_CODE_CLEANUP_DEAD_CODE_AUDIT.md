# P3 Code Cleanup — Proven Dead/Legacy Code Audit

Status: **CLEANUP APPLIED — BEHAVIOR-PRESERVING STATIC PASS; NATIVE METAEDITOR RECOMPILE REQUIRED**

## Safety rule
A function was removed only when its `name(` token occurred exactly once in the canonical source, proving the definition had no caller. Structs were removed only when the type name occurred exactly once, proving no use site existed. Public compatibility inputs and active BBMA/risk/execution gates were intentionally retained.

## Removed
- `NormalizePrice()`
- `RoundToLotStep()`
- `ValidatePrice()`
- `IsSymbolAllowed()`
- `GetTolerance()`
- `FormatNumber()`
- `RefreshPrices()`
- `GetPairState()`
- `StorePairState()`
- `CopyPairState()`
- `CopyTimeframeData()`
- `GetCandleTimeFromBarIndex()`
- `GetExpiryTime()`
- `GetGlobalExpiryTime()`
- `GetCombinedExpiry()`
- `GetEffectiveMaxLot()`
- `ConvertSpreadToPoints()`
- `CreateCandleFromData()`
- `GetHighestHigh3()`
- `GetLowestLow3()`
- `AverageBodySize()`
- `CalculateBollingerArray()`
- `GetBBStateString()`
- `IsReversalCandle()`
- `IsCandleCloseOutsideBB()`
- `IsCandleCloseInsideBB()`
- `IsCandleCloseAbove()`
- `IsCandleCloseBelow()`
- `IsCandleCloseNear()`
- `IsDoubleTopPattern()`
- `IsDoubleBottomPattern()`
- `HasRecentCSD()`
- `HasRecentCSM()`
- `GetTrend()`
- `GetTrendFromMA50()`
- `BuildSLTP_Extreme()`
- `BuildSLTP_CSD()`
- `BuildReEntrySignal()`
- `CheckEffectiveExpiry()`
- `CalculateBasketProfitPercent_EA()`
- `struct TradeRequest`
- `struct OrderResult`
- `struct ExecutionSnapshot`

## Candidates retained automatically
- GetEffectiveExpiry: kept (occurrences=2)

## Explicit non-changes
- No BBMA detector, lifecycle, Re-Entry, MTF owner, REM/RRE/REE, M15/M16 authority, or M17 SL/TP behavior changed.
- No risk, portfolio, lot-sizing, trade-lock, broker execution, recovery, or dashboard behavior changed.
- Compatibility/display inputs were not removed in this pass even when non-authoritative.
- No new strategy condition, threshold, score, filter, or indicator was introduced.

## Verification
- Critical function anchors verified exactly once before/after cleanup.
- Removed functions verified to have zero surviving call-form references.
- `git diff --check` required before commit.
- Native MetaEditor compile remains required before this cleanup can be called compile-verified.
