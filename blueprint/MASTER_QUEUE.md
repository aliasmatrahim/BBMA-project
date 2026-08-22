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
Status: **RESOLVED — USER APPROVED**
Source: `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-03
Decision record: `blueprint/decisions/CORE_V2_F2_EXTREME_MATURITY_DECISION.md`
Decision:
- raw Extreme alone is not sufficient for executable REM/REE;
- Extreme used as REM/REE component must be **reversal-confirmed**;
- standalone Extreme entry still requires the later **retest** stage;
- classification: **SOURCE-INFERRED / STRONG HINT**, not a verbatim source rule specifically defining REM/REE maturity.
Remaining dependency before code: define a deterministic source-faithful reversal-confirmation contract. Do not invent a candle pattern.

#### CORE-V2-F3 — Re-Entry Type 1 context
Priority: **HIGH**
Status: **SPECIFICATION PHILOSOPHY RESOLVED — USER APPROVED; CODE PATCH/AUDIT STILL PENDING**
Source: `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-09
Decision record: `blueprint/decisions/CORE_V2_F3_TYPE1_CONTEXT_DECISION.md`
Locked decisions:
- Type 1 requires `prior rise/fall -> sideways/ranging -> MA5/MA10 retest -> valid close-side`;
- MA5/MA10 touch alone is insufficient;
- sideways/ranging is BBMA structural ranging, not `BB_FLAT` alone;
- `BB_FLAT` may be supporting evidence only;
- no fixed minimum candle count is required; structural completion governs maturity;
- qualifying prior rise/fall must be evidenced by source-valid BBMA direction/momentum state (`eCSD`, `CSD`, or `CSM/Momentum`) under its own contract;
- transition into ranging is owner/state based: prior direction/momentum -> active momentum ceases/pauses -> retrace/consolidation toward relevant MA5/MA10;
- one non-CSM candle alone is insufficient proof of ranging;
- pending Type 1 uses structural invalidation: MA5/MA10 close-side failure, same-direction momentum resumption/reset, opposite source-valid direction/momentum, or transfer to exact Type 3/Type 4 ownership;
- owner lifetime has **no generic fixed candle expiry** and remains valid only while the same authoritative BBMA structure/cycle survives;
- age may be logged but is not a BBMA validity rule.
Constraint: implementation must use BBMA-owned state/owner transitions; no RSI/ADX/ATR/fixed-pip or timer heuristics as disguised Core rules.
Next action for F3: patch/audit M12 only after the remaining higher-priority Core specification closures are reconciled; do not alter code during specification review.

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
Dependency: CORE-V2-F4 must be resolved and F3 implemented/audited before Mode 1 can be declared source-compliant.

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
2. Resolve CORE-V2-F4 higher-timeframe H1 Re-Entry context.
3. Define deterministic reversal-confirmation semantics required to implement the already-approved CORE-V2-F2 maturity decision.
4. Implement/audit CORE-V2-F3 Type 1 state/owner contract and repair CORE-V2-F1 M09 MHV/MLV against the resolved canonical Core contract.
5. Repair CORE-V2-F5 BB-flat classification and run CORE-V2-F6 timing verification.
6. Re-run Core V2 static audit until no critical/high Strategy-Core mismatch remains.
7. Complete P3-M1 Mode 1 end-to-end compliance closure and opposite-direction cycle audit.
8. Verify sequential risk-budget admission.
9. Complete P3 Step 5 live runtime closure evidence.
10. Address observability/UI items: invalid-lot diagnostics and dashboard active-count refresh.
11. Recompile and run regression/backtest gates before optimization or win-rate based analysis.

## Governance
- GitHub records are authoritative over chat recollection.
- BBMA strategy semantics must remain governed by `docs/references/` and locked contracts.
- `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md` is the active consolidated developer-facing Core reference; unresolved HOLD/UNCERTAIN items remain excluded.
- No optimization, score-based entry authority, win-rate gating, RSI/MACD/Stochastic/ADX/news/correlation filters, or unsupported strategy additions may be introduced through these queue items.
- Completed queue items must receive a dedicated audit/fix/closure record and then be marked here.
