# N2-02 — NMJE Decision Correlator Audit

Date: 2026-08-25

## Result
**PASS — decision/journey correlation research tooling staged and deterministic synthetic preflight passed.**

## Added
- `blueprint/tools/n2_nmje_decision_correlator.py`
- `blueprint/tests/test_n2_nmje_decision_correlator.py`

## What it correlates
The tool reads both diagnostic streams from one or more MT4 Experts/Journal logs:
- `[N1-NMJE]` journey observations;
- `[N2-NMJE-DEC]` validated-decision shadow tags.

For every validated decision it records signal type, direction, nested relation, parent context, JourneyID and DecisionID, then attempts to bind it to the most recent preceding N1 observation from the same pair and exact JourneyID.

## Integrity rules
- Exact JourneyID match is preferred and reported separately.
- Same-pair fallback is allowed only when the decision has no JourneyID (`J=-`) and is labelled as weak diagnostic context.
- A decision with a non-empty JourneyID is never silently attached to a different journey.
- Orphan decisions, relation/parent/journey mismatches and duplicate DecisionIDs are reported explicitly.

## Synthetic preflight
Verified synthetic sequence:
`BUILDING -> SUPPORTING -> validated REM -> ALIGNED -> validated standalone RE`

Expected results passed:
- 3 N1 observations;
- 3 N2 validated decisions;
- 2 exact JourneyID correlations;
- 1 explicit orphan with no prior context;
- correct relation and signal counts;
- zero false context mismatches;
- zero duplicate DecisionIDs.

## Scope
Research/diagnostic tooling only. No EA source, signal detection, REM/RRE/REE signature, M15/M16 authority, SL/TP, risk, execution or entry count is changed by N2-02.

## Dependency note
N2-01 native MT4 compile/materialization on `d1-owner-dev` remains a separate gate. N2-02 being ready does not imply N2-01 has landed or compiled.

## Next
Once real `[N2-NMJE-DEC]` lines exist in demo/live forward logs, run this correlator on actual MT4 logs. Outcome/win-rate attribution is a later research layer and must not be inferred from validated-decision counts alone.
