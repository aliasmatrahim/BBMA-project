# M24 Recovery Engine Contract

## Status
P0 Step 15 is **COMPLETED AT RECOVERY / RESTART-IDEMPOTENCY CONTRACT LEVEL**.

P3 Step 5B adds an explicit missing-execution-identity safety state without changing BBMA strategy semantics.

M24 is recovery infrastructure only. It does not recreate BBMA strategy decisions, change direction, resize positions, alter SL/TP, or open replacement trades.

## Core rule
Broker comment metadata is not authoritative enough to reconstruct a full original `DecisionID` after restart.

The only restart-stable execution identity intentionally written by M22 is the prefix:

`BBMA|H:<SHORT_HASH(DecisionID)>`

M24 therefore treats `H:` as the canonical recovery/idempotency key whenever it is available. It must never fabricate a full `DecisionID` from lossy comment metadata.

A missing `H:` is not, by itself, proof that the live broker position is corrupt. It means execution identity cannot be reconstructed safely.

## Why the old rebuild was invalid
The baseline `CreateOrderComment()` stores `Q:` as `SHORT_HASH(sequenceHash)`. The original `DecisionID` was generated from the original `sequenceHash`, not the already-hashed `Q:` value. Rebuilding `DecisionID` from `Q:` can therefore produce a different identity.

Broker/MT4 comment truncation can also remove fields after the stable `H:` prefix. Recovery must remain safe even when the full comment cannot be parsed.

## Exact EA ownership versus execution identity
Two concepts are deliberately separate.

### Exact live EA ownership
A live order is considered exact EA-owned for portfolio/lifecycle safety only when all of the following match broker truth:
- market order only (`OP_BUY` or `OP_SELL`);
- exact configured broker symbol;
- exact configured pair magic number;
- live order state.

Magic number alone is insufficient.

### Recoverable execution identity
A stable restart execution identity additionally requires a valid:

`BBMA|H:<SHORT_HASH(DecisionID)>`

If exact live ownership is proven but `H:` is absent, the order must remain visible to M19/M20/M23 safety accounting but must not be assigned a fabricated strategy identity or execution tombstone.

## Restart execution tombstones
`SignalHistoryEntry` carries `ExecutionHash`.

`RebuildExecutionHistory()` scans both:
- current open orders; and
- account order history.

For each exact EA-owned BBMA order that contains a valid `H:` prefix, it stores/upserts an executed hash tombstone. `IsDecisionExecuted()` checks both full `DecisionID` and `SHORT_HASH(DecisionID)` against those tombstones.

This prevents a previously executed decision from being recreated after terminal/EA restart, including after the original position has already closed, when the stable execution identity is still observable.

If `H:` is absent, M24 must not invent a tombstone. The resulting loss of restart idempotency evidence is an explicit degraded state and must remain observable in diagnostics.

## Ambiguous M22 reconciliation
Step 13 M22 uses `H:` to find an order after an ambiguous send result. Step 15 extends that identity across restart.

If an order accepted by the broker becomes visible only later, M24 can recover it from the stable hash without sending another order.

M24 never retries `OrderSend()`.

## Live trade-state preservation
On recovery, broker state is authoritative for the existing position:
- Entry = `OrderOpenPrice()`;
- SL = `OrderStopLoss()`;
- TP = `OrderTakeProfit()`;
- lot = `OrderLots()`.

M24 does not move SL/TP, restore lot size, infer a new target, or reopen a missing portion.

Direction geometry must still be sane:
- BUY: `SL < Entry < TP`;
- SELL: `TP < Entry < SL`.

Invalid geometry/spec state is marked `REC_RECOVERY_INVALID` rather than repaired.

## Recovery-state classification
Recovery classification must distinguish actual broker-state corruption from identity degradation.

### `REC_NORMAL`
Full metadata is available and agrees with live broker ownership/direction/geometry.

### `REC_IDENTITY_HASH_ONLY`
The stable `H:` execution hash is available but later comment metadata is unavailable/truncated.

The position remains monitored. No fake signal type, sequence, candle time, or full `DecisionID` is manufactured.

### `REC_IDENTITY_MISSING_FROZEN`
Exact live EA ownership is proven from broker symbol + magic + order type, live Entry/SL/TP/lot geometry is valid, but no valid `H:` execution hash is observable.

This state is intentionally **not** named `LEGACY`, because an empty/missing comment can come from either:
- a pre-execution-hash order; or
- broker/server comment loss or stripping.

Required behavior:
- preserve exact broker Entry/SL/TP/lot;
- include the position in M19/M20 exposure, basket and portfolio safety accounting;
- keep emergency liquidation precedence available through M23;
- freeze all ordinary strategy/lifecycle actions that would require reconstructed identity;
- do not fabricate `DecisionID`, execution hash, signal type, sequence, candle time or tombstone;
- expose a one-time structured recovery diagnostic with cause `MISSING_EXECUTION_HASH`;
- do not label the position `REC_RECOVERY_INVALID` solely because `H:` is missing.

### `REC_RECOVERY_INVALID`
Reserved for genuinely invalid recoverable broker state, including invalid directional Entry/SL/TP geometry, non-positive live lot, invalid live lot step, or another hard state inconsistency that cannot be safely preserved as a normal position.

### `REC_CORRUPTED`
Used when full metadata proves a hard mismatch such as live lot exceeding the intended recorded lot.

### `REC_PARTIAL_INFERRED`
If full metadata is available and live lot is lower than intended but otherwise valid, preserve the reduced live lot. M24 never restores the old lot or authorizes another partial close.

Step 14's removal of automatic 1R partial-close and breakeven remains binding.

## Missing-identity idempotency limitation
`REC_IDENTITY_MISSING_FROZEN` solves live-position safety classification; it does **not** restore the missing execution identity.

Therefore P3 runtime validation must separately verify that a freshly created post-fix M22 order retains an `OrderComment()` beginning with `BBMA|H:` after broker acceptance. If a fresh order loses that prefix, the issue is broker comment persistence and restart idempotency remains unresolved; M24 must not disguise that failure as a legacy-order case.

## Parser repair
The full order-comment parser retains the final field after the last `|` delimiter. Full parsing is metadata-only and is not used as the primary restart identity.

## Ownership boundaries
M24 may:
- discover exact EA-owned existing orders;
- rebuild execution-hash tombstones when `H:` exists;
- reconstruct monitoring state from live broker values;
- classify recovery integrity and identity degradation.

M24 may not:
- generate a new strategy decision;
- regenerate a full `DecisionID` from lossy fields;
- fabricate an execution hash or tombstone for an order with no `H:`;
- call `OrderSend()`;
- change Entry/SL/TP/lot;
- infer partial-close or breakeven permission;
- bypass M19/M20/M22 controls.

## P3 Step 5B implementation requirements
Canonical source implementation must:
1. add `REC_IDENTITY_MISSING_FROZEN` to `ENUM_RECOVERY_STATE`;
2. classify valid exact-owned/no-`H:` positions into that state rather than `REC_RECOVERY_INVALID`;
3. keep hard geometry/lot failures mapped to `REC_RECOVERY_INVALID`;
4. make M23 freeze `REC_IDENTITY_MISSING_FROZEN` for ordinary lifecycle while keeping emergency-close precedence;
5. keep M19/M20 accounting unchanged for the monitored live position;
6. keep M22's `BBMA|H:` requirement for all new executions unchanged;
7. compile with 0 errors / 0 warnings before runtime acceptance.

## Implementation record
Original P0 patch:
`blueprint/patches/0023-p0-step15-m24-recovery-hash-tombstone.patch`

Original patch commit:
`7b75d4807396c666368e62af250b689c74115438`

P3 Step 5B is a runtime-driven recovery-contract amendment and must be implemented and revalidated before P3 Step 5 can close.

Do not merge to `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
