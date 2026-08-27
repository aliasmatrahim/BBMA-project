# NMJE Dependency Hardening Audit — DEP-A06 M27 Orchestration / Synchronization Barrier

Date: 2026-08-27
Status: DOCUMENTATION-ONLY AUDIT — NO EA SOURCE CHANGE

## Baseline verdict
Current ProcessPair() ordering is substantially compatible with the intended NMJE architecture: market snapshots are built, D1/H4 owners updated, M08/M09/M10/M12 owner states are advanced, C044/D1 opportunity lifecycle is advanced, D1 opportunity is materialized, then NMJE observation runs before M15 PriorityEngine and M16 invalidation. This is a good baseline for N1/N2.

## Strengths observed
- one per-pair processing guard (`is_processing`);
- one frozen scan processing time;
- closed D1/H4/H1/M15 snapshots are built before owner evaluation;
- D1 strategic owner and H4 owner update before downstream candidate selection;
- M08 Extreme lifecycles across D1/H4/H1/M15 are updated before final decision;
- both direction passes update canonical owner/candidate state before D1 opportunity and NMJE observation;
- `UpdateNestedJourneyObservation()` runs before `PriorityEngine_Atomic()`;
- M15 remains final decision selector; M16 only runs on an actual M15-created decision;
- N2 is shadow-only and does not alter execution.

## Hardening findings before N3

### DEP-A06-F1 — Formal owner synchronization barrier is implicit
Ordering is currently encoded procedurally in ProcessPair(), but there is no explicit epoch/barrier object proving all required owner modules belong to the same processing pass.
Action: introduce a lightweight read-only processing epoch/snapshot identity for N3 consumption. NMJE evaluates only when required owner updates for that epoch are complete.

### DEP-A06-F2 — Mixed-timeframe freshness must be explicit
All TF snapshots are closed, but D1/H4/H1 naturally refer to different candle timestamps. N3 must distinguish valid MTF asynchrony from stale/mixed processing state.
Action: freeze each owner source candle + current processing epoch; do not require equal candle times across TFs.

### DEP-A06-F3 — NMJE exactly-once invariant should be enforced
Current placement suggests one call per ProcessPair() pass. N3 should make this an explicit invariant so a refactor/timer/tick path cannot evaluate it twice against partially changed state.
Action: store `LastNMJEEpoch`/equivalent diagnostic identity and fail closed on duplicate/incomplete evaluation.

### DEP-A06-F4 — Owner-write completion should precede candidate assembly consistently
Current owner updates and candidate assembly are interleaved inside direction loops. This works today, but N3 hardening should define a clear phase boundary: canonical owner updates complete -> synchronization barrier -> derived combination assembly/NMJE -> M15/M16.
Action: prefer phase separation during future refactor, without changing BBMA strategy semantics.

### DEP-A06-F5 — Live-position management is intentionally outside NMJE new-entry path
ManagePortfolio()/ManagePositions() execute before pair scanning. N3 must not accidentally reinterpret a new-entry NMJE conflict as an automatic live-position close.
Action: preserve explicit new-entry vs live-trade separation; live exits remain under M23/M24/lifecycle/emergency contracts.

### DEP-A06-F6 — Restart/recovery gate must complete before N3 eligibility
H4 recovery and other persisted lifecycle recovery exist elsewhere. N3 evaluation must not run as authoritative when required canonical owners are still recovery-unresolved.
Action: formal readiness flag/barrier per required owner set; unresolved -> NMJE UNRESOLVED for new-entry use.

## N3 readiness
- Basic processing order: PASS
- NMJE before M15/M16: PASS
- M15/M16 authority boundary: PASS
- Formal synchronization epoch/barrier: HARDEN
- Exactly-once invariant: HARDEN
- Recovery readiness barrier: HARDEN
- New-entry/live-trade separation: PRESERVE
- Safe for N1/N2: YES
- Safe for mandatory N3 today: NO

## Timing
Implement only after current runtime evidence is preserved and after N3 schema/owner identities are defined.

## Next
DEP-A07 — M15 NMJE-consumer/final-authority audit.
