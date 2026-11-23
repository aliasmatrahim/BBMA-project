# Tengri + Hedge: MT4 data acquisition gate

## Why the locked historical replay is still on hold

The requested replay is locked to EURUSD and USDCHF, 1 May–18 November 2026, with enough earlier D1 data to warm up the BBMA D1/H4/H1 filters. The G40 audit found only limited HFM MT4 terminal history and no complete raw Bid/Ask archive for that period. The existing full tick archive was fetched through MT5 from `HFMarketsGlobal-Demo4`; it is a different platform/server source and must not be substituted into the MT4 test.

The HFM MT4 terminal installed on G40 currently has only EURUSD/USDCHF H4 history files in its default history folder and no populated tester history. The MT4 research terminals used for prior runs are separate from this HFM installation. No credentials were read, no HFM terminal was connected, and no capture program was attached to a chart. The research indicator compiled on G40's MT4 build 1492 with 0 errors and 0 warnings.

## Two valid paths

### A. Historical replay for 1 May–18 November 2026

Ask HFM support whether they can provide historical bid/ask tick files for the exact MT4 demo server `HFMarketsSV-Demo Server`, for EURUSD and USDCHF, including at least 51 closed D1 sessions before 1 May. The export must identify the server, timezone, symbol names, and timestamp basis. Keep the original files unchanged and record SHA-256 hashes.

If HFM cannot provide that archive, the old locked historical tick replay cannot be reproduced from the current MT4 files. The only fallback is to re-lock a lower-fidelity MT4 bar-based study using verified HFM MT4 M1 bars and the MT4 Strategy Tester’s `Every tick` model. MT4 documents that this model interpolates ticks from lower timeframes and that stored history is Bid-based with Ask modeled from a spread. Such a study can screen signal rules; it cannot validate historical Bid/Ask execution or margin excursions tick by tick. Do not mix that result with the locked tick test.

### B. Independent forward holdout from MT4

`MT4_TickCapture_Research.mq4` is a demo-only chart indicator that records the Bid/Ask quotes delivered to an MT4 chart. It refuses the Strategy Tester, non-demo accounts, a different server, and the wrong symbol. It contains no order functions. Attach one copy to an EURUSD chart and another to a USDCHF chart in a separate HFM demo research terminal. It writes one CSV file per server day under `MQL4/Files/MT4RawTicks/`.

This captures only from the time it is attached; it cannot recover ticks from February–November 2026. Use the captured period as a future, untouched holdout and keep it separate from May–November development results. Attach one copy to each chart and set `ExpectedSymbolPrefix` to `EURUSD` or `USDCHF` for that chart. Since the indicator itself does not trade, AutoTrading is not needed. Do not attach it to a terminal that has other trading EAs enabled.

HFM documents its server clock as GMT+2 in winter and GMT+3 in summer, with DST changes at the last Sunday of March and October. Use `Europe/Helsinki` for timestamp checks only after verifying the MT4 server label and clock against the account terminal. The capture output stores both UTC and server time plus the offset so DST changes can be audited.

## Run the data-quality gate

After collecting exact-server MT4 files, merge the daily CSVs per pair with the helper below. It leaves the daily files unchanged and writes hashes into a sidecar manifest. Then run the validator:

```powershell
python merge_mt4_tick_files.py `
  --input-dir "C:\path\to\MQL4\Files\MT4RawTicks" `
  --symbol EURUSD `
  --out EURUSD_ticks.csv
python merge_mt4_tick_files.py `
  --input-dir "C:\path\to\MQL4\Files\MT4RawTicks" `
  --symbol USDCHF `
  --out USDCHF_ticks.csv
python validate_mt4_tick_archive.py `
  --eurusd EURUSD_ticks.csv `
  --usdchf USDCHF_ticks.csv `
  --source-server "HFMarketsSV-Demo Server" `
  --server-timezone Europe/Helsinki `
  --out mt4_tick_manifest.json
```

The default window is 1 February 2026 00:00 UTC through 18 November 2026 23:59:59 UTC, with evaluation from 1 May and a minimum of 51 weekday D1 warm-up sessions. Because HFM is GMT+2/+3, the server-date coverage includes part of 19 November. `PASS_DATA_QA_ONLY` means the CSV structure, quotes, timestamps, metadata, warm-up count, and weekday coverage passed. It does not prove that the broker produced the file, validate execution quality, or show profitability. Preserve terminal evidence and verify the account’s actual server separately.

## Next test sequence after data passes

1. Reconcile the two small remaining statement residuals from the original account statement.
2. Pin the existing Build 5.16 event stream and the exact HFM server/timezone evidence.
3. Run the locked set: Tengri baseline, then BBMA Type 1, Type 2, Type 3, and Type 4 separately; same size rules, exit, costs, and margin stress for all variants.
4. Report expectancy, profit factor, combined and hedge P&L, floating drawdown, minimum equity/free margin, costs, trade and re-entry counts, rejected fills, and any open hedge exposure at the end.
5. Keep May–November as development data. Select no “best” setting until a separate holdout is complete.

EA production source remains unchanged; this capture indicator is not attached or trading-enabled by this research package.

## Official references

- [HFM trading hours and server time](https://www.hfm.com/sc/en/trading-instruments/trading-hours)
- [MetaTrader 4 Strategy Tester modeling modes](https://www.metatrader4.com/en/trading-platform/help/overview/strategy_tester/strategy_tester_setup)
- [MetaTrader 4 History Center](https://www.metatrader4.com/en/trading-platform/help/service/history_center)
- [HFM Tick Chart Trader guide](https://static.hfm.com/assets/docs/tools_hfm/premium-trader-tools/tick-chart-trader-user-guide-HFSC-en.pdf?v=68)
