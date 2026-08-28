# NMJE v2 / M5 Stage-E4 P8 Stability Record — 2026-08-29

## Scope

Stabilize observation-parent provenance without delaying or suppressing any
M15 decision. P8 retains the prior parent only while that exact canonical event
and the same D1 epoch remain current.

## Retention rules

- The previous journey must be valid/resolved and carry ParentEventID/JourneyID.
- Current D1 canonical EventID must equal the previous D1 node identity.
- H4/D1 Re-Entry parents require the same currently confirmed Re-Entry EventID.
- H4/D1 owner parents require the same current canonical owner EventID.
- If any identity check fails, normal deterministic parent resolution runs.
- Selection telemetry distinguishes retained, selected, transitioned, and no
  replacement after invalidation.

There is no candle counter, wall-clock timer, wait period, cooldown, or delayed
entry. A new higher-priority observation candidate cannot displace an exact
still-canonical parent merely because it appeared on a later M15 cycle.

## Attribution and durability

- `ParentRetained` and a deterministic parent-selection-reason hash freeze with
  the selected decision's shadow snapshot.
- P4 persists both under execution identity and emits `PR`/`PAH` at outcome.
- Parent-transition identity remains attributable across restart/recovery.

## Authority boundary

- Retention exists only inside `UpdateNestedJourneyObservation`.
- It is absent from candidate construction, PriorityEngine selection,
  eligibility, M16 outcomes, risk, OrderSend, lifecycle, D1TPW, and C044.
- NMJE execution authority, D1TPW, and C044 remain disabled.

## Build and evidence target

- Header: `Version 4.6.8 - NMJE v2 Parent Provenance Stability`
- Property: `4.68`
- Required: full N3 and M5 Stage A-E4 regression/static suite, Python compile,
  and native MT4 MetaEditor `0 errors, 0 warnings`.
- PR remains draft; no activation or merge authorization.

