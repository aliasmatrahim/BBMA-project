# NMJE Dependency Hardening Audit — DEP-A08 M16 Frozen-Owner / Journey Revalidation

Date: 2026-08-27
Status: DOCUMENTATION-ONLY AUDIT — NO EA SOURCE CHANGE

## Baseline verdict
M16 is already behaving as a revalidator rather than a second strategy detector. It checks frozen D1 authority and exact component ownership against current canonical owner states, then validates/invalidates/expires the M15 decision. This is the correct base for N3.

## Strengths observed
- M16 only accepts `DEC_CREATED` from M15.
- frozen D1 strategic/opportunity snapshots are verified against current canonical state.
- each frozen component is matched by type/direction/timeframe/candle identity against M08/M09/M12 owner state.
- M16 does not redetect Re-Entry/MHV/Extreme formulas.
- owner expiry and structural break are distinguished into EXPIRED vs INVALIDATED.
- only after all checks pass does decision become `DEC_VALIDATED`.

## N3 hardening findings

### DEP-A08-F1 — Revalidate frozen NMJE identity, not recompute strategy
N3 should add validation of frozen JourneyID/verdict/owner identities and processing epoch. M16 may compare those identities with current M12N state, but must not rebuild the nesting formula independently.

### DEP-A08-F2 — Supersession reason must be explicit
If a frozen journey owner was superseded between M15 and M16, reject with a reason-coded NMJE/owner supersession result rather than collapsing every case into generic sequence break where practical.

### DEP-A08-F3 — Pending decision vs live trade separation
M16 authority applies to a pending/new-entry decision. A later opposite NMJE event must not be interpreted by M16 as a broker-close instruction for an already-live trade.

### DEP-A08-F4 — Owner identity hardening dependency
Current component matching relies heavily on direction/timeframe/confirmation candle. When M08/M09/M12 stable EventIDs become available, freeze/revalidate those IDs to reduce accidental same-timeframe lineage collisions.

### DEP-A08-F5 — Fail-closed on recovery uncertainty
If current owner/journey state cannot be reconstructed deterministically after restart, M16 should invalidate/freeze new-entry eligibility as UNRESOLVED rather than accepting a best-effort match.

## N3 readiness
- Revalidator authority boundary: PASS
- No duplicate strategy formulas: PASS
- Exact component ownership check: PASS
- D1 frozen authority verification: PASS
- Frozen NMJE JourneyID/verdict verification: NOT YET IMPLEMENTED
- Reason-coded NMJE supersession: PENDING
- Live-trade separation: MUST PRESERVE
- Safe for mandatory N3 today: NO

## Next
DEP-A09 — M24 recovery/replay readiness audit.
