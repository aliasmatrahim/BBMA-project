# P2 Step 11 — Timer / Orchestration Consistency Audit

## Result
FAIL — static orchestration defect found.

## Scope
Canonical `blueprint/source/BBMA_PROFESSIONAL_EA.mq4` on `blueprint-dev`, focusing on `OnTick()`, `OnTickMain()`, `OnTimer()`, emergency protection ordering, scanning ownership, and candle-processing side effects.

## Defect
`OnTickMain()` uses the correct orchestration order:
1. `ManagePortfolio()`
2. `ManagePositions()`
3. emergency latch gate
4. `g_is_scanning` ownership gate
5. strategy scan / `ProcessPair()`

`OnTimer()` duplicates strategy orchestration independently and does not follow that contract. It currently:
- does not call `ManagePortfolio()` before lifecycle/strategy work;
- does not gate on `g_portfolio_emergency_close_requested` before scanning;
- does not use `g_is_scanning` as the shared scan owner;
- does not check terminal connectivity before broker/lifecycle/strategy calls;
- can still call `ProcessPair()` while emergency liquidation is latched. `RunEntryPreflightAndExecute()` prevents a new order, but `ProcessPair()` can still mutate persistent signal/re-entry/extreme state and advance `g_processed_candle_time` during the emergency window.

## Why this matters
The timer path can therefore consume/mark a closed M15 candle while the portfolio is in exclusive liquidation state. When the emergency latch later clears, that candle has already been processed and the setup may no longer be evaluated under normal admission conditions. It also means basket-loss protection is not newly latched from the timer path if no tick has yet invoked `ManagePortfolio()`.

This is an orchestration ownership defect, not a BBMA strategy-logic defect.

## Required Fix A
Use one shared orchestration authority for both event sources. Preserve timer-only maintenance (history cleanup and daily reset), but after maintenance and a connectivity check, route strategy/lifecycle work through `OnTickMain()` rather than duplicating `ManagePositions()` + scan logic in `OnTimer()`.

Expected properties after fix:
- M20 always runs before M23 and before any scan.
- emergency latch blocks both tick-driven and timer-driven scans identically.
- `g_is_scanning` has one owner path.
- timer cannot consume `g_processed_candle_time` during emergency liquidation.
- disconnected terminal causes timer broker/strategy work to fail closed.
- no BBMA Entry/SL/TP/MM semantics change.

## Status
P2 Step 11: FAIL (STATIC)
Next: P2 Step 11 Fix A — unify OnTimer with `OnTickMain()` orchestration.
