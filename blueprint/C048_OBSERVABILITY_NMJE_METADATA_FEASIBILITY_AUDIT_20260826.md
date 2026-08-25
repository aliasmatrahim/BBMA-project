# C048 Extreme Magic Observability / NMJE Metadata Feasibility Audit — 2026-08-26

Branch: `d1-owner-dev`

## Status
**PASS / TECHNICALLY FEASIBLE AS DERIVED OBSERVABILITY METADATA / NO MQL4 IMPLEMENTATION AUTHORIZED / NO EXECUTION AUTHORITY**

## Scope
Assess whether the approved C048 `Extreme Magic` strength subtype can be represented later in diagnostics/NMJE without changing canonical Extreme detection, maturity, combinations or execution.

## Source/contract anchors
- C048 defines Extreme Magic as normal Extreme context where MA10 is also outside the relevant outer BB together with MA5, while explicitly preserving normal Extreme confirmation/retest maturity and rejecting independent execution authority.
- M08 remains the canonical Extreme owner/detector lifecycle boundary.
- M12N/NMJE is read-only observation/lineage and is forbidden from changing owner states or M15 execution eligibility.

## Technical feasibility
The active data model already carries all required closed-candle numeric inputs:
- MA5 High / MA10 High;
- MA5 Low / MA10 Low;
- TOP_BB / LOW_BB;
- canonical Extreme direction/state through the existing M08 lifecycle.

No new indicator, external data source, score, timeframe or detector family is required merely to identify the C048 annotation.

## Safe derived definition for future observability
Only after a canonical source-owned Extreme context is already present, a read-only metadata layer may classify:

### SELL-side Extreme Magic context
`canonical Extreme SELL context` AND `MA5_High > TOP_BB` AND `MA10_High > TOP_BB`.

### BUY-side Extreme Magic context
`canonical Extreme BUY context` AND `MA5_Low < LOW_BB` AND `MA10_Low < LOW_BB`.

This is a subtype/annotation check only. It must not become a replacement for `DetectExtreme()` and must not change the canonical price-close VOID rule or CSM invalidation/lifecycle behavior.

## Hard non-mutation guards
A future C048 observability implementation must not modify or influence:
- `ExtremeLifecycleData.Maturity`;
- canonical Extreme `IsValid` / direction / confirmation / retest ownership;
- M13 component type or component count;
- exact REM/RRE/REE signatures;
- M14 validation;
- M15 candidate eligibility, direction or selection;
- M16 invalidation;
- SL/TP;
- MM/risk;
- `DecisionID`, `SequenceHash`, execution hash or duplicate identity;
- broker execution or position lifecycle.

## Recommended representation if separately authorized later
Prefer a read-only derived metadata field/enum or compact diagnostic label such as:
- `ExtremeStrengthSubtype = NORMAL | MAGIC`;
- or equivalent boolean `IsExtremeMagicContext`.

The value should be recomputed from the same frozen closed-candle owner snapshot used for diagnostics rather than persisted as execution authority.

For NMJE it may appear only in node/diagnostic metadata and must not alter `NESTED_*` relation eligibility rules or parent selection authority.

## Why no source patch is made now
C048 explicitly states that its decision is documentation/strategy-spec only and authorizes no MQL4 path by itself. Technical feasibility is not implementation authorization.

Adding even read-only source metadata would change the EA source identity and require a new compile/regression lineage. There is no current execution need that justifies doing that while C044 broker-runtime validation remains blocked.

## Decision
**C048 feasibility gate CLOSED/PASS. No EA source change required or authorized.**

If a later explicit observability implementation is approved, it can be added as non-execution metadata using the guards above and must receive static + native MetaEditor regression before closure.
