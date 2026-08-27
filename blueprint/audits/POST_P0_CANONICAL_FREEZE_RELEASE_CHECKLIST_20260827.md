# Post-P0 Canonical Freeze / Release Checklist — PREP ONLY

Date: 2026-08-27  
Preparation branch: `p0-exec-id-persistence-fix`  
Status: **PREPARED / DOCUMENTATION-ONLY / RELEASE BLOCKED UNTIL P0 #94 BROKER-RUNTIME PASS**

## 1. Purpose

Define the exact release gate for promoting the accepted v4.59 EXEC_ID repair into the next canonical `d1-owner-dev` baseline after P0 broker/demo runtime acceptance.

This checklist is not permission to merge now. It does not modify `blueprint/source/BBMA_EA.mq4`, does not change strategy, SL/TP, MM/risk, lifecycle or module ownership, and does not enable D1TPW, C044 or N3 execution policy.

The objective is to prevent a successful isolated hotfix from being canonicalized with hidden source drift, incomplete identity attribution, temporary workflow plumbing, stale runtime tooling, or unrecorded build identity.

## 2. Preparation snapshot

At checklist creation:

- canonical development branch: `d1-owner-dev`;
- canonical head: `5a1e7785f88c2ea1bf8f38917df413cb9cfcfce7`;
- P0 preparation branch head before this record: `8495780620abd4d3c7aef59da8e60fd6bd968121`;
- P0 production implementation commit: `03c4c3b90abbc6f669a89b1379218a26c5a57369`;
- P0 source build marker: `Version 4.5.9 - P0 Execution Identity Persistence Fix`;
- property version: `4.59`;
- isolated P0 source blob: `dc83e62748c93171d89a312e9f7a53c06d97e261`;
- Issue #94: OPEN;
- P0 code/static/native compile: PASS;
- HFM fresh-trade + restart + no-duplicate runtime acceptance: PENDING;
- `EnableD1TPWLifecycle=false`;
- `EnableC044Lifecycle=false`.

All identities above are preparation references. The final canonical identity must be freshly captured from the exact integrated source after integration from the then-current `d1-owner-dev` head.

## 3. Release-state definitions

Use these terms precisely:

### `P0_ACCEPTED`
The isolated v4.59 candidate has passed the required authenticated HFM demo fresh-trade, restart and duplicate-protection gate.

### `INTEGRATION_CANDIDATE`
The reviewed P0 production delta has been applied onto a fresh branch from the latest `d1-owner-dev`, with no wholesale hotfix-branch merge.

### `CANONICAL_CANDIDATE`
The integration candidate has passed protected-surface regression, exact-source official MetaEditor 0E0W, identity capture and required documentation/tooling checks.

### `CANONICAL_FROZEN`
`d1-owner-dev` points to the reviewed canonical candidate, its exact source/build identities are recorded, Issue #94 is closed with evidence references, and no opportunistic source edits are allowed before the next approved runtime stage.

`CANONICAL_FROZEN` does **not** mean D1TPW/C044 is enabled for production. Both staged lifecycle defaults remain OFF unless a separate explicit activation decision is approved later.

## 4. Gate CF-00 — P0 broker-runtime acceptance

Before any integration branch is created for canonicalization, require all of the following on a fresh v4.59 HFM demo order:

- [ ] EA identifies itself as `Version 4.5.9 - P0 Execution Identity Persistence Fix` / property `4.59`.
- [ ] Order is opened automatically by v4.59, not a legacy pre-fix ticket.
- [ ] `[P3S5][EXEC_ID]` reports `Persist=PASS`.
- [ ] Durable local identity is positively present (`Local=Y` or exact accepted post-P0 equivalent).
- [ ] Broker comment being blank/replaced does not invalidate local identity.
- [ ] Same live ticket is preserved for restart validation.
- [ ] Full EA/terminal restart is performed in the same MT4 installation.
- [ ] Exact ticket recovers without `REC_IDENTITY_MISSING_FROZEN` caused only by broker-comment loss.
- [ ] One DecisionID/execution hash does not create a second broker ticket across restart.
- [ ] Raw Experts/log evidence is attached or referenced in Issue #94.

If any required positive condition fails: **STOP. Keep `d1-owner-dev` unchanged. Fix only the isolated P0 branch.**

## 5. Gate CF-01 — fresh canonical-base capture

Immediately after P0 runtime PASS and before source integration:

- [ ] Re-fetch the current `d1-owner-dev` head.
- [ ] Record its commit SHA.
- [ ] Record current canonical `blueprint/source/BBMA_EA.mq4` Git blob.
- [ ] Review every canonical commit added since this checklist was prepared.
- [ ] Classify each new canonical change as docs/tooling/source.
- [ ] If any new EA-source change exists, perform a new conflict/ownership audit before applying P0.
- [ ] Do not assume the preparation-time head `5a1e7785...` is still current.

## 6. Gate CF-02 — fresh integration branch

Create a new integration branch from the then-current `d1-owner-dev` only after CF-00 and CF-01 PASS.

Required:

- [ ] Branch starts exactly from latest canonical head.
- [ ] Preserve canonical audits/documentation/history.
- [ ] Apply only the reviewed P0 production source delta.
- [ ] Do not merge `p0-exec-id-persistence-fix` wholesale.
- [ ] Do not import one-shot trigger tokens merely because they exist on the hotfix branch.
- [ ] Do not import temporary P0 workflows unless separately reviewed and intentionally retained as permanent tooling.
- [ ] Record the exact source diff between canonical base and integration candidate.

## 7. Gate CF-03 — allowed source-delta boundary

The integrated source may contain the approved P0 behavior only:

### Allowed
- compact broker execution hash comment;
- terminal-side durable execution identity persistence;
- local-first duplicate lookup/history/recovery;
- broker comment as secondary/fallback/migration evidence;
- `REC_NORMAL` guarded by successful durable identity state;
- ambiguous OrderSend/result reconciliation needed by the P0 fix;
- MT4 error 128 treated as ambiguous rather than blindly retryable;
- v4.59 header/property/dashboard/init identity synchronization.

### Not allowed without a separate explicit decision
- BBMA detector formula changes;
- Re-Entry/REM/RRE/REE semantic changes;
- D1/H4/H1/M15 owner/eligibility changes;
- M15 authority changes;
- M16 invalidation changes;
- M17 SL/TP geometry changes;
- M19/M20 risk/emergency changes;
- M21 sizing changes;
- M23 strategy-lifecycle semantic changes;
- default activation of D1TPW or C044;
- N3 trading-policy activation;
- new filters or indicators outside approved BBMA project governance.

Any unauthorized semantic delta: **RELEASE BLOCKED**.

## 8. Gate CF-04 — protected-surface regression

Run the prepared `POST_P0_PROTECTED_SURFACE_REGRESSION_MATRIX_20260826.md` against the exact integration candidate.

Minimum acceptance:

- [ ] M06–M12/M12N detector and owner semantics unchanged.
- [ ] M13 collector unchanged.
- [ ] M14 validator unchanged.
- [ ] M15 remains sole final new-entry authority.
- [ ] M16 invalidation unchanged.
- [ ] M17 SL/TP geometry unchanged.
- [ ] M21 final/frozen lot-sizing semantics unchanged.
- [ ] M19/M20 risk/portfolio/emergency authority unchanged.
- [ ] M22 delta is restricted to approved execution identity / ambiguous-result handling.
- [ ] M23 lifecycle strategy semantics unchanged.
- [ ] M24 delta is restricted to approved execution-identity persistence/recovery integration.
- [ ] D1TPW default gate remains OFF.
- [ ] C044 default gate remains OFF.
- [ ] N3 execution policy remains `NONE`.
- [ ] Closed-candle timing and M15 processing-clock invariants remain intact.

Focused path:

`M15 -> M16 -> M17 -> M21 -> M19 -> M20 -> M22 -> M24`

with M23 lifecycle sanity.

Any protected-surface FAIL blocks release.

## 9. Gate CF-05 — exact integrated identity capture

Before compile, record the exact candidate identity:

- [ ] integration branch name;
- [ ] integration commit SHA;
- [ ] `blueprint/source/BBMA_EA.mq4` Git blob SHA;
- [ ] exact MQ4 SHA-256;
- [ ] build marker;
- [ ] `#property version`;
- [ ] `EnableD1TPWLifecycle` declaration/value;
- [ ] `EnableC044Lifecycle` declaration/value;
- [ ] N3 execution-policy state;
- [ ] source-diff audit reference.

No later source edit may occur after identity capture without invalidating this gate and requiring recapture.

## 10. Gate CF-06 — official native compile

Compile the exact CF-05 source using official MT4 MetaEditor.

Require:

- [ ] 0 errors.
- [ ] 0 warnings.
- [ ] compile log identifies the exact candidate source/build.
- [ ] compiled EX4 is produced from that exact source.
- [ ] EX4 SHA-256 is recorded.
- [ ] compile workflow/run/job/artifact identifiers are recorded where applicable.
- [ ] no source modification occurs between source hashing and compile.

Any warning/error or source-identity mismatch blocks release.

## 11. Gate CF-07 — post-P0 runtime-tooling re-baseline

Follow `POST_P0_V459_RUNTIME_TOOLING_REBASELINE_PLAN_20260826.md` only after the exact canonical candidate identity exists.

Require:

- [ ] v4.59/post-P0 builder binds to the exact integrated source identity.
- [ ] analyzer binds to the intended post-P0 bundle/source identity and explicitly understands local durable EXEC_ID authority.
- [ ] broker comment remains secondary evidence in analyzer rules.
- [ ] observer remains read-only.
- [ ] collector/native matrix references v4.59 package identity, not the frozen v4.58 identity.
- [ ] baseline profile is D1TPW OFF / C044 OFF.
- [ ] R1 profile changes only D1TPW OFF -> ON.
- [ ] R2 profile changes only C044 OFF -> ON.
- [ ] builder/analyzer self-tests PASS.
- [ ] observer read-only static check PASS.
- [ ] native compile matrix for baseline/R1/R2/observer PASS 0E0W.

The old v4.58 builder/analyzer package remains immutable historical evidence and must not be silently rewritten into v4.59.

## 12. Gate CF-08 — canonical documentation reconciliation

Before updating `d1-owner-dev`:

- [ ] Create a dedicated P0 closure/canonicalization audit tied to exact commit/blob/MQ4 SHA/EX4 SHA/runtime evidence.
- [ ] Update `CURRENT.md` only where necessary to identify the new canonical source/build and P0 closure.
- [ ] Update `MASTER_QUEUE.md` only where necessary to move P0 from blocker to closed and release R1 as next formal runtime stage.
- [ ] Preserve historical v4.58 records as provenance; do not rewrite old evidence as though it were generated by v4.59.
- [ ] Update `MASTER_R1_R6_RUNTIME_EVIDENCE_INDEX_20260827.md` so R1 transitions from `BLOCKED` to `INCOMPLETE` only when its runtime collection actually starts.

## 13. Gate CF-09 — canonical branch update

Only after CF-00 through CF-08 PASS:

- [ ] Update `d1-owner-dev` to the reviewed canonical candidate using the project's approved integration method.
- [ ] Confirm `d1-owner-dev` now resolves to the exact reviewed commit.
- [ ] Re-fetch canonical source and verify its blob/SHA/build/gates match the release audit.
- [ ] Confirm no temporary trigger/workflow artifact was accidentally imported unless intentionally retained.
- [ ] Confirm `main` has not been casually advanced as part of this runtime-development canonicalization.

## 14. Gate CF-10 — Issue #94 closure

Close Issue #94 only after canonical branch verification succeeds.

Closure evidence must reference:

- [ ] fresh HFM v4.59 execution identity PASS;
- [ ] restart exact-ticket recovery PASS;
- [ ] no duplicate DecisionID/hash execution across restart;
- [ ] protected-surface regression PASS;
- [ ] official exact-source MetaEditor 0E0W;
- [ ] final canonical commit/blob/MQ4 SHA/EX4 SHA;
- [ ] post-P0 tooling re-baseline/native/selftest result or its explicitly sequenced completion record if project governance keeps tooling materialization immediately after canonical source update;
- [ ] canonical `d1-owner-dev` verification.

Issue closure without attributable broker-runtime evidence is forbidden.

## 15. Gate CF-11 — freeze

After Issue #94 closure and canonical verification:

Declare the new candidate `CANONICAL_FROZEN` and record:

- [ ] canonical commit;
- [ ] source blob;
- [ ] MQ4 SHA-256;
- [ ] EX4 SHA-256;
- [ ] build/version;
- [ ] lifecycle default gates;
- [ ] native compile identity;
- [ ] P0 closure audit;
- [ ] runtime/tooling package identity.

Freeze rule:

**No opportunistic EA-source edit while R1 broker-runtime evidence is being attributed.**

A new source patch requires either:

1. a concrete runtime defect with attributable evidence; or
2. a separately approved strategy/architecture decision.

## 16. Gate CF-12 — R1 handoff

After canonical freeze:

- [ ] Master tracker identifies R1 as the next formal stage.
- [ ] R1 uses the re-baselined v4.59 test package.
- [ ] R1 test-only profile is D1TPW ON / C044 OFF.
- [ ] Production/default canonical source remains D1TPW OFF / C044 OFF.
- [ ] `MinRRRatio=0` is used for targetless R1 acceptance where required by the existing test contract.
- [ ] Authenticated HFM demo/broker evidence is required; hosted/disconnected smoke is never runtime PASS.
- [ ] R1 follows `R1_D1_TPW_BROKER_RUNTIME_TEST_MATRIX_PREP_20260826.md` and the 115-case master tracker.

## 17. Rollback / stop conditions

Immediately stop canonicalization and leave/revert `d1-owner-dev` to the last proven canonical state if any of these occurs before final freeze:

- P0 runtime regression;
- duplicate execution identity;
- exact-ticket restart failure caused by broker-comment dependence;
- unexpected source conflict;
- protected-surface semantic drift;
- lifecycle gate accidentally ON in baseline;
- N3 policy becomes active;
- official compile warning/error;
- source/blob/SHA mismatch;
- builder/analyzer bound to wrong source identity;
- observer gains write/trade authority;
- evidence cannot be traced to exact build/ticket/logs.

Do not patch around a failed gate by weakening the acceptance criterion.

## 18. Release verdict template

Use exactly one of these conclusions:

### `RELEASE BLOCKED`
One or more required gates are not yet available or have failed.

### `CANONICAL CANDIDATE READY`
P0 runtime + integration + protected regression + exact-source 0E0W + identity/tooling/docs gates are complete, but `d1-owner-dev`/Issue #94 finalization is not yet finished.

### `CANONICAL FROZEN / R1 RELEASED`
`d1-owner-dev` points to the exact verified post-P0 baseline, Issue #94 is closed with evidence, build identities are frozen, and R1 may begin under its test-only profile.

## 19. Preparation verdict

**CHECKLIST READY. CURRENT VERDICT: `RELEASE BLOCKED` BY P0 #94 HFM FRESH-TRADE + RESTART + NO-DUPLICATE RUNTIME ACCEPTANCE.**

No EA source, lifecycle gate, canonical branch or strategy behavior is changed by this preparation record.


---

# 2026-08-27 Execution Reconciliation Overlay — IP-09

This overlay is the current execution status and supersedes the preparation verdict above where it conflicts. Preparation text remains immutable provenance.

| Gate | Status | Evidence |
|---|---|---|
| CF-00 P0 broker runtime | **PASS** | `P0_EXEC_ID_RUNTIME_PASS_RECORD_20260827.md`; ticket `484701907` / hash `7AADB1796BF36399` |
| CF-01 fresh base | **PASS** | `d1-owner-dev` base `5a1e7785f88c2ea1bf8f38917df413cb9cfcfce7` |
| CF-02 integration branch | **PASS** | `p0-v459-postpass-integration-20260827` created from exact base |
| CF-03 allowed source delta | **PASS** | source-bearing commit `aa74898ead8725f78141924f8bcb1725f0c113ca`; P0 identity/recovery scope only |
| CF-04 protected surfaces | **PASS** | `POST_P0_PROTECTED_SURFACE_REGRESSION_EXECUTION_20260827.md`; PS-01..PS-30 closed after IP-07 |
| CF-05 exact identity | **PASS** | blob `dc83e62748c93171d89a312e9f7a53c06d97e261` / repo-LF `07a69ccfca19e19d71c95ca891c66d953343261276d7722107624ce974830843` / Windows compile `0a42ee2e6c32810f655b592d8738f500e8b63b4e08c4c874e82452f75ce94b2e` / build 4.5.9 / property 4.59 / both lifecycle gates OFF |
| CF-06 official compile | **PASS** | run `33025004203`, job `98364184047`, artifact `9628390588`; EX4 `89821c5b1ae2d7c28a6cad7569cb2ced0e45090d0897451e0f61e0b46eb8944c`; 0E0W |
| CF-07 v4.59 tooling | **PASS** | run `33027817870`, artifact `9629222430`; builder/analyzer selftests + native matrix PASS |
| CF-08 documentation | **PASS at IP-09** | dedicated closure audit + CURRENT + MASTER_QUEUE + tracker + release identity reconciled in this execution |
| CF-09 canonical branch update | **PENDING** | IP-10 next; `d1-owner-dev` intentionally untouched by IP-09 |
| CF-10 Issue #94 closure | **PENDING** | issue remains OPEN until canonical verification at IP-11 |
| CF-11 freeze | **PENDING** | IP-12 only after #94 closure/canonical verification |
| CF-12 R1 handoff | **PENDING FINAL FREEZE** | tracker releases R1 from P0 blocker as INCOMPLETE/ready; collection waits canonical freeze |

Current verdict: **`CANONICAL CANDIDATE READY` / IP-10 NEXT**.

This status does not enable D1TPW/C044 in the canonical baseline and does not advance `main`.
