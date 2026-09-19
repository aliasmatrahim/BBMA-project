# Q9 Build 4.91 P6 Validation — 2026-09-19

Status: **STATIC/CROSS-MODULE/NATIVE COMPILE PASS + STRATEGY TESTER FUNCTIONAL RUNTIME PASS — LIVE TERMINAL/TIMER FOLLOW-UP PENDING**

## Exact identity

- Version: `4.91`
- BuildTag: `V491_Q9_P6_MATURITY_FINGERPRINT_20260919`
- SourceRev: `Q9_P6_MATURITY_FINGERPRINT_101_20260919`
- Git source blob before commit: `3818e4befd3a71981d6aeca33c86f19192cea7d6`
- MQ4 SHA-256: `B9AB1289153DD3505E1B96C1970F30435A4819A2EDC3C8ED6E7E4E23140102E4`
- exact runtime-name EX4 SHA-256: `DBC4BA11AB2FE507E55B49283CD0D0A44F7434BB8710027D4EA7673B94377FDC`
- EX4 size: 619134 bytes

## Static / model / regression

PASS:
- Q9 P6 maturity static firewall
- Q9 P6 maturity persistence/model
- P5 conflict refinement
- P4 attribution static
- P4 persistence model
- P2/P3 shadow
- P1 epoch model
- NMJE read-only authority
- M12N orchestration order
- D1O execution identity
- N3 policy-readiness activation firewall
- protected authority function-body comparison vs P5
- `git diff --check`

## Cross-module authority

Protected function bodies are unchanged from P5:
- combination construction;
- canonical comparator;
- M15 priority;
- M16 invalidation;
- risk;
- preflight;
- signal-allowed;
- broker send/retry.

No P6 maturity symbol occurs in those authority bodies.

Order primitive counts remain 1/3/0/0 for Send/Close/Modify/Delete.

## Native compile

Exact runtime deployment filename:
`D:\BBMA\MT4_NMJE_141_Demo\MQL4\Experts\BBMA_EA_Q9_491_P6.mq4`

MetaEditor:
`Result: 0 errors, 0 warnings, 1141 msec elapsed`

The deployed MQ4 hash equals the worktree source hash.

## Saturday live-terminal attempt

Profile: `Q9_491_P6_READONLY`
- EURUSD M15
- ExpertsTrades=false
- MaxTradePerPair=0
- MaxTotalTrade=0
- InstanceID=91

Two bounded attempts both reached:
- terminal start;
- Expert `BBMA_EA_Q9_491_P6` loaded;
- zero-trade inputs logged.

Neither attempt reached broker login / attributable OnInit completion / `[F7-BUILD]` / NMJE observer logs.

Classification for this path: **LIVE TERMINAL/TIMER NOT VERIFIED**.

Per user direction, live-terminal/`OnTimer` verification is deferred to Monday and is not substituted by the Strategy Tester result below.

## Strategy Tester functional runtime

A local non-committed tester harness was derived from the exact canonical source with tester-only:
- connection bypass under `IsTesting()`;
- current tester-symbol fallback under `IsTesting()`;
- timer-registration skip under `IsTesting()`.

Diff firewall confirmed no P6 classifier or authority-path changes. Both P5 and P6 tester harnesses compiled 0E/0W.

GBPUSD M15 August 2026:
- P6-A: 2016 bars / clean exit;
- P6-B: 2016 bars / clean exit;
- P5 baseline: 2016 bars / clean exit;
- zero broker-action markers.

P6 A/B deterministic replay:
- 20,662 normalized strategy/event lines each;
- normalized SHA-256 both:
  `457B204DB50A71604995D349249BEC00E8C6E4E79A9BE20B74BF45D86373F3F7`;
- only discarded difference was the wall-clock performance-summary duration line.

Base maturity states exercised:
- MOMENTUM_CONTINUATION: 102
- RE_CONFIRMED: 1705
- DIRECTION_STAGE: 72
- OWNER_ONLY: 10
- MHV_MATURE: 90
- EXTREME_MATURE: 37

P5/P6 exact authority equality:
- M15_COUNTS: 523 / 523
- M15_SELECT: 523 / 523
- M16_PASS: 523 / 523
- DECISION_FINAL: 523 / 523

See:
`blueprint/audits/Q9_BUILD491_P6_STRATEGY_TESTER_20260919.md`

Classification for this path: **STRATEGY TESTER FUNCTIONAL RUNTIME PASS**.

## Natural M5-context coverage

No synthetic signal/context was created.

Bounded GBPUSD historical search over January, March, May, July and August 2026 produced 10,368 single-run M5 shadow observations with:
- `PRESENT=Y`: 0.

Therefore:
- base P6 maturity runtime is exercised;
- M5 natural-context branch is **not naturally runtime-exercised**;
- M5 maturity mapping remains static/model validated only.

This is a bounded coverage gap, not evidence that the source rule/context does not exist.

## Result

The requested P6 Strategy Tester functional-runtime exit criteria are complete:
- historical maturity transitions exercised;
- deterministic rerun PASS;
- P5/P6 authority regression PASS;
- zero broker actions;
- canonical source unchanged.

Do **not** claim live-terminal/timer verification from this result.

Remaining separate follow-ups:
1. live-terminal/`OnTimer` smoke on Monday;
2. natural M5-context runtime coverage if/when a genuine event occurs.

P7 was not started by this validation task.
