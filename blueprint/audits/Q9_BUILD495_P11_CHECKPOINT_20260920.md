# Q9 Build 4.95 P11 Checkpoint — 2026-09-20

> **SUPERSEDED FOR P11 LINEAGE SEMANTICS.** Build 4.96 / decision A replaces the 4.95 higher-owner-root mapping with strict canonical ParentEventID/JourneyID semantics. Retain this file as historical evidence only.

Issue: #101
Branch: `q9-nmje-v2-p11-lineage-refinement-101`
Base: P10 `dcf9d6a627e24dbc65b95b7374a5decc2a006fa2`

## VERIFIED checkpoint

P11 First-event / Continuation-event lineage refinement reached its implementation and authority-preservation exit criteria.

Identity:
- Build `4.95`
- BuildTag `V495_Q9_P11_LINEAGE_REFINEMENT_20260920`
- SourceRev `Q9_P11_LINEAGE_REFINEMENT_101_20260920`
- MQ4 SHA `F8E9DD081BF660820F72467D45558C1A5D8F6B95FC0512F0A6DBE96334E6C52D`

Validation:
- focused model/static/persistence PASS;
- inherited P1-P10/read-only/M12N/D1O/N3 regression PASS;
- protected P10->P11 executable bodies exact-equal;
- canonical/runtime/tester native compile 0E/0W;
- tester adapter firewall = same three environment-only deltas / 46 diff lines;
- deterministic A/B = 26,188/26,188 exact, SHA `D705BDB6C8208EA9D484EC8369BE71066137C54219004F077E6BE45B4BC33C60`;
- P10/P11 authority trace = 2,092/2,092 exact, SHA `EFF894BAA8497EF6EB4A54AD43EB6354D80D61772B202E1ADBEAC430FEF2DDBF`;
- zero broker actions and zero targeted runtime errors.

Natural lineage coverage:
- CONTINUATION = 2016 / runtime verified;
- FIRST = 0 / bounded-unexercised;
- NEW_JOURNEY = 0 / bounded-unexercised.

A pre-fix phantom startup NEW_JOURNEY was found and fixed by requiring canonical 16-character previous/current lineage-root identity.

Ticket-bound P11 persistence remains bounded-unexercised under the zero-trade safety profile; static + persistence model PASS.

GlobalVariables were restored byte-identically after tester runs.

No merge.
No production activation.
No P2 activation.
No M5 authority change.

Parallel live state at checkpoint:
- Q3 isolated Build 4.81 terminal PID 13064 remains active / runtime gate pending.
- Q6 native archive is STOPPED_BY_USER at 17/720 PASS; do not auto-resume.
