# D1TPW Build 4.87 Checkpoint Atomicity Validation

Date: 2026-09-20
Issue: #210
Branch: `fix/d1tpw-checkpoint-atomicity-210`
Base: `d1-owner-dev@8da9dae0801f414f8d4c659a226ff58451cca7e6`
Status: **VERIFIED IN SCOPED DRAFT BRANCH / NOT MERGED / NOT ACTIVATED**

## Classification

**CONFIRMED BUG — FIXED IN SCOPED BRANCH.**

The prior D1TPW checkpoint writer could report success from key presence even when a replacement write partially failed over an older checkpoint. A stale cursor/latch/frozen value could therefore remain loadable after restart.

This is engineering persistence/recovery integrity. No BBMA Strategy-Core rule changes.

## Fix boundary

Build identity:
- `4.87`
- `V487_D1TPW_CHECKPOINT_ATOMICITY_20260920`
- `D1TPW_CHECKPOINT_ATOMICITY_210_20260920`

D1TPW lifecycle gate remains `false`.

The checkpoint now:
1. invalidates the prior commit marker before payload mutation;
2. increments a generation;
3. exact-writes payload and generation;
4. verifies the uncommitted payload;
5. publishes the commit marker last;
6. accepts loads only when committed generation and payload generation match;
7. invalidates the commit marker first during clear.

Legacy eight-key checkpoints with no generation/commit identity are not accepted as committed D1TPW state. Existing targetless recovery then fails frozen through `TARGETLESS_CHECKPOINT_MISSING_OR_INVALID`; no owner is guessed.

C044 exact GlobalVariable helpers are wrappers over the same exact set/delete primitives. Its generation/checkpoint/replay bodies remain byte-exact to Build 4.86.

## Protected behavior

Exact-body comparison Build 4.86 -> 4.87 PASS for:
- D1 TP-Wajib completion detection;
- D1 opportunity journey and candidate construction;
- D1TPW lifecycle identity;
- approved SL/TP resolution;
- M16 D1 opportunity validation;
- D1TPW closed-candle processing/latch/close;
- M20 position management;
- D1TPW initialization;
- C044 checkpoint/replay save/load;
- risk preflight and broker execution.

## Deterministic/static validation

- D1TPW generation failure-injection model: **PASS**, 12 replacement failure points.
- D1TPW source/static commit-last guard: **PASS**.
- Build 4.86 -> 4.87 protected-body comparison: **PASS**.
- Existing C044 generation model: **PASS**, normal 145 ops / frozen 85 ops and all modeled failure points.
- Existing v4.82 F7 source guards: **PASS**.
- `git diff --check`: **PASS**.

Evidence:
- `blueprint/audits/evidence/D1TPW_BUILD487_20260920/STATIC_REGRESSION.log`
- `blueprint/tests/test_d1tpw_generation_atomicity.py`
- `blueprint/tests/test_d1tpw_checkpoint_atomicity_static.py`
- `blueprint/tests/compare_d1tpw_486_487_protected.py`

## Native compile

Canonical Build 4.87:
- MetaEditor: **0 errors / 0 warnings**
- MQ4 SHA-256: `E66B444E66CF0F4F5A6AF9A87D5133D1F17A5F88251D1E48D8D013C0A7C74B26`
- EX4 SHA-256: `3ECEE2B74F30600C95F539C8B7782F43F0C4450E09A9AE025CFEE7490CF3370B`

Tester-only adapter:
- invariant transform: **PASS**
- MetaEditor: **0 errors / 0 warnings**
- MQ4 SHA-256: `6F3AD0746371D20B14532936C5E63BE6BB1330D4D4677BDCA2EB1DCE3E47E752`
- EX4 SHA-256: `09A90C9928ECE5ED9B892E7E1B77B69B274468EE7F4418F36691BFDD0967931C`

The adapter contains only the previously verified offline-tester environment guards: test-symbol resolution, tester connectivity, and EventSetTimer bypass.

## Targeted offline runtime regression

Profile: verified GBPUSD engineering profile, M15, 2026-08-01 through 2026-09-01, Every Tick.

Build 4.87 versus verified Build 4.86 smoke:
- total trades: 14 / 14;
- M15_COUNTS: 523 / 523 exact;
- M15_SELECT: 523 / 523 exact;
- M16_PASS: 523 / 523 exact;
- DECISION_FINAL: 523 / 523 exact;
- EXEC: 14 / 14 exact;
- all compared authority traces: exact-equal;
- D1TPW managed events: 0, as expected with gate OFF;
- fatal targeted runtime faults: 0.

OfflineDiag GlobalVariables were restored after the smoke:
- pre-run SHA-256: `DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6`;
- post-restore SHA-256: `DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6`.

No D1TPW/Q9 tester process remains active. Q3 isolated C10 terminal PID 13064 was not restarted or modified.

Evidence:
- `blueprint/audits/evidence/D1TPW_BUILD487_20260920/D1TPW487_SMOKE_ANALYSIS.json`
- `blueprint/audits/evidence/D1TPW_BUILD487_20260920/METAEDITOR_COMPILE.log`
- `blueprint/audits/evidence/D1TPW_BUILD487_20260920/TESTER_METAEDITOR_COMPILE.log`
- `blueprint/audits/evidence/D1TPW_BUILD487_20260920/TESTER_ADAPTER_INVARIANT.log`

## Runtime boundary

This is not R1 broker-runtime proof with D1TPW enabled. The feature gate remains OFF. No claim is made that natural broker D1TPW lifecycle branches were exercised.

## Exit result

**Issue #210 scoped implementation exit criteria: VERIFIED.**

Draft PR only. No merge, production activation, D1TPW enablement, Strategy-Core change, risk/MM change or execution-policy change is authorized by this validation.
