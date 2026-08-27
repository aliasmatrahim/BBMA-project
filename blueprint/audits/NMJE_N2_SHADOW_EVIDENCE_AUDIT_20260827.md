# NMJE N2 Shadow Evidence Audit — 2026-08-27

Status: DOCUMENTATION-ONLY AUDIT — NO EA SOURCE CHANGE

## Verdict
N2 is correctly implemented as post-M16 observational telemetry. Current code prints the NMJE relation/JourneyID alongside the exact validated decision identity and also emits closed-order outcome telemetry. It does not change M15, M16, risk, SL/TP or execution.

## Existing evidence fields
Validated-decision shadow includes:
- pair, signal, direction;
- NMJE relation;
- parent kind/direction;
- JourneyID;
- DecisionID/token/hash;
- D1 authority mode;
- D1 opportunity family/cycle;
- LTF opportunity cluster;
- sequence hash.

Closed-order shadow includes exact ticket/decision/execution identity and realized net P/L, with identity mismatch failing closed.

## Missing evidence before N3 promotion
1. reason-coded NMJE verdict should be included with every validated-decision shadow record;
2. processing epoch/owner-source candle identities should be captured to prove no mixed snapshot;
3. explicit WITH-NMJE hypothetical outcome is needed for decisions that would be blocked/waited under proposed N3, not only validated decisions;
4. rejected/no-decision samples need correlation with NMJE state to measure false blocking risk;
5. coverage must include BUILDING->ALIGNED, CONFLICT, UNRESOLVED, supersession, opposite H4-local/D1, exact REM/RRE/REE, D1 opportunity and standalone H1 RE;
6. restart/replay-equivalence samples are still missing;
7. sample counts must be sufficient across pairs/timeframes before any claim that N3 enforcement is safe.

## Promotion gate
N2 is not complete merely because telemetry exists. Promotion to N3 requires shadow evidence showing that the proposed setup-aware NMJE gate is source-faithful, deterministic, does not promote immature components, and does not introduce unsupported universal nesting.

## Status
- N2 telemetry architecture: PASS
- decision/outcome identity attribution: PASS
- N2 enforcement authority: NONE (correct)
- reason/epoch coverage: PARTIAL
- rejected/no-decision counterfactual coverage: MISSING
- restart/replay coverage: MISSING
- ready for N3 enforcement today: NO

## Next safe step
Draft the N3 pre-enforcement contract/schema from the dependency closure matrix and N1/N2 findings, without changing EA source.
