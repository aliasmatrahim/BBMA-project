# NMJE v2 / M5 Stage-E3 P7 Density Record — 2026-08-29

## Scope

Record structural presence for an already-selected BBMA decision without
introducing a score, threshold, filter, or alternate selection strategy.

## Metadata

- five-bit support mask: D1=1, H4=2, H1=4, M15=8, M5=16;
- bit count from 0 to 5;
- existing `RequirementCompleteness` from the selected canonical candidate;
- existing `SequenceCompleteness` from the selected canonical candidate.

A timeframe bit is set only when its canonical node is valid, has deterministic
event identity, and matches the selected direction. M5 additionally requires a
valid resolved `SUPPORTING` or `ALIGNED` shadow relation. Opposition is retained
in P5 conflict telemetry and is not counted as support.

## Freeze, durability, and outcome join

- Completeness values are copied only after PriorityEngine has selected the
  canonical candidate.
- The structure mask/count is frozen by the shadow snapshot and recomputed only
  for diagnostic equality validation.
- P4 persists mask/count/completeness under the stable execution identity and
  validates mask domain and exact bit count during restart recovery.
- Closed outcomes emit `SM`, `SC`, `RQ`, and `SQ`.

## Authority boundary

- P7 metadata does not enter candidate construction, comparison, eligibility,
  M16 outcomes, risk, lot sizing, OrderSend, lifecycle, D1TPW, or C044.
- The sole valid candidate cannot be rejected for low density/completeness.
- NMJE execution authority, D1TPW, and C044 remain disabled.

## Build and evidence target

- Header: `Version 4.6.7 - NMJE v2 Structural Density Telemetry`
- Property: `4.67`
- Required: full N3 and M5 Stage A-E3 regression/static suite, Python compile,
  and native MT4 MetaEditor `0 errors, 0 warnings`.
- PR remains draft; no activation or merge authorization.

