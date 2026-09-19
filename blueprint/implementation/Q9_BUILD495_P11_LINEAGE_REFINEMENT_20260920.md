# Q9 Build 4.95 P11 First/Continuation Lineage Refinement — 2026-09-20

Issue: #101
Branch: `q9-nmje-v2-p11-lineage-refinement-101`
Base: verified P10 commit `dcf9d6a627e24dbc65b95b7374a5decc2a006fa2`
Build: `4.95` / `V495_Q9_P11_LINEAGE_REFINEMENT_20260920`
SourceRev: `Q9_P11_LINEAGE_REFINEMENT_101_20260920`
Status: SHADOW / PROVENANCE METADATA ONLY / NO ACTIVATION

## Purpose

P11 distinguishes observer-only parent-event lineage roles without changing BBMA authority:
- FIRST: current parent equals the deterministic lineage root;
- CONTINUATION: later canonical parent event under the same proven higher-owner root;
- NEW_JOURNEY: current deterministic root changed from a previous canonical root;
- UNRESOLVED/NONE: fail-closed metadata states.

This is an EA engineering lineage mapping. It is not a new BBMA entry, exit, filter, rank, score or re-arm rule.

## Deterministic root

`NMJE_ResolveLineageRootEventID()` resolves provenance root in fail-closed order:
1. valid confirmed D1 owner epoch EventID;
2. otherwise active valid H4 owner EventID;
3. otherwise current ParentEventID as self-root.

D1 TRANSITION/UNRESOLVED does not silently fall through.
All usable lineage EventIDs must be canonical 16-character identities.

## State / attribution additions

`NestedJourneyState` adds:
- `LineageClass`;
- `LineageRootEventID`;
- `PreviousLineageRootEventID`;
- `LineageReason`.

Validated decision attribution freezes the same observer fields after `DEC_VALIDATED`.
P4 ticket-bound research attribution adds optional:
- lineage class;
- lineage-root hash;
- previous-lineage-root hash.

Pre-P11 attribution remains readable when P11 keys are absent.
Persistence failure cannot alter candidate, recovery, risk, execution or trade lifecycle.

## Runtime telemetry

P11 emits:
`[Q9-P11-LINEAGE] Pair=... LC=... LR=... PLR=... PE=... J=... R=...`

The row is observer telemetry only and is not consumed by executable authority.

## Confirmed bug found during validation

Initial runtime A/B exposed one startup row classified `NEW_JOURNEY` while `PLR` was empty.

Classification: CONFIRMED BUG.

Cause:
the initial implementation treated `previous.LineageRootEventID != ""` as sufficient prior-root proof. A malformed/non-canonical startup observer string could therefore pass the non-empty comparison even though it was not a valid canonical EventID.

Fix:
- add `NMJE_IsCanonicalLineageEventID()`;
- require exact 16-character canonical identity for current D1/H4/self roots;
- require a canonical previous root before classifying `NEW_JOURNEY`;
- malformed prior observer state degrades to current FIRST/CONTINUATION semantics rather than fabricating a transition.

Post-fix Strategy Tester has zero phantom NEW_JOURNEY rows.

## Authority preservation

P10 -> P11 exact body equality is preserved for:
- M13 combination construction;
- M14 sequence validation/candidate construction;
- canonical comparator;
- M15 PriorityEngine;
- M16 invalidation;
- execution-reference resolution;
- M17 SL/TP resolver;
- risk;
- preflight;
- signal allowance;
- broker SendOrderWithRetry.

No parent-source family or `NMJE_BuildJourneyID()` semantics were changed.
P2 remains HOLD/UNRESOLVED.
M5 remains shadow/context only.
