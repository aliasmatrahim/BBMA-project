# BBMA Home Course Reconciliation Audit — 2026-08-24

## Scope
Source reviewed: user-supplied `333531988-BBMA-Home-Course.pdf` (19-page BBMA Home Course Workbook).
Baseline: `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md` plus accepted Finale V01–V07.

This audit is evidence reconciliation only. It does NOT silently modify Strategy Core or EA source.

## Executive result
The Home Course strongly corroborates the canonical cycle and adds materially clearer operational statements in five areas: signal-based layering/additional entries, MTF parent/child behavior, D1/MA50 major-trend ownership, Re-Entry strength/timing, and lifecycle-dependent TP/hold behavior.

Several statements are direct enough to justify a future Core-V2 amendment, but they must be integrated with provenance and without converting discretionary phrases such as `lot besar`, `pasti`, or `100%` into unsupported numeric EA rules.

## HC-01 — Canonical cycle — STRONG CORROBORATION
Workbook summary explicitly gives:
`Extreme -> TP Wajib -> MHV -> CS Arah -> Reentry -> Momentum -> Reentry`.
It also calls this repeating structure the market/mainframe cycle.

Effect: strengthens existing Core V2 cycle; no contradiction.

## HC-02 — Signal-based layering / additional entry — NEW EXPLICIT OPERATIONAL EVIDENCE
Lesson 10 explicitly states:
- Reentry is `tempat menambah entry level ke-2`; level 1 is the MHV retest entry.
- Within an H4 setup/candle window, move to smaller TF to find additional entries in the higher-TF direction.
- D1 SELL context: smaller-TF retracements are SELL opportunities.
- If higher-TF MHV is complete, lower-TF Extreme can be used as an entry without waiting for another lower-TF MHV.

Accepted interpretation candidate:
BBMA supports signal-based pyramiding/additional entries. It does NOT support fixed-distance grid, averaging by drawdown, or lot-multiplier martingale.

Important: `lot besar` versus `lot kecil` is qualitative source language. No numeric multiplier/risk percentage is supplied and none may be invented.

## HC-03 — D1/MA50 major-trend ownership — MATERIAL CLARIFICATION
Lesson 10 states:
- major trend = MA50;
- MA50 works properly from minimum Daily (D1);
- H4 does not carry the major trend;
- if D1 says BUY and H4 says SELL, follow D1;
- D1 candle close determines the next day's movement context;
- Extreme against major trend is weak/not strong.

This is stronger than the current generic Core wording that MA50 is a higher structural/trend reference.

Potential architecture impact:
Current F4 policy allowing H4 as immediate parent for standalone H1 Re-Entry may remain useful for immediate setup ownership, but Home Course evidence means H4 should not be labelled `major trend`. D1/MA50 conflict handling now requires explicit reconciliation before any code change.

Do NOT automatically make D1 a hard gate for every trade yet: source also teaches H4 -> lower-TF additional entries. Separate `major-trend context` from `immediate setup parent`.

## HC-04 — MTF hierarchy and nested cycles — STRONGER DIRECT EVIDENCE
Workbook explicitly teaches:
- H4 setup -> seek entries on smaller TF during the H4 candle / expected movement window;
- D1 setup -> use smaller-TF retracements in D1 direction;
- double H1 Extreme can indicate H4 MHV;
- when H4 MHV is valid, lower-TF behavior changes and repeated lower-TF Extreme may be directly actionable;
- sideway on a large TF forms new setup(s) on smaller TF.

Effect: strongly supports nested parent/child cycle model and shows that TF stages need not be identical simultaneously.

## HC-05 — Re-Entry quality hierarchy — MATERIAL CLARIFICATION
Workbook states:
- CS close not beyond MA5/MA10 is Re-Entry condition;
- confluence with MA5 + MA10 + Mid BB is a strong/high-quality Re-Entry;
- MA5 + MA10 + Mid BB + MA50 is described as even stronger / `no compromise` in trend-change context;
- Re-Entry at MA5/MA10/Mid BB is associated with a minimum three-candle movement expectation on that timeframe;
- normally first Re-Entry candle is confirmation; second candle is entry.

Coding caution:
`minimum 3 candles` is instructional expectation, not automatically a guaranteed holding period or TP formula. `lot besar` is not a numeric sizing rule.

## HC-06 — Momentum -> Re-Entry recurrence — DIRECT CORROBORATION
Workbook explicitly states:
`Arah -> Reentry -> Momentum`; when Momentum occurs, another Re-Entry follows; Momentum can therefore generate continuing Re-Entry opportunities.

Effect: strengthens existing repeated same-cycle Re-Entry/pyramiding interpretation.

## HC-07 — Lifecycle-dependent TP / hold rules — MATERIAL NEW CLARITY
Workbook distinguishes several cases:
1. Extreme entry: mandatory TP at MA5/MA10; farthest Mid BB.
2. MHV entry: TP is negotiable; next candle outside BB (Momentum) can justify holding, while close inside BB is described as a reason to close because market can reverse.
3. Arah -> Re-Entry -> no Momentum: close/TP; market expected to reverse.
4. Arah -> no Re-Entry yet: position may be held while waiting for required Re-Entry.
5. MHV -> strong Arah directly to outer BB without Re-Entry: source says no TP yet; wait for Re-Entry.
6. After Re-Entry, if no Momentum follows: TP is required.

Impact on F7:
This source materially improves lifecycle exit provenance. It supports structural exit/hold logic more directly than a universal fixed outer-BB TP. It still does NOT provide a universal broker hard-SL formula.

## HC-08 — Momentum timing — DIRECT BUT CONTEXT-SENSITIVE
Workbook states that after a Momentum candle closes, next/second candle can be entered, with lower-TF same-direction setup confirmation. News examples are included.

Do not convert news-specific teaching into a news filter; project Core excludes news filtering unless separately approved.

## HC-09 — Weekly context — SUPPORTING EVIDENCE
Workbook says when Daily and Weekly major trend are down, an upward news move should not be followed against them. This confirms Weekly appears as broader trend context in teaching.

It does not by itself require adding W1 as an EA processing timeframe.

## HC-10 — BB state clarification — DIRECT SOURCE
Workbook differentiates flat BB from directional/vertical BB. Outside-BB close in directional BB is Momentum/continuation; flat BB has different behavior and can precede a large expansion.

Effect: corroborates F5 / current BB-state distinction.

## Items that must NOT be converted literally into deterministic EA rules
- `price pasti`, `100%`, or guaranteed wording;
- `lot besar` / `lot kecil` without numeric definition;
- news-driven entry behavior as a mandatory filter;
- account-splitting/money-management lesson as Strategy Core;
- a universal three-candle guaranteed move;
- a universal hard SL: workbook does not specify one.

## Conflict / reconciliation queue
### R1 — D1 major trend vs H4 immediate parent
Need architecture distinction:
- D1/MA50 = major-trend context;
- H4 can still be immediate setup parent for H1/lower-TF entries.
Decide whether D1 disagreement is a hard block, quality downgrade, or only context. Do not change code until this is explicitly resolved.

### R2 — Existing F7 TP mapping
Re-audit M17 against Home Course lifecycle exits. Current universal/combo TP assumptions must not override direct Home Course distinctions between Extreme TP, MHV negotiable TP, no-Momentum exit, and hold-until-Re-Entry behavior.

### R3 — Layering implementation
Audit current TradeLockMode and candidate deduplication to ensure legitimate new same-direction, source-valid Re-Entry/additional-entry signals are not incorrectly blocked. Any implementation must be signal-triggered, not grid-triggered.

### R4 — MTF lower-TF entry completion
Home Course gives explicit H4->lower-TF and D1->lower-TF additional-entry teaching. Compare current fixed D1/H4/H1/M15 architecture with this principle without automatically adding M5 or W1.

## Recommended next actions
1. Amend Source of Truth only after resolving R1–R4 with provenance labels.
2. Re-open F7 exit audit using Home Course as original-source evidence.
3. Audit signal-based layering behavior in current EA.
4. Audit D1/MA50 ownership semantics separately from H4 immediate-parent semantics.
5. Preserve current runtime candidate until strategy changes are approved and then require fresh compile/runtime validation.
