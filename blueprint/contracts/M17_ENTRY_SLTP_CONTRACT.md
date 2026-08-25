# M17 Entry / SL / TP Resolution & Validation Contract

## Status

**ACTIVE CONTRACT — v4.52 / M17-SLRANGE-01**

This contract governs the currently executable M17 initial Entry/SL/TP resolver on branch `d1-owner-dev`.

Source-governance order remains:

`Primary Oma Ally PDF -> accepted Finale clarification -> authoritative Core -> approved project decision -> broker/EA engineering`.

The contract deliberately separates source-owned BBMA semantics from deterministic autonomous-EA safety policy.

## Provenance boundary

The current implementation uses these provenance classes:
- `BBMA_STRATEGY_CORE` — source-authoritative BBMA/Oma Ally semantics;
- `PROJECT_EXECUTION_POLICY` — deterministic executable mapping selected by the project where complete universal Core authority is not established;
- `EA_SAFETY` — deterministic broker-side protection / execution normalization required for autonomous operation;
- `HOLD` — source material that is not permitted to alter executable behavior without a later explicit strategy decision.

No `PROJECT_EXECUTION_POLICY` or `EA_SAFETY` rule may be described as an explicit universal Oma Ally rule.

## TP authority boundary

### Normal Extreme TP-Wajib

Normal Extreme TP-Wajib is separate source-authoritative Core semantics:
- Extreme BUY -> opposite MA5/MA10 High area first;
- Extreme SELL -> opposite MA5/MA10 Low area first;
- Mid BB is farther/maximum context.

This normal-Extreme rule does **not** automatically redefine the current Re-Entry-owned M17 TP table.

### Current executable Re-Entry-owned static TP table

The current deterministic executable policy remains:
- confirmed H1 `RE_ENTRY`: BUY -> H1 TOP BB, SELL -> H1 LOW BB;
- `REM`: BUY -> H4 TOP BB, SELL -> H4 LOW BB;
- `RRE`: BUY -> D1 TOP BB, SELL -> D1 LOW BB;
- `REE`: BUY -> D1 TOP BB, SELL -> D1 LOW BB.

The validated Re-Entry component owns the mapped timeframe.

Classification of this exact H1/H4/D1 static outer-BB table: **PROJECT_EXECUTION_POLICY / source-derived and community-corroborated, but not certified as a universal BBMA Strategy-Core hard-TP formula**.

Authority record:
`blueprint/TP_SOURCE_AUTHORITY_EXECUTION_MAPPING_AUDIT_20260825.md`.

Post-Re-Entry no-Momentum / pre-Re-Entry outer-BB hold / related deterministic lifecycle exits remain **HOLD** under current 2026-08-25 precedence and are not enabled by M17.

SELL TP Bid/Ask spread normalization also remains a separate pending TP execution decision. v4.52 does **not** alter TP broker-price semantics.

## Decision payload / owner identity

`BBMA_Decision` carries:
- `HasSLTPSourceComponent`;
- `SLTPSourceComponent`.

M15 preserves the already validated Re-Entry component identity required downstream:
- standalone Re-Entry -> H1 Re-Entry component;
- REM -> H4 Re-Entry component;
- RRE/REE -> D1 Re-Entry component.

The component payload survives M14 -> M15 -> M16, and M16 continues to revalidate owner-state identity before M17 executes.

## Exact closed-candle TP source resolver

M17 resolves the TP source component by exact `CandleTime` and timeframe with `iBarShift(..., exact=true)`.

Resolution is accepted only when:
- component type is `SIGNAL_RE_ENTRY`;
- component direction equals final decision direction;
- component timeframe exactly matches the approved mapping;
- resolved bar time equals the stored component candle time;
- resolved shift is `>= 1`, therefore closed.

A missing, stale, current-bar or ambiguous source fails closed.

## Current static BB destination resolver

The current project-policy single TP is read from the Bollinger Band on the exact closed mapped source candle:
- BUY -> upper BB;
- SELL -> lower BB.

M17 does not substitute another timeframe or manufacture a replacement target.

A BUY target at/below execution entry or SELL target at/above execution entry fails closed with `REJ_SLTP_UNRESOLVED`.

## Protective hard SL — M17-SLRANGE-01

Classification: **EA_SAFETY / STRUCTURAL EXECUTION NORMALIZATION**.

The previous exact-confirmation-candle wick stop is superseded by the approved whole-Re-Entry lifecycle structural range.

### Lifecycle ownership

M17 does not redetect Re-Entry and does not perform an arbitrary swing scan.

It resolves the exact confirmed M12 Re-Entry state that owns `SLTPSourceComponent` and requires:
- `RE_STATE_CONFIRMED`;
- `IsValid == true`;
- exact direction match;
- exact timeframe match;
- `ReEntryData.ConfirmationCandle == SLTPSourceComponent.CandleTime`;
- valid `StartCandleTime` and `ConfirmationCandle`;
- `StartCandleTime <= ConfirmationCandle`.

The hard-SL structural window is exactly:

`StartCandleTime -> ConfirmationCandle`, inclusive.

Both endpoints must resolve exactly to closed bars. Every candle included in the range must be valid and closed. Any missing/ambiguous lifecycle identity fails closed.

### BUY structural SL

For BUY:
- structural anchor = **lowest Low** across the exact lifecycle window;
- structural hard SL = `lowest Low - one broker Point`;
- no spread buffer is added.

Reason: the Bid-chart structure and BUY close/SL trigger side are both Bid-aligned.

### SELL structural SL

For SELL:
- structural anchor = **highest High** across the exact lifecycle window;
- structural hard SL = `highest High + one broker Point`;
- then add the frozen SELL execution-spread buffer.

Approved spread buffer:

`SpreadBufferPips = max(2, ceil(CurrentSpreadPips))`

Examples:
- 1.1 pip -> 2 pip;
- 1.8 pip -> 2 pip;
- 2.0 pip -> 2 pip;
- 2.1 pip -> 3 pip.

`CurrentSpreadPips` is derived from the preflight `RiskValidationSnapshot.CurrentSpreadPrice` and the pair pip value. The snapshot is frozen before SL resolution.

This is broker-side Ask-trigger normalization for a Bid-chart structural high. It is **not** a new BBMA trading rule.

`MaxSpreadPips` remains a separate entry rejection filter and is never used as the SL buffer.

### Tick-size normalization

After the structural/broker SL is resolved:
- BUY SL normalizes outward/downward to broker tick size;
- SELL SL normalizes outward/upward to broker tick size.

No inward normalization is permitted.

## Lot-sizing consequence

M17 owns final SL geometry but does not own lot sizing.

The final normalized SL is frozen into the risk snapshot before M21/lot calculation. Therefore:
- AutoLot uses the actual final Entry-to-SL distance; a wider SL naturally produces a smaller lot for the same configured risk percentage;
- FixedLot does not automatically shrink, so monetary risk rises when the SL is farther away.

No lot multiplier or ad-hoc compensation is introduced by M17.

## Execution reference price

Broker execution geometry remains:
- BUY market execution reference = ASK;
- SELL market execution reference = BID.

This is broker-side execution normalization and does not redefine BBMA setup entry semantics.

## Direction-aware geometry

A source-resolved pair is valid only when:
- BUY: `SL < Entry < TP`;
- SELL: `TP < Entry < SL`.

Wrong-side, zero-distance or inverted geometry is rejected.

## MaxSL ownership

`MaxSLPips` remains a project rejection cap only.

It may reject an excessively distant final source-resolved/broker-normalized SL. It never manufactures or clips the SL.

## MinRR ownership

`MinRRRatio` remains a rejection filter only and defaults off when configured as `0`.

When enabled it evaluates the final actual Entry/SL/TP geometry after M17 resolution. It never manufactures or moves TP to preserve RR.

## StopLevel / FreezeLevel

Direction-aware broker checks remain:
- BUY close/trigger side = BID;
- SELL close/trigger side = ASK.

Broker StopLevel/FreezeLevel constraints are engineering guards and never create replacement BBMA levels.

## Fail-closed behavior

`REJ_SLTP_UNRESOLVED` remains mandatory when the resolver cannot produce an unambiguous complete pair, including:
- mapped source component missing;
- source type/timeframe/direction mismatch;
- exact closed source candle unresolved;
- matching confirmed M12 Re-Entry lifecycle unresolved;
- lifecycle Start/Confirmation identity invalid;
- any required lifecycle candle unavailable/non-closed/invalid;
- structural anchor invalid;
- BB destination invalid;
- destination already crossed/stale;
- final geometry invalid.

No arbitrary swing scan, fixed-pip stop, fixed-pip TP or RR-manufactured fallback is allowed.

## Diagnostics

v4.52 adds diagnostic markers without changing detection/selection authority:
- `[M17-SL][STRUCT]` — source timeframe, lifecycle start/confirmation, structural anchor, confirmation wick, raw spread, rounded SELL spread buffer, structural SL, final broker SL, TP;
- `[M17-SL][LOT]` — final Entry/SL/TP and post-risk lot.

These logs are observability only.

## Lifecycle boundary

M17 remains initial Entry/SL/TP owner only.

It does not enable:
- post-Re-Entry no-Momentum automatic close;
- pre-Re-Entry outer-BB hold exception;
- dynamic opposite-CSM normal close;
- trailing stop;
- breakeven migration;
- partial close;
- TP2/TP3.

Any future dynamic source-owned exit belongs to M23/M24 lifecycle governance and requires a separately authorized strategy decision plus recovery/idempotency design.

## Ownership guard

M17 owns:
- execution-reference price normalization;
- validation of approved SLTP source-component identity;
- exact closed TP source lookup;
- current project-policy BB destination resolution;
- exact M12 lifecycle identity lookup for hard-SL anchoring;
- lifecycle structural-range BUY/SELL hard-SL resolution;
- SELL hard-SL spread normalization;
- outward tick-size normalization;
- BUY/SELL geometry validation;
- broker StopLevel/FreezeLevel checks;
- MaxSL and MinRR rejection filters;
- explicit fail-closed source-resolution behavior.

M17 does **not** own:
- BBMA signal detection;
- Re-Entry confirmation/state creation;
- REM/RRE/REE construction;
- final direction selection;
- lot sizing;
- portfolio risk;
- order execution;
- live-position lifecycle close;
- trailing stop / TP2 / TP3.

## Implementation records

Historical Step 8 engineering guard:
`blueprint/patches/0015-p0-step8-m17-sltp-source-guard-direction-validation.patch`

Historical Step 8C resolver:
`blueprint/patches/0016-p0-step8c-m17-approved-sltp-resolver.patch`

Current structural-range decision:
`blueprint/decisions/M17_REENTRY_STRUCTURAL_RANGE_SL_EXECUTION_NORMALIZATION_DECISION_20260825.md`

TP provenance audit:
`blueprint/TP_SOURCE_AUTHORITY_EXECUTION_MAPPING_AUDIT_20260825.md`

Current source marker:
`M17-SLRANGE-01`

Current source version:
`4.52 — M17 Structural SL Normalization`

## Verification requirement

Production closure for this source update requires:
1. static invariants above;
2. native MetaEditor compile with **0 errors / 0 warnings**;
3. repository source identity recorded;
4. future broker/demo runtime evidence for BUY/SELL structural-anchor and spread-buffer behavior.

Runtime evidence must verify actual broker Bid/Ask/SL geometry; compile success alone does not prove live spread behavior.
