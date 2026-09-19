# Q9 Build 4.96 P11 Strict Journey Lineage Validation — 2026-09-20

Status: **STATIC/MODEL/NATIVE COMPILE/STRATEGY TESTER AUTHORITY REGRESSION PASS**

## Identity

- Version: `4.96`
- BuildTag: `V496_Q9_P11_STRICT_JOURNEY_LINEAGE_20260920`
- SourceRev: `Q9_P11_STRICT_JOURNEY_LINEAGE_101_20260920`
- canonical MQ4 SHA-256: `B08CBDEFED1B1A6B6F0B9CADC3CA53B25BD3F98334E7E797A51D765F53E0C148`
- canonical EX4 SHA-256: `73CFC1A82656D0658CCEF4BF41DB85473E580E8C142983FE14A9647010FAFBEF`
- runtime-name EX4 SHA-256: `F0B5831A276422357329F360653764A310239925710F0CAD5B74EC87F2C6EEF8`
- tester adapter MQ4 SHA-256: `FA5BA5F597846E18B95AE7580B4B46DDB9B867E283221AAAE4E369AEEAF2C424`
- tester EX4 SHA-256: `D69556BF7E7CF921163227C1A44167255BD4E5DE65C44515A642A1D7285C3FE6`

## Static / inherited regression

PASS:
- P11 strict JourneyID model/static/persistence;
- P10/P8/P7/P6/P5/P4/P2-P3/P1 inherited guards;
- NMJE read-only authority;
- M12N orchestration;
- D1O execution identity;
- N3 activation firewall;
- `git diff --check`.

Protected P10 -> P11 executable bodies remain exact-equal:
- BuildPossibleCombinations;
- ValidateSequence;
- standalone/confirmed/D1O candidate builders;
- CompareCanonicalCandidates;
- PriorityEngine_Atomic;
- InvalidationEngine_Atomic;
- ResolveExecutionReferencePrice;
- ResolveApprovedInitialSLTP;
- CheckRiskBeforeTrade;
- RunEntryPreflightAndExecute;
- IsSignalAllowed;
- SendOrderWithRetry.

## Native compile

MetaEditor result for all three exact artifacts:
- canonical short path: 0 errors / 0 warnings;
- runtime-name expert: 0 errors / 0 warnings;
- tester adapter: 0 errors / 0 warnings.

Tester adapter firewall remains the same three environment-only deltas and 46 diff lines.

## Strategy Tester

GBPUSD M15, 2026-08-01 through 2026-09-01, model 0, spread 20, zero-trade safety caps.
Final post-BuildID + persistence-fix A/B runs both exited clean and were not forced.

Determinism:
- normalized A lines: 26,188;
- normalized B lines: 26,188;
- exact equality: PASS;
- SHA-256 both: `616CCED8BFBD8D73BEFC3971AE61E6DD8A1B44C70E72441D00A7DC2A3959BA0F`.

P10 -> P11 authority trace:
- P10: 2,092;
- P11: 2,092;
- exact equality: PASS;
- SHA-256 both: `EFF894BAA8497EF6EB4A54AD43EB6354D80D61772B202E1ADBEAC430FEF2DDBF`.

Broker-action markers:
- P10=0;
- P11A=0;
- P11B=0.

Runtime error scan: none.

## Natural strict-lineage coverage

Across each final A/B run, P11 emitted 2016 lineage rows:
- FIRST: 1988;
- NEW_JOURNEY: 28;
- CONTINUATION: 0;
- UNRESOLVED: 0;
- NONE: 0.

This is the intended result of decision A:
- canonical ParentEventID/JourneyID transition is observed as NEW_JOURNEY;
- unchanged canonical root remains FIRST;
- higher-owner continuity cannot manufacture CONTINUATION;
- CONTINUATION remains reserved until a distinct source-owned continuation-event identity exists.

Persistence hardening:
- Build 4.96 does not save `CONTINUATION` as durable lineage metadata;
- a legacy Build 4.95 persisted `CONTINUATION` is loaded fail-closed as `UNRESOLVED`;
- FIRST / NEW_JOURNEY durable semantics remain available; this does not alter trade recovery authority.

## Supersession

Build 4.95 P11 evidence is historical/superseded for lineage classification semantics. It remains useful as provenance for the discovered cross-contract mismatch but must not be used as accepted P11 classification evidence.

## Runtime boundary

No live-terminal/OnTimer verification is claimed from Strategy Tester evidence. The existing Q3 isolated C10 terminal was not restarted or modified.

## Result

**P11 Build 4.96 strict canonical-JourneyID implementation + authority-preservation exit gate: VERIFIED.**

No merge / no production activation / no P2 activation / no M5 execution authority.
