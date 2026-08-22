# CORE-V2-F2 — Extreme Maturity inside REM / REE

Date: 2026-08-22
Status: **PARTIALLY RESOLVED — MATURITY + REVERSAL-DIRECTION + FIRST-QUALIFYING-CANDLE PROMOTION USER APPROVED; REVERSAL-PHASE ANCHOR/RETEST TRANSITION STILL PENDING**
Branch: `blueprint-dev`

## Decision 1 — Extreme maturity inside REM / REE
For an Extreme to be eligible as a component of an executable REM or REE combination, it must be at least **reversal-confirmed**.

A standalone Extreme entry remains a different maturity level and requires the later **retest** entry stage.

Operational maturity distinction:

`RAW EXTREME -> REVERSAL-CONFIRMED EXTREME -> RETEST/ENTRY-READY EXTREME`

- RAW EXTREME: MA5/MA10 outside the relevant outer BB under the strict accepted detector rule. Not sufficient for executable REM/REE.
- REVERSAL-CONFIRMED EXTREME: raw Extreme plus source-valid reversal confirmation. Eligible as an Extreme component of REM/REE.
- RETEST/ENTRY-READY EXTREME: reversal-confirmed Extreme plus the later retest. Required for standalone Extreme entry eligibility.

### Evidence classification
This maturity decision is **SOURCE-INFERRED / STRONG HINT**, not an explicit verbatim Oma Ally rule for REM/REE component maturity.

Evidence:
- Finale V04 00:27:23–00:31:55 distinguishes raw Extreme condition, reversal confirmation and retest, and states that the retest is the point of standalone Extreme entry.
- Finale V05 00:46:16–00:53:55 teaches higher-timeframe Re-Entry being completed/read through lower-timeframe Extreme/MHV/direction structures, supporting a distinction between supporting Extreme context and standalone Extreme entry.
- Finale V05 00:54:12–00:54:40 mentions some Extreme occurrences embedded in higher-timeframe Re-Entry context behaving differently from normal standalone Extreme TP-Wajib treatment; this remains HOLD for TP semantics but reinforces that MTF component use is not identical to standalone Extreme entry.

## Decision 2 — minimal deterministic reversal-direction mapping
The project adopts **DIRECTIONAL REVERSAL CANDLE / REVERSAL PHASE** as the minimum deterministic interpretation of the source requirement for a reversal candle after RAW Extreme.

Accepted mapping:
- after a valid RAW Extreme, reversal confirmation must come from one or more **closed candles on the same source timeframe** that show movement away from the Extreme direction;
- for a SELL Extreme, a qualifying reversal-direction candle is bearish: `Close < Open`;
- for a BUY Extreme, a qualifying reversal-direction candle is bullish: `Close > Open`;
- the previous candle is **not** required to have the opposite colour merely to manufacture a two-candle colour-flip pattern;
- no named candlestick pattern such as engulfing, pin bar, hammer, morning/evening star or similar is required unless future source evidence explicitly establishes it;
- reversal confirmation must not be reduced to a fixed one-candle or two-candle template because the source allows reversal-candle behaviour to span more than one candle;
- closing back inside the Bollinger Band is **supporting/preferred evidence**, not a universal hard requirement, because Finale V04 describes it as preferable and V05 contains nuance around a reversal candle that may remain outside BB while closing inside the relevant MA5;
- the accepted strict Extreme detector rule itself is unchanged; the HOLD around touch-only Extreme and outside-BB-but-inside-MA5 universal acceptance remains unresolved;
- if the candidate becomes source-valid Momentum/CSM or otherwise satisfies the accepted outside-BB Extreme invalidation rule before reversal confirmation is established, the RAW Extreme candidate is void rather than being promoted to reversal-confirmed.

### Evidence classification
This reversal contract is **DIRECT SOURCE REQUIREMENT + MINIMAL DETERMINISTIC PROJECT MAPPING**.

Direct source support:
- the primary reference requires reversal-candle behaviour as part of Extreme and does not prescribe a named candlestick pattern;
- the primary wording allows reversal candles to involve more than a fixed one/two-candle pattern;
- Finale V04 explicitly identifies a reversal candle as the second Extreme condition and says closing inside BB is preferable rather than a universal mandatory condition;
- Finale V05 preserves nuance that an outside-BB reversal may still matter if it has moved inside the relevant MA5, while a structure that remains outside/beyond MA5 and behaves as Momentum invalidates the Extreme interpretation.

The exact software mapping `SELL: Close < Open` / `BUY: Close > Open` is intentionally the smallest deterministic encoding of reversal direction. It is not claimed as a verbatim Oma Ally Boolean formula.

## Decision 3 — first qualifying closed reversal candle promotes maturity
The project adopts **FIRST QUALIFYING CLOSED REVERSAL-DIRECTION CANDLE IS SUFFICIENT TO PROMOTE `RAW EXTREME -> REVERSAL-CONFIRMED EXTREME`**.

Accepted operational rule:
- once a valid RAW Extreme exists, the first subsequent closed candle on the same source timeframe that satisfies the accepted reversal direction (`SELL: Close < Open`, `BUY: Close > Open`) promotes the Extreme to `REVERSAL-CONFIRMED`, provided the candidate has not already been voided by the accepted outside-BB/Momentum invalidation rule;
- the project does **not** require two consecutive reversal candles, three candles, a named candlestick pattern, a Mid-BB/EMA condition, or eCSD/CSD before this maturity promotion;
- additional same-direction reversal candles may continue the broader reversal phase, but REM/REE component maturity does not wait for an arbitrary minimum number of reversal candles once the first qualifying closed reversal candle has validly confirmed reversal direction;
- this decision affects **maturity timing**, not the later standalone Extreme retest requirement;
- standalone Extreme remains non-entry-ready until its later retest contract is satisfied;
- if the RAW candidate is structurally invalidated before the first qualifying reversal-direction candle closes, it is void and cannot be promoted by a later candle as though the original Extreme were still active.

### Evidence classification
This rule is **SOURCE-FAITHFUL ABSENCE OF A FIXED MINIMUM + MINIMAL DETERMINISTIC PROJECT MAPPING**.

The sources clearly separate RAW Extreme, reversal confirmation and later retest, but do not impose a universal two-/three-candle minimum before reversal confirmation exists. Therefore the first qualifying closed reversal-direction candle is the minimal deterministic promotion point, while any subsequent multi-candle reversal behavior is handled as lifecycle continuation rather than a prerequisite to basic reversal-confirmed maturity.

## Rejected alternatives
- Raw Extreme alone as executable REM/REE component: rejected as too immature relative to the accepted Extreme lifecycle.
- Reversal + retest required for every REM/REE Extreme component: rejected because the source ties retest specifically to standalone Extreme entry and does not clearly require it for supporting MTF components.
- Disable REM/REE indefinitely: rejected as a safety-only engineering choice, not the selected Core interpretation.
- Previous-candle colour flip as the mandatory reversal algorithm: rejected as an invented pattern not stated by the source.
- Mandatory named candlestick pattern: rejected as unsupported.
- Mandatory close-back-inside-BB for every reversal candle: rejected as stricter than the accepted source wording.
- Waiting for eCSD/CSD before calling Extreme reversal-confirmed: rejected because direction confirmation is a later BBMA cycle stage, not the Extreme reversal-candle stage itself.
- Requiring two or more qualifying reversal candles before `REVERSAL-CONFIRMED`: rejected because the source provides no universal minimum count for this stage.

## Remaining sub-specification before code
The reversal **direction** and basic maturity-promotion point are now locked. One focused lifecycle review remains before M08/Extreme lifecycle code is patched:
- when the multi-candle reversal phase stops extending the highest/lowest body reference;
- which body reference is frozen for the later retest when reversal spans multiple candles;
- when the lifecycle transitions from reversal-confirmed into the later retest phase without moving the reference indefinitely;
- how the existing outside-BB/Momentum invalidation is applied during that transition.

Until the reversal-phase anchor/retest-transition details are closed, active Mode 2 REM/REE cannot yet be declared fully Core-V2-compliant merely because a raw M08 Extreme plus one colour condition is present.
