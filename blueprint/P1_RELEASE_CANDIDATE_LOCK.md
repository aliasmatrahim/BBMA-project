# P1 Release Candidate Lock

Status: **LOCKED — P1 RELEASE CANDIDATE**

Branch: `blueprint-dev`

Canonical source:
`blueprint/source/BBMA_PROFESSIONAL_EA.mq4`

Canonical SHA-256:
`30363d08437b85f253e6baf3e9c82af0d59d70727639ac0e6420a7677f975bc9`

Release-candidate qualification:
- immutable baseline reconstruction verified;
- ordered patch chain `0001` through `0025` materialized successfully;
- integration conflicts rebased without intentional BBMA strategy-semantic changes;
- architecture ownership and structural invariants passed;
- native MetaEditor compile verified by user at `0 errors, 0 warnings`;
- post-compile canonical invariant audit passed directly against the canonical source.

This lock freezes the P1 release-candidate identity. Any subsequent source modification invalidates this RC SHA and requires a new verification cycle.

This is not yet a production/live-trading release. P2 functional and Strategy Tester verification remains required before production promotion or merge to `main`.
