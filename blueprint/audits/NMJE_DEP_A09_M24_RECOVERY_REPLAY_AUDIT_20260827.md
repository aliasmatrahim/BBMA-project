# NMJE Dependency Hardening Audit — DEP-A09 M24 Recovery / Replay Readiness

Date: 2026-08-27
Status: DOCUMENTATION-ONLY AUDIT — NO EA SOURCE CHANGE

## Baseline verdict
M24 already contains strong recovery patterns for live-trade lifecycle state: persistent checkpoints, exact ticket/magic/open-time identity checks, replay cursors, fail-freeze behaviour and H4 owner replay. These are good primitives for future NMJE recovery, but NMJE journey/owner recovery itself is not yet production-ready.

## Strengths observed
- lifecycle checkpoints validate exact trade identity before restore;
- corrupted/missing identity can freeze lifecycle management rather than guess;
- missed D1 candles can be replayed sequentially from the last processed cursor;
- D1 TP-Wajib lifecycle validates exact closed candle and required MA history before advancing;
- H4 directional owner has verified checkpoint + closed-history replay support;
- recovery states are distinguished and live management skips corrupted/frozen identities.

## N3 hardening findings

### DEP-A09-F1 — NMJE journey checkpoint/rebuild schema is not yet defined
N3 needs either persisted JourneyID/provenance or deterministic reconstruction from canonical owner histories. Do not persist derived state that cannot be independently verified.

### DEP-A09-F2 — Owner recovery must precede journey recovery
M08/M09/M12/M11/H4 canonical owners must be reconstructed first. Only then may NMJE rebuild parent-child lineage. If any required owner is unresolved, NMJE returns UNRESOLVED for new-entry eligibility.

### DEP-A09-F3 — Replay equivalence is mandatory
For identical closed-candle history, uninterrupted runtime and restart/replay must produce identical canonical owner states, JourneyID, relation verdict and reason code. This must be tested for Extreme->MHV->RE, opposite supersession, standalone H1 RE, REM/RRE/REE and D1 opportunity paths.

### DEP-A09-F4 — No stale derived-state resurrection
Persisted/replayed journey state must be monotonic. A superseded/void owner or journey cannot reappear because an older checkpoint loads before newer owner history is replayed.

### DEP-A09-F5 — Separate live-trade provenance from new-entry eligibility
A live position may retain the journey identity that admitted it for diagnostics/recovery, but reconstructed current NMJE conflict cannot automatically close it. Live exits remain M23/M24/lifecycle/emergency owned.

### DEP-A09-F6 — Recovery reason codes
Add deterministic outcomes such as OWNER_RECOVERY_UNRESOLVED, JOURNEY_ID_MISMATCH, PARENT_SUPERSEDED, HISTORY_GAP and REPLAY_DIVERGENCE for diagnostics. No scores/heuristic recovery.

## N3 readiness
- General checkpoint/replay infrastructure: STRONG
- H4 owner recovery precedent: PASS
- Fail-freeze safety pattern: PASS
- NMJE-specific journey recovery: NOT YET IMPLEMENTED
- Canonical owner replay equivalence across M08/M09/M12: NOT YET PROVEN
- Safe for N1/N2: YES
- Safe for mandatory N3 after restart today: NO

## Dependency-audit series status
DEP-A01 M11: DONE
DEP-A02 M12: DONE
DEP-A03 M08: DONE
DEP-A04 M09: DONE
DEP-A05 M10: DONE
DEP-A06 M27: DONE
DEP-A07 M15: DONE
DEP-A08 M16: DONE
DEP-A09 M24: DONE

## Next safe work while runtime candidate remains untouched
1. consolidate DEP-A01..A09 into one NMJE dependency closure matrix;
2. reconcile findings into the existing NMJE N3 hardening queue without changing EA source;
3. mark which findings are N1/N2 evidence tasks vs post-freeze implementation tasks;
4. stop before any source patch that would invalidate the running runtime candidate.
