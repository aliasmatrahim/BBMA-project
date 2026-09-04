# P2 Dashboard Active-Trade Count Static Audit — 2026-09-04

## Mode
ORIGIN MODE: CHAT
VERIFY MODE: CHAT (static/read-only source audit)

## Scope
M25 dashboard active-trade count refresh only. No EA source modification, compile, runtime, Strategy Tester, or MT4 forward-test action.

## Finding
The canonical `d1-owner-dev` source already contains `P2-DASHCOUNT-01`.

`CountDashboardLiveEAOwnedTrades()` enumerates the live broker order pool through `OrdersTotal()` / `OrderSelect(..., MODE_TRADES)` and increments the display count only when `IsExactEAOwnedSelectedOrder(pairIdx)` accepts the selected order. The dashboard therefore does not derive its displayed trade count from `g_monitored_count` or stale lifecycle registry state.

`BuildDashboardSnapshot()` uses that broker-derived count for the `Trades:` display.

`RefreshDashboardLiveTradeCount()` compares the current broker-derived count with the last displayed count, rebuilds the snapshot only when the count changes, updates the display, and clears `g_dashboard_needs_update`.

`OnTimer()` calls `RefreshDashboardLiveTradeCount()` after connection/processing checks, providing periodic presentation refresh so a broker-side close does not need to wait for a new M15 signal-processing event before the displayed count can change.

## Static conclusion
STATUS: IMPLEMENTATION PRESENT / STATIC PATH CONFIRMED / RUNTIME VERIFICATION PENDING

The previously queued symptom "dashboard can display stale active-trade count" is no longer an unimplemented source item in the current `d1-owner-dev` source. Runtime display evidence is still a separate verification boundary and is intentionally not claimed by this audit.

## Safety
- No `.mq4` source changed.
- No strategy, risk, sizing, execution, lifecycle, or broker behavior changed.
- Existing forward/runtime candidate remains untouched.

## Tracking note
`blueprint/MASTER_QUEUE.md` still contains an older `P2 — Dashboard active-trade count refresh / Status: QUEUED` entry. That status is stale relative to the current source and should be reconciled in a later tracking-only edit as `IMPLEMENTATION PRESENT / STATIC PATH CONFIRMED / RUNTIME VERIFICATION PENDING`.
