# M24 Recovery Engine Contract

## Status
P0 Step 15 is **COMPLETED AT RECOVERY / RESTART-IDEMPOTENCY CONTRACT LEVEL**.

M24 is recovery infrastructure only. It does not recreate BBMA strategy decisions, change direction, resize positions, alter SL/TP, or open replacement trades.

## Core rule
Broker comment metadata is not authoritative enough to reconstruct a full original `DecisionID` after restart.

The only restart-stable execution identity guaranteed by M22 is the prefix:

`BBMA|H:<SHORT_HASH(DecisionID)>`

M24 therefore treats `H:` as the canonical recovery/idempotency key. It must never fabricate a full `DecisionID` from lossy comment metadata.

## Why the old rebuild was invalid
The baseline `CreateOrderComment()` stores `Q:` as `SHORT_HASH(sequenceHash)`. The original `DecisionID` was generated from the original `sequenceHash`, not the already-hashed `Q:` value. Rebuilding `DecisionID` from `Q:` can therefore produce a different identity.

Broker/MT4 comment truncation can also remove fields after the stable `H:` prefix. Recovery must remain safe even when the full comment cannot be parsed.

## Exact EA ownership
A recoverable live order must satisfy all of the following:
- market order only (`OP_BUY` or `OP_SELL`);
- exact configured pair symbol;
- exact configured pair magic number;
- live order state;
- valid `BBMA|H:` execution hash prefix.

Magic number alone is insufficient.

## Restart execution tombstones
`SignalHistoryEntry` now carries `ExecutionHash`.

`RebuildExecutionHistory()` scans both:
- current open orders; and
- account order history.

For each exact EA-owned BBMA order, it stores/upserts an executed hash tombstone. `IsDecisionExecuted()` checks both full `DecisionID` and `SHORT_HASH(DecisionID)` against those tombstones.

This prevents a previously executed decision from being recreated after terminal/EA restart, including after the original position has already closed.

## Ambiguous M22 reconciliation
Step 13 M22 already uses `H:` to find an order after an ambiguous send result. Step 15 extends that identity across restart.

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

Invalid geometry/spec state is marked recovery-invalid rather than repaired.

## Truncated comments
If the stable `H:` execution hash is present but later comment metadata is unavailable/truncated:
- the position may be recovered as `REC_IDENTITY_HASH_ONLY`;
- live broker state remains monitored;
- M23 normal broker-side SL/TP behavior remains untouched;
- M20 emergency basket-loss liquidation may still act through M23;
- no fake signal type, sequence, candle time, or full `DecisionID` is manufactured.

## Lot drift
If full metadata is available:
- live lot greater than intended lot -> `REC_CORRUPTED`;
- live lot lower than intended but still valid -> preserve the reduced live lot and mark the legacy/external reduction state;
- M24 never restores the old lot or authorizes another partial close.

Step 14's removal of automatic 1R partial-close and breakeven remains binding.

## Parser repair
The full order-comment parser now retains the final field after the last `|` delimiter. Full parsing is metadata-only and is not used as the primary restart identity.

## Ownership boundaries
M24 may:
- discover exact EA-owned existing orders;
- rebuild execution-hash tombstones;
- reconstruct monitoring state from live broker values;
- classify recovery integrity.

M24 may not:
- generate a new strategy decision;
- regenerate a full `DecisionID` from lossy fields;
- call `OrderSend()`;
- change Entry/SL/TP/lot;
- infer partial-close or breakeven permission;
- bypass M19/M20/M22 controls.

## Implementation record
Patch:
`blueprint/patches/0023-p0-step15-m24-recovery-hash-tombstone.patch`

Patch commit:
`7b75d4807396c666368e62af250b689c74115438`

No new full-chain compile/SHA is claimed until the complete ordered patch chain is materialized and verified.

Do not merge to `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
