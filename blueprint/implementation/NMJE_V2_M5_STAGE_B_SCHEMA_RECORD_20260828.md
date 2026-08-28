# NMJE v2 / M5 Stage-B Schema Record — 2026-08-28

## Scope

Issue #101 P1 provenance schema only. This stage adds no M5 data acquisition,
processing-loop call, signal formula, candidate influence, rejection, ranking,
execution, lifecycle, or activation.

## Materialized schema

- `NMJEM5RefinementState` stores EventID, ParentEventID, JourneyID, direction,
  context code, event-start candle, latest closed M5 candle, canonical relation,
  validity/resolution, and reason.
- `NMJE_M5ContextEventID` defines a deterministic `M5CTX` identity domain from
  explicit immutable inputs only.
- `NMJE_M5LineageSnapshotValid` fails closed for incomplete present snapshots.
- `NestedJourneyState.M5Refinement` reserves shadow provenance storage.

## No-wiring boundary

`UpdateNestedJourneyObservation` does not call either M5 helper, load PERIOD_M5,
or populate `M5Refinement`. M15 remains the sole processing clock and final
decision authority. M22 remains OrderSend owner.

## Build identity

- Header: `Version 4.6.1 - NMJE v2 M5 Lineage Schema`
- Property: `4.61`

