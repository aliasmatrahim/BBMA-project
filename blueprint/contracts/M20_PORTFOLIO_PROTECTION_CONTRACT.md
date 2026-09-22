# M20 Portfolio Risk & Protection Contract

Status: P0 Step 11 LOCKED at portfolio-gate / protection-ownership level.

## Responsibility
M20 is portfolio-control infrastructure. It may:
- count current live EA-owned positions;
- reject a new already-validated M15-M17 decision when the prospective portfolio would breach `MaxActivePair`, `MaxTradePerPair`, or `MaxTotalTrade`;
- raise a latched emergency portfolio-close request when `BasketLossPercent` protection is breached.

M20 may NOT:
- create or change BBMA direction, signal type, Entry, SL or TP;
- use M18 score/level/SignalMode to gate trades;
- call `OrderClose()` directly;
- create an alternate profit target that competes with the M17-approved BBMA TP.

## Prospective atomic entry gate
Portfolio admission must evaluate the portfolio as it would exist AFTER the proposed trade:
- `wouldBeTotal = current EA-owned trades + 1`;
- `wouldBePairTrades = current EA-owned trades for decision.Pair + 1`;
- `wouldBePairs = current active pairs + 1 only when decision.Pair is not currently active`.

The decision is rejected with `REJ_PORTFOLIO_LIMIT_ATOMIC` when any prospective hard limit would be exceeded.

If the current live portfolio is already above a hard portfolio limit, no additional trade may be admitted.

## EA ownership
Portfolio counts and protection actions are limited to live orders represented by the EA monitored registry whose live order magic matches the configured magic for that pair. Closed, missing, mismatched or foreign orders are excluded from M20 counts/actions.

A failed `OrderSelect(ticket)` on a monitored row is **UNKNOWN**, not an ordinary exclusion result. UNKNOWN ownership fails closed for prospective new-entry admission and must not be counted as zero current exposure.

UNKNOWN basket/ownership observation alone does not prove that `BasketLossPercent` has been breached and therefore must not fabricate an emergency-liquidation request. M20 defers that threshold evaluation for the tick and keeps any already-latched emergency request subject to the existing fail-closed broker-confirmed release rule.

## Basket-loss protection
`BasketLossPercent` is EA-safety protection, not a BBMA strategy signal.

When the basket-loss threshold is reached:
1. M20 sets `g_portfolio_emergency_close_requested = true`;
2. the request remains latched until no live EA-owned monitored positions remain;
3. M23 owns the broker close action and retries on later ticks when a close does not complete.

This separation prevents M20 from competing with M23 execution/lifecycle ownership.

## Basket-profit behavior
`BasketProfitPercent` is retained only for compatibility/display metadata in the current blueprint. It MUST NOT automatically close trades.

Reason: M17 owns the approved BBMA TP destination. A portfolio basket-profit close would be an alternate TP policy and would violate the locked BBMA TP provenance/ownership contract.

## Clock boundary
M20 may use live order/account state because portfolio limits and protection are execution-time risk controls. This does not change the closed-candle strategy clock owned by M15.

## Downstream boundary
M23 remains the position-action owner. Step 11 only routes the emergency protection request into M23; detailed M23 partial-close, breakeven, TP-close, retry and lifecycle behavior remains subject to its dedicated downstream P0 audit.

## D1-05 runtime input-capacity overlay
`MaxActivePair` remains an M20 hard portfolio-admission limit, but M26 now supplies a sanitized runtime-effective value. The supported pair-state capacity is 40. A requested value below 1 or above 40 is capped to the nearest supported bound with an unconditional Experts/Journal warning; this recoverable input condition must not detach the EA. M20 applies the effective value to both current-portfolio and prospective atomic admission checks. No BBMA signal, direction, SL/TP, or lifecycle semantics change.
