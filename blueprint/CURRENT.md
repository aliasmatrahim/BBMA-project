# BBMA Master Blueprint Development Status

## Current branch
`blueprint-dev`

## Source of truth
GitHub `aliasmatrahim/BBMA-project` is authoritative for the active Master Blueprint. BBMA strategy semantics are governed by the user-supplied references indexed under `docs/references/`.

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
16. `blueprint/patches/0016-p0-step8c-m17-approved-sltp-resolver.patch`
17. `blueprint/patches/0017-p0-step9-m18-label-only-scoring-authority.patch`
18. `blueprint/patches/0018-p0-step10-m19-risk-filter-accounting.patch`
19. `blueprint/patches/0019-p0-step11-m20-portfolio-gate-protection-ownership.patch`
20. `blueprint/patches/0020-p0-step12-m21-deterministic-money-management.patch`
21. `blueprint/patches/0021-p0-step13-m22-dumb-executor-idempotent-order-send.patch`
22. `blueprint/patches/0022-p0-step14-m23-position-lifecycle-exit-ownership.patch`

## Full-source SHA verification status
The previously recorded SHA-256 `274b3d380463f5cd9a477ce0c37b6da0db6c4cc6721013fdef4e984326b291bf` remains withdrawn because it was calculated from a partial reconstruction.

Last exact verified full-chain working-source SHA through patches 0001–0005:
`9ccbfd77032e3e9acdbf4b343ceaf98f632162d932cbb3fcad04a58539c1e3d8`

Patches 0006–0022 currently have focused patch/contract verification only. A new full-chain SHA must only be claimed after exact materialization and compilation of the complete ordered patch chain.

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
- `blueprint/contracts/M17_SLTP_EXIT_RESOLUTION_CONTRACT.md`
- `blueprint/contracts/M18_SIGNAL_SCORING_LABEL_CONTRACT.md`
- `blueprint/contracts/M19_RISK_FILTER_CONTRACT.md`
- `blueprint/contracts/M20_PORTFOLIO_PROTECTION_CONTRACT.md`
- `blueprint/contracts/M21_MONEY_MANAGEMENT_CONTRACT.md`
- `blueprint/contracts/M22_ORDER_EXECUTION_CONTRACT.md`
- `blueprint/contracts/M23_POSITION_LIFECYCLE_CONTRACT.md`
- `docs/references/SOURCE_INDEX.md`
- `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md`

## Complexity limiter
Limiter taxonomy remains LOCKED for the current blueprint-development cycle.

M01 BEGINNER; M02 BEGINNER; M03 INTERMEDIATE; M04 INTERMEDIATE; M05 INTERMEDIATE; M06 INTERMEDIATE; M07 INTERMEDIATE; M08 INTERMEDIATE; M09 INTERMEDIATE+; M10 INTERMEDIATE; M11 BEGINNER; M12 INTERMEDIATE+; M13 INTERMEDIATE+; M14 EXPERT-RESTRICTED; M15 EXPERT-RESTRICTED; M16 EXPERT-RESTRICTED; M17 INTERMEDIATE; M18 INTERMEDIATE; M19 EXPERT-RESTRICTED; M20 EXPERT-RESTRICTED; M21 INTERMEDIATE+; M22 EXPERT; M23 EXPERT-RESTRICTED; M24 EXPERT; M25 BEGINNER; M26 INTERMEDIATE; M27 EXPERT-RESTRICTED.

# P0 Architecture Repair

## Steps 1–13
Status: **COMPLETED AT THEIR LOCKED PATCH/CONTRACT LEVELS**

Core locked outcomes remain:
- source-aligned BBMA detectors and lifecycle ownership;
- M13 collector-only and M14 validate-only;
- M15 sole final entry authority with EntryMode 1/2 contract;
- M16 invalidation-only;
- M17 source-based BBMA TP/structural SL with no fixed-pip/RR-manufactured fallback;
- M18 observability-only with no trading score authority;
- M19 risk-filter-only with unit-correct EA-wide accounting;
- M20 prospective portfolio gate and protection-state ownership;
- M21 deterministic frozen-snapshot money management;
- M22 dumb/idempotent order execution.

## Step 14 — M23 Position Management / lifecycle exit policy
Status: **COMPLETED AT POSITION-LIFECYCLE / EXIT-OWNERSHIP CONTRACT LEVEL**

Baseline defects repaired:
- automatic 50% partial close at 1R changed the approved trade profile without a locked BBMA source rule;
- automatic breakeven migration replaced the M17 structural hard SL after entry;
- explicit manual `OrderClose()` at `initial_take_profit` duplicated the broker-side TP already supplied by M17->M22;
- normal-position lifecycle management mixed strategy exit policy with broker execution mechanics.

Implemented by:
`blueprint/patches/0022-p0-step14-m23-position-lifecycle-exit-ownership.patch`

Patch commit:
`47ae3c91440667148df63fffc72f4081d54b1e21`

Contract:
`blueprint/contracts/M23_POSITION_LIFECYCLE_CONTRACT.md`

Contract commit:
`e1eaf7f49a5f7987551f98977cc54c2ae7fdfd44`

Locked M23 behavior:
- normal positions retain broker-side M17-approved SL/TP unchanged;
- no 1R partial close, automatic breakeven, trailing stop, TP2/TP3 or synthetic manual TP close;
- M23 synchronizes monitored state with live broker state and revalidates EA ownership before lifecycle action;
- M20 basket-loss emergency protection remains the sole active M23-initiated close policy;
- emergency liquidation is full-lot only and retries on later ticks while the M20 latch remains active;
- dynamic opposite-CSM + BB-expansion close remains `FORUM_SUPPORTED` but disabled until a separate explicit lifecycle mapping is approved;
- M23 does not consume M18 score/level or recreate M15 strategy decisions.

### Verification boundary
The previously inspected M23 baseline block showed the 1R partial close, breakeven migration and manual TP close paths. Step 14 removes those unsupported normal-position actions and preserves only the M20 emergency protection route. Patch 0022 and the M23 contract are stored on `blueprint-dev`. No new full-chain compile/SHA is claimed yet.

## Next P0 action
**Step 15 — audit M24 Recovery Engine.**

Required focus:
1. recovery must rebuild only live EA-owned orders with exact pair/magic identity;
2. recovered positions must preserve broker Entry/SL/TP/lot state rather than reconstructing strategy levels from current market data;
3. reconcile ambiguous M22 send results without creating duplicate trades;
4. ensure missing/corrupt order comments or DecisionID mapping fail safe and cannot invent signal identity;
5. verify restart recovery is compatible with the simplified M23 lifecycle contract and M20 emergency-close latch.

Do not merge into `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
