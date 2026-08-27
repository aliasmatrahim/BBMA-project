# NMJE N3 Step 3 — Parent Provenance Materialization Record

Date: 2026-08-27
Branch: `nmje-n3-hardening-dev`
Status: SOURCE MATERIALIZED / REVALIDATION TRIGGER

Materialized provenance-only changes:
- `NestedTFNode.CanonicalEventID` is derived from immutable canonical owner facts.
- `NestedJourneyState.ParentEventID` records the exact canonical owner selected as the N1 parent.
- Re-Entry identity anchors to `StartCandleTime`; Extreme anchors to `RawCandleTime`; MHV/MLV anchors to canonical parent Extreme raw+confirmation identity; D1/H4 owner identities use their canonical source candle provenance.
- N1/N2 diagnostics expose compact deterministic event identity metadata.

No entry signature, maturity rule, D1 authority, M15/M16 authority, risk rule, SL/TP rule, or order-execution behavior is changed by this step.

This normal repository commit intentionally retriggers branch-aware static and native MetaEditor validation against the materialized source.
