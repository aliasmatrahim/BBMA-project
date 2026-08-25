# GAP-A1 — D1O EXTREME_TPW Lifecycle Exit Decision — 2026-08-26

Branch: `d1-owner-dev`
Status: **APPROVED STRATEGY/EXECUTION DECISION / SOURCE-CONTRACT GAP CLOSED / IMPLEMENTATION PENDING**

## Decision

For `D1_OPP_EXTREME_TPW`, use a **lifecycle-managed D1 TP-Wajib exit** rather than a frozen static MA price or the LTF Re-Entry outer-BB TP.

Canonical ownership split:

- fresh LTF Re-Entry = execution/dedup identity and structural hard-SL owner;
- D1 Extreme = TP-Wajib semantic owner;
- D1 Opportunity family/cycle = attribution + lifecycle metadata;
- M15 remains final entry authority;
- M23 owns broker full-position close after a canonical TP-Wajib completion event;
- M24 owns persistence/recovery;
- M20 emergency protection retains precedence.

## TP-Wajib completion event

Use the existing canonical dynamic D1 completion semantics already embodied in `D1OpportunityTPWCompletedSince()`:

- source Extreme must be mature/reversal-confirmed and valid;
- only fully closed D1 candles after the Extreme confirmation are evaluated;
- Extreme SELL journey completes normal TP-Wajib when a later closed D1 candle range reaches either current D1 MA5 Low or MA10 Low;
- Extreme BUY journey completes normal TP-Wajib when a later closed D1 candle range reaches either current D1 MA5 High or MA10 High;
- first qualifying opposite MA5/MA10 interaction completes the normal TP-Wajib objective;
- Mid BB remains farther/maximum context and is not required after the first normal TP-Wajib completion.

This preserves the dynamic nature of the MA objective. No arbitrary frozen MA5/MA10 price is manufactured at entry.

## Broker payload

For an `EXTREME_TPW`-managed D1 Opportunity trade:

- retain the approved hard structural SL from the exact LTF Re-Entry source;
- broker TP = `0` / absent;
- close the full position through the lifecycle owner when canonical D1 TP-Wajib completion is observed;
- no partial close, trailing stop, TP2 or TP3 is introduced.

Classification:
- underlying Extreme TP-Wajib = `[BBMA-ORIGINAL]`;
- D1-to-LTF opportunity family = `[BBMA-SOURCE-CONSISTENT][PROJECT-EXTENSION]`;
- lifecycle `TP=0` broker implementation = `[PROJECT-EXTENSION][ENGINEERING-ONLY]`.

## MinRR

Because the dynamic lifecycle has no fixed reward coordinate at entry:
- `MinRRRatio == 0` -> may proceed subject to all other gates;
- `MinRRRatio > 0` -> fail closed for `EXTREME_TPW` lifecycle-managed entries unless a future approved deterministic reward reference is added.

Do not retain the LTF outer-BB TP merely to manufacture an RR value.

## Persistence / recovery

The open trade must preserve enough immutable identity to recover safely:
- D1 Opportunity family = `D1_OPP_EXTREME_TPW`;
- D1 Extreme direction;
- D1 Extreme confirmation/source candle time;
- D1 opportunity CycleID / source attribution;
- selected LTF Re-Entry source identity for hard SL and execution lineage;
- last processed fully closed D1 candle for TP-Wajib lifecycle evaluation;
- exit-latched/idempotency state.

Missing/ambiguous recovery identity -> fail frozen; never fabricate a TP owner.

## Idempotency

One canonical D1 TP-Wajib completion event may produce at most one broker close for the position. Repeated M15 processing cycles or restart replay must not issue duplicate closes.

## Relationship to C044

`EXTREME_TPW` lifecycle is **not C044**.

- C044 manages Re-Entry continuation/failure using the selected Re-Entry owner timeframe.
- `EXTREME_TPW` manages the normal D1 Extreme TP-Wajib objective using D1 as TP owner.
- A trade must have one normal strategy lifecycle exit owner at a time.
- `D1_OPP_EXTREME_TPW` uses this TPW lifecycle, not the generic C044 lifecycle.

## Non-authority

This decision does not:
- make raw Extreme executable;
- create a fifth BBMA original setup;
- change REM/RRE/REE;
- change D1O execution hash ownership;
- change M15 final entry authority;
- change lot sizing ownership;
- weaken hard SL or M20 emergency protection;
- assert that the D1O family itself is verbatim original Oma Ally nomenclature.

## Closure verdict

The material strategy choice that previously blocked GAP-A1 is now resolved:

`D1 EXTREME_TPW OPPORTUNITY -> LTF RE ENTRY IDENTITY + HARD SL -> TP=0 -> CLOSED-D1 DYNAMIC OPPOSITE MA5/MA10 TPW COMPLETION -> M23 FULL CLOSE`.

Remaining work is implementation/static/native/runtime validation only; there is no remaining Core/strategy ambiguity in GAP-A1.
