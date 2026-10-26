# M07 BB Shape Classification Contract

## Status
CP10 static reconciliation for the Build 5.15 owner source. This contract defines M07's auxiliary shape-label boundary; it does not add BBMA strategy or entry rules.

## Accepted Core boundary
Core V2 §4 distinguishes an expanding/directional Bollinger Band context from a flat/horizontal context. An outside-band close alone is not Momentum, and an outside close during flat/horizontal BB is not Momentum.

Evidence route: primary operational PDF p2 for the BBMA cycle; secondary `BBMA technique.pdf` pp.18–19 for BB movement context; Finale V02 rules OA-F-V02-001/002/003 (00:13:51–00:18:07, 00:24:44–00:25:59); accepted Core V2 §4. The detailed expansion/flat distinction is corroboration of the accepted Core, not a new filter.

## Ownership and connections
- M06 owns BB numeric production from closed source candles.
- M07 classifies a supplied current/previous band pair through `BuildBBShapeState` and `DetectBBState`.
- M27 currently invokes `BuildBBShapeState` for H1 and H4 snapshots and stores the resulting band structs.
- M10 owns CSM signal production. `DetectCSM` uses its own closed-band geometry and does not read `BollingerBand.State`, `BB_EXPANDING` or `BB_FLAT`.
- M12 consumes M10 CSM as a Type-3 Re-Entry precursor. M07 does not own, produce or gate that setup.

## Current engineering encoding
- `BB_FLAT` is returned only when Top, Mid and Low each move no more than one broker point between the current and previous closed band snapshots. One point is a numeric equality tolerance supplied by symbol properties; it is not a BBMA trading threshold.
- Otherwise, width ratio below 0.9 maps to `BB_SQUEEZE`; above 1.1 maps to `BB_EXPANDING`; the remaining range maps to `BB_CONTRACTING`. These legacy project labels are engineering classifications, not source-defined cutoffs. A modest width increase can therefore be labelled `BB_CONTRACTING` by M07.
- In the pinned Build 5.15 source, the `BB_*` enum is written by M07 but has no downstream code reader. The stored M27 band-state snapshots are likewise not used by the active Strategy-Core path. Consequently, these labels do not alter current CSM or entry behavior.

Do not connect these enum labels as a CSM gate or change their thresholds without a separately scoped source/architecture review and regression evidence. If the labels are later exposed to a user or consumed by strategy logic, their semantics and boundaries require independent validation.

## Verification status
Static inspection of owner source `459c0588e625d7f7630f0fb5612b7f04fda496de` confirms the described producer/call/reader boundary. No M07-specific test or runtime validation was run in CP10. Strategy Tester and broker/runtime remain governed by the qualified-history gate in Issue #292.
