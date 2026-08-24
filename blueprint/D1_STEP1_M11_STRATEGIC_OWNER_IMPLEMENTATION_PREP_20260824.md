# D1 Step 1 — M11 Strategic Owner Implementation Preparation

Date: 2026-08-24  
Development branch: `d1-owner-dev`  
Canonical frozen branch: `blueprint-dev`  
Status: **PATCH PREPARED / NOT YET APPLIED TO EA SOURCE / NATIVE COMPILE PENDING**

## Purpose
Prepare the first code step from the reconciled D1 implementation sequence without modifying the frozen `blueprint-dev` runtime candidate.

Target step:

`M11 D1 strategic-owner producer`

This step intentionally does **not** connect the new state to M15/M16 entry authority yet. Therefore when the patch is eventually applied, this first dependency step should be observability/state-production only and must not independently change trading eligibility.

## Canonical specification basis
Authoritative records:
- `blueprint/decisions/HOME_COURSE_D1_TRANSITION_MAJOR_TREND_OWNER_DECISION.md`;
- `blueprint/CORE_V2_D1_CANONICAL_CONTRACT_RECONCILIATION_AUDIT_20260824.md`;
- `blueprint/contracts/M11_D1_MAJOR_TREND_OWNER_CONTRACT.md`;
- reconciled `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`.

Resolved states:
- BUY confirmed: latest fully closed D1 `Close > MA50` AND current MA50 > previous closed-D1 MA50;
- SELL confirmed: latest fully closed D1 `Close < MA50` AND current MA50 < previous closed-D1 MA50;
- otherwise-valid disagreement/equality/flat-slope state: `D1_TRANSITION`;
- invalid/incomplete D1/MA50 history: `D1_OWNER_UNRESOLVED`.

## Frozen-source baseline
Canonical frozen source checked on `blueprint-dev`:
- path: `blueprint/source/BBMA_EA.mq4`;
- Git blob SHA: `105d992d8e6bf667e928172af1938b8ce573dfb9`;
- current header before future patch: `Version 4.5.1 - P3-UI-01 Input Panel Cleanup`;
- current Module 11 contains no D1 major-trend owner implementation;
- current `TimeframeData.trend` is price-vs-EMA50 only and is not reused as the new owner formula;
- current `PairState` already contains `prev_daily_ema50` and `current_daily_ema50`, which the prepared M11 producer uses as diagnostic/cache values rather than introducing duplicate MA50 cache ownership.

## Prepared patch
Patch artifact:

`blueprint/patches/0026-d1-step1-m11-strategic-owner-producer.patch`

Prepared on branch:

`d1-owner-dev`

The patch adds:
1. `ENUM_D1_OWNER_STATE` with `UNRESOLVED`, confirmed BUY, confirmed SELL, and `D1_TRANSITION`;
2. `D1MajorTrendOwner` state payload;
3. one `PairState.d1_major_trend_owner` owner slot;
4. deterministic initialization to unresolved;
5. Module 11 producer functions using only fully closed D1 data;
6. previous closed-D1 MA50 from the existing M06 `EMA()` helper at `barIndex + 1`;
7. one producer call after frozen D1/H4/H1/M15 snapshot loading in `ProcessPair()`;
8. `DBG_SIGNAL` trace output for focused future runtime verification;
9. future build identifier `D1-01 M11 Strategic Owner`, left-aligned in the source header as required by project governance;
10. matching dashboard/init-log build markers.

## Architecture checks
### M15 sole processing clock
PASS by design. M11 is called only from the existing M15-triggered `ProcessPair()` path. No D1 timer/independent processing clock is introduced.

### Closed-candle discipline
PASS by design. Classification requires:
- `d1_data.is_valid`;
- `d1_data.is_closed`;
- `timeframe == PERIOD_D1`;
- closed D1 candle time;
- current and immediately previous closed-D1 MA50 values.

### No invented threshold
PASS by design. No ATR, pip tolerance, percentage distance, timer, fixed-N confirmation days, score, RSI/ADX, session or news logic is added.

### No H4 override
PASS at producer level. M11 does not consume H4 data.

### No trading-authority change in Step 1
PASS by design. The prepared patch does not change:
- `BuildConfirmedReEntryCandidate()`;
- M15 `PriorityEngine_Atomic()` eligibility;
- M16 invalidation;
- REM/RRE/REE signatures;
- M17/M19/M20/M21/M22 execution/risk behavior;
- M23/M24 lifecycle/recovery behavior.

The M11 owner becomes an available state only. M15/M16 consumption remains the next dependency step.

## Static review findings
No new strategy ambiguity was introduced in the prepared producer mapping.

One deliberate semantic distinction is preserved:
- `D1_TRANSITION` has valid market data (`IsValid=true`) but no executable direction (`DIR_NONE`);
- `D1_OWNER_UNRESOLVED` means the required D1 data/history itself is not deterministically available (`IsValid=false`).

This distinction is required so future M15/M16 can fail closed for both states without conflating source-valid transition with broker/history failure.

## Verification status
Completed:
- source/contract preflight;
- exact frozen-source context review for enum/struct/init/M11/ProcessPair/header/dashboard/init-log insertion points;
- patch ordering normalized for apply-ready unified-diff structure;
- source-build identifier in patch is unique and left-aligned.

Pending before integration:
- actual patch application to an EA source working copy/branch;
- native MetaEditor compile 0 errors / 0 warnings;
- static structural diff review after materialization;
- focused runtime traces for BUY, SELL, TRANSITION and UNRESOLVED classifications.

## Freeze protection
`blueprint-dev/blueprint/source/BBMA_EA.mq4` is intentionally unchanged by this preparation step.

The current P3 runtime evidence remains attributable to the frozen source. The patch is isolated on `d1-owner-dev` until the project deliberately chooses to replace/release that runtime candidate.

## Next dependency step
After D1-01 is materialized and compile-clean, the next implementation step is:

**D1 Step 2 — M15 frozen D1-owner payload + strategic entry gate**

Required behavior for that step:
- M15 consumes M11 output; it must not calculate MA50 itself;
- `D1_TRANSITION` / `D1_OWNER_UNRESOLVED` blocks new-entry authority;
- confirmed opposite D1 blocks the candidate;
- confirmed same-direction D1 permits the candidate to continue to existing H4/structural checks;
- REM remains a three-component signature; D1 is a separate strategic gate, not a fourth component;
- frozen D1 owner identity must be carried for M16 revalidation in the following dependency step.
