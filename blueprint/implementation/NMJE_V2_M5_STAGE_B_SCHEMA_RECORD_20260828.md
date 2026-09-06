# NMJE v2 / M5 Stage-B Schema Record — 2026-09-07

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

- Header: `Version 4.6.4 - NMJE v2 M5 Lineage Schema`
- Property: `4.64`


Rematerialized from historical intent onto the v4.63/F7-reconciled replacement baseline; no historical source blob was reused.

## 2026-09-07 replacement validation

- Source SHA-256: `bd62e019dd1a5e6926788fa1feb0ffd5fbbbf2ba460a67c40967fc346d014284`.
- Native-compiled EX4 SHA-256: `460054a6604275987d0e17092349edba527f0218552dd395f3891f5c98ca8506`.
- MetaEditor MT4: `0 errors, 0 warnings`, 560 ms, source-copy hash matched repository source exactly.
- Stage-A lineage fixture: PASS.
- Stage-A authority/static firewall: PASS.
- Stage-B schema/no-wiring static: PASS.
- N3 policy, replay, recovery fail-closed, authority, identity-domain and D1 epoch tests: PASS.
- N3 static guard: PASS.
- N2 shadow/research synthetic suite: PASS.
- `git diff --check`: PASS.

No runtime/trading behavior is claimed from this schema-only stage. M5 remains unpopulated and non-authoritative.
