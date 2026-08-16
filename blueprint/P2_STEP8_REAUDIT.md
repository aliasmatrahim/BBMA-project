# P2 Step 8 — Re-Audit After Fix A

## Result
FAIL — Fix A closes cumulative closed-ticket exhaustion, but one residual admission/lifecycle defect remains.

## What Fix A successfully closes
- `CompactMonitoredTrades()` removes only broker-confirmed closed tickets.
- Failed `OrderSelect()` records are preserved fail-closed rather than being guessed closed.
- `AddToMonitoredTrades()` updates duplicate tickets, compacts stale closed tickets, and reuses capacity.
- M23 remains broker-state synchronization + emergency full-close only; it does not alter the M17/M22 broker-side SL/TP, does not trail, breakeven, partial-close, or synthesize TP.

## Residual defect
`ProcessEntry()` sends the broker order first. Only after a ticket is confirmed and selected does it call `AddToMonitoredTrades(info)`.

`AddToMonitoredTrades()` returns `void`. If compaction still leaves `g_monitored_count >= MAX_MONITORED` (for example, the registry contains many records that cannot currently be `OrderSelect`ed and are intentionally preserved fail-closed), it only logs `Monitored registry full` and returns.

`ProcessEntry()` nevertheless immediately marks the decision `DEC_EXECUTED`, creates the execution tombstone, and returns success. Therefore a newly opened broker order can theoretically exist without being present in `g_monitored_trades`.

Consequences of an unregistered live owned trade:
- M19 total-risk calculation can miss it.
- M20 portfolio counting / basket-loss protection can miss it.
- M23 emergency liquidation cannot manage it because M23 iterates `g_monitored_trades`.
- TradeLock checks can miss it.

The normal `MaxTotalTrade <= MAX_MONITORED` contract prevents this when the registry cleanly represents current live trades. The gap exists specifically when fail-closed unselectable records occupy capacity while portfolio admission sees fewer live selectable trades.

## Required Fix B
Add a fail-closed monitored-registry capacity gate BEFORE `OrderSend` / `SendOrderWithRetry`.

Preferred contract:
1. Compact broker-confirmed closed records before execution admission.
2. If no monitored slot is safely available, reject the decision before sending any broker order.
3. Do not evict an unselectable/possibly-live record just to make space.
4. Keep `AddToMonitoredTrades()` as the post-send registration step, but its capacity failure should be unreachable under the pre-send gate.

No BBMA signal/SL/TP semantics need to change.

## Status
P2 Step 8: FAIL pending Fix B.
