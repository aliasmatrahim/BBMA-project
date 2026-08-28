# NMJE v2 / M5 Stage-E1 P5 Conflict Record — 2026-08-28

## Scope

Refine conflict diagnostics without changing the canonical NMJE relation or any
BBMA decision. P5 attaches one deterministic subtype to the base journey and M5
shadow context, carries it through P4 attribution, and emits it with outcomes.

## Diagnostic families

- `TEMPORARY_RETRACEMENT`: opposite candidate Re-Entry still building.
- `LOCAL_CHILD_OPPOSITION`: confirmed H1/M5 Re-Entry or M5 Extreme opposes parent.
- `PARENT_DIRECTION`: local H4 parent direction opposes D1 strategic direction.
- `OWNER_TRANSITION`: D1 canonical owner is transitioning.
- `STRUCTURAL`: fallback for a canonical conflict not covered by a narrower case.
- `UNRESOLVED_PROVENANCE`: missing, ambiguous, unavailable, invalid, or unresolved identity.

The top-level `BUILDING`, `SUPPORTING`, `ALIGNED`, `CONFLICT`, or `UNRESOLVED`
relation is not rewritten by this classification.

## Attribution and durability

- Base and M5 subtypes freeze with the already-selected shadow snapshot.
- P4 stores both subtype enums under the execution/ticket attribution record.
- Restart loading validates enum domains and requires a non-`NONE` subtype for
  any stored top-level `CONFLICT`.
- Closed-outcome telemetry emits `SUB` and `M5SUB` alongside stable hashes.

## Authority boundary

- No subtype is read by candidate construction, canonical comparison, M16
  outcomes, risk, lot sizing, OrderSend, position management, D1TPW, or C044.
- No score, gate, rejection reason, delay, or all-timeframe alignment is added.
- NMJE execution authority, D1TPW, and C044 remain disabled.

## Build and evidence target

- Header: `Version 4.6.5 - NMJE v2 Conflict Subtype Telemetry`
- Property: `4.65`
- Required: full N3 and M5 Stage A-E1 regression/static suite, Python compile,
  and native MT4 MetaEditor `0 errors, 0 warnings`.
- PR remains draft; no activation or merge authorization.

