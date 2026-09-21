# M17 Build 4.99 Broker Distance Guards Validation

Date: 2026-09-21
Issue: #216
Branch: `fix/m17-broker-distance-guards-216`
Base: `d1-owner-dev@8da9dae0801f414f8d4c659a226ff58451cca7e6`
Status: **VERIFIED IN SCOPED DRAFT BRANCH / NATIVE + OFFLINE RUNTIME VERIFIED / NOT MERGED / NOT ACTIVATED**

## Classification

**CONFIRMED BUGS — scoped EA-safety / validation repair.**

No BBMA Strategy-Core rule, signal detector, confirmation rule, M15/M16 authority, SL structural owner or TP semantic owner is changed.

## Confirmed defects

1. Targetless C044/D1TPW decisions bypassed an explicitly enabled `MinRRRatio`, contrary to active lifecycle contracts.
2. `RiskValidationSnapshot` froze StopLevel but omitted FreezeLevel.
3. M17 used absolute broker-distance checks, which did not prove BUY levels were on the Bid trigger side or SELL levels on the Ask trigger side.

## Build 4.99 repair

Identity:
- `4.99`
- `V499_M17_BROKER_DISTANCE_GUARDS_20260921`
- `M17_BROKER_DISTANCE_GUARDS_216_20260921`

Changes:
- freeze `MODE_FREEZELEVEL` beside StopLevel in the existing risk snapshot;
- targetless lifecycle with `MinRRRatio > 0` fails closed with `REJ_INVALID_RR`;
- one frozen-snapshot broker geometry helper validates StopLevel and FreezeLevel using the stricter distance;
- BUY SL/TP are validated against frozen Bid;
- SELL SL/TP are validated against frozen Ask;
- invalid levels are rejected only; no SL/TP is moved or manufactured;
- two obsolete live-price `ValidateStopLevel()` / `ValidateFreezeLevel()` helpers had zero callers and were removed to avoid duplicate validation authority.

## Strategy / ownership invariants preserved

Byte-exact against Build 4.86:
- `ResolveApprovedInitialSLTP()`;
- `ValidateDirectionalSLTPGeometry()`;
- Re-Entry structural-range anchor resolver;
- standalone Extreme RAW->RETEST anchor resolver;
- standalone Extreme TP-Wajib resolver;
- D1TPW and C044 lifecycle identity;
- M16 invalidation;
- M21 lot sizing;
- M19 risk;
- M22 existing-ticket / send-retry execution;
- M24 recovery.

Standalone Extreme #175 remains:
- H1 RETEST/ENTRY-READY only;
- RAW->RETEST inclusive wick window;
- 3.0-pip project buffer;
- broker distance/tick handling = EA_SAFETY.

## Build 4.98 compatibility

Before #216, staged Build 4.98 is byte-identical to owner Build 4.86 for:
- `RiskValidationSnapshot`;
- `BuildRiskValidationSnapshot()`;
- `ValidateSLTP()`;
- `ResolveApprovedInitialSLTP()`.

Therefore #216 has no pre-existing M17 semantic conflict with Draft PR #215 / Option-A D1O enrichment.

## Deterministic validation

- broker-distance model: **PASS**;
- scoped source/static checks: **PASS**;
- BUY wrong-trigger-side SL case: rejected;
- SELL wrong-trigger-side SL case: rejected;
- `FreezeLevel > StopLevel`: stricter frozen distance enforced;
- exact minimum distance boundary: accepted;
- targetless `MinRRRatio == 0`: allowed to continue;
- targetless `MinRRRatio > 0`: rejected;
- one `OrderSend` callsite retained;
- no M17 broker helper queries live `MarketInfo` after the snapshot is frozen.

Committed tests:
- `blueprint/tests/test_m17_broker_distance_model.py`
- `blueprint/tests/test_m17_broker_distance_static.py`
- `blueprint/tests/compare_m17_486_499_protected.py`

## Final validation closure — 2026-09-21

Validated code head: `a0ee13f6febf73e96771d6579d6b6828dfdc5641`.
The commit at this head is test-only after the Build 4.99 source repair; EA source is unchanged from the previously audited Build 4.99 source blob.

Committed current-head tests on G40:
- broker-distance deterministic model: **PASS**;
- current static source guard: **PASS**;
- protected Build 4.86 -> 4.99 bodies: **PASS** against exact owner base `8da9dae0801f414f8d4c659a226ff58451cca7e6`.
- local branch `d1-owner-dev` was stale at `3c2af83d72701a7b92eda33cc04d3d6026639a61` and was explicitly not used as the owner comparator.

Native MetaEditor compile:
- **0 errors / 0 warnings**;
- source MQ4 SHA256: `09C720E9E3160B5D870315C170C101ACCE0162D8C6B13D7FC98C72CC20E31B10`.

Tester adapter:
- regenerated from the exact current Build 4.99 source;
- only three environment-only differences are permitted: tester-symbol fallback, `IsTesting()` connectivity bypass, and skipping `EventSetTimer` under tester;
- reverse-normalized adapter -> source invariant: **PASS**;
- tester MetaEditor compile: **0 errors / 0 warnings**;
- harness MQ4 SHA256: `0CA6669FCCB2BC27C5AD37B1C0C3ED8BF6767BDC417F406508C56C22572D6BED`;
- harness EX4 SHA256: `F6AB250048BC44EBC18BAC77191DFDDA7187104F2F924C96C9E05D143426CF5A`.

Important evidence correction:
- the earlier local candidate harness `BBMA_EA_M17_499_GBPUSD_HARNESS.mq4` contained additional stale M17 implementation differences and is **SUPERSEDED / NOT CURRENT-HEAD RUNTIME EVIDENCE**;
- only its `FRESH_BASE486` baseline artifacts are reused as the verified Build 4.86 comparison baseline.

Current-head bounded GBPUSD smoke:
- M15, Every Tick, 2026-08-01 through 2026-09-01, spread 20;
- build marker: 1;
- init pass: 1; init failed: 0; deinit reason 0: 1;
- mismatched chart errors: 0;
- candidate trades: 14; baseline trades: 14;
- all 28 report trade rows are exact-equal;
- M15_COUNTS: 523/523 exact-equal;
- M15_SELECT: 523/523 exact-equal;
- M16_PASS: 523/523 exact-equal;
- EXEC: 14/14 exact-equal;
- C044 MOMENTUM_HOLD / EXIT_LATCHED / CLOSE_SUCCESS traces: exact-equal;
- fatal runtime scan: zero divide 0, array range 0, critical 0, unresolved stack 0, access violation 0.

Expected M17 validation-layer effect:
- `DECISION_FINAL` has exactly one delta across 523 records;
- same DecisionID `GBPUSD|2026.08.17 11:00|1|7|F64CFECF5DB3AC98`;
- baseline final reason: `REJ_DUPLICATE`;
- Build 4.99 final reason: `REJ_INVALID_SL`;
- interpretation: the corrected M17 broker-geometry guard rejects the invalid SL earlier; no execution/order change results.

OfflineDiag state:
- pre-smoke `gvariables.dat` SHA256: `DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6`;
- restored SHA256: exact same;
- bytes: 240;
- no validation session remains active.

Acceptance: **PASS_CURRENT_HEAD_NO_REGRESSION_IN_EXERCISED_SMOKE**.

Evidence package:
- `blueprint/audits/evidence/M17_BUILD499_20260921/M17499_CURRENT_SMOKE_ANALYSIS.json`;
- `.../STATIC_REGRESSION.log`;
- `.../METAEDITOR_COMPILE.log`;
- `.../TESTER_ADAPTER_INVARIANT.log`;
- `.../TESTER_METAEDITOR_COMPILE.log`;
- `.../LOCAL_EVIDENCE_MANIFEST.json`.

Boundary remains:
- no merge;
- no production activation;
- no live-broker acceptance claim;
- no profitability claim.


## GitHub Actions note

PR #217 triggered two historical v4.58 workflows:
- N3 NMJE v4.58 staging selftest run 35539270375;
- N2 NMJE v4.58 research selftest run 35539270386.

Both fail before their substantive selftests because the workflow checkout is current `d1-owner-dev@8da9dae0801f414f8d4c659a226ff58451cca7e6` while their source guards still require literal Build 4.58 markers such as `Version 4.5.8 - D1 TP-Wajib Lifecycle Stage` / `#property version "4.58"`.

Classification: **STALE WORKFLOW BASELINE MISMATCH / NOT BUILD 4.99 SOURCE-FAILURE EVIDENCE**.

They are not rerun as #216 validation.
