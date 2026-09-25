# N3 — NMJE Active Selection Policy Contract

Status: **ACTIVE IMPLEMENTATION CONTRACT / DEFAULT OFF / VALIDATION PENDING**

Decision authority:
`blueprint/decisions/Q9_NMJE_V2_P2_P5_N3_ACTIVE_SELECTION_POLICY_DECISION_20260926.md`

## Position
`M08/M09/M10/M11/M12 -> M12N/NMJE -> M13/M14 -> M15 selection -> M16 -> Risk -> Execution`

M15 remains the sole final new-entry authority.

## Authorized active capability
When `EnableNMJESelectionPolicy=true`, N3 may arbitrate only among two or more already-eligible same-direction candidates.

Preconditions:
- candidate eligibility already proven;
- D1 authority already permits the candidate;
- V1 journey is valid/resolved and positively coherent (`ALIGNED` or `SUPPORTING`);
- canonical M5 semantic owner state is resolved and positively coherent (`ALIGNED` or `SUPPORTING`).

Comparator:
1. longer canonical structural prefix;
2. greater bounded canonical stage count;
3. legacy `CompareCanonicalCandidates` fallback.

The bounded structural representation is existing P7 canonical-stage metadata, not a weighted score.

## P5 conflict boundary
M5 alone never emits executable `NESTED_CONFLICT` and never rejects a trade.
Opposite confirmed M5 Re-Entry remains `UNRESOLVED`.
Existing V1 owner-level conflict classification is unchanged.

## Prohibited authority
N3 may not create eligibility, alter detector state, reject/delay a sole candidate, change M16/M17/risk/MM, create SL/TP, call `OrderSend`/`OrderClose`, or become a second clock.

## Lifecycle/restart
The active comparator is stateless per closed-M15 cycle and consumes current canonical owner state only. No selection-policy state is reconstructed across restart. The resulting selected DecisionID/SequenceHash and existing durable execution/NMJE attribution remain the downstream identity.

## Activation
Input default is OFF. Turning it ON is a strategy-selection behavior change and is permitted only for the validation programme until the Build 5.17 validation record is complete.
