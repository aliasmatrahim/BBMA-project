# Tengri + BBMA Hedge — indicator feasibility study

Date: 22 Nov 2026  
Status: **RESEARCH ONLY — BBMA is technically usable as a signal input; no profitable production combination established**  
Branch: `research/tengri-bbma-hedge-replay-20261122`

## Question

Can the Hedge EA use BBMA signals, alone or with indicators such as H4 Mid-BB and ADX, to improve entry and exit timing while Tengri remains unchanged?

## Decision

**Technically yes; performance and production readiness are not established.** The pinned Build 5.16 research event stream contains closed-candle BBMA H1 Re-Entry events with D1/H4/M15 approval, so a Hedge consumer can be built around those events. The installed G40 Hedge still uses H4 Mid-BB + ADX(14)>25 + directional DI and does not read BBMA events.

The May 1–Nov 18, 2026 locked replay does not support selecting a BBMA type or indicator combination. Type 1, 3, and 4 had negative closed-campaign expectancy and reduced net account P&L versus the Tengri-only baseline; Type 2 had no eligible events/trades. Max flow-adjusted equity drawdown exceeded 100% for every variant. No normal BBMA exit event fired. This replay is not a direct, same-exit comparison against the installed ADX/H4 Hedge EA.

The pre-registered April holdout cannot answer the alternate-exit question: 15 of 19 weekdays lack matching EURUSD and USDCHF ticks. It was marked invalid before performance calculations. Do not select a winner from the May–November sample or substitute a partial April window.

## Proposed signal role

For a same-pair Tengri basket, the Hedge signal should represent the **current adverse move to insure**, rather than predict that the market has reached a reversal point:

- Tengri net long under adverse downward movement: consider a sell Hedge only when the confirmed BBMA direction is down.
- Tengri net short under adverse upward movement: consider a buy Hedge only when the confirmed BBMA direction is up.
- Keep the existing research gates: at least six same-side Tengri orders, 25% of same-pair net lots rounded down to 0.01, spread cap 3 pips, no cross-pair hedge, and first valid quote after the confirmed event/M15 decision.
- Keep Type 1–4 as separate signal variants. Do not relax or redefine a type to create more trades.

This is a research design inference, not evidence that a BBMA signal forecasts reversals or will improve account returns.

## Fixed candidate comparison

Use a single complete, untouched holdout and identical quote source, Tengri order path, size, costs, safety rules, and exit policy across entry arms. Preserve the currently locked BBMA D1/H4/M15 entry approval. Compare:

| Arm | Entry rule | Purpose |
|---|---|---|
| Control | Current H4 Mid-BB + ADX(14)>25 + DI entry logic | Measure the existing Hedge logic on the same test harness |
| A | Approved BBMA H1 Re-Entry only | Establish BBMA event timing without extra indicator filters |
| B | A + H4 ADX(14)>25 and DI aligned with Hedge direction | Test whether the existing trend-strength/direction filter improves BBMA entries |
| C | A + closed H4 Mid-BB location aligned with Hedge direction | Isolate the H4 price-location filter |
| D | A + both B and C filters | Test the combined BBMA + current H4 regime logic |

The ADX threshold of 25 is inherited from the installed EA for a controlled comparison; it is not an optimized or validated threshold. Test the four BBMA types separately within each arm. Freeze all settings before opening the holdout. If the independent data cannot support this full matrix, reduce the number of arms before seeing results and document the reduced design.

For a fair entry-timing comparison, all arms must use one shared exit policy. Separately comparing the full deployed ADX EA with a BBMA package whose exit differs can assess package performance, but cannot isolate which entry rule helped.

## Exit hypothesis

Keep exit logic independent of entry filters:

1. Close an open Hedge at the first confirmed, closed H1 Re-Entry event pointing back toward the **current** Tengri net direction. The exit closes existing hedge exposure only and bypasses the combined D1/H4/M15 entry-approval flag.
2. Keep the safety close if Tengri becomes flat or its net direction changes so that the hedge is no longer opposite.
3. Use the same exit and execution timing for every entry arm.

The ordinary locked exit had zero eligible events in the May–November replay. The alternative exit is pre-registered but untested because the April holdout failed its tick-data gate. Therefore neither exit is selected as effective yet.

## Additional indicators

- **ADX + DI:** most relevant first filter to test because it separates trend strength (ADX) from directional side (+DI/-DI), and is already present in the installed EA. In MQL4, iADX exposes the main ADX, +DI, and -DI lines. The proposed use is as a regime gate, not as a separate entry trigger. [MQL4 iADX reference](https://docs.mql4.com/indicators/iadx)
- **H4 Mid-BB:** test as a separate closed-candle location/direction filter. MQL4 exposes the Bollinger main, upper, and lower lines. Avoid conflating this filter with BBMA event logic when reporting results. [MQL4 iBands reference](https://docs.mql4.com/indicators/ibands)
- **ATR:** consider only later as a volatility/execution filter (for example, a pre-registered spread-to-range guard), not a directional signal. MQL4 iATR returns Average True Range. Do not choose an ATR threshold from the same evaluation sample. [MQL4 iATR reference](https://docs.mql4.com/en/indicators/iatr)
- Do not add RSI, MACD, or Stochastic in the first comparison. There is no project evidence that they improve Hedge entry or exit, and adding more filters at once would make attribution harder.

## Required report

For every arm, pair, and BBMA Type 1–4, report:

- eligible signals, rejected signals by each individual gate, and entry/exit event coverage;
- number of campaigns and trades, open exposure at end, and rejected/partial fills;
- net Hedge P&L and net account P&L after actual bid/ask, spread, commission, swap, and declared slippage;
- expectancy, profit factor, maximum floating drawdown, worst floating loss, and margin/stop-out events;
- base and stress-cost results;
- comparison to the same-path control.

A favourable P&L alone is insufficient if the margin/stop-out model, actual build identity, complete ticks/warm-up, or ledger-to-executable crosswalk is unresolved.

## Gates before any profitability conclusion

1. Obtain complete, timestamp-verified EURUSD and USDCHF ticks for a new independent period from the same HFM Demo4 feed; do not reuse May–Nov for selection or patch April gaps with another source.
2. Pin and reconcile the Build 5.16 signal producer, exported events, and installed/tested EA identities.
3. Verify warm-up, closed-candle timing, and individual D1/H4/M15 rejection reasons.
4. Close the existing 739.47 USC ledger reconciliation gap and verify margin, stop-out, commission, swap, and failed/partial fill behavior.
5. Freeze one entry matrix, shared exit, costs, and safety rules before running the holdout once.

## Source records

- [Locked replay result](TENGRI_BBMA_HEDGE_LOCKED_REPLAY_RESULT_20261122.md)
- [Exit coverage diagnostic](TENGRI_BBMA_EXIT_COVERAGE_DIAGNOSTIC_20261122.md)
- [Alternate-exit holdout lock](TENGRI_BBMA_ALTERNATE_EXIT_HOLDOUT_LOCK_20261122.md)
- [Alternate-exit data gate](TENGRI_BBMA_ALTERNATE_EXIT_HOLDOUT_GATE_20261122.md)

No Hedge EA source was changed. No trading was activated, no forward test was run, and no branch was merged.
