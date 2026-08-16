# P2 Step 7 — Execution / Idempotency Re-Audit

## Result
PASS — static re-audit after Fix A.

## Compile evidence
User-reported native MetaEditor compile after Fix A: 0 errors, 0 warnings.

## Defect closure
The original defect was that a successful execution could fail to leave an in-memory execution tombstone when no ordinary history row already existed. This could allow the same DecisionID to become eligible again later in the same terminal session after the original trade had closed.

Fix A closes that path:
- `MarkDecisionExecuted()` now UPSERTs by full DecisionID or execution hash.
- If no matching row exists, it creates a new executed tombstone immediately.
- The tombstone records DecisionID, ExecutionHash, ticket, Executed=true and CreatedTime.
- `IsDecisionExecuted()` checks both the full DecisionID and execution hash.

## Retention re-audit
`CleanupGlobalSignalHistory()` no longer removes executed tombstones through the generic size cap. It removes only non-executed rows. If executed tombstones alone exceed `SIGNAL_HISTORY_MAX`, correctness takes precedence and they are retained.

`CleanupSignalHistoryEntries()` also preserves executed rows with a valid ticket.

## M22 duplicate-prevention chain
The execution path now has three complementary protections:
1. `IsDecisionExecuted()` blocks a previously executed DecisionID / execution hash before a new send.
2. `FindExistingExecutionTicket()` blocks/reconciles a matching currently-open broker order by pair + magic + direction + execution hash.
3. `SendOrderWithRetry()` rechecks for an existing matching order before every possible resend and does not blindly resend an ambiguous broker result.

After a confirmed ticket is selectable, `ProcessEntry()` records the trade and calls `MarkDecisionExecuted()` before returning success.

## Restart behavior
`RebuildExecutionHistory()` scans both open and historical EA-owned orders and recreates execution-hash tombstones from the leading `BBMA|H:` order-comment identity. This complements the same-session UPSERT fix.

## Architecture conclusion
Fix A changes only execution-state persistence / duplicate prevention. It does not alter M15 selection, M16 invalidation, M17 SL/TP, M21 sizing, M19 risk policy, M20 portfolio policy, direction, EntryMode semantics, or BBMA signal definitions.

## Residual runtime limitation
This result is a static re-audit plus native compile confirmation. Broker-specific ambiguous-result timing and restart/history reconstruction still require controlled runtime verification when MT4 test data/environment is available.

## Status
P2 Step 7: PASS (STATIC + COMPILE VERIFIED)
Original Step 7 idempotency defect: CLOSED
P2 Step 1 remains KIV / blocked by MT4 historical-data integrity.
