# Build 4.81 C10 Strategy Tester Evidence — 2026-09-08

Status: **PASS for targeted tester/runtime-mechanism evidence; NOT a substitute for the pending broker-clock physical ACTIVE restart.**

## Identity
- EA: `BBMA_EA_BUILD481_C10_ISSUE122_0E0W`
- BuildID: `4.81`
- source SHA-256: `5DE9FD783BB930CC0591612479FE9D9440C938C142D91CB3BA978A233A658D57`
- embedded C10 SourceHash: `D6B0ADB94BB4EFB2829B33519550D349FABCB8C77251B6477E17489651F2089D`
- runtime EX4 SHA-256: `05733566540A2E5F0BA109BADA7EB17920DF5853201DAA5D9E8023E65C1912C0`
- StrategyID=1; InstanceID=81; `EnableC10StatisticsLedger=true`; `EnableC10ShadowOutcomes=true`.
- `MaxTradePerPair=0`; `MaxTotalTrade=0`.

## Tester run
- terminal: MetaTrader 4 Build 1479 / MetaQuotes-Demo.
- symbol/timeframe: GBPUSD M15.
- range: 2026-08-10 through 2026-08-12.
- model: Control points; spread=20.
- report: `C10DB_481_ACTIVE_KNOWN.html`.
- report Bars in test=1193; Ticks modelled=7769; mismatched chart errors=0.
- Total trades=0; total net profit=0.00.

This run is used only for C10 state/lifecycle/evidence validation. The MT4 report explicitly labels Control points as crude, so it is not accepted as profitability or strategy-performance evidence.
## C10 observations
- Build-4.81 tester log lines: 1932.
- `[C10][SHADOW_REGISTER]`: 3 genuine geometry-validated shadow registrations.
- `[C10][SHADOW_OUTCOME]`: 5 outcomes total.
- `[C10][SHADOW_UNPROVABLE]`: 2 fail-closed cases.
- `[C10][LEDGER_DISABLED]`: 0.
- `OrderSend`: 0; `OrderClose`: 0; `OrderModify`: 0; `OrderDelete`: 0; `DEC_EXECUTED`: 0.
- signal ledger rows: 28; duplicate EventID=0.
- outcome ledger rows: 5; duplicate OutcomeEventID=0.
- all signal/outcome rows are BuildID 4.81 and ConfigFingerprint `71748A56F01A2E3F`.
- end-of-run checkpoint rows: 5 `SEEN`, 0 `ACTIVE` because the registered shadows had resolved before tester shutdown.

Observed realized shadow outcomes:
- `GBPUSD|2026.08.10 13:00|1|7|6365325817470039`: TP after enrollment.
- `GBPUSD|2026.08.10 21:00|1|7|1751981D97A28A12`: EXPIRED at canonical expiry.
- `GBPUSD|2026.08.11 20:00|1|7|FFCD29ABCA31595F`: SL after enrollment.

Two additional rows fail-closed as `UNKNOWN / EXPIRY_UNPROVABLE`; neither creates a broker trade.
## Acceptance relevance
This evidence strengthens Issue #122 acceptance for:
- no broker execution under C10 Authority=NONE;
- deterministic geometry-validated shadow registration;
- post-enrollment TP/SL/expiry outcome handling;
- fail-closed unprovable cases without global ledger disable;
- provenance-domain EventID/OutcomeEventID uniqueness.

It does **not** close the acceptance item `active checkpoint remains recoverable across a physical restart`, because the tester run completed all ACTIVE rows before shutdown and is not a broker-clock same-terminal restart capture.

## Included artifacts
- exact MT4 report + graph;
- filtered Build-4.81 tester log;
- exact tester `.ini` + `.set`;
- C10 signal/outcome/checkpoint CSVs;
- MQ4/EX4/report/log SHA-256 records.

No Strategy Core, risk/MM, execution authority, canonical `d1-owner-dev` source or production deployment is changed by this evidence package.
Packaging note: the byte-exact generated HTML report and filtered tester log are retained inside `raw_report_log_bundle.zip` to preserve raw whitespace while keeping repository text checks clean. Their individual SHA-256 records remain alongside the bundle; the generated GIF is also retained as a standalone artifact.