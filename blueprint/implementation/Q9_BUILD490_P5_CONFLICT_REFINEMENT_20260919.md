# Q9 Build 4.90 P5 Conflict Refinement Materialization — 2026-09-19

Issue: #101  
Build: 4.90 / `V490_Q9_P5_CONFLICT_REFINEMENT_20260919`

## Change

P5 changes only M5 shadow diagnostic relation mapping inside `NMJE_BuildM5Refinement`.

- opposite confirmed M5 Re-Entry: `NESTED_CONFLICT` -> `NESTED_UNRESOLVED`;
- reason: `M5_TEMPORARY_CONFIRMED_RE_OPPOSES_PARENT` -> `M5_OPPOSITE_CONFIRMED_RE_UNRESOLVED`;
- opposite active M5 Extreme: `NESTED_CONFLICT` -> `NESTED_BUILDING`;
- reason: `M5_TEMPORARY_EXTREME_OPPOSES_PARENT` -> `M5_OPPOSITE_EXTREME_BUILDING`.

Build/version identity is advanced to 4.90.

## Non-change boundary

No change to:
- M5 sampling cadence;
- canonical Re-Entry/Extreme helpers;
- candidate creation/eligibility;
- P2 comparator/order;
- M13/M14/M15/M16/M17/M22 strategy authority;
- risk/execution/lifecycle;
- P4 outcome attribution semantics.

This is a fail-closed diagnostic correction, not a Strategy-Core rule addition.
