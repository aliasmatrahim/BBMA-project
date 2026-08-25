# C039 Double H1 Extreme -> H4 MHV Watch Decision — 2026-08-25

Branch: `d1-owner-dev`

## Status
**APPROVED / PARTIAL ACCEPT / CROSS-TF H4-MHV ANTICIPATION CONTEXT / NO CONFIRMATION OR EXECUTION AUTHORITY**

## Decision
The previous broad C039 HOLD is narrowed.

Accepted bounded interpretation:
- two source-valid H1 Extreme events in the same direction;
- with no source-valid opposite H1 Extreme between them;
- may be treated as **cross-timeframe evidence that H4 MHV may be forming**;
- this may create a read-only `H4_MHV_WATCH` / suspected-context state;
- it does **not** create or confirm H4 MHV.

## Confirmation boundary
H4 MHV remains owned and confirmed only by the H4 MHV lifecycle/detector on H4 itself. The H1 pattern cannot bypass H4 requirements for valid parent-cycle provenance, loss-of-momentum formation, frozen marked body/reference and the approved maturity/invalidation rules.

Canonical interpretation:

`H1 EXTREME(direction X) -> later H1 EXTREME(direction X) with no opposite H1 Extreme between -> H4_MHV_WATCH only -> H4 owner independently confirms or rejects H4 MHV`

## Explicit guards
This decision must not be interpreted as:
- `2x H1 Extreme => H4 MHV CONFIRMED`;
- automatic H4 setup creation;
- automatic entry, trade rejection, ranking, direction override or TP/SL change;
- replacement of the exact REM/RRE/REE contracts;
- bypass of H4 MHV source-timeframe maturity/invalidation;
- proof that H4 MHV must eventually occur.

If the H1 sequence is invalidated, an opposite H1 Extreme appears, or H4 fails its own MHV lifecycle, the watch context must be dropped.

## Architecture mapping
This decision fits the M12N/NMJE N1 observation-only boundary:
- cross-TF evidence may be collected as context/lineage;
- M12N/NMJE may not create, mature, reject, rank or execute a strategy-owned setup;
- H4 remains the authoritative owner of H4 MHV state.

## Source basis
- Home Course states that repeated same-direction H1 Extremes without an opposite Extreme between them can indicate a higher-timeframe structure, and specifically links Double H1 Extreme with H4 MHV formation.
- Accepted Finale/Core supports the broader principle that lower-TF structures may explain/complete higher-TF context, but does not establish a deterministic `2x H1 Extreme = H4 MHV confirmed` rule.
- External BBMA community examples are treated as corroboration only and do not outrank project source governance.

## Classification
- Double H1 Extreme as H4-MHV anticipation clue: **SOURCE-SUPPORTED CONTEXT / ACCEPTED**;
- H4 MHV confirmation from H1 count alone: **REJECTED / NOT AUTHORIZED**;
- execution authority from the clue: **NOT AUTHORIZED**.

## Change control
Documentation/strategy-spec decision only. No MQL4 source change is authorized by this record alone.
