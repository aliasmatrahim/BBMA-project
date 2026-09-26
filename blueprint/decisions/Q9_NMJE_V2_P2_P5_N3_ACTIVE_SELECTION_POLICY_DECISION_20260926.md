# Q9 NMJE V2 — P2/P5 Closure + N3 Active Selection Policy Decision — 2026-09-26

Status: **DECIDED / IMPLEMENTATION AUTHORIZED / VALIDATION PENDING / DEFAULT OFF**

Issue: #101

## User authorization
On 2026-09-26 the user explicitly instructed:
`Run P2 policy closure -> P5 true-conflict closure -> N3 active-authority implementation.`

This is the explicit project strategy-policy authorization required by the earlier P2/P5/N3 HOLD records. It does not claim that the active comparator is an original Oma Ally rule. Where source does not define simultaneous-candidate arbitration, the policy below is an explicit bounded engineering mapping.

## Source constraints retained
- M15 remains the sole processing/final new-entry authority.
- A sole valid candidate is never rejected, delayed or downgraded by NMJE.
- No M5 signal independently creates/rejects/ranks/executes a trade.
- Opposite-looking M5 structure is not automatically an independent reversal.
- No universal `ALIGNED > SUPPORTING > BUILDING > CONFLICT > UNRESOLVED` score/order is introduced.
- Existing candidate eligibility, D1 authority, M16, M17, risk/MM and M22 execution remain unchanged.

## P5 true-conflict closure
M5 **does not own hard `NESTED_CONFLICT` authority**.

Deterministic policy:
- same-direction confirmed M5 Re-Entry -> `ALIGNED`;
- same-direction candidate M5 Re-Entry -> `SUPPORTING`;
- opposite candidate M5 Re-Entry -> `BUILDING`;
- opposite confirmed M5 Re-Entry -> `UNRESOLVED`;
- same-direction active M5 Extreme -> `SUPPORTING`;
- opposite active M5 Extreme -> `BUILDING`;
- multiple simultaneously mapped M5 states -> `UNRESOLVED`.

No M5-only state becomes a hard rejection. Genuine `NESTED_CONFLICT` remains the existing V1 owner-level classification, such as a canonical confirmed H1 Re-Entry opposing its attributable parent. This closes P5 for active-policy design without inventing an M5 hard-conflict rule.

## P2 active tie-break closure
N3 arbitration may run only when:
1. two or more candidates are already eligible;
2. all competing candidates are in the same M15 target direction;
3. D1 authority already permits those candidates;
4. the V1 journey is resolved/valid, parent direction matches the target direction, and relation is `ALIGNED` or `SUPPORTING`;
5. canonical M5 semantics are resolved and M5 diagnostic relation is `ALIGNED` or `SUPPORTING`.

When those conditions hold, candidates are compared lexicographically by:
1. canonical structural prefix length from the bounded six-stage BBMA structure mask;
2. total distinct canonical structural stage count;
3. existing `CompareCanonicalCandidates()` as deterministic fallback.

There is no weighted score, probability, timeframe vote or new signal formula. Structural completeness is used only to arbitrate among already-valid candidates as explicitly contemplated by Issue #101 P7. If positive-coherence conditions are absent or tied, the existing M15 comparator wins unchanged.

## N3 authority boundary
N3 may influence **selection only** under the exact P2 policy above. It may not:
- create candidate eligibility;
- reject or delay the sole candidate;
- convert M5 opposition into a hard reject;
- change risk approval;
- change SL/TP formulas;
- size a position;
- send/close orders;
- change lifecycle ownership.

Implementation is gated by `EnableNMJESelectionPolicy=false` by default. M15 `PriorityEngine_Atomic` remains the actual decision owner.

## Validation state
This decision authorizes implementation. It does not declare the build validated or release-ready. Required next gates remain:
static/cross-module -> native MetaEditor -> targeted regression/A-B -> Strategy Tester -> demo forward -> restart/provenance/order-log validation.

Until those gates pass:
**IMPLEMENTED / DEFAULT OFF / NOT RELEASE-READY**.
