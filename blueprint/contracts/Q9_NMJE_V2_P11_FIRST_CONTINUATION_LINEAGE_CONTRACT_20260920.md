# Q9 NMJE v2 P11 Strict Canonical Journey Lineage Contract — 2026-09-20

Issue: #101
Base: verified P10 Build 4.94 / Draft PR #202
Target: Build 4.96 / `V496_Q9_P11_STRICT_JOURNEY_LINEAGE_20260920`
Status: SHADOW / PROVENANCE METADATA ONLY / NO ACTIVATION

## Source / architecture boundary

P11 is an **EA ENGINEERING LINEAGE MAPPING** over accepted canonical owner/event identities.
It does not change BBMA Strategy Core, parent selection, JourneyID semantics, signal eligibility,
candidate ordering, M15 final authority, validation, risk, execution or trade lifecycle.

Accepted Core remains the recurring BBMA journey:
`Extreme -> TP Wajib -> MHV/MLV -> direction -> Re-Entry -> Momentum/CSM -> further Re-Entry -> opposite Extreme / cycle restart`.

P11 MUST NOT infer that newest parent is best, earliest parent is best, or that continuation is executable authority.
## Deterministic lineage root

User decision A locks **strict canonical JourneyID semantics**.

For a valid resolved NMJE journey, P11 sets observer-only `LineageRootEventID`
to the exact canonical `ParentEventID` already used by `NMJE_BuildJourneyID()`.

A broader D1/H4 owner family is context only. It MUST NOT merge two different
`ParentEventID/JourneyID` values into one same-journey lineage.

If ParentEventID is missing/malformed or JourneyID is unavailable, lineage is unresolved.
No new detector, lifecycle owner or alternative JourneyID is created.

## Event-role classification

Categorical values are storage labels only:
- `FIRST`: current canonical ParentEventID is the root event of the current JourneyID;
- `CONTINUATION`: reserved for a distinct source-owned continuation/re-arm event identity that can be proven inside the unchanged canonical JourneyID;
- `NEW_JOURNEY`: previous valid ParentEventID/JourneyID differs from the current canonical ParentEventID/JourneyID;
- `UNRESOLVED`: required canonical lineage identity cannot be proven, including any attempted continuation without a distinct source-owned continuation-event identity;
- `NONE`: no valid resolved parent.

`NEW_JOURNEY` is a one-observation transition marker. It does not rewrite ParentEventID or JourneyID.
## Continuation / re-arm boundary

`CONTINUATION` requires a distinct source-owned continuation-event identity inside the unchanged
canonical JourneyID. The current owner model does not expose such a separate identity.

Therefore Build 4.96 MUST NOT infer CONTINUATION from elapsed M15 observations, an unchanged D1/H4
owner family, or a later ParentEventID that would itself change JourneyID. The current canonical root
remains `FIRST`; a ParentEventID/JourneyID transition is `NEW_JOURNEY`; any attempted continuation
without a distinct identity is fail-closed `UNRESOLVED`.

This label is NOT the C044/F7 trade-lifecycle `REENTRY_REARM` state and MUST NOT consume or modify C044.
P11 does not create a universal BBMA “re-arm rule”.

## Restart behavior

On restart, derive the current root from current canonical owner/event state.
Do not synthesize a previous root that is no longer available in observer memory.

Therefore:
- current canonical root may be reconstructed as FIRST;
- CONTINUATION is not reconstructed without a distinct source-owned continuation-event identity;
- NEW_JOURNEY requires attributable previous ParentEventID/JourneyID observer memory;
- missing pre-restart transition history never fabricates NEW_JOURNEY or CONTINUATION.

No P11 state is required for order/trade recovery.
## Selected-decision attribution and persistence

Only after the base decision is already DEC_VALIDATED, P11 may freeze:
- lineage class;
- LineageRootEventID;
- PreviousLineageRootEventID when a root transition is observed.

P4 ticket-bound attribution may persist additive hashes of the root identities plus lineage class.
Pre-P11 records remain readable with lineage metadata unavailable.

Under strict-A:
- durable lineage persistence may write only FIRST or NEW_JOURNEY;
- CONTINUATION must not be written without a distinct source-owned continuation-event identity;
- a legacy Build 4.95 persisted CONTINUATION is read fail-closed as UNRESOLVED rather than accepted under Build 4.96 semantics.

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
