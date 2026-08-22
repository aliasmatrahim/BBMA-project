# CORE-V2-F3 — Re-Entry Type 1 Context

Date: 2026-08-22
Status: **RESOLVED — USER-APPROVED TYPE 1 CORE SPECIFICATION PHILOSOPHY**
Branch: `blueprint-dev`

## User-approved decision 1 — Type 1 context
Re-Entry Type 1 must **not** be defined by an arbitrary MA5/MA10 touch alone.

Required structural context:

`PRIOR RISE/FALL -> SIDEWAYS/RANGING PHASE -> RELEVANT MA5/MA10 RETEST -> VALID CLOSE-SIDE`

Direction mapping remains source-derived:
- SELL Type 1: relevant MA5/MA10 High acts as resistance; the validating candle finds the cluster and remains/closes on the permitted SELL side.
- BUY Type 1: relevant MA5/MA10 Low acts as support; the validating candle finds the cluster and remains/closes on the permitted BUY side.

## User-approved decision 2 — structural meaning of sideways/ranging
The project adopts **BBMA structural ranging** rather than equating Type 1 ranging to one fixed numeric threshold or to `BB_FLAT` alone.

Accepted interpretation:
- a prior directional rise/fall has already occurred;
- active directional momentum has paused/ended rather than continuing as a valid CSM/momentum state;
- price consolidates/retraces rather than continuing impulsively;
- the relevant MA5/MA10 cluster begins acting as support/resistance for the intended Re-Entry direction;
- the final Re-Entry candle must still satisfy the accepted MA5/MA10 close-side rule.

`BB_FLAT` / horizontal BB may be **supporting evidence** for the ranging phase, but it is not by itself a universal or mandatory definition of Type 1 sideways.

## User-approved decision 3 — no fixed minimum candle count
The project adopts **NO FIXED MINIMUM CANDLE COUNT** for Type 1 ranging.

The source does not define a universal Type 1 requirement such as 2 candles, 3 candles, or any other fixed number. Therefore Type 1 maturity is governed by completion of the accepted structural conditions rather than by an invented candle-count threshold.

Consequences:
- do not copy the Type 2 three-candle rule into Type 1;
- do not reject a structurally valid Type 1 solely because it formed in fewer than an arbitrary project candle count;
- do not accept Type 1 solely because an arbitrary minimum candle count was reached;
- candle count may be recorded as metadata/observability, but it is not a BBMA Type 1 eligibility rule.

Evidence classification: **SOURCE-FAITHFUL ABSENCE OF NUMERIC RULE / USER-APPROVED PROJECT SPECIFICATION**.

## User-approved decision 4 — qualifying prior rise/fall
The project adopts **SOURCE-VALID BBMA DIRECTION/MOMENTUM STATE** as proof that the required prior rise/fall has occurred.

Accepted interpretation:
- a qualifying prior move must be evidenced by an already source-valid BBMA directional or momentum state before the Type 1 ranging/retrace phase;
- accepted state families are existing BBMA direction/momentum producers (`eCSD`, `CSD`, or `CSM/Momentum`) when valid under their own source contracts;
- EMA50 slope, ATR, pip displacement, candle-count movement and external indicators are not substitutes for this BBMA-state evidence;
- the prior state must precede the ranging/retrace phase.

This is classified **SOURCE-INFERRED / STRONG HINT**.

### Type-family classification guard
- if the active structure specifically satisfies Type 3 (`CSM -> retrace to MA5/MA50`), classify it as Type 3 rather than generic Type 1;
- if the active structure specifically satisfies Type 4 (`CSD -> retrace to MA5/10`), classify it as Type 4 rather than generic Type 1.

This is a deterministic project ownership rule, not a quality ranking.

## User-approved decision 5 — momentum pause / transition into ranging
The project adopts a **BBMA state-transition** interpretation rather than treating one non-CSM candle or `BB_FLAT` alone as proof that momentum has ended.

Accepted transition:

`PRIOR SOURCE-VALID DIRECTION/MOMENTUM -> ACTIVE MOMENTUM CEASES/PAUSES -> RETRACE/CONSOLIDATION TOWARD RELEVANT MA5/MA10 -> TYPE 1 VALIDATION`

Operational meaning:
- prior eCSD/CSD/CSM evidence must already exist under its own source-valid contract;
- the market must no longer be continuing as an active same-direction CSM/Momentum state;
- price must begin a retrace/consolidation phase toward the relevant MA5/MA10 support/resistance cluster rather than continue impulsively;
- one candle that merely fails the CSM detector is **not** sufficient by itself to prove ranging;
- `BB_FLAT`/horizontal BB may corroborate the pause but is not mandatory and is not the sole ranging definition;
- if source-valid same-direction CSM/Momentum resumes before Type 1 validation, the current ranging interpretation is no longer valid and must be re-evaluated;
- an opposite source-valid momentum/directional transition cannot be ignored.

Evidence classification: **SOURCE-INFERRED / STRONG HINT**.

## User-approved decision 6 — structural invalidation before Type 1 validation
The project adopts **STRUCTURAL INVALIDATION** for a pending Type 1 setup rather than a fixed candle expiry.

A pending Type 1 setup is invalidated, reset, or reclassified when any of the following occurs before validation:

1. **MA5/MA10 close-side failure**
   - price closes through/clears the relevant MA5/MA10 cluster against the intended Re-Entry direction;
   - pending Type 1 is invalid.

2. **Same-direction CSM/Momentum resumes**
   - the old ranging/pause phase is no longer the same setup;
   - reset/re-evaluate the pending Type 1 state.

3. **Opposite source-valid direction/momentum appears**
   - the old Type 1 directional context loses authority.

4. **A more specific Re-Entry family becomes the correct owner**
   - Type 3 or Type 4 takes ownership when its exact source-defined precursor/retrace contract is satisfied.

Evidence classification:
- MA5/MA10 close-side invalidation is directly source-supported;
- momentum-resumption/opposite-direction invalidation are **SOURCE-INFERRED / STRONG HINT**;
- Type 3/4 reclassification is deterministic project ownership.

## User-approved decision 7 — structural owner lifetime / freshness
The project adopts **STRUCTURAL OWNER LIFETIME WITH NO GENERIC FIXED EXPIRY**.

Accepted rule:
- prior direction/momentum evidence and the pending Type 1 context remain structurally relevant while the same BBMA setup/cycle remains authoritative;
- there is no generic 3/5/10-candle expiry merely because time has passed;
- owner lifetime ends only through one of the accepted structural invalidation/supersession events: MA5/MA10 close-side failure, resumed same-direction momentum that resets the ranging phase, opposite source-valid direction/momentum, more-specific Type 3/4 ownership, or a new authoritative BBMA state/cycle that supersedes the old owner;
- stale-state prevention must therefore be owner/state based, not timer based;
- candle age may be recorded for observability but is not a BBMA Type 1 validity rule.

Evidence classification: **SOURCE-INFERRED / STRONG HINT + SOURCE-FAITHFUL ABSENCE OF NUMERIC EXPIRY RULE**. The source teaches structural sequence/state and provides no universal Type 1 expiration count.

## Consolidated Type 1 contract

A Type 1 candidate may mature only through this structural path:

`SOURCE-VALID PRIOR DIRECTION/MOMENTUM`
`-> MOMENTUM CEASES/PAUSES`
`-> BBMA STRUCTURAL RANGING/RETRACE`
`-> RELEVANT MA5/MA10 SUPPORT/RESISTANCE INTERACTION`
`-> VALID CLOSE-SIDE`
`-> TYPE 1 VALIDATION`

There is:
- no MA-touch-only shortcut;
- no mandatory `BB_FLAT` requirement;
- no fixed minimum candle count;
- no fixed generic expiry;
- no EMA/ATR/pip heuristic substitution;
- no relabelling of exact Type 3/4 structures as generic Type 1.

## Source basis
- Primary PDF page 9: rise/fall + sideways/ranging + MA5/MA10 support/resistance context.
- Finale V01: Re-Entry follows directional confirmation in the cycle.
- Finale V02: expanding BB versus flat/no-momentum distinction.
- Finale V03: MA5 as Re-Entry/retest area after direction/momentum.
- Finale V05: direction is signal, Re-Entry is setup; MA5/MA10 close-side boundary.
- Finale V06: Re-Entry after direction confirmation around MA5, with MA10 confluence strengthening context.

## Rejected alternatives
- MA5/MA10 touch + close-side only;
- `BB_FLAT` alone as the ranging definition;
- fixed ATR/pip/range threshold as a Core rule;
- fixed 2-candle or 3-candle minimum for Type 1;
- EMA50 slope or raw price displacement alone as proof of prior rise/fall;
- requiring only CSM or only CSD as the universal prior move;
- one non-CSM candle as sufficient proof of momentum pause;
- fixed `N`-candle expiry as a BBMA Type 1 rule;
- disabling Type 1 indefinitely.

## Implementation guard
This record closes the **strategy specification philosophy** for CORE-V2-F3. It does not itself patch M12. Implementation must encode the approved state/owner transitions faithfully and then be audited against this record before CORE-V2-F3 can be called code-complete.