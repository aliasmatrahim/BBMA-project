# CORE-V2-F2 — Extreme Maturity inside REM / REE

Date: 2026-08-22
Status: **PARTIALLY RESOLVED — MATURITY + REVERSAL-DIRECTION + FIRST-QUALIFYING-CANDLE PROMOTION + STRUCTURAL ANCHOR FREEZE + RETEST-START TRIGGER + BODY-ANCHOR MAPPING + RETEST-INTERACTION VALIDATION USER APPROVED; BODY-vs-MA5 PRIORITY FINAL CHECK STILL PENDING**
Branch: `blueprint-dev`

## Decision 1 — Extreme maturity inside REM / REE
For an Extreme to be eligible as a component of an executable REM or REE combination, it must be at least **reversal-confirmed**.

A standalone Extreme entry remains a different maturity level and requires the later **retest** entry stage.

Operational maturity distinction:

`RAW EXTREME -> REVERSAL-CONFIRMED EXTREME -> RETEST/ENTRY-READY EXTREME`

- `RAW EXTREME`: MA5/MA10 outside the relevant outer BB under the strict accepted detector rule. Not sufficient for executable REM/REE.
- `REVERSAL-CONFIRMED EXTREME`: raw Extreme plus source-valid reversal confirmation. Eligible as an Extreme component of REM/REE.
- `RETEST/ENTRY-READY EXTREME`: reversal-confirmed Extreme plus the later retest. Required for standalone Extreme entry eligibility.

### Evidence classification
**SOURCE-INFERRED / STRONG HINT**, not a verbatim Oma Ally rule specifically defining REM/REE component maturity.

Evidence basis:
- Finale V04 separates raw Extreme, reversal confirmation and retest, and identifies retest as the standalone Extreme entry stage.
- Finale V05 teaches lower-timeframe Extreme/MHV/direction structures as components/completion context for higher-timeframe Re-Entry, supporting a maturity distinction between component use and standalone Extreme entry.

## Decision 2 — minimal deterministic reversal-direction mapping
The project adopts **DIRECTIONAL REVERSAL CANDLE / REVERSAL PHASE** as the minimum deterministic interpretation of the source requirement for reversal after RAW Extreme.

Accepted mapping:
- confirmation uses closed candles on the same source timeframe;
- SELL Extreme reversal-direction candle: `Close < Open`;
- BUY Extreme reversal-direction candle: `Close > Open`;
- previous-candle colour flip is not mandatory;
- no named candlestick pattern is mandatory;
- reversal is not forced into a fixed one-/two-candle template;
- close back inside BB is supporting/preferred, not a universal hard requirement;
- if accepted outside-BB/Momentum invalidation occurs before confirmation, the RAW candidate is void.

### Evidence classification
**DIRECT SOURCE REQUIREMENT + MINIMAL DETERMINISTIC PROJECT MAPPING**.

The exact Boolean `SELL: Close < Open` / `BUY: Close > Open` is the project's smallest deterministic encoding of reversal direction and is not claimed as verbatim source wording.

## Decision 3 — first qualifying closed reversal candle promotes maturity
The first subsequent qualifying closed reversal-direction candle is sufficient to promote:

`RAW EXTREME -> REVERSAL-CONFIRMED EXTREME`

provided the candidate has not already been structurally voided.

Operational meaning:
- no two-/three-candle minimum is added;
- later same-direction reversal candles may continue the reversal phase;
- REM/REE component maturity does not wait for an arbitrary minimum reversal count;
- standalone Extreme still requires the later retest stage.

### Evidence classification
**SOURCE-FAITHFUL ABSENCE OF A FIXED MINIMUM + MINIMAL DETERMINISTIC PROJECT MAPPING**.

## Decision 4 — structural reversal-phase continuation and anchor freeze
The project adopts:

`FIRST REVERSAL CONFIRMATION -> OPTIONAL CONTINUED REVERSAL PHASE -> STRUCTURAL RETEST BEGINS -> BODY/REFERENCE ANCHOR FREEZES -> RETEST EVALUATION`

Operational meaning:
- the provisional body/reference anchor may update while the same reversal phase continues;
- once price transitions into the retest phase, the anchor is frozen;
- after retest starts, the anchor must not drift with newer candles;
- no fixed reversal-phase candle count is imposed.

### Evidence classification
**SOURCE-DERIVED BODY/RETEST CONCEPT + SOURCE-INFERRED STRUCTURAL PHASE TRANSITION**.

## Decision 5 — deterministic retest-start trigger
Retest begins on the first closed candle whose close moves back toward the original Extreme/reference relative to the previous close.

Accepted predicate:
- SELL Extreme: first later closed candle with `CurrentClose > PreviousClose`;
- BUY Extreme: first later closed candle with `CurrentClose < PreviousClose`.

Additional rules:
- the trigger is evaluated on the same source timeframe;
- the trigger candle is the first retest-phase candle;
- the trigger candle is excluded from the completed reversal-phase anchor;
- candle colour alone is not the trigger;
- no previous-high/low breakout, fixed-N delay, EMA/Mid-BB condition, or actual anchor/MA5 touch is required merely to declare retest phase start;
- if accepted outside-BB/Momentum invalidation voids the Extreme first, the lifecycle is cancelled.

### Evidence classification
**SOURCE-DERIVED RETEST SEQUENCE + MINIMAL DETERMINISTIC PROJECT MAPPING**.

## Decision 6 — numeric frozen body-anchor mapping
The project adopts the **extreme body edge across the completed reversal phase** as the frozen body/reference anchor.

For each reversal-phase candle:
- `BodyTop = max(Open, Close)`
- `BodyBottom = min(Open, Close)`

Frozen anchor:
- SELL Extreme = highest `BodyTop` across the completed reversal phase;
- BUY Extreme = lowest `BodyBottom` across the completed reversal phase.

Guards:
- wick `High/Low` is not the numeric body anchor;
- the raw-Extreme candle is not automatically substituted for the reversal-phase body reference;
- the first retest-start candle is excluded;
- relevant MA5 remains a source-supported alternate/confluent retest reference and does not erase the frozen body anchor.

### Evidence classification
**DIRECT SOURCE BODY-REFERENCE CONCEPT + MINIMAL NUMERIC PROJECT MAPPING**.

## Decision 7 — standalone Extreme retest interaction validation
The project adopts **PRICE-RANGE/WICK INTERACTION WITH THE FROZEN BODY ANCHOR OR THE RELEVANT MA5 AREA IS SUFFICIENT TO COMPLETE THE STANDALONE EXTREME RETEST**, provided the Extreme has not been voided by the accepted outside-BB/Momentum rule.

Accepted operational rule:
- retest validation is evaluated only after the lifecycle has entered the retest phase under Decision 5;
- the frozen body anchor and the relevant MA5 are both source-supported retest references;
- body-anchor interaction is range-based, not close-only:
  - SELL Extreme: a candle can interact with the frozen SELL body anchor when its `High >= BodyAnchor`;
  - BUY Extreme: a candle can interact with the frozen BUY body anchor when its `Low <= BodyAnchor`;
- interaction with the relevant MA5 area is also eligible as a retest interaction under the accepted source wording;
- a wick/range touch is sufficient to prove that the reference area has been revisited; the project does **not** add a universal extra close-side confirmation, named candlestick pattern or second confirmation candle merely to call the retest complete;
- body anchor **and** MA5 are not both mandatory; no invented dual-touch/confluence requirement is added;
- accepted outside-BB/Momentum invalidation has priority: if the same completed candle/structure satisfies the established Extreme-void condition, the lifecycle becomes `VOID` rather than `RETEST/ENTRY-READY`;
- this decision concerns standalone Extreme retest maturity only and does not alter the earlier rule that REM/REE Extreme components need only be reversal-confirmed.

### Evidence classification
**DIRECT SOURCE RETEST-TARGET CONCEPT + MINIMAL PRICE-INTERACTION PROJECT MAPPING**.

Source support:
- Finale V04 identifies retest as the third condition for standalone Extreme entry;
- Finale V04 allows retest to revisit the marked body/reference or the relevant MA5;
- Finale V04 states that outside-BB close/Momentum behavior during or after attempted retest invalidates the Extreme interpretation.

The exact range predicates (`High >= anchor`, `Low <= anchor`) are deterministic software mappings of a source-described revisit/touch concept and are not claimed as verbatim Oma Ally formulas.

## Rejected alternatives
- raw Extreme alone as executable REM/REE component;
- reversal + retest required for every REM/REE Extreme component;
- mandatory previous-candle colour flip;
- mandatory named candlestick pattern;
- mandatory close-back-inside-BB for every reversal confirmation;
- waiting for eCSD/CSD before reversal confirmation;
- requiring two or more qualifying reversal candles before `REVERSAL-CONFIRMED`;
- fixed-N reversal-phase duration;
- indefinitely moving retest anchor;
- MA5-only anchor with body-reference discarded;
- first opposite-colour candle as mandatory retest-start trigger;
- waiting for actual anchor/MA5 touch before freezing the anchor;
- mandatory previous-high/low breakout for retest start;
- wick High/Low as the body anchor itself;
- first reversal candle body as the only possible final anchor;
- mandatory body-anchor + MA5 dual-touch;
- mandatory close-side confirmation after every retest touch;
- mandatory named reversal pattern at the retest.

## Remaining sub-specification before code
One final focused review remains:
- when frozen body anchor and relevant MA5 are materially separated, decide whether the **first valid interaction with either source-supported reference** completes retest, or whether one reference has priority;
- preserve outside-BB/Momentum invalidation as higher-priority void logic during that interaction.

No M08/Extreme lifecycle code patch is authorized until this final priority question is closed.
