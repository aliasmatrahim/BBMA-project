# Repository Hygiene Audit + Deferred Cleanup Plan — PREP ONLY

Date: 2026-08-27  
Preparation branch: `p0-exec-id-persistence-fix`  
Status: **PREPARED / DOCUMENTATION-ONLY / NO PR OR ISSUE CLOSED**

## 1. Purpose

Classify the currently open GitHub pull requests and issues so repository cleanup can be performed later without accidentally removing evidence, runtime lineage or the active P0 blocker.

This audit does **not** close, merge, label, retarget or edit any open PR/issue. It does not modify EA source, lifecycle gates, strategy, SL/TP, MM/risk, canonical branches or runtime tooling.

Cleanup remains deferred until P0 #94 passes broker-runtime acceptance and the accepted v4.59 candidate is integrated/frozen canonically.

## 2. Snapshot

At audit creation:

- `p0-exec-id-persistence-fix` head before this record: `40f6985c680d4214daa8264a2b88e37e9f07c83c`;
- active P0 owner issue: #94;
- open PR count found: 8;
- open issue count found: 13;
- no open PR is currently approved as a canonical production merge path;
- multiple open PRs explicitly identify themselves as temporary, trigger-only or `Do not merge`;
- multiple open issues are historical one-shot runtime/diagnostic trigger artifacts.

## 3. Classification vocabulary

Use only these classifications in this audit:

- `KEEP_ACTIVE` — currently owns an unresolved project blocker or required live work.
- `KEEP_UNTIL_P0_FREEZE` — not an active production path, but retain temporarily for forensic/runtime lineage until P0 canonical freeze.
- `SUPERSEDED` — historical trigger/test path whose intended work has been replaced by later evidence or canonical implementation.
- `SAFE_TO_CLOSE_LATER` — no longer an active execution path; may be closed only after the cleanup gate below.
- `DO_NOT_MERGE` — PR is temporary infrastructure/trigger evidence and must never be merged as production source merely because it remains open.

`SUPERSEDED` does not mean “delete evidence”. Git history and issue/PR discussion remain part of the audit trail after closure.

## 4. Cleanup gate

Do not execute bulk cleanup before all of the following:

1. Issue #94 fresh v4.59 HFM demo runtime gate passes;
2. same-terminal restart recovery passes;
3. duplicate DecisionID/execution-hash protection passes;
4. accepted P0 delta is integrated from latest `d1-owner-dev`;
5. protected-surface regression passes;
6. exact integrated source compiles official MetaEditor 0E0W;
7. post-P0 source/build identity is recorded;
8. Issue #94 is closed with evidence references;
9. the new canonical candidate is frozen.

Only after this gate should the repository cleanup batch be executed.

---

# 5. Open pull-request classification

## PR #83 — D1O-03 observable runtime V2

Current body explicitly says: temporary observable runtime V2 and **Do not merge**.

Classification:
- `SUPERSEDED`
- `SAFE_TO_CLOSE_LATER`
- `DO_NOT_MERGE`

Reason: it is a temporary runtime validation path for older D1O work, not the current P0/canonical integration path.

## PR #82 — D1O-06 telemetry native compile

Body explicitly says temporary native MT4 compile validation and **Do not merge**.

Classification:
- `SUPERSEDED`
- `SAFE_TO_CLOSE_LATER`
- `DO_NOT_MERGE`

Reason: compile/telemetry validation artifact only; current runtime queue and post-P0 tooling plan supersede it as an active path.

## PR #81 — D1O-03 observable runtime fallback

Body explicitly says temporary observable runtime fallback and **Do not merge**.

Classification:
- `SUPERSEDED`
- `SAFE_TO_CLOSE_LATER`
- `DO_NOT_MERGE`

Reason: fallback dispatcher evidence, not a canonical source path.

## PR #77 — D1O-03 opportunity execution runtime smoke

Body explicitly says temporary dispatcher PR and **Do not merge**.

Classification:
- `SUPERSEDED`
- `SAFE_TO_CLOSE_LATER`
- `DO_NOT_MERGE`

Reason: hosted/trading-disabled runtime smoke infrastructure is historical evidence and cannot replace authenticated broker runtime.

## PR #15 — Dispatch CORE-V2-F2 implementation

Body identifies it as a sentinel PR used only to trigger an implementation workflow and says not to merge the sentinel file.

Classification:
- `SUPERSEDED`
- `SAFE_TO_CLOSE_LATER`
- `DO_NOT_MERGE`

Reason: one-shot dispatch sentinel; intended implementation lineage is already represented elsewhere in repository history.

## PR #10 — Trigger M17 runtime hotfix

Temporary draft PR used only to trigger an existing M17 runtime workflow.

Classification:
- `SUPERSEDED`
- `SAFE_TO_CLOSE_LATER`
- `DO_NOT_MERGE`

Reason: trigger-only artifact; current M17 baseline/runtime queue has moved beyond this trigger.

## PR #9 — RUN M17 RUNTIME FIX TOKEN 20260821

Body says temporary PR-target trigger and **Do not merge**.

Classification:
- `SUPERSEDED`
- `SAFE_TO_CLOSE_LATER`
- `DO_NOT_MERGE`

## PR #8 — Trigger M17 runtime hotfix workflow

Body says temporary trigger PR; actual fix is applied by base-branch workflow.

Classification:
- `SUPERSEDED`
- `SAFE_TO_CLOSE_LATER`
- `DO_NOT_MERGE`

### PR verdict

All 8 currently open PRs are temporary/trigger/validation artifacts and none is an approved production merge path. Keep them open only until the P0 canonical-freeze gate for forensic continuity, then close them in a dedicated hygiene batch with a consistent superseded/temporary explanation.

Do **not** merge any of these PRs during cleanup.

---

# 6. Open issue classification

## Issue #94 — P0: EXEC_ID persistence fails when broker strips oversized OrderComment

Classification:
- `KEEP_ACTIVE`

Reason: this is the current P0 acceptance owner. Code/static/native compile is already PASS, but fresh v4.59 HFM demo order + restart + duplicate-protection runtime validation remains pending.

Action: do not close until exact runtime acceptance and post-P0 canonicalization conditions are met.

## Issues #63, #62, #61, #60 — D1-02 MT4 runtime smoke trigger series

These are repeated one-shot/registered workflow attempts for hosted/trading-disabled D1-02 runtime smoke.

Classification for each:
- `SUPERSEDED`
- `KEEP_UNTIL_P0_FREEZE`
- `SAFE_TO_CLOSE_LATER`

Reason: later runtime architecture recognizes authenticated broker/demo evidence as the real acceptance authority. Hosted/disconnected smoke remains historical implementation/environment evidence only.

## Issue #49 — D1 Step1 native diagnostic retry

Classification:
- `SUPERSEDED`
- `KEEP_UNTIL_P0_FREEZE`
- `SAFE_TO_CLOSE_LATER`

Reason: bounded native diagnostic retry artifact; later native compile/runtime packages supersede it as an active task.

## Issues #12, #11, #7, #6 — M17 runtime fix trigger series

These are one-shot retry/trigger issues for the historical M17 runtime wiring path.

Classification for each:
- `SUPERSEDED`
- `KEEP_UNTIL_P0_FREEZE`
- `SAFE_TO_CLOSE_LATER`

Reason: trigger purpose is historical; current M17 structural-range implementation/runtime matrix is governed by later canonical records.

## Issues #4, #3, #2 — P3 PairID verification run records

These issues record historical PairID verification workflow runs, including static success and native compile failure in those old runs.

Classification for each:
- `SUPERSEDED`
- `KEEP_UNTIL_P0_FREEZE`
- `SAFE_TO_CLOSE_LATER`

Reason: they are run records, not current unresolved functional owners. Later P3/P0 execution-identity work and native compile evidence supersede these runs as the active verification path. Preserve them as historical evidence, but they need not remain open indefinitely.

### Issue verdict

Of the 13 currently open issues:

- 1 is `KEEP_ACTIVE`: #94;
- 12 are historical trigger/run artifacts classified `SUPERSEDED` and `SAFE_TO_CLOSE_LATER`, but cleanup is deliberately deferred until P0 canonical freeze.

---

# 7. Deferred cleanup execution plan

After the cleanup gate passes:

1. re-fetch all open PRs/issues first; do not assume this snapshot is still current;
2. verify no new comments or dependencies converted a historical item back into active work;
3. close temporary PRs #83, #82, #81, #77, #15, #10, #9, #8 without merging;
4. use a consistent close note such as: `Temporary/trigger validation path superseded by later canonical/runtime lineage; closed for repository hygiene. Historical evidence retained in GitHub.`;
5. re-check issue #94 is already closed by the P0 canonicalization process;
6. close historical issues #63, #62, #61, #60, #49, #12, #11, #7, #6, #4, #3, #2 with a similar superseded-history note;
7. do not delete branches/files merely as part of issue/PR cleanup unless a separate branch/file retention audit explicitly approves it;
8. record one closure audit listing every item actually closed and any item intentionally retained.

## 8. Explicit non-actions

This audit does not authorize:

- merging any temporary PR;
- deleting source branches;
- deleting workflow evidence/artifacts;
- changing `main` or `d1-owner-dev`;
- modifying `BBMA_EA.mq4`;
- closing #94 early;
- enabling D1TPW/C044/N3;
- treating hosted runtime as broker-runtime PASS.

## 9. Preparation verdict

**REPO HYGIENE PLAN READY / CLEANUP DEFERRED.**

Current actionable state:

- keep #94 active;
- retain all historical PR/issue artifacts until P0 canonical freeze;
- after freeze, close 8 temporary PRs without merge and review/close 12 superseded historical issues in one traceable cleanup batch.

No repository item was closed or merged by this preparation step.
