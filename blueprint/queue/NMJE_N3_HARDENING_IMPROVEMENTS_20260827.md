# NMJE N3 Hardening Improvement Queue — 2026-08-27

Status: **QUEUED / EXECUTE IN DEPENDENCY-HARDENING -> N1/N2 -> N3 PRE-ENFORCEMENT ORDER**
Owner scope: `M08–M12`, `M12N / NMJE`, `M15`, `M16`, `M24`, `M27`, with M13/M14 preserved as exact-combination owners.

## Purpose
Preserve the agreed NMJE hardening improvements and dependency refinements so they are executed at the correct stage instead of being added prematurely or lost as chat-only decisions.

## Mandatory constraints
- NMJE must remain BBMA-context/lineage infrastructure, not a new strategy or optimization filter.
- NMJE must consume canonical owner states from M08–M12; it must not redetect Extreme/MHV/Re-Entry independently.
- M15 remains final new-entry authority; M16 remains final revalidation/invalidation authority.
- M13/M14 exact REM/RRE/REE signatures and maturity requirements must remain unchanged unless a separate source-backed Core decision changes them.
- No NMJE rule may be promoted to execution authority without source/contract support and N2 shadow evidence.
- No confidence score, timeframe voting, weighted alignment, AI filter or universal perfect-nesting requirement is permitted.
- N3 production M12N limiter = `EXPERT-RESTRICTED`.

## Priority rule
Do **not** harden N3 execution logic before the owner/dependency modules are stable. The correct order is:
1. refine and synchronize dependency/owner modules;
2. validate N1/N1.1 observer correctness;
3. collect N2 shadow evidence;
4. harden and enforce N3.

## Dependency hardening before N3

### DEP-H01 — M11 D1 strategic-owner hardening
Priority: **CRITICAL**
Refine deterministic D1 owner, transition, unresolved and handover semantics so NMJE never receives ambiguous strategic ownership.
Required properties:
- closed-candle owner state only;
- explicit confirmed BUY/SELL/TRANSITION/UNRESOLVED;
- stable owner identity/anchor metadata;
- deterministic opposite-owner handover;
- no stale previous owner used as executable authority during transition.
Timing: **before N2 conclusions are promoted to N3 enforcement.**

### DEP-H02 — M12 Re-Entry owner/lifecycle hardening
Priority: **CRITICAL**
Refine Re-Entry owner identity, anchor, confirmation, invalidation, supersession and recovery provenance.
Goal: NMJE must be able to distinguish two different Re-Entry journeys even when direction/timeframe are the same.
Timing: **before N2 shadow attribution is treated as reliable.**

### DEP-H03 — M08 Extreme lifecycle/supersession hardening
Priority: **HIGH**
Verify RAW -> REVERSAL-CONFIRMED -> RETEST/ENTRY-READY maturity and atomic opposite-cycle handover remain deterministic and source-aligned.
Timing: **before N3 conflict/supersession rules are finalized.**

### DEP-H04 — M09 MHV/MLV lifecycle identity hardening
Priority: **HIGH**
Verify frozen marked-body identity, lifecycle completion, retest provenance and supersession cannot drift across journey epochs.
Timing: **before N3 journey lineage is frozen.**

### DEP-H05 — M10 direction/Momentum state hardening
Priority: **HIGH**
Ensure eCSD/CSD/CSM/Momentum progression used by owner lifecycles is explicit, closed-candle and non-duplicated inside NMJE.
Timing: **before N2/N3 progression analysis.**

### DEP-H06 — M15 NMJE-consumer hardening
Priority: **CRITICAL FOR N3**
M15 may consume only approved NMJE verdict/metadata and must remain the sole final new-entry authority.
Required design:
- setup-aware consumption;
- no universal full-chain requirement;
- WAIT/BUILDING is not automatically REJECT;
- unresolved/conflict behavior follows approved contract only;
- frozen NMJE payload belongs to the exact candidate/decision identity.
Timing: **N3 integration stage after N2 evidence.**

### DEP-H07 — M16 NMJE revalidation hardening
Priority: **CRITICAL FOR N3**
M16 revalidates frozen owner/journey provenance without reimplementing M08–M12 or M12N formulas.
Required design:
- detect owner/journey supersession;
- reject stale/unproven frozen context fail-closed;
- distinguish pending/new-entry invalidation from live-position management;
- no blanket live-trade close from an opposite event without a separate source-backed rule.
Timing: **before N3 execution enforcement.**

### DEP-H08 — M24 deterministic recovery support
Priority: **HIGH**
Recovery must restore or reconstruct owner provenance and journey identity deterministically. If evidence cannot be proven, NMJE resolves `UNRESOLVED` instead of guessing.
Timing: **after N3 state schema is stable, before production-lock.**

### DEP-H09 — M27 orchestration barrier
Priority: **HIGH**
Enforce processing order per pair/cycle:
`owner modules update -> owner-state synchronization barrier -> NMJE exactly once -> M13 -> M14 -> M15 -> M16`.
Prevent NMJE from reading a mixture of old/new owner epochs.
Timing: **before N3 runtime validation.**

## NMJE/N3 hardening improvements

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
N3 must apply only the MTF relationship required by the executable setup/contract. It must not require an invented full D1->H4->H1->M15 perfect chain for every trade when the source/approved signature does not require it.
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

### N3-H09 — Canonical event identity
Every owner event consumed by NMJE must carry deterministic identity sufficient to distinguish lineage, e.g. owner/module, timeframe, pair, anchor time, structural direction and owner epoch/cycle identity where available.
Purpose: prevent false parent-child pairing without introducing any quality score.
Timing: **dependency/schema hardening before N3 JourneyID freeze.**

### N3-H10 — Journey provenance chain
Store enough read-only provenance to explain why a child belongs to a parent and why a verdict was produced.
Examples of provenance classes: parent owner identity, child owner identity, anchor relationship, lifecycle state and supersession source.
Purpose: auditability, M16 verification and restart recovery only; never scoring.
Timing: **N2 diagnostics first, frozen into N3 schema only after evidence proves usefulness.**

### N3-H11 — Monotonic transition guard
A journey/owner state already proven `SUPERSEDED`, void or invalid must not resurrect from stale snapshots, delayed processing or restart artifacts unless the canonical owner module proves a genuinely new owner/cycle identity.
Timing: **N3 state-machine + recovery design.**

### N3-H12 — Single-writer ownership rule
Only the canonical owner module may mutate the underlying strategy state. NMJE creates derived lineage/context only; M15/M16 consume/freeze/revalidate but must not rewrite M08–M12 owner state.
Timing: **permanent architecture invariant and static regression rule.**

### N3-H13 — Closed-candle owner synchronization barrier
NMJE evaluates only after all required owner modules for the current processing cycle have completed their closed-candle updates. It must never combine mixed owner epochs from different processing passes.
Timing: **M27 orchestration hardening before N3 runtime enforcement.**

### N3-H14 — Reason-coded verdict diagnostics
In addition to the semantic verdict, expose deterministic diagnostic reason tags such as `PARENT_SUPERSEDED`, `OWNER_UNRESOLVED`, `DIRECTION_CONFLICT`, `CHILD_OUTSIDE_OWNER_CYCLE`, or equivalent names approved during contract design.
Reason codes are diagnostics only and may not become weights/scores.
Timing: **N2 shadow diagnostics, then N3 observability.**

### N3-H15 — New-entry versus live-trade journey separation
Explicitly distinguish NMJE context used to admit/reject a new candidate from provenance attached to an already-live position.
An opposite/new cycle may invalidate pending/new-entry context according to the approved lifecycle, but it must not become an implicit close-position rule unless a separate source-backed M23/M24 rule says so.
Timing: **before M16 N3 enforcement and live-position regression.**

### N3-H16 — Deterministic replay scenario library
Build a reusable replay/regression suite covering at minimum:
- Extreme -> MHV/MLV -> Re-Entry;
- Extreme A -> opposite Extreme B;
- D1/H4/H1/M15 nested chain;
- standalone H1 Re-Entry under valid/invalid HTF ownership;
- REM/RRE/REE exact signatures;
- BUILDING/WAIT -> ALIGNED;
- CONFLICT and UNRESOLVED;
- supersession;
- restart mid-journey;
- missed-candle/recovery reconstruction.
For identical canonical closed-candle history, outputs before and after restart/replay must be identical.
Timing: **develop during N2/N3 hardening; mandatory before production-lock.**

## Explicitly prohibited "improvements"
The following must not enter NMJE unless a future source-backed BBMA Core decision explicitly requires them:
- confidence percentage;
- weighted timeframe score;
- majority/timeframe voting;
- AI/ML ranking;
- hidden quality score;
- win-rate based gate;
- mandatory perfect D1->H4->H1->M15 nesting for every setup;
- new RSI/MACD/Stochastic/ADX/news/correlation/volatility/session filters;
- heuristic expiry/TTL not owned by the canonical source lifecycle.

## Execution sequence
1. Synchronize latest Core/contracts/current code and run the **NMJE Dependency Hardening Audit** over M08–M12 + M15/M16 + M24/M27.
2. Resolve dependency findings in priority order, with M11/M12 first and no unsupported BBMA additions.
3. Re-run owner-module static/native/runtime verification where affected.
4. Complete N1/N1.1 observer correctness against the stabilized owner states.
5. Complete N2 shadow/outcome evidence including reason-coded provenance diagnostics.
6. Run N3 pre-enforcement source + contract reconciliation.
7. Apply N3-H01/H02/H04/H05/H06/H08/H09/H11/H12/H13/H15 to the N3 contract/design.
8. Integrate approved NMJE verdict consumption into M15/M16 only.
9. Apply N3-H03/H10 and DEP-H08 recovery/replay hardening after the state schema stabilizes.
10. Run N3-H07 shadow-vs-enforced comparison gate.
11. Complete N3-H14 diagnostics and N3-H16 deterministic replay library.
12. Raise M12N limiter to `EXPERT-RESTRICTED` in the N3 production source.
13. Assign new unique left-aligned EA build/patch identifier.
14. Native MetaEditor compile `0E0W` + static cross-module/Core purity regression.
15. Runtime validation including aligned, building/wait, conflict, unresolved, supersession, restart, missed-candle, owner-handover and live-trade-separation scenarios.
16. Only after all gates PASS may NMJE N3 be marked production-locked.

## Completion rule
Do not mark this queue item complete merely because N3 code exists. Completion requires:
- dependency/owner-state stability;
- source/contract alignment;
- N1/N2 evidence;
- N3 implementation;
- compile-clean result;
- static regression;
- deterministic replay/recovery tests;
- runtime evidence;
- no unsupported BBMA filtering introduced;
- no M15/M16 authority leakage;
- no implicit live-position close behavior created by NMJE.