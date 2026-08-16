# P2 Step 7 — M22 Execution / Idempotency / Retry Audit

## Result
FAIL — one execution-integrity defect found. Repair required before P2 Step 7 can be closed.

## What passes
- M22 is execution-only and consumes frozen M17/M21/M19/M20 outputs.
- Before every send attempt, `FindExistingExecutionTicket()` checks live orders using pair + magic + direction + stable `BBMA|H:<hash>` identity.
- Retryable broker errors are retried only after the duplicate-order reconciliation guard runs again.
- Ambiguous broker errors are not resent automatically; one reconciliation attempt is made and unresolved ambiguity returns `REJ_AMBIGUOUS_RESULT`.
- Execution deviation is checked against the frozen allowed deviation before sending.
- Fatal broker errors fail closed.
- Restart recovery rebuilds execution-hash tombstones from both open and historical EA-owned orders.

## Defect P2-7A — successful execution may not create an in-session tombstone
`ProcessEntry()` calls `MarkDecisionExecuted(decision.DecisionID, ticket)` after a confirmed successful order.

However, `MarkDecisionExecuted()` only updates an already-existing `g_global_signal_history` item whose `DecisionID` matches. If no such row exists, the function exits without inserting anything.

The current M15 -> M22 path does not establish a guaranteed pre-execution global-history row for every decision. Therefore a newly executed decision can have no in-memory execution tombstone.

### Failure scenario
1. A decision executes successfully.
2. `MarkDecisionExecuted()` finds no pre-existing history row and records nothing.
3. While the position remains open, `FindExistingExecutionTicket()` still prevents a duplicate.
4. The position later closes during the same terminal session.
5. `FindExistingExecutionTicket()` no longer sees that ticket because it scans live trades only.
6. `IsDecisionExecuted()` can return false because no execution tombstone was created.
7. If the same still-valid owner snapshot recreates the same DecisionID, M22 may admit the same decision again.

Restarting the EA masks this defect because `RebuildExecutionHistory()` scans broker history and creates execution-hash tombstones. The gap exists specifically between successful execution and a later restart.

## Secondary retention observation
`CleanupSignalHistoryEntries()` preserves executed tombstones, but `CleanupGlobalSignalHistory()` can blindly drop the oldest block when the array exceeds `SIGNAL_HISTORY_MAX`. Execution identity should not be discarded solely because of a generic history-size cap while it may still be needed for idempotency.

## Required repair
1. Change successful execution recording to UPSERT semantics: if the DecisionID / execution hash does not already exist, append an executed tombstone immediately.
2. Preserve execution tombstones from generic history cleanup, or otherwise prove they cannot be required after eviction.
3. Recompile native MetaEditor to 0 errors / 0 warnings after the repair.
4. Re-run the P1 invariant audit relevant to M22/M24 ownership and then re-run this P2 Step 7 audit.

## Status
P2 Step 7: FAIL — P2-7A
P2 Step 1 remains KIV / blocked by MT4 historical-data integrity.
