# NMJE v2 / M5 Stage-C1 Acquisition Record — 2026-08-28

## Scope

Acquire the latest fully closed M5 candle only from the existing M15-driven
`ProcessPair` cycle. This stage does not classify M5 context or create a new
event, relation, processing clock, candidate rule, rejection, ranking, trade
operation, persistence rule, or activation path.

## Materialized data path

- `TimeframeSnapshot.M5_CandleTime` and `M5_IsClosed` freeze the selected bar.
- `PairState.m5_data` stores read-only `TimeframeData`.
- `BuildTimeframeSnapshot` selects `GetLatestClosedCandleTime(..., PERIOD_M5)`.
- `ProcessPair` calls `GetDataForTimeframe` once for that frozen M5 candle.

## Explicitly absent

- No M5 `DetectExtreme`, Re-Entry, CSD, ECSD, CSM, or MLV invocation.
- No `M5Refinement` population or validation call.
- No M5 processing trigger; `IsNewCandle` remains PERIOD_M15-only.
- No candidate, M15/M16, M22, D1TPW, or C044 authority change.

## Build identity

- Header: `Version 4.6.2 - NMJE v2 M5 Closed-Data Acquisition`
- Property: `4.62`

