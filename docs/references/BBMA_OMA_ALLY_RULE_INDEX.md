# BBMA Oma Ally - Page-Indexed Rule Digest

## Status
Supporting digest derived from the user-supplied `Oma ally BBMA - AL.pdf`.

This file is **not a replacement for the PDF**. It exists to make blueprint audits traceable by page. If this digest and the PDF ever disagree, the PDF takes precedence and the digest must be corrected.

## Page 1 - Indicator contract
- BBMA uses Moving Averages and Bollinger Bands.
- MA set: MA5 High, MA10 High, MA5 Low, MA10 Low, EMA50.
- Bollinger Band: period 20, deviation 2, shift 0, applied to Close.
- MA50 is used as an important trend/support-resistance reference.

## Page 2 - BBMA cycle
Operational sequence described by the reference:
1. Extreme forms.
2. Price moves toward MA5/MA10 or Mid BB for mandatory profit taking after an Extreme entry.
3. MLV structure forms and highest/lowest body is marked for possible retest.
4. Price indicates direction through eCSD/CSD behaviour, with CSD crossing MA5/10 and Mid BB.
5. Price retraces toward MA5 and a Re-Entry may be taken.
6. Price continues with CSM/momentum candles; additional Re-Entry opportunities may occur on retracement.
7. An opposite Extreme can mark cycle restart/reversal.

## Pages 5-6 - Extreme
- Extreme is a signal; MLV is a setup.
- An isolated Extreme does not by itself establish a trend reversal.
- Extreme is associated with MA5 or MA5/10 outside the relevant BB and reversal-candle behaviour.
- Extreme becomes void if candlesticks close outside the relevant Top/Low BB.
- Presence of CSM invalidates the Extreme context described by the reference.
- The reference describes four Extreme categories.

## Pages 7-8 - MLV and direction confirmation
- MLV normally forms after an Extreme.
- MLV is invalid/void when price breaks and closes outside the relevant Top/Low BB.
- Highest/lowest body marking is used because price may retrace for a retest.
- MLV may resemble double/triple-top or double/triple-bottom structures.
- eCSD crosses MA5/10; CSD crosses MA5/10 and Mid BB.
- CSD provides stronger directional intent and retracement toward MA5/10 is associated with Re-Entry opportunity.

## Page 9 - Re-Entry Type 1
- Re-Entry forms after a rise/fall and sideways/ranging behaviour.
- Uptrend context: MA5/10 High acts as resistance; sell Re-Entry is considered when price finds MA5/10 High and candlesticks remain below it.
- Downtrend context: MA5/10 Low acts as support; buy Re-Entry is considered when price finds MA5/10 Low and candlesticks remain above it.

## Page 10 - Re-Entry Types 2-4
### Type 2 - Powerful Re-Entry
- MA5/10 and Mid BB meet/collide.
- Strongest form includes MA50 in the confluence/collision.
- Minimum duration stated: 3 candles per timeframe (for example H1 = 3 hours, H4 = 12 hours, D1 = 3 days).

### Type 3 - CSM Re-Entry
- CSM forms first.
- Price then reverses/retraces toward MA5 or MA50, indicating a Re-Entry setup.

### Type 4 - CSD Re-Entry
- CSD forms first.
- Price then gyrates/retraces toward MA5/10.
- Downtrend example: CSD finds MA5/10 Low for buy Re-Entry context.
- Uptrend example: CSD finds MA5/10 High for sell Re-Entry context.

### Multi-timeframe note
- The reference explicitly instructs checking multiple timeframes.
- MA50 on the Daily chart is highlighted for trend confirmation/continuation-vs-reversal context.

## Pages 12-13 - REM / RRE / REE
- REM, RRE and REE are multi-timeframe setups formed from three components on three timeframes.
- REM example: Re-Entry on H4 + Extreme on H1 + MLV on M15.
- REE example: Re-Entry on D1 + Extreme on H4 + Extreme on H1.
- RRE example: Re-Entry on D1 + Re-Entry on H4 + Extreme on H1.
- Re-Entry trend direction should be checked against higher timeframes.
- Intraday guidance uses H4, H1 and M15 alignment.

## P0 audit rule
For P0 Step 3B, Type 2-4 implementation must be reconciled against the page-10 contracts above before those types are execution-eligible. No substitute confirmation rule may be invented merely to fit the current code.
