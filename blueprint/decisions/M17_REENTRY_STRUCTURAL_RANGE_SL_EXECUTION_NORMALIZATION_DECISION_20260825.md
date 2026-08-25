# M17 Re-Entry Structural-Range SL + SELL Spread Normalization Decision — 2026-08-25

Status: **IMPLEMENTED / STATIC REGRESSION PASS / NATIVE METAEDITOR 0E0W PASS / RUNTIME TRACE PENDING**

Supersedes:
`blueprint/decisions/M17_SELL_SPREAD_BUFFER_EXECUTION_NORMALIZATION_DECISION_20260825.md`

## Purpose
Replace the former exact-confirmation-candle wick SL mapping with a deterministic source-owned Re-Entry structural-range anchor for both BUY and SELL, while retaining the already-approved SELL-only broker spread normalization.

## Source / provenance boundary
- BBMA PDF and Finale support Re-Entry as a MA5/MA10 structural retest/setup and support structural invalidation concepts, but do **not** prove this exact multi-candle range formula as a universal Oma Ally hard-SL rule.
- Finale V05 00:37:25–00:41:16 corroborates Re-Entry validity around the MA5/MA10 cluster and that penetration does not automatically invalidate the setup merely by wick interaction.
- Finale V07 00:51:55–00:53:28 contains a personal MA10 + allowance stop method; project governance keeps that as personal risk-management evidence, not universal Strategy Core.
- F7 keeps the exact hard-SL resolver classified as `EA_SAFETY` / deterministic project execution policy.
- Therefore the rule below is **EA_SAFETY / PROJECT EXECUTION NORMALIZATION**, not a new `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2` trading law.

## Locked structural window
For every executable Re-Entry-owned decision, use the exact validated `ReEntryData` lifecycle belonging to the decision's approved `SLTPSourceComponent`.

The structural window is:

`[ReEntryData.StartCandleTime ... ReEntryData.ConfirmationCandle]` inclusive

on the same source timeframe, direction and Re-Entry identity.

Rules:
1. `StartCandleTime` is the candle where M12 created/established that Re-Entry candidate lifecycle.
2. `ConfirmationCandle` is the fully closed source-timeframe validation candle that promoted the same lifecycle to `RE_STATE_CONFIRMED`.
3. Include every closed source-timeframe candle from start through confirmation, inclusive.
4. Do not scan arbitrary candles before `StartCandleTime`.
5. Do not use a generic fractal/swing detector, fixed lookback, ATR, session high/low or outer BB merely to widen the stop.
6. The source lifecycle must match the decision component by direction, timeframe and confirmation-candle identity. If it cannot be reconstructed exactly, fail closed rather than guess.
7. Once the decision reaches execution preflight, freeze the structural range used for that decision; do not drag the hard SL later because new candles print.

## BUY hard SL
Determine:

`StructuralLow = minimum Low of all closed candles in the locked Re-Entry structural window`

Then:

`BUY StructuralSL = StructuralLow - 1 broker Point`

Locked BUY behavior:
- no spread buffer;
- no forced placement at Low BB;
- no forced placement at MA5/MA10 Low;
- MA5/MA10 remains Re-Entry structure/validity context, not the hard-SL coordinate;
- normalize outward to broker tick size/digits;
- existing StopLevel/geometry/MaxSL/risk guards remain authoritative.

## SELL hard SL
Determine:

`StructuralHigh = maximum High of all closed candles in the locked Re-Entry structural window`

Then:

`SELL StructuralSL = StructuralHigh + 1 broker Point`

The broker-facing SELL stop then adds the already-approved frozen spread buffer:

`CurrentSpreadPips = FrozenCurrentSpreadPrice / CanonicalPipPrice`

`SpreadBufferPips = max(2.0, ceil(CurrentSpreadPips))`

`SELL BrokerSL = SELL StructuralSL + SpreadBufferPips * CanonicalPipPrice`

Examples for the spread buffer:
- 0.6 pip -> 2 pip
- 1.0 pip -> 2 pip
- 1.1 pip -> 2 pip
- 1.8 pip -> 2 pip
- 2.0 pip -> 2 pip
- 2.1 pip -> 3 pip
- 2.9 pip -> 3 pip
- 3.0 pip -> 3 pip

SELL rules:
- use the same frozen preflight `RiskValidationSnapshot` spread;
- do not chase live spread after entry;
- `MaxSpreadPips` remains an entry rejection filter and is not the SL buffer;
- no forced placement at Top BB;
- no forced placement at MA5/MA10 High;
- normalize final broker SL outward to valid tick size/digits.

## Why this replaces exact confirmation-candle High/Low
The current M17 hard SL uses only the High/Low of the exact mapped Re-Entry confirmation/source candle. A Re-Entry candidate can exist across multiple closed source-timeframe candles before confirmation. Therefore the confirmation candle can have a materially smaller wick range than an earlier candle that belongs to the same validated Re-Entry lifecycle.

Example SELL structural window:
- candidate start candle High = 198.340
- middle candle High = 198.325
- confirmation candle High = 198.326

Old exact-candle mapping anchors near 198.326.
New locked mapping anchors the same Re-Entry lifecycle at 198.340 before engineering/spread buffers.

This prevents the broker hard stop from sitting inside the very Re-Entry structure that produced the validated decision.

BUY is symmetrical on structural ownership:
- use the lowest Low in the Re-Entry window;
- do not add spread because BUY protective-stop triggering is already aligned to the Bid-side chart structure used by MT4 candles.

## Combination ownership
The rule follows the already-approved M17 `SLTPSourceComponent` ownership; it does not invent a new timeframe:
- normal standalone Re-Entry -> approved H1 Re-Entry source unless an existing approved D1-opportunity path selects H1/M15;
- REM -> approved H4 Re-Entry source;
- RRE / REE -> approved D1 Re-Entry source.

The structural range is reconstructed only from the matching Re-Entry lifecycle on that approved source timeframe.

## Money management
1. Final hard SL must be resolved before M21 AutoLot sizing.
2. `MM_AUTO_LOT` must size from the final entry-to-broker-SL distance, so a wider structural stop automatically produces a smaller lot while preserving the configured risk percentage subject to broker min/max/step constraints.
3. `MM_FIXED_LOT` remains fixed; a wider stop increases monetary exposure and existing M19/M20 risk gates remain authoritative.
4. Do not add an independent manual lot-reduction multiplier.

## RR / TP
- RR is recalculated using the final broker hard-SL distance.
- Do not manufacture a farther TP merely to preserve the old RR.
- TP mapping/lifecycle policy is outside this decision.
- SELL TP Bid/Ask normalization remains a separate unresolved/audit item unless explicitly approved later.

## Implementation requirements for next source update
1. Preserve current runtime/evidence attribution before changing `BBMA_EA.mq4`.
2. Expose or reconstruct the exact matching M12 `StartCandleTime` through `ConfirmationCandle` range for M17 without creating a second independent Re-Entry detector.
3. BUY: minimum window Low -> minus one Point -> outward tick normalization; no spread buffer.
4. SELL: maximum window High -> plus one Point -> rounded frozen spread buffer -> outward tick normalization.
5. Fail closed on missing/mismatched lifecycle identity or unavailable closed bars.
6. Run existing geometry, StopLevel, MaxSL and risk validations on the final hard SL.
7. Let M21 AutoLot calculate from that final SL.
8. Add diagnostics: source timeframe, start candle, confirmation candle, structural Low/High, old confirmation-candle wick, raw spread, rounded spread buffer, final broker SL, final lot.
9. Native MetaEditor: 0 errors / 0 warnings.
10. Static regression: prove no arbitrary lookback, no Top/Low-BB forced SL, BUY has no spread buffer, SELL buffer follows `max(2, ceil(spreadPips))`.
11. Runtime evidence: at least one BUY and one SELL; include at least one JPY cross and one non-JPY FX pair where practical.

## Explicit non-scope
This decision does not change:
- Re-Entry detection or confirmation conditions;
- D1/H4/H1/M15 authority hierarchy;
- REM/RRE/REE signatures;
- entry timing;
- TP strategy/lifecycle;
- `MaxSpreadPips` meaning;
- trailing stop or dynamic post-entry SL management;
- BBMA Core source semantics.

## Governance
- Locked by explicit user approval on 2026-08-25.
- This decision **supersedes** the prior SELL-spread-only queued decision because BUY/SELL structural anchor ownership is now intentionally upgraded from exact confirmation candle High/Low to the full validated M12 Re-Entry structural window.
- The old decision remains historical provenance only and must not be implemented independently.


## Implementation closure — 2026-08-25

Implemented in `blueprint/source/BBMA_EA.mq4` version 4.52.

Final source Git blob: `4ccd444a96a34b494653143a7560516a4147b5bc`.

Implementation audit: `blueprint/M17_STRUCTURAL_RANGE_SL_EXECUTION_NORMALIZATION_IMPLEMENTATION_AUDIT_20260825.md`.

Final native compile: run `32849850304`, job `97807956720`, **0 errors / 0 warnings**.

Static protected/MM regression: run `32849979993`, **PASS**.

TP semantics remain unchanged and separately governed by `blueprint/M17_TP_AUTHORITY_RECONCILIATION_AUDIT_20260825.md`. Runtime BUY/SELL broker evidence remains pending.
