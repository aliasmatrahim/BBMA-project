# BBMA Home Course Workbook — Full 19-Page Forensic Audit

Status: ACTIVE FORENSIC SOURCE AUDIT
Date: 2026-08-25
Source: `docs/references/original/333531988-BBMA-Home-Course.pdf`
Target: `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`

## Audit contract

This audit treats the 19-page BBMA Home Course Workbook as source evidence at the PDF evidence layer. Every source statement must be classified before any Core promotion:

- `COVERED` — materially represented by Core V2.
- `PARTIAL` — Core V2 represents only part of the source meaning.
- `MISSING` — applicable Strategy-Core rule not represented by Core V2.
- `CONFLICT/HOLD` — source conflicts with accepted evidence or needs explicit strategy resolution.
- `DUPLICATE/CORROBORATION` — repeats an already mapped source rule.
- `NON_CORE` — platform instructions, chart cosmetics, personal workflow, money management, news-specific discretionary trading, or other material outside universal EA Strategy Core.

Coverage denominator is **applicable atomic Strategy-Core rules only**. No percentage may be published until every applicable atomic rule from all 19 pages has an explicit mapping row.

## Full-page source inventory completed

All 19 pages were read end-to-end. The workbook covers:

1. BB setting/state, horizontal vs directional BB, Momentum and Mid-BB zones.
2. MA5 High/Low settings and momentum relationship.
3. MA10 High and early/strong direction candle.
4. MA10 Low and MA ordering.
5. EMA50/MA50 trend structure.
6. BBMA basic laws and Mid-BB direction confirmation.
7. Extreme lifecycle: MA5 outside BB -> reversal -> retest entry -> mandatory TP.
8. MHV lifecycle: failed outer-BB continuation -> reversal -> marked-volume retest; post-MHV TP behavior.
9. Early/strong direction signal and Re-Entry expectation.
10. Re-Entry, powerful MA5/MA10/Mid-BB confluence, minimum three-candle movement, MTF continuation, D1/MA50 major-trend ownership, cross-timeframe Extreme/MHV relationships.
11. Momentum lifecycle, Re-Entry after Momentum, first-candle validation/second-candle entry wording, strongest direction crossing MA5/MA10/Mid-BB/MA50.
12. Final summary/cycle: Extreme -> TP Wajib -> MHV -> Direction -> Re-Entry -> Momentum -> Re-Entry, plus account-management material.

## Confirmed Core-V2 coverage

The following workbook contracts are already materially represented in Core V2:

- indicator contract: BB20/2, MA5/MA10 High/Low LWMA, EMA/MA50 Close;
- canonical cycle ordering;
- Momentum requires an outside outer-BB close in accepted directional/expanding BB context;
- raw Extreme is signal/context, not standalone entry authority;
- Extreme reversal confirmation and later retest/entry-ready lifecycle;
- Extreme TP-Wajib structure;
- MHV/MLV requires prior Extreme provenance and is setup/context rather than standalone execution authority;
- MHV marked-body and later retest concepts;
- eCSD/early direction versus CSD/strong direction separation;
- Re-Entry as the actual entry/setup zone after direction/momentum context;
- powerful Re-Entry at MA5/MA10 + Mid BB, strengthened by MA50;
- source-supported minimum-three-candle Re-Entry wording;
- first-candle validation / second-candle entry wording;
- multi-timeframe structural scaling and higher-timeframe ownership;
- accepted REM/RRE/REE signatures.

## Material delta candidates found in the Workbook

These are not silently promoted yet; each requires row-level evidence mapping against Core V2 and existing PDF/Finale evidence.

### HC-D01 — Horizontal-BB three-condition behavior
Workbook gives explicit horizontal-BB behavior for wick-through/close-inside, body+wick outside/close-outside, and wick-near-boundary cases, generally targeting at least Mid BB. Core V2 intentionally focuses on accepted Momentum semantics and does not currently encode this full three-condition horizontal-BB behavioral table.

Preliminary status: `MISSING/PARTIAL — candidate clarification`, not execution-authority yet.

### HC-D02 — Mid-BB Buying Zone / Selling Zone semantics
Workbook explicitly defines Mid->Top as Buying Zone and Mid->Low as Selling Zone, with Mid-BB slope as same-timeframe trend guide. Core V2 uses Mid BB structurally but does not expose this complete zone contract as a canonical named rule.

Preliminary status: `PARTIAL`.

### HC-D03 — MA5-close momentum strengthening
Workbook states a falling candle closing outside MA5 Low is momentum and closing outside BB + MA5 Low with MA5 Low hugging Lower BB is very strong momentum. Core V2 canonical Momentum is outer-BB/BB-state based and does not presently elevate this MA5 relationship into a separate universal momentum class.

Preliminary status: `HOLD/CLARIFY` because it may be strength/context rather than a distinct validity rule.

### HC-D04 — Direction-strength ladder
Workbook distinguishes: close beyond MA10 but not Mid BB = weak/early direction; close beyond MA10 + Mid BB = strong direction; later summary uses MA5+MA10 and MA5+MA10+Mid BB; strongest wording adds MA50. Core V2 covers eCSD/CSD but does not currently expose the full strength ladder including MA50 as a named highest-strength tier.

Preliminary status: `PARTIAL`.

### HC-D05 — D1 MA50 explicit major-trend precedence
Workbook explicitly says MA50 is major trend, works best from D1, H4 does not own major trend, and when D1 says buy while H4 says sell, follow D1. Core V2 uses D1/MA50 as higher structural/trend reference but its standalone H1 Re-Entry owner contract deliberately blocks silent fallback to D1 when H4 has `NO_OWNER`.

Preliminary status: `POTENTIAL CONFLICT / STRATEGY DECISION` only if interpreted as universal execution precedence. Preserve on HOLD until exact scope is reconciled.

### HC-D06 — Cross-timeframe Double-Extreme -> higher-TF MHV relationship
Workbook states repeated same-side Extremes on H1 can indicate H4 MHV and that a valid higher-TF MHV changes how lower-TF Extremes are used. Core V2 contains generic MTF scaling and exact REM/RRE/REE contracts but does not currently encode this Double-Extreme inference as a canonical universal detector.

Preliminary status: `MISSING/HOLD` pending corroboration and deterministic definition.

### HC-D07 — Direction destination / hold-until-Re-Entry lifecycle
Workbook repeatedly states that after strong direction, if price reaches the outer BB without Momentum and Re-Entry has not yet occurred, the position may be held because Re-Entry is still expected. Core V2 models direction -> Re-Entry -> Momentum progression but does not currently encode this discretionary hold/TP exception as universal execution law.

Preliminary status: `PARTIAL/HOLD`.

### HC-D08 — No-Momentum after Re-Entry -> mandatory exit/reversal expectation
Workbook states direction -> Re-Entry -> no Momentum means close/TP because market will reverse, while Momentum implies another Re-Entry. Core V2 models same-cycle progression but does not yet expose this as a universal deterministic exit contract.

Preliminary status: `MISSING/HOLD` because wording contains deterministic market-outcome claims and requires reconciliation with primary operational PDF/Finale.

### HC-D09 — Lower-timeframe entry windows during the three-candle Re-Entry move
Workbook explicitly instructs moving to lower TFs during candles 2/3 of a higher-TF Re-Entry and gives H4->lower-TF examples. Core V2 preserves structural MTF scaling but project execution uses explicitly approved signatures.

Preliminary status: `PARTIAL`; educational MTF execution timing must not silently expand approved timeframe signatures.

### HC-D10 — Sideway -> Re-Entry and nested lower-TF replay
Workbook repeatedly states sideways forms Re-Entry and a large-TF sideways phase creates a new setup on a smaller TF. Core V2 Type-1 ranging semantics substantially cover the structural part, but nested replay wording is broader than current approved execution contracts.

Preliminary status: `COVERED/PARTIAL`.

## Explicit NON_CORE material

The following workbook material is not eligible to change universal Strategy Core without a separate user decision:

- MT4 menu-click instructions, chart colors and line thickness cosmetics;
- example instrument selection (`EUR/USD`);
- account splitting/growing/withdrawal workflow on page 19;
- discretionary lot-size language such as “lot besar” as a strategy rule;
- news-event trading instructions. The project explicitly does not use a news filter as BBMA Core logic;
- absolute predictive wording (for example “100%” / “pasti”) is preserved as source wording but is not converted into guaranteed software behavior merely because it appears in the workbook.

## Immediate result

The 19-page source has now been promoted from an unindexed repository binary to an **active audited evidence source**. The audit has already identified material candidate deltas, especially horizontal-BB behavior, named Mid-BB zones, D1/MA50 precedence wording, cross-TF Double-Extreme->MHV inference, and post-Re-Entry no-Momentum lifecycle behavior.

**Coverage percentage is intentionally not fabricated in this checkpoint.** Exact coverage remains blocked until the atomic row ledger is complete. Publishing an invented numerator/denominator would defeat the purpose of this forensic audit.

## Next autonomous gate

1. Build the atomic rule ledger for all 19 pages.
2. Map every applicable row to an exact Core V2 section or mark `PARTIAL/MISSING/HOLD`.
3. Deduplicate summary-page restatements without deleting provenance.
4. Reconcile every material delta against primary `Oma ally BBMA - AL.pdf`, secondary `BBMA technique.pdf`, Finale V01-V07 and existing conflict register.
5. Publish exact `covered / applicable = coverage%`.
6. Promote Core V2 -> V2.x only for non-conflicting source-backed clarifications. Any material strategy conflict remains HOLD for user decision.
