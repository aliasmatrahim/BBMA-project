# BBMA Master Project Queue

Status owner: `blueprint-dev`
Reconciled: 2026-08-22

## Purpose
This file is the canonical work queue for active development. It complements `blueprint/CURRENT.md` and prevents chat-only decisions from becoming the only record of pending work.

## Reconciled phase status

- P0 Architecture Repair — COMPLETE at locked patch/contract level.
- P1 Integration Verification / compile-clean canonicalization — COMPLETE / PASS at recorded level.
- P2 Functional / cross-module audit series — RECORDED with Step 2–18 audit/re-audit/fix artifacts present in repository; treat individual record status as authoritative per file.
- P3 Runtime Validation — ACTIVE. Steps 1–4 have closure records. Step 5 source/compile work exists, but final live MT4 runtime closure remains pending until the Step 5 checklist evidence is satisfied. PairID/magic static validation is PASS. Latest runtime source also includes the M17 market-price-before-SLTP fix.
- BBMA Strategy Core V2 static audit — COMPLETE WITH MATERIAL FINDINGS. Authoritative record: `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md`.

## Priority queue

### P0 — Strategy correctness gate

#### CORE-V2-F1 — M09 MHV/MLV source alignment
Priority: **CRITICAL**
Status: QUEUED FROM CORE V2 AUDIT
Source: `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-04/CV2-05/CV2-06
Required scope:
- one canonical MHV/MLV owner-state model;
- source-timeframe outer-BB close must void candidate/confirmed MHV/MLV;
- replace synthetic High/Low + fixed-point neckline construction with source-faithful body/retest ownership;
- morphology must not be restricted to an invented mandatory double-top/bottom formula;
- remove/demote independent legacy `DetectMHV()` semantics so MHV and MLV cannot disagree.
Constraint: audit/spec first, then patch. Do not invent arbitrary pip thresholds and present them as BBMA rules.

#### CORE-V2-F2 — Extreme maturity inside REM/REE
Priority: **HIGH**
Status: SPECIFICATION CLOSURE REQUIRED BEFORE CODE
Source: `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-03
Problem:
- Source of Truth V2 requires reversal-candle confirmation for the normal Extreme context;
- active M08 raw Extreme is safely withheld from standalone execution but is still usable as a REM/REE component;
- project lacks a deterministic reversal-candle maturity algorithm.
Required action: define what maturity level an `Extreme` must reach before it can satisfy executable REM/REE. Do not invent a candle pattern from unsupported assumptions.

#### CORE-V2-F3 — Re-Entry Type 1 context
Priority: **HIGH**
Status: SPECIFICATION CLOSURE REQUIRED BEFORE CODE
Source: `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-09
Problem:
- Core V2 says Type 1 forms after rise/fall + sideways/ranging behaviour;
- active `DetectReEntry_Type1()` currently confirms from MA5/10 cluster touch/close-side only.
Required action: define a deterministic source-faithful context contract without adding RSI/ADX/range heuristics or arbitrary non-source filters; then patch M12 if required.

#### CORE-V2-F4 — Higher-timeframe context for standalone H1 Re-Entry
Priority: **HIGH**
Status: SPECIFICATION CLOSURE REQUIRED BEFORE CODE
Source: `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-12
Problem:
- Core V2 requires multi-timeframe reading/higher-timeframe context;
- M12 previously deferred this responsibility downstream;
- active final eligibility does not consume `GetTrend()`/`TimeframeData.trend` or any explicit higher-timeframe context gate.
Required action: define the exact BBMA context/alignment rule and owner. Do not reduce it to an invented EMA-only or score-based filter unless the Core source explicitly supports that mapping.

#### P3-M1 — Mode 1 Official BBMA Compliance Audit
Priority: CRITICAL / NEXT STRATEGY GATE AFTER CORE-V2 SPEC CLOSURE
Status: STATIC CORE COVERAGE PARTIAL; MODE-1-SPECIFIC END-TO-END/RUNTIME CLOSURE STILL QUEUED
Scope:
- EntryMode 1 (`RE_ENTRY_ONLY`) end-to-end compliance against `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`;
- M12 Re-Entry Type 1–4 semantics;
- H1 ownership and multi-timeframe context;
- cycle/direction authority;
- Powerful / Most Powerful Re-Entry interpretation where supported by source;
- M13 -> M14 -> M15 -> M16 selection/invalidation integrity;
- ensure no non-compliant Re-Entry can reach M17/M21/M19/M20/M22.
Rule: audit first; only create strategy fixes from evidence-backed deviations. Do not introduce win-rate heuristics or non-BBMA filters.
Dependency: CORE-V2-F3/F4 must be resolved before Mode 1 can be declared source-compliant.

### P1 — Core support / semantic verification

#### CORE-V2-F5 — M07 flat/horizontal BB state
Priority: MEDIUM
Status: QUEUED
Source: `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-02
Current issue: `BB_FLAT` is effectively unreachable in the current ratio branching. M10 CSM remains independently source-aligned, so this is not currently a proven entry leak, but the state classification must be repaired before other modules depend on it.

#### CORE-V2-F6 — Re-Entry validation-candle / entry-candle timestamp audit
Priority: MEDIUM
Status: VERIFY, NO CODE CHANGE YET
Source: `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-11
Evidence required: Re-Entry confirmation candle time, M15 decision time, and actual `OrderOpenTime()`.
Goal: prove whether current closed-candle processing already means “first Re-Entry candle validates, next candle executes.” Do not insert an extra full-candle delay without evidence.

#### CORE-V2-F7 — M17 SL/TP provenance decision
Priority: MEDIUM / SOURCE GOVERNANCE
Status: QUEUED FOR DECISION, NOT A CORE BUG CLAIM
Source: `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-16
Current contract explicitly separates `FORUM_SUPPORTED` TP and `EA_SAFETY` hard SL from PDF Core. Decide whether this provenance is acceptable as project execution policy or whether stronger Strategy-Core source evidence is required before calling executable SL/TP fully Core-derived.

### P1 — Opposite-direction / same-pair cycle integrity
Priority: HIGH
Status: QUEUED; dependency/overlap with P3-M1
Problem statement:
- runtime observation can show BUY and SELL positions on the same pair;
- determine whether this is a valid cycle transition with an older position still open, or opposite-direction leakage from one active authoritative cycle.
Audit path:
`M13 -> M14 -> M15 -> M16 -> M20/M22`
Evidence fields:
`Pair`, `Direction`, `CycleStartTime`, `DecisionID`, `SequenceHash`, decision state, cycle state, existing position direction.
Expected invariant to verify: one active authoritative BBMA cycle per pair must not simultaneously authorize contradictory directions unless an explicit, source-backed cycle transition has occurred.

### P1 — Sequential risk-budget admission
Priority: HIGH
Status: QUEUED
Purpose:
- confirm that when multiple valid decisions compete, higher-authority/selected decision consumes prospective risk budget first;
- subsequent trades are admitted only if cumulative prospective risk remains within M19/M20 limits;
- do not create a rule that rejects a second trade merely because its individual risk exceeds the first trade; use cumulative approved risk and strategy authority.

### P2 — REJ_INVALID_LOT diagnostics
Priority: MEDIUM
Status: QUEUED
Current behavior: multiple M21 failure causes collapse into `REJ_INVALID_LOT`.
Add observability only; do not change risk sizing semantics.
Capture at minimum:
`rawLot`, `normalizedLot`, `MinLot`, `MaxLot`, `LotStep`, `LotDigits`, `TickValue`, `TickSize`, SL distance, effective max lot, MMMode.
Desired reason tags include: `BELOW_MIN`, `ABOVE_MAX`, `STEP_MISMATCH`, `BROKER_SNAPSHOT_INVALID`, `MAXAUTOLOT_BELOW_MIN`, `FIXEDLOT_INVALID`.

### P2 — Dashboard active-trade count refresh
Priority: MEDIUM
Status: QUEUED
Observed symptom: dashboard can display 5 trades while only 3 are active.
Audit M25 display source and monitored/open-order compaction so dashboard derives active count from current exact-owned open positions rather than stale lifecycle state.
No strategy logic change.

## Active P3 closure dependency
Before declaring P3 complete, preserve the existing Step 5 closure rule in `P3_STEP5_RUNTIME_CLOSURE_CHECKLIST.md`. Tests A–D require direct runtime evidence; safety invariants E–F must remain satisfied.

## Execution order
1. Keep `CURRENT.md` + this queue reconciled.
2. Resolve Core V2 specification closures: CORE-V2-F2 (Extreme maturity), CORE-V2-F3 (Type 1 context), CORE-V2-F4 (higher-timeframe H1 Re-Entry context).
3. Repair CORE-V2-F1 M09 MHV/MLV against the resolved canonical Core contract.
4. Repair CORE-V2-F5 BB-flat classification and run CORE-V2-F6 timing verification.
5. Re-run Core V2 static audit until no critical/high Strategy-Core mismatch remains.
6. Complete P3-M1 Mode 1 end-to-end compliance closure and opposite-direction cycle audit.
7. Verify sequential risk-budget admission.
8. Complete P3 Step 5 live runtime closure evidence.
9. Address observability/UI items: invalid-lot diagnostics and dashboard active-count refresh.
10. Recompile and run regression/backtest gates before optimization or win-rate based analysis.

## Governance
- GitHub records are authoritative over chat recollection.
- BBMA strategy semantics must remain governed by `docs/references/` and locked contracts.
- `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md` is the active consolidated developer-facing Core reference; unresolved HOLD/UNCERTAIN items remain excluded.
- No optimization, score-based entry authority, win-rate gating, RSI/MACD/Stochastic/ADX/news/correlation filters, or unsupported strategy additions may be introduced through these queue items.
- Completed queue items must receive a dedicated audit/fix/closure record and then be marked here.
