# M17 Structural-Range SL + SELL Spread Normalization — Implementation Audit

Date: 2026-08-25
Branch: `d1-owner-dev`
Status: **IMPLEMENTED / STATIC REGRESSION PASS / NATIVE METAEDITOR 0E0W PASS / RUNTIME TRACE PENDING**

## 1. Scope

This audit closes the source implementation of the user-approved decision:

`blueprint/decisions/M17_REENTRY_STRUCTURAL_RANGE_SL_EXECUTION_NORMALIZATION_DECISION_20260825.md`

The implementation changes only initial protective hard-SL resolution / broker-side SELL SL normalization for Re-Entry-owned executable decisions. It does not promote the engineering stop formula into universal BBMA Strategy Core.

## 2. Final source identity

Source:
`blueprint/source/BBMA_EA.mq4`

Version marker:
`Version 4.5.2 - M17 Structural SL Normalization`

MQL4 property:
`#property version "4.52"`

Final Git blob:
`4ccd444a96a34b494653143a7560516a4147b5bc`

Source implementation commit:
`c211395b2fbe94a4362f3e209eb2f1423b909ee5`

Protected-flow cleanup commit:
`b94cff5b3e382d55ebff0a7083389d9f5f57ffc9`

The cleanup removed only the unnecessary added `[M17-SL][LOT]` block from protected preflight flow; existing baseline preflight telemetry already records final Entry/SL/TP/Lot.

## 3. Implemented structural ownership

M17 does not redetect Re-Entry.

`ResolveMatchingReEntryLifecycle()` resolves the exact current M12 `ReEntryData` state corresponding to the approved `SLTPSourceComponent` and requires:
- confirmed and valid lifecycle;
- exact direction match;
- exact source timeframe match;
- `ConfirmationCandle == source.CandleTime`;
- valid `StartCandleTime` and `ConfirmationCandle` ordering.

`ResolveSourceOwnedStructuralAnchor()` then reconstructs only:

`StartCandleTime .. ConfirmationCandle`, inclusive.

Every bar must resolve exactly and be closed. Missing, mismatched, ambiguous or invalid lifecycle/bar data fails closed.

No arbitrary lookback, fractal/swing detector, ATR, session high/low or forced outer-BB hard-stop anchor is introduced.

## 4. BUY hard SL

Implemented:

`StructuralLow = minimum Low across exact Re-Entry lifecycle window`

`BUY StructuralSL = StructuralLow - Point`

Broker-facing BUY SL receives no spread buffer because the protective close side is Bid, aligned with MT4 Bid-chart structural candles.

Final SL is normalized outward to broker tick size/digits and remains subject to existing geometry, StopLevel/FreezeLevel, MaxSL and risk guards.

## 5. SELL hard SL

Implemented:

`StructuralHigh = maximum High across exact Re-Entry lifecycle window`

`SELL StructuralSL = StructuralHigh + Point`

Frozen preflight spread is converted through the canonical pip-price helper:

`RawSpreadPips = snapshot.CurrentSpreadPrice / pipValue`

`SpreadBufferPips = max(2.0, ceil(RawSpreadPips))`

with a small numerical epsilon before `MathCeil` to avoid a binary representation of an exact integer spread being rounded one pip too far.

Then:

`SELL BrokerSL = SELL StructuralSL + SpreadBufferPips * pipValue`

The final SELL stop is normalized outward to broker tick size/digits.

`MaxSpreadPips` remains an admission/rejection filter and is not used as the SL buffer.

## 6. Money-management / risk interaction

No M21 sizing formula was changed.

M17 writes final resolved SL into the decision/snapshot before lot sizing. Existing M21 AutoLot therefore uses the final entry-to-broker-SL distance:

- wider structural SL -> larger risk-per-lot -> smaller risk-based lot, subject to existing broker/min/max/step and `MaxAutoLot` constraints;
- FixedLot remains fixed, so wider SL increases monetary exposure and existing downstream risk guards remain authoritative.

No second spread adjustment or manual lot-reduction multiplier is introduced.

Existing baseline `[P3M1][PREFLIGHT_PASS]` / `[P3M2][PREFLIGHT_PASS]` telemetry records final Entry, SL, TP and Lot, so no protected-flow telemetry modification is required.

## 7. Protected-function / MM regression proof

Regression workflow:
`M17 structural SL regression audit`

Run:
`32849979993`

Job:
`97808366225`

Conclusion:
`SUCCESS`

Compared byte-for-byte against pre-M17 baseline commit:
`f2a59637762981dfb4f5583844a8b251c34a32da`

Unchanged function-body SHA-256 values:
- `ResolveSelectedSLTPSourceComponent` = `2579a475fea93577f999a89d3ffe89fb2c3c43f12479f5b1213fcc805db52ef8`
- `RunEntryPreflightAndExecute` = `ae7eae85403777fcc482ac61724a1ace8bb18db54d7781c489e55a97bce8e8c3`
- `CalculateLotSize` = `04d27247f8d5d51718403669dcacac76928d8769aa52d4e04d4a28297724ac79`

Regression artifact:
- name: `m17-structural-sl-regression-evidence`
- ID: `9563845694`
- digest: `sha256:15ed08315ee3b73c3e39156365c2fb3bff3701c3914fd806e3208522ea8185b4`

Result: no D1O-07 protected-flow leak and no M21 sizing-semantic change.

## 8. Native MetaEditor final compile

Final compile workflow run:
`32849850304`

Job:
`97807956720`

Head used for compile:
`b2574f8a3272599bb2e1c9e84f2042e2c02b94b0`

Source Git blob verified by the Windows runner:
`4ccd444a96a34b494653143a7560516a4147b5bc`

Windows checkout SHA-256:
`0b6fd57c56b193918c828db5270fa5239d02b4c2f7b5f103f712c260d9539d52`

MetaEditor:
`C:\Program Files (x86)\MetaTrader 4\metaeditor.exe`

Compile result:
**0 errors, 0 warnings, 151 msec elapsed**

Compile artifact:
- name: `m17-structural-sl-native-compile-evidence`
- ID: `9564102891`
- size: `376207` bytes
- digest: `sha256:5309c228855aa728edfceb97b8146d643327d8e8f2e91cccf96a153df8d9c1ac`

Artifact contains the EX4, MetaEditor compile log and compile-summary evidence.

## 9. TP boundary

TP semantics are deliberately unchanged by this source update.

Separate authority reconciliation:
`blueprint/M17_TP_AUTHORITY_RECONCILIATION_AUDIT_20260825.md`

Latest 2026-08-25 authoritative reconciliation retains material TP/lifecycle questions as HOLD, including universal `Re-Entry -> no Momentum => mandatory TP/reversal` behavior. Therefore this implementation does not:
- remove the current static TP;
- enable historical F7 no-Momentum dynamic closes;
- add SELL TP spread normalization;
- alter M23/M24 lifecycle authority;
- invent a replacement reward model.

Current static Re-Entry-owned outer-BB TP remains current project execution behavior, not newly promoted universal BBMA Core provenance.

## 10. Explicit non-regressions

This implementation does not intentionally change:
- Re-Entry detection/confirmation;
- D1/H4/H1/M15 authority hierarchy;
- REM/RRE/REE signatures;
- D1 Opportunity / D1O-07 canonical execution identity;
- entry timing;
- final signal selection;
- M21 lot formula;
- M19/M20 risk policy;
- M22 order-execution semantics;
- TP strategy/lifecycle;
- trailing stop, TP2 or TP3;
- BBMA Core detector semantics.

## 11. Remaining runtime evidence

Static/source and native-compile closure are complete. Runtime semantic validation remains pending.

Required broker/demo evidence should include:
- at least one BUY and one SELL;
- at least one JPY cross and one non-JPY FX pair where practical;
- `[M17-SL][STRUCT]` source timeframe, lifecycle start, confirmation candle, structural anchor, confirmation wick, raw spread, rounded SELL spread buffer and final broker SL;
- existing preflight Entry/SL/TP/Lot telemetry;
- actual Bid/Ask/spread around order placement where available;
- proof BUY received no spread buffer;
- proof SELL buffer followed `max(2, ceil(spreadPips))`;
- proof final AutoLot/risk uses the finalized hard-SL distance.

## Final verdict

**M17 STRUCTURAL-RANGE SL EXECUTION NORMALIZATION: IMPLEMENTED / STATIC REGRESSION PASS / NATIVE METAEDITOR 0E0W PASS.**

Only broker/demo runtime traces remain before semantic runtime closure. TP architecture remains a separate material strategy-HOLD boundary.
