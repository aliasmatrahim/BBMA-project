# M12N — Nested MTF Journey Engine Contract

## Status
N1 observation-only architecture contract.

Module position: logical sub-module between M12 and M13.  
Orchestration owner: M27.

## Purpose
M12N/NMJE provides deterministic multi-timeframe context and lineage over already-owned BBMA states. It does not detect a new strategy signal and it does not have execution authority.

Its job is to answer:
- what BBMA state is currently known on each supported timeframe;
- which lower-timeframe states belong under which higher-timeframe structural parent;
- whether the observed relationship is aligned, supporting/completing, building, conflicting, unresolved or not applicable;
- which observed events belong to the same deterministic journey identity for diagnostics and shadow research.

## Source basis
Accepted Core interpretation:
- BBMA is read recursively across related timeframes;
- higher-timeframe Re-Entry may be completed/read through lower-timeframe signal/setup structures;
- an opposite-looking lower-timeframe direction does not automatically prove an independent reversal when it is structurally part of a higher-timeframe Re-Entry;
- recursive chains include D1/H4/H1 and H4/H1/M15 within the project's supported universe;
- exact REM/RRE/REE signatures remain unchanged.

Decision provenance: `blueprint/decisions/N1_NESTED_MTF_MAPPING_DECISION_20260824.md`.

## Position in architecture

`M08/M09/M10/M11/M12 owners -> M12N NMJE -> M13 collector -> M14 validator -> M15 final authority -> M16 revalidation`

M12N runs after current-cycle owner updates are complete and before M13 combination assembly.

## Hard ownership guard
M12N must never call or reimplement:
- Extreme detection/maturity logic;
- MHV/MLV detection/lifecycle logic;
- eCSD/CSD/CSM detection logic;
- D1 major-trend formula;
- Re-Entry detection/lifecycle logic;
- REM/RRE/REE construction;
- SL/TP/risk/execution logic.

Owner sources remain:
- M08 -> Extreme;
- M09 -> MHV/MLV;
- M10 -> direction / Momentum;
- M11 -> D1 strategic owner;
- M12 -> Re-Entry;
- M13 -> exact combination assembly;
- M14 -> exact combination validation;
- M15 -> final new-entry authority;
- M16 -> invalidation/revalidation.

M12N is read-only with respect to all those owner states.

## Supported timeframe hierarchy
N1 observes the existing project universe only:

`D1 -> H4 -> H1 -> M15`

N1 does not add M5/M1 data collection and does not extend detector coverage to a timeframe that the current owner implementation does not already provide.

## Data model
### ENUM_NESTED_RELATION
Required semantic states:
- `NESTED_NOT_APPLICABLE` — no meaningful nested relation can be formed from the available snapshots;
- `NESTED_BUILDING` — source-valid child structure exists but the parent/child journey is still developing;
- `NESTED_SUPPORTING` — child structure is consistent with supporting/completing an active higher-timeframe structural context;
- `NESTED_ALIGNED` — parent and child authoritative directional contexts are structurally compatible;
- `NESTED_CONFLICT` — authoritative resolved states are structurally incompatible and cannot be explained merely as a pre-direction/supporting child state under the current mapping;
- `NESTED_UNRESOLVED` — required owner provenance is missing, stale, restart-unresolved or otherwise cannot be proven safely.

No numeric confidence score or weighting is permitted.

### NestedTFNode
A node is an immutable observation summary for one timeframe. Conceptual fields:
- timeframe;
- authoritative signal/stage type where one exists;
- direction where source-owned;
- maturity/state code;
- source candle time;
- validity/resolution flags;
- owner provenance class.

The node must represent only facts available from existing owner snapshots. Missing detector coverage must remain unknown/not-observed rather than inferred.

### NestedJourneyState
Conceptual fields:
- pair identity;
- `JourneyID`;
- strategic direction where M11 has a confirmed D1 owner;
- D1/H4/H1/M15 node summaries;
- selected immediate parent timeframe/state;
- relation enum;
- resolved/valid flags;
- update candle time;
- diagnostic reason.

Exact struct names are implementation detail, but M12N must preserve enough identity to make output deterministic and debuggable.

## Parent selection in N1
Parent selection is descriptive only; it does not create strategy ownership.

Preference order for an observable structural parent:
1. current source-valid H4 Re-Entry when present;
2. otherwise current active H4 directional owner;
3. otherwise confirmed D1 Re-Entry where relevant to the observed chain;
4. otherwise confirmed D1 strategic owner as broad strategic context only;
5. if none is provable -> unresolved/not-applicable.

This order is an engineering observation hierarchy, not a new BBMA setup ranking and must not be reused by M15 as entry priority.

## Relation rules
N1 relation classification must remain conservative.

### ALIGNED
Use only when the relevant authoritative parent and child directional owners are both resolved and directionally compatible.

### SUPPORTING
May be used when a lower-timeframe pre-direction/supporting structure (for example source-valid Extreme/MHV/MLV stage) exists under an active higher-timeframe Re-Entry/structural context and the source relationship supports reading the child as part of completion rather than as an autonomous reversal.

Do not require raw direction equality for a pre-direction child structure.

### BUILDING
Use when source-valid components/stages exist but required maturity or parent-child resolution is incomplete.

### CONFLICT
Use only for resolved authoritative states that cannot coexist under the accepted parent-child interpretation. Do not classify a raw/pre-direction Extreme or MHV stage as conflict merely because its nominal direction differs from the higher-timeframe continuation direction.

### UNRESOLVED
Use on missing/stale/restart-unproven provenance. Fail-safe classification is mandatory.

## JourneyID
JourneyID is engineering metadata only.

Requirements:
- deterministic for the same pair + parent identity + structural direction + parent anchor candle;
- changes when the owning parent identity materially changes or is superseded;
- never acts as signal validity, freshness, expiry or execution authority;
- may remain available in historical diagnostics after the live relation is no longer current.

A recommended deterministic composition is:
`pair | parent timeframe | parent signal/owner type | parent direction | parent anchor candle time`
then hashed/string-normalized using existing stable project helpers where practical.

## Freshness and lifecycle
M12N must not invent TTLs, fixed candle expiry or session expiry.

Current journey state is derived from current owner-valid snapshots. If an underlying owner becomes void, superseded, expired under its own contract, or unresolved, M12N must reflect that immediately on the next processing cycle.

M12N does not mutate the underlying owner to force journey continuity.

## Restart behavior
N1 is fail-safe.

After restart:
- consume only owner states that their own recovery logic has proven;
- if H4 owner is recovery-unresolved or a required child lifecycle has no proven provenance, classify nested relation `NESTED_UNRESOLVED`;
- never reconstruct a journey from current price guesses;
- never use a last-known direction as current proof unless the owning module contract explicitly does so.

## D1 watch-only / non-execution-authority boundary
The following D1-origin states are deliberately context-only for NMJE and may never become a shortcut to lower-timeframe execution:
- **D1 MHV/MLV = WATCH ONLY / CONTEXT ONLY.** It may be represented in diagnostics or node history, but it must not be selected as an executable D1 parent, install a D1 opportunity family, create an M15 candidate, or authorize an LTF entry.
- **D1 eCSD = WATCH ONLY / DIRECTION-STAGE CONTEXT ONLY.** It may be observed/logged, but it must not install a D1 opportunity family, create an M15 candidate, or authorize an LTF entry.
- **D1 CSD remains a direction signal, not a direct entry.** The separately approved D1 Opportunity Journey may use confirmed D1 CSD only as opportunity context and still requires approved fresh lower-timeframe Re-Entry readiness.
- For D1-origin N1 parent selection, only the already-approved **D1 Re-Entry** parent and **D1 strategic owner** broad context are eligible parent kinds. D1 MHV/MLV and D1 eCSD are not parent kinds.
- No `higher-TF MHV/MLV -> direct lower-TF entry` shortcut is authorized.

This boundary is consistent with the canonical Core distinction `MHV/MLV = setup/context`, `eCSD/CSD = direction`, `Re-Entry = entry/setup zone`, exact REM/RRE/REE signatures, and the D1 Opportunity decision record.

## M13/M14 boundary
M13 and M14 must remain unchanged in strategy semantics.

M12N may expose metadata that can be copied beside a candidate for diagnostics, but M13 must still assemble only:
- REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV;
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme;
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

Nested metadata must not add a fourth component, substitute a timeframe or relax component maturity.

## M15 boundary — N1 hard invariant
M15 must ignore nested relation for entry eligibility and final selection in N1.

M12N is forbidden from:
- creating an M15 candidate;
- rejecting an M15 candidate;
- changing candidate direction;
- changing EntryMode behavior;
- ranking REM/RRE/REE;
- changing entry count.

## Diagnostics / shadow research
N1 may provide:
- compact per-pair journey diagnostics;
- JourneyID;
- relation label;
- parent identity;
- node summaries;
- frozen shadow metadata attached to a final decision/trade record only if doing so cannot affect execution identity or duplicate prevention.

Initial implementation should prefer logging/dashboard state over invasive payload changes.

## Prohibited scoring
Do not add:
- confidence %;
- AI score;
- weighted timeframe score;
- voting system;
- minimum nested score;
- hidden quality ranking.

The engine is state/lineage based only.

## N1 verification gates
Before N1 can be considered implemented:
1. native MT4 MetaEditor compile = 0 errors / 0 warnings;
2. no new strategy detector calls inside M12N;
3. M13 exact signatures unchanged;
4. M15 candidate eligibility code unchanged semantically;
5. M16 revalidation unchanged semantically;
6. SL/TP/risk/execution paths unchanged;
7. one M12N update per pair per closed-M15 processing cycle;
8. restart-unproven context becomes `NESTED_UNRESOLVED`;
9. diagnostics demonstrate deterministic relation/JourneyID output;
10. source diff audit confirms N1 cannot alter trade behavior.

## Future phases
N2 may collect shadow outcome statistics by relation state.

N3 may propose an optional execution gate only after measured evidence and a separate approved decision. N1 does not authorize N2/N3 behavior.
