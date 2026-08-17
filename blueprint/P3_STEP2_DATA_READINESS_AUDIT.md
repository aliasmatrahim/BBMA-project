# P3 Step 2 — Data Readiness & Historical-Series Validation

## Status
FIX A REQUIRED / RUNTIME VERIFICATION PENDING

## Finding
`ProcessPair()` loads D1/H4/H1/M15 snapshots, but the existing runtime path had no atomic readiness gate before detector/state-engine execution. `GetDataForTimeframe()` may leave a timeframe invalid when the target candle/history is unavailable.

## P3 S2 Fix A
Add:
1. `IsTimeframeDataReady()` requiring a valid closed candle, minimum EMA50+3 history, non-zero OHLC/point, all BBMA MA values, and Bollinger values.
2. DebugLevel=4 diagnostics per pair: `D1/H4/H1/M15 = OK/FAIL` plus bar counts.
3. Fail-closed pair-cycle gate: if any timeframe is not ready, skip that pair's signal pipeline for the current M15 cycle while allowing other pairs to continue.
4. Mark the blocked M15 candle processed to avoid a tight every-tick retry loop; retry on the next closed M15 candle.

No BBMA strategy semantics, EntryMode, SL/TP, risk, or execution rules are changed.

## Runtime acceptance target
For all seven pairs, Experts should show lines equivalent to:
`[P3S2] EURUSD D1=OK(...) H4=OK(...) H1=OK(...) M15=OK(...)`
with no unexpected `[P3S2][BLOCK]` once history is fully available.
