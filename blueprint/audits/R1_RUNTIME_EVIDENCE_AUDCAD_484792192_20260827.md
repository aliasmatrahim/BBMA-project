# R1 Runtime Evidence — AUDCAD Ticket 484792192

Date: 2026-08-27
Status: ATTRIBUTED NON-D1TPW EXECUTION / DOES NOT SATISFY R1-01
Source: authenticated HFM demo MT4 runtime log supplied by operator

## Evidence

Runtime log around 2026-08-27 20:17 shows:

- Pair: AUDCAD
- Signal: `SIGNAL_RE_ENTRY`
- Direction: `DIR_BUY`
- Validate candle: `2026.08.27 15:30`
- Process time: `2026.08.27 15:45`
- D1 state visible immediately before execution: `D1_OWNER_BUY_CONFIRMED`
- M16 validation: PASS
- M17 structural SL/TP source timeframe: M15 (`TF=15`)
- Structural anchor: `0.99602`
- Confirmation wick: `0.99653`
- Final broker SL: `0.99601`
- TP: `0.99735`
- `C044=N`
- `D1TPW=N`
- Preflight entry: `0.99678`
- Lot: `0.16`
- Broker ticket: `484792192`
- Broker open: `0.99676`
- Broker SL: `0.99601`
- Broker TP: `0.99735`
- Execution identity persistence: PASS
- Local persistence: Y
- Broker hash found: Y
- Broker hash match: Y
- Hash: `CB9A8014BBF8C16E`
- Broker comment: `BBMA|H:CB9A8014BBF8C16E`
- Final decision state: `DEC_EXECUTED`
- Rejection reason: `REJ_NONE`

## Classification

This trade is an attributable ordinary `SIGNAL_RE_ENTRY` execution and is useful as runtime health / P0 execution-identity continuity evidence.

It is **not** an R1 D1 Extreme TP-Wajib targetless lifecycle case because the M17 runtime record explicitly reports `D1TPW=N` and the order has a non-zero TP (`0.99735`).

Therefore this evidence must **not** be promoted to R1-01 PASS and does not by itself satisfy any D1 TP-Wajib completion case R1-04..R1-09.

## Source interpretation lock

Frozen v4.59 source defines `decision.D1TPWLifecycleManaged` only when the decision is a D1 Opportunity `D1_OPP_EXTREME_TPW` identity and the D1TPW lifecycle gate is enabled. Targetless lifecycle decisions set TP to `0.0`; ordinary decisions retain the approved static BB destination. The runtime `D1TPW=N` plus non-zero TP is therefore consistent with an ordinary RE execution, not evidence that the R1 test binary gate itself is necessarily OFF.

## Next evidence needed

Continue natural HFM demo runtime collection without changing the running EA/Observer. The next useful R1 evidence is a decision whose M17 record shows `D1TPW=Y`, `C044=N`, and `TP=0.0`, followed by attributable D1TPW lifecycle logging.
