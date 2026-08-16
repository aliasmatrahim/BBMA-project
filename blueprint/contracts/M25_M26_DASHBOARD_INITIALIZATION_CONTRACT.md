# M25 / M26 Dashboard + Initialization Contract

## Status
P0 Step 16 is completed at dashboard-display and initialization/cleanup ownership level.

## M25 — dashboard-only boundary
M25 is strictly presentation/observability. It may read already-owned runtime state and render it. It may not:
- score, rank, promote or demote a setup;
- alter M15 decision selection;
- alter Entry/SL/TP/lot;
- mutate M19/M20 risk or protection state;
- mutate M23/M24 lifecycle/recovery state;
- create broker actions.

`PriorityTier` is not displayed as a trade-quality signal because the current architecture has removed numeric/ranking authority from M18 and does not permit the dashboard to imply an unsupported quality hierarchy.

The current dashboard may display signal type, direction, decision state, rejection reason, account balance/equity, monitored-trade count and protection reference as observability only.

## M26 — initialization ordering
Initialization must remain fail-closed until all ownership/recovery prerequisites are complete.

Required sequence:
1. `g_is_initialized = false` and orchestration flags reset;
2. broker info initialization;
3. pair loading and exact symbol/magic construction;
4. PairID and magic-collision validation;
5. clear transient in-memory history/monitored arrays;
6. set protection reference from current `AccountEquity()` and reject invalid equity;
7. set processing time and transient protection state explicitly;
8. rebuild M24 execution-hash tombstones;
9. recover live EA-owned orders;
10. only then set `g_is_initialized = true`.

Recovery must never run before configured pair/symbol/magic ownership is known and collision-checked.

## Protection reference
M19 defines drawdown against `g_protection_reference_equity` using live equity. Therefore initialization and daily reset must establish the reference from `AccountEquity()`, not `AccountBalance()`.

This avoids a restart artefact where existing floating P/L is incorrectly interpreted as immediate drawdown relative to balance.

If a valid positive equity reference cannot be obtained during initialization, initialization fails closed.

## M20 emergency latch on restart
`g_portfolio_emergency_close_requested` is transient process state, not strategy identity. It is initialized false. Recovered positions are then evaluated by the live M20 protection engine, which may latch emergency close again from current broker state.

M26 must not infer or restore an emergency-close latch from stale process memory.

## Recovery identity preservation
M26 may clear transient in-memory arrays before recovery because M24 reconstructs execution tombstones from broker open/history records. It must not clear/rewrite M24 state after `RebuildExecutionHistory()` / `RecoverExistingOrders()` complete.

No full DecisionID may be fabricated during initialization.

## Deinitialization
Deinitialization must:
- set `g_is_initialized = false` first;
- stop local scan/manage flags;
- stop pending dashboard refresh;
- clear only the local chart comment when dashboard display is enabled.

It must not close/modify broker orders, rewrite SL/TP, erase broker history, or attempt to persist fabricated strategy identity.

## Deprecated concepts
The following are not active M25/M26 authorities:
- signal quality score/tier as a trading gate;
- 1R partial-close lifecycle;
- automatic breakeven lifecycle;
- basket-profit synthetic TP execution.

## Implementation record
Patch:
`blueprint/patches/0024-p0-step16-m25-m26-dashboard-init-cleanup.patch`

Patch commit:
`cb148e3dc9b074d1ad0811ba6b9b4e237a2b1a42`

A full-chain compile/SHA is not claimed until the complete ordered patch chain is exactly materialized and verified.
