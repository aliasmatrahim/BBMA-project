# M12N — Nested MTF Journey Engine Contract

## Status
N1 observation-only architecture contract.  
Origin branch: `d1-owner-dev`  
Synchronized to canonical records: 2026-08-25

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

## Relation states
Required semantic states:
- `NESTED_NOT_APPLICABLE`
- `NESTED_BUILDING`
- `NESTED_SUPPORTING`
- `NESTED_ALIGNED`
- `NESTED_CONFLICT`
- `NESTED_UNRESOLVED`

No numeric confidence score or weighting is permitted.

## JourneyID
JourneyID is engineering metadata only and must be deterministic for the same pair + parent identity + structural direction + parent anchor candle. It must never act as signal validity, freshness, expiry or execution authority.

## Freshness / lifecycle
M12N must not invent TTLs, fixed candle expiry or session expiry. Current journey state is derived from current owner-valid snapshots. If an underlying owner becomes void, superseded, expired under its own contract or unresolved, M12N reflects that on the next processing cycle.

## Restart behavior
After restart M12N consumes only owner states their own recovery logic has proven. Missing/unproven provenance must resolve fail-safe to `NESTED_UNRESOLVED` rather than guessing from current price or last-known direction.

## M13/M14 boundary
M13 and M14 strategy semantics remain unchanged. Exact signatures remain:
- REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV;
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme;
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

Nested metadata must not add a fourth component, substitute a timeframe or relax component maturity.

## M15 boundary — N1 invariant
M15 ignores nested relation for entry eligibility and final selection in N1. M12N is forbidden from creating/rejecting candidates, changing direction, changing EntryMode behavior, ranking REM/RRE/REE or changing entry count.

## Diagnostics / shadow research
N1 may provide compact per-pair journey diagnostics, JourneyID, relation label, parent identity, node summaries and frozen shadow metadata where it cannot affect execution identity or duplicate prevention.

## Prohibited scoring
Do not add confidence %, AI score, weighted timeframe score, voting, minimum nested score or hidden quality ranking. The engine is state/lineage based only.

## N1 verification gates
Before N1 can be considered implemented:
1. native MT4 MetaEditor compile = 0 errors / 0 warnings;
2. no new strategy detector calls inside M12N;
3. M13 exact signatures unchanged;
4. M15 candidate eligibility unchanged semantically;
5. M16 revalidation unchanged semantically;
6. SL/TP/risk/execution paths unchanged;
7. one M12N update per pair per closed-M15 processing cycle;
8. restart-unproven context becomes `NESTED_UNRESOLVED`;
9. diagnostics demonstrate deterministic relation/JourneyID output;
10. source diff audit confirms N1 cannot alter trade behavior.

## Future phases
N2 may collect shadow outcome statistics by relation state. Any execution-affecting extension requires a separate approved decision and explicit Strategy-Core review.
