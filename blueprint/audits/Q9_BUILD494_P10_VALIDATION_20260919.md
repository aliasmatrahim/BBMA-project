# Q9 Build 4.94 P10 Validation — 2026-09-19

Status: **STATIC/MODEL/CROSS-MODULE/NATIVE COMPILE PASS + STRATEGY TESTER AUTHORITY REGRESSION PASS**

P10 post-fill displacement telemetry is **BOUNDED-UNEXERCISED** in the zero-trade tester profile and remains **VERIFICATION REQUIRED** for a natural successful-fill runtime branch.

## Identity

- Version: `4.94`
- BuildTag: `V494_Q9_P10_ENTRY_DISPLACEMENT_20260919`
- SourceRev: `Q9_P10_ENTRY_DISPLACEMENT_101_20260919`
- canonical MQ4 SHA-256:
  `25F57C7E39CCB516B3463614CC77C4C924DA95753121E8F9605E10351DBC3CF6`
- short-path EX4 SHA-256:
  `9BD4EAA603A20B9BFFE4C11E2CDA099F77FC38C25E04A753DF55A852224AAE66`
- exact runtime-name EX4 SHA-256:
  `D2AE82940F1DF91F4CC54EF6D2686C3EA4D1C485C2BCD65DE67D06AAE2715832`

## Static / model / inherited regression

PASS:
- P10 entry-displacement static/model;
- P8 provenance stability static/model;
- P7 structural density static/model;
- P6 maturity static/model;
- P5 conflict refinement;
- P4 attribution static/persistence;
- P2/P3 shadow;
- P1 epoch model;
- NMJE read-only authority;
- M12N orchestration order;
- D1O execution identity;
- N3 activation firewall;
- `git diff --check`.

Historical `test_q9_nmje_p1_current_owner_static.py` remains intentionally outside the post-Stage-C gate because it hard-codes the obsolete owner/build assumptions already excluded by P6/P8 validation.

## Protected-body comparison

P8 -> P10 exact body equality PASS for:
- M13 combination construction;
- M14 candidate construction;
- canonical comparator;
- M15 PriorityEngine;
- M16 invalidation;
- execution reference resolution;
- M17 approved SL/TP resolver;
- risk;
- preflight;
- `IsSignalAllowed`;
- broker `SendOrderWithRetry`.

## Native compile

Short-path exact-source: `0 errors, 0 warnings, 1174 msec`.

Exact runtime-name: `0 errors, 0 warnings, 1027 msec`.
Tester-only adapter:
- canonical SHA `25F57C7E39CCB516B3463614CC77C4C924DA95753121E8F9605E10351DBC3CF6`;
- tester MQ4 SHA `EDB70A67CEE7910E2FDF6A2C87B7C2F297CC1501DC3DA4A556BCBFD77B076945`;
- adapter diff lines: 46;
- adapter diff firewall: PASS;
- tester compile: `0 errors, 0 warnings, 1239 msec`;
- tester EX4 SHA `0EA0E2D13363B52FCC480D5FEEA4A0FC6EDE9D111D0270BE320E64D7248789FA`.

Allowed tester-only deltas are the same three verified P8 adapters:
1. `IsTerminalConnected()` allows `IsTesting()`;
2. tester symbol fallback in `FindActualSymbol()`;
3. timer registration skipped under `IsTesting()`.

## Strategy Tester

Pair/TF: GBPUSD M15.
Window: 2026-08-01 through 2026-09-01.
Model: 0.
Zero-trade caps remain:
- `MaxTradePerPair=0`;
- `MaxTotalTrade=0`;
- `MaxActivePair=1`.
`InstanceID=94`.

P10-A and P10-B each processed 2016 tick events / 2016 bars / 3017 bar states with clean exit and `FORCED=False`.
After dropping only the wall-clock performance-summary line:
- A normalized lines: 24,172;
- B normalized lines: 24,172;
- exact equality: PASS;
- SHA-256 both:
  `45501221FB9D6AF0AAE79FD5C3E76638A8B4C7B454EDA2F8AC93AD3DCEE20411`.

## P8 -> P10 authority regression

Exact equality:
- M15_COUNTS: 523 / 523;
- M15_SELECT: 523 / 523;
- M16_PASS: 523 / 523;
- DECISION_FINAL: 523 / 523;
- M15 conflict / M16 reject / owner reject / D1O block families remain 0 / 0 where absent.

Aggregate authority trace:
- P8: 2,092 lines;
- P10: 2,092 lines;
- exact equality: PASS;
- SHA-256 both:
  `EFF894BAA8497EF6EB4A54AD43EB6354D80D61772B202E1ADBEAC430FEF2DDBF`.

Broker-action markers: P8=0, P10-A=0, P10-B=0.
Runtime error scan: none in P10 A/B.
## P10 telemetry runtime coverage

`[Q9-P10-DISP-OPEN]` and `[Q9-P10-DISP-OUT]` counts are 0 in both A/B.

This is expected because the safety profile intentionally prevents broker execution with `MaxTradePerPair=0` and `MaxTotalTrade=0`.

Classification: **BOUNDED-UNEXERCISED / VERIFICATION REQUIRED for natural successful-fill P10 telemetry only**.

No synthetic fill was introduced. This does not block the P10 authority-preservation exit gate because the contract explicitly allows this classification when no successful fill exists in the bounded tester window.

## Environment restoration

OfflineDiag GlobalVariables backup SHA-256:
`AA6F6663F81F2278953EF87147C53EA0A9FF8F7947C8BE6CAB1DC285D4F0F208`.

Restored GlobalVariables SHA-256:
`AA6F6663F81F2278953EF87147C53EA0A9FF8F7947C8BE6CAB1DC285D4F0F208`.

No OfflineDiag terminal remains. Q3 isolated Build 4.81 terminal PID 13064 remains active and untouched. Q6 was not restarted or duplicated.

## Result

**P10 implementation + authority-preservation exit gate: VERIFIED.**

Natural post-fill displacement telemetry remains separately `VERIFICATION REQUIRED / BOUNDED-UNEXERCISED`.

No merge / no production activation.
