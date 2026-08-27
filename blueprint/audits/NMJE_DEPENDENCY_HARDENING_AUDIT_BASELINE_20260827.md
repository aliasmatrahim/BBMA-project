# NMJE Dependency Hardening Audit — Baseline Pass (2026-08-27)

Status: **DOCUMENTATION-ONLY / SAFE DURING ACTIVE RUNTIME OBSERVATION**

## Purpose
Start Step 1 of the queued NMJE hardening sequence without modifying the active EA source while runtime/order evidence is still being collected.

This pass establishes the current repository baseline and identifies documentation/code-state drift that must be reconciled before N3 enforcement work.

## Baselines checked
- Active implementation branch source: `d1-owner-dev/blueprint/source/BBMA_EA.mq4`.
- Current source header observed: **Version 4.5.9 — P0 Execution Identity Persistence Fix**.
- NMJE contract: `blueprint/contracts/M12N_NESTED_MTF_JOURNEY_ENGINE_CONTRACT.md`.
- NMJE hardening queue: `blueprint/queue/NMJE_N3_HARDENING_IMPROVEMENTS_20260827.md`.
- Canonical master queue: `blueprint/MASTER_QUEUE.md`.

## Baseline findings

### DEP-A00-01 — Master Queue / implementation drift
Severity: **HIGH / GOVERNANCE**
Status: **CONFIRMED**

`MASTER_QUEUE.md` is reconciled to 2026-08-24 and still contains historical wording that M11 has no dedicated D1 owner implementation. The current `d1-owner-dev` source already contains `D1MajorTrendOwner d1_major_trend_owner` inside `PairState`, and the active source header is now 4.5.9.

Decision: do not use the older queue wording as proof of the current code state. Before any new source patch, reconcile `CURRENT.md`, `MASTER_QUEUE.md`, current contracts/audits and the actual 4.5.9 source lineage.

### DEP-A00-02 — NMJE remains observation-only in current locked contract
Severity: **INFO / ARCHITECTURE**
Status: **CONFIRMED**

The M12N contract still defines N1 as read-only context/lineage infrastructure between owner modules and M13, with M15/M16 retaining final authority. Current source globals also label `g_nested_journeys` as N1 observation only.

Decision: no N3 execution assumption is permitted yet.

### DEP-A00-03 — Central owner-state container exists
Severity: **INFO / POSITIVE BASELINE**
Status: **CONFIRMED**

Current `PairState` already centralizes D1/H4/H1/M15 timeframe data plus Re-Entry states, H4 directional owner, D1 major-trend owner, Extreme lifecycles and MHV/MLV-related state. This is a suitable base for deterministic NMJE consumption provided each owner identity/provenance is audited and remains single-writer.

Decision: prefer consuming/fixing owner metadata at the owner modules rather than duplicating detection logic inside M12N.

### DEP-A00-04 — Existing recovery infrastructure is not yet proof of NMJE recovery
Severity: **MEDIUM**
Status: **OPEN / VERIFY LATER**

Current `TradeInfo` contains deterministic persistence/replay fields for existing execution/C044/D1 TP-Wajib lifecycles. This proves the project has recovery infrastructure patterns, but it does **not** by itself prove that NMJE JourneyID/parent-child provenance can be reconstructed deterministically after restart.

Decision: keep DEP-H08 / N3-H03 open. Do not reuse unrelated recovery state implicitly as NMJE provenance.

### DEP-A00-05 — Processing snapshot foundation exists, synchronization barrier still needs explicit audit
Severity: **MEDIUM**
Status: **PARTIAL / VERIFY**

The source has a frozen `g_processing_time` and `TimeframeSnapshot` construction for D1/H4/H1/M15 closed candles. This is a useful prerequisite for N3-H13, but the full owner-update -> synchronization barrier -> NMJE exactly once -> M13 -> M14 -> M15 -> M16 ordering still requires a dedicated M27 call-order audit.

Decision: DEP-H09 remains open until call-order evidence is recorded.

## Module-by-module audit order now locked
1. **M11** — D1 owner identity, transition/unresolved, handover, recovery provenance.
2. **M12** — Re-Entry owner identity, anchors, confirmation, invalidation, supersession, recovery.
3. **M08** — Extreme maturity and atomic opposite-cycle handover.
4. **M09** — MHV/MLV frozen identity, provenance and supersession.
5. **M10** — eCSD/CSD/CSM/Momentum state ownership and closed-candle progression.
6. **M27** — call-order/synchronization barrier and exactly-once NMJE update.
7. **M15** — setup-aware NMJE consumption design; authority remains M15.
8. **M16** — frozen journey/owner revalidation; no duplicate formulas and no implicit live-trade close.
9. **M24** — deterministic NMJE replay/recovery once the N3 schema is stable.

## Runtime-freeze rule
No EA source patch is authorized by this baseline audit. While the user is waiting for live/open-order evidence, continue only documentation, repository reconciliation, static review and queue/audit preparation that do not alter the active runtime candidate.

## Next documentation-only action
Run **DEP-A01: M11 D1 Owner Dependency Audit** against the latest 4.5.9 source + M11 contract/decision records, then classify each requirement as `PASS / PARTIAL / GAP / RUNTIME-PENDING` without changing EA source.

## Completion state
Baseline pass: **COMPLETE**.
Dependency hardening workstream: **ACTIVE / SOURCE PATCHES DEFERRED DURING RUNTIME OBSERVATION**.
