# BBMA Master Blueprint Development Status

## Current branch
`blueprint-dev`

## Source of truth
GitHub `aliasmatrahim/BBMA-project` is authoritative for the active Master Blueprint. Notion is supporting documentation only.

BBMA strategy semantics are governed by the user-supplied references indexed under `docs/references/`. If active blueprint logic conflicts with a supported BBMA source rule, blueprint/code must be repaired rather than the source being reinterpreted to fit the code.

## Immutable baseline
Source: `Master Blueprint 2.0.txt`

Verified baseline SHA-256:
`e217816e95126857c1e7fa3fde1ac10ecc28f196a82eb51cb2f3625a6901aa00`

The exact baseline is stored as deterministic gzip+base64 chunks under `blueprint/archive/`.

## Current revision — ordered patch chain
1. `blueprint/patches/0001-fix-m25-complexity-limiter.patch`
2. `blueprint/patches/0002-p0-step1-bbshape-extreme-contract.patch`
3. `blueprint/patches/0003-p0-step2-mlv-persistence-lifecycle.patch`
4. `blueprint/patches/0004-p0-step2b-mlv-void-transition-contract.patch`
5. `blueprint/patches/0005-p0-step3-reentry-persistence-lifecycle.patch`
6. `blueprint/patches/0006-p0-step3b-reentry-source-alignment.patch`
7. `blueprint/patches/0007-p0-step3c-m06-ma-source-alignment.patch`
8. `blueprint/patches/0008-p0-step3d-m08-extreme-source-alignment.patch`
9. `blueprint/patches/0009-p0-step3e-m10-csd-ecsd-csm-source-alignment.patch`
10. `blueprint/patches/0010-p0-step4a-m13-combination-collector-source-alignment.patch`
11. `blueprint/patches/0011-p0-step4b-m27-signal-owner-routing.patch`
12. `blueprint/patches/0012-p0-step5-m14-combination-validation.patch`
13. `blueprint/patches/0013-p0-step6-m15-final-authority-atomic-entry-mode.patch`

## Full-source SHA verification status
The previously recorded SHA-256 `274b3d380463f5cd9a477ce0c37b6da0db6c4cc6721013fdef4e984326b291bf` was discovered during Step 3D to have been calculated from a partial reconstruction and remains withdrawn.

Last previously verified exact full-chain working-source SHA through patches 0001–0005:
`9ccbfd77032e3e9acdbf4b343ceaf98f632162d932cbb3fcad04a58539c1e3d8`

Patches 0006–0013 have focused verification records in their contracts. A new full-chain SHA must only be claimed after exact materialization of the complete ordered patch chain.

## Locked supporting contracts
- `blueprint/ENTRY_MODE_CONTRACT.md`
- `blueprint/contracts/M06_MA_SOURCE_CONTRACT.md`
- `blueprint/contracts/M08_EXTREME_SOURCE_CONTRACT.md`
- `blueprint/contracts/M10_DIRECTION_MOMENTUM_SOURCE_CONTRACT.md`
- `blueprint/contracts/M12_REENTRY_SOURCE_CONTRACT.md`
- `blueprint/contracts/M13_COMBINATION_COLLECTOR_CONTRACT.md`
- `blueprint/contracts/M14_COMBINATION_VALIDATION_CONTRACT.md`
- `blueprint/contracts/M15_FINAL_SIGNAL_AUTHORITY_CONTRACT.md`
- `docs/references/SOURCE_INDEX.md`
- `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md`

## Complexity limiter
Limiter taxonomy remains LOCKED for the current blueprint-development cycle.

M01 BEGINNER; M02 BEGINNER; M03 INTERMEDIATE; M04 INTERMEDIATE; M05 INTERMEDIATE; M06 INTERMEDIATE; M07 INTERMEDIATE; M08 INTERMEDIATE; M09 INTERMEDIATE+; M10 INTERMEDIATE; M11 BEGINNER; M12 INTERMEDIATE+; M13 INTERMEDIATE+; M14 EXPERT-RESTRICTED; M15 EXPERT-RESTRICTED; M16 EXPERT-RESTRICTED; M17 INTERMEDIATE; M18 INTERMEDIATE; M19 EXPERT-RESTRICTED; M20 EXPERT-RESTRICTED; M21 INTERMEDIATE+; M22 EXPERT; M23 EXPERT-RESTRICTED; M24 EXPERT; M25 BEGINNER; M26 INTERMEDIATE; M27 EXPERT-RESTRICTED.

# P0 Architecture Repair

## Step 1 — BB Shape → Extreme contract
Status: **COMPLETED / VERIFIED AT BLUEPRINT LEVEL**

M07 owns BB-shape classification; BB shape is auxiliary Extreme context and no fabricated state is substituted when classification is disabled.

## Step 2 — M09 MLV persistence/lifecycle
Status: **COMPLETED / VERIFIED AT BLUEPRINT LEVEL**

Persistent BUY/SELL MLV slots, M09 lifecycle ownership, confirmed chronology/expiry and downstream immutable snapshots are established.

## Step 3 / 3B — M12 Re-Entry persistence + BBMA source alignment
Status: **COMPLETED AT M12 CONTRACT LEVEL**

Persistent H1/H4/D1 × BUY/SELL state is established. Type 1–4 contracts are source-aligned; only confirmed Re-Entry may be exported downstream.

## Step 3C — M06 MA producer source alignment
Status: **COMPLETED / VERIFIED AT BLUEPRINT LEVEL**

MA5/10 High/Low use source-specific LWMA High/Low production; EMA50 uses EMA Close.

## Step 3D — M08 Extreme source alignment
Status: **COMPLETED AT EXTREME SIGNAL CONTRACT LEVEL / TEMPORAL CSM INVALIDATION REMAINS**

BUY/Sell MA-side mapping, outer-BB rule and VOID-on-close-outside behavior are source-aligned. Raw Extreme is not standalone execution authority.

## Step 3E — M10 CSM / CSD / eCSD source alignment
Status: **COMPLETED AT SIGNAL-PRODUCER CONTRACT LEVEL**

Legacy unsourced CSM formula was removed; CSM follows directional outer-BB momentum context. eCSD and CSD use source-aligned crossing contracts; same-candle CSD-over-eCSD precedence is handled by M13.

## Step 4 — M13 Combination Engine / collector contract
Status: **COMPLETED AT COLLECTOR / COMBINATION CONTRACT LEVEL**

Source-locked project rows:
- REM = H4 Re-Entry + H1 Extreme + M15 confirmed MLV;
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme;
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

M13 is collector/assembler only and does not detect, mutate lifecycle, rank or choose SL/TP.

## Step 5 — M14 REM/RRE/REE validation
Status: **COMPLETED AT VALIDATE-ONLY CONTRACT LEVEL**

M14 validates exact combination identity/type/timeframe/direction, populates `candidate.Components[0..2]`, removes unrelated legacy sequence signatures and does not invent strict chronology, priority tier or SL/TP source.

## Step 6 — M15 Final Signal Authority / Entry Mode / atomic direction
Status: **COMPLETED AT FINAL-AUTHORITY CONTRACT LEVEL / M16+ DOWNSTREAM BLOCKERS REMAIN**

### Entry Mode now enforced
- `EntryMode 1 = RE_ENTRY_ONLY` → confirmed H1 Re-Entry only.
- `EntryMode 2 = ALL_VALIDATED_BBMA_ENTRIES` → confirmed H1 Re-Entry + validated REM/RRE/REE.
- raw Extreme, MLV, CSD, eCSD and CSM cannot become execution candidates merely from detector validity.
- standalone Extreme remains withheld until its source-required confirmation/retest entry lifecycle is deterministically locked.

### Atomic BUY / SELL repair
- M27 collects BUY and SELL candidates first into one pair-level pool.
- M15 is called exactly once after both directions have been built.
- if eligible BUY and SELL candidates coexist, M15 creates no winner/no final trade decision because the supplied source provides no universal tie-break rule.
- this no-trade-on-unresolved-opposite policy is a conservative engineering guard, not a claimed BBMA source rule.

### Priority policy repair
- `SignalMode` SAFE/NORMAL/AGGRESSIVE tier gating is removed from M15 final entry authority.
- no REM/RRE/REE superiority ranking is invented.
- same-direction multiple candidates use freshness/hash canonicalization for stable decision identity only, not quality ranking.
- final M15 decision remains `PriorityTier = TIER_NONE` and `SLTPSource = SIGNAL_NONE`.

### Freshness ownership repair
- removed generic combination expiry derived from `Comp1.CandleTime * M15 multiplier` in M27.
- combination candidates are rebuilt from current owner-valid snapshots every closed M15 cycle.
- standalone Re-Entry carries M12's explicit `ExpiryCandleTime`.
- M16 still contains legacy generic decision-expiry logic and is not certified yet.

Patch:
`blueprint/patches/0013-p0-step6-m15-final-authority-atomic-entry-mode.patch`

Contract:
`blueprint/contracts/M15_FINAL_SIGNAL_AUTHORITY_CONTRACT.md`

### Focused verification
- dry-run/apply clean;
- exact generated target match;
- braces 484/484;
- parentheses 1467/1467;
- brackets 334/334;
- old M15 tier gate absent;
- old per-direction M15 call absent;
- exactly one pair-level `PriorityEngine_Atomic(allCandidates, ...)` call;
- old generic Comp1/M15 candidate-expiry assignment absent;
- Entry Mode guard and standalone confirmed Re-Entry candidate builder present.

No new full-chain working-source SHA is claimed from this focused verification.

## Next P0 action
**Step 7 — M16 conflict / invalidation / owner-aware freshness integration.**

Priorities:
1. remove M16's legacy generic `decision.CandleTime + MaxWaitBars_Global * 900` and `CycleStartTime + ... * 900` invalidation assumptions;
2. preserve the Step 6 atomic no-trade result for unresolved opposite directions without inventing a winner;
3. connect temporal CSM invalidation of an existing Extreme only through an explicit lifecycle/owner contract — no same-candle hack;
4. define how owner-invalidated Re-Entry/MLV/Extreme components invalidate an assembled REM/RRE/REE decision;
5. keep M16 conflict/invalidation-only — no detection, priority, SL/TP, risk or execution ownership.

After M16, continue to M17 entry/SL/TP resolution and direction-aware validation.

Do not merge into `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
