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

## Full-source SHA verification status
The previously recorded SHA-256 `274b3d380463f5cd9a477ce0c37b6da0db6c4cc6721013fdef4e984326b291bf` remains withdrawn because it was calculated from a partial reconstruction.

Last exact verified full-chain working-source SHA through patches 0001–0005:
`9ccbfd77032e3e9acdbf4b343ceaf98f632162d932cbb3fcad04a58539c1e3d8`

Patches 0006–0021 currently have focused patch/contract verification only. A new full-chain SHA must only be claimed after exact materialization and compilation of the complete ordered patch chain.

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
- `docs/references/SOURCE_INDEX.md`
- `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md`

## Complexity limiter
Limiter taxonomy remains LOCKED for the current blueprint-development cycle.

M01 BEGINNER; M02 BEGINNER; M03 INTERMEDIATE; M04 INTERMEDIATE; M05 INTERMEDIATE; M06 INTERMEDIATE; M07 INTERMEDIATE; M08 INTERMEDIATE; M09 INTERMEDIATE+; M10 INTERMEDIATE; M11 BEGINNER; M12 INTERMEDIATE+; M13 INTERMEDIATE+; M14 EXPERT-RESTRICTED; M15 EXPERT-RESTRICTED; M16 EXPERT-RESTRICTED; M17 INTERMEDIATE; M18 INTERMEDIATE; M19 EXPERT-RESTRICTED; M20 EXPERT-RESTRICTED; M21 INTERMEDIATE+; M22 EXPERT; M23 EXPERT-RESTRICTED; M24 EXPERT; M25 BEGINNER; M26 INTERMEDIATE; M27 EXPERT-RESTRICTED.

# P0 Architecture Repair

## Steps 1–12
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
- M21 deterministic frozen-snapshot money management.

## Step 13 — M22 Order Execution Engine
Status: **COMPLETED AT DUMB-EXECUTOR / IDEMPOTENT-SEND CONTRACT LEVEL**

Baseline defects repaired:
- M22 could mutate immutable payload by filling `decision.Pair` and regenerating `DecisionID`;
- retry loop used `retry <= MaxRetry`, permitting one extra send attempt;
- ambiguous broker outcomes were allowed to re-enter the retry loop, creating duplicate-order risk;
- ambiguous reconciliation searched for the entire long generated comment, which may fail because MT4/brokers can truncate order comments;
- duplicate detection and trade-lock checks were not consistently constrained to live EA-owned execution identity;
- execution deviation and generic broker failure were not cleanly distinguished in the send return path.

Implemented by:
`blueprint/patches/0021-p0-step13-m22-dumb-executor-idempotent-order-send.patch`

Patch commit:
`2aefae1f7cf422b936dccd2f353a1519b6e4ea64`

Contract:
`blueprint/contracts/M22_ORDER_EXECUTION_CONTRACT.md`

Contract commit:
`fa46a2105f21df5f275525dd98f4b07a15c5c58f`

Locked M22 behavior:
- M22 executes only; it cannot recreate `DecisionID`, direction, Entry, SL, TP or lot;
- missing/mismatched immutable payload fails closed;
- BUY uses live ASK and SELL uses live BID, bounded by the frozen execution deviation;
- only definite retryable broker errors can retry;
- before every send M22 checks for an already-open order using symbol + exact EA magic + order type + stable `BBMA|H:<SHORT_HASH(DecisionID)>` comment prefix;
- after an ambiguous broker result M22 reconciles once and then stops: if the order is not observable it returns `REJ_AMBIGUOUS_RESULT` and never automatically resends;
- this allows M24 recovery to reconcile any order that becomes visible later without duplicate creation;
- trade-lock checks consider live EA-owned positions only;
- `MaxRetry <= 0`, negative slippage or negative execution-deviation minimum fail initialization.

### Verification boundary
The baseline M22 send loop, ambiguous-error reconciliation, duplicate checks, execution-deviation path, order-comment identity scheme, and `ProcessEntry()` payload mutation were inspected. Patch 0021 and the M22 contract are stored on `blueprint-dev`. No new full-chain compile/SHA is claimed yet.

## Next P0 action
**Step 14 — audit M23 Position Management / lifecycle exit policy.**

Required focus:
1. remove or justify the current automatic 50% partial close at 1R because it is not part of the locked BBMA exit policy;
2. remove or justify automatic breakeven SL migration because M17 owns the structural hard SL and no trailing/extra exit management is part of BBMA Core;
3. verify TP handling preserves the original M17-approved BBMA destination and does not create a second synthetic TP path;
4. retain M20 emergency basket-loss liquidation as a protection action, but make close/retry ownership deterministic and EA-owned only;
5. audit all M23 `OrderClose()`/`OrderModify()` paths for ambiguous/failure handling and M24 recovery consistency.

Do not merge into `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
