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

## Accepted reversal and retest lifecycle (Core V2 §5.4; CP11)

The primary PDF identifies reversal-candle confirmation and later retest entry. The deterministic lifecycle below is the user-approved project mapping in Core V2 §5.4 and `blueprint/decisions/CORE_V2_F2_EXTREME_MATURITY_DECISION.md`; its Boolean candle-direction and phase triggers are not verbatim source formulas.

- `DetectExtreme()` identifies only a strict MA5/MA10 outside-band RAW candidate on valid closed data. RAW alone is neither an MTF component nor entry authority.
- `UpdateExtremeLifecycle()` checks accepted invalidation before each maturity promotion. The first subsequent closed source-timeframe reversal-direction candle promotes to `REVERSAL_CONFIRMED`. It adds no fixed candle/session expiry, named pattern or universal close-inside-BB gate.
- During continued reversal, the provisional body edge may update. The first close progression back toward the prior close starts retest and freezes the body reference: SELL `CurrentClose > PreviousClose`; BUY `CurrentClose < PreviousClose`.
- The retest-start candle is excluded from the body anchor but may itself complete the retest. The first valid range/wick interaction with the frozen body anchor **or** relevant MA5 yields `RETEST_READY`; there is no mandatory dual touch or reference hierarchy.
- `REVERSAL_CONFIRMED` (including retest-phase/ready) is the F2 decision's source-inferred maturity for REM/REE Extreme components. Standalone H1 Extreme entry requires exact `RETEST_READY`.
- CF-02/03/04 are handled by Core V2 §5.3: strict outside remains; there is no universal inside-close gate or blanket outside-BB reversal exception; the repeated-LTF no-TPW case remains bounded and is excluded from D1.

### CSM invalidation dependency — current-owner reconciliation (CP10, 2026-10-27)
The accepted source rule remains: a later source-valid Momentum/CSM context invalidates the Extreme lifecycle; an outside close through the original Extreme-side outer BB also remains a separate source invalidation.

The older Step 3D statement that this temporal link awaited M10 source alignment is superseded by the current Build 5.15 source. `UpdateExtremeLifecycle` calls `IsExtremeLifecycleInvalidation` before maturity promotion; that helper calls the M08-local `IsExtremeMomentumInvalidation` predicate. For valid closed BB inputs, its geometry matches the M10 CSM definition: width increases, Mid and the relevant outer band move in the same direction, and close is outside that outer band.

This is a static behavioral mapping, not a direct call to M10 `DetectCSM`. M08 remains the Extreme lifecycle owner and M10 remains the CSM signal owner. No focused M08/M10 parity test or attributable runtime proof was run; that status remains NOT VERIFIED. Do not route the M07 enum into M10 or infer a new source rule from this mapping.

## Ownership rule
- M06 owns closed-candle OHLC and numeric MA/BB production; incomplete-history validity is tracked separately under Issue #292.
- M07 may classify BB shape as auxiliary context; it is not an M08/M10 signal gate.
- M08 owns RAW detection, maturity, invalidation, supersession and retest lifecycle.
- M09 consumes a reversal-confirmed M15 Extreme as the parent of its separate TP-Wajib/MHV-MLV lifecycle.
- M10 owns CSM production; M08's current invalidation helper is a local equivalent predicate, not a direct call to M10.
- M12N observes Extreme state as read-only lineage only.
- M13 collects reversal-confirmed H1/H4 Extreme snapshots for the exact REM/RRE/REE signatures; it does not redetect Extreme.
- M15 permits standalone H1 Extreme only at RETEST_READY under Mode 2 plus the active same-direction H4 and M11 D1 gates.
- M16 revalidates the frozen exact M08 lifecycle identity; it does not promote maturity.
- M17 maps standalone H1 Extreme to the approved structural-wick SL and normal TP-Wajib area. The exact H1 broker mapping is project execution policy.
- M11J's D1 Extreme TP-Wajib opportunity is a separate project extension. Its dedicated lifecycle gate is OFF; M17 fails closed for that identity while OFF, and M23's D1 TPW lifecycle remains gated.
- M23 C044 replay uses private M08 state copies; M27 owns closed-snapshot call order and downstream handoffs.

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
