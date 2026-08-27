# NMJE N3 Step 4 — M15/M16 Shadow Provenance Record

Date: 2026-08-27
Branch: `nmje-n3-hardening-dev`
Status: SOURCE MATERIALIZED / SHADOW ONLY

## Materialized behavior
- `BBMA_Decision` now carries frozen NMJE journey provenance metadata: JourneyID, ParentEventID, relation, update-candle identity, and snapshot-present flag.
- M15 freezes the current already-built NMJE observation after canonical candidate selection.
- M16 compares the frozen provenance with the same current closed-M15 NMJE snapshot.
- M16 emits `[N3-NMJE-SHADOW][M16]` diagnostics.

## Authority firewall
This step does **not** add an execution gate.
- NMJE mismatch does not set DEC_INVALIDATED, DEC_REJECTED, or DEC_EXPIRED.
- Candidate/RAW maturity is unchanged.
- M15 remains final selection authority.
- M16 remains final revalidation authority using existing BBMA owner/component rules.
- M22 remains sole OrderSend owner.

## Purpose
Collect exact M15->M16 identity-consistency evidence before any N3 enforcement decision. This is provenance hardening only and introduces no BBMA strategy filter, score, vote, session/news/correlation rule, or universal nesting requirement.

## Next safe gate
1. Native MetaEditor compile 0E0W.
2. Static authority-leak guard PASS.
3. N2/N3 selftests PASS.
4. Add replay/restart equivalence tooling for the frozen NMJE identity path.
5. Keep enforcement disabled until runtime evidence and explicit activation boundary are satisfied.
