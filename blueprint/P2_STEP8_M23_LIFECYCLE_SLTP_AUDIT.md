# P2 Step 8 — M23 Lifecycle / Broker-side SL/TP Preservation Audit

## Result
FAIL — one lifecycle-capacity defect found. Broker-side SL/TP preservation itself is correct.

## Scope
Canonical source on `blueprint-dev` after P2 Step 7 Fix A.

## What passes

### Broker-side SL/TP ownership is preserved
- M23 synchronizes monitored state from the live broker order only.
- It does not manufacture, move, replace, trail, or reinterpret SL/TP.
- Normal exits remain broker-side SL/TP supplied by M17 -> M22.
- No 1R partial close, breakeven migration, trailing stop, TP2/TP3, or synthetic manual TP close is active.

### Emergency close ownership is correctly separated
- M20 owns the emergency basket-loss latch.
- M23 is the broker-close executor when that latch is active.
- A failed emergency close does not clear the M20 request; the request remains latched for later ticks.
- Emergency close uses the full live OrderLots(), so it does not create a partial-close policy.

### Live ownership is revalidated before lifecycle action
- M23 rechecks symbol/pair mapping and expected magic before acting on a monitored order.
- Corrupted/recovery-invalid entries are frozen rather than modified.

## Defect found — monitored-trade array is append-only across the terminal session

### Root cause
`AddToMonitoredTrades()` updates an existing slot only when the same ticket is already present. For a new ticket, it appends while `g_monitored_count < MAX_MONITORED`. Closed broker orders are skipped later by `ManagePositions()` / `IsLiveEAOwnedPortfolioTrade()`, but their slots are never compacted or reused.

There is no M23/M24 routine that removes closed monitored rows or reclaims their slots during the running terminal session.

### Failure mode
After enough cumulative trades (up to `MAX_MONITORED`, currently 400), `g_monitored_count` can reach the hard cap even if most or all older tickets are already closed. A subsequent successful new order can then fail to be inserted into `g_monitored_trades`.

That creates a dangerous split state:
- the broker order exists and was executed;
- the execution tombstone may exist;
- but M23 no longer monitors that live order;
- M19/M20 portfolio/risk loops that depend on `g_monitored_trades` may omit it;
- M20 emergency liquidation via M23 may omit it;
- trade-lock / portfolio counting can become incomplete.

This is a lifecycle/accounting defect, not a BBMA strategy-rule defect.

## Required repair
P2 Step 8 Fix A should add deterministic monitored-trade compaction/reuse:
1. Before appending a new monitored trade, reclaim slots whose tickets are definitively closed/non-live.
2. Preserve every still-live exact EA-owned trade.
3. Never drop an unresolved/live EA-owned ticket merely to satisfy the array cap.
4. Keep `g_monitored_count` equal to the compacted live/retained set.
5. Prefer a single ownership-safe helper used before append and optionally once per M23 lifecycle pass.

The fix must not modify M17 SL/TP semantics or add new exit policy.

## Status
P2 Step 8: FAIL pending Fix A.
P2 Step 1 remains KIV / blocked by MT4 historical-data integrity.
