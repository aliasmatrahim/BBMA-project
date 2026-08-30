# BBMA Core End-to-End Journey Contract — C2-A

Status: **LOCKED STATIC/MODEL BASELINE — NO EA SOURCE CHANGE**

Source baseline: `BBMA_EA.mq4` build/header 4.72, normalized-text SHA-256
`1c40c6d692a66652f5cdff25d7f81a6ca7fed2d340f8beee24ea797d30fd4e49`.

## Canonical runtime chain

One closed-M15 processing cycle owns the active strategy path. The source order
is fixed as follows:

1. `ProcessPair` acquires closed D1, H4, H1 and M15 state. M5 is sampled on the
   same M15 clock for NMJE research only.
2. M15 `PriorityEngine_Atomic` selects at most one canonical candidate, freezes
   its component identities and D1 authority snapshot, creates `DecisionID`, and
   publishes `DEC_CREATED`.
3. M16 `InvalidationEngine_Atomic` consumes only a valid `DEC_CREATED` decision,
   revalidates the frozen D1 authority and exact component owners, and publishes
   `DEC_VALIDATED`. NMJE comparison is descriptive and cannot reject.
4. M17 builds one broker/account snapshot, resolves the live execution side,
   resolves only the approved semantic source-owned SL/TP, and validates geometry.
5. M21 calculates one lot from that same frozen snapshot. M19 then checks trade
   risk and M20 applies the final portfolio guard.
6. M22 `ProcessEntry` rejects identity, duplicate, capacity, or deviation
   failures before calling `SendOrderWithRetry`. `SendOrderWithRetry` is the sole
   `OrderSend` owner.
7. A confirmed broker ticket is bound to pair, direction, magic, open time,
   `DecisionID`, sequence hash, and `SHORT_HASH(DecisionID)`. The trade is added
   to the monitored registry only after broker selection and identity persistence
   have been attempted; failed durable identity freezes recovery authority.
8. M23 owns live closes: portfolio emergency close has precedence, followed by
   separately gated D1TPW and C044 lifecycle close owners.
9. M24 reconstructs only exact EA-owned broker orders. It verifies local/broker
   execution identity, parses metadata when available, validates geometry and lot,
   restores an unambiguous checkpoint, and fails closed when identity is missing,
   corrupt, or ambiguous.

The exact preflight order is therefore:

`M17 geometry -> M21 sizing -> M19 risk -> M20 portfolio -> M22 execution`.

## Immutable identity handoff

The protected lineage is:

`candidate components + D1 authority -> DecisionID -> execution hash -> ticket + magic + pair + direction + open time -> monitored/recovered TradeInfo`.

The following rules are mandatory:

- M16 must not reconstruct or replace M15 identity.
- M17–M22 must consume the same `BBMA_Decision` and frozen
  `RiskValidationSnapshot`; no later strategy lookup may substitute a source.
- `execution_hash` must originate from `SHORT_HASH(DecisionID)` or from an exact
  durable/broker recovery match.
- A targetless order requires exactly one valid lifecycle checkpoint. Missing or
  ambiguous checkpoint identity freezes the trade.
- A normal TP order may recover with full metadata or hash-only identity, but
  missing identity is frozen and invalid geometry is rejected from management.

## Single-writer ownership

- `DEC_CREATED`: M15 `PriorityEngine_Atomic` only.
- `DEC_VALIDATED`: M16 `InvalidationEngine_Atomic` only.
- `DEC_EXECUTED`: M22 `ProcessEntry` only.
- broker open: M22 `SendOrderWithRetry` only; exactly one `OrderSend` callsite.
- broker close: M23 emergency, D1TPW, and C044 close owners only.
- monitored registry insertion/update: `AddToMonitoredTrades`; compaction:
  `CompactMonitoredTrades`; initialization reset: `InitializeEA`.
- restart reconstruction: M24 `RecoverExistingOrders` only.

## Dormant and excluded authority

- `EnableD1TPWLifecycle=false`.
- `EnableC044Lifecycle=false`.
- NMJE/M5 remains research/shadow metadata and has no selection, rejection,
  sizing, execution, or close authority.
- W1 and M30 remain absent. Primary M1 remains excluded.
- No daily-loss gate is introduced. Same-currency exposure and loss/broker-error
  cooldown remain KIV only and outside the executable queue.

## Evidence boundary

C2-A proves source topology, state order, identity continuity, single-writer
ownership, fail-closed recovery, and a deterministic journey model. It does not
prove broker runtime behavior, historical profitability, or activation safety;
those require C3/C4 native MT4 evidence.
