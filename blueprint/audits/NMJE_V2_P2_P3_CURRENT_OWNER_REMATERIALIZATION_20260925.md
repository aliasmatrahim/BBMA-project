# NMJE V2 P2/P3 Current-Owner Rematerialization Audit — 2026-09-25

Status: **VALIDATED / P2-P3 SHADOW REMATERIALIZATION COMPLETE / READY FOR GOVERNANCE MERGE**

Latest verification: dedicated current-owner static workflow PASS (run `36077659180`) plus final rev003 native compile/regression/Strategy Tester evidence on G40.

## Base and identity
- Owner base: `d1-owner-dev@39843ce333ba939cf290271fc0c76cfffe452e44`
- Historical Build 4.96/PR #205: not merged or transplanted.
- Candidate build: `5.12`
- Build tag: `V512_NMJE_P2P3_SHADOW_20260925`
- Source revision: `NMJE_P2P3_SHADOW_003_20260925`
- Production EX4 SHA-256: `DECCE17D2BAC0694A9A25C4C66C7828DE520D7EFBA4A977FF6703C5B4EECD252`

## Scope
- P2 equal-eligibility coherence telemetry only.
- P3 latest closed-M5 snapshot metadata only.
- M15 remains the sole processing clock.
- P2/P3 cannot create, reject, rank, validate, risk-approve or execute.
- M5 is not a signal detector and has no execution authority.

## Current-owner rematerialization
- Current Build 5.11 source was used as the only implementation base.
- P1 identity substrate was not reapplied.
- Current Build 5.11 execution/risk/lifecycle code was not replaced.
- Historical V2 helper/persistence layer was not copied wholesale.

## Static checks performed
- Source diff is limited to `blueprint/source/BBMA_EA.mq4`.
- Build identity is unique and visible.
- P2/P3 helper declarations occur once each.
- Protected Priority/Invalidation path contains no P2/P3/M5 reference.
- M5 read is bound to `GetLatestClosedCandleTime(..., PERIOD_M5)` inside the M15-owned `ProcessPair` cycle.
- Final rev003 source SHA-256: `D80FA8D1A11A1FBAFFEC1F2E3FFF029DBAAB96BB58D89C29EDEBC25830379D1E`.

## Validation status
- Native MetaEditor compile: **PASS — 0 errors / 0 warnings** on exact final rev003 source; production EX4 SHA-256 `DECCE17D2BAC0694A9A25C4C66C7828DE520D7EFBA4A977FF6703C5B4EECD252`. Manual F7 was attempted through the active MetaEditor GUI; because that route did not emit an artifact, the final auditable compile was executed by the same native MetaEditor `/compile` path and its log is retained as `evidence/NMJE_V2_P2_P3_20260925/native_compile_rev003.log`.
- Targeted regression: **PASS** on rev003. P2/P3 are single-owner shadow helpers; latest-closed-M5 binding/closed-data guard PASS; P2 has no ordering/score/reject writes; P3 has no detector/risk/execution calls; protected comparator/M16/risk/preflight/order-send functions remain exact and free of NMJE/M5 references.
- Harness compile: **PASS — 0 errors / 0 warnings**; harness EX4 SHA-256 `0E3DD3738352F2C8AF788831C1E8A36DA027DCAE3EB1F8F01470CCEADD654D81`.
- Runtime/Strategy Tester: **PASS for targeted engineering runtime** on isolated GBPUSD M15, 2026-08-01..2026-09-01. Exact runtime identity is Build `5.12`, tag `V512_NMJE_P2P3_SHADOW_20260925`, rev `...003`; clean deinit; zero targeted fatal-runtime tokens; final report contains 14 trades (4 profit / 10 loss). Performance is descriptive only.
- Runtime evidence: `evidence/NMJE_V2_P2_P3_20260925/runtime_summary_rev003.json`; tester log/report hashes are bound there.
- Existing legacy N2/N3 v4.58 workflows are retired from PR gating and pinned to their immutable historical revisions via manual `workflow_dispatch`; they no longer misroute current-owner EA PRs.

## Exit decision
All scoped P2/P3 rematerialization exit gates are satisfied for merge: exact final source identity, native 0E/0W compile, targeted regression PASS, isolated Strategy Tester runtime/order coverage PASS, and no protected authority-path delta. P2 remains telemetry-only and P3 remains closed-M5 shadow context only; this merge does **not** activate P2 ordering, M5 execution authority, or any new Strategy-Core/risk/execution rule.
