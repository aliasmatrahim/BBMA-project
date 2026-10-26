# M10 BBMA Direction / Momentum Source Contract

## Status
P0 Step 3E source-alignment contract for Module 10.

The user-supplied BBMA PDFs govern BBMA strategy semantics. `Oma ally BBMA - AL.pdf` is the primary operational reference; `BBMA technique.pdf` is secondary corroboration.

## Source-derived signal roles
The primary reference classifies CSM, eCSD and CSD as BBMA **signals**, not standalone execution authority.

Primary reference page 8 states:
- eCSD = candlestick that crosses MA5/10;
- CSD = candlestick that crosses MA5/10 and MID BB;
- CSD shows real intent of price direction by crossing MID BB;
- retracement often follows CSD/eCSD and the later MA5/10 retracement is where Re-Entry context appears.

Therefore M10 detects signal mechanics only. It does not turn CSM/eCSD/CSD directly into trades.

## eCSD contract
Source rule:
- eCSD crosses MA5/10.

Operational directional mapping retained for deterministic implementation:
- BUY eCSD crosses the MA5 High and MA10 High pair upward.
- SELL eCSD crosses the MA5 Low and MA10 Low pair downward.

The supplied text says `MA5/10` but does not explicitly spell out which High/Low pair is used for each direction. The mapping above is therefore an implementation interpretation consistent with the directional MA arrangement already used throughout the BBMA project; it must not be quoted as verbatim PDF wording.

`DetectECSD` implements the raw MA5/MA10 crossing predicate. Since CSD also crosses this pair, the raw predicate can be true on a same-direction CSD candle. The normalized event classification must prefer CSD when its Mid-BB cross is also present; only a same-direction MA-pair cross without CSD is labelled eCSD.

## CSD contract
Source rule:
- CSD crosses MA5/10 **and MID BB**;
- the MID BB cross distinguishes the stronger direction signal and shows real price intent.

Operational mapping:
- BUY CSD crosses MA5 High, MA10 High and MID BB upward.
- SELL CSD crosses MA5 Low, MA10 Low and MID BB downward.

## Deterministic meaning of `crosses`
The PDF uses the word `crosses` but does not provide a wick-vs-body coding formula.

Step 3E encodes crossing as the **closed candle body spanning the required line from open to close**:
- BUY: `open <= level && close > level`.
- SELL: `open >= level && close < level`.

Wick-only touches do not count as a cross.

This is an explicit engineering interpretation required for deterministic EA behaviour, not a claimed verbatim Oma Ally rule.

## CSM contract
Primary reference pages 2 and 5 describe CSM as momentum candle(s) created while price travels in its intended direction after a short retracement, continuing until momentum diminishes.

Secondary reference page 18 provides the missing operational momentum law:
- candlestick close outside TOP BB while BB is vertical marks upward momentum;
- candlestick close outside LOW BB while BB is declining/vertical marks downward momentum.

The same secondary reference explains that expanding BB reflects strengthening momentum, while page 19 distinguishes horizontal-BB outer closes as reversal context rather than directional momentum.

Therefore Step 3E rejects the old CSM implementation based on:
- exactly three same-colour candles; and
- each body being greater than 70% of the three-candle average body.

Those conditions are not supported by the supplied BBMA sources.

### Deterministic CSM encoding
A source-valid CSM requires:
- BUY: closed candle `close > TOP_BB`;
- SELL: closed candle `close < LOW_BB`;
- current BB width greater than previous closed-candle BB width;
- MID BB and the relevant outer BB moving in the same direction as momentum.

The width increase + directional MID/outer movement is the project's deterministic encoding of the source phrase `BB vertical / expanding`. No arbitrary percentage threshold is added.

## Downstream consequences
### M12 Re-Entry Type 3
Type 3 now receives a source-aligned CSM precursor from M10. The existing Step 3B lifecycle remains:
`CSM precursor -> candidate -> later retrace to MA5 or MA50 -> confirmed Re-Entry`.

### M12 Re-Entry Type 4
Type 4 now receives the corrected CSD crossing signal as its precursor. Its existing Step 3B lifecycle remains:
`CSD precursor -> candidate -> later retrace to MA5/10 -> confirmed Re-Entry`.

### M08 Extreme invalidation — current-owner reconciliation (CP10, 2026-10-27)
The accepted primary/Core rule states that Extreme is no longer valid in the presence of source-valid CSM/Momentum. The older Step 3E note that M08 had no persistent lifecycle is superseded by current Build 5.15 source.

M08 owns that temporal lifecycle: `UpdateExtremeLifecycle` invokes `IsExtremeLifecycleInvalidation` before maturity promotion, and the latter invokes M08's local `IsExtremeMomentumInvalidation`. On valid closed BB inputs, that helper mirrors M10 `DetectCSM` geometry (increased width, directional Mid/relevant outer movement, and close outside the relevant band). It is not a direct M08 → M10 function call, so no direct call edge is claimed.

Static source mapping is VERIFIED. A focused helper-parity regression and attributable runtime evidence were not run; they remain NOT VERIFIED. Keep M10 as the CSM signal producer and M08 as the Extreme lifecycle owner; this reconciliation authorizes no behavior change.

## Current-owner classification and handoff (CP13, 2026-10-26)

`DetectECSD` returns the raw MA5/MA10 cross predicate, so it can be true on the same candle as a same-direction CSD. Consumers normalize the class before strategy use:
- M12 `DetectReEntryDirectionOwnerSignal()` classifies `CSM > CSD > eCSD`. CSM and CSD may start their own Type 3/Type 4 Re-Entry candidates; a later source-specific MA retrace confirms them. eCSD may establish/advance Type 1 direction ownership but does not confirm entry.
- M13 `CollectSignalSnapshots()` suppresses a same-direction eCSD when CSD has the same candle timestamp. Its REM/RRE/REE assembler does not make raw CSD/eCSD a component.
- M27's H4 authoritative classifier uses `CSM > CSD > eCSD`. Its M15 data comes from the exact latest-closed M15 snapshot. M09's canonical MHV/MLV update independently requires valid, closed source data and consumes a same-direction M15 CSD/eCSD only as the later direction-takeover event.
- The approved D1O-01 M11J path uses closed D1 CSD only as opportunity context. D1 eCSD is watch-only; its logger reports the raw MA-cross predicate and can overlap with a same-direction CSD, but it installs no opportunity family. A D1 CSD opportunity still requires an aligned D1 strategic owner and a fresh confirmed LTF Re-Entry after activation. The materialized candidate is `SIGNAL_RE_ENTRY`; M15 remains final authority and M16 remains fail-closed.

M12/H4/D1 caller paths validate closed data; the M15 input path selects an exact candle through `GetLatestClosedCandleTime` and `GetDataForTimeframe`, and M09 rejects invalid or unclosed M15 data before state takeover. This confirms the static closed-candle handoff.

Input quality is a separate dependency: current owner Build 5.15 still has the recorded M06 incomplete-history validity defect. Its repair is candidate-scoped in Build 5.20/PR #293 and does not make current-owner CSD/eCSD signals on incomplete histories runtime-verified.

The old instruction that M13 must later decide CSD/eCSD precedence is stale and is corrected by the existing M13 contract and owner implementation. CP13 is static only; no focused precedence test or attributable runtime was run. It adds no signal formula, combination component or direct raw-signal execution path.

## Scope guard
Step 3E does not change:
- Re-Entry retracement confirmation rules already locked in M12;
- REM/RRE/REE combination contracts;
- M14 sequence validation;
- final M15 entry eligibility;
- SL/TP, risk or execution logic.

## Implementation record
Patch:
`blueprint/patches/0009-p0-step3e-m10-csd-ecsd-csm-source-alignment.patch`

Patch commit:
`d3b804da58e8cb837e66f46d65c9c56fc1e3840d`

## Verification
Focused reconstruction verification:
- patch dry-run: clean;
- patch apply: exact output match;
- braces balanced;
- parentheses balanced;
- brackets balanced;
- old three-candle / 70%-average-body CSM formula removed;
- CSD requires MA5/10 + MID BB crossing;
- the raw eCSD predicate requires MA5/10 crossing; CSD-over-eCSD is normalized by the active consumer precedence;
- CSM requires directional outer-BB close plus expanding/directional BB context.

Because the project previously discovered that a partial reconstruction had been mislabeled as a full-chain source, no new full-working-source SHA is claimed from this focused Step 3E verification.

Do not merge to `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
