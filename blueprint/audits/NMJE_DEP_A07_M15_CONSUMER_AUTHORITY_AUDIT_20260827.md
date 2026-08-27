# NMJE Dependency Hardening Audit — DEP-A07 M15 Final-Authority / NMJE Consumer

Date: 2026-08-27
Status: DOCUMENTATION-ONLY AUDIT — NO EA SOURCE CHANGE

## Baseline verdict
M15 is already the sole final new-entry selector in the current architecture. NMJE N1/N2 remains descriptive/shadow-only and does not alter candidate selection or execution. This authority boundary is correct and must be preserved in N3.

## Strengths observed
- `PriorityEngine_Atomic()` selects one canonical candidate only after structural eligibility and D1 authority checks.
- opposite eligible directions fail closed with no winner.
- selected authority snapshot is frozen before decision creation.
- component identity, candidate expiry, sequence identity and SL/TP source identity are frozen into the decision.
- decision only proceeds to M16 when M15 actually produced a valid `DEC_CREATED` decision.
- NMJE N2 shadow telemetry runs only after M16 validates; it does not mutate execution.

## N3 hardening findings

### DEP-A07-F1 — Add explicit NMJE frozen payload to decision
When N3 becomes authoritative, M15 must freeze the exact NMJE verdict, JourneyID, relevant owner/event identities, processing epoch and reason code that justified admission/blocking. Do not let M16 query an unrelated newer journey and pretend it is the same decision context.

### DEP-A07-F2 — Scope-aware gate only
N3 consumption must be setup-aware. M15 may require only the MTF relation established by the approved setup contract; no universal D1->H4->H1->M15 perfect chain.

### DEP-A07-F3 — WAIT is not automatic reject
Incomplete but source-valid lineage should remain WAIT/BUILDING where the contract permits. M15 blocks only true conflict/unresolved/unsupported states defined by the N3 contract.

### DEP-A07-F4 — No NMJE candidate promotion
NMJE cannot make RAW Extreme, candidate Re-Entry or pre-formation MHV executable merely because parentage looks aligned. M15 keeps canonical component maturity requirements.

### DEP-A07-F5 — Preserve canonical winner semantics
NMJE is an eligibility/context gate, not a competing priority/scoring engine. Canonical candidate selection remains M15-owned.

## N3 readiness
- Final new-entry authority boundary: PASS
- Canonical winner selection: PASS
- Opposite-direction fail-closed: PASS
- NMJE frozen decision payload: NOT YET IMPLEMENTED
- Setup-aware N3 gating contract: PENDING
- Safe for N1/N2: YES
- Safe for mandatory N3 today: NO

## Next
DEP-A08 — M16 frozen-owner/journey revalidation audit.
