# N2 NMJE Research Methodology

Date: 2026-08-25  
Status: ACTIVE RESEARCH METHOD — no execution authority

## Objective
Measure whether the already-defined NMJE context classes (`ALIGNED`, `SUPPORTING`, `BUILDING`, `CONFLICT`, `UNRESOLVED`, `N/A`) are associated with meaningfully different realized BBMA trade outcomes **without changing the EA's trade selection while evidence is being collected**.

## Canonical telemetry chain

```text
[N1-NMJE]
journey/context observation
        ↓ exact pair + JourneyID
[N2-NMJE-DEC]
M15-selected + M16-validated decision shadow
        ↓ exact DecisionID
[N2-NMJE-OUT]
realized closed-order outcome
        ↓
correlation → identity reconciliation → attribution → uncertainty report
```

## Identity hierarchy
1. Full `DecisionID` is authoritative.
2. Persisted `SHORT_HASH(DecisionID)` may recover identity only when it maps to **exactly one** validated DecisionID in the analyzed dataset **and** pair identity matches.
3. Hash collision, duplicate DecisionID, duplicate ticket, pair mismatch, missing identity or ambiguous mapping fails closed and remains unattributed.
4. Pair-only, direction-only, timestamp-only and nearest-event matching are forbidden.

## Outcome accounting
For a closed order:

```text
NET = OrderProfit() + OrderSwap() + OrderCommission()
```

Descriptive classification:
- `NET > 0` → observed win
- `NET < 0` → observed loss
- `NET == 0` → observed breakeven

Breakeven is excluded from the decisive win-rate denominator but remains visible as its own count.

## Required reports
The research pipeline must expose at minimum:
- total N1 observations;
- total N2 validated decisions;
- exact JourneyID decision correlations;
- orphan/mismatched/duplicate identities;
- closed-outcome coverage;
- outcome counts by nested relation;
- outcome counts by signal type;
- relation × signal cross-tab;
- net and average realized profit;
- decisive win rate;
- Wilson 95% interval for decisive win rate;
- unresolved hash-only outcomes;
- data-integrity status.

## Evidence interpretation
No fixed minimum sample size is invented as a strategy rule. Evidence is judged by visible uncertainty and data quality:
- identity integrity must be valid;
- outcome coverage must be shown explicitly;
- relation buckets with very small samples or very wide uncertainty intervals are descriptive only;
- apparent differences between relation classes are not called an edge merely because point estimates differ;
- multiple pairs, signal families and different market periods should be represented before considering execution use.

## Hard strategy guard
N2 does **not** authorize any of the following:
- reject `NESTED_CONFLICT`;
- prefer or boost `NESTED_ALIGNED`;
- require `SUPPORTING` as an entry filter;
- create additional LTF entries from nested sub-cycles;
- change REM/RRE/REE signatures;
- change D1 strategic owner logic;
- alter M15/M16/M17/risk/execution semantics;
- claim nested context improves win rate without realized forward evidence.

Any transition from descriptive research to an execution gate is a separate strategy decision and requires explicit approval after evidence review.

## Current tooling map
- N2-02: `n2_nmje_decision_correlator.py`
- N2-03: `n2_nmje_outcome_attributor.py`
- N2-04: `n2_nmje_evidence_sufficiency.py`
- N2-05: `n2_nmje_research_pipeline.py`
- N2-07: `n2_nmje_outcome_log_extractor.py`
- N2-08/N2-10: `n2_nmje_auto_research_pipeline.py`
- N2-09: `n2_nmje_hash_identity_reconciler.py`

## Current blocker for actual evidence
Synthetic tooling can verify parser/correlation mechanics only. Actual nested-performance conclusions require real MT4 forward/runtime logs containing the telemetry chain plus realized closed outcomes.
