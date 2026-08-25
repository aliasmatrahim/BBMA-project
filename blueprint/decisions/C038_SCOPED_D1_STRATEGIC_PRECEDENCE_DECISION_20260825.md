# C038 Scoped D1 Strategic Precedence Decision — 2026-08-25

Branch: `d1-owner-dev`

## Status
**APPROVED / PARTIAL ACCEPT / SCOPED D1 STRATEGIC PRECEDENCE / NO UNIVERSAL D1 OVERRIDE**

## Decision
The previous broad C038 HOLD is narrowed.

Accepted bounded interpretation:
- D1 may own the higher structural / major-trend context when the approved D1 strategic state is valid and established;
- an H4 direction that is temporarily opposite to that D1 context does not, by itself, become universal major-trend reversal authority;
- the H4 opposite leg may represent retracement, correction or child structure inside the higher-timeframe D1 context;
- lower-timeframe opposite-looking direction must be interpreted through the approved multi-timeframe ownership/context before being promoted as an independent reversal;
- execution authority remains governed by the existing approved setup/signature and lower-timeframe lifecycle contracts.

Canonical bounded interpretation:

`VALID ESTABLISHED D1 STRATEGIC CONTEXT -> OPPOSITE H4 DIRECTION -> DO NOT AUTO-PROMOTE H4 AS MAJOR-TREND REVERSAL -> INTERPRET AS POSSIBLE RETRACEMENT/CHILD STRUCTURE -> APPLY APPROVED MTF SETUP/OWNER CONTRACT -> EXECUTION ONLY THROUGH EXISTING AUTHORITY`

## Unresolved / transition guard
If D1 is `TRANSITION`, `UNRESOLVED`, stale, invalid, or otherwise lacks established strategic ownership, this decision must not force BUY/SELL merely from the last D1 candle or MA50 relationship. No universal directional override is authorized in unresolved D1 state.

## Exact execution contracts remain unchanged
This decision does not redefine or replace:
- REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV;
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme;
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme;
- standalone/deduplicated Re-Entry execution ownership;
- D1 Opportunity / D1O-07 canonical dedup identity;
- M15 final authority / lower-TF execution timing;
- existing SL/TP, risk, money-management or broker-execution contracts.

## Explicitly NOT promoted
The following are rejected / not authorized:
- `D1 BUY + H4 SELL => BUY always` as a universal executable law;
- `D1 SELL + H4 BUY => SELL always` as a universal executable law;
- cancelling any valid approved setup merely because an H4 leg is opposite to D1;
- treating one H4 signal as sufficient to reverse established D1 ownership;
- forcing direction when D1 is unresolved or transitional;
- bypassing exact REM/RRE/REE and Re-Entry authority with a raw D1-vs-H4 comparison.

## Source basis
- Home Course teaches MA50/D1 as major-trend / daily structural context and includes the literal pedagogical statement that when D1 and H4 conflict, D1 should be followed.
- The primary Oma Ally reference supports higher-timeframe checking and highlights Daily MA50 for continuation-vs-reversal context, but does not establish a universal executable `D1 always overrides H4` law.
- Finale strongly supports higher-timeframe ownership/context: a lower-timeframe opposite-looking signal may belong to the higher-timeframe Re-Entry structure and should not automatically be interpreted as an independent reversal.
- External BBMA community examples are treated as corroboration only and do not outrank project source governance.

## Classification
- valid established D1 as higher strategic / major-trend context: **SOURCE-SUPPORTED / ACCEPTED WITH SCOPE**;
- H4 opposite direction as possible retracement/child structure: **SOURCE-SUPPORTED MTF CONTEXT**;
- universal literal D1-over-H4 execution override: **REJECTED / NOT AUTHORIZED**;
- current scoped D1/MA50 owner architecture: **CONSISTENT WITH THIS DECISION**.

## Current EA impact
The current scoped D1 strategic-owner architecture is already closer to this decision than the literal Workbook wording. Therefore this record does **not** authorize an MQL4 logic change by itself.

## Change control
Documentation/strategy-spec decision only. Any future source change must preserve exact approved setup ownership and cannot create a new universal D1 override without a separate explicit decision.
