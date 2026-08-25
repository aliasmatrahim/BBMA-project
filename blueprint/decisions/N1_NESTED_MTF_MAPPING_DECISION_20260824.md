# N1 — Nested / Recursive MTF BBMA Mapping Decision

Date: 2026-08-24  
Origin branch: `d1-owner-dev`  
Synchronized to canonical records: 2026-08-25

## Status
**APPROVED CORE CLARIFICATION / NO EXECUTION CHANGE**

This decision records the accepted interpretation of the BBMA multi-timeframe teaching after re-auditing the archived BBMA Finale V01–V07 transcript set, the project PDF references, the reconciled Home Course evidence and the current Strategy Core.

## Source-supported principle
BBMA structure is recursive/nested across related timeframes. A higher-timeframe structure is not read in isolation; lower-timeframe signal/setup structures may explain, support or complete the higher-timeframe journey.

Accepted examples of the structural principle include:
- higher-timeframe Re-Entry being read/completed through lower-timeframe structures;
- lower-timeframe Extreme / MHV/MLV / direction / Re-Entry appearing as part of a higher-timeframe journey;
- lower-timeframe direction that appears opposite in isolation not automatically proving an independent reversal when it belongs to a higher-timeframe Re-Entry context;
- the recurring BBMA lifecycle being observable at multiple timeframe scales.

## Canonical recursive cycle
The accepted BBMA lifecycle remains:

`Extreme -> TP Wajib -> MHV/MLV -> direction (eCSD/CSD) -> Re-Entry -> Momentum/CSM -> further Re-Entry -> opposite Extreme / cycle restart`

The same structural sequence may appear at different timeframe scales.

## Important non-rule
Nested mapping is **not** a deterministic one-to-one formula.

The project must not encode any unsupported rule such as:
- one D1 candle = exactly one H4 cycle;
- one D1 Momentum = exactly one complete H1 cycle;
- every lower-timeframe sub-cycle must be executed;
- every lower-timeframe signal must agree in raw direction with the higher-timeframe parent.

## Execution boundary
This clarification does **not** alter executable BBMA setup signatures.

Exact signatures remain:
- `REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV`;
- `RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme`;
- `REE = D1 Re-Entry + H4 Extreme + H1 Extreme`.

Standalone H1 Re-Entry, EntryMode semantics, D1 strategic gating, H4 owner semantics, SL/TP, risk and execution authority remain unchanged.

## Engineering interpretation
The project may implement a read-only nested context/lineage layer that:
- consumes existing owner-produced snapshots;
- links parent and child timeframe structures;
- identifies a deterministic journey/lineage identity;
- classifies relationship state for diagnostics and shadow research;
- does not independently detect BBMA signals;
- does not create, reject, rank or execute trades in N1.

## N1 invariant
For N1 observation mode:

`TRADE BEHAVIOUR BEFORE NMJE == TRADE BEHAVIOUR AFTER NMJE`

Specifically unchanged:
- eligible signal types;
- REM/RRE/REE signatures;
- candidate counts presented to M15;
- M15 final authority logic;
- M16 revalidation;
- SL/TP;
- lot/risk;
- broker execution;
- trade limits.

## Evidence classification
- recursive MTF / higher-lower relationship: **DIRECT SOURCE PRINCIPLE / STRONGLY CORROBORATED**;
- exact software states, JourneyID and lineage metadata: **EA ENGINEERING MAPPING**;
- using nested relation as an execution gate: **NOT APPROVED IN N1**.

## Change-control rule
Any future proposal to make nested state affect entry acceptance, entry count, priority or execution must be a separate N2/N3 decision backed by measured shadow data and explicit Strategy-Core review.
