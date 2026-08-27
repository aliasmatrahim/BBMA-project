# Dashboard PR #98 — Prematerialization Audit & Acceptance Matrix

Date: 2026-08-27
Status: PREMATERIALIZATION / SOURCE UNTOUCHED / NO MERGE
Scope: isolated dashboard preparation only

## 1. Safety boundary

This audit does not authorize or materialize any change to `blueprint/source/BBMA_EA.mq4`.

R1 remains active under Issue #96. The frozen v4.59 runtime lineage must not receive opportunistic source edits while attributable R1 evidence is being collected. PR #98 therefore remains DRAFT / NO MERGE until its own source materialization, static guard, native MetaEditor 0E0W and isolated runtime checks are complete.

## 2. Reviewed preparation state

PR #98 preparation currently consists of:
- `.github/workflows/dashboard-chain-materialize.yml`
- `blueprint/.run-dashboard-chain`
- `blueprint/tests/test_dashboard_chain_safety_fix.py`
- `blueprint/tools/dashboard_chain_compact_apply.py`
- `blueprint/tools/dashboard_chain_safety_fix.py`

`blueprint/source/BBMA_EA.mq4` is not currently part of the PR diff.

The workflow is ordered fail-closed:
1. safety selftest + Python compile check
2. primary M25 materializer
3. dashboard safety hardening
4. M25 authority/performance/semantic static guard
5. source commit only if the preceding checks pass

## 3. Canonical compatibility checks completed

The proposed dashboard references canonical objects that exist in frozen v4.59 source:
- `PairState`, `g_pair_states`, `g_pair_count`
- `re_d1_*`, `re_h4_*`, `re_h1_*`
- H4/H1 Extreme lifecycle state
- M15 MHV/MLV state
- `last_decision`
- `IsExactEAOwnedSelectedOrder()`
- `g_dashboard_needs_update`
- `BuildDashboardSnapshot()`, `UpdateDashboard()`, `RefreshDashboardLiveTradeCount()` integration hooks

The canonical exact-owned order helper admits only live `OP_BUY` / `OP_SELL` orders with matching EA symbol/magic ownership. Pending orders are therefore outside dashboard live-position counts by design.

## 4. Static findings

### DASH-PRE-01 — PASS: multi-position aggregation is prepared
The post-materialization safety helper replaces first-order-only display with BUY/SELL counts and mixed-direction representation.

### DASH-PRE-02 — PASS: exact BUY/SELL rank tie is explicit
Equal-rank opposite directions are prepared to display `MIX`; the old implicit BUY tie bias is rejected by the safety guard.

### DASH-PRE-03 — PASS: validated and executed states are separated
`DEC_VALIDATED` is prepared as `VAL` / `~`; `DEC_EXECUTED` is prepared as `EXE` / `✓`.

### DASH-PRE-04 — OPEN BLOCKER: chart-object cleanup on deinitialization
The new dashboard uses `OBJ_LABEL` objects under prefix `BBMA_DASH_`. Canonical `OnDeinit()` currently clears only `Comment("")`; it does not call the proposed `ClearDashboardObjects()`.

Risk: removing/recompiling the EA can leave stale dashboard labels on the chart until another explicit cleanup path runs.

Required before promotion: an attributable display-only cleanup hook must call `ClearDashboardObjects()` on deinitialization, with a static guard proving no trade/risk/lifecycle authority is added.

### DASH-PRE-05 — OPEN BLOCKER: setup/chain family mismatch can be displayed
`DashBuildDirectionChain()` locally selects the highest numeric display rank across REM/RRE/REE, then later overwrites `setup` with `last_decision.SignalType` without necessarily rebuilding `chain` for that same family.

Example failure mode: current local state ranks REE above REM while `last_decision.SignalType == SIGNAL_REM`; the row can show `SETUP=REM` with an REE component chain.

Required before promotion: setup and chain must be family-consistent. If a decision state is displayed as VAL/EXE, its displayed setup must never be paired with another family's chain.

### DASH-PRE-06 — HARDENING ITEM: live-position refresh signature is order-sensitive
The prepared signature concatenates exact-owned orders in `OrderSelect(..., SELECT_BY_POS, MODE_TRADES)` enumeration order. If terminal enumeration order changes while the actual set of positions is unchanged, the dashboard can redraw unnecessarily.

This is a performance/determinism issue, not trading correctness. Before promotion, prefer an order-invariant signature (for example deterministic ticket sorting) or explicitly accept the harmless redraw behaviour in the runtime matrix.

### DASH-PRE-07 — EVIDENCE REQUIRED: Unicode/native MetaEditor compatibility
The proposed labels contain arrows and a check mark. Static review cannot establish native MetaEditor encoding/compile behaviour. Native MetaEditor 0 errors / 0 warnings remains mandatory after materialization.

### DASH-PRE-08 — PASS: timer does not become strategy authority
Canonical timer calls `OnTickMain()` and then `RefreshDashboardLiveTradeCount()`. Prepared dashboard timer work is presentation-only and reads exact-owned broker position identity. No strategy/risk/validation/lifecycle/execution authority is permitted in M25.

## 5. CI zero-step anomaly investigation

Latest dashboard materializer run `33074855091` failed before attributable executable work:
- dashboard job exists but reports `runner_id=0`
- executable step list is empty

The same dashboard head triggered multiple other repository workflows at the same time, and those runs also failed immediately; at least one sampled sibling run reports zero jobs. Recent repository success evidence exists earlier on 2026-08-27, while the later run group fails before jobs execute.

Classification: REPOSITORY / GITHUB ACTIONS EXECUTION AVAILABILITY ANOMALY — exact external cause not proven.

Do not classify the dashboard source or Python tooling as PASS or FAIL from these zero-step runs. A fresh attributable workflow execution is required later.

## 6. Dashboard acceptance matrix

| ID | Case | Expected result | Evidence class |
|---|---|---|---|
| DSH-00 | ShowDashboard=false | no BBMA dashboard objects/comment remain | native/runtime |
| DSH-01 | no active setup, no position | `IDL`, setup `-`, chain `-`, empty POS | runtime |
| DSH-02 | H4 RE only | REM building prefix shown without invented completion | runtime |
| DSH-03 | complete REM | setup and chain both REM-consistent | runtime |
| DSH-04 | complete RRE | setup and chain both RRE-consistent | runtime |
| DSH-05 | complete REE | setup and chain both REE-consistent | runtime |
| DSH-06 | standalone H1 RE | RE row shown without combination invention | runtime |
| DSH-07 | equal BUY/SELL display rank | explicit `MIX`; no BUY bias | static + runtime |
| DSH-08 | one BUY live position | `POS↑` and exact-owned live count +1 | runtime |
| DSH-09 | two BUY live positions | `POS↑x2`; no first-order hiding | runtime |
| DSH-10 | BUY+SELL live positions | mixed POS representation with both counts | runtime |
| DSH-11 | DEC_VALIDATED | `VAL` / `~`; never execution check mark | static + runtime |
| DSH-12 | DEC_EXECUTED | `EXE` / `✓`; broker position attribution still independently verifiable | static + runtime |
| DSH-13 | position open/close without new M15 signal | timer refresh updates POS without strategy mutation | runtime |
| DSH-14 | unchanged order set across timer ticks | no unnecessary redraw where deterministic signature is implemented/accepted | runtime |
| DSH-15 | EA remove/recompile | all `BBMA_DASH_` objects removed | runtime |
| DSH-16 | chart restart / EA reattach | no duplicate stale labels; fresh row set only | runtime |
| DSH-17 | Unicode labels | native MetaEditor 0E0W and chart text renders acceptably | native + runtime |

## 7. Promotion gate

PR #98 must remain DRAFT / NO MERGE until all of the following are true:
1. DASH-PRE-04 cleanup blocker resolved in preparation tooling.
2. DASH-PRE-05 setup/chain family-consistency blocker resolved.
3. DASH-PRE-06 determinism either fixed or explicitly accepted with runtime evidence.
4. Materializer executes with attributable non-empty steps.
5. Static display-only guard passes on the actual materialized source.
6. Native MetaEditor compile is 0 errors / 0 warnings.
7. DSH-00..DSH-17 mandatory acceptance cases are resolved as PASS or explicitly documented BLOCKED with no false PASS.
8. No strategy, risk, validation, lifecycle or execution authority change is present.
9. Frozen R1 canonical lineage remains untouched unless separately authorized after its evidence boundary.
