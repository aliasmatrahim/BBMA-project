# M17 Build 4.99 Broker Distance Guards Validation

Date: 2026-09-21
Issue: #216
Branch: `fix/m17-broker-distance-guards-216`
Base: `d1-owner-dev@8da9dae0801f414f8d4c659a226ff58451cca7e6`
Status: **STATIC/MODEL VERIFIED / NATIVE COMPILE + RUNTIME PENDING**

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

## Validation boundary

Native MetaEditor compile has **not** been claimed.
Targeted Strategy Tester/runtime regression has **not** been claimed.

G40 remote execution was unavailable at this checkpoint. The next safe gate is:
1. fetch exact scoped branch;
2. run committed model/static/protected tests;
3. native MetaEditor compile;
4. tester-adapter invariant + compile;
5. bounded GBPUSD regression against verified Build 4.86 evidence;
6. restore OfflineDiag state exactly;
7. record hashes/logs and update this audit.

Until those gates pass: **NOT NATIVE COMPILE VERIFIED / NOT RUNTIME VERIFIED / NO MERGE / NO ACTIVATION**.


## GitHub Actions note

PR #217 triggered two historical v4.58 workflows:
- N3 NMJE v4.58 staging selftest run 35539270375;
- N2 NMJE v4.58 research selftest run 35539270386.

Both fail before their substantive selftests because the workflow checkout is current `d1-owner-dev@8da9dae0801f414f8d4c659a226ff58451cca7e6` while their source guards still require literal Build 4.58 markers such as `Version 4.5.8 - D1 TP-Wajib Lifecycle Stage` / `#property version "4.58"`.

Classification: **STALE WORKFLOW BASELINE MISMATCH / NOT BUILD 4.99 SOURCE-FAILURE EVIDENCE**.

They are not rerun as #216 validation.
