# NMJE V2 P2/P3 Current-Owner Rematerialization Audit — 2026-09-25

Status: **DRAFT / IMPLEMENTATION PATCH PREPARED / VALIDATION BLOCKED**

## Base and identity
- Owner base: `d1-owner-dev@39843ce333ba939cf290271fc0c76cfffe452e44`
- Historical Build 4.96/PR #205: not merged or transplanted.
- Candidate build: `5.12`
- Build tag: `V512_NMJE_P2P3_SHADOW_20260925`
- Source revision: `NMJE_P2P3_SHADOW_001_20260925`

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
- Local source hash for PR head: `0B6F754AAFEFB12A219B9C7C2C719E67E951C0DB84C49C19D7DAFF086F053C9B`.

## Validation status
- Native MetaEditor compile: **BLOCKED / NO VERIFIABLE ARTIFACT**. MetaEditor was invoked against the exact PR source using absolute, repository-relative and `MQL4\\Experts` working-directory paths. Each process returned exit code 0, but no candidate `.ex4` or compile log was produced; therefore no compile PASS is claimed.
- Static project suite: **NOT RUN / repository checkout unavailable locally**.
- Targeted regression: **NOT RUN**.
- Runtime/Strategy Tester: **NOT RUNTIME VERIFIED**. Existing MT4 terminal is present, but the PR source was not compiled into a verifiable `.ex4`.
- Merge/activation: **NOT AUTHORIZED until required evidence is attached**.
- Existing PR workflows: **MISROUTED**. N2/N3 checked out `d1-owner-dev` and failed legacy v4.58 marker checks; their actual selftests were skipped.

## Exit decision
This patch remains review-only. The remaining genuine gate is a verifiable MetaEditor compile artifact/log followed by targeted regression and MT4/G40 runtime evidence. No merge or activation is justified from the current evidence.
