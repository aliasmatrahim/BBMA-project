# Q9 Build 4.93 P8 Parent/Child Hysteresis & Provenance Stability — 2026-09-19

Issue: #101
Branch: `q9-nmje-v2-p8-provenance-stability-101`
Base: verified P7 head `87e1417c2a99f8c595089f4d67f250fcdacfecb2`
Build: `4.93` / `V493_Q9_P8_PROVENANCE_STABILITY_20260919`
Status: SHADOW / OBSERVER STATE STABILITY ONLY / NO ACTIVATION

## Purpose

P8 stabilizes **observer provenance**, not trading authority.

Existing raw `NestedJourneyState.Relation` and current parent resolution remain unchanged. P8 adds a second read-only lane representing the last canonical relation that can still be attributed to the same immutable parent journey.

There is no fixed-bar wait, cooldown, time delay, rejection, rank or execution gate.

## Source / architecture basis

Accepted N1 recursive mapping remains controlling:
- BBMA structure is nested across related TFs;
- lower-TF activity may support/complete a higher-TF journey;
- opposite-looking child activity is not automatically an independent reversal;
- exact REM/RRE/REE signatures remain unchanged;
- M15 remains the sole processing/final-decision clock.

P8 software state is an **EA ENGINEERING MAPPING**.

## Implementation

Added observer metadata:
- `StableRelation`;
- `RelationEvidenceID`;
- `StableRelationEvidenceID`;
- `ParentTransitioned`;
- `PreviousParentEventID`;
- `StabilityReason`.

M5 shadow state also records:
- `StableRelation`;
- `StableEventID`;
- `StabilityReason`.

### Relation evidence

Stable relation may advance only from already-owned canonical identities/state:
- confirmed H1 Re-Entry;
- supporting H1/M15 Extreme;
- supporting M15 MHV/MLV;
- H4 owner identity;
- strategic D1 owner identity;
- immutable current ParentEventID/JourneyID.

Candidate/developing child state remains raw-only and cannot seed stable evidence.

### Parent transition

Parent transition is detected only from exact canonical parent identity change. Previous stable relation is not carried into a new ParentEventID/JourneyID.

No H1/M15/M5 child state is allowed to become a parent source.

### Identity-based hysteresis

For the same parent journey:
- current attributable canonical evidence updates the stable relation immediately;
- raw relation without new attributable evidence keeps the previous last-proven stable relation;
- no prior proof => stable relation initializes from raw state without claiming evidence.

This is identity-based provenance hysteresis only.

## Confirmed partial-work defect found during recovery

Classification: **CONFIRMED BUG**.

ISSUE:
The interrupted partial implementation used `journey.D1Node.CanonicalEventID` for `D1_TRANSITION` / `H4_LOCAL_OPPOSES_D1` relation evidence.

IMPACT:
`D1Node` may represent a confirmed D1 Re-Entry before the strategic D1 owner, and owner `StateCode` is not populated through that node path. The stability evidence hash could therefore attribute a D1-owner relation to the wrong D1 event.

FIX:
Use exact `NMJE_D1OwnerEventID(state.actual_symbol, state.d1_major_trend_owner)` plus `d1_major_trend_owner.State` for those owner-based reasons.

The corrected candidate was recompiled and all required runtime regression was rerun. Pre-fix Build 4.93 artifacts are superseded and are not validation evidence for the committed candidate.

## Decision attribution

P8 freezes stable-relation metadata into the already-validated in-memory `BBMA_Decision` observer snapshot.

Durable P4-P7 GlobalVariable persistence is deliberately **not widened** in this patch. Missing post-restart P8 last-proven memory therefore rebuilds fail-closed from currently provable canonical state; it does not alter trade recovery.

## Authority firewall

Exact-body unchanged P7 -> P8:
- `BuildPossibleCombinations`;
- `ValidateSequence`;
- `BuildConfirmedReEntryCandidate`;
- `BuildStandaloneExtremeCandidate`;
- `BuildD1OpportunityCandidate`;
- `CompareCanonicalCandidates`;
- `PriorityEngine_Atomic`;
- `InvalidationEngine_Atomic`;
- `CheckRiskBeforeTrade`;
- `RunEntryPreflightAndExecute`;
- `IsSignalAllowed`;
- `SendOrderWithRetry`.

P2 active deterministic ordering remains HOLD/UNRESOLVED.

No merge / no production activation.
