# R1 Runtime Session Isolation and Observer Profile

Date: 2026-08-27  
Canonical branch: `d1-owner-dev`  
Status: **OPERATOR PREFLIGHT / EVIDENCE-HYGIENE ADDENDUM**

## 1. Purpose

This addendum records an operational evidence-hygiene rule discovered during the authenticated HFM demo R1 preflight. It does **not** modify BBMA strategy logic, canonical EA source, lifecycle defaults, risk/MM rules, execution policy or R1 acceptance semantics.

R1 remains governed by:

- `blueprint/audits/R1_D1_TPW_BROKER_RUNTIME_TEST_MATRIX_PREP_20260826.md`
- `blueprint/audits/R1_D1_TPW_RUNTIME_OPERATOR_HANDOFF_20260827.md`
- `blueprint/audits/MASTER_R1_R6_RUNTIME_EVIDENCE_INDEX_20260827.md`
- Issue #96

## 2. Frozen source boundary

The R1 campaign remains attributable to v4.59 lineage:

- build: `Version 4.5.9 - P0 Execution Identity Persistence Fix`
- property version: `4.59`
- canonical source Git blob: `dc83e62748c93171d89a312e9f7a53c06d97e261`
- canonical baseline defaults: `EnableD1TPWLifecycle=false`, `EnableC044Lifecycle=false`
- R1 test-only profile: D1TPW ON / C044 OFF

This addendum does not authorize any canonical source edit.

## 3. Operator preflight observation

The latest supplied HFM demo operator evidence showed:

- R1 EA attached and initialized on MT4;
- Entry Mode 2 profile in use;
- `MinRRRatio=0.0`;
- debug increased to `DBG_FULL` for R1 evidence collection;
- `V459_Runtime_Observer` attached on a separate chart;
- Observer cadence reduced operationally from the source default `5` seconds to `60` seconds;
- Observer history lookback reduced operationally from the source default `168` hours to `1` hour;
- global AutoTrading enabled after the preflight checks;
- at the supplied checkpoint, the EA dashboard showed `Trades: 0`.

The reduced Observer cadence/lookback changes observation volume only. It does not alter EA strategy, execution, lifecycle or broker-write behavior.

## 4. Pre-existing persistence namespace observation

The Observer output also exposed multiple existing terminal GlobalVariables under `StrategyID=1 / InstanceID=0`, including execution-identity namespace entries such as `BBXT|S1|I0|...` and related persisted state.

These entries can legitimately belong to earlier accepted runtime activity. They must **not** be deleted merely to make a new R1 session look clean, because deletion could destroy prior persistence/recovery evidence.

They are therefore classified as **pre-existing state / evidence-contamination risk**, not as fresh R1 evidence.

## 5. Isolation rule for a new R1 campaign

If no new attributable R1 ticket has yet been created in the current session, the preferred evidence-hygiene procedure is:

1. stop automated execution before changing identity inputs;
2. use a fresh unused `InstanceID` for the new R1 campaign;
3. set the **same StrategyID and InstanceID** on both the R1 EA and `V459_Runtime_Observer`;
4. restart/reinitialize the observer and confirm its `[V459-OBS][START]` line reports the selected namespace;
5. verify the selected namespace has no pre-existing `D1TPW`, `C044`, `BBXH` or `BBXT` state before enabling automated execution;
6. preserve that identity unchanged for the entire attributable R1 campaign and any restart/recovery test.

If a new R1 ticket has already been created under the current identity, **do not switch InstanceID mid-trade**. Freeze the current configuration and capture that ticket/checkpoint/execution identity first.

## 6. Why InstanceID isolation is valid

The canonical EA exposes `InstanceID` as execution identity input. The observer uses StrategyID/InstanceID to derive its owned magic-number range and to filter lifecycle/execution GlobalVariable prefixes. Therefore a fresh matching namespace gives cleaner evidence attribution without changing BBMA trading semantics.

This is runtime campaign isolation, not a strategy modification.

## 7. Observer profile rule

For routine R1 collection, the low-noise operator profile may use:

- `SnapshotSeconds=60`
- `HistoryLookbackHours=1`

For a critical transition (fresh execution, pre-restart snapshot, restart recovery, lifecycle latch/close), increase evidence density only when needed. Any such observer-setting change remains observation-only and must not change the EA identity or trading inputs being attributed.

## 8. Fail-closed boundaries

- Never delete old terminal GlobalVariables to manufacture a clean result.
- Never change StrategyID/InstanceID while an attributable R1 trade is live.
- Never classify old I0 persistence records as fresh R1 evidence.
- Never mark R1 PASS from static/source evidence alone.
- Never advance R2 while R1 remains INCOMPLETE.
- Never enable C044 in the R1 profile.

## 9. Verdict

**R1 PREFLIGHT ADDENDUM RECORDED.**

The current canonical source remains frozen. The next broker-runtime action is evidence collection under one stable, isolated R1 identity namespace; if a fresh R1 ticket already exists, its current namespace is preserved rather than changed.