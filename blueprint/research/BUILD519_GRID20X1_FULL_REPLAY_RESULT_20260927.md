# Build 5.19 GBPUSD — Tester-Only Grid20x1 Full Replay

Issue: #285  
Baseline implementation: `q9-nmje-v2-build516-forward-m5-prep-101@a6b8fca43d2ba39bbd76d537500db6b016f9fbd6`

## Classification

**ENGINEERING RESEARCH ONLY / NOT BBMA CORE / NOT EXECUTABLE PRODUCTION AUTHORITY**

No canonical EA file was changed.

## Tester harness

The grid overlay was applied to the already-verified Build 5.19 offline tester adapter, not directly to canonical production source.

Working Build 5.19 tester-adapter MQ4 baseline SHA-256:
`841A400D34A2B090BFC4AF2C665357BE3FF046A30436D0CFB02E5B04487A87AB`

Grid harness MQ4 SHA-256:
`F88B06A7D5C5F4932C4A89E088A5A683EE45A2F3AB212ABC2CC8073B2E6C9379`

Grid harness EX4 SHA-256:
`CB968FEDF14B3A921AB7D0BAF7E611B2A811265C8A05B244AA02569ACED6E7F1`

Native compile:
- 0 errors
- 0 warnings

Harness build tag:
`V519_GRID20X1_TESTER_20260927`

## Locked test setup

- Pair: GBPUSD
- Period: M15
- Model: Every Tick
- Window: 2026-03-01 through 2026-09-01 continuous
- EntryMode=1
- MaxTradePerPair=1
- MaxTotalTrade=1
- MaxActivePair=1
- MMMode=AUTO
- AutoLotPercent=1.5
- MaxAutoLot=1.0
- TradeLockMode=0
- MinRRRatio=0
- MaxSLPips=60
- NMJE forward evidence ON
- NMJE active selection ON
- DebugLevel=4

Control and treatment used the same compiled harness. The only treatment gate was `EnableGrid20x1Research`.

## Grid20x1 engineering mapping

Applied only when a normal C044 lifecycle close was latched while the original position was floating negative.

- preserve L1 instead of executing the loss close;
- anchor = market price at attempted lifecycle loss close;
- one L2 maximum;
- L2 trigger = 20 pips further adverse from anchor;
- L2 lot = 1.0x L1 current lot;
- original SL retained as hard stop on both positions;
- before L2: close L1 when original entry is recovered;
- after L2: close both at weighted basket breakeven;
- 24-hour timeout;
- emergency/portfolio close remains higher authority;
- research L2 uses a non-canonical tester-only magic range;
- L2 send failure falls back to canonical lifecycle close.

This mapping is not sourced BBMA semantics.

## Control result — Grid OFF

Report SHA-256:
`F4E2BB8590BD5CBD9C549CE95108CF729EE502A0474F3974A4C48CBB080CADDF`

- Net profit: **+1038.38**
- Profit factor: **1.67**
- Total trades: **49**
- Relative / maximal DD: **9.19%**
- Initial deposit: 10000

## Grid ON result

Report SHA-256:
`C08180DA0B47AFC2DDDAF4F699841DE7C2992FFA1BCB1A1520C9E303B81D7D8B`

- Net profit: **-167.07**
- Profit factor: **0.94**
- Total trades: **57**
- Relative / maximal DD: **11.27%**
- Initial deposit: 10000

Delta vs control:
- Net profit: **-1205.45**
- Profit factor: **-0.73**
- Trades: **+8**
- Relative DD: **+2.08 percentage points**

## Overlay runtime evidence

Grid events:
- ACTIVATE: 26
- L2_OPEN: 6
- L2_SEND_FAIL: 1
- L1_BE: 11
- BASKET_BE: 1
- TIMEOUT24H: 1
- L2_GONE_RELEASE: 0
- EMERGENCY_RELEASE: 0

Canonical executions under Grid ON:
- canonical exec count: 51
- duplicate DecisionIDs: 0
- duplicate canonical tickets: 0

Runtime:
- zero divide: 0
- array out of range: 0
- critical error: 0
- unresolved stack function: 0
- access violation: 0
- Build tag identity: PASS
- NMJE active marker: PASS
- deinit reason 0: PASS

A real broker constraint was also observed: at least one L2 trigger failed with `Error 130` and correctly fell back to canonical close. This was retained as part of the full-replay result rather than synthetically forced.

## Decision

**GRID20X1 FULL REPLAY FAILS.**

The earlier loss-subset counterfactual suggested a small improvement, but once the overlay was replayed through the full six-month EA path with equity, AutoLot, subsequent signals and broker-order constraints, performance deteriorated materially:

- profitable control became net negative;
- PF fell below 1;
- DD increased above the prior 10% research cap;
- the execution path produced additional downstream canonical trades because the changed lifecycle/equity state altered later behavior.

Therefore:
- do not promote Grid20x1;
- do not add martingale/grid authority to canonical EA;
- no BBMA Strategy Core change is authorized;
- no production setting change is authorized.
