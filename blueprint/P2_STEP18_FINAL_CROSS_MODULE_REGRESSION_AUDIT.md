# P2 Step 18 — Final Cross-Module Regression Audit

Status: FAIL — Fix A required

Compile baseline entering S18: 0 Errors / 0 Warnings (user-reported after P2 S17 Fix A)

## Scope
Final P2 static regression across initialization/input contract, broker symbol identity, signal-to-decision lifecycle, invalidation, SL/TP, risk, portfolio protection, execution, recovery and orchestration.

## Finding — TradeLockMode is not enforced at execution boundary
`IsSignalAllowed()` contains the intended TradeLockMode contract for `LOCK_ONE_POSITION` and `LOCK_SAME_DIRECTION`, but the current `ProcessEntry()` path never calls it before `OrderSend()`.

Therefore `TradeLockMode` can be configured yet have no effect on live entry admission. The final execution path currently checks duplicate DecisionID, pair/magic ownership, monitored-registry capacity, execution deviation and broker execution, but not the trade-lock policy.

This is a cross-module regression because the input contract is declared in M01, the lock predicate exists in M22, while M27 routes validated decisions through M17 -> M21 -> M19 -> M20 -> M22 without enforcing that predicate.

A related input-contract gap also exists: `ValidateInputParameters()` validates EntryMode and MMMode but does not reject TradeLockMode values outside 0..2. Invalid values therefore silently behave as lock-off.

## Required Fix A
1. Validate `TradeLockMode` is one of `LOCK_OFF`, `LOCK_SAME_DIRECTION`, `LOCK_ONE_POSITION` during input validation.
2. Enforce `IsSignalAllowed(decision, pair, magic)` in `ProcessEntry()` after pair/magic resolution and before monitored-capacity/broker-send work.
3. Reject with `REJ_TRADE_LOCK` when the lock predicate fails; existing dedicated duplicate checks remain authoritative for duplicate execution identity.
4. Preserve M22 as execution-only. No BBMA signal, EntryMode, SL/TP, risk or portfolio formulas are changed.

P2 cannot be closed until Fix A compiles 0E/0W and passes Step 18 re-audit.