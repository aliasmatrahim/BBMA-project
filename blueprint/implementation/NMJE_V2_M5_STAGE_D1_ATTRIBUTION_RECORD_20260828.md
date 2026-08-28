# NMJE v2 / M5 Stage-D1 Attribution Record — 2026-08-28

## Scope

Implement Issue #101 P4's first durable research slice without changing the
live/base BBMA decision. Freeze the existing 4-TF journey and Stage-C2 M5
context after M15 selects a decision, bind it to stable execution identity,
restore it after restart, and emit it with the exact closed-order outcome.

## Attribution payload

- base journey hash, parent-event hash, and canonical relation;
- M5 event hash, relation, direction, context family, start/closed candle times,
  and deterministic reason-subtype hash;
- existing decision/execution hash, ticket, magic, and open time as join keys;
- realized net result from the exact selected closed order.

## Durability and fail-closed attribution

- MT4 terminal GlobalVariables store fixed numeric fields and four-part hex
  identity hashes under a ticket-scoped `BBXA` domain.
- Version is written last and the completed record is read back for verification.
- Restart recovery requires ticket, magic, open time, and execution-hash match.
- Missing, partial, stale, or mismatched metadata is treated as attribution
  unavailable; it never changes the canonical trade recovery state.

## Authority boundary

- Attribution is captured only after M15 has selected the base decision.
- It does not enter candidate construction, canonical comparison, M16 outcomes,
  risk, lot sizing, OrderSend, trade lifecycle, D1TPW, or C044.
- Persistence failure only emits a diagnostic; it cannot reject, freeze, close,
  delay, resize, rerank, or otherwise change a trade.
- NMJE execution authority, D1TPW, and C044 remain disabled.

## Build and evidence target

- Header: `Version 4.6.4 - NMJE v2 Shadow Outcome Attribution`
- Property: `4.64`
- Required: N3 epoch/authority/identity/recovery/replay/static regressions,
  M5 Stage A/B/C1/C2/D1 tests, Python compile, and native MT4 0E0W.
- PR remains draft; no activation or merge authorization.

