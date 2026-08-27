# R1 D1 TP-Wajib Runtime Operator Handoff

Date: 2026-08-27  
Canonical branch: `d1-owner-dev`  
Status: **READY FOR AUTHENTICATED HFM DEMO COLLECTION / R1 REMAINS INCOMPLETE**

## 1. Authority and current status

This is the operator-facing handoff for R1. Detailed PASS/FAIL semantics remain authoritative in:

`blueprint/audits/R1_D1_TPW_BROKER_RUNTIME_TEST_MATRIX_PREP_20260826.md`

The preparation-era header in that matrix says R1 was blocked by P0. That historical blocker is now superseded by:

`blueprint/audits/P0_V459_IP12_CANONICAL_FREEZE_R1_HANDOFF_20260827.md`

Current project state is therefore:

- P0: PASS
- IP-01..IP-12: PASS
- Issue #94: CLOSED / completed
- R1: **INCOMPLETE / RELEASED FOR COLLECTION**
- R2-R6: BLOCKED by predecessor order

Tracking issue:
`#96 — R1: D1 Extreme TP-Wajib broker runtime evidence collection`

## 2. Frozen canonical lineage

R1 must remain attributable to this frozen v4.59 lineage:

- build: `Version 4.5.9 - P0 Execution Identity Persistence Fix`
- property: `4.59`
- canonical source Git blob: `dc83e62748c93171d89a312e9f7a53c06d97e261`
- repository/LF MQ4 SHA-256: `07a69ccfca19e19d71c95ca891c66d953343261276d7722107624ce974830843`
- Windows compile-checkout MQ4 SHA-256: `0a42ee2e6c32810f655b592d8738f500e8b63b4e08c4c874e82452f75ce94b2e`
- canonical source-bearing promotion commit: `4373e55b3baca7c99a3ca643cb5fa97629be09b7`

Canonical production defaults remain:

- D1TPW OFF
- C044 OFF
- N3 non-execution-authority

R1 does not modify those production defaults.

## 3. Accepted v4.59 R1 tooling package

Official tooling validation source:

- GitHub Actions run `33027817870`
- artifact `9629222430` — `v459-runtime-tooling-gate-evidence`
- artifact digest `sha256:2bcdef749fed42eb5e40a196125706e49a8fab7928b29ac3307b9e4692e62842`
- variant builder/analyzer selftests: PASS
- BASELINE / R1_D1TPW / R2_C044 / observer native compile matrix: PASS, 0 errors / 0 warnings

Relevant R1 binaries from that validated artifact:

- `BBMA_EA_V459_BASELINE.ex4`
  - D1TPW OFF / C044 OFF
  - SHA-256 `e1a9c004a2a31d3074fae02c5b8944041b64d2d18332a47ce6cae7188f7d67ba`
- `BBMA_EA_V459_R1_D1TPW.ex4`
  - D1TPW ON / C044 OFF
  - SHA-256 `4efc57153435b266c72348460b66077f145c27a484c4c9b4a1a76393918cd6b3`
- `V459_Runtime_Observer.ex4`
  - read-only observer
  - SHA-256 `abf7881fe1fb084cfa70a02cd16e0751248e13d6e0e97552ddbc8279a4a715c9`

The validated R1 variant metadata records semantic scope as canonical v4.59 plus the already-approved D1TPW lifecycle gate flip only.

## 4. Safety boundary

**HFM DEMO ONLY. NEVER USE THE R1 TEST BUILD ON A LIVE ACCOUNT.**

Do not edit the EX4 files. Do not enable C044 in normal R1 acceptance. Do not change the frozen canonical EA source merely to make a runtime case occur.

A runtime case that has not naturally/controllably occurred remains `INCOMPLETE`; it is not a failure unless contradictory behavior is observed.

## 5. Required R1 profile

For active R1 cases use:

- authenticated HFM demo / broker-connected MT4 session
- `BBMA_EA_V459_R1_D1TPW.ex4`
- D1TPW ON / C044 OFF as built into the test variant
- Entry Mode 2 for D1 Opportunity execution
- `MinRRRatio=0` for targetless lifecycle acceptance
- debug/telemetry sufficient to capture D1/D1O, M17, P3 execution, M23/M24 lifecycle/recovery records
- observer on a separate chart when used
- controlled non-production demo risk

For R1-00 gate-OFF control use the validated `BBMA_EA_V459_BASELINE.ex4`, not the R1-active binary.

## 6. First operator sequence

### Phase A — environment/preflight

1. Use HFM **demo** MT4 only.
2. Use the same MT4 installation/data folder throughout any restart-attribution case.
3. Preserve exact R1 binary identity; do not recompile or rename-and-edit its source.
4. Confirm AutoTrading and broker connection only when beginning an executable case.
5. Avoid unrelated EA-managed positions that would make ticket/lifecycle attribution ambiguous.
6. If using `V459_Runtime_Observer.ex4`, attach it on a separate chart; it is observation-only.

### Phase B — R1-00 gate-OFF control

Use `BBMA_EA_V459_BASELINE.ex4`.

The case is not complete merely because no order exists. R1-00 requires a valid `D1_OPP_EXTREME_TPW` candidate to be encountered while D1TPW is OFF. PASS requires that candidate to fail closed: no legacy fixed outer-BB TP execution/fallback.

If the required candidate has not occurred, record the case as `INCOMPLETE`.

### Phase C — active R1 profile

Switch to `BBMA_EA_V459_R1_D1TPW.ex4` only for the active R1 evidence campaign.

For a qualifying fresh `D1_OPP_EXTREME_TPW` + fresh H1 Re-Entry execution, R1-01 expects:

- valid hard SL
- broker TP = 0
- D1TPW lifecycle identity/checkpoint present
- C044 is not lifecycle owner

If a generic legacy outer-BB fixed TP is substituted, the case FAILS.

Do not manually open an order and call it R1 evidence; executable R1 entry evidence must remain attributable to the EA decision/execution path.

## 7. Restart evidence rule — R1-02

Before restarting, capture:

- live ticket
- pair / magic / direction / open time
- DecisionID or execution hash
- D1TPW checkpoint fields
- current fully-closed-D1 cursor

Then preserve the ticket open and perform a **full MT4/EA restart using the same installation/data folder**.

After restart capture the exact-ticket recovery state and reconstructed checkpoint/source/cursor fields. The case must not create a duplicate entry.

A restart without the pre-restart checkpoint snapshot is insufficient to PASS R1-02.

## 8. Missed-candle replay — R1-03

R1-03 requires an actual interval where one or more D1 candles complete while the terminal/EA is offline, followed by recovery.

PASS requires oldest-to-newest replay of missed fully closed D1 candles exactly once and correct cursor advancement. Do not manufacture a PASS from a normal quick restart that missed no D1 close.

## 9. TP-Wajib completion cases

Completion is based on **fully closed D1 candle** evidence and same-candle dynamic MA values.

Mandatory alternative coverage includes:

- BUY via MA5 High
- BUY via MA10 High
- SELL via MA5 Low
- SELL via MA10 Low

One candle touching both MA5 and MA10 proves a completion event but does not automatically prove both alternative code paths independently.

Forming/current D1 touch alone must not close the lifecycle trade.

## 10. Negative/safety cases

R1-12, R1-13 and R1-14 must never be forced unsafely:

- dual-checkpoint ambiguity: controlled corruption/test facility only
- missing/corrupt checkpoint: controlled negative recovery only
- M20 emergency precedence: safe demo controlled occurrence/facility only

If a safe attributable occurrence is unavailable, leave the case `INCOMPLETE`.

## 11. Evidence to retain

For every executable ticket retain enough evidence to identify:

- canonical and test-variant identity
- broker/demo classification
- pair / ticket / magic / direction / open time
- DecisionID / execution hash
- D1 Opportunity family
- D1 Extreme source/confirmation candle
- H1 Re-Entry identity used for entry/dedup/hard-SL provenance
- hard SL / broker TP at open
- D1TPW checkpoint and closed-D1 cursor
- latch candle/state if completion occurs
- close result/time
- recovery state around restart where applicable

Screenshots may support evidence, but raw Experts/Journal/observer logs should be preserved whenever available.

## 12. Closure boundary

R1 remains **INCOMPLETE** until all mandatory R1 cases are positively demonstrated with attributable HFM demo evidence.

Do not activate D1TPW in canonical production defaults after R1 merely because runtime PASS is eventually achieved. R1 closure requires a dedicated closure audit; production/default activation remains a separate explicit project decision.
