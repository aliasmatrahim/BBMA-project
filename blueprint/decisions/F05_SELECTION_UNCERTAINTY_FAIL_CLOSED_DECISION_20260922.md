# F05 Selection Uncertainty Fail-Closed Decision — 2026-09-22

Status: **LOCKED / ENGINEERING RISK-OBSERVATION SAFETY MAPPING**
Issue: **#226** / downstream Issue #101 F05
Baseline: `d1-owner-dev@2e524cdfe8829da774698cb96c8fc848518250d3` / Build 5.05

## Classification
This is not a BBMA Strategy-Core rule. It does not change signal direction, setup eligibility, TradeLock mode semantics, M17 geometry, M21 sizing, F07 ambiguity ownership or M24 recovery identity.

## Problem
The previous boolean portfolio helper mapped monitored-ticket `OrderSelect()` failure to ordinary `false`.
That made UNKNOWN broker observation indistinguishable from proven closed/missing/mismatched/foreign exclusion.

## Locked mapping
1. Canonical portfolio ownership observation has three states: `UNKNOWN`, `EXCLUDED`, `LIVE_OWNED`.
2. `OrderSelect(ticket)` failure is `UNKNOWN`; it is never treated as zero exposure.
3. Proven closed, invalid pair mapping, configured-magic mismatch or foreign live magic remain `EXCLUDED`.
4. Proven live monitored configured-magic match is `LIVE_OWNED`.
5. M19 basket pretrade validation fails closed on `UNKNOWN` with `REJ_BASKET_LOSS`.
6. M20 prospective admission fails closed on `UNKNOWN` using the existing atomic portfolio rejection path.
7. TradeLock modes 1 and 2 fail closed on `UNKNOWN`; mode 0 remains unrestricted by TradeLock.
8. `UNKNOWN` alone does not prove `BasketLossPercent` breach and therefore does not create an emergency-close request.
9. M20 defers basket-threshold evaluation for that tick when observation is `UNKNOWN`; an already-latched emergency request still uses the existing broker-confirmed fail-closed release path.
10. M19 total-risk F01 logic remains unchanged and independently fail-closed.
11. No symbol/type registry predicate is added here; F10 remains separate.
12. No universal opposite-direction guard is added; F03 remains separate.

## Validation
- deterministic model and source guard;
- protected Build 5.05 body comparison;
- native MetaEditor 0E0W;
- exact tester-adapter invariant + compile;
- normal isolated smoke exact-equal to Build 5.05;
- targeted UNKNOWN-selection harness proving new-entry suppression without emergency-latch fabrication;
- exact tester GlobalVariables restore;
- no primary MT4 restart or live/demo activation.
