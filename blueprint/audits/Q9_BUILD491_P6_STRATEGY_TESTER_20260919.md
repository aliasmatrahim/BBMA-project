# Q9 Build 4.91 P6 Strategy Tester Functional Runtime — 2026-09-19

Issue: #101
Draft PR: #198
Branch: `q9-nmje-v2-p6-maturity-fingerprint-101`
Canonical Build: `4.91` / `V491_Q9_P6_MATURITY_FINGERPRINT_20260919`

## Classification

**STRATEGY TESTER FUNCTIONAL RUNTIME PASS**

This record closes the Saturday functional-runtime gate requested for P6 using MT4 Strategy Tester historical execution.

It does **not** claim:
- live-terminal timer verification;
- live broker/login verification;
- a naturally occurring valid M5 shadow context;
- production activation.

Live-terminal/`OnTimer` smoke remains a separate follow-up for Monday.

## Canonical identity

Canonical source was not modified for Strategy Tester compatibility.

- canonical MQ4 SHA-256:
  `B9AB1289153DD3505E1B96C1970F30435A4819A2EDC3C8ED6E7E4E23140102E4`
- canonical runtime-name compile:
  0 errors / 0 warnings
- canonical runtime-name EX4 SHA-256:
  `DBC4BA11AB2FE507E55B49283CD0D0A44F7434BB8710027D4EA7673B94377FDC`

## Tester-only adapter

A local, non-committed tester harness was generated from the exact canonical source.

Only three tester-environment adaptations were allowed:
1. `IsTerminalConnected()` returns true when `IsTesting()`;
2. `FindActualSymbol()` accepts the current Strategy Tester symbol when broker symbol enumeration is unavailable;
3. `EventSetTimer(1)` is skipped only while `IsTesting()`.

Diff firewall PASS:
- no change to P6 maturity classifiers;
- no change to combination construction;
- no change to canonical comparator;
- no change to M15 PriorityEngine;
- no change to M16 invalidation;
- no change to risk;
- no change to preflight;
- no change to broker send/retry.

Tester harness identities:
- P6 tester MQ4 SHA-256:
  `81F3A4ACAC1C6BAD5A157F796D9AF09595E994A11E6461211331FC9134E60FB3`
- P6 tester EX4 SHA-256:
  `407F8CCEF6E9243202047CBAC65F2F98F0BC120DC3F5A60B4043B16528DC1D17`
- P5 tester MQ4 SHA-256:
  `85A8FA6054013845767C6B09613E82426C046EC9863B968FB43AFD1825186B92`
- P5 tester EX4 SHA-256:
  `34A3E679F7A9451918742C2F68BF8C82EB68DC8C6BEF93B4B6A043A9B3E5DD73`

Both tester harnesses compiled 0 errors / 0 warnings.

## Functional smoke

EURUSD smoke proved:
- exact `[F7-BUILD]` Build 4.91 identity;
- successful `OnInit`;
- valid pair initialization;
- closed-M15 processing;
- historical NMJE observer execution;
- base maturity transitions including `MOMENTUM_CONTINUATION` and `RE_CONFIRMED`.

GBPUSD one-day probe then proved the cached/offline symbol path:
- GBPUSD M15;
- 96 tick events / 96 bars;
- clean deinit;
- base maturity transitions including `RE_CONFIRMED` and `DIRECTION_STAGE`.

## August 2026 deterministic A/B

Pair/TF: GBPUSD M15
Window: 2026-08-01 through 2026-09-01
Trade caps:
- MaxTradePerPair=0
- MaxTotalTrade=0

Both P6 runs:
- 2016 tick events;
- 2016 bars;
- 3017 bar states;
- clean deinit;
- zero broker-action markers.

After removing only the wall-clock performance-summary line, P6-A and P6-B contain 20,662 strategy/event lines each.

Normalized deterministic SHA-256 for both:
`457B204DB50A71604995D349249BEC00E8C6E4E79A9BE20B74BF45D86373F3F7`

Result: **deterministic equality PASS**.

## Exercised base maturity coverage

P6-A base journey maturity observations:
- `MOMENTUM_CONTINUATION`: 102
- `RE_CONFIRMED`: 1705
- `DIRECTION_STAGE`: 72
- `OWNER_ONLY`: 10
- `MHV_MATURE`: 90
- `EXTREME_MATURE`: 37

These are descriptive observer metadata only. No maturity value entered selection, validation, risk or execution authority.

## P5 versus P6 authority regression

P5 baseline used the same GBPUSD M15 August window and isolated-state reset.

Exact equality:
- `[P3M2][M15_COUNTS]`: 523 vs 523
  SHA `2323F5D0BF064A3E437807DAF2426C843E70382B393900C503E87929457BF02F`
- `[P3M2][M15_SELECT]`: 523 vs 523
  SHA `7CC31E3A9E55C1A91A5E37C975D6451ADA99390E9946DC382B17B56BDA9BCDC1`
- `[P3M2][M16_PASS]`: 523 vs 523
  SHA `9B016D2A8DA87903541C2490F8064A0424E0409526F9E3980DB4294D8443C62F`
- `[P3M2][DECISION_FINAL]`: 523 vs 523
  SHA `5C34C6588D7D6DD2DAE291C2811BE44388DF6798ABF561069D46D46A8215ED86`

Result: **P5/P6 authority regression equality PASS**.

No broker-action markers were found in P6-A, P6-B or P5 baseline.

## Natural M5 context coverage

No synthetic signal/context was created.

Bounded GBPUSD historical searches:
- January 2026: 2016 M5 shadow observations, `PRESENT=Y` = 0
- March 2026: 2112 observations, `PRESENT=Y` = 0
- May 2026: 2016 observations, `PRESENT=Y` = 0
- July 2026: 2208 observations, `PRESENT=Y` = 0
- August 2026 P6-A: 2016 observations, `PRESENT=Y` = 0

Total bounded single-run observations: 10,368.
Natural valid M5 context occurrences: 0.

Classification: **VERIFICATION REQUIRED for natural M5-context branch exercise only**.

This does not authorize synthetic M5 events and does not change P3/P6 authority. M5 maturity mapping remains covered by static/model tests, not natural historical runtime evidence.

## Environment restoration

The isolated tester `profiles\gvariables.dat` was restored after validation.

Restored SHA-256:
`AA6F6663F81F2278953EF87147C53EA0A9FF8F7947C8BE6CAB1DC285D4F0F208`

Q3 terminal and Q6 acquisition process were not intentionally modified by this validation.

## Exit result

The requested P6 Strategy Tester functional-runtime exit criteria are met:
- historical P6 state transitions exercised;
- deterministic replay PASS;
- P5/P6 authority regression PASS;
- zero broker actions;
- canonical source unchanged.

Remaining follow-ups are explicitly separate:
1. live-terminal/`OnTimer` smoke on Monday;
2. natural M5-context runtime coverage when/if a genuine event occurs.

P7 was not started by this validation task.
