# C006 Horizontal-BB Compression Decision — 2026-08-25

Branch: `d1-owner-dev`

## Status
**APPROVED / PARTIAL ACCEPT / COMPRESSION PRINCIPLE ACCEPTED / FIXED 10–20 PIP THRESHOLD REJECTED**

## Decision
The previous broad C006 HOLD is narrowed.

Accepted bounded interpretation:
- flat/horizontal Bollinger Bands may represent a compression / low-momentum context;
- prolonged/narrow compression may precede later BB expansion and a large move;
- compression itself does not determine BUY/SELL direction;
- direction/momentum authority still requires the approved BBMA condition: a valid outside-outer-BB close together with expanding/directional BB state;
- no direct entry is authorized merely because BB is narrow or flat.

## Fixed 10–20 pip wording
The Home Course wording that a horizontal BB width of roughly 10–20 pips precedes a large breakout is retained as historical/source evidence but is **rejected as a universal executable threshold** because:
- the primary PDF / accepted Finale layer does not establish 10–20 pips as a universal BBMA Core law;
- pip width is instrument-, price-scale- and timeframe-dependent;
- one fixed pip range cannot safely govern all approved FX pairs/timeframes.

## Source-consistent operational interpretation
Canonical sequence remains:

`BB FLAT / HORIZONTAL -> COMPRESSION CONTEXT -> wait for CLOSED CANDLE -> BB EXPANDING/DIRECTIONAL + valid outside-BB close -> MOMENTUM/CSM -> existing BBMA lifecycle`

This decision must not be interpreted as:
- `BB_FLAT => BUY`;
- `BB_FLAT => SELL`;
- `BB_FLAT => Extreme`;
- `10–20 pips => guaranteed breakout`;
- compression itself as an entry/exit/TP/SL authority.

## Optional diagnostic note
If a future observability-only compression metric is desired, a normalized BB-width/BandWidth-style measure may be researched as diagnostics/context only. It must not silently become entry authority or replace the accepted BB-state/Momentum contract without a separate decision.

## Classification
- flat/narrow BB compression principle: **SOURCE-SUPPORTED CONTEXT / ACCEPTED**;
- later expansion potential: **SOURCE-SUPPORTED CONTEXT / ACCEPTED**;
- universal 10–20 pip threshold: **REJECTED FROM UNIVERSAL EXECUTABLE CORE**;
- direction prediction or standalone execution from compression: **NOT AUTHORIZED**.

## Change control
Documentation/strategy-spec decision only. No MQL4 source change is authorized by this decision alone.
