# NMJE N3 Hardening Improvement Queue — 2026-08-27

Status: **QUEUED / EXECUTE AT N3 PRE-ENFORCEMENT + N3 IMPLEMENTATION GATES**
Owner scope: `M12N / NMJE`, with integration impact to `M15`, `M16`, recovery/orchestration where explicitly required.

## Purpose
Preserve the agreed NMJE hardening improvements so they are executed at the correct stage instead of being added prematurely or lost as chat-only decisions.

## Mandatory constraints
- NMJE must remain BBMA-context/lineage infrastructure, not a new strategy or optimization filter.
- NMJE must consume canonical owner states from M08–M12; it must not redetect Extreme/MHV/Re-Entry independently.
- M15 remains final new-entry authority; M16 remains final revalidation/invalidation authority.
- No NMJE rule may be promoted to execution authority without source/contract support and N2 shadow evidence.
- N3 production M12N limiter = `EXPERT-RESTRICTED`.

## Queued improvements

### N3-H01 — Deterministic journey state machine
Implement explicit `JourneyID`, parent/child identity, owner, epoch and deterministic transitions. Avoid heuristic or score-based lineage guessing.
Timing: **N3 design/contract gate, before execution enforcement.**

### N3-H02 — Separate WAIT from BLOCK
Do not treat every incomplete/building relation as rejection. Distinguish at minimum semantic outcomes equivalent to `WAIT/BUILDING`, `VALID/ALIGNED`, `BLOCK/CONFLICT`, `UNRESOLVED`, and `SUPERSEDED` where supported by the approved contract.
Timing: **before M15/M16 consume NMJE as a gate.**
Goal: reduce false rejection/over-filtering while preserving fail-closed behavior for true uncertainty.

### N3-H03 — Deterministic snapshot/replay recovery
Persist or deterministically reconstruct enough journey identity so restart/missed-candle recovery cannot silently invent parentage. Missing or contradictory evidence must fail closed/freeze rather than guess.
Timing: **after N3 state schema is stable, before production-lock/runtime recovery tests.**

### N3-H04 — Canonical upstream-owner-only inputs
NMJE consumes M08–M12 owner/state outputs only. No duplicate Extreme/MHV/Re-Entry formulas inside M12N.
Timing: **continuous invariant; verify during every N3 static regression.**

### N3-H05 — Scope-aware gating, not universal perfect nesting
N3 must apply only the MTF relationship required by the executable setup/contract. It must not require an invented full D1→H4→H1→M15 perfect chain for every trade when the source/approved signature does not require it.
Timing: **M15/M16 integration design.**
Goal: prevent NMJE becoming an unsupported extra strategy filter.

### N3-H06 — Explicit supersession semantics
Opposite/new-cycle events must supersede only the journey/candidate/provenance that the approved lifecycle says is superseded. Do not interpret an opposite event as an automatic instruction to close every live trade unless a separate source-backed live-position rule exists.
Timing: **N3 conflict/invalidation contract stage before M16 enforcement.**

### N3-H07 — Shadow comparison before enforcement
Use N2 evidence to compare `WITH_NMJE` versus existing canonical eligibility/decision outcomes. Enforcement is allowed only where NMJE behavior is source-faithful, deterministic and regression-safe.
Timing: **mandatory gate immediately before enabling N3 execution authority.**

### N3-H08 — Preserve M15/M16 authority boundary
M12N supplies context verdict/metadata. M12N must not call order execution, independently select trades, alter REM/RRE/REE signatures, or become a second final authority.
Timing: **permanent architecture invariant.**

## Execution sequence
1. Finish/synchronize current Core/contract/code gaps affecting NMJE inputs.
2. Complete N1/N1.1 observer correctness and N2 shadow/outcome evidence.
3. Run N3 pre-enforcement source + contract reconciliation.
4. Apply N3-H01, H02, H04, H05, H06 and H08 to the N3 contract/design.
5. Integrate approved NMJE verdict consumption into M15/M16 only.
6. Apply N3-H03 recovery/replay hardening after state schema stabilizes.
7. Run N3-H07 shadow-vs-enforced comparison gate.
8. Raise M12N limiter to `EXPERT-RESTRICTED` in the N3 production source.
9. Assign new unique left-aligned EA build/patch identifier.
10. Native MetaEditor compile `0E0W` + static cross-module/Core purity regression.
11. Runtime validation including aligned, building/wait, conflict, unresolved, supersession, restart and missed-candle scenarios.
12. Only after all gates PASS may NMJE N3 be marked production-locked.

## Completion rule
Do not mark this queue item complete merely because N3 code exists. Completion requires contract alignment, implementation, compile-clean result, static regression, recovery tests and runtime evidence with no unsupported BBMA filtering introduced.
