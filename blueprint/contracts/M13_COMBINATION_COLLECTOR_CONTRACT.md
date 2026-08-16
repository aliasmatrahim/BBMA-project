# M13 BBMA Combination / Collector Contract

## Status
P0 Step 4 source-alignment contract for Module 13, with M27 routing support.

The user-supplied BBMA PDFs govern BBMA strategy semantics. `Oma ally BBMA - AL.pdf` is the primary operational reference.

## Source-derived REM / RRE / REE contract
Primary reference pages 12–13 state that REM, RRE and REE are setups formed from three components on three different timeframes. The BBMA code table defines:
- REM = Re-Entry + Extreme + MLV;
- RRE = Re-Entry + Re-Entry + Extreme;
- REE = Re-Entry + Extreme + Extreme.

The project is intentionally limited to D1 / H4 / H1 / M15. Therefore the supported rows are:
- REM: H4 Re-Entry + H1 Extreme + M15 confirmed MLV;
- RRE: D1 Re-Entry + H4 Re-Entry + H1 Extreme;
- REE: D1 Re-Entry + H4 Extreme + H1 Extreme.

M13 must not invent alternative component types or timeframe substitutions.

## Pure collector ownership
M13 is now a true collector/assembler only.

M13 does not call:
- `DetectExtreme()`;
- `DetectMHV()`;
- `DetectCSD()`;
- `DetectECSD()`;
- `DetectCSM()`;
- `DetectMLV_State()`;
- `UpdateReEntryState()`.

Ownership remains:
- M08 -> Extreme signal semantics;
- M09 -> MHV/MLV semantics and MLV lifecycle;
- M10 -> CSM/CSD/eCSD signal semantics;
- M12 -> Re-Entry lifecycle;
- M27 -> orchestrates one owner call per processing cycle and passes immutable copies to M13.

`CollectSignalSnapshots()` only copies the per-cycle owner outputs and applies collector-level classification precedence.

## CSD-over-eCSD same-candle precedence
Primary reference page 8 distinguishes:
- eCSD = crosses MA5/10;
- CSD = crosses MA5/10 and MID BB, with the MID BB cross showing real directional intent.

A source-valid CSD candle can mechanically satisfy the simpler eCSD predicate on the same closed candle. M13 therefore suppresses eCSD as an independent collected confirmation when CSD and eCSD have the same direction and candle time.

This does not change M10 detection semantics; it prevents one physical candle from being double-counted as two separate confirmations downstream.

## Component identity
`ComponentIdentity` now includes `Timeframe`.

`ComponentSet` now includes:
- `CombinationType` (`SIGNAL_REM`, `SIGNAL_RRE`, or `SIGNAL_REE`);
- `ComponentCount`.

`GenerateSequenceHash()` includes combination type, component count, each component type, direction, timeframe and candle time. This prevents multi-timeframe combination identity from being represented without its timeframe context.

## MLV chronology
A REM MLV component becomes usable only when the persistent MLV state is `MLV_CONFIRMED && IsValid`.

The component candle time is `ConfirmationCandleTime`, not the original candidate/start candle. `SequenceStartTime` is metadata only and is the earliest of the three actual component times.

## No M13 SL/TP ownership
The supplied REM/RRE/REE source pages define the component setup, not an M13-specific SL/TP-source selection rule.

M13 therefore no longer selects MLV, Re-Entry or Extreme as `SLTPSource`. A completed M13 combination candidate leaves `SLTPSource = SIGNAL_NONE` for the later owning validation/SLTP architecture to resolve.

This prevents a collect-only module from silently creating trading semantics that are not stated in the BBMA combination source.

## No chronology invention in M13
The source describes the three setups as forming at the same time / across three different timeframes. M13 therefore assembles coexisting source-valid components but does not impose an artificial `Comp1 < Comp2 < Comp3` chronological sequence.

Direction consistency, coexistence/expiry windows and final validation belong to M14/M15. The existing M14 strict chronological validator is therefore a known next-step blocker and must be repaired before these combinations can become final decisions.

## M27 routing support
Step 4B moves owner calls out of M13 and into M27 orchestration.

M27 now:
- creates H1/H4/M15 numeric BB snapshots from frozen `TimeframeData` regardless of whether optional BB-shape classification is enabled;
- optionally asks M07 to classify H1/H4 BB shape;
- calls M08/M09/M10/M12 owners;
- stamps raw `Signal` snapshots with their real timeframe, bar index, candle time and close;
- passes immutable copies into M13;
- exports confirmed H4/D1 Re-Entry snapshots through the existing M12 export contract.

The numeric-BB routing change prevents disabling `EnableBBShapeEngine` from accidentally zeroing the TOP/LOW BB values required by source-valid Extreme detection.

## Scope guard
Step 4 does not certify or change:
- M09 MHV strategy semantics beyond routing its existing output;
- temporal CSM invalidation of a previously existing Extreme;
- M14 sequence/combination validation;
- M15 final priority/entry authority;
- trend-alignment policy;
- standalone Extreme entry confirmation/retest;
- SL/TP, risk or execution rules.

## Implementation record
Patches:
- `blueprint/patches/0010-p0-step4a-m13-combination-collector-source-alignment.patch`
- `blueprint/patches/0011-p0-step4b-m27-signal-owner-routing.patch`

Patch commits:
- 0010: `1a7cdede87fce5bf3ebc6ecc6e2a05ac9e3dc73b`
- 0011: `0a48a6f13cfa9a8885408fbd6ae90181388b088a`

Local patch SHA-256:
- 0010: `273f88d8b9e3c9d4781a3ba3bed26828c26f3e26c0a255ce376c1a9408709262`
- 0011: `65c8ad9c791816567b5875bd70f21c8f7cb85e6610d8f1dc86749f79780d3db6`

## Verification
Focused current-state reconstruction verification:
- patch 0010 dry-run/apply: clean;
- patch 0011 dry-run/apply after 0010: clean;
- sequential output exactly matches the generated Step 4 target;
- braces: 489 / 489;
- parentheses: 1454 / 1454;
- brackets: 339 / 339;
- M13 calls to strategy detectors/state mutators: 0;
- old `CollectAllSignals()` calls: 0;
- REM/RRE/REE each carry an explicit combination identity and three timeframe-stamped components;
- CSD-over-eCSD same-candle suppression is present.

No new full-working-source SHA is claimed from this focused reconstruction. The previously withdrawn partial-reconstruction SHA remains withdrawn until the entire patch chain is exactly materialized.

Do not merge to `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
