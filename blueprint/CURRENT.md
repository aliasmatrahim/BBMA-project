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
24. `blueprint/patches/0024-p0-step16-m25-m26-dashboard-init-cleanup.patch`
25. `blueprint/patches/0025-p0-step17-m27-end-to-end-orchestration-ownership.patch`

## Canonical compile-clean source
Path:
`blueprint/source/BBMA_EA.mq4`

SHA-256:
`30363d08437b85f253e6baf3e9c82af0d59d70727639ac0e6420a7677f975bc9`

Native MetaEditor result reported and verified from the user compile session:
**0 errors, 0 warnings**.

The pre-compile-repair Step 3 materialized SHA `e81b91a96d95b4446531b445a54c7d60ee5eb71d91646e98eac15ad8e1001da6` remains retained only as the deterministic input to the compile-repair layer. It is not the canonical current source SHA.

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
- `blueprint/contracts/M25_M26_DASHBOARD_INITIALIZATION_CONTRACT.md`
- `blueprint/contracts/M27_ORCHESTRATOR_END_TO_END_CONTRACT.md`
- `docs/references/SOURCE_INDEX.md`
- `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md`

## Complexity limiter
Limiter taxonomy remains LOCKED for the current blueprint-development cycle.

M01 BEGINNER; M02 BEGINNER; M03 INTERMEDIATE; M04 INTERMEDIATE; M05 INTERMEDIATE; M06 INTERMEDIATE; M07 INTERMEDIATE; M08 INTERMEDIATE; M09 INTERMEDIATE+; M10 INTERMEDIATE; M11 BEGINNER; M12 INTERMEDIATE+; M13 INTERMEDIATE+; M14 EXPERT-RESTRICTED; M15 EXPERT-RESTRICTED; M16 EXPERT-RESTRICTED; M17 INTERMEDIATE; M18 INTERMEDIATE; M19 EXPERT-RESTRICTED; M20 EXPERT-RESTRICTED; M21 INTERMEDIATE+; M22 EXPERT; M23 EXPERT-RESTRICTED; M24 EXPERT; M25 BEGINNER; M26 INTERMEDIATE; M27 EXPERT-RESTRICTED.

# P0 Architecture Repair

## Steps 1–17
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
- M24 recovery is restart-idempotent and hash-based without fabricating strategy identity;
- M25 is display-only and no longer presents PriorityTier as trading-quality authority;
- M26 initialization is fail-closed, recovery runs only after pair/magic ownership validation, and protection reference is equity-based;
- M27 is orchestration-only with one owner/one pass for pre-execution validation and exclusive emergency-liquidation state.

Locked end-to-end entry order:
`M06-M12 -> M13 -> M14 -> M15 -> M16 -> M17 -> M21 -> M19 -> M20 -> M22`

Locked tick/lifecycle order:
`M20 ManagePortfolio() -> M23 ManagePositions() -> emergency-latch gate -> strategy scan`

# P1 Integration Verification

## Step 1 — immutable baseline reconstruction and SHA verification
Status: **PASS**

Verified reconstructed SHA-256:
`e217816e95126857c1e7fa3fde1ac10ecc28f196a82eb51cb2f3625a6901aa00`

Verification run: GitHub Actions `31950155981`, conclusion `success`.

## Step 2 — ordered patch-chain conflict discovery
Status: **PASS**

## Step 3 — integration repair and full patch-chain materialization
Status: **PASS**

Verification run: GitHub Actions `31950925592`, conclusion `success`.

Pre-compile-repair source SHA-256:
`e81b91a96d95b4446531b445a54c7d60ee5eb71d91646e98eac15ad8e1001da6`

## Step 4 — architecture ownership / structural invariants
Status: **PASS**

Verification run: GitHub Actions `31951148538`, conclusion `success`.

## Compile repair passes 1–5
Status: **PASS — NATIVE METAEDITOR 0 ERRORS, 0 WARNINGS**

Evidence record:
`blueprint/P1_COMPILE_REPAIR_RECORD.md`

Compile repairs are restricted to MQL4 compatibility, cross-module signature alignment, deterministic snapshot field completion, and warning cleanup; no intentional BBMA strategy-semantic modification.

# P1 Finalization

## Step 1 — canonicalize compile-clean source
Status: **PASS**

Successful workflow:
`.github/workflows/p1-finalization-step1.yml`

Successful GitHub Actions run:
`31953336281`, conclusion `success`.

Canonical source:
`blueprint/source/BBMA_EA.mq4`

Canonical source SHA-256:
`30363d08437b85f253e6baf3e9c82af0d59d70727639ac0e6420a7677f975bc9`

Exact compile-repair transformation is reproducibly stored as:
- `blueprint/finalization/compile_repair.patch.gz.b64.part00`
- `blueprint/finalization/compile_repair.patch.gz.b64.part01`

## Step 2 — canonical post-compile architecture/invariant audit
Status: **PASS**

Successful workflow:
`.github/workflows/p1-finalization-step2-canonical-invariants.yml`

Successful GitHub Actions run:
`31953540304`, conclusion `success`.

Verified directly against canonical compile-clean source:
- SHA-256 exactly matches `30363d08437b85f253e6baf3e9c82af0d59d70727639ac0e6420a7677f975bc9`;
- M22 remains executor-only and consumes frozen lot;
- M27 retains single preflight ownership/order and one delegate from `ProcessPair`;
- tick lifecycle remains `M20 -> M23 -> emergency gate -> scan`;
- M25 remains display-only with no PriorityTier authority;
- M26 remains equity-reference based;
- M17 StopLevel snapshot and rejection propagation added during compile repair are present without breaking ownership;
- unsupported MQL4 array returns/reserved `input` parameter/struct aggregate initialization do not remain;
- all Module 01–27 markers remain present;
- structural brace/string/comment sanity passed.

## Current P1 status
**P1 RELEASE CANDIDATE ELIGIBLE**

The canonical source has now passed deterministic reconstruction, ordered patch integration, architecture-invariant verification, native MetaEditor compilation at **0 errors / 0 warnings**, canonicalization, and a second architecture/invariant audit directly against that compile-clean canonical source.

## Historical next action — P1 Finalization Step 3
This section is retained as historical context only. P1 subsequently progressed into recorded P2/P3 work; it is no longer the current next action.

Do not merge into `main` until the release-candidate/phase gate appropriate to the active development phase is explicitly recorded and approved.

# 2026-08-22 Project State Reconciliation

This section is the authoritative current-status overlay and supersedes stale phase/next-action wording above where there is a conflict.

## Reconciled status
- **P0:** complete at locked patch/contract level.
- **P1:** integration verification, compile repair, canonicalization and release-candidate records exist; no longer the active phase.
- **P2:** functional/cross-module audit and re-audit records exist through Step 18, with recorded fixes/workflows in repository. Individual P2 record files remain authoritative for their exact pass/fix status.
- **P3:** ACTIVE runtime-validation phase. Step 1–4 closure records exist. Step 5 source/compile/deployment records exist, but final live MT4 runtime closure remains pending under `blueprint/P3_STEP5_RUNTIME_CLOSURE_CHECKLIST.md` until Tests A–D are directly evidenced and E–F remain satisfied.
- **P3 PairID/Magic:** static validation PASS; local MetaEditor compile reported 0 errors / 0 warnings in `P3_PAIRID_VERIFICATION_RECORD.md`.
- **Strategy Core V2:** F1 MHV/MLV and F2 Extreme maturity are implemented with static regression PASS; F3 Re-Entry Type 1 and F4 standalone H1/H4 parent-owner remain specification-resolved with code patch/audit pending. Native MetaEditor compile/runtime traces remain pending for the new F1/F2 code.
- **F1 resolved lifecycle:** prior reversal-confirmed Extreme + TP-Wajib provenance -> structural loss of momentum -> most-extreme body + first move-away -> frozen body -> optional range-touch retest -> same-cycle direction progression; opposite reversal-confirmed Extreme atomically supersedes old-cycle MHV provenance.
- **Latest runtime source state observed during reconciliation:** branch head before the source-review tracking updates was commit `cdcaf8f849f357512be23f91bbb9184098fce574` — `P3 runtime fix: wire M17 market price before SLTP validation`.

## Canonical active queue
The authoritative work queue is:
`blueprint/MASTER_QUEUE.md`

Highest-priority next engineering gate:
**Implement/audit CORE-V2-F3 Re-Entry Type 1 next, then CORE-V2-F4 H4 parent-owner; preserve the implemented F1/F2 lifecycle contracts.**

After Core implementation/audit and re-run static Core verification:
**P3-M1 — Mode 1 Official BBMA Compliance Audit** remains the next end-to-end strategy gate.

Queued alongside/later according to `MASTER_QUEUE.md`:
- CORE-V2-F5 BB-flat classification repair and CORE-V2-F6 timing verification;
- opposite-direction / same-pair cycle integrity audit;
- sequential cumulative risk-budget admission verification;
- `REJ_INVALID_LOT` diagnostics (observability only);
- dashboard active-trade count refresh.

## Change control
This reconciliation changes project tracking/specification records only. It does not change EA strategy code, execution logic, risk logic, lot sizing, dashboard code, or broker behavior.
