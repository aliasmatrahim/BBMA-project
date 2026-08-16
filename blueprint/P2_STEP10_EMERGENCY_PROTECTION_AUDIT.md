# P2 Step 10 — Emergency Protection / Liquidation Ownership Audit

## Result
FAIL — one residual lifecycle defect found.

## Scope
Canonical `blueprint-dev` source after P2 Step 9 Fix A.

## Confirmed correct
- M20 owns the emergency basket-loss latch.
- M23 owns actual broker close execution.
- M23 revalidates exact EA ownership before closing.
- Emergency liquidation has precedence over recovery-state freezing.
- While the latch remains active, M27 blocks new strategy scanning/admission.
- BasketProfitPercent is not used as an alternate synthetic TP.

## Defect
`ManagePortfolio()` clears `g_portfolio_emergency_close_requested` when `CountLiveEAOwnedPortfolioTrades() == 0`.

`CountLiveEAOwnedPortfolioTrades()` depends on `IsLiveEAOwnedPortfolioTrade()`, which depends on selecting each monitored ticket. A transient `OrderSelect(ticket, SELECT_BY_TICKET)` failure therefore returns false for that live trade.

If every still-open monitored EA trade is temporarily unselectable on that tick, the count can become zero even though broker-side live positions still exist. M20 can then clear the emergency latch before M23 closes those positions. On the same tick M23 can also skip them because selection failed, after which M27 is no longer blocked and may resume strategy scanning/new admission.

This violates fail-closed emergency protection semantics.

## Required Fix A
Emergency-latch release must be broker-authoritative and fail-closed:
- while latched, scan the broker live trade pool directly for exact EA-owned orders;
- clear the latch only when the broker scan definitively confirms zero exact EA-owned live orders;
- if any order enumeration/selection needed for the confirmation is uncertain, keep the latch set;
- do not alter BBMA strategy, SL/TP, or normal lifecycle semantics.

## Status
P2 Step 10: FAIL pending Fix A.
