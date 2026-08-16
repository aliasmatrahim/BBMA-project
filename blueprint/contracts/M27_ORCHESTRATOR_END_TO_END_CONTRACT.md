# M27 Orchestrator / End-to-End Ownership Contract

## Role
M27 is **ORCHESTRATION ONLY**. It controls call ordering and routes already-owned snapshots/payloads between modules. It may not invent BBMA semantics, rank setups, manufacture direction, alter SL/TP, calculate an alternative lot, or perform broker execution logic itself.

## Strategy clock
M15 closed-candle processing remains the sole strategy clock. Signal detection, persistence updates, combination collection/validation, final direction selection, conflict invalidation and BBMA SL/TP resolution must be driven from the frozen closed-candle cycle.

Live account/broker conditions are intentionally evaluated only after the strategy decision has been frozen.

## Canonical entry pipeline
The final entry pipeline is:

1. M06-M12 owner detectors/state engines produce frozen source snapshots.
2. M13 collects snapshots only.
3. M14 validates REM/RRE/REE only.
4. M15 performs one pair-level atomic final-authority pass after BUY and SELL candidates have both been collected.
5. M16 invalidates conflicts only.
6. M17 resolves and validates the source-owned BBMA TP destination and protective structural SL.
7. M21 calculates one deterministic lot from the frozen risk snapshot.
8. M19 evaluates live spread/drawdown/basket/EA-wide prospective risk using that proposed lot.
9. M20 performs the final prospective portfolio/protection gate.
10. M22 executes the immutable approved payload once, with idempotent ambiguous-result handling.

M21 must precede M19 because M19 prospective total-risk calculation requires the proposed lot. Any documentation suggesting M19 precedes M21 is superseded by this dependency-correct ordering.

## One-owner / one-pass rule
For one DecisionID, M27 must invoke each pre-execution owner at most once per execution attempt:
- one M17 SL/TP resolution/validation pass;
- one M21 lot-sizing pass;
- one M19 risk-filter pass;
- one M20 final portfolio/protection pass;
- one M22 execution path.

M22 must not re-run M21, M19 or M20. This removes duplicate authority and prevents two different live reads from producing contradictory acceptance/rejection paths for the same decision.

## Frozen execution payload
After M17 and M21 complete, the execution payload is immutable for M22:
- Pair;
- DecisionID / execution hash identity;
- Direction;
- Entry reference;
- StopLoss;
- TakeProfit;
- frozen lot;
- frozen execution-deviation basis.

M22 may use live Bid/Ask only to obtain the actual send price within the allowed frozen deviation. It cannot resize, re-risk, regenerate identity or repair strategy geometry.

## Protection/lifecycle tick ordering
Every operational tick runs live protection/lifecycle before any new scan:

`M20 ManagePortfolio() -> M23 ManagePositions()`

If `g_portfolio_emergency_close_requested` is latched after this sequence, M27 must not begin a new strategy scan or admit a new order on that tick. Emergency liquidation is an exclusive portfolio state until M20 clears the latch after no live EA-owned monitored positions remain.

This prevents a race where basket loss falls below the original trigger after some emergency closes, but the liquidation latch is still active and a new trade would otherwise be admitted.

## M18 / dashboard boundary
M18 and M25 are observability-only. Score, level, PriorityTier, dashboard rendering or display compatibility inputs may never gate or reorder M27 execution.

## Rejection propagation
M27 preserves the rejection reason emitted by the owning module. It must not collapse:
- M17 SL/TP resolution failures;
- M21 lot failures;
- M19 spread/DD/basket/total-risk failures;
- M20 portfolio-limit/protection failures;
- M22 broker/ambiguous/deviation failures
into a generic rejection when a more specific reason exists.

## Recovery boundary
M24 recovery is initialization/restart ownership and does not recreate strategy decisions during normal scanning. Recovered execution-hash tombstones are consulted by M22 idempotency/decision-history logic; M27 must not fabricate a full DecisionID from recovered lossy comment metadata.

## P0 Step 17 outcome
Step 17 closes the architecture-ownership audit at focused patch/contract level. It does **not** yet prove full-source compilation or full ordered-patch materialization.

Before merge to `main`, the next phase must:
1. materialize the immutable baseline plus patches 0001-0025 in exact order;
2. detect patch conflicts/context drift;
3. compile the complete MT4 source;
4. repair compile/integration defects without changing locked BBMA semantics;
5. calculate and record a new SHA-256 only from the exact successfully materialized full source.
