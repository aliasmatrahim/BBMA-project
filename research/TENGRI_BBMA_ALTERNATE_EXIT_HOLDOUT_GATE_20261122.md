# Tengri + BBMA alternate-exit holdout — data gate

Date: 22 Nov 2026  
Status: **HOLD — April holdout INVALID for performance evaluation**  
Lock: `TENGRI_BBMA_ALTERNATE_EXIT_HOLDOUT_LOCK_20261122.md`  
Branch: `research/tengri-bbma-hedge-replay-20261122`

## Gate result

The pre-registered 2026-04-06 to 2026-04-30 holdout cannot be used for the locked P&L replay. The full interval requires complete quote/tick coverage for both EURUSD and USDCHF. Only four of the 19 weekdays contain non-empty tick arrays, and both symbols have data on those same four days:

| Date | EURUSD ticks | USDCHF ticks |
|---|---:|---:|
| 2026-04-06 | 28,817 | 20,666 |
| 2026-04-08 | 1,048 | 474 |
| 2026-04-29 | 82,684 | 45,776 |
| 2026-04-30 | 166,122 | 106,945 |

The other **15 weekdays have empty tick arrays for both symbols**. Their `.npz` files exist, so filename presence alone gave a false impression of full coverage. Non-empty arrays checked above had positive Bid, Ask >= Bid, and non-decreasing timestamps. This is not coverage for the full test interval.

A read-only check of the active G40 MT5 connection confirmed server **HFMarketsGlobal-Demo4** and that EURUSD and USDCHF are available. `copy_ticks_range` returned zero ticks with no API error for 2026-04-07, 04-09, 04-10, and 04-20 on both pairs. The configured broker session therefore does not provide the missing historical tick rows through the existing downloader path.

## Other April records

- Frozen Tengri ledger: 1,357 rows total, first open 2026-04-06 14:28:43.
- No Tengri order opened before 2026-04-06.
- Between Apr 6 and Apr 30 there are 200 order opens and 194 order closes; six positions extend past the Apr 30 cutoff and would need tick-based end marking.
- First external contribution is +3,578 USC at 2026-04-06 14:28:20, 23 seconds before the first order.
- D1/H4/H1/M15 bar warm-up exists from 2025-01-02, but bar coverage cannot replace the missing tick fills/marks required by the locked cost and exit test.
- No April Build 5.16 event export or performance replay was generated.

## Decision

**Stop before calculating performance.** Missing 15 weekday quote days make expectancy, profit factor, drawdown, costs, and campaign counts invalid for the locked April alternative-exit test. Do not fill these gaps with another broker, bars, interpolation, or a selectively shortened April window; that would change the locked cost/execution basis or period after registration.

The alternate exit remains locked and untested. Resume only after obtaining a complete, timestamp-verified tick archive for the entire holdout from the same broker feed, or after a new untouched forward period has accumulated complete matching quotes. The May–Nov 18 sample remains unavailable for tuning or evaluating this alternate exit.

No MT4 tester run, EA change, live/forward trade, production activation, or merge occurred.
