# SIG-05 Extreme source readiness implementation plan

> For agentic workers: execute inline with superpowers:executing-plans; finish SIG-05 before any later signal.

Goal: preserve accepted M08 RAW/reversal/retest/void semantics and remove the duplicated unavailable Momentum interpretation.
Architecture: M10 is the sole Momentum producer. M08 consumes its ready source snapshot before owner mutation. Existing M15 clock, signatures, strict MA extension, reversal body anchor, retest and normal TPW policy remain unchanged.
Tech stack: MQL4 strict, native isolated G40 tester, Python evidence collectors.
Spec: accepted Core section5, F2 maturity decision, M08 contract and current serial user authorization.

## Review focus
Missing/interior/revised inputs must not mutate M08. A changed symbol/TF identity must not reset an owner before readiness. Valid source must retain BUY/SELL lifecycle results, equality/void priority and no TTL. Raw flags never create execution authority. Shared controller fields must remain attributable.

## Task1 — M08 source-boundary repair and bounded acceptance
Files: blueprint/source/BBMA_EA.mq4; tests/custom_mtf/CustomExtremeSourceHarness.mq4; scoped source/lifecycle native tests, regression runner and evidence.
Interfaces: IsExtremeMomentumInvalidation retains signature and delegates ReadM10MomentumSource; UpdateExtremeLifecycle retains signature and defers before owner reset when source is unavailable.
- [x] Observe actual native RED on Build6.10:8 PASS/14 FAIL across7TF, 0E0W, no orders; source unavailable but M08 false Momentum and owner VOID.
- [ ] Replace duplicate numeric Momentum calculation with canonical M10 ready snapshot. Guard lifecycle before any direction/TF reset. New unique Build6.11 rev001.
- [ ] Native RED fixture becomes22/22 GREEN. Expand valid lifecycle/raw/source-history and unavailable classes, including owner identity/reset and duplicate candle behavior.
- [ ] Run affected native regressions and exact-source controller comparison; retain REDs and classify any fixture dependency separately.
- [ ] Bind final source/includes/harness/binaries/traces, inspect regression effects, publish acceptance/checkpoint and verify GitHub before SIG-06.

No standalone execution expansion, custom admission, merge/deployment, session/epoch promotion or new BBMA rule.


Progress: rev002 direct22/22 GREEN; independent review exposed M09 Extreme-handover availability propagation. Native expanded106 PASS/35 FAIL includes28 direct unavailable handover failures and7 actual M09 second-read revision failures (mutation after162 reads). Rev003 adds explicit availability output and updates all3 M09 callers before cursor changes. Driver8896 running source141/lifecycle716 plus18 existing native groups/controller610. Initial lifecycle295/141 was test-only missing g_processing_time, corrected before acceptance; no production change for that fixture. SIG-05 remains IN_PROGRESS.
