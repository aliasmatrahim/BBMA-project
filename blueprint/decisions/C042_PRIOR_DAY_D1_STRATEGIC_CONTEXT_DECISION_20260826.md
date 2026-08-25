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

---

## 2026-08-26 Contract-Consistency Clarification

This clarification narrows terminology only; it does **not** change C042 strategy semantics or authorize source changes.

### Observation / interpretation is not execution eligibility
The phrase `lower-timeframe opposite-looking structures must still be interpreted` applies to analysis/NMJE observation only. It means an opposite-looking child structure may be read as `BUILDING`, `SUPPORTING`, `ALIGNED`, `CONFLICT` or `UNRESOLVED` under the existing nested-MTF contract instead of being declared an autonomous reversal merely from nominal direction.

It does **not** mean that an opposite-direction lower-timeframe structure remains executable against the current M11 strategic owner.

When a structure reaches the executable candidate path:
- M11 remains the sole producer of the current D1 major-trend strategic owner;
- M15 remains the sole final new-entry direction / eligibility authority;
- confirmed D1 BUY permits only BUY execution candidates;
- confirmed D1 SELL permits only SELL execution candidates;
- `D1_TRANSITION` / `D1_OWNER_UNRESOLVED` block new strategy entries;
- NMJE/C042 context cannot override or bypass this gate.

Canonical distinction:

`OPPOSITE-LOOKING LTF STRUCTURE -> MAY STILL BE OBSERVED / INTERPRETED IN NESTED CONTEXT`

but

`EXECUTABLE CANDIDATE -> MUST STILL PASS CURRENT M11 D1 OWNER + M15 FINAL AUTHORITY`

### Prior-day context does not create a second D1 owner
C042 does not install a separate persisted `prior-day bias` execution variable and does not compete with the current M11 owner snapshot. For new-entry authority, the M11 result derived from the latest fully closed D1 state remains canonical.

D1 Momentum/CSM, CSD/direction and Re-Entry mentioned by C042 may remain source-owned higher-timeframe context under their existing modules/contracts, but they do not substitute for M11 MA50 strategic-owner confirmation and do not gain direct-entry authority through C042.

### D1 Opportunity boundary preserved
C042 does not create, extend or re-rank a D1 Opportunity family. Any existing D1 Opportunity execution still requires its separately approved fresh lower-timeframe readiness and identity contracts.

### Implementation consequence
**No MQL4 change required or authorized.** The current execution hierarchy remains:

`M11 D1 OWNER -> owner-valid H4/H1/M15 structures -> M13/M14 where applicable -> M15 FINAL AUTHORITY -> M16 revalidation -> downstream SL/risk/execution`
