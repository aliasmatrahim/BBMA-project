# NMJE N3 4-TF Baseline Re-Lock — 2026-09-04

## Scope

This re-lock supersedes the implementation/evidence references in `NMJE_N3_4TF_BASELINE_LOCK_20260828.md` after PR #97 was reconciled with the current `d1-owner-dev` implementation state. It does not merge PR #97 and does not activate any dormant strategy or execution authority.

## Locked code lineage

- PR: #97 `nmje-n3-hardening-dev` -> `d1-owner-dev`
- Reconciled implementation base: `2ea85060696d96b9e892505693d07d8b2cffbff0`
- Locked source commit: `13f6a95c5065a00e4e451503171eca7e700864c6`
- EA identifier: `Version 4.6.2 - N3 D1 Epoch + F7 Reconcile`
- MQL property: `4.62`
- `main`: untouched

## Locked topology and authority

The deterministic N3 baseline remains exactly:

`D1 -> H4 -> H1 -> M15`

- D1 remains the strategic owner.
- H4 remains higher-owner / journey context.
- H1 remains setup context.
- M15 remains the sole processing and final-decision clock.
- M15/M16 retain entry/revalidation authority under the active architecture.
- M22 remains the sole `OrderSend` owner.
- NMJE relation/provenance remains diagnostic/shadow-only in this staging baseline.
- M5 is not part of this baseline.

## D1 owner epoch invariant

- `SourceCandleTime` is the latest valid closed-D1 snapshot time.
- `EpochStartCandleTime` is the stable start time of the current canonical D1 owner epoch.
- Ordinary closed-D1 refreshes may advance `SourceCandleTime` without rotating D1 owner identity.
- `NMJE_D1OwnerEventID` is bound to the stable epoch rather than the moving snapshot.
- Replay/recovery tests remain fail-closed on identity/provenance mismatch.

## Reconciliation firewall

Current `d1-owner-dev` F7 implementation was retained where unrelated to N3 authority. The staging branch explicitly keeps the following OFF:

- NMJE execution gate / independent NMJE rejection authority: absent/disabled
- `EnableD1TPWLifecycle=false`
- `EnableC044Lifecycle=false`

The d1-side `BlockNMJEConflict` / `BlockNMJEBuilding` execution-gate path and `REJ_NMJE_RELATION` rejection path were not carried into the locked N3 staging authority boundary.

## Verification evidence

Exact locked source `13f6a95c5065a00e4e451503171eca7e700864c6`:

- Local repository `nmje_n3_static_guard.ps1`: PASS
- GitHub N3 Step5 D1 owner epoch materializer, run `33888537175`: PASS
- GitHub N3 NMJE staging selftest, run `33888536341`: PASS
  - authority regression: PASS
  - identity-domain regression: PASS
  - replay regression: PASS
  - recovery/fail-closed regression: PASS
  - D1 owner epoch static regression: PASS
  - parent/shadow provenance regression: PASS
- GitHub NMJE N3 static guard, run `33888536179`: PASS
- Local native MT4 MetaEditor compile: `Result: 0 errors, 0 warnings, 527 msec elapsed`
- Local compiler: `C:\Program Files (x86)\MetaTrader 4\metaeditor.exe`
- Local compile log: `C:\Users\Afiq Mat Rahim\Documents\BBMA_compile_pr97_v462\compile_installed.log`
- GitHub native compile run `33888536148`: static precompile gate PASS; official-MetaEditor acquisition was still in progress at lock preparation time. This run is not counted as a compile PASS unless it completes successfully.

## Safety / release boundary

- PR #97 remains DRAFT / NO MERGE / NO ACTIVATION.
- This is a deterministic 4-TF strategy-core/provenance baseline lock, not a release approval.
- No NMJE execution authority, D1TPW, C044, M5, W1, M30, or primary M1 activation is authorized.
- No final Strategy Tester / live broker acceptance is claimed by this lock.
- F7 runtime evidence remains a separate runtime-validation responsibility.

## Issue #101 handoff

Issue #101 may proceed only in an isolated M5 accuracy/research workstream stacked from this locked source lineage.

The existing PR #102 / `nmje-v2-m5-dev` history is not a safe continuation base because its P10 commit `d50178abcb74d2c9e8275c4010a8eb25cf111eb8` is the first demonstrated source-corruption boundary and the current later head still lacks the MODULE 17 end marker. Preserve that branch as evidence; do not merge/rebase its corrupted source into this baseline.

Any rebuilt M5 workstream must preserve the Issue #101 authority rules: M5 is closed-candle context/refinement only, M15 remains the sole processing/final-decision clock, and no M5/NMJE rule may create/reject/rank/execute/delay trades without a separate explicit strategy-policy decision and evidence.
