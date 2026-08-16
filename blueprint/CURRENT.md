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
14. `blueprint/patches/0014-p0-step7-m16-owner-aware-invalidation.patch`
15. `blueprint/patches/0015-p0-step8-m17-sltp-source-guard-direction-validation.patch`

## Full-source SHA verification status
The previously recorded SHA-256 `274b3d380463f5cd9a477ce0c37b6da0db6c4cc6721013fdef4e984326b291bf` was discovered during Step 3D to have been calculated from a partial reconstruction and remains withdrawn.

Last exact verified full-chain working-source SHA through patches 0001–0005:
`9ccbfd77032e3e9acdbf4b343ceaf98f632162d932cbb3fcad04a58539c1e3d8`

Patches 0006–0015 have focused verification records in their contracts. A new full-chain SHA must only be claimed after exact materialization of the complete ordered patch chain.

## Locked supporting contracts
- `blueprint/ENTRY_MODE_CONTRACT.md`
- `blueprint/contracts/M06_MA_SOURCE_CONTRACT.md`
- `blueprint/contracts/M08_EXTREME_SOURCE_CONTRACT.md`
- `blueprint/contracts/M10_DIRECTION_MOMENTUM_SOURCE_CONTRACT.md`
- `blueprint/contracts/M12_REENTRY_SOURCE_CONTRACT.md`
- `blueprint/contracts/M13_COMBINATION_COLLECTOR_CONTRACT.md`
- `blueprint/contracts/M14_COMBINATION_VALIDATION_CONTRACT.md`
- `blueprint/contracts/M15_FINAL_SIGNAL_AUTHORITY_CONTRACT.md`
- `blueprint/contracts/M16_CONFLICT_INVALIDATION_CONTRACT.md`
- `blueprint/contracts/M17_ENTRY_SLTP_CONTRACT.md`
- `docs/references/SOURCE_INDEX.md`
- `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md`

## Complexity limiter
Limiter taxonomy remains LOCKED for the current blueprint-development cycle.

M01 BEGINNER; M02 BEGINNER; M03 INTERMEDIATE; M04 INTERMEDIATE; M05 INTERMEDIATE; M06 INTERMEDIATE; M07 INTERMEDIATE; M08 INTERMEDIATE; M09 INTERMEDIATE+; M10 INTERMEDIATE; M11 BEGINNER; M12 INTERMEDIATE+; M13 INTERMEDIATE+; M14 EXPERT-RESTRICTED; M15 EXPERT-RESTRICTED; M16 EXPERT-RESTRICTED; M17 INTERMEDIATE; M18 INTERMEDIATE; M19 EXPERT-RESTRICTED; M20 EXPERT-RESTRICTED; M21 INTERMEDIATE+; M22 EXPERT; M23 EXPERT-RESTRICTED; M24 EXPERT; M25 BEGINNER; M26 INTERMEDIATE; M27 EXPERT-RESTRICTED.

# P0 Architecture Repair

## Steps 1–3E — BBMA source alignment foundations
Status: **COMPLETED AT THEIR LOCKED CONTRACT LEVELS**

- M07 BB-shape ownership repaired.
- M09 MLV persistence/lifecycle repaired.
- M12 Re-Entry persistence and Type 1–4 source alignment repaired.
- M06 MA5/10 High/Low producer corrected to BBMA LWMA High/Low semantics.
- M08 Extreme source contract repaired.
- M10 CSM/CSD/eCSD source contracts repaired.

## Step 4 — M13 Combination Engine
Status: **COMPLETED AT COLLECTOR / COMBINATION CONTRACT LEVEL**

Source-locked project rows:
- REM = H4 Re-Entry + H1 Extreme + M15 confirmed MLV;
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme;
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

M13 is collector/assembler only.

## Step 5 — M14 Validation
Status: **COMPLETED AT VALIDATE-ONLY CONTRACT LEVEL**

M14 validates exact REM/RRE/REE identity, timeframe and direction; populates component payload; no invented chronology, priority or SL/TP source.

## Step 6 — M15 Final Signal Authority
Status: **COMPLETED AT FINAL-AUTHORITY CONTRACT LEVEL**

- `EntryMode 1 = RE_ENTRY_ONLY` -> confirmed H1 Re-Entry only.
- `EntryMode 2 = ALL_VALIDATED_BBMA_ENTRIES` -> confirmed H1 Re-Entry + validated REM/RRE/REE.
- raw Extreme/MLV/CSD/eCSD/CSM cannot directly execute.
- BUY and SELL are resolved atomically; unresolved opposite validated directions -> no trade.
- no arbitrary REM/RRE/REE quality ranking.

## Step 7 — M16 Conflict / Invalidation
Status: **COMPLETED AT CONFLICT / INVALIDATION CONTRACT LEVEL**

- decision components are revalidated against their real owner state;
- generic M15-based expiry assumptions removed;
- persistent H1/H4 Extreme validity overlay added;
- later same-timeframe source-valid CSM invalidates stored Extreme;
- M16 remains invalidation-only.

## Step 8 — M17 Entry / SL / TP
Status: **PARTIALLY COMPLETED / SAFE SOURCE GUARD ACTIVE**

### Source finding
The primary BBMA reference explicitly states for Extreme that reversal confirmation is required, retest is the point of entry, and SL may be placed a few pips beyond the highest shadow/wick. However, the supplied source does **not** define a deterministic TP formula.

For the currently executable confirmed Re-Entry / REM / RRE / REE paths, the supplied pages define setup/entry-location concepts but do not define a complete deterministic SL + TP pair suitable for autonomous execution.

Therefore the old blueprint formulas that manufactured SL from `MaxSLPips` and TP from `MinRRRatio` are **not accepted as BBMA source rules**.

### Safe guard
M17 now fails closed with `REJ_SLTP_UNRESOLVED` unless a future approved source resolver supplies a complete SL/TP pair and a non-`SIGNAL_NONE` source identity.

This means upstream BBMA setups may still be detected and validated, but they are not execution-ready until the SL/TP source gap is resolved.

### Engineering fixes completed
- BUY execution reference uses ASK; SELL uses BID.
- direction-aware geometry enforced: BUY `SL < Entry < TP`, SELL `TP < Entry < SL`.
- MaxSL conversion corrected using the project pip-price helper; `MaxSLPips` is a rejection cap only.
- `MinRRRatio` is a rejection filter only and no longer manufactures TP.
- StopLevel/FreezeLevel are direction-aware: BUY uses BID close/trigger side, SELL uses ASK.
- M23 compatibility call updated to pass explicit direction.
- `StopLossPoints` is normalized to actual broker points after valid resolution.

Patch:
`blueprint/patches/0015-p0-step8-m17-sltp-source-guard-direction-validation.patch`

Contract:
`blueprint/contracts/M17_ENTRY_SLTP_CONTRACT.md`

Focused patch SHA-256:
`8aeeb013aaa76182f222b31eb0b0dfeb67a2765090cc8dad7dc9a488188e0b8c`

### Focused verification
- dry-run/apply clean and exact generated target match;
- braces 521/521;
- parentheses 1583/1583;
- brackets 355/355;
- old M17 `MaxSLPips * Point / 10` formula absent;
- BID-only StopLevel/FreezeLevel behavior absent;
- source-resolution fail-closed guard present.

No new full-chain working-source SHA is claimed from this focused verification.

## Next P0 action
**Step 8B — resolve the BBMA SL/TP source gap before execution can be certified.**

Acceptable routes:
1. add another authoritative BBMA/Oma Ally source that explicitly defines deterministic SL/TP/exit rules; or
2. explicitly approve a separate non-BBMA trade-management SL/TP rule, clearly labelled as project management logic rather than BBMA strategy semantics.

Until Step 8B is resolved, later modules may still be audited, but the EA must remain fail-closed before execution.

Do not merge into `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
