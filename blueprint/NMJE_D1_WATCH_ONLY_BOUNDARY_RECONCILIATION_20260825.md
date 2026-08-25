# NMJE D1 Watch-Only / Non-Execution-Authority Boundary Reconciliation

Date: 2026-08-25
Branch: `d1-owner-dev`
Status: **PASS / DOCUMENTATION GAP CLOSED / NO EA SOURCE CHANGE**

## Revalidated boundary
D1 MHV/MLV and D1 eCSD may be observed as context, but they may not be used by NMJE as a higher-timeframe trigger/parent that directly authorizes a lower-timeframe entry.

## Source/Core basis
- MHV/MLV is setup/context rather than standalone direct execution authority.
- eCSD/CSD is direction intent; raw direction is not direct entry authority and the taught execution setup is Re-Entry.
- Exact executable MTF signatures remain REM = H4 RE + H1 Extreme + M15 MHV/MLV; RRE = D1 RE + H4 RE + H1 Extreme; REE = D1 RE + H4 Extreme + H1 Extreme.
- Home Course cross-source reconciliation keeps `higher-TF MHV -> direct lower-TF entry` as HOLD.
- Forum evidence is corroborating only and provides no higher-precedence authority for a D1 MHV/eCSD -> direct LTF shortcut.

## D1 Opportunity boundary
The approved D1 Opportunity Journey explicitly keeps **D1 MHV/MLV and D1 eCSD WATCH ONLY**. Active D1 opportunity families remain the separately approved Extreme->TPW tactical context, confirmed CSD context, confirmed D1 Re-Entry, and Momentum/CSM retrace context, each subject to its own LTF readiness/authority rules.

## Current-source verification
- `ENUM_D1_OPPORTUNITY_FAMILY` has no D1 MHV/MLV or eCSD executable family.
- D1 eCSD is handled by a watch helper and only logs `Action=WATCH_ONLY`; it never installs a D1 opportunity family.
- NMJE parent kinds include D1 Re-Entry and D1 strategic owner, but no D1 MHV/MLV or D1 eCSD parent kind.
- M12N remains read-only and M15 remains sole final new-entry authority.

## Locked guard
`D1 MHV/MLV or D1 eCSD -> NMJE context only -> NO direct LTF execution authority.`

Any future promotion requires separate source reconciliation and explicit strategy approval.
