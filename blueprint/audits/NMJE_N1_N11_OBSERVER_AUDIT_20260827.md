# NMJE N1 / N1.1 Observer Correctness Audit — 2026-08-27

Status: DOCUMENTATION-ONLY AUDIT — NO EA SOURCE CHANGE

## Verdict
N1/N1.1 is correctly non-authoritative in the current source. It observes canonical M08/M09/M11/M12/H4/D1-opportunity state, distinguishes candidate vs confirmed Re-Entry, reversal-confirmed Extreme vs RAW, and mature vs building MHV/MLV. It runs before M15 but does not mutate candidate selection or execution.

## Strengths
- N1 explicitly labels itself observation-only.
- confirmed Re-Entry and candidate Re-Entry are separated;
- RAW Extreme is not treated as supporting maturity;
- mature MHV states are separated from pre-formation states;
- D1 confirmed owner, transition and unresolved are represented distinctly;
- H4 local opposition to D1 is recorded as BUILDING, not autonomously promoted to reversal authority;
- confirmed H1 RE aligned/opposed to parent produces ALIGNED/CONFLICT respectively;
- ambiguous opposite RE states become UNRESOLVED;
- N1.1 overlay captures all owner states for coverage without changing strategy state;
- JourneyID/reason/parent labels provide useful shadow provenance.

## Hardening / evidence gaps
1. JourneyID should ultimately be rebuilt from canonical EventIDs rather than mutable/timestamp-only identity.
2. `supporting` currently aggregates several LTF structures; N3 must not inherit that aggregate as a universal execution gate without setup-specific contract.
3. BUILDING/SUPPORTING/ALIGNED meanings need a formal N3 contract before enforcement.
4. Observer output should gain owner-epoch/processing-epoch diagnostics after dependency identities are hardened.
5. N1/N1.1 replay equivalence has not yet been proven across restart/missed-candle reconstruction.

## Status
- N1 observer architecture: PASS
- N1.1 coverage overlay: PASS
- Non-authoritative boundary: PASS
- Suitable baseline for N2 evidence: YES
- Ready to become N3 gate as-is: NO

## Next
Audit N2 validated-decision/outcome shadow evidence and missing coverage scenarios.
