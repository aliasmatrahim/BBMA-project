# C048 Extreme Magic Strength-Subtype Decision — 2026-08-26

Branch: `d1-owner-dev`

## Status
**APPROVED / PARTIAL ACCEPT / SOURCE-SUPPORTED EXTREME STRENGTH SUBTYPE / NO INDEPENDENT EXECUTION AUTHORITY / NORMAL EXTREME MATURITY PRESERVED**

## Decision
The previous broad C048 HOLD is narrowed.

Accepted bounded interpretation:
- `Extreme Magic` is source-supported terminology for an Extreme where MA10 also extends outside the relevant outer Bollinger Band together with the usual MA5 Extreme extension;
- this represents a rarer/stronger Extreme extension or reversal-strength context;
- the presence of MA10 outside BB does **not** create a separate executable setup family and does not bypass the normal Extreme lifecycle;
- valid Extreme confirmation/reversal and retest requirements remain required before any standalone Extreme entry-ready interpretation;
- normal Extreme TP-Wajib semantics remain attached to the Extreme lifecycle unless a separately approved advanced/MTF exception applies.

Canonical bounded interpretation:

`NORMAL EXTREME CONDITION + MA10 ALSO OUTSIDE RELEVANT OUTER BB -> EXTREME MAGIC / STRONGER EXTREME CONTEXT`

but:

`EXTREME MAGIC != IMMEDIATE ENTRY AUTHORITY`

and:

`EXTREME MAGIC -> still require valid Extreme reversal confirmation -> retest/maturity -> existing lifecycle`

## Source basis
- Home Course / Workbook material states that `Magic Extreme / Extreme Magic` occurs when MA5 and MA10 are outside the BB, is rare, and is often associated with prolonged sideways.
- Finale V05 OA-F-V05-002 describes MA10 extending outside together with MA5 as a stronger/double Extreme while explicitly retaining it as an Extreme rather than a separate entry contract.
- Public/derivative BBMA manuals consistently describe MA10 outside BB as `Extreme Magic` / `strong for reverse`, but in the same teaching sequence still require valid Extreme confirmation, reverse candle, retest and TP-Wajib.
- Public/community material is corroboration only and does not outrank project source governance.

## Explicit guards
This decision must not be interpreted as:
- `MA5 + MA10 outside BB => BUY/SELL now`;
- a new standalone detector family with independent broker execution authority;
- bypassing reversal-candle confirmation;
- bypassing retest/maturity;
- overriding Momentum invalidation;
- overriding REM/RRE/REE exact signatures;
- changing SL/TP, MM, ranking, timeframe ownership or broker execution;
- promoting unresolved advanced/MTF no-TP Extreme exceptions.

## Relationship to normal Extreme
Extreme Magic is an **Extreme subtype / strength annotation**. It strengthens the qualitative interpretation of the Extreme condition but does not replace the canonical Extreme owner/lifecycle.

The normal accepted Extreme lifecycle remains:
1. source-valid Extreme condition;
2. reversal confirmation;
3. retest/maturity;
4. only then any standalone Extreme entry-ready interpretation under separately approved execution authority;
5. normal TP-Wajib behavior remains unless a separately approved exception governs the specific context.

## Classification
- MA5 + MA10 outside relevant outer BB as `Extreme Magic`: **SOURCE-SUPPORTED / ACCEPTED**;
- rarity / stronger reversal-extension context: **SOURCE-SUPPORTED QUALITATIVE CONTEXT**;
- independent executable authority: **REJECTED / NOT AUTHORIZED**;
- bypass of normal Extreme maturity: **REJECTED / NOT AUTHORIZED**;
- advanced/no-TP exception: **SEPARATE HOLD / NOT RESOLVED HERE**.

## Current EA impact
No new MQL4 execution path is authorized. If represented later in observability/NMJE, it should be metadata/strength context only unless a separate execution decision is explicitly approved. Existing Extreme, REM/RRE/REE, SL/TP, MM, ownership and broker-execution contracts remain unchanged.

## Change control
Documentation/strategy-spec decision only. No MQL4 source change is authorized by this record alone.
