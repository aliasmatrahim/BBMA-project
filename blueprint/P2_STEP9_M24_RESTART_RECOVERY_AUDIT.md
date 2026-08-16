# P2 Step 9 — M24 Restart / Recovery Audit

## Result
FAIL — one recovery ownership defect requires repair.

## Scope
Canonical `blueprint-dev` source after P2 Step 8 Fix A/B/C.

## What is correct
- InitializeEA enters non-operational state before ownership/recovery setup and enables `g_is_initialized` only after pair/magic validation, execution-history rebuild and live-order recovery.
- Recovery uses broker live order values for entry, SL, TP and lot and does not manufacture replacement BBMA lifecycle levels.
- Exact EA ownership is checked before recovery.
- Full order-comment metadata is treated as optional/untrusted; when available it must agree with execution hash, pair and live direction.
- Truncated metadata with a surviving H: execution identity degrades to `REC_IDENTITY_HASH_ONLY` rather than fabricating a DecisionID.
- Recovered execution hashes are upserted into execution tombstones, supporting restart idempotency.
- Corrupted / invalid recovered positions remain monitorable and, after P2 Step 8 Fix C, remain eligible for emergency liquidation.

## Defect S9-A — exact EA-owned live order with missing/unparseable H: tag is skipped entirely
`RecoverExistingOrders()` first establishes exact EA ownership through `IsExactEAOwnedSelectedOrder(pairIdx)`. It then calls `ExtractExecutionHash(comment, executionHash)`. If extraction fails, the function logs and `continue`s.

That means a live order which is unquestionably owned by this EA instance via symbol/magic can disappear from `g_monitored_trades` solely because its broker comment is missing, truncated before the H tag, externally modified, or otherwise unparseable.

### Consequences
After restart such an order can be invisible to monitored-registry consumers:
- M19 existing-position total-risk accounting,
- M20 portfolio counts / emergency latch completion,
- M23 lifecycle synchronization and emergency liquidation,
- trade-lock checks based on monitored live trades.

This is a safety/ownership defect. Execution identity uncertainty must not erase known live portfolio ownership.

## Required Fix A
Recover exact EA-owned live orders even when no execution hash can be extracted:
1. Build `TradeInfo` from authoritative broker fields as usual.
2. Mark recovery state as a fail-safe identity-invalid/corrupted state (reuse an existing recovery state if semantically appropriate; do not invent strategy metadata).
3. Add the live order to `g_monitored_trades` so risk, portfolio and emergency management retain ownership.
4. Do **not** fabricate a DecisionID or execution hash and do not create a false execution tombstone when identity is unavailable.
5. Normal strategy lifecycle remains frozen for that position; emergency liquidation must remain possible.

## Status
P2 Step 9: FAIL
Next: P2 Step 9 Fix A — recover exact-owned/hash-missing live orders into monitored fail-safe state.
