# Dashboard PR #98 — Prematerialization Audit & Acceptance Matrix

Date: 2026-08-27
Status: PREMATERIALIZATION / SOURCE UNTOUCHED / NO MERGE
Scope: isolated dashboard preparation only

## 1. Safety boundary

This audit does not authorize or materialize any change to `blueprint/source/BBMA_EA.mq4`.

R1 remains active under Issue #96. The frozen v4.59 runtime lineage must not receive opportunistic source edits while attributable R1 evidence is being collected. PR #98 therefore remains DRAFT / NO MERGE until its own source materialization, static guard, native MetaEditor 0E0W and isolated runtime checks are complete.

All follow-up hardening in this record is prepared on isolated branch `dashboard-chain-audit-20260827`. It is not a canonical source change and is not a PASS claim for the future materialized dashboard.

## 2. Reviewed preparation state

Original PR #98 preparation consists of:
- `.github/workflows/dashboard-chain-materialize.yml`
- `blueprint/.run-dashboard-chain`
- `blueprint/tests/test_dashboard_chain_safety_fix.py`
- `blueprint/tools/dashboard_chain_compact_apply.py`
- `blueprint/tools/dashboard_chain_safety_fix.py`

The isolated audit branch additionally prepares:
- `blueprint/tools/dashboard_chain_prematerialization_fix.py`
- `blueprint/tests/test_dashboard_chain_prematerialization_fix.py`
- `blueprint/tools/dashboard_chain_scope_guard.py`
- `.github/workflows/dashboard-chain-audit-static.yml`
- this audit record

`blueprint/source/BBMA_EA.mq4` remains absent from the audit-branch delta relative to `dashboard-chain-dev`.

Prepared future materializer ordering is fail-closed:
1. primary and prematerialization fixture selftests + Python compile check
2. primary M25 materializer
3. primary dashboard safety hardening
4. prematerialization display hardening
5. strict source-scope guard
6. M25 authority/performance/semantic static guard
7. diff hygiene
8. source commit only if all preceding checks pass

The primary safety stage and the prematerialization stage are deliberately non-overlapping. Primary safety owns multi-position aggregation, BUY/SELL tie handling, live-position change detection, and VALIDATED-vs-EXECUTED separation. The later prematerialization stage owns deterministic signature ordering, decision-family chain consistency, and OnDeinit chart-object cleanup.

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

### DASH-PRE-01 — PASS/PREPARED: multi-position aggregation
The primary safety helper replaces first-order-only display with BUY/SELL counts and mixed-direction representation.

### DASH-PRE-02 — PASS/PREPARED: exact BUY/SELL rank tie
Equal-rank opposite directions are prepared to display `MIX`; the old implicit BUY tie bias is rejected by the safety guard.

### DASH-PRE-03 — PASS/PREPARED: validated and executed states separated
`DEC_VALIDATED` is prepared as `VAL` / `~`; `DEC_EXECUTED` is prepared as `EXE` / `✓`.

### DASH-PRE-04 — PREPARED, NOT YET MATERIALIZED: chart-object cleanup on deinitialization
Static review found that the new dashboard uses `OBJ_LABEL` objects under prefix `BBMA_DASH_` while canonical `OnDeinit()` clears only `Comment("")`.

The isolated prematerialization helper now prepares unconditional `ClearDashboardObjects();` plus `Comment("");` during deinitialization. The separate scope guard permits only the complete M25 replacement plus this exact display-only OnDeinit delta.

This blocker is preparation-complete but cannot be promoted to PASS until actual materialization, static guard and runtime removal/recompile checks prove the labels are removed.

### DASH-PRE-05 — PREPARED, NOT YET MATERIALIZED: setup/chain family consistency
Static review found that a decision family could overwrite `SETUP` while retaining another locally ranked family's `CHAIN`.

The isolated prematerialization helper now reconstructs the chain only inside the selected decision family (`REM`, `RRE`, `REE`, `RE`). Where current component state cannot reconstruct that family, it degrades to an explicit same-family `DEC:<family>` marker rather than reusing another family's chain.

This blocker is preparation-complete but remains runtime/static-evidence pending.

### DASH-PRE-06 — PREPARED, NOT YET MATERIALIZED: order-invariant live-position signature
The original prepared signature serialized MT4 `SELECT_BY_POS` enumeration order and could redraw if pool order changed without a position-set change.

The isolated prematerialization helper now captures exact-owned ticket/pair/type triples, sorts them deterministically by unique ticket, and only then serializes the signature. This is presentation determinism only and does not change trading state.

Native/runtime confirmation remains required.

### DASH-PRE-07 — EVIDENCE REQUIRED: Unicode/native MetaEditor compatibility
The proposed labels contain arrows and a check mark. Static review cannot establish native MetaEditor encoding/compile behaviour. Native MetaEditor 0 errors / 0 warnings remains mandatory after materialization.

### DASH-PRE-08 — PASS: timer does not become strategy authority
Canonical timer calls `OnTickMain()` and then `RefreshDashboardLiveTradeCount()`. Prepared dashboard timer work is presentation-only and reads exact-owned broker position identity. No strategy/risk/validation/lifecycle/execution authority is permitted in M25.

### DASH-PRE-09 — PASS/PREPARED: transformation stages are non-redundant and fail closed
A temporary audit-branch overlap was detected when deterministic signature, family consistency and deinit cleanup were added to both the primary safety stage and the later prematerialization stage. That would have made the second textual transform fail because its expected predecessor text had already been consumed.

The audit branch was reconciled so those three responsibilities exist only in `dashboard_chain_prematerialization_fix.py`. The primary `dashboard_chain_safety_fix.py` is restored to its original four responsibilities. This preserves exact stage contracts and avoids redundant transformations.

## 5. CI zero-step anomaly investigation

Dashboard materializer run `33074855091` failed before attributable executable work:
- dashboard job exists but reports no usable runner execution
- executable step list is empty

A deliberately read-only, fixture-only audit workflow was then created on the isolated audit branch. Run `33083370710`, job `98556304055`, also completed as failure with an empty step list; the job-log fetch has no usable log blob. That workflow had no source materialization and no write permission.

Multiple unrelated repository workflows triggered around the same periods also fail immediately before useful job execution, while earlier repository workflows on 2026-08-27 have successful executions.

Classification: **REPOSITORY / GITHUB ACTIONS EXECUTION AVAILABILITY ANOMALY**. The exact external cause is not proven.

The repeated zero-step result from a read-only fixture-only workflow materially strengthens the conclusion that these runs are not attributable evidence of dashboard Python/source PASS or FAIL. Do not use them as verification. A future non-empty attributable run is still required.

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
| DSH-14 | unchanged order set across timer ticks | deterministic ticket-sorted signature prevents pool-order-only redraws | static + runtime |
| DSH-15 | EA remove/recompile | all `BBMA_DASH_` objects removed | runtime |
| DSH-16 | chart restart / EA reattach | no duplicate stale labels; fresh row set only | runtime |
| DSH-17 | Unicode labels | native MetaEditor 0E0W and chart text renders acceptably | native + runtime |
| DSH-18 | decision family differs from highest current local family | displayed SETUP and CHAIN remain in the same decision family or use same-family `DEC:` fallback | static + runtime |

## 7. Promotion gate

PR #98 must remain DRAFT / NO MERGE until all of the following are true:
1. prepared DASH-PRE-04 cleanup is actually materialized and verified.
2. prepared DASH-PRE-05 family consistency is actually materialized and verified.
3. prepared DASH-PRE-06 deterministic signature is actually materialized and verified.
4. materializer executes with attributable non-empty steps.
5. fixture selftests and Python syntax checks execute with attributable PASS evidence.
6. strict source-scope guard passes on actual materialized source.
7. static display-only guard passes on actual materialized source.
8. native MetaEditor compile is 0 errors / 0 warnings.
9. DSH-00..DSH-18 are resolved as PASS or explicitly documented BLOCKED with no false PASS.
10. no strategy, risk, validation, lifecycle or execution authority change is present.
11. frozen R1 canonical lineage remains untouched unless separately authorized after its evidence boundary.
