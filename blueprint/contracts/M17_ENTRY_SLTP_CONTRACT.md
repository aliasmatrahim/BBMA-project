# M17 Entry / SL / TP Resolution & Validation Contract

## Status
P0 Step 8C is **COMPLETED AT ACTIVE-BLUEPRINT PATCH LEVEL**.

The Step 8 engineering guard remains active, and the Step 8B approved BBMA destination / structural-stop contract is now implemented by ordered patch `0016`.

The user-supplied BBMA PDFs govern BBMA strategy semantics. `Oma ally BBMA - AL.pdf` remains the primary operational reference. Community-supported exit rules remain explicitly separated from PDF-core rules.

## Provenance boundary
The implementation preserves three provenance classes:
- `PDF_CORE` — explicit BBMA/Oma Ally source semantics;
- `FORUM_SUPPORTED` — community-supported BBMA destination/exit interpretation;
- `EA_SAFETY` — deterministic broker-side protection required for autonomous execution.

No `FORUM_SUPPORTED` or `EA_SAFETY` rule may be described as an explicit PDF Oma Ally rule.

## Approved executable TP mapping
For currently executable M15 decision types:
- confirmed H1 `RE_ENTRY`: BUY -> H1 TOP BB, SELL -> H1 LOW BB;
- `REM`: BUY -> H4 TOP BB, SELL -> H4 LOW BB;
- `RRE`: BUY -> D1 TOP BB, SELL -> D1 LOW BB;
- `REE`: BUY -> D1 TOP BB, SELL -> D1 LOW BB.

The TP source is always the validated Re-Entry component at the exact mapped timeframe.

## Decision payload extension
`BBMA_Decision` now carries:
- `HasSLTPSourceComponent`;
- `SLTPSourceComponent`.

M15 does not invent a price target. It only preserves the already validated component identity needed by the downstream Step 8B mapping:
- standalone Re-Entry -> H1 Re-Entry component;
- REM -> H4 Re-Entry component;
- RRE/REE -> D1 Re-Entry component.

The full component payload still survives M14 -> M15 -> M16, and M16 continues to revalidate owner-state identity before M17 executes.

## Closed-candle source resolver
M17 resolves the source component candle by exact `CandleTime` and timeframe using `iBarShift(..., exact=true)`.

Resolution is accepted only when:
- the component type is `SIGNAL_RE_ENTRY`;
- the component direction equals the final decision direction;
- the component timeframe exactly matches the approved mapping;
- the resolved bar time exactly equals the stored component candle time;
- the resolved shift is `>= 1`, therefore fully closed.

A missing, stale, current-bar or ambiguous source fails closed.

## BB destination resolver
The approved single TP is read from the Bollinger Band on the exact closed source candle:
- BUY -> upper BB;
- SELL -> lower BB.

M17 does not substitute another timeframe and does not create a replacement target if the mapped destination has already been crossed.

A BUY target at/below execution entry or SELL target at/above execution entry fails closed with `REJ_SLTP_UNRESOLVED`.

## Protective hard SL
Classification: **EA_SAFETY informed by FORUM_SUPPORTED structural practice**.

For the current deterministic implementation, the source-owned structural anchor is the wick of the exact closed Re-Entry source candle selected by the approved mapping:
- BUY -> source-candle LOW;
- SELL -> source-candle HIGH.

The broker hard stop is placed one broker point beyond that wick:
- BUY -> `LOW - Point`;
- SELL -> `HIGH + Point`.

This one-point buffer is engineering protection only and is not represented as a PDF Oma Ally rule.

The resolver does not scan an unrelated arbitrary swing window. If the exact source candle cannot be resolved, it fails closed.

## Execution reference price
Broker execution geometry remains:
- BUY market execution reference = ASK;
- SELL market execution reference = BID.

This is broker-side execution normalization and does not redefine BBMA setup entry semantics.

## Direction-aware geometry
A source-resolved pair is valid only when:
- BUY: `SL < Entry < TP`;
- SELL: `TP < Entry < SL`.

Wrong-side, zero-distance or inverted geometry is rejected.

## MaxSL ownership
`MaxSLPips` remains a project rejection cap only.

It uses the project pip-price helper and may reject an excessively distant source-resolved SL. It never manufactures the SL itself.

## MinRR ownership
`MinRRRatio` remains a rejection filter only.

It may reject a source-resolved SL/TP pair whose reward/risk is below the configured threshold. It never manufactures TP.

## StopLevel / FreezeLevel
Direction-aware broker geometry from Step 8 remains active:
- BUY uses BID as the close/trigger side;
- SELL uses ASK.

## Fail-closed behavior
`REJ_SLTP_UNRESOLVED` remains mandatory when:
- mapped source component is missing;
- source type/timeframe/direction does not match the approved mapping;
- source candle cannot be resolved exactly as a closed bar;
- wick anchor is invalid;
- BB destination is invalid;
- destination is already crossed/stale;
- the initial source resolver otherwise cannot produce a complete pair.

No fixed-pip or RR-manufactured fallback is allowed.

## Lifecycle boundary
Opposite confirmed CSM/momentum + BB expansion remains a possible `FORUM_SUPPORTED` dynamic invalidation concept, but Step 8C does **not** enable it as a broker close rule.

M23/M24 lifecycle ownership must be audited separately before any dynamic cut-loss close path is enabled.

M16 invalidation does not directly close live broker positions.

## Ownership guard
M17 owns:
- execution-reference price normalization;
- validation of the approved source component identity;
- exact closed-source-candle lookup;
- approved BB destination resolution;
- structural hard-SL resolution from the exact source candle wick;
- BUY/SELL geometry validation;
- broker StopLevel/FreezeLevel checks;
- MaxSL and MinRR rejection filters;
- explicit fail-closed source-resolution behavior.

M17 does **not** own:
- BBMA signal detection;
- Re-Entry confirmation;
- REM/RRE/REE construction;
- final direction selection;
- lot sizing;
- portfolio risk;
- order execution;
- live-position dynamic invalidation close;
- trailing stop;
- TP2/TP3.

## Implementation record
Step 8 engineering guard patch:
`blueprint/patches/0015-p0-step8-m17-sltp-source-guard-direction-validation.patch`

Step 8C resolver patch:
`blueprint/patches/0016-p0-step8c-m17-approved-sltp-resolver.patch`

Step 8C patch commit:
`2afeee76806f4b1c4e56f829fd7c8d42403a1450`

## Focused verification status
Verified directly from the stored `0016` patch:
- decision payload carries an explicit mapped SL/TP source component;
- only H1/H4/D1 Re-Entry source mapping is accepted for RE_ENTRY/REM/RRE/REE respectively;
- exact closed candle identity is enforced;
- BB target is source-timeframe and direction aware;
- structural stop uses the exact source-candle wick plus one broker point;
- crossed destination fails closed;
- `REJ_SLTP_UNRESOLVED` remains active;
- fixed-pip and RR-manufactured fallback are absent from Step 8C;
- dynamic opposite-CSM broker close is not introduced.

This is a focused patch-level verification. A new complete full-chain working-source SHA is **not** claimed until the ordered patch chain is exactly materialized and tested as one source.

Do not merge to `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
