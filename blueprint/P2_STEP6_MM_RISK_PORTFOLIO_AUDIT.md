# P2 Step 6 — Money Management + Risk + Portfolio Gate Audit

## Result
PASS — static functional audit. No new repair required.

## Scope
Canonical P1 release-candidate source on `blueprint-dev`.

## Findings

### M21 Money Management
- M21 is sizing-only and consumes the already validated M17 EntryPrice/StopLoss.
- It rejects mismatched frozen risk snapshots instead of mixing later broker/account state.
- AutoLot uses frozen equity and monetary risk per lot derived from SL distance, TickValue and TickSize_Price.
- AutoLot normalization rounds DOWN to broker LotStep; it never rounds risk upward.
- AutoLot rejects results below MinLot or above broker MaxLot / user MaxAutoLot rather than silently clamping.
- FixedLot is treated as explicit user intent and must already satisfy broker min/max/step; invalid values fail closed.
- Unknown MMMode fails closed.

### M19 Risk Gate
- Spread is converted from frozen spread-price to pips through the project pip helper before MaxSpreadPips comparison.
- Drawdown is measured against the EA protection reference equity.
- Basket-loss gate rejects new admission when the configured threshold is reached.
- MaxTotalRiskPercent is EA-wide: existing monitored open positions plus the prospective new position are included.
- Existing risk is calculated using each position's own symbol specification; inability to calculate safely rejects admission.
- Frozen snapshot equity is used for prospective total-risk percentage validation.

### M20 Portfolio Gate
- Portfolio counts are limited to live EA-owned monitored trades whose magic matches the configured pair ownership.
- FinalPortfolioGuard is prospective/atomic: it checks the would-be state after admitting one additional trade.
- MaxActivePair, MaxTotalTrade and MaxTradePerPair therefore cannot be exceeded by the candidate being admitted.
- M20 only rejects; it does not mutate M15–M17 strategy payload.
- Basket-loss emergency state is latched until EA-owned monitored positions have actually been closed by the lifecycle owner.
- BasketProfitPercent is deliberately not used as an alternate TP trigger because M17 owns the BBMA TP destination.

## Architecture conclusion
The chain remains:
M17 validated Entry/SL/TP -> frozen snapshot -> M21 lot sizing -> M19 prospective monetary-risk filters -> M20 prospective portfolio-cap filters -> M22 execution.

No fixed-pip SL/TP, quality-score gating, or alternate strategy semantics were introduced by these modules.

## Runtime limitation
This is a static audit. Exact broker TickValue/TickSize, spread, lot-step, equity, monitored-position recovery, and emergency-close behavior still require runtime/Strategy Tester or controlled demo verification when clean MT4 historical data is available.

## Status
P2 Step 6: PASS (STATIC)
P2 Step 1 remains KIV / blocked by MT4 historical-data integrity.
