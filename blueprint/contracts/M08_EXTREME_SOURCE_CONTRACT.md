# M08 BBMA Extreme Source Contract

## Status
P0 Step 3D source-alignment contract for Module 08.

The user-supplied BBMA PDFs govern BBMA strategy semantics. `Oma ally BBMA - AL.pdf` is the primary operational reference; `BBMA technique.pdf` is secondary corroboration.

## Source-derived Extreme signal contract

### Signal vs entry
The primary reference classifies Extreme as a **signal**, while MLV and Re-Entry are setups. It also states that an Extreme indicates potential reversal but requires reversal-candle confirmation, and identifies the retest candle as the point of entry.

Therefore M08 `DetectExtreme()` answers only: **is a source-defined Extreme signal present on this closed candle?**

A `true` detector result is **not standalone execution authority**. Standalone Extreme entry eligibility must later require the source-defined reversal/retest contract through the final entry-eligibility architecture.

### Direction and MA side
Secondary reference page 28 explicitly states:
- Extreme SELL -> MA5/10 High outside TOP BB.
- Extreme BUY -> MA5/10 Low outside LOW BB.

Primary reference page 6 states the characteristic as MA5 or MA5/10 outside the relevant Top/Bottom BB.

M08 therefore maps:
- SELL: `MA5_High > TOP_BB` OR `MA10_High > TOP_BB`.
- BUY: `MA5_Low < LOW_BB` OR `MA10_Low < LOW_BB`.

This uses the source-correct M06 MA producers locked in P0 Step 3C.

### Price-close VOID rule
Primary reference page 6 states that an Extreme is VOID when candlesticks close outside the relevant TOP/LOW BB.

M08 therefore rejects the current closed candle as a valid Extreme signal when:
- SELL context: `close > TOP_BB`.
- BUY context: `close < LOW_BB`.

This is a source rule, not a risk filter.

## Removed non-source detector logic
Step 3D removes these old M08 gates because they are not part of the supplied Extreme definition:
- close merely being within 10% of the outer BB;
- MA5 slope / previous-MA extension requirement;
- mandatory `BB_EXPANDING || BB_SQUEEZE` gate;
- the reversed MA-side mapping where BUY used MA5 High and SELL used MA5 Low.

BB shape can still be auxiliary classification data because the source describes multiple Extreme types, including sideways/momentum variants, but BB shape is not a universal prerequisite for existence of an Extreme signal.

## Source rules intentionally not invented inside M08

### Reversal candle and retest entry
The primary reference says:
- reversal candle(s) confirm the Extreme;
- the reversal may involve more than one candle;
- the retest candle is the point of entry.

The supplied references do not define a deterministic candle-pattern algorithm precise enough to encode a universal reversal-candle lifecycle without interpretation. Step 3D therefore does not silently invent one.

This means:
- Extreme may remain a valid BBMA **signal/component** for source-defined combinations such as REM/REE;
- Extreme must not become a standalone trade merely because `DetectExtreme()` returned true;
- final standalone Extreme entry eligibility must remain separate from raw signal validity.

### CSM invalidation dependency
The primary reference states that Extreme is no longer valid in the presence of CSM, regardless of MA5 position outside the BB.

M08 does not own CSM detection. M10 owns CSM. Because M10 is still awaiting its own source-alignment audit, Step 3D does not hard-wire the current unaudited M10 result into M08.

The CSM invalidation rule remains a required downstream dependency and must be connected after M10 CSM is source-aligned.

## Ownership rule
- M06 owns MA/BB numeric production.
- M07 may classify BB shape as auxiliary context.
- M08 owns Extreme signal detection semantics.
- M10 owns CSM production.
- M13 collects immutable signal snapshots; it must not redefine Extreme.
- M15/final eligibility decides whether a source-valid Extreme is actually an entry opportunity.

## Implementation record
Patch:
`blueprint/patches/0008-p0-step3d-m08-extreme-source-alignment.patch`

GitHub commit:
`2a37d505c28b9b78a83eb045c2c2333ce2a1091d`

## Verification
The M08 patch was generated against the post-Step3C M08 body and then dry-run/applied locally with exact output match.

Focused local verification after the patch:
- braces balanced;
- parentheses balanced;
- brackets balanced;
- old 10% outer-BB proximity gate removed;
- old MA5 slope gate removed;
- old BB-state mandatory gate removed;
- BUY/SELL MA-side mapping source-aligned.

A previously recorded full-working-source SHA after patch 0007 was discovered during Step 3D to have been calculated from a partial reconstruction rather than the full patch chain. That SHA must not be treated as authoritative and is withdrawn in `blueprint/CURRENT.md`. A full-chain SHA will be regenerated only from an exact materialization of patches 0001 onward.

Do not merge to `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
