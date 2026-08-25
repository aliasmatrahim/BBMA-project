# C042 Prior-Day D1 Strategic Context Decision — 2026-08-26

Branch: `d1-owner-dev`

## Status
**APPROVED / PARTIAL ACCEPT / PRIOR-DAY D1 STRATEGIC CONTEXT / LITERAL NEXT-DAY PREDICTION REJECTED / NO DIRECT EXECUTION AUTHORITY**

## Decision
The previous broad C042 HOLD is narrowed.

Accepted bounded interpretation:
- only a fully closed D1 candle/state may be carried forward as strategic context for the next trading day;
- valid D1 Momentum/CSM, CSD/direction, Re-Entry and MA50/major-trend context may influence how lower-timeframe structures are interpreted on the following day;
- the prior-day D1 state is a higher-timeframe prior/context, not a deterministic forecast that the next day must move in the same direction;
- next-day execution still requires fresh source-valid lower-timeframe / approved combination structure under the existing owner contracts.

Canonical bounded interpretation:

`FULLY CLOSED D1 STATE TODAY -> NEXT-DAY STRATEGIC PRIOR / HTF CONTEXT -> read fresh H4/H1/M15 structure -> execute only if existing BBMA setup/combination authority is satisfied`

## Literal predictive wording rejected
The source wording equivalent to `today's D1 close determines tomorrow's movement` must not be encoded as a universal prediction law.

The following interpretations are rejected:
- `bullish D1 close today => all trades tomorrow must be BUY`;
- `bearish D1 Momentum today => price tomorrow must fall`;
- prior-day D1 direction alone creating an order;
- bypassing fresh H4/H1/M15 validation;
- using the still-forming current D1 candle as if its close were already known;
- treating qualitative source words such as `determine`, `pasti` or equivalent as mathematical certainty.

## Scope and ownership
- D1 remains strategic / higher-timeframe context under the approved scoped owner architecture;
- a prior-day D1 state may bias interpretation, but it does not replace the current-day setup owner;
- if D1 is transitional, unresolved or invalid under the current D1 strategic-state rules, no forced next-day direction is allowed;
- lower-timeframe opposite-looking structures must still be interpreted through the approved MTF/nested ownership rules rather than automatically rejected.

## Exact combination preservation
The approved combination signatures remain unchanged:
- REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV;
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme;
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

C042 does not add, remove or substitute any component in those signatures and does not alter the D1 Opportunity / D1O-07 execution-identity contracts.

## Source basis
- Home Course HC-P14-016 contains the predictive wording that today's D1 close determines tomorrow's movement.
- The accepted source hierarchy supports D1 as major strategic/higher-timeframe context, but the primary/Core and Finale layers do not establish a universal deterministic next-day forecasting law.
- Finale supports higher-timeframe context and recursive lower-timeframe completion while explicitly requiring caution with literal qualitative words such as `pasti` / `100%`.
- External/community copies are corroboration only and do not outrank project source governance.

## Classification
- fully closed prior-day D1 as next-day strategic prior/context: **SOURCE-CONSISTENT / ACCEPTED WITH BOUNDED SCOPE**;
- literal deterministic next-day prediction: **REJECTED / NOT AUTHORIZED**;
- direct entry from prior-day D1 alone: **REJECTED / NOT AUTHORIZED**;
- fresh current-day lower-TF setup/combination validation: **REQUIRED / UNCHANGED**.

## Current EA impact
This decision is a strategy-spec clarification only. It does not authorize a new MQL4 execution path, does not alter REM/RRE/REE, D1O-07, SL/TP, MM, ranking, ownership or broker execution.

## Change control
Documentation/strategy-spec decision only. No MQL4 source change is authorized by this record alone.
