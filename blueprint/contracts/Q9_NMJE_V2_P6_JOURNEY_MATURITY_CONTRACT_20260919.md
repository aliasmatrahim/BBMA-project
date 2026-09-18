# Q9 NMJE v2 P6 Journey Maturity Contract — 2026-09-19

Issue: #101
Base: verified P5 Build 4.90 / Draft PR #196
Target: Build 4.91 / `V491_Q9_P6_MATURITY_FINGERPRINT_20260919`
Status: SHADOW / ATTRIBUTION METADATA ONLY / NO ACTIVATION

## Source boundary

P6 consumes only already-owned canonical BBMA state:
- Extreme maturity from M08/F2;
- MHV/MLV lifecycle from M09/F1;
- direction/Momentum owner state already produced by canonical owners;
- Re-Entry lifecycle from M12;
- D1/H4 owner transition/provenance already produced by M11/H4 owner logic;
- P1/P3 immutable journey and closed-M5 shadow lineage.

Accepted Core supports the recursive cycle:
`Extreme -> TP Wajib -> MHV/MLV -> direction (eCSD/CSD) -> Re-Entry -> Momentum/CSM -> further Re-Entry -> opposite Extreme / cycle restart`.

The exact P6 software label is an ENGINEERING MAPPING. It is not a new Oma Ally rule, signal, score, or ranking.

## Non-ordinal categorical fingerprint

`ENUM_NMJE_JOURNEY_MATURITY` is a categorical fingerprint. Enum numeric values MUST NOT be interpreted as strength, quality, probability or execution priority.

Allowed labels:
- `NONE`;
- `OWNER_ONLY`;
- `EXTREME_DEVELOPING`;
- `EXTREME_MATURE`;
- `MHV_DEVELOPING`;
- `MHV_MATURE`;
- `DIRECTION_STAGE`;
- `REENTRY_CANDIDATE`;
- `REENTRY_CONFIRMED`;
- `MOMENTUM_CONTINUATION`;
- `OWNER_TRANSITION`;
- `UNRESOLVED`.

No numeric score, weight, minimum maturity, threshold or arithmetic comparison is authorized.

## Base journey fingerprint mapping

P6 selects one descriptive current-stage label from canonical snapshots only.

Fail-closed precedence for one fingerprint:
1. unproven/invalid journey provenance -> `UNRESOLVED`;
2. D1 owner transition -> `OWNER_TRANSITION`;
3. confirmed H1/M15 Re-Entry child -> `REENTRY_CONFIRMED`;
4. candidate H1/M15 Re-Entry child -> `REENTRY_CANDIDATE`;
5. selected H4 directional-owner parent sourced by CSM -> `MOMENTUM_CONTINUATION`;
6. selected H4 directional-owner parent sourced by CSD/eCSD -> `DIRECTION_STAGE`;
7. canonical M15 MHV/MLV formation/retest/direction-taken provenance -> `MHV_MATURE`;
8. canonical active earlier MHV/MLV states -> `MHV_DEVELOPING`;
9. reversal-confirmed/retest-phase/retest-ready H1/M15 Extreme -> `EXTREME_MATURE`;
10. RAW valid H1/M15 Extreme -> `EXTREME_DEVELOPING`;
11. valid immutable parent/journey with no more specific child stage -> `OWNER_ONLY`;
12. otherwise -> `NONE`.

This precedence is only a deterministic single-label selection rule. It MUST NOT be reused as a candidate ranking or trading preference.

Completed structural provenance may remain valid after later cycle stages; the fingerprint describes the selected current observer stage, not deletion of earlier provenance.

## M5 fingerprint mapping

P3 remains controlling. M5 can represent only the already-approved shadow context families:
- Re-Entry candidate -> `REENTRY_CANDIDATE`;
- Re-Entry confirmed -> `REENTRY_CONFIRMED`;
- RAW Extreme -> `EXTREME_DEVELOPING`;
- reversal-confirmed/retest-phase/retest-ready Extreme -> `EXTREME_MATURE`;
- absent canonical context -> `NONE`;
- invalid/unprovable context state -> `UNRESOLVED`.

P6 records the exact M5 canonical state code beside the existing stable M5 EventID. Maturity changes do not rotate EventID.

## Freeze / attribution / restart

P6 freezes base and M5 maturity only after the base decision is already `DEC_VALIDATED`, through the existing P4 observer snapshot.

Newly saved P4 attribution persists:
- base maturity;
- M5 maturity;
- M5 canonical context state code.

Existing P4 records that predate P6 remain backward-readable. Missing P6-only keys degrade to `UNRESOLVED` / state-code 0 for research metadata and MUST NOT affect trade recovery, lifecycle, validation, risk or execution.

Closed outcomes may emit `MAT` and `M5MAT` for research joins.

## Authority invariants

P6 MUST NOT:
- create/reject/rank/delay a candidate;
- activate P2 tie-break ordering;
- alter M13/M14 combination semantics;
- alter M15 selection;
- alter M16 validation/rejection;
- alter SL/TP, risk/MM, lot sizing or execution;
- create a second processing clock;
- add any M5 detector family beyond approved Re-Entry/Extreme shadow context;
- use enum ordinal arithmetic as a quality score.

M15 remains the sole processing/final-decision clock. NMJE remains observation-only.

## HOLD

P2 active deterministic ordering remains HOLD/UNRESOLVED. P6 metadata does not resolve it.

No maturity category is authorized as an execution gate or minimum-quality requirement without a separate evidence-backed strategy-policy decision.
