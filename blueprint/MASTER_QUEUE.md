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

### CORE-V2 integrated re-audit after F1–F6
Status: **STATIC RE-AUDIT PASS — METAEDITOR/RUNTIME EVIDENCE PENDING**
Record: `blueprint/P3_CORE_V2_STRATEGY_REAUDIT_20260822.md`
Result: original CV2-01..CV2-15 findings are either MATCH/DORMANT or statically resolved by F1–F6. CV2-16 remains F7 source-governance only, not a proven Strategy-Core code defect.
Next strategy gate: **P3-M1 Mode 1 Official BBMA Compliance Audit**.


### P0 — Strategy correctness gate

#### CORE-V2-F1 — M09 MHV/MLV source alignment
Priority: **CRITICAL**
Status: **CODE IMPLEMENTED / STATIC REGRESSION PASS — NATIVE METAEDITOR COMPILE + RUNTIME TRACE PENDING**
Source: `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-04/CV2-05/CV2-06
Decision record: `blueprint/decisions/CORE_V2_F1_MHV_MLV_LIFECYCLE_DECISION.md`
Locked decisions:
- MHV/MLV is one canonical structural lifecycle/owner-state model, not a one-candle detector;
- a prior source-valid Extreme in the same source timeframe/owner-cycle is mandatory;
- minimum parent maturity = `REVERSAL-CONFIRMED EXTREME`;
- normal TP-Wajib structural completion is mandatory before canonical MHV formation;
- loss of prior momentum is a developing structural failed-continuation state inside the relevant outer BB without source-valid Momentum/CSM; one ordinary non-Momentum candle is insufficient;
- concrete formation uses the most-extreme body during that phase plus the first closed move away from that side;
- prior Extreme SELL -> track lowest `BodyBottom=min(Open,Close)`; first later `CurrentClose > PreviousClose` establishes bottom-side MHV;
- prior Extreme BUY -> track highest `BodyTop=max(Open,Close)`; first later `CurrentClose < PreviousClose` establishes top-side MHV;
- move-away trigger candle is excluded from the accumulated body extreme;
- marked body freezes immediately at formation and cannot drift;
- retest completes on a later price-range/wick interaction with the frozen marked body: bottom-side `Low <= FrozenMarkedBody`, top-side `High >= FrozenMarkedBody`;
- no universal extra close-away, named pattern, mandatory double/triple morphology, eCSD/CSD or fixed candle count is added for formation/retest;
- MHV remains setup/context, not standalone direct entry authority;
- M15 MHV/MLV used in REM requires minimum `FORMATION ESTABLISHED + FROZEN MARKED BODY`; later MHV retest completion is not mandatory merely for the REM component;
- same-cycle eCSD/CSD advances the cycle and does not retroactively void completed MHV provenance;
- active MHV outer-BB/Momentum invalidation window closes when valid same-cycle eCSD/CSD takes direction ownership; later same-cycle Re-Entry/CSM/Momentum cannot retroactively erase completed MHV provenance;
- opposite RAW Extreme is only a new-cycle candidate;
- **opposite `REVERSAL-CONFIRMED EXTREME` on the same source timeframe atomically supersedes the old cycle**, after which old MHV/MLV provenance/frozen reference are historical-only and cannot satisfy new REM/current-cycle authority;
- no generic fixed candle/session/day expiry is used;
- double/triple top/bottom and H&S-like forms remain morphology/examples, not mandatory formulas;
- independent legacy `DetectMHV()`/MLV semantics must converge into one canonical M09 owner-state result.
Classification: **DIRECT SOURCE STRUCTURAL/SEQUENCE/LOSS-OF-MOMENTUM/BODY-RETEST/REM/CYCLE-RESTART CONCEPT + PROJECT DETERMINISTIC STATE-MACHINE / PROVENANCE / TURNING-POINT / FIXED-REFERENCE / COMPONENT-MATURITY / STAGE-BOUNDARY / ATOMIC-SUPERSESSION MAPPING**.
Constraint: implementation must reproduce the resolved contract without arbitrary pip thresholds, fixed-N expiry, generic consolidation heuristics, broker-order prerequisites, mandatory morphology, moving anchors, or unsupported extra REM gates.
Next action for F1: native MetaEditor compile and runtime lifecycle traces; static implementation/regression is complete.

#### CORE-V2-F2 — Extreme maturity inside REM/REE
Priority: **HIGH**
Status: **CODE IMPLEMENTED / STATIC REGRESSION PASS — NATIVE METAEDITOR COMPILE + RUNTIME TRACE PENDING**
Source: `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-03
Decision record: `blueprint/decisions/CORE_V2_F2_EXTREME_MATURITY_DECISION.md`
Locked decisions:
- maturity lifecycle is `RAW EXTREME -> REVERSAL-CONFIRMED EXTREME -> RETEST/ENTRY-READY EXTREME`;
- raw Extreme alone is not sufficient for executable REM/REE;
- Extreme used as REM/REE component must be at least **reversal-confirmed**;
- standalone Extreme entry requires the later **retest/entry-ready** stage;
- reversal confirmation uses closed source-TF candles with the minimal deterministic direction mapping: SELL `Close < Open`, BUY `Close > Open`;
- the first qualifying closed reversal-direction candle promotes `RAW -> REVERSAL-CONFIRMED`, provided accepted outside-BB/Momentum invalidation has not already voided the candidate;
- no mandatory previous-candle colour flip, named pattern, fixed two-/three-candle template, eCSD/CSD prerequisite, or universal close-back-inside-BB requirement is added;
- the reversal phase may continue structurally after first confirmation; provisional body reference may update only while that reversal phase remains active;
- retest starts on the first later closed candle whose close moves back toward the original Extreme/reference relative to the previous close: SELL `CurrentClose > PreviousClose`; BUY `CurrentClose < PreviousClose`;
- the retest-start candle is the first retest-phase candle and is excluded from the completed reversal-phase anchor;
- frozen body anchor across the completed reversal phase is SELL = highest `max(Open,Close)`; BUY = lowest `min(Open,Close)`;
- wick `High/Low` is not the body-anchor value;
- standalone retest is completed by price-range/wick interaction with the frozen body anchor **or** the relevant MA5 area; no universal extra close-side/named-pattern/second-confirmation rule is added;
- body anchor and MA5 are alternative source-supported retest references, not mandatory dual-touch confluence;
- if body anchor and MA5 are separated, the **first valid interaction with either** completes the retest; there is no body-first/MA5-first priority and no nearest-reference heuristic;
- accepted outside-BB/Momentum invalidation has priority over reversal/retest promotion and results in `VOID`;
- classification: component maturity is **SOURCE-INFERRED / STRONG HINT**; reversal/retest direction, phase, body-reference and first-valid-interaction predicates are **DIRECT SOURCE REQUIREMENT / SOURCE-DERIVED CONCEPT + MINIMAL DETERMINISTIC PROJECT MAPPING**.
Constraint: implementation must reproduce this lifecycle without arbitrary candle counts, named candlestick patterns, EMA/ATR/RSI filters, moving anchors, mandatory dual-touch, or invented target hierarchy.
Next action for F2: native MetaEditor compile and runtime lifecycle traces; static implementation/regression is complete.

#### CORE-V2-F3 — Re-Entry Type 1 context
Priority: **HIGH**
Status: **CODE IMPLEMENTED / STATIC REGRESSION PASS — NATIVE METAEDITOR COMPILE + RUNTIME TRACE PENDING**
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
Next action for F3: native MetaEditor compile and runtime Type1 lifecycle traces; static implementation/regression is complete.

#### CORE-V2-F4 — Higher-timeframe context for standalone H1 Re-Entry
Priority: **HIGH**
Status: **CODE IMPLEMENTED / STATIC REGRESSION PASS — NATIVE METAEDITOR COMPILE + RUNTIME TRACE PENDING**
Source: `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-12
Decision record: `blueprint/decisions/CORE_V2_F4_H1_RE_HTF_CONTEXT_DECISION.md`
Locked decisions:
- standalone H1 Re-Entry must not be treated as autonomous from higher-timeframe BBMA context;
- **H4 is the immediate parent/context owner** for standalone H1 Re-Entry in the approved intraday chain;
- D1 remains broader structural context but is not a universal hard gate for every standalone H1 Re-Entry;
- H4 compatibility is based on an **active authoritative BBMA directional/cycle state**, not the current H4 candle alone;
- raw H4 Extreme alone and raw H4 MHV/MLV alone are insufficient as directional authority;
- H4 uses an **inherited directional cycle owner**: direction signal establishes/advances ownership, while same-direction Re-Entry and CSM/Momentum inherit/continue the same owner;
- **valid H4 eCSD alone may establish H4 directional ownership** for same-direction H1 Re-Entry parent compatibility; CSD/Re-Entry/CSM strengthen or advance the same owner but are not mandatory prerequisites;
- eCSD remains directional context only and does not become direct entry authority;
- a valid opposite H4 `eCSD`, `CSD`, or `CSM/Momentum` causes **atomic owner handover**: the old H4 owner is superseded and the new opposite owner becomes authoritative on the closed-candle transition;
- simultaneous authoritative H4 BUY and SELL owners are not allowed;
- opposite raw Extreme/MHV alone do not establish the new directional owner;
- a neutral H4 candle does not erase an already-valid inherited H4 owner if that owner remains structurally valid;
- when H4 is truly **NO_OWNER**, standalone H1 Re-Entry execution is blocked until a compatible authoritative H4 owner exists;
- no-owner must not silently fall back to D1, MA50/Mid BB, candle color, generic price position or absence of an opposite signal;
- H4 owner lifetime is **purely structural with no generic fixed candle/time/day/session expiry**;
- restart/recovery uses **verified persisted checkpoint + deterministic closed-H4 replay**; checkpoint is cache/provenance aid, not unquestioned truth;
- if checkpoint/history cannot prove an authoritative owner, recovery resolves to `NO_OWNER` and standalone H1 execution remains blocked;
- recovered owner must match the owner the same closed-candle state machine would have produced under uninterrupted runtime.
Classification:
- H4 MTF/owner semantics: direct source principle + source-inferred/strong-hint project mapping;
- restart/recovery mechanics: EA engineering policy only, preserving the approved Core semantics.
Constraint: implementation must not invent EMA-only, score-based, timer-based, D1-fallback, or current-snapshot shortcuts.
Next action for F4: native MetaEditor compile and H4 owner/recovery runtime traces; static implementation/regression is complete.

#### P3-M1 — Mode 1 Official BBMA Compliance Audit
Priority: CRITICAL / STRATEGY GATE
Status: **STATIC END-TO-END COMPLIANCE PASS — NATIVE METAEDITOR + RUNTIME MODE1 TRACE PENDING**
Audit record: `blueprint/P3_M1_MODE1_OFFICIAL_BBMA_COMPLIANCE_AUDIT.md`
Scope:
- EntryMode 1 (`RE_ENTRY_ONLY`) end-to-end compliance against `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`;
- M12 Re-Entry Type 1–4 semantics;
- H1 ownership and multi-timeframe context;
- cycle/direction authority;
- Powerful / Most Powerful Re-Entry interpretation where supported by source;
- M13 -> M14 -> M15 -> M16 selection/invalidation integrity;
- ensure no non-compliant Re-Entry can reach M17/M21/M19/M20/M22.
Rule: audit first; only create strategy fixes from evidence-backed deviations. Do not introduce win-rate heuristics or non-BBMA filters.
Dependency: CORE-V2-F4 must be implemented/audited and F3 implemented/audited before Mode 1 can be declared source-compliant.

### P1 — Core support / semantic verification

#### CORE-V2-F5 — M07 flat/horizontal BB state
Priority: MEDIUM
Status: **CODE IMPLEMENTED / STATIC REGRESSION PASS — NATIVE METAEDITOR COMPILE + RUNTIME TRACE PENDING**
Source: `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-02
Implementation record: `blueprint/CORE_V2_F5_IMPLEMENTATION_AUDIT.md`
Resolved mapping: `BB_FLAT` is now a reachable geometric three-line horizontal state using one broker point only as numerical equality tolerance. Existing squeeze/expanding width thresholds are preserved; remaining non-flat valid near-width states remain contracting. M10 CSM remains independently source-aligned and was not changed by F5.
Next action for F5: native MetaEditor compile and focused runtime BB-shape trace; proceed to F6 timing verification before full Core re-audit.

#### CORE-V2-F6 — Re-Entry validation-candle / entry-candle timestamp audit
Priority: MEDIUM
Status: **STATIC TIMING VERIFIED / METADATA REPAIRED — NATIVE METAEDITOR + RUNTIME ORDER-TIME TRACE PENDING**
Implementation/audit record: `blueprint/CORE_V2_F6_TIMING_VERIFICATION_AUDIT.md`
Resolved mapping: the closed source-TF Re-Entry candle is the validation candle; M27 may execute during the immediately following live source-TF candle. No extra full-candle delay is added. `ReEntryData.EntryCandle` metadata now identifies that immediately following candle rather than duplicating `ConfirmationCandle`.
Runtime closure evidence still required: `ConfirmationCandle`, processing/decision time and actual `OrderOpenTime()`.

#### CORE-V2-F7 — M17 SL/TP provenance decision
Priority: MEDIUM / SOURCE GOVERNANCE
Status: QUEUED FOR DECISION, NOT A CORE BUG CLAIM
Source: `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-16
Current contract explicitly separates `FORUM_SUPPORTED` TP and `EA_SAFETY` hard SL from PDF Core. Decide whether this provenance is acceptable as project execution policy or whether stronger Strategy-Core source evidence is required before calling executable SL/TP fully Core-derived.

### P1 — Opposite-direction / same-pair cycle integrity
Priority: HIGH
Status: **BUG CONFIRMED / FIX IMPLEMENTED / STATIC REGRESSION PASS — METAEDITOR + RUNTIME TRACE PENDING**
Audit record: `blueprint/P3_OPPOSITE_DIRECTION_PAIR_INTEGRITY_AUDIT.md`
Finding: M15 already rejects contradictory eligible BUY/SELL candidates in one atomic scan. The observed BUY+SELL coexistence under `TradeLockMode=1` came from a reversed M22 lock predicate: mode 1 blocked same-direction adds and allowed opposite-direction orders.
Fix: `LOCK_SAME_DIRECTION` now means same-direction-only coexistence on the pair; an existing live EA-owned opposite direction rejects the new order with `REJ_TRADE_LOCK`. Mode 0 and mode 2 semantics remain unchanged.
Next action: native compile + focused TradeLock runtime trace; proceed to sequential cumulative risk-budget admission audit.

### P1 — Sequential risk-budget admission
Priority: HIGH
Status: **STATIC PASS — NO CODE FIX REQUIRED; RUNTIME MULTI-DECISION TRACE PENDING**
Audit record: `blueprint/P3_SEQUENTIAL_RISK_BUDGET_ADMISSION_AUDIT.md`
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
2. Implement/audit resolved CORE-V2-F1/F2/F3/F4 contracts in dependency-safe order.
3. Repair CORE-V2-F5 BB-flat classification and run CORE-V2-F6 timing verification.
4. Re-run Core V2 static audit until no critical/high Strategy-Core mismatch remains.
5. Complete P3-M1 Mode 1 end-to-end compliance closure and opposite-direction cycle audit.
6. Verify sequential risk-budget admission.
7. Complete P3 Step 5 live runtime closure evidence.
8. Address observability/UI items: invalid-lot diagnostics and dashboard active-count refresh.
9. Recompile and run regression/backtest gates before optimization or win-rate based analysis.

## Governance
- GitHub records are authoritative over chat recollection.
- BBMA strategy semantics must remain governed by `docs/references/` and locked contracts.
- `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md` is the active consolidated developer-facing Core reference; unresolved HOLD/UNCERTAIN items remain excluded.
- No optimization, score-based entry authority, win-rate gating, RSI/MACD/Stochastic/ADX/news/correlation filters, or unsupported strategy additions may be introduced through these queue items.
- Completed queue items must receive a dedicated audit/fix/closure record and then be marked here.