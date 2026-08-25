# C044 Post-Re-Entry Failed-Momentum TP Lifecycle Decision — 2026-08-26

Branch: `d1-owner-dev`

## Status
**APPROVED / PARTIAL ACCEPT / POST-REENTRY FAILED-MOMENTUM TP LIFECYCLE / GUARANTEED REVERSAL REJECTED / NO MQL4 CHANGE YET**

## Decision
The previous broad C044 HOLD is narrowed.

Accepted bounded interpretation:
- a valid Direction/CSD context must already exist;
- a valid Re-Entry must then form and own the continuation lifecycle;
- the post-Re-Entry move must progress to / test the direction-side outer Bollinger Band;
- if, on a fully closed candle, that outer-BB continuation attempt fails to produce source-valid Momentum/CSM, the continuation is treated as failed and TP/close of the existing lifecycle position is source-supported;
- this is an exit/TP lifecycle rule, not authority for an automatic opposite-direction entry.

Canonical bounded sequence:

`VALID DIRECTION -> VALID RE-ENTRY -> CONTINUATION TO/TEST OF DIRECTION-SIDE OUTER BB -> NO SOURCE-VALID MOMENTUM ON CLOSED CANDLE -> POST-REENTRY CONTINUATION FAILURE -> TP/CLOSE EXISTING POSITION`

Source-valid Momentum remains governed by the accepted Core rule:

`close outside relevant outer BB + expanding/directional BB state`

## Explicitly rejected
This decision must not be interpreted as:
- `first candle after Re-Entry is not Momentum => immediate close`;
- a one-candle timer for declaring no-Momentum;
- `no Momentum => guaranteed reversal`;
- `no Momentum => automatic opposite BUY/SELL`;
- bypassing opposite-trade Extreme/MHV/CSD/Re-Entry requirements;
- disabling broker hard SL, emergency protection or portfolio/risk controls;
- silently replacing current static TP architecture before separate implementation reconciliation.

## Relationship to C035
C035 governs the earlier pre-Re-Entry stage:
- strong direction reaches outer BB before Re-Entry/no Momentum -> outer-BB touch alone does not force TP; continue observing for Re-Entry.

C044 governs the later post-Re-Entry stage:
- Direction -> Re-Entry -> continuation reaches/tests outer BB -> no canonical Momentum -> TP/close lifecycle.

The two rules must not be merged.

## Reversal interpretation
Source wording may describe the market as reversing after no-Momentum. For executable governance, this is constrained to:
- continuation failure;
- elevated reversal risk / cycle-transition context.

It is **not** encoded as a deterministic or guaranteed reversal law. A new opposite trade still requires its own source-valid setup/entry authority.

## Source basis
- Home Course HC-P10-010: MHV -> direction -> Re-Entry -> no Momentum => mandatory TP.
- Home Course HC-P16-003: Direction -> Re-Entry -> no Momentum => close position; market expected to reverse.
- Home Course HC-P13-013 provides the stronger structural context of strong direction -> Re-Entry -> outer BB without Momentum before later reverse/retest structure.
- Accepted Core/Finale governance requires closed-candle Momentum classification and rejects literal qualitative absolutes such as guaranteed reversal.
- External/community BBMA material is corroboration only and does not outrank project source governance.

## Classification
- post-Re-Entry failed-Momentum TP/close lifecycle: **SOURCE-SUPPORTED / ACCEPTED WITH BOUNDED EVENT-BASED SCOPE**;
- one-candle no-Momentum timeout: **REJECTED / NOT AUTHORIZED**;
- guaranteed reversal: **REJECTED**;
- automatic opposite entry: **REJECTED**.

## Current EA / TP architecture impact
Current v4.52 still retains static Re-Entry-owned outer-BB broker TP as a project execution-policy payload. This C044 decision does not by itself alter that implementation.

A later TP-architecture reconciliation is required to decide coexistence/precedence among:
- current static outer-BB broker TP;
- C044 lifecycle close after failed Momentum;
- any future lifecycle-only TP model.

Until that implementation decision is explicitly approved:
- do not remove static TP;
- do not add dynamic C044 close logic;
- do not change M23/M24 ownership;
- do not change MinRR reward semantics.

## Change control
Strategy-spec decision only. No MQL4 source change is authorized by this record alone.
