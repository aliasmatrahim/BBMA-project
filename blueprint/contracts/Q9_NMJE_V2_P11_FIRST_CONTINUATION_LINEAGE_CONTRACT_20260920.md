# Q9 NMJE v2 P11 First/Continuation Lineage Refinement Contract — 2026-09-20

Issue: #101
Base: verified P10 Build 4.94 / Draft PR #202
Target: Build 4.95 / `V495_Q9_P11_LINEAGE_REFINEMENT_20260920`
Status: SHADOW / PROVENANCE METADATA ONLY / NO ACTIVATION

## Source / architecture boundary

P11 is an **EA ENGINEERING LINEAGE MAPPING** over accepted canonical owner/event identities.
It does not change BBMA Strategy Core, parent selection, JourneyID semantics, signal eligibility,
candidate ordering, M15 final authority, validation, risk, execution or trade lifecycle.

Accepted Core remains the recurring BBMA journey:
`Extreme -> TP Wajib -> MHV/MLV -> direction -> Re-Entry -> Momentum/CSM -> further Re-Entry -> opposite Extreme / cycle restart`.

P11 MUST NOT infer that newest parent is best, earliest parent is best, or that continuation is executable authority.
## Deterministic lineage root

For a valid resolved NMJE parent, P11 derives one observer-only `LineageRootEventID`.

Fail-closed precedence:
1. confirmed valid D1 major-trend owner epoch EventID;
2. otherwise active valid H4 directional-owner EventID;
3. otherwise current canonical ParentEventID as self-root.

If D1 is TRANSITION/UNRESOLVED, or a required higher owner identity is malformed,
the lineage root is unresolved rather than silently falling back through conflicting authority.

The root is reconstructible from existing canonical owner/event identity helpers.
No new detector or duplicate lifecycle owner is created.

## Event-role classification

Categorical values are storage labels only:
- `FIRST`: current ParentEventID equals the deterministic LineageRootEventID;
- `CONTINUATION`: current ParentEventID differs from the root while the same deterministic root owns the journey;
- `NEW_JOURNEY`: current root differs from the previous valid root on consecutive M15 observations;
- `UNRESOLVED`: valid parent exists but deterministic root cannot be proven;
- `NONE`: no valid resolved parent.

`NEW_JOURNEY` is a one-observation transition marker. It does not rewrite ParentEventID or JourneyID.
## Continuation / re-arm boundary

`CONTINUATION` means only that a later canonical parent event remains under the same proven higher-owner root.
A confirmed Re-Entry may therefore be observed as a continuation under an unchanged D1/H4 root.

This label is NOT the C044/F7 trade-lifecycle `REENTRY_REARM` state and MUST NOT consume or modify C044.
P11 does not create a universal BBMA “re-arm rule”.

If no higher-owner root can prove same-journey continuity, a changed self-root is treated as NEW_JOURNEY,
not silently promoted to continuation.

## Restart behavior

On restart, derive the current root from current canonical owner/event state.
Do not synthesize a previous root that is no longer available in observer memory.

Therefore:
- FIRST/CONTINUATION may be reconstructed from current root vs current parent;
- NEW_JOURNEY requires an attributable previous root in the current observer memory;
- missing pre-restart transition history degrades to current-role metadata, never guessed transition metadata.

No P11 state is required for order/trade recovery.
## Selected-decision attribution and persistence

Only after the base decision is already DEC_VALIDATED, P11 may freeze:
- lineage class;
- LineageRootEventID;
- PreviousLineageRootEventID when a root transition is observed.

P4 ticket-bound attribution may persist additive hashes of the root identities plus lineage class.
Pre-P11 records remain readable with lineage metadata unavailable.

Persistence failure remains diagnostic only and MUST NOT alter recovery, candidate, risk, execution or lifecycle state.

## Authority invariants

P11 MUST NOT:
- modify `NMJE_ResolveParent` parent-source families or priority;
- modify `NMJE_BuildJourneyID`;
- create/reject/rank/delay candidates;
- change REM/RRE/REE signatures;
- change M13/M14/comparator/M15/M16/M17;
- change SL/TP, risk/MM, lot sizing or execution;
- activate P2 deterministic ordering;
- make M5 executable authority;
- introduce timer/bar-count/cooldown lineage semantics.

M15 remains the sole processing/final-decision clock.
## Validation exit gate

Require:
- focused P11 model/static/persistence tests PASS;
- inherited P10/P8/P7/P6/P5/P4/P2-P3/P1/read-only/M12N/D1O/N3 regressions PASS;
- protected P10 -> P11 M13/M14/comparator/M15/M16/M17/risk/preflight/order-send bodies exact-equal;
- broker primitive counts unchanged;
- native MetaEditor 0 errors / 0 warnings;
- deterministic Strategy Tester P11 A/B on verified GBPUSD M15 August window;
- exact P10/P11 M15/M16/decision authority-trace equality;
- natural FIRST/CONTINUATION/NEW_JOURNEY runtime coverage where present;
- no broker actions in the safety profile;
- no merge / no production activation.

If NEW_JOURNEY or CONTINUATION is not naturally observed in the bounded tester window,
classify that branch BOUNDED-UNEXERCISED rather than synthesizing an event.
