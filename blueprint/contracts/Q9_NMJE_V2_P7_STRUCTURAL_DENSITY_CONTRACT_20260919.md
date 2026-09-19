# Q9 NMJE v2 P7 Structural Density / Sequence Completeness Contract — 2026-09-19

Issue: #101
Base: verified P6 Build 4.91 / Draft PR #198
Target: Build 4.92 / `V492_Q9_P7_STRUCTURAL_DENSITY_20260919`
Status: SHADOW / ATTRIBUTION METADATA ONLY / NO ACTIVATION

## Source boundary

P7 consumes only already-owned canonical BBMA state and the exact already-valid candidate payload:
- accepted Core cycle:
  `Extreme -> TP Wajib -> MHV/MLV -> direction (eCSD/CSD) -> Re-Entry -> Momentum/CSM -> further Re-Entry -> opposite Extreme / cycle restart`;
- F2 Extreme maturity;
- F1 MHV/MLV lifecycle and its mandatory prior Extreme + TP-Wajib provenance;
- canonical H4 directional-owner source state;
- canonical Re-Entry lifecycle;
- immutable P1/P6 journey provenance;
- exact candidate components already admitted by M13/M14 and existing standalone-candidate builders.

Exact REM/RRE/REE signatures remain unchanged:
- REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV;
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme;
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

P7 does not reinterpret these signatures or add missing stages as requirements.

## Engineering mapping

The P7 structural-density fingerprint is an **EA ENGINEERING MAPPING** for shadow research. It is not a new Oma Ally signal, setup, score, probability, quality grade or execution rule.

Canonical stage bits:
- `EXTREME`;
- `TPW`;
- `MHV`;
- `DIRECTION`;
- `REENTRY`;
- `MOMENTUM`.

Each bit means only that P7 can prove the corresponding canonical stage is present in the exact candidate payload or current resolved same-direction canonical journey context.

No weighted score is authorized.

## Candidate-component evidence

Exact candidate components may contribute only their own stage family:
- `SIGNAL_EXTREME` -> EXTREME;
- `SIGNAL_MLV` -> MHV plus EXTREME + TPW provenance because canonical F1 MHV maturity already requires a reversal-confirmed prior Extreme and normal TP-Wajib structural completion;
- `SIGNAL_RE_ENTRY` -> REENTRY.

No component is allowed to imply unrelated stages merely because the source cycle normally contains them.

## Resolved-journey evidence

Additional same-direction support may be recorded only when the NMJE journey is valid, resolved and its parent direction matches the candidate/decision direction.

Allowed evidence:
- current canonical H1/M15 Extreme support -> EXTREME;
- current canonical M15 MHV/MLV supporting state -> EXTREME + TPW + MHV;
- `MLV_DIRECTION_TAKEN` -> DIRECTION in addition to its retained F1 provenance;
- confirmed canonical H1/M15 Re-Entry -> REENTRY;
- H4 owner parent sourced by eCSD/CSD -> DIRECTION;
- H4 owner parent sourced by CSM -> MOMENTUM;
- H4/D1 Re-Entry parent -> REENTRY.

P7 must not infer a missing intermediate stage from a later stage. Example: MOMENTUM alone does not manufacture DIRECTION, REENTRY, MHV or TPW bits.

## Density cardinality

`StageCount` is the number of set canonical stage bits.

It is a cardinality for telemetry only:
- no weights;
- no bonus/penalty;
- no threshold;
- no arithmetic comparison for candidate selection;
- no conversion into SignalScore/PatternStrength/PriorityTier.

The pre-existing `RequirementCompleteness`, `SequenceCompleteness` and `PatternStrength` fields remain untouched and are not repurposed by P7.

## Sequence-prefix fingerprint

P7 also records a fail-closed contiguous prefix through the canonical cycle:

`EXTREME -> TPW -> MHV -> DIRECTION -> REENTRY -> MOMENTUM`

The prefix stops at the first unproven stage.

This prefix is descriptive only. It is **not** a candidate-validity rule because valid REM/RRE/REE/standalone setups have their own exact signatures and do not require every canonical cycle stage to be present in one candidate.

## Candidate shadow telemetry

For every already-valid candidate produced under existing M13/M14/standalone/D1O rules, P7 may log:
- SequenceHash;
- signal type and direction;
- whether existing D1 authority allows it;
- stage mask;
- contiguous-prefix mask;
- stage count;
- resolved JourneyID / ParentEventID when available.

P7 logs sole valid candidates too. A sole valid candidate must never be rejected, delayed or deprioritized because of density metadata.

## Selected-decision freeze and P4 attribution

Only after the base decision is already `DEC_VALIDATED`, P7 freezes the selected decision's structural fingerprint alongside the existing P4/P6 observer snapshot.

Additive durable research keys may persist:
- structure mask;
- prefix mask;
- stage count.

Pre-P7 P4/P6 records without these keys remain backward-readable and degrade to unavailable P7 metadata only.

P7 persistence failure remains diagnostic and must not alter trade state, recovery, lifecycle, risk or execution.

## Authority invariants

P7 MUST NOT:
- create/reject/rank/delay any candidate;
- change REM/RRE/REE signatures or component maturity;
- change `RequirementCompleteness`, `SequenceCompleteness`, `PatternStrength`, `PriorityTier` or SignalScore;
- change `CompareCanonicalCandidates`;
- change `PriorityEngine_Atomic`;
- activate P2 deterministic ordering;
- change M16 validation/invalidation;
- change SL/TP, risk/MM, lot sizing or execution;
- use StageCount, mask or prefix in any executable decision;
- add M5 authority or a second processing clock.

M15 remains sole processing/final-decision clock. NMJE remains observer-only.

## HOLD

P2 active deterministic coherence ordering remains HOLD/UNRESOLVED.

P7 does not authorize a future “highest density wins” rule. Any use of P7 metadata to change ordering, trade count, eligibility or timing requires a separate explicit policy decision plus attributable evidence.

## Validation exit gate

Require:
- focused P7 static/model tests PASS;
- inherited P6/P5/P4/P2-P3/P1/read-only/M12N/D1O/N3 regressions PASS;
- protected M13/M14 comparator/M15/M16/risk/preflight/execution bodies unchanged from P6;
- native MetaEditor 0 errors / 0 warnings;
- MT4 Strategy Tester deterministic P7 A/B replay;
- exact P6-vs-P7 authority-trace equality on the same symbol/window;
- P7 density telemetry exercised naturally;
- zero broker-action markers;
- no merge / no production activation.
