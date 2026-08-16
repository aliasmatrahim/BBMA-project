# M17 Entry / SL / TP Resolution & Validation Contract

## Status
P0 Step 8 is **PARTIALLY COMPLETED / SAFE SOURCE GUARD ACTIVE**.

M17 engineering validation is repaired, but the supplied BBMA source does not yet provide a deterministic complete SL+TP contract for the entry types currently allowed by M15.

The user-supplied BBMA PDFs govern BBMA strategy semantics. `Oma ally BBMA - AL.pdf` remains the primary operational reference.

## Source findings
The primary reference explicitly states for Extreme:
- Extreme requires reversal-candle confirmation;
- retest candle is the point of entry;
- SL can be placed a few pips above the highest shadow/wick (SELL-side wording in the source example).

However, the primary reference does **not** provide a deterministic Take Profit formula.

For Re-Entry, the source defines entry/setup locations such as MA5/10 High/Low, MA5/M50 retrace, and MA5/10 + MID BB confluence, but the supplied pages do not define a complete deterministic SL + TP pair for autonomous execution.

REM/RRE/REE are defined as multi-timeframe setups. The source also says to enter on a lower timeframe such as M15 and align with trend, but it does not provide a universal fixed entry-price/SL/TP formula for every REM/RRE/REE case.

## Legacy blueprint builders are not source authority
The old blueprint contains helper builders that manufacture SL and TP from:
- `MaxSLPips`; and
- `MinRRRatio`.

Examples include legacy Extreme/CSD/Re-Entry/MLV builders.

Those formulas are engineering inventions, not rules established by the supplied BBMA PDF. They must therefore **not** be treated as BBMA source resolution.

`MaxSLPips` and `MinRRRatio` may remain as project **rejection/risk filters** after a genuine BBMA SL/TP has been resolved, but they may not manufacture the actual SL or TP.

## Fail-closed source guard
M17 now requires `SLTPSource != SIGNAL_NONE` plus positive resolved SL and TP before a decision can pass SL/TP validation.

If the strategy source has not resolved a complete SL/TP pair, M17 rejects with:
`REJ_SLTP_UNRESOLVED`.

This prevents the EA from silently converting a valid BBMA setup into a non-BBMA trade-management rule.

Current consequence:
- confirmed Re-Entry, REM, RRE and REE can still be detected/validated upstream;
- they are **not execution-ready** until an approved source-backed SL/TP contract is supplied or explicitly approved as non-BBMA project logic.

## Execution reference price
M17 now distinguishes broker execution geometry from BBMA strategy semantics:
- BUY market execution reference = ASK;
- SELL market execution reference = BID.

This does not redefine the BBMA setup entry location. It only establishes the broker-side execution reference once the upstream setup has already become eligible.

## Direction-aware SL/TP geometry
A resolved pair is structurally valid only when:
- BUY: `SL < Entry < TP`;
- SELL: `TP < Entry < SL`.

The previous absolute-distance-only validation could accept inverted SL/TP geometry and is removed.

## Correct MaxSL conversion
The old M17 formula:
`MaxSLPips * Point / 10`
was dimensionally incorrect for normal 4/5-digit and 2/3-digit FX quoting.

Step 8 uses the existing project pip-price helper (`GetPipValue(pair)`) so the rejection cap is:
`MaxSLPips * pipPrice`.

Again, this is only a maximum-risk cap and never the source of the SL itself.

## MinRR ownership
`MinRRRatio` remains an optional project rejection filter:
- it can reject a source-resolved SL/TP pair whose RR is below the configured minimum;
- it cannot create TP from SL distance.

## StopLevel / FreezeLevel side awareness
The old helpers always compared levels to BID.

Step 8 makes them direction-aware:
- BUY position stop/freeze geometry uses BID as the close/trigger side;
- SELL position stop/freeze geometry uses ASK.

The existing M23 breakeven call is updated to pass explicit trade direction so the signature change does not leave a compile-time mismatch.

## StopLossPoints semantics
When a valid source-resolved pair eventually passes M17, `decision.StopLossPoints` is normalized as:
`abs(EntryPrice - StopLoss) / Point`.

## Ownership guard
M17 owns:
- execution-reference price normalization;
- structural BUY/SELL SL/TP geometry validation;
- broker StopLevel/FreezeLevel geometry helpers;
- MaxSL and MinRR rejection filters;
- explicit fail-closed source-resolution guard.

M17 does **not** own:
- BBMA signal detection;
- final direction selection;
- invention of SL/TP strategy rules;
- lot sizing;
- portfolio risk;
- order execution.

## Current unresolved architecture decision
A source-backed deterministic TP rule is still missing from the supplied BBMA material for the currently executable setup types.

Before live execution can be enabled, one of the following must happen:
1. an additional authoritative BBMA source is supplied that defines deterministic SL/TP/exit rules; or
2. the user explicitly approves an exit/SLTP rule as **non-BBMA project management logic**, clearly separated from BBMA strategy semantics.

Until then, `REJ_SLTP_UNRESOLVED` is the correct safety behavior.

## Implementation record
Patch:
`blueprint/patches/0015-p0-step8-m17-sltp-source-guard-direction-validation.patch`

Patch commit:
`fe06331500acf5cbce11ce2e411134e9b9b333d2`

Focused patch SHA-256:
`8aeeb013aaa76182f222b31eb0b0dfeb67a2765090cc8dad7dc9a488188e0b8c`

## Verification
Focused post-Step7 reconstruction:
- dry-run patch: clean;
- patch apply: clean;
- applied output exact-match to generated Step 8 target;
- braces: 521 / 521;
- parentheses: 1583 / 1583;
- brackets: 355 / 355;
- legacy M17 `MaxSLPips * Point / 10` formula absent;
- legacy BID-only M17 StopLevel/FreezeLevel behavior absent;
- explicit direction-aware geometry present;
- execution ASK/BID reference resolver present;
- `REJ_SLTP_UNRESOLVED` source guard present;
- M23 caller updated to explicit direction.

This remains focused verification. No new complete full-chain working-source SHA is claimed until the ordered patch chain is materialized exactly into one source file.

Do not merge to `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
