# P0 EXEC_ID Branch Reconciliation + Post-Runtime Merge Plan — 2026-08-26

## Purpose
Prepare a safe integration path for the isolated execution-identity hotfix without changing the currently frozen canonical strategy source before broker/demo runtime acceptance.

## Snapshot
- Canonical development branch: `d1-owner-dev`
- Canonical head at audit time: `5a1e7785f88c2ea1bf8f38917df413cb9cfcfce7`
- Canonical head message: `Audit: reconcile SL/TP families against latest 4.5.8 baseline`
- P0 fix branch: `p0-exec-id-persistence-fix`
- P0 fix head before this audit record: `03c4c3b90abbc6f669a89b1379218a26c5a57369`
- P0 build: `Version 4.5.9 - P0 Execution Identity Persistence Fix`
- Merge base: `ffc102f884eede745d41a94c2a5ad9dc7e180ebe`
- Git comparison: P0 branch is **ahead 8 / behind 1** relative to `d1-owner-dev`.

## Divergence classification
The single commit present on `d1-owner-dev` but absent from the P0 branch is the SL/TP reconciliation audit commit `5a1e7785...`. Its diff adds `blueprint/audits/SLTP_RECONCILIATION_MATRIX_20260826.md`; it does not modify `blueprint/source/BBMA_EA.mq4`.

Therefore the current divergence is not a competing EA-source edit. The P0 source delta still descends from the same v4.58 EA source lineage, while the canonical branch has moved only by a documentation/audit commit.

## P0 branch delta inventory
Current compare against `d1-owner-dev` shows these P0-side changed files:
1. `.github/workflows/p0-exec-id-final-native-v2.yml` — temporary/native validation plumbing.
2. `.github/workflows/p0-exec-id-persistence-fix.yml` — temporary patch/native validation plumbing.
3. `blueprint/.run-p0-exec-id-final-v2` — one-shot trigger token.
4. `blueprint/source/BBMA_EA.mq4` — actual runtime fix, build v4.59.
5. `blueprint/tools/p0_exec_id_persistence_fix.py` — deterministic patch helper.
6. `blueprint/tools/p0_exec_id_persistence_fix_v2.py` — patch compatibility helper.
7. `blueprint/tools/p0_exec_id_runtime_identity_sync.py` — build-identity sync helper.

## Actual EA-source scope inspected
The v4.59 source change is execution/recovery infrastructure, not a BBMA strategy rewrite. The inspected delta includes:
- compact broker comment `BBMA|H:<SHORT_HASH(DecisionID)>` instead of long full metadata;
- terminal-side durable execution identity persistence and lookup;
- local identity first for duplicate/recovery/history reconstruction, broker comment as secondary/fallback evidence;
- post-send identity state no longer allowed to report normal recovery when durable identity persistence failed;
- MT4 error 128 handled as ambiguous/fail-closed rather than blindly retryable;
- runtime/header/dashboard/init identity synchronized to v4.59.

Both staged lifecycle gates remain OFF in the v4.59 source:
- `EnableC044Lifecycle = false`
- `EnableD1TPWLifecycle = false`

No intentional change is authorized here to BBMA detection, M13/M14/M15 selection semantics, M16 strategy invalidation, M17 SL/TP geometry, M19/M20 risk, M21 money management, or D1/C044 strategy lifecycle semantics.

## Existing verification status
P0 isolated branch has already passed:
- static fail-closed verification;
- official native MT4 MetaEditor compile: **0 errors / 0 warnings**;
- final native workflow and EX4 evidence generation.

Still pending before integration:
1. fresh trade opened by v4.59 on authenticated HFM demo;
2. immediate execution identity persistence PASS;
3. restart EA/terminal while that fresh trade remains live;
4. recovery must not become `REC_IDENTITY_MISSING_FROZEN` solely because broker comment is blank/mutated;
5. same DecisionID must not execute twice across restart.

Issue #94 remains the acceptance owner until those broker/runtime gates pass.

# Post-runtime integration plan

## Gate A — runtime acceptance first
Do **not** integrate P0 into `d1-owner-dev` until the fresh-trade + restart checks above PASS. If runtime evidence fails, keep the canonical branch untouched and fix only the isolated P0 branch.

## Gate B — integrate from the latest canonical head, not by wholesale branch merge
After runtime PASS:
1. create a fresh integration branch from the then-current `d1-owner-dev` head;
2. preserve the canonical SL/TP reconciliation audit and any later documentation-only canonical commits;
3. apply the exact v4.59 EA-source execution/recovery delta onto that latest canonical head;
4. do not merge the temporary trigger token or one-shot workflow plumbing merely because it exists on the hotfix branch;
5. retain only permanent tooling/evidence files that are useful for reproducibility and explicitly approved for the canonical branch.

Reason: the P0 branch contains validation plumbing in addition to the production source fix. A clean source-focused integration makes the canonical history easier to audit and avoids importing temporary dispatch artifacts.

## Gate C — protected-surface regression on the integrated source
Before updating `d1-owner-dev`, verify at minimum:
- M06-M12 / M12N detector and owner semantics unchanged;
- M13 collector and M14 validator unchanged;
- M15 sole final entry authority unchanged;
- M16 strategy invalidation unchanged;
- M17 SL/TP decision geometry unchanged;
- M21 frozen lot sizing unchanged;
- M19/M20 risk and portfolio gates unchanged;
- M22 changes limited to execution identity / ambiguous-send reconciliation;
- M23 lifecycle strategy semantics unchanged;
- M24 changes limited to execution-identity persistence/recovery integration;
- D1TPW and C044 gates remain OFF;
- build identity is unique and internally consistent.

Focused cross-module regression path:
`M15 -> M16 -> M17 -> M21 -> M19 -> M20 -> M22 -> M24`
with lifecycle sanity through M23.

## Gate D — compile
Compile the exact integrated source with official MT4 MetaEditor and require:
**0 errors / 0 warnings**.

The compiled EX4 and compile log must correspond to the exact integrated source blob/commit that will become the new canonical runtime candidate.

## Gate E — canonicalization
If Gates A-D PASS:
1. update `d1-owner-dev` to the reviewed integrated commit;
2. record the new source blob/SHA-256 and build identity in a dedicated closure audit;
3. update `CURRENT.md` / `MASTER_QUEUE.md` only where necessary to show P0 closed and runtime queue resumed;
4. close Issue #94 as completed with runtime evidence references;
5. freeze the new candidate before proceeding to R1 D1 TP-Wajib runtime closure.

## Next queue after P0 closure
Resume the existing broker/runtime order:
1. R1 — D1 TP-Wajib lifecycle runtime gate;
2. R2 — C044 runtime gate;
3. R3 — D1 owner / D1O runtime identity and dedup matrix;
4. R4 — validation-to-order timing + M17 live SL geometry;
5. R5 — TradeLock + cumulative risk + remaining P3 runtime tests;
6. R6 — N2 real forward identity/outcome chain; N3 execution policy remains `NONE`.

## Decision
**SAFE TO PREPARE / NOT SAFE TO MERGE YET.**

The branch divergence is understood and currently non-conflicting at the canonical EA-source level. The remaining blocker is broker/demo fresh-trade + restart acceptance of v4.59. No further strategy-source change is justified by this reconciliation audit.