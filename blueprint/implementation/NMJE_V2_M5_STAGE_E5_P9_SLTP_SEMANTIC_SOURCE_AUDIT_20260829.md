# NMJE v2 / M5 Stage-E5 P9 SL/TP Semantic-Source Audit — 2026-08-29

## Decision

The approved existing mapping is retained unchanged:

- D1-opportunity Re-Entry: H1 Re-Entry, with M15 Re-Entry as explicit fallback.
- Legacy Re-Entry: H1 Re-Entry.
- REM: H4 Re-Entry.
- RRE / REE: D1 Re-Entry.

The user explicitly confirmed that P9 must remain audit-only. No alternative
owner, score, geometry rule, or runtime switch is introduced.

## Audit finding

- `ResolveSelectedSLTPSourceComponent` selects by candidate semantic family and
  required timeframe, not component-array order, recency, or candidate hash.
- The owner is frozen once from the M15-selected canonical candidate before
  shadow attribution.
- M17 independently validates the same signal family, direction, timeframe,
  and exact confirmed Re-Entry candle.
- The structural anchor is reconstructed only inside that source lifecycle's
  `StartCandleTime..ConfirmationCandle` closed-candle window.
- The BB destination is read from the same source timeframe and candle.
- No ATR, volatility substitute, fixed stop, risk/reward destination, or
  non-BBMA geometry is introduced.

## Safety boundary

- EA source and visible build remain unchanged at `4.68` because P9 introduces
  no source-bearing behavior or telemetry.
- Candidate eligibility, ranking, M15 timing, SL/TP values, risk, OrderSend,
  D1TPW, C044, and NMJE authority remain unchanged.
- The new static regression locks the verified mapping and exact-source
  lifecycle/destination chain against accidental future processing-order drift.
- PR remains draft; no activation or merge authorization.

## Evidence

- P9 semantic-source static regression PASS.
- Full N3 and M5 Stage A-E5 regression/static suite PASS.
- Python compile PASS.
- N3 static guard PASS, including M15/M16 authority and shadow-no-gate checks.
- Native MT4 MetaEditor: `Result: 0 errors, 0 warnings, 411 msec elapsed`;
  unchanged-source EX4 refreshed at 573,094 bytes.

