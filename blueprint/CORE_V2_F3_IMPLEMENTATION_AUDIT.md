# CORE-V2-F3 — Re-Entry Type 1 Structural Context Implementation Audit

Date: 2026-08-22
Status: **IMPLEMENTED / STATIC REGRESSION PASS — NATIVE METAEDITOR COMPILE + RUNTIME TRACE STILL REQUIRED**
Branch: `blueprint-dev`

## Scope
Implements the resolved `CORE_V2_F3_TYPE1_CONTEXT_DECISION.md` contract in M12 while preserving F1 MHV/MLV, F2 Extreme maturity, exact REM/RRE/REE signatures, risk, execution and dashboard semantics.

## Removed mismatch
- Removed the old `DetectReEntry_Type1()` MA5/MA10-touch-only shortcut.
- Type 1 is no longer confirmed atomically from a single MA-cluster touch with no prior BBMA owner.
- Removed generic `MaxWaitBars_ReEntry` expiry from Type 1 strategy lifetime only; Type 2/3/4 retain their existing project freshness behavior pending their own reviews.
- Exact Type 3 (`CSM`) and Type 4 (`CSD`) precursor families are evaluated before generic Type 1 ownership, preventing Type 1 from stealing their setup.

## Implemented Type 1 lifecycle
`SOURCE-VALID SAME-TF eCSD/CSD/CSM OWNER -> STRUCTURAL MOMENTUM PAUSE / RETRACE TOWARD MA5/10 -> TYPE1 RANGING OWNER -> MA5/MA10 INTERACTION + VALID CLOSE-SIDE -> TYPE1 CONFIRMED`.

### Prior move owner
- Same-timeframe source-valid `eCSD`, `CSD`, or `CSM` is required before Type 1 ranging can exist.
- The direction event is stored as structural owner/provenance only; it does not itself create a Type 1 entry.
- EMA slope, ATR, fixed pip displacement and arbitrary candle-count movement are not used.

### Structural pause/ranging
- One candle that merely fails CSM is not enough.
- Ranging/retrace starts only after the prior owner when a later closed candle provides actual retrace evidence toward the relevant MA cluster: direction-only close progression toward the cluster, or a valid cluster interaction itself.
- No pip/ATR threshold and no mandatory BB_FLAT gate is introduced.
- No fixed minimum candle count is used; if the structurally proven retrace candle also reaches the MA5/10 cluster and closes on the permitted side, it may complete Type 1 on that candle.

### Validation and invalidation
- Final BUY validation uses MA5/MA10 Low support interaction with close back/on the valid BUY side; SELL mirrors at MA5/MA10 High resistance.
- A pending/confirmed Type 1 is cleared when price closes clear through the full MA5/MA10 cluster against the intended direction. Penetration of only one MA is not automatically treated as failure.
- Opposite source-valid eCSD/CSD/CSM removes the old Type 1 direction owner.
- Same-direction CSM/CSD during Type 1 transfers to exact Type 3/4 ownership when enabled; otherwise the old ranging state is reset and the new direction/momentum event becomes fresh prior-move provenance. Same-direction eCSD similarly refreshes the direction owner rather than validating stale Type 1.

### Structural lifetime
- Type 1 candidate and confirmed owner use `ExpiryCandleTime = 0`; `IsReEntryIntrinsicExpired()` explicitly bypasses `RE_TYPE_1`.
- Type 1 therefore has no generic N-candle/session/day expiry. Its validity ends through structural invalidation/supersession.
- Type 2/3/4 behavior is intentionally left outside F3 scope.

## Static regression invariants
- no MA-touch-only `DetectReEntry_Type1()` remains;
- Type1 direction-owner and ranging states are present;
- exact Type3/Type4 precursors have ownership precedence over generic Type1;
- opposite direction/momentum invalidation and MA-cluster close-side failure are wired;
- Type1 fixed TTL is disabled without globally changing Type2/3/4;
- downstream standalone H1 `SIGNAL_RE_ENTRY` and REM/RRE/REE architecture remains present;
- full-source brace/parenthesis/bracket lexical sanity passes.

## Remaining verification
1. Native MetaEditor compile must report **0 errors / 0 warnings**.
2. Runtime traces should cover: no-owner MA touch rejection; eCSD->pause->touch confirmation; CSD/CSM owner cases; one non-CSM candle without retrace rejection; direct structural retrace+touch completion without fixed count; MA-cluster close-side failure; same-direction CSM reset/Type3 transfer; same-direction CSD Type4 transfer; opposite direction invalidation; long-lived Type1 with no timer expiry.
3. F4 H4 parent-owner implementation must gate standalone H1 Re-Entry without weakening this same-TF Type1 lifecycle.

Decision provenance: `blueprint/decisions/CORE_V2_F3_TYPE1_CONTEXT_DECISION.md`.
