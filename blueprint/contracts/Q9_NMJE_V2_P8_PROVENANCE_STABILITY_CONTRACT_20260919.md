# Q9 NMJE v2 P8 Parent/Child Hysteresis & Provenance Stability Contract — 2026-09-19

Issue: #101
Base: verified P7 Build 4.92 / Draft PR #199
Target: Build 4.93 / `V493_Q9_P8_PROVENANCE_STABILITY_20260919`
Status: SHADOW / OBSERVER STATE STABILITY ONLY / NO ACTIVATION

## Source / architecture boundary

P8 is an **EA ENGINEERING MAPPING** over the already-approved N1 recursive BBMA context layer.

Accepted source facts remain:
- BBMA structure is recursive/nested across related timeframes;
- lower-timeframe structures may support/complete a higher-timeframe journey;
- an opposite-looking lower-timeframe structure does not automatically prove an independent reversal;
- exact REM/RRE/REE signatures remain unchanged;
- canonical cycle remains `Extreme -> TP Wajib -> MHV/MLV -> direction -> Re-Entry -> Momentum/CSM -> ... -> opposite Extreme / cycle restart`.

P8 does not add a BBMA setup, detector, entry rule, rejection rule, score or timeframe authority.

## Raw state versus stable observer state

Existing `NestedJourneyState.Relation` remains the instantaneous/raw observer relation for backward comparability.

P8 adds a separate **last-proven stable relation**:
- `StableRelation`;
- `RelationEvidenceID` for the current raw relation when attributable;
- `StableRelationEvidenceID` for the last accepted stable relation;
- `StabilityReason`.

The stable relation is diagnostic/research metadata only.

P8 does not silently rewrite the raw current relation.

## Canonical relation evidence

A stable-relation transition is attributable only when its evidence fingerprint is built from already-owned canonical identities/state:
- current ParentEventID / JourneyID;
- H1 Re-Entry candidate/confirmed EventID + state;
- H1 Extreme EventID + maturity;
- M15 Re-Entry candidate/confirmed EventID + state;
- M15 Extreme EventID + maturity;
- M15 MHV/MLV EventID + lifecycle state;
- current D1/H4 owner identity when the relation reason is owner/transition based.

The evidence fingerprint is an engineering hash. It is not strategy authority.

No detector is duplicated. P8 only hashes existing owner/lifecycle identities.

## Stable-relation transition rule

For one unchanged ParentEventID/JourneyID:
1. if the current raw relation has attributable canonical relation evidence, the stable relation follows the raw relation and stores that evidence identity;
2. if the current raw relation has **no new attributable relation evidence** (for example, current parent merely waits with no child context) and a last-proven stable relation exists for the same parent journey, keep the last-proven stable relation;
3. if no last-proven relation exists, initialize stable relation from the raw relation but leave stable evidence absent.

When ParentEventID/JourneyID changes:
- do not carry the previous stable relation into the new journey;
- initialize the new stable state from the new journey's current raw relation/evidence;
- emit explicit parent-transition metadata.

This is identity-based hysteresis. There is no minimum candle count, fixed bar hold, timer, cooldown or delayed entry.

## Parent provenance transition

Existing raw parent resolution remains canonical-source driven and observer-only.

P8 records:
- previous ParentEventID;
- whether the parent changed this M15 observation;
- transition reason.

A child candidate by itself cannot rotate parent identity.

Parent changes remain attributable only to the canonical parent sources already consumed by `NMJE_ResolveParent`:
- confirmed H4 Re-Entry;
- active valid H4 owner;
- confirmed D1 Re-Entry;
- confirmed valid D1 owner.

P8 must not make candidate H1/M15/M5 state a parent source.

## M5 child stability

Existing P5 raw M5 relation remains unchanged.

P8 adds M5 last-proven observer fields:
- stable M5 relation;
- stable M5 EventID;
- stability reason.

A current M5 context becomes **stable evidence** only when its own existing canonical maturity is sufficiently resolved for provenance:
- confirmed M5 Re-Entry;
- reversal-confirmed / retest-phase / retest-ready M5 Extreme.

M5 Re-Entry candidate and RAW Extreme remain current/raw shadow context but do not replace a last-proven stable M5 relation merely by appearing for one observation.

If current M5 context is absent/unresolved/developing and the parent JourneyID/ParentEventID is unchanged, the previous stable M5 relation may remain as **historical last-proven metadata only**.

A parent transition clears M5 stable carry-forward.

Raw `M5Refinement.Present` remains false when there is no current M5 context; P8 does not manufacture M5 presence.

## Restart behavior

P1 canonical ParentEventID/JourneyID remains reconstructible from canonical owner/event identities.

P8 last-proven in-memory stable relation is **not execution state** and is not required for trade recovery.

After process restart, if no previous P8 observer memory exists:
- rebuild raw parent/journey/relation from current canonical closed-candle state;
- initialize stable relation only from currently provable evidence;
- do not invent or backfill a pre-restart last-proven relation.

Selected-decision attribution may persist P8 stable-relation metadata independently; missing P8-only keys in older records degrade to unavailable research metadata and never alter recovery or execution.

## Selected-decision attribution

Only after the base decision is already `DEC_VALIDATED`, P8 may freeze:
- stable base relation;
- stable relation evidence identity/hash;
- parent-transition flag / previous parent identity for research attribution.

This metadata is additive to P4/P6/P7 and cannot alter trade lifecycle.

Pre-P8 records remain backward-readable.

## Authority invariants

P8 MUST NOT:
- create/reject/rank/delay a candidate;
- change parent source families;
- change REM/RRE/REE signatures;
- change M13/M14 collection/validation;
- change `CompareCanonicalCandidates`;
- change `PriorityEngine_Atomic`;
- activate P2 ordering;
- change M16;
- change SL/TP, risk/MM, lot sizing or execution;
- introduce any time/bar-count hysteresis;
- turn stable relation into an execution gate;
- create a second processing clock.

M15 remains sole processing/final-decision clock.

## HOLD

P2 deterministic active ordering remains HOLD/UNRESOLVED.

P8 stable relation does not authorize `ALIGNED > SUPPORTING > BUILDING > CONFLICT` ordering, scoring or filtering.

## Validation exit gate

Require:
- focused P8 static/model PASS;
- inherited P7/P6/P5/P4/P2-P3/P1/read-only/M12N/D1O/N3 regressions PASS;
- protected M13/M14/comparator/M15/M16/risk/preflight/execution bodies exact-equal to P7;
- native MetaEditor 0 errors / 0 warnings;
- Strategy Tester P8 A/B deterministic replay on the verified GBPUSD M15 August window;
- exact P7-vs-P8 authority-trace equality;
- natural P8 stable-relation and parent-transition telemetry coverage;
- zero broker-action markers;
- no merge / no production activation.
