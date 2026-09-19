# Q9 Build 4.91 — P6 Journey Maturity Fingerprint

Date: 2026-09-19
Issue: #101
Branch: `q9-nmje-v2-p6-maturity-fingerprint-101`
Base: verified P5 / Build 4.90 / Draft PR #196
Build: `4.91` / `V491_Q9_P6_MATURITY_FINGERPRINT_20260919`

## Purpose

Materialize Issue #101 P6 as categorical, non-ordinal NMJE journey-maturity metadata. This is research/attribution state only.

The implementation consumes existing canonical owner/lifecycle snapshots. It does not create a BBMA signal, alter source semantics, add a processing clock, score candidates, reject candidates, delay decisions, change risk, or execute trades.

## Source / contract basis

Preflight used the live `SOURCE_INDEX.md` router, accepted Strategy Core V2, CORE-V2-F1 MHV/MLV lifecycle, CORE-V2-F2 Extreme maturity and the N1 nested-MTF mapping decision.

Source-supported concepts:
- recursive BBMA lifecycle across timeframes;
- Extreme maturity progression;
- MHV/MLV lifecycle progression;
- direction/eCSD/CSD, Re-Entry and Momentum/CSM continuation;
- owner transitions and cycle provenance.

Engineering mapping:
- the exact P6 categorical enum;
- single-label deterministic fingerprint precedence;
- durable MT4 GlobalVariable keys for research attribution.

P2 deterministic active ordering remains HOLD/UNRESOLVED.

## Code delta

Added `ENUM_NMJE_JOURNEY_MATURITY`:
- NONE
- OWNER_ONLY
- EXTREME_DEVELOPING
- EXTREME_MATURE
- MHV_DEVELOPING
- MHV_MATURE
- DIRECTION_STAGE
- REENTRY_CANDIDATE
- REENTRY_CONFIRMED
- MOMENTUM_CONTINUATION
- OWNER_TRANSITION
- UNRESOLVED

Enum ordinals are storage values only and are not quality/ranking scores.

Added observer helpers:
- `NMJE_IsMaturityDomainValue()`
- `NMJE_MaturityText()`
- `NMJE_IsM5ContextStateValid()`
- `NMJE_ClassifyM5Maturity()`
- `NMJE_ClassifyJourneyMaturity()`
- `NMJE_CommitM5Refinement()`

M5 shadow refinement now freezes the underlying canonical state code beside its existing EventID. EventID identity does not rotate merely because the same event matures.

P4 validated-decision attribution now freezes:
- base journey maturity;
- M5 maturity;
- M5 context state code.

P4 durable attribution adds optional keys:
- `JM`
- `M5M`
- `M5S`

Backward compatibility is fail-closed for research metadata: pre-P6 P4 records lacking the additive keys remain readable, with P6-only maturity fields degrading to UNRESOLVED/state 0. Missing/corrupt observer metadata still cannot alter trade recovery or lifecycle.

Closed-outcome telemetry adds `MAT`, `M5MAT` and `M5STATE`.

## Authority boundary

Function-body comparison against P5 confirms byte-identical authority bodies for:
- `BuildPossibleCombinations`
- `CompareCanonicalCandidates`
- `PriorityEngine_Atomic`
- `InvalidationEngine_Atomic`
- `CheckRiskBeforeTrade`
- `RunEntryPreflightAndExecute`
- `IsSignalAllowed`
- `SendOrderWithRetry`

Broker primitive counts remain:
- OrderSend = 1
- OrderClose = 3
- OrderModify = 0
- OrderDelete = 0

M15 remains sole processing/final-decision clock. NMJE remains observer-only.

## Validation state

Static/model/inherited regression: PASS.
Protected authority body comparison: PASS.
Native MetaEditor exact deployment-name compile: 0 errors / 0 warnings.
Strategy Tester functional runtime: PASS — historical P6 maturity transitions exercised, deterministic replay PASS, P5/P6 authority traces equal, zero broker actions.
Live-terminal/timer runtime: PENDING — Saturday isolated terminal attempts stalled before attributable OnInit/F7-BUILD; live timer smoke is deferred to Monday.
Natural M5 context: bounded historical search produced no genuine PRESENT=Y occurrence; M5 maturity remains static/model validated only.

No production activation is authorized by this record. P7 was not started by the Strategy Tester validation task.
