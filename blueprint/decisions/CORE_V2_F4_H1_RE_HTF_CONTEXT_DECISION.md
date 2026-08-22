# CORE-V2-F4 — Higher-Timeframe Context for Standalone H1 Re-Entry

Date: 2026-08-22
Status: **PARTIALLY RESOLVED — USER-APPROVED H4 PARENT + AUTHORITATIVE CYCLE-STATE ALIGNMENT; EXACT H4 OWNER FAMILIES/TRANSITIONS STILL PENDING**
Branch: `blueprint-dev`

## User-approved decision 1 — immediate higher-timeframe owner
For a standalone executable H1 Re-Entry, the project adopts **H4 as the immediate higher-timeframe parent/context owner**.

Accepted principle:

`H4 BBMA CONTEXT -> H1 RE-ENTRY -> lower-TF completion/observation where applicable`

Operational meaning:
- a standalone H1 Re-Entry must not be treated as fully autonomous from higher-timeframe BBMA context;
- H4 is the immediate parent timeframe that must provide a compatible BBMA context for the H1 Re-Entry direction;
- D1 remains broader structural context and may be informative/important, but is **not** a universal mandatory hard gate for every standalone H1 Re-Entry;
- this decision does not redefine REM/RRE/REE signatures and does not convert standalone H1 Re-Entry into a three-timeframe combination setup;
- this decision does not authorize an EMA50-only, score-based, or generic trend filter as the H4 compatibility rule.

## User-approved decision 2 — H4 compatibility is an authoritative BBMA cycle/directional state
The project adopts **ACTIVE AUTHORITATIVE H4 BBMA DIRECTIONAL/CYCLE STATE** as the basis of H4 compatibility for a standalone H1 Re-Entry.

Accepted interpretation:
- H4 compatibility is not determined from one current H4 candle alone;
- H4 must have a source-valid BBMA state that has already established directional authority and remains current under its own owner/invalidation contract;
- a neutral candle occurring after a valid H4 directional state does not automatically erase that state if the H4 owner/cycle has not been invalidated or superseded;
- raw H4 `Extreme` alone is not sufficient as directional authority because Extreme is a signal/context stage and does not by itself establish completed reversal direction;
- raw H4 `MHV/MLV` alone is not sufficient as directional authority because MHV/MLV is a setup/loss-of-volume stage before direction is established;
- Mid-BB/MA50 position may remain supporting structural context but is not by itself the authoritative H4 owner;
- exact H4 owner families, transition priority and supersession rules still require a separate sub-review before code is patched.

Evidence classification: **SOURCE-INFERRED / STRONG HINT** built on direct source MTF principles and the source separation between Extreme/MHV setup stages, direction signals, Re-Entry and Momentum/continuation stages.

## Evidence classification
The source explicitly requires multi-timeframe reading and instructs that Re-Entry direction be checked against higher timeframes. The primary PDF also gives intraday H4/H1/M15 alignment guidance.

Finale strongly corroborates parent/child timeframe ownership:
- V05 teaches that a lower-timeframe direction signal may actually be completing a higher-timeframe Re-Entry and therefore must not be interpreted atomically;
- V05 teaches higher-TF Re-Entry with lower-TF completion across chains including H4/H1/M15;
- V06 repeats that a higher-timeframe Re-Entry is completed/read through lower-timeframe structures;
- V05/V06 preserve the source distinction between direction, setup and continuation stages rather than reducing higher-timeframe context to a single indicator reading.

Classification: **DIRECT SOURCE PRINCIPLE + SOURCE-INFERRED / STRONG HINT FOR H4 AS THE IMMEDIATE PARENT AND FOR OWNER/STATE-BASED ALIGNMENT**.

The source does not provide a single verbatim Boolean formula for every standalone H1 Re-Entry. The exact compatibility state machine remains a project specification.

## Rejected alternatives
- H1-only execution with no higher-timeframe context: rejected as inconsistent with the source's MTF requirement.
- universal D1 + H4 hard alignment for every H1 Re-Entry: not selected; this is stricter than the source clearly establishes for the H4/H1/M15 intraday chain.
- `H4 OR D1` alignment as a generic fallback: rejected as an unsupported engineering compromise.
- H4 EMA50-only alignment: rejected as an insufficient substitute for BBMA higher-timeframe context.
- current-H4-candle-only directional gating: rejected as too atomic for the source's cycle/state teaching.
- raw H4 Extreme-only or raw H4 MHV/MLV-only ownership: rejected because those stages do not by themselves establish authoritative direction.

## Remaining sub-specification
Before code is patched, define exactly which H4 states may own directional authority for H1 Re-Entry and how they transition.

The next review must decide:
- whether `eCSD`, `CSD`, `Re-Entry`, and `CSM/Momentum` are all valid H4 directional-owner states;
- whether some of those states merely initiate direction while later states inherit the same owner;
- how priority/transition works when multiple same-direction states are present;
- how opposite or superseding H4 states terminate the old owner;
- whether H4 neutral/transitional state with no active authoritative owner must block H1 execution.

No M12/M15 code patch is authorized until this H4 owner-state contract is resolved.
