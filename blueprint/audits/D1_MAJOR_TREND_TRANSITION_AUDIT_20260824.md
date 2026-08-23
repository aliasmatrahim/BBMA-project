# D1 Major Trend / Transition Audit — 2026-08-24

## Scope
Determine the source-faithful D1 major-trend state and what is actually supported as a D1 trend reversal/transition before modifying EA code.

## Source findings

### Direct / strong source rules
1. Home Course: major trend is MA50.
2. Home Course: candle/price playing above MA50 means major trend BUY.
3. Home Course: MA50 functions properly at minimum Daily (D1); H4 does not carry major trend; if D1 says BUY and H4 says SELL, follow D1.
4. Home Course: a D1 momentum SELL candle means that day's market strength is SELL/falling; today's D1 close determines the next day's movement/context.
5. Oma Ally operational PDF: always confirm trend using MA50 on Daily. If price breaks MA50 it indicates trend reversal; failure to break MA50 indicates trend continuation. MA50 acts as support/resistance.
6. The same PDF also contains a stricter descriptive trend statement: above MA50 with MA50 ascending = bull; below MA50 with MA50 descending = bear.

## Important distinction
The source supports two related but non-identical concepts:
- MAJOR-TREND SIDE / CONTEXT: D1 price relative to MA50.
- CONFIRMED / CLEAN TREND CONDITION: price side plus MA50 direction/slope.

A single close marginally crossing MA50 is not sufficiently specified by the source as a universal Boolean handover formula. The phrase "break MA50" is structurally meaningful, but the sources do not define an exact numeric break tolerance, number of closes, candle-body percentage, or fixed confirmation count.

## What must NOT be invented
Do not add any of the following as Oma Ally Core unless separately approved as project mapping:
- fixed pip buffer around MA50;
- ATR/ADX filter;
- mandatory 2 or 3 D1 closes beyond MA50;
- fixed MA50 slope threshold;
- intraday/H4 cross of MA50 as major-trend handover;
- treating one H4 counter-direction setup as a D1 major-trend reversal.

## Recommended deterministic architecture
Use a state model rather than `Close > MA50 = BUY` / `Close < MA50 = SELL` as the whole concept:

- `D1_MAJOR_BUY`: closed D1 price is above MA50; strongest/clean confirmation when MA50 is also ascending.
- `D1_MAJOR_SELL`: closed D1 price is below MA50; strongest/clean confirmation when MA50 is also descending.
- `D1_TRANSITION`: price has crossed/broken to the opposite side while MA50 direction/structural confirmation is not yet aligned or the evidence is conflicting.

For execution gating, do not silently choose how `D1_TRANSITION` behaves until explicitly reconciled. Conservative choices include blocking new counter-major entries during transition or retaining the last confirmed major-trend owner until a clean opposite state is confirmed. This behavior is PROJECT POLICY, not directly specified by Oma Ally.

## Current EA implication
Current source already defines D1 as `TIMEFRAME_TREND = 1440` and EMA50 period 50, but the new Home Course evidence changes the required semantic authority: D1 major trend must sit above H4 local setup direction. Before code modification, locate every existing trend/owner/entry gate and ensure D1 major authority is introduced without changing REM/RRE/REE signatures.

## Status
SOURCE AUDIT COMPLETE.
CODE CHANGE: NOT YET AUTHORIZED/IMPLEMENTED.
NEXT: audit current EA call sites and choose deterministic `D1_TRANSITION` execution policy before implementation.
