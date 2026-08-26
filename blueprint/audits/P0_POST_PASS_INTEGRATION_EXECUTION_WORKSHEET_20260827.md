# P0 Post-PASS Integration Execution Worksheet — PREP ONLY

Date: 2026-08-27  
Preparation branch: `p0-exec-id-persistence-fix`  
Status: **PREPARED / DOCUMENTATION-ONLY / DO NOT EXECUTE UNTIL ISSUE #94 BROKER-RUNTIME PASS**

## 1. Purpose

Provide the exact operational worksheet to execute immediately after P0 EXEC_ID broker-runtime acceptance passes. It converts the existing reconciliation plan, protected-surface matrix, tooling re-baseline plan and canonical freeze checklist into one ordered execution record.

This worksheet is **not authorization to integrate now**. It does not modify `blueprint/source/BBMA_EA.mq4`, does not create the integration branch, does not merge P0 into `d1-owner-dev`, does not activate D1TPW/C044, and does not alter BBMA strategy, SL/TP, MM/risk, lifecycle or module ownership.

## 2. Preparation snapshot

Fresh repository state at worksheet creation:

- canonical development branch: `d1-owner-dev`;
- canonical head: `5a1e7785f88c2ea1bf8f38917df413cb9cfcfce7`;
- P0 preparation branch head before this record: `a5f60b8e0a8648021856d701c529447bd16f69db`;
- P0 production implementation commit: `03c4c3b90abbc6f669a89b1379218a26c5a57369`;
- isolated P0 source build marker: `Version 4.5.9 - P0 Execution Identity Persistence Fix`;
- property version: `4.59`;
- isolated P0 source blob: `dc83e62748c93171d89a312e9f7a53c06d97e261`;
- Issue #94: OPEN;
- P0 code/static/native compile: PASS;
- authenticated HFM fresh-trade + restart + no-duplicate acceptance: PENDING;
- default lifecycle gates: D1TPW OFF / C044 OFF.

All preparation-time branch identities must be refreshed again when this worksheet becomes executable.

## 3. Execution trigger — hard gate

Do not start Section 4 until Issue #94 contains attributable runtime evidence proving all of the following:

- [ ] fresh order created by v4.59 P0-fixed EA;
- [ ] `[P3S5][EXEC_ID]` reports `Persist=PASS`;
- [ ] durable local identity is present (`Local=Y` or exact accepted equivalent);
- [ ] broker comment may be blank/replaced without invalidating identity;
- [ ] same ticket is kept live through full EA/terminal restart in the same MT4 installation;
- [ ] recovery reconstructs the exact same ticket without identity-missing freeze caused only by broker-comment loss;
- [ ] no second ticket is created for the same DecisionID/execution hash across restart;
- [ ] raw logs/screenshots/bundle references are attached to Issue #94.

If any item fails: **STOP. Keep `d1-owner-dev` unchanged and fix only the isolated P0 branch.**

---

# 4. Step IP-01 — capture fresh canonical base

Execution record:

- execution date/time: `________________`
- current `d1-owner-dev` head: `________________`
- current canonical source blob: `________________`
- current canonical MQ4 SHA-256: `________________`
- current build marker/property version: `________________`

Actions:

- [ ] fetch current `d1-owner-dev` head;
- [ ] compare it with preparation-time head `5a1e7785...`;
- [ ] list every commit added since preparation;
- [ ] classify each as docs / tooling / source;
- [ ] if any EA-source commit exists, stop and perform a new conflict/ownership audit before applying P0;
- [ ] confirm canonical strategy source remains traceable and internally consistent.

Verdict: `PASS / FAIL / BLOCKED`  
Evidence: `________________`

# 5. Step IP-02 — create fresh integration branch

Branch name to record: `________________`

Requirements:

- [ ] branch created from exact IP-01 `d1-owner-dev` head;
- [ ] no branch is created from the old hotfix head merely for convenience;
- [ ] canonical documentation/audit history is preserved;
- [ ] integration branch identity recorded before any source delta is applied.

Base commit: `________________`  
New integration branch head before P0 delta: `________________`

Verdict: `PASS / FAIL / BLOCKED`

# 6. Step IP-03 — apply only reviewed P0 production delta

Allowed production scope:

1. compact broker comment `BBMA|H:<16hex>`;
2. terminal-side durable execution identity persistence/cross-validation;
3. local-first duplicate lookup/history rebuild/recovery;
4. broker comment as secondary/fallback evidence only;
5. `REC_NORMAL` requires successful durable local identity where applicable;
6. error 128 remains ambiguous/fail-closed rather than blindly retryable;
7. v4.59 build/runtime identity synchronization.

Forbidden during integration:

- [ ] no BBMA detector rewrite;
- [ ] no M13/M14/M15 strategy-selection change;
- [ ] no M16 strategy-invalidation change;
- [ ] no M17 SL/TP geometry change;
- [ ] no M19/M20 risk semantics change;
- [ ] no M21 MM/lot semantics change;
- [ ] no M23 lifecycle strategy-semantic change;
- [ ] no D1/D1O semantic change;
- [ ] no C044/D1TPW default activation;
- [ ] no opportunistic dashboard/feature patch;
- [ ] no wholesale merge of temporary P0 workflows/trigger plumbing.

Applied source commit: `________________`

Verdict: `PASS / FAIL / BLOCKED`

# 7. Step IP-04 — changed-file classification

Record all files changed by the integration candidate:

| Path | Classification | Keep? | Reason |
|---|---|---|---|
| `blueprint/source/BBMA_EA.mq4` | production source | `YES` | reviewed P0 execution/recovery delta |
| `________________` | `________________` | `YES/NO` | `________________` |

Rules:

- temporary one-shot trigger files are excluded unless separately approved as permanent infrastructure;
- old v4.58 evidence/tooling is not rewritten in place merely to look current;
- permanent audit evidence may be retained if it improves traceability;
- every retained non-source file needs an explicit reason.

Verdict: `PASS / FAIL / BLOCKED`

# 8. Step IP-05 — protected-surface regression

Run the prepared `POST_P0_PROTECTED_SURFACE_REGRESSION_MATRIX_20260826.md` against the exact integration candidate.

Minimum mandatory path:

`M15 -> M16 -> M17 -> M21 -> M19 -> M20 -> M22 -> M24`

with M23 lifecycle sanity and upstream detector/owner invariants.

Required outcome:

- [ ] P0 execution/recovery changes present;
- [ ] M06-M12/M12N semantics unchanged;
- [ ] M13/M14 unchanged;
- [ ] M15 remains sole final new-entry authority;
- [ ] M16 invalidation unchanged;
- [ ] M17 SL/TP geometry unchanged;
- [ ] M21 lot sizing semantics unchanged;
- [ ] M19/M20 risk/emergency semantics unchanged;
- [ ] M23 strategy lifecycle semantics unchanged;
- [ ] M24 change limited to intended identity persistence/recovery integration;
- [ ] D1TPW remains OFF;
- [ ] C044 remains OFF;
- [ ] N3 remains firewalled at `execution_policy=NONE`;
- [ ] no strategy/risk/MM drift found outside the allowed P0 delta.

Regression report path/commit: `________________`

Verdict: `PASS / FAIL / BLOCKED`

# 9. Step IP-06 — capture exact integration identity

Capture **before compile**:

- integration commit SHA: `________________`
- source Git blob SHA: `________________`
- exact MQ4 SHA-256: `________________`
- build marker: `________________`
- property version: `________________`
- D1TPW default: `OFF / OTHER: ________`
- C044 default: `OFF / OTHER: ________`

Any identity mismatch with the reviewed file invalidates later compile/runtime evidence.

Verdict: `PASS / FAIL / BLOCKED`

# 10. Step IP-07 — official MetaEditor compile

Compile the exact IP-06 MQ4 source using official MT4 MetaEditor.

Required:

- [ ] errors = 0;
- [ ] warnings = 0;
- [ ] compile log references exact source identity;
- [ ] generated EX4 SHA-256 recorded;
- [ ] no source edit occurs between IP-06 identity capture and accepted compile without restarting IP-05/IP-06.

Compile log/artifact: `________________`

EX4 SHA-256: `________________`

Verdict: `PASS / FAIL / BLOCKED`

# 11. Step IP-08 — post-P0 v4.59 runtime tooling re-baseline

Only after IP-07 PASS, materialize the prepared post-P0 tooling plan against the exact integration identity.

Expected parallel package:

- `v459_runtime_variant_builder.py`;
- `v459_runtime_analyzer.py`;
- reviewed v4.59 observer;
- v4.59 collector/native compile matrix/selftests as required.

Required invariants:

- [ ] exact new canonical blob/SHA/build bindings;
- [ ] baseline profile = D1TPW OFF / C044 OFF;
- [ ] R1 profile = D1TPW ON / C044 OFF only;
- [ ] R2 profile = D1TPW OFF / C044 ON only;
- [ ] builder cannot patch execution identity/strategy/SLTP/risk code;
- [ ] analyzer includes P0 durable local EXEC_ID/restart/no-duplicate checks;
- [ ] observer remains read-only;
- [ ] old v4.58 package remains immutable historical evidence;
- [ ] builder/analyzer selftests PASS;
- [ ] native compile matrix PASS / 0E0W.

Tooling commit(s): `________________`

Verdict: `PASS / FAIL / BLOCKED`

# 12. Step IP-09 — canonical documentation reconciliation

Update only after source + compile + tooling gates pass:

- [ ] dedicated P0 closure/integration audit created;
- [ ] exact commit/blob/MQ4 SHA/EX4 SHA/build identity recorded;
- [ ] `CURRENT.md` updated only where necessary;
- [ ] `MASTER_QUEUE.md` updated to mark P0 closure and release R1;
- [ ] master R1–R6 tracker changes P0 to PASS and R1 from BLOCKED to INCOMPLETE/ready for collection;
- [ ] no later stage is prematurely marked PASS;
- [ ] freeze/release checklist is completed with evidence references.

Documentation commit(s): `________________`

Verdict: `PASS / FAIL / BLOCKED`

# 13. Step IP-10 — update canonical development branch

Precondition: IP-01 through IP-09 all PASS.

Required:

- [ ] reviewed canonical candidate is the exact commit being promoted;
- [ ] `d1-owner-dev` moves to that exact candidate without unrelated changes;
- [ ] post-update fetch confirms expected commit SHA;
- [ ] post-update source fetch confirms expected Git blob/SHA/build;
- [ ] D1TPW/C044 remain OFF in canonical default source;
- [ ] no merge to `main` is implied or performed by this step.

Expected canonical commit: `________________`

Observed post-update `d1-owner-dev`: `________________`

Verdict: `PASS / FAIL / BLOCKED`

# 14. Step IP-11 — close Issue #94

Close #94 only after canonical update and identity verification.

Closure evidence must include:

- [ ] original failure summary;
- [ ] fresh v4.59 HFM demo PASS ticket evidence;
- [ ] restart recovery evidence;
- [ ] no-duplicate evidence;
- [ ] integration commit/blob/MQ4 SHA;
- [ ] official compile 0E0W;
- [ ] EX4 SHA-256;
- [ ] protected-surface regression PASS;
- [ ] canonical `d1-owner-dev` post-update identity;
- [ ] note that broker comment is secondary and same-terminal GlobalVariables are the current persistence scope.

Issue closure comment/reference: `________________`

Verdict: `PASS / FAIL / BLOCKED`

# 15. Step IP-12 — freeze canonical baseline

After #94 closes:

- [ ] mark the exact v4.59 post-P0 canonical identity as frozen;
- [ ] no opportunistic strategy/source patch before R1 unless a concrete new defect is found and triaged;
- [ ] old temporary hotfix/trigger plumbing is not merged into canonical history by default;
- [ ] repo hygiene cleanup may now be executed according to the deferred cleanup audit;
- [ ] R1 becomes the next formal runtime stage;
- [ ] R1 test variant may enable D1TPW only in the dedicated test profile;
- [ ] canonical/default D1TPW remains OFF until an explicit later activation decision;
- [ ] canonical/default C044 remains OFF until its own runtime/activation decision.

Freeze audit/reference: `________________`

Verdict: `PASS / FAIL / BLOCKED`

# 16. Final handoff record

Complete only after IP-01..IP-12 PASS.

| Identity | Value |
|---|---|
| Canonical `d1-owner-dev` commit | `________________` |
| MQ4 Git blob | `________________` |
| MQ4 SHA-256 | `________________` |
| Build marker / property version | `________________` |
| EX4 SHA-256 | `________________` |
| Issue #94 | `CLOSED / ________` |
| Protected regression | `PASS / ________` |
| v4.59 tooling re-baseline | `PASS / ________` |
| D1TPW default | `OFF / ________` |
| C044 default | `OFF / ________` |
| Next formal stage | `R1 D1 TP-Wajib broker runtime` |

## 17. Stop conditions

At any point, stop canonicalization and leave `d1-owner-dev` unchanged if:

- fresh P0 runtime evidence is incomplete/failed;
- canonical branch moved with an unreviewed EA-source edit;
- P0 delta cannot be isolated cleanly;
- protected-surface regression finds unauthorized semantic drift;
- exact MetaEditor compile is not 0E0W;
- source/blob/SHA/build/EX4 identities do not reconcile;
- tooling silently targets the old v4.58 identity;
- D1TPW/C044 is unintentionally enabled in canonical default source;
- documentation claims PASS without raw attributable evidence.

## 18. Preparation verdict

**POST-P0 INTEGRATION EXECUTION WORKSHEET READY. EXECUTION REMAINS BLOCKED BY ISSUE #94 BROKER-RUNTIME ACCEPTANCE.**

No source, lifecycle gate, canonical branch, PR state or issue state is changed by this worksheet.