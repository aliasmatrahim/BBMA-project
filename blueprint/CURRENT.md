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
23. `blueprint/patches/0023-p0-step15-m24-recovery-hash-tombstone.patch`

## Full-source SHA verification status
The previously recorded SHA-256 `274b3d380463f5cd9a477ce0c37b6da0db6c4cc6721013fdef4e984326b291bf` remains withdrawn because it was calculated from a partial reconstruction.

Last exact verified full-chain working-source SHA through patches 0001–0005:
`9ccbfd77032e3e9acdbf4b343ceaf98f632162d932cbb3fcad04a58539c1e3d8`

Patches 0006–0023 currently have focused patch/contract verification only. A new full-chain SHA must only be claimed after exact materialization and compilation of the complete ordered patch chain.

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
- `blueprint/contracts/M24_RECOVERY_CONTRACT.md`
- `docs/references/SOURCE_INDEX.md`
- `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md`

## Complexity limiter
Limiter taxonomy remains LOCKED for the current blueprint-development cycle.

M01 BEGINNER; M02 BEGINNER; M03 INTERMEDIATE; M04 INTERMEDIATE; M05 INTERMEDIATE; M06 INTERMEDIATE; M07 INTERMEDIATE; M08 INTERMEDIATE; M09 INTERMEDIATE+; M10 INTERMEDIATE; M11 BEGINNER; M12 INTERMEDIATE+; M13 INTERMEDIATE+; M14 EXPERT-RESTRICTED; M15 EXPERT-RESTRICTED; M16 EXPERT-RESTRICTED; M17 INTERMEDIATE; M18 INTERMEDIATE; M19 EXPERT-RESTRICTED; M20 EXPERT-RESTRICTED; M21 INTERMEDIATE+; M22 EXPERT; M23 EXPERT-RESTRICTED; M24 EXPERT; M25 BEGINNER; M26 INTERMEDIATE; M27 EXPERT-RESTRICTED.

# P0 Architecture Repair

## Steps 1–15
Status: **COMPLETED AT THEIR LOCKED PATCH/CONTRACT LEVELS**

Core locked outcomes:
- BBMA detectors and persistence are source-aligned;
- M13 collector-only, M14 validate-only, M15 sole final entry authority;
- EntryMode 1 = H1 Re-Entry only; EntryMode 2 = H1 Re-Entry + validated REM/RRE/REE;
- M16 invalidation-only;
- M17 uses source-owned BBMA destinations and structural protective SL with provenance separation (`PDF_CORE`, `FORUM_SUPPORTED`, `EA_SAFETY`);
- M18 is observability-only with no trading score authority;
- M19 is filter-only with unit-correct EA-wide risk accounting;
- M20 performs prospective portfolio gating and owns protection state, not broker closes;
- M21 performs deterministic frozen-snapshot lot sizing;
- M22 is a dumb/idempotent executor using stable `BBMA|H:<SHORT_HASH(DecisionID)>` identity;
- M23 preserves broker-side M17 SL/TP and removes unsupported 1R partial close/breakeven/synthetic TP handling;
- M24 recovery is restart-idempotent and hash-based without fabricating strategy identity.

## Step 15 — M24 Recovery Engine
Status: **COMPLETED AT RECOVERY / RESTART-IDEMPOTENCY CONTRACT LEVEL**

Baseline defects repaired:
- recovery rebuilt a full `DecisionID` from lossy order-comment fields;
- `Q:` stores `SHORT_HASH(sequenceHash)`, so rebuilding with `Q:` cannot reproduce the original `DecisionID` deterministically;
- broker/MT4 comment truncation could remove later metadata while the stable `H:` prefix remained available;
- execution history was rebuilt only from currently open orders, allowing a previously executed-and-closed decision to be forgotten after restart;
- comment parsing dropped the final field when no trailing `|` existed;
- recovery matched magic but did not require exact live symbol + market-order ownership before rebuilding state;
- legacy recovery inferred partial-close/breakeven lifecycle state that Step 14 has removed.

Implemented by:
`blueprint/patches/0023-p0-step15-m24-recovery-hash-tombstone.patch`

Patch commit:
`7b75d4807396c666368e62af250b689c74115438`

Contract:
`blueprint/contracts/M24_RECOVERY_CONTRACT.md`

Contract commit:
`6f08d0be253da6dadb8f91cb6aebf4ae23cbebce`

Locked M24 behavior:
- stable execution identity is `H:SHORT_HASH(DecisionID)`, not a fabricated full DecisionID;
- exact EA ownership requires matching configured symbol + exact magic + market-order type;
- restart tombstones are rebuilt from both open orders and account order history;
- `IsDecisionExecuted()` recognizes full DecisionID or matching executed hash tombstone;
- ambiguous M22 orders that appear later can be recovered without a second `OrderSend()`;
- live broker Entry/SL/TP/lot are preserved exactly and are never recreated from current market data;
- valid hash-only/truncated-comment positions may be monitored as `REC_IDENTITY_HASH_ONLY` without inventing signal metadata;
- invalid geometry or unsafe lot state fails recovery closed;
- recovery does not reactivate partial-close or breakeven behavior.

### Verification boundary
The baseline M24 recovery block, execution-history rebuild, comment creation/parser, decision-execution history helpers and initialization ordering were inspected. Patch 0023 and the M24 contract are stored on `blueprint-dev`. No new full-chain compile/SHA is claimed yet.

## Next P0 action
**Step 16 — audit M25 Dashboard + M26 Initialization/Cleanup boundaries.**

Required focus:
1. M25 must remain display-only and must not influence trading decisions or mutate state;
2. remove stale dashboard concepts such as score tiers, partial-close/breakeven status or deprecated basket-profit execution semantics;
3. verify M26 initializes all newly introduced protection/recovery/hash state deterministically and in safe order;
4. ensure restart initialization performs pair/magic validation before M24 recovery and does not wipe required recovery state after reconstruction;
5. audit deinitialization/timer cleanup for side effects on strategy or order lifecycle.

Do not merge into `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
