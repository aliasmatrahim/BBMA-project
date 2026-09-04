# v4.61 — F7 Re-Entry Lifecycle Implementation

Date: 2026-09-04
Branch: `d1-owner-dev`
Status: **IMPLEMENTED / STATIC PASS / METAEDITOR 0E0W / RUNTIME VALIDATION PENDING**

## Decision boundary
User explicitly reopened the historical F7 lifecycle material for implementation on 2026-09-04. This satisfies the 2026-08-25 precedence condition requiring a later explicit strategy decision before executable promotion.

## Implemented F7 scope
- Re-Entry-owned trades use lifecycle management only for source-backed owners: standalone RE=H1, REM=H4, RRE=D1, REE=D1.
- Broker hard SL remains structural EA_SAFETY from the owner Re-Entry lifecycle window.
- Universal static outer-BB TP is removed for F7-managed trades; broker TP is `0`.
- Fixed `MinReEntrySLPips=5` and `MinReEntryRRRatio=1.0` introduced in v4.60 are removed.
- Global `MinRRRatio` is bypassed for targetless F7 trades because no source-proven reward coordinate exists at entry.
## Lifecycle reducer
Initial/re-armed state is `MOMENTUM_PENDING` after the owner Re-Entry. On each later fully closed owner-TF candle:
- same-direction canonical M10 CSM -> `WAIT_NEXT_REENTRY` / hold;
- later same-direction owner Re-Entry -> re-arm `MOMENTUM_PENDING`;
- opposite canonical M10 CSM while pending -> latched full close;
- first reverse-direction confirmation candle while pending and before same-direction CSM -> latched full close;
- opposite reversal-confirmed owner-TF Extreme -> cycle-superseded latched full close from any ordinary lifecycle state.

No timer, candle-count expiry, fixed pip target, ATR/ADX filter, trailing stop, partial close, TP2 or TP3 is introduced.

## Recovery / execution
Existing C044/F7 checkpoint plumbing is activated: immutable owner TF/Re-Entry candle, epoch anchor, last-processed owner candle, lifecycle state, exit reason/candle, replay seed and execution identity persist across restart. Replay is chronological and fail-frozen if required history/identity is unavailable. M20 emergency handling retains precedence. M23 executes full-position latched closes idempotently.

## Isolation guards
- M15 is excluded as an F7 lifecycle owner because the accepted F7 owner table is H1/H4/D1.
- D1 Extreme TP-Wajib lifecycle remains a separate feature and stays OFF.
- NMJE execution gating from v4.60 is unchanged by this F7 SL/TP implementation.
## Validation
Native MetaEditor compile of an isolated v4.61 checkout:
`Result: 0 errors, 0 warnings, 714 msec elapsed`.

Static checks passed for version identity, removal of fixed Re-Entry SL/RR, F7 gate enabled, D1TPW gate unchanged OFF, no outer-BB-test dependency, CSM/reverse/re-arm/cycle events, and checkpoint/recovery presence.

## Remaining gate
Runtime behavior is not yet production-verified. Required next evidence: same-CSM hold, no-Momentum reverse close, opposite-CSM close, re-arm, opposite-Extreme cycle close, restart replay, and close idempotency. Do not claim profitability from implementation/compile alone.