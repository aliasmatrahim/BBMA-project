# C005 Horizontal-BB Rejection Context Decision — 2026-08-25

Branch: `d1-owner-dev`

## Status
**APPROVED / PARTIAL ACCEPT / CORE-SUPPORTED CLARIFICATION / NON-EXECUTION AUTHORITY**

## Decision
The previous broad C005 HOLD is narrowed.

Accepted bounded interpretation:
- Bollinger Band must already be classified as flat/horizontal by the approved BB-state architecture;
- upper-side rejection context: candle High pierces Top BB and the same closed candle closes back inside/below Top BB;
- lower-side rejection context: candle Low pierces Low BB and the same closed candle closes back inside/above Low BB;
- this is classified as a **no-Momentum / mean-reversion context**;
- Mid BB is a **structural reversion reference**, not a guaranteed broker TP;
- this context alone is **not** standalone entry authority, not a new detector path, and not a replacement for Extreme/MHV/CSD/Re-Entry/REM/RRE/REE rules.

## Evidence basis
- Home Course rows HC-P02-002/003 directly describe horizontal-BB wick rejection and an expected move at least toward Mid BB.
- Finale V02 OA-F-V02-003 strongly confirms that outside-BB closes under flat BB are not Momentum.
- Finale V02 OA-F-V02-004 describes flat-BB excursions tending to revert, with Mid BB repeatedly used as a minimum/reference objective; Finale itself does not justify a universal guaranteed trade rule.
- External BBMA community material is treated only as corroboration and does not outrank primary/project source governance.

## Explicitly NOT promoted
The following remain HOLD / context-only:
- every horizontal-BB outer-band touch must reverse;
- every candle with body+wick outside a flat BB must immediately reverse;
- a wick merely approaching/touching an outer BB is sufficient for entry;
- Mid BB is a guaranteed broker TP;
- flat-BB rejection by itself authorizes BUY/SELL execution.

## Execution guard
If the same market event also satisfies an approved BBMA setup, execution must still come from that setup's existing lifecycle/authority. Example: a source-valid Extreme continues to require its approved reversal/retest maturity rather than being bypassed by this C005 context.

## Classification
- flat-BB rejection/no-Momentum context: **SOURCE-SUPPORTED / ACCEPTED CLARIFICATION**;
- Mid-BB reversion reference: **SOURCE-SUPPORTED CONTEXT**;
- standalone entry/guaranteed TP: **NOT AUTHORIZED**.

## Change control
This decision is documentation/strategy-spec clarification only. It does not authorize an MQL4 source change by itself. Any future use as a coded context flag must preserve non-execution authority unless separately approved.
