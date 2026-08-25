# CORE-V2-F7 — Deterministic No-Momentum Exit Resolution Audit

> **2026-08-25 EXECUTABLE-PRECEDENCE NOTICE**
> This document is retained as historical/provisional evidence reconstruction. Where it treats post-Re-Entry no-Momentum, re-arm, hold/no-TP, or related lifecycle-close behavior as executable/source-spec `RESOLVED`, that promotion is superseded by `docs/references/HOME_COURSE_19P_CROSS_SOURCE_RECONCILIATION_20260825.md`, `docs/references/HOME_COURSE_49_FAMILY_CORE_REVALIDATION_20260825.md`, and the current authoritative Strategy Core. Those material lifecycle behaviors remain HOLD unless a later explicit strategy decision reopens them. No EA execution authority may be derived from the superseded conclusion alone.

Date: 2026-08-24  
Branch: `blueprint-dev`  
Scope: post-Re-Entry Momentum / no-Momentum lifecycle close trigger  
Status: **AUDIT COMPLETE — EVENT CLASS RESOLVED FOR A RE-ENTRY-OWNED POSITION; COMBINATION OWNER ROUTING REMAINS UNRESOLVED; NO EA CODE CHANGE**

## 1. Question

After a valid BBMA Re-Entry has produced an open position, at what source-owned event may the EA legitimately conclude that the expected continuation Momentum failed to appear and the position should be closed, without inventing a fixed candle count, timer, session timeout, pip threshold, ATR/ADX rule, or other non-BBMA heuristic?

This audit resolves only the **event/candle class**. It does not authorize changing the frozen P3 runtime candidate.

## 2. Governance / preflight

Applied project order:

`Original Evidence -> Canonical Strategy Core -> Contracts -> Current lifecycle ownership`

Relevant live contracts/state:
- `M10_DIRECTION_MOMENTUM_SOURCE_CONTRACT.md` — source-valid CSM producer;
- `M12_REENTRY_SOURCE_CONTRACT.md` — source-timeframe Re-Entry confirmation;
- `CORE_V2_F6_TIMING_VERIFICATION_AUDIT.md` — first closed Re-Entry candle validates; immediately following source-TF candle is the live entry window;
- `M23_POSITION_LIFECYCLE_CONTRACT.md` — broker-side owner for already-open positions; dynamic BBMA close requires a separately approved source-owned closed-candle mapping;
- Path A strict provenance remains active.

## 3. Workbook evidence

Source: user-supplied `333531988-BBMA-Home-Course.pdf` (Tier-B strong-provenance copy under the prior authentication audit).

### 3.1 Momentum/no-Momentum definition

Workbook Lesson 6 establishes:
- candle close outside the relevant outer BB = Momentum;
- if no candle closes outside Top/Low BB, there is no Momentum;
- no Momentum is associated with market changing direction.

Under current project governance, this raw workbook statement is reconciled through the canonical M10 rule: a source-valid directional CSM requires the outer-BB close **plus** the already accepted expanding/directional BB state. Therefore F7 must reuse M10 and may not create a second, weaker Momentum detector.

### 3.2 Direct post-Re-Entry close rule

Workbook Lesson 11 states the lifecycle directly:

`Arah -> Re-Entry -> Momentum`

and:

`Arah -> Re-Entry -> Tiada Momentum -> Close position, market akan reverse.`

It separately states:

`Arah -> Tiada Re-Entry -> hold position, tunggu Re-Entry.`

Therefore the no-Momentum close window cannot start before a valid Re-Entry has actually completed.

### 3.3 Structural confirmation after no Momentum

Workbook Re-Entry material provides the key deterministic clue:

- after strong direction gives a Re-Entry and the continuation does **not** produce Momentum, the teaching says to wait for a **confirmation reverse candle** that kills the attempted move, then the next setup is read from the retest;
- the summary repeats that after Re-Entry, no Momentum means the market rotates, while Momentum means continuation and another Re-Entry.

This is stronger than an absence-only rule and avoids inventing `N` candles.

### 3.4 MHV next-candle wording is context-specific

Lesson 8 says, for the MHV position context, to inspect the next candle: outside-BB close means Momentum/hold; inside-BB close means close because price is expected to reverse.

This is **not** promoted as a universal Re-Entry `next candle or exit` rule because the wording is attached to MHV management, while the Re-Entry sections use a structural `no Momentum -> reverse confirmation -> rotation` sequence. Therefore the project must not force a one-candle timeout onto all Re-Entry positions.

## 4. Primary / secondary PDF reconciliation

Primary `Oma ally BBMA - AL.pdf` establishes:

`... CSD/direction -> Re-Entry -> Momentum/CSM -> further Re-Entry -> opposite Extreme / cycle restart`.

It says that after the Re-Entry retracement, price should travel in the intended direction and create Momentum candles until Momentum diminishes; once trend/Momentum ends, the next cycle/reversal develops.

This corroborates:
- Momentum as the expected continuation state after Re-Entry;
- failure/end of Momentum as a structural transition, not a timer;
- opposite-cycle evidence as later confirmation of reversal.

The secondary PDF corroborates the BBMA Momentum law through outer-BB close plus vertical/expanding BB context and provides no fixed post-Re-Entry candle timeout.

## 5. Finale V05 / V06 reconciliation

V05/V06 strongly corroborate:
- direction signal is not the entry;
- Re-Entry is the actual setup/entry stage;
- Momentum follows Re-Entry in the cycle;
- Momentum can generate further Re-Entry opportunities;
- higher/lower timeframe relationships must be respected.

They do not provide a universal `after exactly X candles without CSM, close` rule. F6 also proves that the validation candle and live entry candle are distinct, so evaluating the already-closed validation candle as a post-entry no-Momentum failure would be temporally wrong.

## 6. Deterministic resolution

### DNM-01 — Start of observation window

**RESOLVED.**

The no-Momentum lifecycle window begins only after:

1. a valid Re-Entry is confirmed on its source timeframe;
2. the broker position has actually been opened from that Re-Entry;
3. subsequent **closed candles of the owning Re-Entry timeframe** become available.

The Re-Entry validation candle itself is not a post-entry no-Momentum observation candle.

No fixed expiry is introduced.

### DNM-02 — Continuation success event

**RESOLVED.**

If a later closed candle establishes a **same-direction source-valid CSM under the canonical M10 contract**, continuation is confirmed.

State transition:

`RE_ENTRY_OPEN / MOMENTUM_PENDING -> SAME_DIRECTION_CSM -> MOMENTUM_CONFIRMED`

The no-Momentum failure window for that Re-Entry is then closed. Future lifecycle follows normal Momentum -> Re-Entry progression rather than the initial post-Re-Entry failure rule.

### DNM-03 — No-Momentum is not declared by elapsed candles

**RESOLVED.**

The EA must **not** declare no Momentum merely because:
- the immediately next candle is not CSM;
- two or three candles pass;
- a fixed number of minutes/hours passes;
- price fails to travel a fixed pip distance;
- BB width is below an arbitrary threshold.

Absence alone has no deterministic deadline in the reconciled source set.

### DNM-04 — Executable failure event

**RESOLVED AS A MINIMAL SOURCE-DERIVED DETERMINISTIC MAPPING.**

For a position whose owning Re-Entry timeframe is known, the first executable `NO_MOMENTUM -> CLOSE` event is:

> **the first later fully closed source-timeframe reverse-direction confirmation candle that occurs while no same-direction source-valid CSM has appeared since the Re-Entry position was opened.**

Directional mapping reuses the already accepted source-derived BBMA reversal-candle convention:
- BUY position: reverse confirmation candle is bearish, `Close < Open`;
- SELL position: reverse confirmation candle is bullish, `Close > Open`.

The candle must be evaluated only after it closes. This is a lifecycle confirmation event, not a live intrabar guess.

Why this is the minimum supported mapping:
- workbook directly says post-Re-Entry no Momentum -> close / market reverses;
- workbook specifically says, in the no-Momentum Re-Entry example, wait for the **confirmation reverse candle** that kills the attempted move;
- primary PDF/Finale support Re-Entry -> Momentum as the expected continuation sequence;
- no source requires an arbitrary N-candle delay;
- no source requires waiting all the way for an opposite Extreme merely to recognize the failed initial continuation.

Evidence classification:
- `post-Re-Entry no Momentum -> close/rotation` = **DIRECT / REPEATED WORKBOOK RULE + STRONG CYCLE CORROBORATION**;
- `confirmation reverse candle` as the structural failure event = **DIRECT WORKBOOK CLUE**;
- exact Boolean `BUY: Close<Open`, `SELL: Close>Open` = **MINIMAL DETERMINISTIC PROJECT MAPPING reusing the already approved reversal-direction convention**, not claimed as verbatim universal wording.

### DNM-05 — Opposite Momentum has priority

**RESOLVED.**

If, before same-direction Momentum is confirmed, a later closed candle forms **source-valid opposite CSM/Momentum**, this is stronger than simple no-Momentum failure and must be treated as immediate thesis invalidation/close once lifecycle routing is implemented.

It must not be mislabeled as merely `no Momentum`.

### DNM-06 — Neutral / same-direction inside-BB candles

**RESOLVED CONSERVATIVELY.**

A neutral candle, doji, or same-direction candle that does not qualify as CSM does not by itself authorize a close.

The position remains in `MOMENTUM_PENDING` until one of the structural events occurs:

1. same-direction CSM -> continuation confirmed; or
2. reverse-direction confirmation before same-direction CSM -> no-Momentum failure / close; or
3. source-valid opposite CSM -> stronger invalidation / close.

This avoids inventing a timer while preserving the workbook's requirement that no-Momentum failure must become a structural rotation/reversal, not merely an elapsed absence.

## 7. Timeframe ownership boundary

### Standalone H1 Re-Entry

For the currently approved standalone H1 Re-Entry path, the owning Re-Entry timeframe is H1. Therefore the future lifecycle event is evaluated on **closed H1 candles**, while M15 may remain the orchestration clock that notices the new closed H1 candle.

### REM / RRE / REE

This audit does **not** automatically certify the current M17 assumption that:
- REM exit owner = H4 Re-Entry;
- RRE/REE exit owner = D1 Re-Entry.

The source supports multi-timeframe Re-Entry ownership conceptually, but exact lifecycle-exit ownership for the combination setup must be resolved separately under Path A before the new dynamic close rule is applied to REM/RRE/REE.

Therefore:
- deterministic event class = resolved;
- combination-specific owner timeframe = **HOLD / UNRESOLVED**.

## 8. Architecture implication

The resolved rule is a **post-entry lifecycle exit**, not an initial static TP-price builder.

Ownership implication:
- M10 remains sole CSM/Momentum producer;
- M12 remains Re-Entry setup/confirmation owner;
- M23 remains broker-side close owner for open positions;
- the lifecycle state must be advanced only on new closed candles of the owning Re-Entry timeframe;
- M23 must consume source-owned lifecycle evidence rather than recreate M10 or M12 strategy semantics independently;
- M17 initial protective SL/TP logic is not modified by this audit;
- M24 recovery must eventually reconstruct the lifecycle state (`MOMENTUM_PENDING` / `MOMENTUM_CONFIRMED`) if this rule is implemented across restart.

A separate M23/M24 integration contract update is required before coding.

## 9. Effect on Path A / F7

This audit materially narrows F7:

### Resolved
- Re-Entry continuation expectation = Momentum/CSM;
- no fixed candle/time timeout is allowed;
- post-Re-Entry failure becomes executable only on structural reversal confirmation before same-direction CSM;
- same-direction CSM confirms continuation;
- opposite CSM is stronger invalidation;
- standalone H1 event timeframe = H1.

### Still unresolved
- REM/RRE/REE lifecycle owner timeframe / source component for this exit rule;
- whether any static non-Extreme TP price should coexist with the dynamic lifecycle exit;
- universal Re-Entry hard-SL provenance beyond current `EA_SAFETY`;
- exact recovery/persistence fields for the future lifecycle state.

The current static outer-BB M17 TP mapping remains **not production-certified as Strategy Core** by this audit.

## 10. Runtime freeze

**NO EA CODE CHANGE NOW.**

The current P3 runtime candidate remains frozen so pending P3 runtime evidence stays attributable to the same build.

If this lifecycle rule is later integrated, it must be a new build with:
1. canonical Core/spec update;
2. M23/M24 lifecycle ownership contract update;
3. build/header identifier update;
4. implementation patch;
5. static cross-module/purity audit;
6. native MetaEditor 0E0W compile;
7. fresh runtime tests including positive/negative no-Momentum traces and restart recovery.

## 11. Final verdict

**Deterministic No-Momentum Exit verdict:**

`VALID RE-ENTRY POSITION OPEN`

`-> MOMENTUM_PENDING`

`-> SAME-DIRECTION SOURCE-VALID CSM`  
`   => CONTINUATION CONFIRMED / DO NOT CLOSE UNDER INITIAL NO-MOMENTUM RULE`

`OR`

`-> FIRST LATER CLOSED REVERSE-DIRECTION CONFIRMATION BEFORE SAME-DIRECTION CSM`  
`   => NO-MOMENTUM FAILURE CONFIRMED / CLOSE POSITION`

`OR`

`-> SOURCE-VALID OPPOSITE CSM`  
`   => STRONGER THESIS INVALIDATION / CLOSE POSITION`

No fixed candle count, elapsed-time rule, fixed pip distance or new indicator is introduced.

**Event class is resolved for a known Re-Entry owner. Combination-specific owner routing remains HOLD. Code remains unchanged while P3 runtime evidence is pending.**