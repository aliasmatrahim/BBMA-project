# CORE-V2-F2 — Extreme Lifecycle Implementation Audit

Date: 2026-08-22
Status: **IMPLEMENTED / STATIC AUDIT PASS — NATIVE METAEDITOR COMPILE + REGRESSION/RUNTIME STILL REQUIRED**
Branch: `blueprint-dev`

## Scope
Implements the resolved `CORE_V2_F2_EXTREME_MATURITY_DECISION.md` contract on the executable H1/H4 Extreme component paths. No M09/F1 MHV lifecycle, F3 Type-1, F4 H4-owner, risk, SL/TP, lot-sizing, portfolio or dashboard semantics are changed here.

## Pre-fix mismatch
- `DetectExtreme()` conflated RAW detection with a close-inside-BB condition and exported the result immediately as `SIGNAL_EXTREME`.
- REM/RRE/REE could therefore consume an atomic/RAW-like Extreme without the approved subsequent reversal-confirmation lifecycle.
- M16 persistence stored that atomic signal and invalidated it through a generic later any-CSM snapshot rather than an explicit F2 maturity owner.
- No deterministic reversal phase, frozen body anchor, retest-start state or body/MA5 retest-ready maturity existed.

## Applied implementation
- Added `ENUM_EXTREME_MATURITY`: `NONE -> RAW -> REVERSAL_CONFIRMED -> RETEST_PHASE -> RETEST_READY`, plus `VOID`.
- Added `ExtremeLifecycleData` owner state for H1/H4 BUY/SELL executable Extreme paths.
- `DetectExtreme()` is now RAW MA5/MA10-outside-BB detection only; close-inside-BB is no longer RAW eligibility.
- First subsequent same-TF reversal-direction closed candle promotes RAW to reversal-confirmed: SELL `Close < Open`, BUY `Close > Open`.
- Reversal phase can continue without fixed candle count; provisional body anchor updates until retest starts.
- Retest starts on first close progression back toward the original Extreme: SELL `CurrentClose > PreviousClose`, BUY `CurrentClose < PreviousClose`; trigger candle is excluded from anchor construction and freezes the anchor.
- Frozen body anchor = SELL highest body top / BUY lowest body bottom across the completed reversal phase.
- First valid range interaction with frozen body anchor OR current relevant MA5 completes standalone retest maturity.
- Applicable continuation outer-BB / source-valid directional Momentum invalidation is evaluated before promotion and resolves the lifecycle to `VOID`.
- REM/RRE/REE receive an Extreme `Signal` only from `ExportReversalConfirmedExtremeSignal()`, so RAW Extreme cannot satisfy an executable combination component.
- `MaxWaitBars_Extreme` remains downstream as the existing **project component-freshness overlay only**. It does not expire/reset RAW, reversal, retest or structural Extreme provenance in M08.
- M16 no longer owns the old any-CSM strategy invalidation; it consumes only mature M08 exports and retains component freshness/exact owner identity checks.

## Static invariants verified by patch script
- RAW detector contains no close-inside-BB gate.
- Reversal-confirmed export is the only path populating H1/H4 executable Extreme snapshots.
- Exact REM/RRE/REE signatures remain unchanged.
- Legacy `h1AnyCSMSnapshot/h4AnyCSMSnapshot` persistence path is removed.
- M16 component owner still exact-matches direction, timeframe and confirmation-candle identity.
- No standalone Extreme direct-entry authority is introduced.

## Remaining verification
1. Native MetaEditor compile must report **0 errors / 0 warnings**.
2. Regression/static re-audit should prove RAW Extreme never reaches M13/M14/M15 as an executable component.
3. Runtime trace should cover: RAW->REVERSAL_CONFIRMED; invalidation-before-confirmation; multi-candle reversal anchor update; retest start/freeze; body-touch completion; MA5-touch completion; invalidation precedence.
4. F1 implementation must consume the underlying F2 lifecycle for prior-Extreme provenance without weakening F2 maturity or converting `MaxWaitBars_Extreme` into a strategy-lifecycle TTL.

Decision provenance: `blueprint/decisions/CORE_V2_F2_EXTREME_MATURITY_DECISION.md`.
