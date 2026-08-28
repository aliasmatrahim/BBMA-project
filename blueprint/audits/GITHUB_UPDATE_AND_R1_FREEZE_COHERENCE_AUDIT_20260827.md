# GitHub Update and R1 Freeze Coherence Audit

Date: 2026-08-27  
Canonical branch: `d1-owner-dev`  
Status: **R1 FREEZE PRESERVED / NEW DEVELOPMENT QUARANTINED**

## 1. Purpose

Record the latest repository developments while authenticated R1 broker-runtime evidence is being collected, and prove that unrelated development remains isolated from the frozen v4.59 runtime candidate.

This audit is documentation only. It does not modify `blueprint/source/BBMA_EA.mq4`, does not activate lifecycle gates, does not alter BBMA strategy/risk/execution semantics, and does not advance `main`.

## 2. R1 canonical boundary

R1 remains governed by Issue #96 and the frozen v4.59 lineage:

- build: `Version 4.5.9 - P0 Execution Identity Persistence Fix`
- property: `4.59`
- canonical source Git blob: `dc83e62748c93171d89a312e9f7a53c06d97e261`
- canonical baseline: D1TPW OFF / C044 OFF
- R1 test-only profile: D1TPW ON / C044 OFF
- R1 status: `INCOMPLETE / RELEASED FOR AUTHENTICATED HFM DEMO COLLECTION`
- R2-R6 remain blocked by predecessor ordering

No opportunistic canonical EA-source edit is permitted during attributable R1 collection.

A current Issue #96 checkpoint records the HFM demo session as armed/preparation-only: R1 EX4 attached, Observer attached, `MinRRRatio=0` visible, `DBG_FULL` operator-confirmed, Observer reduced to 60-second snapshots / 1-hour history, and MT4 automated trading enabled. At that checkpoint the dashboard still showed `Trades: 0`; no mandatory R1 case was promoted.

## 3. Isolated PR #97 — NMJE N3 hardening staging

PR #97 remains **DRAFT / NO MERGE / NO ACTIVATION**.

Reviewed scope includes:

- M08/M09 Extreme single-writer hardening;
- deterministic NMJE provenance identities;
- ParentEventID/JourneyID propagation;
- M15/M16 shadow-only provenance freeze/revalidation;
- recovery/replay/authority regression tooling.

The current materialized PR source still derives the D1 owner NMJE EventID from `D1MajorTrendOwner.SourceCandleTime`, which refreshes on closed-D1 snapshots. Therefore the known owner-epoch identity gap is not yet closed in the current source patch.

Safe isolated preparation now includes:

- branch head: `19b34544515b71ef805008a0e59595d154a99b75`;
- `blueprint/tools/nmje_n3_step5_d1_owner_epoch_apply.py`, which adds a provenance-only `EpochStartCandleTime` anchor while preserving `SourceCandleTime` as the latest closed-D1 snapshot;
- `blueprint/tests/test_nmje_n3_d1_owner_epoch_apply.py`, a synthetic fail-closed transformation selftest that checks the epoch migration and rejects execution/trade-operation markers;
- `.github/workflows/nmje-n3-step5-d1-owner-epoch-materialize.yml`, which runs the selftest plus `py_compile`, applies the helper, verifies epoch provenance markers, rejects N3 execution-authority markers, and commits source only after those checks;
- latest materializer run `33074399592`; its only job `98524700906` completed as failure with `steps=null` / zero executable steps.

Therefore the epoch change is **prepared but not materialized/verified**. The zero-step result remains an unclassified CI/runner availability anomaly and must not be promoted to source PASS or source FAIL.

Required boundary:

- preserve N3 non-execution authority;
- keep PR draft;
- obtain fresh successful static/native gates after CI recovers;
- do not merge during current R1 attribution.

## 4. Isolated PR #98 — Dashboard compact cycle-aware chain UI

PR #98 remains **DRAFT / NO MERGE**.

The intended combination display signatures were cross-checked against the canonical combination engine and match:

- REM = H4 Re-Entry + H1 Extreme + M15 MLV;
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme;
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

Static review of the first materializer design found four display-layer correctness/performance issues:

1. `DashLivePosition()` returned the first EA-owned order and could hide additional same-pair positions;
2. exact BUY/SELL chain-rank ties silently preferred BUY through `buyRank >= sellRank`;
3. the timer design redrew the complete dashboard every 1 second even if exact-owned broker positions had not changed;
4. `DEC_VALIDATED` and `DEC_EXECUTED` were both treated as a completed setup with the same execution-style check mark, which could visually imply a broker execution before execution actually occurred.

The fourth distinction was cross-checked against canonical state transitions: M16 sets `DEC_VALIDATED`; the execution path later sets `DEC_EXECUTED` after an execution ticket is obtained. This is an existing canonical distinction; the isolated dashboard change only reflects it.

Safe isolated hardening now includes:

- branch head: `c37a75cb3461e1516189d74415a7f581c97ae201`;
- `blueprint/tools/dashboard_chain_safety_fix.py` aggregates all exact EA-owned BUY/SELL positions, represents equal-rank opposite chains as `MIX`, refreshes broker-position presentation only when exact-owned order identity changes, and separates validated (`VAL` / `~`) from executed (`EXE` / `✓`) display states;
- `blueprint/tests/test_dashboard_chain_safety_fix.py` provides a fail-closed synthetic transformation selftest covering all four hardening items;
- `.github/workflows/dashboard-chain-materialize.yml` runs the selftest plus `py_compile`, primary materializer, safety hardening, and an M25 display-only authority/performance/semantic guard;
- latest materializer run `33074855091`; its only materialize job `98526273497` completed as failure with `steps=null` / zero executable steps.

Thus DASH-SAFE-01 through DASH-SAFE-04 are **prepared in isolated tooling but not yet materialized/native-compiled**. The PR must remain draft.

These findings and preparations are display-layer only and do not justify canonical source mutation during R1.

## 5. CI interpretation rule

A workflow conclusion of `failure` without executable job steps/log evidence is **unclassified CI/runner failure**, not proof of an EA source defect or compile defect.

Legacy broad-push workflow failures on isolated branches are not authoritative runtime gates. A branch-specific gate must provide attributable executable evidence before it can be promoted to PASS or FAIL for source correctness.

Repeated zero-step failures currently affect both isolated PR #97 and PR #98 materializers. Repeated reruns are not useful evidence while this infrastructure condition persists.

## 6. Runtime session evidence hygiene

The companion record `R1_RUNTIME_SESSION_ISOLATION_AND_OBSERVER_PROFILE_20260827.md` governs the current operator session.

Pre-existing `StrategyID=1 / InstanceID=0` terminal persistence records must not be deleted merely to obtain a clean-looking R1 run.

If no fresh attributable R1 ticket exists, a new R1 campaign should use one fresh matching StrategyID/InstanceID namespace on both EA and Observer after automated execution is stopped and the namespace is verified clean. If a fresh R1 ticket already exists, identity inputs must not be changed mid-trade.

## 7. Master index historical-snapshot note

`MASTER_R1_R6_RUNTIME_EVIDENCE_INDEX_20260827.md` contains historical blocker wording from an earlier preparation stage in addition to the current R1-R6 matrix. Historical statements that P0/#94 is still pending must not override later canonical closure records:

- P0 broker-runtime acceptance: PASS;
- IP-01..IP-12: complete;
- Issue #94: closed/completed;
- Issue #96: current R1 runtime tracker.

The large master index is intentionally not rewritten by this audit merely to normalize historical prose. Current stage authority comes from the later freeze/handoff, Issue #96, and this coherence record.

## 8. Main branch boundary

`main` is not part of the active R1 runtime attribution and must not be advanced by these isolated PRs or documentation audits.

## 9. Verdict

**PASS — R1 CANONICAL FREEZE PRESERVED.**

New NMJE/dashboard hardening is quarantined in draft PRs, source materialization remains blocked by zero-step CI/runner availability failures, no lifecycle default is activated, canonical EA source remains unchanged, R1 remains INCOMPLETE, and R2-R6 remain blocked until predecessor evidence is closed.