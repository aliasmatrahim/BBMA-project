# Q9 Build 4.92 P7 Structural Density / Sequence Completeness — 2026-09-19

Issue: #101
Branch: `q9-nmje-v2-p7-structural-density-101`
Base: verified P6 head `cfd65d4e914e52620428bae6e54afb9984bff570`
Build: `4.92` / `V492_Q9_P7_STRUCTURAL_DENSITY_20260919`
Status: SHADOW / RESEARCH ATTRIBUTION ONLY / NO ACTIVATION

## Source basis

Implementation follows the active Source Index retrieval path and consumes the accepted canonical cycle:

`Extreme -> TP Wajib -> MHV/MLV -> direction (eCSD/CSD) -> Re-Entry -> Momentum/CSM -> further Re-Entry -> opposite Extreme / cycle restart`.

Material source/decision constraints:
- exact REM/RRE/REE signatures remain unchanged;
- F1 mature MHV/MLV proves its own same-cycle prior reversal-confirmed Extreme + normal TP-Wajib provenance;
- F2 Extreme maturity remains unchanged;
- N1 recursive mapping remains read-only and cannot create/reject/rank/execute;
- P2 active deterministic ordering remains HOLD/UNRESOLVED.

The P7 fingerprint is an **EA ENGINEERING MAPPING**, not a new Oma Ally rule.

## Implementation

Canonical stage bits:
- EXTREME = 1
- TPW = 2
- MHV = 4
- DIRECTION = 8
- REENTRY = 16
- MOMENTUM = 32

`NMJEStructuralDensityState` stores:
- `Present`;
- `Valid`;
- `StageMask`;
- `PrefixMask`;
- `StageCount`;
- diagnostic `Reason`.

`StageCount` is cardinality only. It is never a strength/quality score.

`PrefixMask` records only the contiguous proven prefix through:
`Extreme -> TPW -> MHV -> Direction -> Re-Entry -> Momentum`.
It stops at the first unproven stage and does not invalidate an otherwise valid candidate.

Candidate component mapping:
- Extreme component -> EXTREME;
- mature MLV/MHV component -> EXTREME + TPW + MHV;
- Re-Entry component -> REENTRY;
- CSD/eCSD component, if ever present in observer input -> DIRECTION;
- CSM component, if ever present in observer input -> MOMENTUM.

Resolved same-direction journey context may add only directly provable canonical stages:
- supporting H1/M15 Extreme;
- supporting M15 MHV/MLV;
- MLV direction-taken;
- confirmed H1/M15 Re-Entry;
- H4 owner CSD/eCSD;
- H4 owner CSM;
- H4/D1 Re-Entry parent.

Later stages never backfill missing intermediate bits.

## Observation / attribution

`[Q9-P7-DENSITY]` records every already-valid candidate before M15 selection, including sole candidates and candidates not allowed by existing D1 authority.

P7 does not mutate candidate state.

After an independently selected decision reaches `DEC_VALIDATED`, P7 freezes the selected structural fingerprint into the existing P4/P6 observer snapshot.

Optional durable attribution keys:
- `SDM` = stage mask;
- `SDP` = prefix mask;
- `SDC` = stage count.

The keys are additive and all-or-none. Pre-P7 records remain backward-readable with P7 metadata absent.

Outcome/open telemetry adds `SD/SDM/SDP/SDC` for research joins only.

## Authority firewall

Unchanged from P6:
- `BuildPossibleCombinations`;
- `ValidateSequence`;
- standalone/combination candidate builders;
- `CompareCanonicalCandidates`;
- `PriorityEngine_Atomic`;
- `InvalidationEngine_Atomic`;
- risk;
- preflight;
- `IsSignalAllowed`;
- `SendOrderWithRetry`.

Existing `RequirementCompleteness`, `SequenceCompleteness`, `PatternStrength` and `PriorityTier` are not repurposed.

No P7 value is consumed by selection, validation, risk, SL/TP or execution.

## Result

P7 implementation is compile-ready and Strategy Tester functionally verified for the requested shadow scope.

No merge / no production activation.
Live-terminal timer smoke remains a separate Monday follow-up.
