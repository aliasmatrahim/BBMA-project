# C035 Pre-Re-Entry Outer-BB Hold Context Decision — 2026-08-25

Branch: `d1-owner-dev`

## Status
**APPROVED / PARTIAL ACCEPT / PRE-REENTRY POSITION-MANAGEMENT CONTEXT / NO UNIVERSAL TP OVERRIDE**

## Decision
The previous broad C035 HOLD is narrowed.

Accepted bounded interpretation:
- a valid strong direction / Candle Arah context may reach the direction-side outer Bollinger Band before a Re-Entry has formed;
- if no source-valid Momentum/CSM continuation has formed and no Re-Entry has yet formed, the outer-BB touch by itself must not force TP/close;
- the position-management context may continue to observe for the expected Re-Entry stage;
- this is a **pre-Re-Entry lifecycle context**, not a new entry signal and not a universal rule for already Re-Entry-owned trades.

Canonical bounded sequence:

`VALID STRONG DIRECTION -> DIRECTION-SIDE OUTER BB REACHED -> NO VALID MOMENTUM -> NO RE-ENTRY YET -> OUTER-BB TOUCH ALONE DOES NOT FORCE TP -> CONTINUE OBSERVING FOR RE-ENTRY`

## Scope boundary
This C035 context ends when a valid Re-Entry forms. After Re-Entry formation, position management moves into the separate post-Re-Entry lifecycle/TP questions, including C044/no-Momentum handling. C035 must not be used to decide those later stages.

## Explicit guards
This decision must not be interpreted as:
- `outer BB reached => hold forever`;
- `outer BB reached => guaranteed Re-Entry`;
- `outer BB reached => new entry authority`;
- disabling broker hard SL, emergency protection or portfolio/risk controls;
- overriding a valid opposite-cycle invalidation or other approved lifecycle termination;
- suppressing the existing TP of an already executable Re-Entry/REM/RRE/REE trade merely because C035 exists;
- creating a new MQL4 execution path from Candle Arah alone.

## Source basis
- Home Course teaching states that when strong direction reaches the direction-side outer BB before Re-Entry and without Momentum, TP is not forced merely because the outer BB has been reached, because the Re-Entry stage is still expected.
- The same source separates this pre-Re-Entry situation from the later `Re-Entry -> no Momentum` management question.
- Finale strongly corroborates the structural sequence that Candle Arah/direction is a signal rather than the entry setup and that Re-Entry is the subsequent setup/entry stage; Finale does not by itself justify a broader universal hold rule.
- External BBMA community material is treated only as corroboration and does not outrank project source governance.

## Classification
- pre-Re-Entry outer-BB touch not forcing TP by itself: **SOURCE-SUPPORTED / ACCEPTED WITH BOUNDED SCOPE**;
- expectation that Re-Entry remains the next structural stage: **SOURCE-SUPPORTED CONTEXT**;
- universal hold/never-TP behavior: **REJECTED / NOT AUTHORIZED**;
- management after Re-Entry/no-Momentum: **SEPARATE C044 DECISION, NOT RESOLVED HERE**.

## Current EA impact
Current executable architecture enters through approved Re-Entry-owned paths (including REM/RRE/REE) rather than raw Candle Arah. Therefore this decision does **not** authorize a current M17/M23 source change by itself and must not alter the existing TP payload of already Re-Entry-owned trades.

## Change control
Documentation/strategy-spec decision only. No MQL4 source change is authorized by this record alone.
