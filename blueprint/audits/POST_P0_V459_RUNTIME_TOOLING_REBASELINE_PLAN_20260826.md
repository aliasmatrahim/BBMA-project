# Post-P0 v4.59 Runtime Tooling Re-baseline Plan

Date: 2026-08-26  
Preparation branch: `p0-exec-id-persistence-fix`  
Status: **PREPARED / EXECUTION BLOCKED UNTIL P0 #94 BROKER-RUNTIME PASS**

## 1. Purpose

Prepare the exact tooling transition from the frozen v4.58 broker-runtime package to the first post-P0 v4.59 integrated runtime package.

This record is preparation only. It does **not**:

- change `blueprint/source/BBMA_EA.mq4`;
- activate `EnableD1TPWLifecycle` or `EnableC044Lifecycle`;
- merge `p0-exec-id-persistence-fix` into `d1-owner-dev`;
- alter BBMA strategy, SL/TP, MM, risk, lifecycle semantics or module ownership;
- authorize R1 broker-runtime execution before P0 is accepted.

## 2. Current hard blocker

Issue #94 remains open with status:

`CODE + STATIC + NATIVE PASS / HFM FRESH-TRADE + RESTART RUNTIME VALIDATION PENDING`

Current P0 implementation identity:

- branch: `p0-exec-id-persistence-fix`;
- implementation commit: `03c4c3b90abbc6f669a89b1379218a26c5a57369`;
- source build marker: `Version 4.5.9 - P0 Execution Identity Persistence Fix`;
- `#property version "4.59"`;
- current branch source blob: `dc83e62748c93171d89a312e9f7a53c06d97e261`.

This identity is **not yet the final post-P0 canonical identity** because the P0 branch is not yet accepted/integrated onto the latest canonical `d1-owner-dev` history.

## 3. Why the old runtime package cannot simply be reused

The existing tooling is intentionally source-bound and must fail closed on source drift.

### Existing v4.58 builder

`blueprint/tools/v458_runtime_variant_builder.py` currently binds to:

- expected source blob `5c1b93d7783a00877cb7fd233673ca1ac1340151`;
- expected SHA-256 `6fd9eb52b63dee8861ebf205b1c031d80646b58e0b4941ef21ece9431fe6be5a`;
- build marker `Version 4.5.8 - D1 TP-Wajib Lifecycle Stage`;
- `#property version "4.58"`;
- exact lifecycle gate declarations.

### Existing v4.58 analyzer

`blueprint/tools/v458_runtime_analyzer.py` is also identity-bound to the older v4.58 runtime source and schema `BBMA_V458_RUNTIME_BUNDLE_V1`.

Therefore using either tool unchanged after P0 integration would be an invalid evidence chain. The correct action is a new v4.59 package with new exact source bindings while preserving approved test semantics.

## 4. Re-baseline trigger

Materialization of the v4.59 runtime package may start only after all of the following are true:

1. a fresh HFM demo order created by v4.59 reports `Persist=PASS` with durable local execution identity;
2. full EA/terminal restart recovers that same live ticket without `REC_IDENTITY_MISSING_FROZEN` caused only by broker-comment loss;
3. same DecisionID/execution hash does not create a duplicate ticket across restart;
4. runtime evidence is attached to Issue #94 and the issue is closed as completed;
5. P0 delta is synchronized/integrated with the latest `d1-owner-dev` without losing the latest audit/history;
6. protected-surface regression on the integrated source passes;
7. exact integrated source compiles in official MetaEditor at 0 errors / 0 warnings.

If any item fails, remain on the P0 defect path and do not materialize R1 tooling as production-ready evidence tooling.

## 5. Final source identity capture — mandatory first action after integration

Before changing any runtime tool, record from the exact integrated canonical head:

- canonical commit SHA;
- `blueprint/source/BBMA_EA.mq4` Git blob SHA;
- SHA-256 of exact MQ4 bytes;
- build marker;
- `#property version`;
- exact declarations and default values of `EnableD1TPWLifecycle` and `EnableC044Lifecycle`;
- exact EX4 SHA-256 after native compile.

The new builder/analyzer must bind to this **integrated identity**, never to the current provisional P0 branch identity above.

## 6. File-by-file materialization plan

Do not overwrite the historical v4.58 package. Preserve it as immutable evidence for the v4.58 baseline.

Create a parallel v4.59 package after the trigger gate:

| New file / surface | Source | Required change | Semantic boundary |
|---|---|---|---|
| `blueprint/tools/v459_runtime_variant_builder.py` | clone v458 builder | bind exact integrated v4.59 blob/SHA/build/version; preserve exact gate-only mutation model | no strategy change |
| `blueprint/tools/v459_runtime_analyzer.py` | clone v458 analyzer | bind new source identity/schema; preserve fail-closed classifications; index R1 matrix in greater detail | no strategy authority |
| `blueprint/runtime/V459_Runtime_Observer.mq4` | clone/review v458 observer | update package/build identity only where required; remain read-only | observer must never trade |
| `blueprint/runtime/collect_v459_runtime_bundle.ps1` | clone v458 collector | emit v459 manifest/schema and exact source/variant identities | evidence packaging only |
| `blueprint/runtime/v459_native_compile_matrix.ps1` | clone v458 compile matrix | compile baseline + R1_D1TPW + R2_C044 + observer against integrated identity | compile/test only |
| `blueprint/tests/test_v459_runtime_variant_builder.py` | clone v458 test | assert exact identity drift fails closed and only approved gate changes occur | no source mutation |
| `blueprint/tests/test_v459_runtime_analyzer.py` | clone/extend v458 test | preserve PASS/FAIL/INCOMPLETE/BLOCKED behavior; add P0-aware execution identity fixtures and R1 detailed cases | evidence validation only |
| optional workflow wrapper(s) | clone only if needed | new v459 naming/source binding; no automatic merge to canonical branch | CI orchestration only |

No v459 tool should silently fall back to v458 source identity.

## 7. Builder invariants

The new `v459_runtime_variant_builder.py` must:

1. read the canonical MQ4 from the exact Git blob, not a mutable working copy assumption;
2. verify exact Git blob + SHA-256 + build marker + property version;
3. verify exactly one OFF declaration for each lifecycle gate before mutation;
4. support only these approved profiles unless a later project decision explicitly adds another:
   - `baseline`: D1TPW OFF / C044 OFF;
   - `r1-d1tpw`: D1TPW ON / C044 OFF;
   - `r2-c044`: D1TPW OFF / C044 ON;
5. permit exactly zero semantic changes for baseline and exactly one lifecycle-gate change for R1/R2;
6. emit test-only metadata including canonical blob/SHA, variant SHA and changed declaration;
7. fail closed on any unexpected source/layout/version drift.

The builder must not patch P0 identity code, SL/TP logic, D1 logic, C044 logic, M17-M24 behavior or risk/MM behavior.

## 8. Analyzer invariants

The new `v459_runtime_analyzer.py` must preserve the v4.58 fail-closed evidence model and add awareness of the P0 execution-identity contract.

### Mandatory P0-aware evidence checks

For newly v4.59-created tickets the analyzer should be able to distinguish:

- local durable EXEC_ID persistence present;
- broker comment present/blank/replaced as secondary evidence only;
- exact-ticket recovery after restart;
- execution hash uniqueness across tickets;
- failure if a newly persisted ticket later becomes identity-missing solely because broker comment is absent;
- ambiguous order-send reconciliation behavior where relevant.

Broker `OrderComment()` must not be treated as the sole identity authority.

### R1 evidence checks to preserve/extend

At minimum preserve:

- checkpoint + restart recovery;
- same-ticket TP-Wajib latch then closed history;
- duplicate execution hash detection;
- hosted/disconnected/unauthenticated = `BLOCKED`;
- assertion references must resolve to actual raw evidence.

Extend/index the prepared `R1-00..R1-16` matrix without weakening the old checks.

## 9. Bundle schema and identity rules

Use a new schema name, proposed:

`BBMA_V459_RUNTIME_BUNDLE_V1`

Every bundle must carry:

- canonical commit/blob/SHA/build/version;
- profile and expected lifecycle gates;
- variant SHA-256;
- broker-connected/session-authenticated flags;
- raw log file list;
- optional assertions with resolvable raw evidence references.

An identity mismatch must make the bundle FAIL/invalid, never auto-migrate to a nearby source identity.

## 10. Observer rules

If `V459_Runtime_Observer.mq4` is materialized:

- it remains read-only;
- it cannot call `OrderSend`, `OrderClose`, `OrderModify`, or change GlobalVariables owned by EA runtime state;
- it may inspect/report state needed for exact-ticket checkpoint/restart/history evidence;
- it must expose enough data to distinguish D1TPW and C044 checkpoint families;
- package/build labels must clearly indicate v4.59/post-P0 evidence, not v4.58.

A static observer read-only check remains mandatory.

## 11. Native/self-test gate before any R1 broker run

The post-P0 package must report a complete autonomous gate equivalent to:

- `V459_RUNTIME_VARIANT_BUILDER_SELFTEST=PASS`;
- `V459_RUNTIME_ANALYZER_SELFTEST=PASS`;
- `OBSERVER_READ_ONLY_STATIC=PASS`;
- `METAEDITOR_0E0W_BASELINE=PASS`;
- `METAEDITOR_0E0W_R1_D1TPW=PASS`;
- `METAEDITOR_0E0W_R2_C044=PASS`;
- `METAEDITOR_0E0W_OBSERVER=PASS`;
- `V459_NATIVE_COMPILE_MATRIX=PASS`.

Any source identity mismatch, compile warning/error, unauthorized semantic diff, observer write capability or analyzer self-test failure blocks broker-runtime conclusions.

## 12. R1 variant semantic diff gate

For `r1-d1tpw`, automated diff/assertion must prove the generated MQ4 differs from the exact canonical integrated source only by:

`EnableD1TPWLifecycle = false` -> `true`

and that:

`EnableC044Lifecycle = false`

remains unchanged.

No P0 execution identity line may differ between baseline and R1 variant.

## 13. P0 protected-surface regression before R1

Before R1 broker testing, compare baseline integrated source against the accepted P0 delta and confirm:

- compact broker comment remains active;
- local GlobalVariable execution identity persistence remains active;
- duplicate lookup remains local-first;
- history/recovery remain local-first with broker fallback;
- `REC_NORMAL` still requires proven local persistence where applicable;
- MT4 error 128 remains ambiguous/fail-closed, not blindly retryable;
- BBMA detection, D1 owner, RE/REM/RRE/REE, SL/TP, MM and risk surfaces have no unapproved semantic delta from the intended integrated baseline.

This prevents the R1 test package from accidentally regressing the very P0 fix that makes restart evidence trustworthy.

## 14. R1 execution handoff

After the v4.59 package passes its native/self-test gate:

1. build the `r1-d1tpw` test-only variant;
2. record exact variant SHA-256;
3. attach to authenticated HFM/demo MT4 only;
4. attach V459 observer on a separate chart if used;
5. run the prepared `R1-00..R1-16` acceptance matrix;
6. collect bundles with the v459 collector;
7. analyze with the exact identity-bound v459 analyzer;
8. keep `INCOMPLETE`/`BLOCKED` as such; never force PASS;
9. create a dedicated R1 closure audit only after mandatory scenarios positively pass.

## 15. Branch and merge boundary

Recommended sequence after P0 runtime PASS:

1. synchronize P0 branch with latest `d1-owner-dev` audit/history;
2. integrate P0 cleanly into `d1-owner-dev` only after conflict/protected-surface review;
3. capture final integrated source identity;
4. materialize v459 runtime tooling against that exact identity;
5. run native/self-test matrix;
6. only then begin R1 authenticated broker runtime.

Do not merge to `main` merely to run R1.

## 16. Preparation verdict

**POST-P0 V4.59 TOOLING RE-BASELINE PLAN READY. MATERIALIZATION REMAINS BLOCKED BY P0 #94 RUNTIME ACCEPTANCE.**

The next executable project gate remains the fresh v4.59 HFM demo order + restart + duplicate-protection validation for Issue #94.