# Tengri + BBMA Hedge diagnostic replay — 2026-11-23

## Status

**Diagnostic mechanics replay only. Performance and margin results are not validated.** The replay used an MT5 archive from **HFMarketsGlobal-Demo4**. The locked target is MT4 **HFMarketsSV-Demo Server**. The source feed does not match the target, and complete pre-window warm-up has not been demonstrated.

No production EA was changed and no trading was activated.

## Locked replay behavior

- Window: 2026-05-01 through 2026-11-18.
- Symbols: EURUSD and USDCHF.
- Signals: D1/H4/M15-approved BBMA Re-Entry events; Type 1–4 run as separate variants.
- Entry gate: Tengri net-side layer 6 or higher; hedge at 25% of current net Tengri lots, rounded down to 0.01; maximum spread 3 pips.
- Common signal exit: first fresh approved H1 Re-Entry in Tengri's current net direction.
- Safety handling: close if Tengri becomes flat or changes side; trim hedge when the Tengri basket shrinks.

“Accepted entry” includes an accepted signal that caused no order because the hedge was already at target. The entry-order column counts actual opens/adds. Exit/trim counts are actions, so one hedge campaign can produce more than one partial trim.

## Results

| Type | Pair | Approved signals | Blocked by D1/H4 gate | Other blocked | Accepted entry signals | Actual entry/add orders | BBMA exit signals | Safety closes | Basket trims | Repeat campaigns after safety/trim | Re-entries after BBMA exit |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Type 1 | EURUSD | 18 | 15 | 12 | 6 | 5 | 0 | 4 | 4 | 3 | 0 |
| Type 1 | USDCHF | 24 | 17 | 14 | 10 | 8 | 0 | 3 | 10 | 4 | 0 |
| Type 2 | EURUSD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Type 2 | USDCHF | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Type 3 | EURUSD | 18 | 21 | 12 | 6 | 5 | 0 | 4 | 3 | 3 | 0 |
| Type 3 | USDCHF | 23 | 19 | 15 | 8 | 7 | 0 | 2 | 9 | 4 | 0 |
| Type 4 | EURUSD | 35 | 29 | 25 | 10 | 10 | 0 | 5 | 11 | 5 | 0 |
| Type 4 | USDCHF | 36 | 27 | 28 | 8 | 7 | 0 | 3 | 9 | 5 | 0 |

## What the trace shows

The common BBMA H1 exit was **never accepted while a hedge was open** in these event streams. Every recorded close/trim action came from Tengri becoming flat/changing side or from the Tengri basket shrinking. There were repeat Hedge campaigns after those safety/trim closures, but **no confirmed re-entry after the common BBMA exit**, because that exit did not occur.

This does not prove BBMA cannot produce an exit. It shows that the tested approved event stream did not contain a matching exit at the required time while a Hedge was active. The next diagnostic should inspect H1 Re-Entry event generation and the current Tengri direction at each open-hedge interval before assessing exit quality.

Example event timestamps from the trace (the runner renders the source epoch as UTC; broker civil-time metadata was not independently verified):

- Type 1 EURUSD opened SELL on 2026-06-22 05:00:00Z at Tengri layer 6, net 1.24 lots; Hedge order 0.31 lots. First full safety close was 2026-06-26 15:55:16Z at Tengri layer 4.
- Type 3 USDCHF opened BUY on 2026-06-22 18:00:00Z at Tengri layer 7, net -2.91 lots; Hedge order 0.72 lots. First basket trim was 2026-06-24 16:31:02Z: 0.06 lots trimmed, with 0.66 lots remaining.

The JSON trace contains each received/blocked event, its reason, signal and evaluation timestamps, Tengri layers/net lots, each actual entry/exit/trim action, Hedge ticket count, and re-entry classification.

## Explicitly not reported

P&L, expectancy, profit factor, floating drawdown, costs, margin use, stop-out safety, and production performance remain **unverified**. The diagnostic JSON omits financial performance fields.
