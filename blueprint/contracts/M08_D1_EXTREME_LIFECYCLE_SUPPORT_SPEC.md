# M08 D1 Extreme Lifecycle Support Specification

Status: **IMPLEMENTATION-READY SUPPORT SPEC — NOT YET CODED**

Date: 2026-08-24

## 1. Purpose

F7 final-cycle lifecycle exit for `RRE` and `REE` is owned by D1 and closes the old-direction position when an **opposite D1 reversal-confirmed Extreme** atomically supersedes the old cycle.

The frozen EA currently carries Extreme lifecycle state for M15/H1/H4 but not D1. This specification defines the minimum D1 support extension required after the P3 runtime freeze closes.

This is a support-state extension only. It does **not** enable standalone D1 Extreme entry.

## 2. Source/semantic authority

D1 must reuse the already accepted M08/F2 Extreme lifecycle without reinterpretation:

`RAW EXTREME -> REVERSAL-CONFIRMED -> optional reversal continuation -> RETEST phase -> RETEST/ENTRY-READY or VOID/SUPERSEDED`

For F7 final-cycle proof, only the minimum cycle-boundary maturity is required:

`OPPOSITE RAW EXTREME = candidate only`

`OPPOSITE REVERSAL-CONFIRMED EXTREME = authoritative old-cycle supersession event`

The same deterministic reversal-direction mapping applies:
- SELL Extreme confirmation -> closed candle `Close < Open`;
- BUY Extreme confirmation -> closed candle `Close > Open`.

Accepted source-valid Momentum/outside-BB invalidation retains priority exactly as in F2.

## 3. Required state extension

Future `PairState` must carry D1 equivalents of the existing Extreme lifecycle slots:

- `extreme_d1_buy_lifecycle`;
- `extreme_d1_sell_lifecycle`.

They must use the same `ExtremeLifecycleData` schema unless a later compile-level refactor proves a neutral shared container is safer. No D1-only semantics may be invented.

## 4. Processing clock

M15 remains the sole orchestration clock.

D1 Extreme lifecycle advances only when orchestration observes a **new fully closed D1 candle**. It must not create an independent D1 timer/clock or process the current live D1 candle as confirmed evidence.

The same owner-candle identity/idempotency rule applies: one D1 lifecycle transition per unique closed D1 candle.

## 5. Detection and maturity ownership

M08 remains the Extreme detector/maturity owner.

D1 support must reuse the same canonical functions/state transitions used for H1/H4/M15 where possible. If code currently hard-codes allowed timeframes, implementation must generalize the timeframe routing without changing the Extreme Boolean semantics.

M23/M24 must **consume** the resulting D1 lifecycle state/event; they must not recreate D1 Extreme logic.

## 6. F7 lifecycle event export

For a D1-owned lifecycle-managed RRE/REE position, the event needed by M23/M24 is:

`OppositeExtremeReversalConfirmed = true`

only when:
- the D1 Extreme direction is opposite the live position direction;
- the D1 lifecycle has reached `EXT_MAT_REVERSAL_CONFIRMED` on a fully closed D1 candle;
- the candidate has not already been invalidated/voided by higher-priority accepted Extreme invalidation semantics;
- the event belongs to the currently tracked owner cycle/provenance.

That event maps to:

`LIFE_EXIT_LATCHED / EXIT_CYCLE_SUPERSEDED`.

## 7. No standalone D1 Extreme entry side effect

Adding D1 lifecycle state must not:
- add `SIGNAL_EXTREME` to executable entry eligibility;
- create a D1 standalone Extreme order path;
- bypass M13/M14/M15/M16;
- treat RAW D1 Extreme as entry or close authority;
- relax the existing Extreme retest/entry-ready rule for any future standalone Extreme execution.

D1 lifecycle tracking exists because RRE/REE position management needs D1 cycle proof, not because D1 Extreme execution has been approved.

## 8. Recovery/replay requirement

M24 restart recovery must be able to reconstruct the D1 Extreme lifecycle needed for the owner-cycle supersession decision from closed D1 history using the same canonical M08/F2 state machine.

If required D1 history cannot prove whether an opposite reversal-confirmed Extreme occurred while the terminal was down:
- do not guess;
- preserve broker position/SL/TP/lot truth;
- keep M19/M20 exposure and emergency authority;
- freeze ordinary F7 lifecycle management with a `LIFECYCLE_HISTORY_INSUFFICIENT`-class diagnostic.

A stale checkpoint alone must not override contradictory deterministic replay when sufficient history exists.

## 9. Cross-module contract

- M08/F2 owns D1 Extreme detection/maturity.
- M10 owns D1 CSM/Momentum classification where lifecycle replay requires it.
- M12 owns D1 Re-Entry production/re-arm events.
- M15/M27 remains orchestration clock.
- M23 consumes the D1 supersession event for open RRE/REE positions.
- M24 reconstructs/replays the event across restart.

No duplicated detector is permitted in M23/M24.

## 10. Acceptance checks after implementation

Static/runtime validation must prove:
- D1 RAW Extreme alone does not close RRE/REE;
- first valid opposite D1 reversal-confirmation promotes the lifecycle correctly;
- invalid/void D1 Extreme does not close;
- same-direction D1 Extreme does not close the old-direction position as an opposite-cycle event;
- repeated M15 ticks do not process one D1 closed candle twice;
- restart replay reproduces the uninterrupted D1 Extreme maturity state;
- no standalone D1 Extreme order becomes executable;
- H1/H4/M15 Extreme behavior remains unchanged.

## Final requirement

The F7 targetless lifecycle is not production-complete for `RRE`/`REE` until this D1 Extreme support is implemented and verified. The source semantics are already resolved; this file records the missing support-state contract only.
