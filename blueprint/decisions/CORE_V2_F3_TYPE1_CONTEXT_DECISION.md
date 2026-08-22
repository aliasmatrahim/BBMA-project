# CORE-V2-F3 — Re-Entry Type 1 Context

Date: 2026-08-22
Status: **PARTIALLY RESOLVED — USER-APPROVED CONTEXT/RANGING/PRIOR-MOVE/MOMENTUM-PAUSE PHILOSOPHY; INVALIDATION/OWNER-LIFETIME PREDICATE STILL PENDING**
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

Evidence classification: **SOURCE-FAITHFUL ABSENCE OF NUMERIC RULE / USER-APPROVED PROJECT SPECIFICATION**. The source is explicit about the Type 1 structural context but silent on a universal minimum candle count.

## User-approved decision 4 — qualifying prior rise/fall
The project adopts **SOURCE-VALID BBMA DIRECTION/MOMENTUM STATE** as the proof that the required prior rise/fall has occurred.

Accepted interpretation:
- a qualifying prior move must be evidenced by an already source-valid BBMA directional or momentum state before the Type 1 ranging/retrace phase;
- accepted state families are the existing BBMA direction/momentum producers (`eCSD`, `CSD`, or `CSM/Momentum`) when they are valid under their own source contracts;
- EMA50 slope, ATR, pip displacement, candle-count movement and external indicators are not substitutes for this BBMA-state evidence;
- the prior state must precede the ranging/retrace phase; a same-candle MA touch with no prior BBMA directional/momentum state is not sufficient to manufacture Type 1.

This is classified **SOURCE-INFERRED / STRONG HINT**. The PDF explicitly requires Type 1 after a rise/fall. Finale repeatedly teaches direction/momentum before Re-Entry, but it does not give a verbatim sentence saying that Type 1 must be encoded specifically as `eCSD/CSD/CSM` state memory.

### Type-family classification guard
This prior-state rule must not erase the source-defined special Re-Entry families:
- if the active structure specifically satisfies the Type 3 contract (`CSM -> retrace to MA5/MA50`), classify it as Type 3 rather than relabeling it generic Type 1;
- if the active structure specifically satisfies the Type 4 contract (`CSD -> retrace to MA5/10`), classify it as Type 4 rather than relabeling it generic Type 1.

This guard is deterministic project classification to prevent duplicate/mislabelled setup ownership. It is not a claim that the source ranks Type 3/4 above Type 1 by quality.

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
- an opposite source-valid momentum/directional transition cannot be ignored and carried forward as if the old Type 1 direction were still authoritative.

Evidence classification: **SOURCE-INFERRED / STRONG HINT**. Finale V02 explicitly distinguishes expanding-BB momentum from flat/no-momentum conditions, while V05/V06 repeatedly teach direction/momentum followed by retrace/Re-Entry. The exact state-machine encoding is a project specification, not a verbatim source algorithm.

## Evidence classification
The requirement for **rise/fall + sideways/ranging + MA5/MA10 support/resistance behavior** is directly source-backed by the primary PDF page-9 Type 1 description.

Finale provides supporting context rather than a dedicated numeric Type 1 formula:
- V02 distinguishes expanding BB from flat/horizontal BB and states that flat BB has no directional momentum.
- V01 places Re-Entry after directional confirmation in the normal cycle.
- V03 repeatedly frames MA5 as the Re-Entry/retest area after direction/momentum develops.
- V05 explicitly states that direction is a signal, not the entry, and that the trader waits for Re-Entry; it also reinforces the MA5/MA10 close-side boundary.
- V06 again teaches Re-Entry after direction confirmation around MA5, with MA10 confluence strengthening the setup.

Therefore:
- `MA touch alone = Type 1` is rejected as too broad;
- `BB_FLAT alone = Type 1 sideways` is rejected as too narrow/unsupported;
- a fixed minimum Type 1 candle count is rejected as unsupported;
- generic EMA/ATR/pip movement is rejected as proof of the required prior BBMA move;
- one isolated non-CSM candle is rejected as proof that momentum has ended.

The structural-ranging, prior-BBMA-state and state-transition interpretations are classified as **SOURCE-INFERRED / STRONG HINT** built on explicit PDF requirements plus Finale cycle/context teaching.

## Remaining implementation sub-specification
The Core philosophy is now substantially resolved, but code still needs a deterministic invalidation/ownership predicate.

Remaining questions to resolve before patching M12 include:
- exactly which structural events invalidate a pending Type 1 setup before the validating Re-Entry candle;
- how to treat a break/close through the relevant MA5/MA10 cluster before validation;
- how an opposite source-valid direction/momentum state terminates the old Type 1 direction context;
- how long the prior direction/momentum state remains structurally relevant, using owner-state validity rather than an invented generic candle-count window.

These must be resolved using existing BBMA structure/state where possible, not RSI/ADX/ATR/pip-width heuristics.

## Rejected alternatives
- MA5/MA10 touch + close-side only: rejected as incomplete.
- `BB_FLAT` alone as the ranging definition: rejected.
- fixed ATR/pip/range threshold as a Core rule: rejected as unsupported.
- fixed 2-candle or 3-candle minimum for Type 1: rejected as unsupported.
- EMA50 slope or raw price displacement alone as proof of prior rise/fall: rejected.
- requiring only CSM or only CSD as the universal prior move: rejected as unnecessarily narrow; valid BBMA direction/momentum state is the accepted family-level proof.
- one non-CSM candle as sufficient proof of momentum pause: rejected.
- disabling Type 1 indefinitely: not selected.

## Implementation guard
No M12 code patch is authorized until the remaining invalidation/owner-lifetime predicate is resolved. The current active implementation remains subject to this known Core gap.
