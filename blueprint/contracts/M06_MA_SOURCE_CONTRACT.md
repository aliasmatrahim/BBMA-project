# M06 BBMA Moving-Average Source Contract

## Status
P0 Step 3C source-alignment contract for Module 06.

The user-supplied BBMA PDFs govern BBMA strategy semantics. The primary operational reference identifies the five BBMA moving averages. The secondary reference contains MT4 setup diagrams that expose the exact MA method/applied-price settings.

## Source-derived indicator contract

### Primary operational reference
`Oma ally BBMA - AL.pdf`, page 1 defines five moving averages:
- MA5 High
- MA10 High
- MA5 Low
- MA10 Low
- Exponential MA50

The same page distinguishes two High MAs, two Low MAs and one exponential MA, and uses MA50 as an important trend/support-resistance reference.

### Secondary setup diagrams
`BBMA technique.pdf`, pages 11-14 show the MT4 parameters used to construct the BBMA MA set:
- MA5 High: Period 5, Linear Weighted, Apply to High.
- MA5 Low: Period 5, Linear Weighted, Apply to Low.
- MA10 High: Period 10, Linear Weighted, Apply to High.
- MA10 Low: Period 10, Linear Weighted, Apply to Low.
- MA50: Period 50, Exponential, Apply to Close.

## Rejected old producer behaviour
Before Step 3C, `CalculateAllMA()` called the generic `SMA()` helper for all four MA5/10 lines. `SMA()` reads only `iClose()`. That made MA5 High and MA5 Low numerically identical for the same period, and likewise MA10 High and MA10 Low, which violates the BBMA High/Low MA distinction.

The old custom `EMA()` also iterated the exponential recurrence from the newest requested candle toward older candles. This reverses the chronological direction expected by an EMA recurrence.

## Locked M06 implementation

### MA5/10
M06 owns two source-specific helpers:
- `BBMAHighMA()` -> MT4 `iMA(... MODE_LWMA, PRICE_HIGH ...)`
- `BBMALowMA()` -> MT4 `iMA(... MODE_LWMA, PRICE_LOW ...)`

`CalculateAllMA()` maps:
- `MA5_High` -> period 5 High LWMA
- `MA10_High` -> period 10 High LWMA
- `MA5_Low` -> period 5 Low LWMA
- `MA10_Low` -> period 10 Low LWMA

### MA50
`EMA()` is now a thin MT4 `iMA(... MODE_EMA, PRICE_CLOSE ...)` wrapper. `EMA50_PERIOD` remains 50.

### Bollinger calculations
The generic close-price `SMA()` remains available for Bollinger MID BB and standard-deviation calculations. It must not be reused as the producer for BBMA MA5/10 High/Low.

## Single-producer / previous-value rule
Any previous-candle MA5/10 lookup used by downstream modules must call the M06 BBMA High/Low helpers rather than recomputing MA5/10 with the generic close-price SMA.

Step 3C also removes a hardcoded H1 previous-MA lookup in the existing Extreme consumer path. Previous MA values now use the same `data.timeframe` as the frozen `TimeframeData` being evaluated.

## Scope guard
Step 3C repairs only MA production and source-consistent previous-MA retrieval. It does **not** certify or redefine:
- M08 Extreme BUY/SELL direction semantics,
- M09/MHV strategy interpretation,
- M10 CSM/CSD/eCSD definitions,
- Re-Entry trend-alignment policy,
- combination/sequence logic,
- SL/TP, risk or execution logic.

Those owning modules remain subject to separate source-alignment audits.

## Verification
Patch:
`blueprint/patches/0007-p0-step3c-m06-ma-source-alignment.patch`

Verification on the reconstructed post-Step3B working source:
- patch dry-run: clean;
- applied output: exact match to generated Step3C source;
- braces: 508 / 508;
- parentheses: 1473 / 1473;
- brackets: 330 / 330;
- remaining `SMA(...MA5/10...)` calls: 0.

Reconstructed working-source SHA-256 after patch 0007:
`274b3d380463f5cd9a477ce0c37b6da0db6c4cc6721013fdef4e984326b291bf`

Do not merge to `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
