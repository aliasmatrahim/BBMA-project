# P3 Core V2 Strategy Audit

Date: 2026-08-22  
Branch: `blueprint-dev`  
Authoritative Core baseline: `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`  
Active implementation reviewed: `blueprint/source/BBMA_EA.mq4` blob `32fac8de5ccf10c3c70c1adc4aed66604df8f811`

## Scope
This audit is **BBMA Strategy Core only**. It reviews the active implementation and relevant locked contracts against Source of Truth V2. Money management, portfolio risk, trade lock, dashboard, scheduler, broker execution plumbing and other EA-management features are excluded except where a boundary must be identified.

Classification:
- `MATCH` — current implementation expresses the accepted Core rule.
- `SPEC NEEDS CLARIFICATION` — source intent is clear enough to expose a gap, but not deterministic enough to authorize a code rule without a project specification decision.
- `REQUIRED CORE FIX` — active implementation materially contradicts an accepted Core rule.
- `VERIFY` — likely semantic/runtime mapping issue; do not change code until measured.
- `OUTSIDE CORE` — implementation policy exists but is not certified as universal Core by V2.

## Executive result
The post-Finale Core does **not** require a wholesale strategy rewrite. M06, M10, M13, M14, M15 candidate-set semantics and M16 owner-aware freshness are broadly aligned. The largest material divergence is M09 MHV/MLV. Two additional source-governance gaps require specification work before patching: the maturity definition of an Extreme when it is used inside REM/REE, and the exact higher-timeframe/context gate for standalone H1 Re-Entry.

### Severity summary
| ID | Area | Result | Priority |
|---|---|---|---|
| CV2-01 | M06 indicator/data producer | MATCH | NONE |
| CV2-02 | M07 flat/horizontal BB classification | REQUIRED CORE SUPPORT FIX | MEDIUM |
| CV2-03 | M08 Extreme raw detector | MATCH for strict raw condition; SPEC NEEDS CLARIFICATION for combination maturity | HIGH |
| CV2-04 | M09 MHV/MLV outer-BB invalidation | REQUIRED CORE FIX | CRITICAL |
| CV2-05 | M09 MHV/MLV construction/body/retest ownership | REQUIRED CORE FIX / REDESIGN | CRITICAL |
| CV2-06 | M09 duplicate MHV vs MLV semantics | REQUIRED CORE FIX / CANONICALIZATION | HIGH |
| CV2-07 | M10 CSM/eCSD/CSD | MATCH | NONE |
| CV2-08 | M11 trend helper | DORMANT / NOT A VALID FINAL CONTEXT GATE | LOW |
| CV2-09 | M12 Type 1 context | SPEC NEEDS CLARIFICATION then FIX | HIGH |
| CV2-10 | M12 Types 2–4 | MATCH | NONE |
| CV2-11 | Re-Entry first-validation/second-entry wording | VERIFY | MEDIUM |
| CV2-12 | Higher-timeframe context for standalone H1 RE | SPEC NEEDS CLARIFICATION | HIGH |
| CV2-13 | M13/M14 REM-RRE-REE signatures | MATCH | NONE |
| CV2-14 | M15 entry-mode candidate authority | MATCH | NONE |
| CV2-15 | M16 owner-aware freshness/invalidation | MATCH, but inherits upstream owner defects | NONE directly |
| CV2-16 | M17 SL/TP provenance | OUTSIDE CORE / SOURCE BOUNDARY | MEDIUM SOURCE-GOVERNANCE |

---

## CV2-01 — M06 indicator/data producer
**Result: MATCH.**

Active source produces the expected MA5 High, MA10 High, MA5 Low, MA10 Low, EMA50 and BB20/deviation-2 Close-based structure under the existing source-aligned M06 contract. No Core V2 correction is identified here.

## CV2-02 — M07 flat/horizontal BB classification
**Result: REQUIRED CORE SUPPORT FIX — MEDIUM.**

`DetectBBState()` currently maps:
- width ratio `< 0.9` -> `BB_SQUEEZE`;
- `> 1.1` -> `BB_EXPANDING`;
- `0.9..1.1` -> `BB_CONTRACTING`;
- remaining branch -> `BB_FLAT`.

For valid positive width ratios, the `BB_FLAT` branch is effectively unreachable. Source of Truth V2 gives flat/horizontal BB explicit semantic importance because an outside-BB close under flat/horizontal BB is not directional Momentum/CSM.

Impact is currently limited because M10 `DetectCSM()` independently requires width expansion plus directional BB movement. Therefore this is not presently a proven CSM trading leak, but the state engine itself is semantically incomplete and should be repaired before other modules rely on `BB_FLAT`.

## CV2-03 — M08 Extreme
**Result: MATCH for strict raw condition; SPEC NEEDS CLARIFICATION — HIGH for combination maturity.**

Current raw detector correctly keeps the stricter accepted condition:
- SELL: MA5 High or MA10 High outside Top BB; reject if the current candle closes outside Top BB.
- BUY: MA5 Low or MA10 Low outside Low BB; reject if the current candle closes outside Low BB.

Standalone Extreme remains non-executable, which is correct because Source of Truth V2 requires reversal confirmation plus retest and the unresolved Finale exceptions remain HOLD.

However, the same M08 raw Extreme snapshot is eligible as the `Extreme` component of REM/REE. Source of Truth V2 states that reversal-candle confirmation is required for the normal Extreme context, while the current project intentionally has no deterministic reversal-candle algorithm. This creates a definition gap: **what maturity level must an Extreme reach before it is allowed to satisfy an executable REM/REE component?**

Do not invent a candle-pattern rule. Resolve this in the Core specification first. Until then, Mode 2 combination quality cannot be certified as fully Source-of-Truth-V2 compliant.

## CV2-04 — M09 outer-BB invalidation
**Result: REQUIRED CORE FIX — CRITICAL.**

Source of Truth V2 is explicit: MHV/MLV becomes void when price breaks and closes outside the relevant outer BB.

Active source defines `MarkMLVVoid()` but `DetectMLV_State()` does not call it for a candidate or confirmed MLV when the source-timeframe candle closes outside the relevant outer BB. A confirmed MLV can therefore remain owner-valid until time expiry even after a source-defined void event.

This is directly execution-relevant because M15 MLV is a required REM component and M16 trusts the M09 owner state.

Required future repair: source-timeframe outer-BB close must immediately void the matching MHV/MLV owner state before it can participate in a new REM decision.

## CV2-05 — M09 pattern construction / body / retest ownership
**Result: REQUIRED CORE FIX / REDESIGN — CRITICAL.**

Current candidate construction is hard-coded to:
- current High/Low versus bar `+2`;
- fixed `< point * 10` proximity;
- synthetic neckline offset by `point * 5`;
- only `DoubleTop` / `DoubleBottom` pattern labels.

Source of Truth V2 instead emphasizes:
- formation after Extreme / TP phase;
- loss-of-volume context;
- highest/lowest **candle body or equivalent marked reference** for retest;
- double/triple morphology as supported forms, not a mandatory fixed formula;
- H&S-like morphology as an example only.

The current fixed-point formula is an engineering invention that is narrower than the accepted Core and does not encode the Core body/retest ownership. M09 needs one canonical source-aligned owner/state model rather than incremental patching of the existing synthetic pattern formula.

## CV2-06 — MHV vs MLV duplicate semantics
**Result: REQUIRED CORE FIX / CANONICALIZATION — HIGH.**

Source of Truth V2 standardizes `MHV` and `MLV` as terminology aliases for the same loss-of-volume setup family unless future evidence distinguishes them.

The active source still has both `SIGNAL_MHV` and `SIGNAL_MLV`, plus a separate raw `DetectMHV()` that uses close-vs-MA5 and MA5 slope while the persistent lifecycle is owned by `DetectMLV_State()`.

`DetectMHV()` does not encode prior Extreme/TP context, outer-BB validity or the retest/body structure. This allows two different meanings for what V2 treats as one setup family.

Required future repair: choose one canonical persistent owner model and either remove/demote the legacy raw detector or make it a non-authoritative alias/output of the same canonical state.

## CV2-07 — M10 Momentum / eCSD / CSD
**Result: MATCH.**

`DetectCSM()` requires:
- close outside the relevant outer BB;
- BB width expansion;
- directional Mid/outer BB movement.

This matches the accepted expanding/directional-BB Momentum semantics and avoids treating a flat-BB outside close as Momentum.

`DetectECSD()` requires the relevant MA5/10 cross; `DetectCSD()` adds Mid-BB cross. Raw direction signals are not directly executable by M15. No Core V2 fix is required.

## CV2-08 — M11 trend helper
**Result: DORMANT / NOT A VALID FINAL CONTEXT GATE.**

`GetTrend()` reduces trend to Close versus EMA50, and `TimeframeData.trend` stores the same simple classification. In the active source these values are not consumed by the final Strategy-Core eligibility path.

Therefore M11 is not currently enforcing Source of Truth V2 multi-timeframe context. Do not treat the existing helper as proof that higher-timeframe alignment is implemented.

No immediate code change is required until CV2-12 is specified.

## CV2-09 — M12 Type 1 context
**Result: SPEC NEEDS CLARIFICATION then FIX — HIGH.**

Source of Truth V2 states that Type 1 forms after a rise/fall and sideways/ranging behaviour, then uses the relevant MA5/10 High/Low support/resistance cluster.

Current `DetectReEntry_Type1()` checks only `HasReEntryMAClusterTouch()`. A qualifying closed candle can therefore become confirmed Type 1 without any encoded evidence of the preceding rise/fall + sideways/ranging context.

The source wording is real but does not provide a deterministic numeric definition for the prior movement/ranging phase. Do not invent ADX, range thresholds or arbitrary candle counts. First define a source-faithful deterministic context contract; then patch M12.

This gap can cause over-classification because Type 1 is evaluated before Type 3 and Type 4 in `DetectReEntry_Master()`.

## CV2-10 — M12 Types 2–4
**Result: MATCH.**

- Type 2: MA5/10 + Mid BB confluence, MA50 strengthens, three consecutive qualifying candles, then MA-cluster touch.
- Type 3: CSM first, then later retrace to MA5 or MA50.
- Type 4: CSD first, then later retrace to the relevant MA5/10 cluster.

No new Core V2 correction is identified in these type-specific lifecycle paths.

## CV2-11 — first validation candle / second entry candle
**Result: VERIFY — MEDIUM.**

M12 stores confirmation metadata and `EntryPrice` from the fully closed validation candle. Actual broker execution later uses live ASK/BID after that source candle is already closed. Operationally this may already mean “first candle validates, entry occurs during the next candle.”

Do not add an extra waiting candle. Verify with source-candle timestamp, M15 decision timestamp and actual `OrderOpenTime()` before changing timing semantics. Metadata naming (`ConfirmationCandle` and `EntryCandle` being set to the same closed candle) may need clarification even if runtime timing is already correct.

## CV2-12 — higher-timeframe context for standalone H1 Re-Entry
**Result: SPEC NEEDS CLARIFICATION — HIGH.**

Source of Truth V2 requires BBMA to be read across related timeframes and emphasizes higher-timeframe ownership/context. The existing M12 contract also explicitly deferred higher-timeframe trend alignment to downstream final eligibility.

The active final path does not consume `TimeframeData.trend` or `GetTrend()` at all. M15 therefore accepts a confirmed H1 Re-Entry based on owner validity and EntryMode only; there is no explicit higher-timeframe/context contract for the standalone Mode-1/Mode-2 H1 Re-Entry candidate.

This is a real specification omission, but the source does not give a single universal numeric “trend filter” formula. Do not invent EMA-only, score-based or other external filtering. Define the exact BBMA higher-timeframe context rule first, then decide whether M12 metadata or M15 final eligibility owns it.

## CV2-13 — M13/M14 REM/RRE/REE
**Result: MATCH, subject to upstream component validity.**

Exact signatures match Source of Truth V2:
- REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV.
- RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme.
- REE = D1 Re-Entry + H4 Extreme + H1 Extreme.

M14 validates exact types/timeframes and same direction without inventing strict cross-timeframe chronology. No signature rewrite is justified by Finale.

However, a structurally correct signature is only as trustworthy as its component owners. CV2-03 and CV2-04/05/06 therefore directly affect Mode 2 combination trust.

## CV2-14 — M15 final candidate authority / EntryMode
**Result: MATCH.**

Current eligible candidate set is correct:
- Mode 1: confirmed H1 Re-Entry only.
- Mode 2: confirmed H1 Re-Entry + validated REM/RRE/REE.

Raw Extreme, MHV/MLV, CSD/eCSD and CSM are not standalone executable candidates. Simultaneous eligible BUY and SELL candidates produce no decision rather than an invented winner. Same-direction canonicalization is bookkeeping, not a quality ranking.

No EntryMode candidate-set change is required from Core V2.

## CV2-15 — M16 owner-aware freshness and invalidation
**Result: MATCH at architecture level; inherits upstream defects.**

M16 validates exact owner identity for Re-Entry, MLV and Extreme components, respects owner expiry, and applies later same-timeframe CSM invalidation to stored Extreme state. It does not use the old generic M15 expiry formula.

No direct M16 Core fix is identified. But M16 cannot repair a semantically wrong owner: an M09 state that should already have been voided can still pass M16 because the owner itself remains `MLV_CONFIRMED`/valid.

## CV2-16 — M17 SL/TP provenance boundary
**Result: OUTSIDE CORE / SOURCE-GOVERNANCE ITEM — MEDIUM.**

Source of Truth V2 does not establish a universal executable SL/TP contract for H1 Re-Entry, REM, RRE and REE. It only adds the normal standalone-Extreme TP-Wajib clarification, while standalone Extreme remains non-executable.

The current M17 contract correctly labels its executable Re-Entry BB destination as `FORUM_SUPPORTED` and its wick-plus-point hard stop as `EA_SAFETY`; they are not claimed as explicit PDF Core.

Therefore this audit does **not** call the current M17 mapping a Core V2 match or mismatch. It is a separate approved project execution policy. If project governance requires every executable SL/TP rule to be certified specifically as Strategy Core, additional source resolution is required before that claim can be made.

`MinRRRatio`, MaxSL, broker StopLevel/FreezeLevel and similar risk/execution guards are outside this Strategy-Core audit.

---

## Required action queue from this audit

### P0 / CRITICAL — M09 source alignment
1. Define one canonical MHV/MLV owner-state model.
2. Add source-timeframe outer-BB close invalidation for candidate and confirmed state.
3. Replace the synthetic High/Low + fixed-point neckline formula with a source-faithful body/retest ownership model.
4. Preserve descriptive morphology without making a single double-top/bottom formula mandatory.
5. Remove/demote the independent legacy `DetectMHV()` semantics so MHV/MLV cannot disagree.

### P0 / HIGH — Core specification closure before code
1. Define the maturity contract for an Extreme used as a REM/REE component: raw MA-outside signal versus reversal-confirmed Extreme context.
2. Define the deterministic Type-1 “after rise/fall + sideways/ranging” context without adding non-BBMA indicators or arbitrary filters.
3. Define the exact higher-timeframe/context requirement for standalone H1 Re-Entry and its owning module.

### P1 / MEDIUM
1. Repair M07 `BB_FLAT` reachability/classification.
2. Runtime timestamp audit for first-validation-candle / second-entry-candle semantics.
3. Decide whether M17's non-Core provenance is acceptable as project execution policy or whether stronger Core-source SL/TP evidence is required.

## Explicit non-fixes
Do not change these merely because Finale was added:
- M10 expanding/directional-BB Momentum rule;
- eCSD/CSD semantics;
- Re-Entry Type 2 three-candle confluence;
- Type 3 CSM -> later retrace lifecycle;
- Type 4 CSD -> later retrace lifecycle;
- REM/RRE/REE exact signatures;
- Mode 1 / Mode 2 eligible candidate set;
- M15 opposite-direction no-winner policy;
- M16 owner-aware expiry model.

## Final status
**CORE V2 STATIC AUDIT: COMPLETE WITH MATERIAL FINDINGS.**

The EA is not yet eligible to be called fully Core-V2 strategy-compliant because M09 has critical source-alignment defects and two high-value semantic contracts remain under-specified (Extreme maturity in combinations and higher-timeframe/Type-1 context). No strategy code is changed by this audit.