# CORE-V2-F4 — Higher-Timeframe Context for Standalone H1 Re-Entry

Date: 2026-08-22
Status: **PARTIALLY RESOLVED — USER-APPROVED H4 PARENT OWNERSHIP; H4 ALIGNMENT CONTRACT STILL PENDING**
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

## Evidence classification
The source explicitly requires multi-timeframe reading and instructs that Re-Entry direction be checked against higher timeframes. The primary PDF also gives intraday H4/H1/M15 alignment guidance.

Finale strongly corroborates parent/child timeframe ownership:
- V05 teaches that a lower-timeframe direction signal may actually be completing a higher-timeframe Re-Entry and therefore must not be interpreted atomically;
- V05 teaches higher-TF Re-Entry with lower-TF completion across chains including H4/H1/M15;
- V06 repeats that a higher-timeframe Re-Entry is completed/read through lower-timeframe structures.

Classification: **DIRECT SOURCE PRINCIPLE + SOURCE-INFERRED / STRONG HINT FOR H4 AS THE IMMEDIATE PARENT OF H1 IN THE APPROVED INTRADAY CHAIN**.

The source does not provide a single verbatim sentence stating that every standalone H1 Re-Entry must be hard-gated by a specific Boolean H4 formula. That exact compatibility predicate remains a project specification question.

## Rejected alternatives
- H1-only execution with no higher-timeframe context: rejected as inconsistent with the source's MTF requirement.
- universal D1 + H4 hard alignment for every H1 Re-Entry: not selected; this is stricter than the source clearly establishes for the H4/H1/M15 intraday chain.
- `H4 OR D1` alignment as a generic fallback: rejected as an unsupported engineering compromise.
- H4 EMA50-only alignment: rejected as an insufficient substitute for BBMA higher-timeframe context.

## Remaining sub-specification
Before code is patched, define exactly what counts as **H4 compatible/aligned BBMA context** for an H1 Re-Entry.

The next review must decide whether H4 compatibility is based on:
- active H4 BBMA directional/cycle state;
- absence of opposite authoritative H4 state;
- Mid-BB/MA50 structure only as supporting context rather than sole owner;
- or another source-faithful state combination.

No M12/M15 code patch is authorized until this H4 compatibility contract is resolved.
