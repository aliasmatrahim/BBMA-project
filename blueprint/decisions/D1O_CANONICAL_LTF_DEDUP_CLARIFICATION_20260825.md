# D1O-07 — Canonical LTF Dedup Clarification

Date: 2026-08-25  
Status: **APPROVED IMPLEMENTATION CLARIFICATION / SAFETY CORRECTION**

## Why this clarification exists
The approved D1 Opportunity design says different timeframe does not automatically mean a different trade and that the same H1+M15 structural chain must be one cluster. The first D1O-02 implementation included D1 CycleID and OpportunityFamily inside the executable sequence hash. That could let the same lower-timeframe Re-Entry acquire a different DecisionID merely because D1 opportunity attribution changed, or because a simultaneous H1+M15 cluster later degraded to H1-only as freshness changed.

That behavior would contradict the already-approved dedup principle. D1O-07 therefore separates **execution identity** from **research attribution identity**.

## Locked rule
- **Execution/dedup identity belongs to the fresh LTF Re-Entry sequence.**
- If H1 is present, H1 owns the cluster execution identity, even when M15 is simultaneously present as supporting completion/timing.
- If only M15 is present, M15 owns the execution identity.
- The same LTF Re-Entry confirmation must not become a new trade merely because `D1 CycleID` or `OpportunityFamily` changes.
- D1 CycleID, OpportunityFamily and authority mode remain frozen metadata for context, validation and outcome attribution.
- A later genuinely fresh H1 or M15 Re-Entry with a new confirmation anchor remains a new structural sequence and may create another trade subject to all existing limits.

## Identity split
Execution dedup key:

`Pair + Direction + LTF Re-Entry TF + LTF confirmation anchor`

Attribution context:

`D1 CycleID + OpportunityFamily + D1 source + D1 activation + authority mode`

## H1 + M15 cluster
When H1 and M15 are both fresh in the same opportunity cluster:
- both may remain frozen as validation components;
- H1 remains the structural SL/TP source preference;
- H1 owns the candidate anchor and execution SequenceHash/DecisionID;
- M15 presence is telemetry/support metadata and must not create a second executable identity.

## Scope guard
This clarification does not change:
- D1 opportunity family activation rules;
- tactical Extreme/TP-Wajib confirmation rules;
- CSD/Re-Entry/Momentum opportunity maturity;
- exact REM/RRE/REE signatures;
- M15 final-authority ownership;
- M16 fail-closed validation;
- SL/TP formula;
- risk, lot sizing, portfolio limits or broker execution.

It only prevents duplicate execution of the same LTF structural setup through different D1 attribution paths.
