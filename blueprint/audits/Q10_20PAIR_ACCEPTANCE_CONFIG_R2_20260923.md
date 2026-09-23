# Q10 20-Pair Acceptance Config R2 — Build 5.11 — 2026-09-23

Issue: #109
Scope: final MetaQuotes-Demo Phase-L acceleration only
EA source: unchanged Build 5.11 / `V511_EVENT_DRIVEN_OBSERVER_20260922`

## User decision

For final live testing, widen the monitored universe to 20 pairs to increase the probability of obtaining the natural live events required by Q10, while keeping the final live test last in the overall sequence.

## Configuration boundary

Previous Q10 Phase-L profile:
- PairList: `GBPUSD`
- MaxActivePair: `1`
- settings SHA-256: `37BC585EB3AB5A73914FEC3C532023636D4FACCD7D3AAAF20B774269CF92DA70`

R2 acceptance profile:
- revision: `Q10_20PAIR_R2_20260923`
- settings file: `FINAL_BUILD511_20PAIR.set`
- settings SHA-256: `F114C1DE07ABED434B2754F210E43993E9E3D81599CA5900536E5E2F65F2E700`
- MaxActivePair remains `1`
- MaxTradePerPair remains `2`
- MaxTotalTrade remains `10`
- MMMode remains FixedLot
- FixedLot remains `0.01`
- TradeLock/risk/MM/strategy/debug/InstanceID settings are unchanged.

The only functional settings delta is PairList expansion. This increases observation/opportunity coverage without allowing concurrent exposure across multiple pairs.

## R1 broker-resolution finding

The original source-default 20-pair list was tested read-only on MetaQuotes-Demo. It resolved 18/20 pairs. `GBPAUD` and `GBPCAD` were unavailable and therefore R1 was not promoted to trade-enabled acceptance.

A separate read-only replacement probe tested fixed-PairID symbols:
- PASS: `AUDCHF`, `AUDNZD`, `CADCHF`, `EURNZD`, `GBPCHF`
- unavailable: `GBPNZD`, `NZDCAD`, `NZDCHF`

R2 replaces only the two unavailable default-list symbols:
- `GBPAUD -> AUDCHF`
- `GBPCAD -> AUDNZD`

## Final R2 20-pair universe

`EURUSD, GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD, NZDUSD, EURJPY, GBPJPY, EURGBP, AUDJPY, CADJPY, CHFJPY, NZDJPY, EURAUD, EURCAD, EURCHF, AUDCHF, AUDNZD, AUDCAD`

All 20 use the existing fixed PairID registry.

## Read-only MetaQuotes-Demo smoke

The exact Build 5.11 EX4 and R2 settings were launched on the dedicated Q10 terminal with `ExpertsTrades=false`.

Because the broker connection reinitialized once, two attributable init cycles were observed. Each cycle independently produced:
- Pair requests: 20
- Symbol resolved: 20
- Broker spec PASS: 20
- Symbol-resolution FAIL: 0
- Broker-spec FAIL: 0
- PairID validation: PASS
- Magic validation: PASS
- final initialization: `EA initialized successfully with 20 pairs`

No trade authority was enabled during the smoke. Primary Q3/C10 terminal PID 13064 remained separate and untouched.

## Evidence-provenance hardening

Changing the acceptance settings exposed a tooling provenance gap: prior stage bundles bound source/build/demo identity but not the exact runtime settings hash.

The Q10 runner is hardened so new stage evidence:
- uses `BBMA_Q10_STAGE_BUNDLE_V2`;
- records exact native EX4 SHA and settings SHA;
- uses `BBMA_Q10_STAGE_BUNDLE_SET_V2` for multi-run aggregation;
- rejects mixed runtime settings or EX4 identities;
- propagates runtime identity into stage analysis;
- rejects LIVE_RECONFIRM record-stage if analysis settings/EX4 differ from the live state.

Legacy GBPUSD-only Phase-L bundles therefore cannot be combined with R2 20-pair bundles.

## Phase-H reuse boundary

Historical Phase-H evidence remains reusable under the explicit config-delta policy because:
- EA source and EX4 are byte-identical;
- all Strategy-Core, risk/MM, TradeLock, execution limits and lifecycle settings are unchanged;
- MaxActivePair remains 1;
- the delta only widens which pair may produce a natural event;
- exact 20-pair symbol resolution, broker spec, PairID and magic isolation have now passed read-only runtime validation.

Any observed multi-pair contradiction or isolation defect invalidates this reuse and reopens the affected case(s).

## Regression

Before trade-enabled launch:
- targeted Q10 tests: **28 passed**;
- full repository tests: **72 passed**;
- canonical Git settings blob SHA equals deployed runtime settings SHA;
- EA source unchanged.

## Status

**R2 CONFIG READY FOR FORMAL PHASE-L R3 LIVE USE.**

This record does not itself claim R3 PASS. New formal R3 evidence must be collected under the R2 settings hash.
