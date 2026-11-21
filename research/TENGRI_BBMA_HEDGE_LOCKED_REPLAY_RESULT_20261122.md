# Tengri + BBMA Hedge — locked replay result

Date: 22 Nov 2026  
Status: **Completed once; conditional historical overlay result; no production validation**  
Repository branch: `research/tengri-bbma-hedge-replay-20261122`

## Scope

One frozen comparison for EURUSD and USDCHF over 1 May–18 Nov 2026, with a 4,000 USC starting balance anchor. Baseline and BBMA H1 Re-Entry Types 1–4 use the same Tengri order path, HFM Demo4 quote/tick data, entry gates, exit hypothesis, and cost model. No same-sample parameter tuning was performed.

The pinned Build 5.16 event stream passed closed-candle D1/H4/H1/M15 gates. Approved events: EURUSD T1/T2/T3/T4 = 18/0/18/35; USDCHF = 24/0/23/36; combined = 42/0/41/71. Warm-up and source/build hashes are in the [checkpoint](TENGRI_BBMA_HEDGE_LOCKED_REPLAY_20261122.md).

## Locked rules

- Enter opposite same-symbol net Tengri exposure once there are at least six net-side Tengri orders.
- Hedge size is 25% of net lots, rounded down; entry spread cap is 3 pips.
- Use first valid quote after the confirmed event. All types share one exit: first confirmed H1 Re-Entry toward current Tengri net direction; safety close if Tengri goes flat or net direction flips.
- Actual Bid/Ask execution includes spread. Additional cost is 1 pip per lot per Hedge action; stress is 2 pips. The spread attribution below is already reflected in Bid/Ask P&L and must not be deducted again.
- The frozen Tengri lot path is not changed by Hedge P&L.

## Results

Account P&L is flow-adjusted after base costs. Hedge P&L includes open Hedge mark-to-market. Campaign expectancy and profit factor use closed campaigns after modeled costs. Max equity drawdown is measured on flow-adjusted equity. Actions count distinct entry/add and close/trim executions.

| Variant | Account P&L, base (USC) | Hedge P&L incl. open (USC) | Closed campaigns (wins/losses); open | Expectancy/campaign (USC) | PF | Max equity DD (USC / %) | Worst combined floating (USC) | Entry/add; close/trim |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Baseline | +7,640.34 | 0.00 | — | N/A | N/A | 7,723.28 / 113.51% | -9,198.75 | 0; 0 |
| Type 1 | +7,352.51 | -287.83 | 8 (2/6); 1 | -48.35 | 0.4575 | 6,798.96 / 104.09% | -8,279.31 | 13; 21 |
| Type 2 | +7,640.34 | 0.00 | 0; 0 | N/A | N/A | 7,723.28 / 113.51% | -9,198.75 | 0; 0 |
| Type 3 | +7,220.37 | -419.97 | 8 (2/6); 1 | -62.17 | 0.2566 | 7,204.93 / 106.10% | -8,671.49 | 12; 18 |
| Type 4 | +6,114.56 | -1,525.78 | 10 (1/9); 2 | -161.86 | 0.1232 | 6,901.26 / 102.04% | -8,374.09 | 17; 28 |

### Cost and stress table

| Variant | Added fixed cost, base (USC) | Bid/Ask spread attribution (USC) | Base total estimate (USC) | Stress total estimate (USC) | Account P&L under stress (USC) |
|---|---:|---:|---:|---:|---:|
| Type 1 | 51.97 | 52.80 | 104.77 | 156.74 | +7,300.54 |
| Type 2 | 0.00 | 0.00 | 0.00 | 0.00 | +7,640.34 |
| Type 3 | 47.81 | 47.38 | 95.19 | 143.01 | +7,172.56 |
| Type 4 | 89.33 | 88.94 | 178.27 | 267.60 | +6,025.23 |

## Findings

- Type 2 produced no eligible signals or Hedge trades. This sample cannot establish its profitability.
- No normal Re-Entry exit fired in any variant. Closes were safety exits or exposure trims. The chosen normal exit rule was therefore not exercised.
- Every variant had a negative flow-adjusted minimum equity: baseline/Type 2 -919.34 USC, Type 1 -266.87, Type 3 -414.43, Type 4 -138.06. Maximum drawdown exceeded 100% in all cases. The replay has no margin/stop-out simulation and cannot support a live-safety conclusion.
- Type 1 reduced worst combined floating loss by 919.44 USC versus baseline, but its Hedge expectancy was -48.35 USC/campaign and net account P&L fell by 287.83 USC. Type 3 and Type 4 also had negative Hedge expectancy and lower net account P&L; Type 4 lost the most.
- By pair, Type 1 was positive in EURUSD (4 closed, expectancy +45.35 USC, PF 2.253) but negative in USDCHF (4 closed, expectancy -142.04 USC, PF 0). Type 3 was weakly positive in EURUSD (expectancy +12.64, PF 1.692) and negative in USDCHF (expectancy -136.99, PF 0.0807). Both pairs lost on Type 4.

## Limitations and EA identity

This was a conditional historical overlay replay, not a verified combined two-EA account result. The frozen ledger lacks Magic/comment columns, has small reconciliation residuals, and has not been cross-walked to the actual Tengri tester executable/account build. Hedge P&L did not alter later frozen Tengri lot sizing. Broker commission, swap, slippage beyond quotes, partial/rejected fills, and margin/stop-out were not modeled.

The installed G40 Hedge build is ADX/H4-based: it reads same-symbol Magic 12345 Tengri positions, then uses H4 Mid-BB + ADX(14)>25 + DI for entries. It does **not** consume BBMA Re-Entry Types 1–4. These results come from the separate research harness and do not describe the installed EA’s behavior.

No live orders, forward trading, production activation, or merge occurred. The research harness is in `research/tengri_bbma_hedge_locked_replay.py`; raw account and tick data remain on G40.
