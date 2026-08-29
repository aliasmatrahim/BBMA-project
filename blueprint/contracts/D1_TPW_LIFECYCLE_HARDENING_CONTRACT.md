# D1 TP-Wajib Lifecycle Hardening Contract

Status: audit/hardening only; no runtime activation.

## Frozen authority

- `EnableD1TPWLifecycle` remains `false`.
- `EnableC044Lifecycle` remains `false`.
- M15 remains the sole processing clock.
- The D1 Extreme remains the TP semantic owner.
- M23 may only latch and execute the full close after durable identity recovery.
- M22 remains the sole `OrderSend` owner.
- W1, M30, and primary M1 remain intentional exclusions, not backlog; this
  workstream cannot add them without new explicit user strategy-scope approval.
- No entry, SL/TP geometry, lot, risk, candidate, ranking, or execution rule may change.

## Checkpoint v2 contract

A recoverable D1TPW checkpoint must contain:

- a version-2 commit marker written only after every payload field succeeds;
- exact strategy, instance, ticket, pair, direction, magic, and open-time binding;
- the 16-hex D1 opportunity `CycleID`;
- the 16-hex durable execution identity;
- exact D1 Extreme source candle and last-processed closed-D1 cursor;
- mutually consistent latched, exit-candle, and frozen state.

Missing, torn, stale, ambiguous, cross-pair, cross-execution, invalid-history, or
impossible state must fail closed. No recovery heuristic may infer or select a
newest/earliest D1 owner.

## Activation boundary

Passing static, model, regression, and native compilation evidence does not
authorize demo or live activation, merge, release, D1TPW trade-geometry change,
or C044 work. Activation requires a separate manual decision and broker/demo
restart plus close-idempotency evidence.

