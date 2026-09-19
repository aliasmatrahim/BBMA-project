# Q9 Build 4.87 P1 Validation Closure — 2026-09-18

Issue: #101
PR: #192
Source-bearing validation head: `53487745eeecc43e515d8e64e205b446c7df1732`
Owner baseline: `d1-owner-dev@01f7e8305f6ba558494fc559bb3c734dfc06124a`

## Result

**Q9 P1 VERIFIED — PROVENANCE/LINEAGE ONLY / NMJE AUTHORITY REMAINS READ-ONLY.**

Final source identity:
- header/property: Build `4.87`;
- BuildTag: `V487A_Q9_NMJE_LINEAGE_TRACEFIX_20260918`;
- SourceRev: `Q9_P1_NMJE_LINEAGE_TRACEFIX_101_20260918`;
- MQ4 SHA-256: `2c7039c24eef22509b9fcb102a919413ea81c031b955faabfc17a61306381815`;
- EX4 SHA-256: `33ee141eae829a3b0359426fec6f88721b0cbb9589eb64092d3d8287c6a4139f`.

## Static / regression

PASS:
- Q9 P1 current-owner static guard;
- deterministic D1 epoch model;
- NMJE read-only authority: 6/6;
- D1O execution identity regression;
- Q5 M12N orchestration-order guard;
- N3 activation-firewall self-test;
- `git diff --check`.

Protected owner modules M13/M14/M15/M16/M17/M22 were byte-identical to Build 4.86 in the P1 implementation review. Broker-write primitive counts remained unchanged and no `PERIOD_M5` wiring or NMJE execution gate was introduced.

## Native compile

Portable MT4 MetaEditor produced:
- `0 errors / 0 warnings`;
- elapsed 963 ms.

Evidence: `Q9_BUILD487A_METAEDITOR_COMPILE_20260918.log`.

## Runtime

Isolated environment only:
- `D:\BBMA\MT4_NMJE_141_Demo`;
- EURUSD M15;
- terminal trading disabled via `ExpertsTrades=false`;
- `MaxTradePerPair=0`;
- `MaxTotalTrade=0`;
- InstanceID 87.

The first Build 4.87 runtime exposed one traceability defect: the correct `[F7-BUILD]` identity was followed by a stale v4.8.6 human-readable init message. This was repaired with the smallest trace-only change and a unique `V487A...` BuildTag. No strategy condition changed.

Final tracefix runtime proved:
- exact `[F7-BUILD]` identity;
- successful EA initialization;
- D1 owner epoch reconstructed as `2026.09.14 00:00`;
- connected heartbeat;
- graceful deinitialization;
- no NMJE gate/broker action/executed-decision markers.

Most importantly, the active H4 parent identity survived physical terminal stop/restart exactly:
- pre-restart ParentEventID: `3F16B9B918EA9C6B`;
- post-restart ParentEventID: `3F16B9B918EA9C6B`;
- pre/post JourneyID: `J2|EURUSD|H4_OWNER|3F16B9B918EA9C6B`.

This validates the P1 restart/recovery invariant for the observed active parent without granting NMJE execution authority.

Evidence: `Q9_BUILD487A_RUNTIME_20260918.log`.

## CI note

Two legacy repository workflows named `N2 NMJE v4.58 research selftest` and `N3 NMJE v4.58 staging selftest` fail their first source-marker step because they still hard-code historical Build 4.58 markers and explicitly checkout `d1-owner-dev`. They do not execute the Q9 head-specific tests and are therefore stale CI compatibility failures, not Q9 P1 source failures. Q9 acceptance above is based on exact-head local/static/native/runtime evidence.

## Boundary

No M5 collection, no second processing clock, no candidate create/reject/rank/delay authority, no risk/MM change, no M17/M22 change, no Strategy-Core rule change and no production activation.

P2/P3 may proceed only under Issue #101's approved equal-eligibility/shadow/context boundaries.
