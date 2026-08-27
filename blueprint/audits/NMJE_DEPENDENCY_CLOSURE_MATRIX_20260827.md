# NMJE Dependency Closure Matrix — 2026-08-27

Status: DOCUMENTATION-ONLY CONSOLIDATION — NO EA SOURCE CHANGE
Purpose: consolidate DEP-A01..DEP-A09 into one pre-N3 dependency view while the current runtime candidate remains untouched.

## Completed dependency audits
- DEP-A01 — M11 D1 strategic owner: DONE
- DEP-A02 — M12 Re-Entry owner/lifecycle: DONE
- DEP-A03 — M08 Extreme owner/lifecycle: DONE
- DEP-A04 — M09 MHV/MLV lifecycle identity: DONE
- DEP-A05 — M10 direction/Momentum/eCSD/CSD/CSM: DONE
- DEP-A06 — M27 orchestration/synchronization: DONE
- DEP-A07 — M15 final-authority/NMJE consumer: DONE
- DEP-A08 — M16 frozen-owner/journey revalidation: DONE
- DEP-A09 — M24 recovery/replay readiness: DONE

## Cross-cutting closure groups

### G1 — Canonical event identity
Applies: M11/M12/M08/M09, consumed by M12N/M15/M16/M24.
Need: deterministic immutable owner/event identity derived only from canonical source-owned facts.
Do not add scoring, confidence or heuristic parentage.
Status: REQUIRED BEFORE N3 JourneyID freeze.

### G2 — Single-writer authority
Canonical owner modules must be the only writers of their strategy state.
Key finding: M09's current supersession helper can directly install an Extreme parent; this must be reconciled with M08 single-writer ownership before N3.
Status: ARCHITECTURAL HARDENING REQUIRED.

### G3 — Monotonic terminal states / supersession
VOID/SUPERSEDED/expired/retired owner states must not resurrect from stale snapshots or restart order.
Status: REQUIRED BEFORE REPLAY LOCK.

### G4 — Type/lifecycle-specific freshness vs canonical validity
Project freshness windows must not erase source-owned structural provenance. Type-1 Re-Entry remains structural/no invented fixed timeout. Pre-maturity components remain observation-only.
Status: CONTRACT + CODE AUDIT REQUIRED BEFORE N3.

### G5 — Owner synchronization epoch
ProcessPair ordering is substantially correct, but N3 needs an explicit processing epoch/barrier proving owner updates are complete before NMJE evaluates exactly once.
Status: M27 N3 HARDENING REQUIRED.

### G6 — M15/M16 frozen NMJE payload
M15 must freeze JourneyID/verdict/provenance/reason/epoch for the exact selected candidate; M16 revalidates that frozen identity without recreating strategy logic.
Status: N3 INTEGRATION REQUIRED.

### G7 — WAIT vs BLOCK semantics
BUILDING/WAIT cannot be automatically rejected. Only contract-defined CONFLICT/UNRESOLVED/SUPERSEDED/invalid states may block.
Status: N3 CONTRACT REQUIRED.

### G8 — New-entry vs live-trade separation
NMJE may gate pending/new entries. It must not create an implicit broker-close rule for live positions.
Status: PERMANENT INVARIANT.

### G9 — Deterministic replay/recovery
Canonical owners recover first; NMJE lineage recovers second. Identical closed-candle history must produce identical owner states, JourneyID, verdict and reason before/after restart.
Status: MANDATORY PRE-PRODUCTION TEST GATE.

### G10 — M10 semantic dedup
M10 direction/Momentum predicates remain canonical event evidence. M08/M09/M12 may consume them, but NMJE must not implement another copy. Existing duplicate Momentum semantics between M08 helper and M10 should be reconciled without changing BBMA definition.
Status: STATIC ARCHITECTURE AUDIT REQUIRED.

## What can continue while runtime candidate is active
- N1/N1.1 observer correctness review;
- N2 shadow telemetry/evidence review;
- contract/schema drafting for identities, reason codes and WAIT/BLOCK semantics;
- documentation synchronization;
- replay scenario specification.

## What must wait until runtime evidence/freeze is released
- changes to BBMA_EA.mq4 affecting owner identities/lifecycles/orchestration;
- M15/M16 mandatory N3 gating;
- M24 NMJE recovery implementation;
- M12N limiter raise to EXPERT-RESTRICTED production N3;
- new build identifier + compile/runtime regression.

## Recommended next safe sequence
1. reconcile this matrix into the N3 hardening queue;
2. audit N1/N1.1 observer correctness against the now-documented dependency expectations;
3. audit N2 shadow evidence/coverage and identify missing scenarios;
4. draft N3 pre-enforcement contract/schema documentation;
5. stop before source modification if the current runtime candidate still needs evidence.
