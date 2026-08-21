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

## Priority queue

### P0 — Strategy correctness gate

#### P3-M1 — Mode 1 Official BBMA Compliance Audit
Priority: CRITICAL / NEXT STRATEGY GATE
Status: QUEUED
Scope:
- EntryMode 1 (`RE_ENTRY_ONLY`) end-to-end compliance against the locked BBMA Oma Ally source-of-truth;
- M12 Re-Entry Type 1–4 semantics;
- H1 ownership and multi-timeframe context;
- cycle/direction authority;
- Powerful / Most Powerful Re-Entry interpretation where supported by source;
- M13 -> M14 -> M15 -> M16 selection/invalidation integrity;
- ensure no non-compliant Re-Entry can reach M17/M21/M19/M20/M22.
Rule: audit first; only create strategy fixes from evidence-backed deviations. Do not introduce win-rate heuristics or non-BBMA filters.

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
1. Reconcile/maintain `CURRENT.md` + this queue.
2. Run `P3-M1 — Mode 1 Official BBMA Compliance Audit`.
3. Fix only critical/high findings from P3-M1, including opposite-direction leakage if confirmed.
4. Verify sequential risk-budget admission.
5. Complete P3 Step 5 live runtime closure evidence.
6. Address observability/UI items: invalid-lot diagnostics and dashboard active-count refresh.
7. Recompile and run regression/backtest gates before optimization or win-rate based analysis.

## Governance
- GitHub records are authoritative over chat recollection.
- BBMA strategy semantics must remain governed by `docs/references/` and locked contracts.
- No optimization, score-based entry authority, win-rate gating, RSI/MACD/Stochastic/ADX/news/correlation filters, or unsupported strategy additions may be introduced through these queue items.
- Completed queue items must receive a dedicated audit/fix/closure record and then be marked here.
