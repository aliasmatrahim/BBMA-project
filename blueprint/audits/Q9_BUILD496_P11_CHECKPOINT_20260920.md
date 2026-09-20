# Q9 Build 4.96 P11 Checkpoint — 2026-09-20

Issue: #101
PR: #205
Branch: `q9-nmje-v2-p11-lineage-refinement-101`
Base P10: `dcf9d6a627e24dbc65b95b7374a5decc2a006fa2`
Supersedes P11 Build 4.95 lineage semantics at `a114387d8a3054dfdd819d023165e07f2063f9e1`.

## VERIFIED checkpoint

User decision A is implemented as strict canonical ParentEventID/JourneyID semantics.

Identity:
- Build `4.96`
- BuildTag `V496_Q9_P11_STRICT_JOURNEY_LINEAGE_20260920`
- SourceRev `Q9_P11_STRICT_JOURNEY_LINEAGE_101_20260920`
- MQ4 SHA-256 `B08CBDEFED1B1A6B6F0B9CADC3CA53B25BD3F98334E7E797A51D765F53E0C148`

Validation:
- focused + inherited static/model/persistence PASS;
- protected P10->P11 executable bodies exact-equal;
- canonical/runtime/tester native MetaEditor 0E/0W;
- tester adapter firewall = same 3 environment-only deltas / 46 diff lines;
- final A/B normalized 26,188/26,188 exact, SHA `616CCED8BFBD8D73BEFC3971AE61E6DD8A1B44C70E72441D00A7DC2A3959BA0F`;
- P10/P11 authority trace 2,092/2,092 exact, SHA `EFF894BAA8497EF6EB4A54AD43EB6354D80D61772B202E1ADBEAC430FEF2DDBF`;
- broker-action markers 0;
- runtime error scan empty.

Natural strict-lineage coverage per final run:
- FIRST = 1988;
- NEW_JOURNEY = 28;
- CONTINUATION = 0;
- UNRESOLVED = 0;
- NONE = 0.

Persistence:
- Build 4.96 never writes durable CONTINUATION;
- legacy Build 4.95 durable CONTINUATION loads fail-closed as UNRESOLVED;
- FIRST / NEW_JOURNEY durable attribution remains research-only and does not alter trade recovery.

Environment restoration:
- OfflineDiag pre-P11 GlobalVariables backup SHA-256 = `DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6`;
- post-test `profiles/gvariables.dat` was explicitly restored from that backup;
- fresh post-restore SHA-256 = `DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6`;
- no Q9 terminal/process remained active after restoration; Q3 isolated C10 PID 13064 remained untouched.

No merge.
No production activation.
No P2 activation.
No M5 execution authority.
Q3 isolated C10 terminal remains untouched.
