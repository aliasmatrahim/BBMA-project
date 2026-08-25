# BBMA Master Project Queue

Status owner: `blueprint-dev`
Reconciled: 2026-08-24

## Purpose
This file is the canonical work queue for active development. It complements `blueprint/CURRENT.md` and prevents chat-only decisions from becoming the only record of pending work.

## Reconciled phase status

- P0 Architecture Repair — COMPLETE at locked patch/contract level.
- P1 Integration Verification / compile-clean canonicalization — COMPLETE / PASS at recorded level.
- P2 Functional / cross-module audit series — RECORDED with Step 2–18 audit/re-audit/fix artifacts present in repository; treat individual record status as authoritative per file.
- P3 Runtime Validation — ACTIVE. Steps 1–4 have closure records. Step 5 source/compile work exists, but final live MT4 runtime closure remains pending until the Step 5 checklist evidence is satisfied.
- BBMA Strategy Core V2 — canonical source specification has been reopened/reconciled by the Home Course D1 major-trend evidence and F7 source work. Documentation/specification is intentionally ahead of frozen code in those newly reconciled areas.

## Priority queue

### D1 strategic-owner implementation gate
Priority: **HIGH / STRATEGY CORRECTNESS GATE**
Status: **SPECIFICATION RESOLVED / CANONICAL CONTRACTS RECONCILED / EA IMPLEMENTATION DEFERRED UNTIL P3 RUNTIME FREEZE IS RELEASED**
Decision records:
- `blueprint/decisions/HOME_COURSE_D1_MAJOR_TREND_VS_H4_IMMEDIATE_PARENT_RECONCILIATION.md`;
- `blueprint/decisions/HOME_COURSE_D1_TRANSITION_MAJOR_TREND_OWNER_DECISION.md`;
- reconciled `blueprint/decisions/CORE_V2_F4_H1_RE_HTF_CONTEXT_DECISION.md`.
Canonical contract:
- `blueprint/contracts/M11_D1_MAJOR_TREND_OWNER_CONTRACT.md`.
Reconciliation audit:
- `blueprint/CORE_V2_D1_CANONICAL_CONTRACT_RECONCILIATION_AUDIT_20260824.md`.

Locked specification:
- hierarchy = `D1 strategic owner -> H4 structural/setup parent -> H1/M15 execution structure`;
- D1 BUY confirmed = closed D1 `Close > MA50` + MA50 rising;
- D1 SELL confirmed = closed D1 `Close < MA50` + MA50 falling;
- otherwise-valid disagreement/flat/equality = `D1_TRANSITION`;
- invalid/missing D1 history = `D1_OWNER_UNRESOLVED`;
- transition/unresolved -> block all **new** strategy entries;
- previous confirmed D1 owner is diagnostic only during transition, not executable authority;
- H4 cannot override opposite/transition/unresolved D1;
- H4 `NO_OWNER` also remains a block for standalone H1; there is no D1-only fallback;
- REM signature remains H4 RE + H1 Extreme + M15 MHV/MLV; D1 gate is not a fourth component;
- RRE/REE D1 Re-Entry components do not replace D1 MA50 strategic-owner confirmation;
- D1 transition is not itself a live-position close rule.

Confirmed code gaps:
- M11 has no dedicated D1 owner implementation;
- active `TimeframeData.trend` uses price relative to EMA50 only and does not encode MA50 slope;
- standalone H1 code gate is H4-only;
- REM lacks separate D1 strategic gating;
- RRE/REE lack independent M11 D1-owner compatibility verification through M15/M16.

Future implementation sequence after freeze:
1. M11 producer state;
2. frozen D1 owner payload through M15;
3. M15 D1 strategic filter before final direction/canonical selection;
4. M16 frozen-owner verification without duplicate trend formula;
5. new unique left-aligned build identifier;
6. native MetaEditor 0E0W;
7. static cross-module/Core purity regression;
8. focused D1 runtime traces;
9. rerun P3-M1 compliance.


### CORE-V2 integrated re-audit after F1–F6
Status: **HISTORICAL STATIC RE-AUDIT PASS / NATIVE METAEDITOR 0E0W PASS — SUPERSEDED FOR D1 CONTEXT BY 2026-08-24 CORE RECONCILIATION**
Record: `blueprint/P3_CORE_V2_STRATEGY_REAUDIT_20260822.md`
Result: original CV2-01..CV2-15 were MATCH/DORMANT/statically resolved under the then-current Core. Stronger Home Course D1 evidence later reopened the higher-timeframe context portion; use the 2026-08-24 D1 records for current D1 semantics.


### P0 — Strategy correctness gate

#### CORE-V2-F1 — M09 MHV/MLV source alignment
Priority: **CRITICAL**
Status: **CODE IMPLEMENTED / STATIC REGRESSION PASS / NATIVE METAEDITOR 0E0W PASS — RUNTIME TRACE PENDING**
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
- opposite `REVERSAL-CONFIRMED EXTREME` on the same source timeframe atomically supersedes the old cycle;
- no generic fixed candle/session/day expiry is used;
- double/triple top/bottom and H&S-like forms remain examples, not mandatory formulas.
Classification: **DIRECT SOURCE STRUCTURAL/SEQUENCE/LOSS-OF-MOMENTUM/BODY-RETEST/REM/CYCLE-RESTART CONCEPT + PROJECT DETERMINISTIC STATE-MACHINE MAPPING**.
Next action for F1: runtime lifecycle traces; static implementation/native compile are complete at the recorded source revision.

#### CORE-V2-F2 — Extreme maturity inside REM/REE
Priority: **HIGH**
Status: **CODE IMPLEMENTED / STATIC REGRESSION PASS / NATIVE METAEDITOR 0E0W PASS — RUNTIME TRACE PENDING**
Source: `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-03
Decision record: `blueprint/decisions/CORE_V2_F2_EXTREME_MATURITY_DECISION.md`
Locked decisions:
- lifecycle = `RAW EXTREME -> REVERSAL-CONFIRMED -> RETEST/ENTRY-READY`;
- raw Extreme alone cannot satisfy executable REM/REE;
- REM/REE Extreme component minimum = reversal-confirmed;
- standalone Extreme requires retest/entry-ready;
- closed-candle reversal mapping, frozen body anchor, first valid body/MA5 retest and invalidation precedence remain as recorded in the decision file.
Next action for F2: runtime lifecycle traces; static implementation/native compile are complete at the recorded source revision.

#### CORE-V2-F3 — Re-Entry Type 1 context
Priority: **HIGH**
Status: **CODE IMPLEMENTED / STATIC REGRESSION PASS / NATIVE METAEDITOR 0E0W PASS — RUNTIME TRACE PENDING**
Source: `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-09
Decision record: `blueprint/decisions/CORE_V2_F3_TYPE1_CONTEXT_DECISION.md`
Locked decisions:
- Type 1 requires prior source-valid rise/fall -> structural sideways/ranging -> MA5/MA10 retest -> valid close-side;
- MA touch alone and one non-CSM candle are insufficient;
- no fixed minimum/expiry count;
- structural invalidation/ownership rules remain as recorded.
Next action for F3: runtime Type1 lifecycle traces.

#### CORE-V2-F4 — Higher-timeframe context for standalone H1 Re-Entry
Priority: **HIGH**
Status: **SPECIFICATION RECONCILED 2026-08-24 / PREVIOUS H4-ONLY CODE PASS IS NOW PARTIAL-HISTORICAL / D1 IMPLEMENTATION PENDING**
Decision record: `blueprint/decisions/CORE_V2_F4_H1_RE_HTF_CONTEXT_DECISION.md`
Current canonical decisions:
- D1 is strategic major-trend authority for new-entry direction;
- H4 remains immediate structural/setup parent;
- standalone H1 final higher-timeframe eligibility requires same-direction **confirmed D1 owner + active H4 owner**;
- D1 transition/unresolved blocks new entry;
- H4 `NO_OWNER` blocks standalone H1; no D1-only fallback;
- H4 inherited owner, eCSD establishment, atomic opposite handover, structural lifetime and deterministic recovery rules remain intact;
- no H4-only override of D1 is permitted.
Next action: implement through M11/M15/M16 only after current P3 runtime freeze is released, then rerun static/native/runtime F4 verification.

#### P3-M1 — Mode 1 Official BBMA Compliance Audit
Priority: **CRITICAL / STRATEGY GATE**
Status: **PREVIOUS STATIC PASS IS HISTORICAL; RE-AUDIT REQUIRED AFTER D1 STRATEGIC-OWNER IMPLEMENTATION**
Previous audit: `blueprint/P3_M1_MODE1_OFFICIAL_BBMA_COMPLIANCE_AUDIT.md`
Reason reopened:
- previous pass validated H1 Re-Entry under H4 owner according to the older Core;
- canonical Core now additionally requires confirmed same-direction D1 strategic authority;
- current code has not implemented that new gate.
Future closure requires:
- D1 BUY/SELL/TRANSITION/UNRESOLVED traces;
- H4 same/opposite/no-owner cases under confirmed D1;
- proof that Mode 1 cannot execute while D1 transition/unresolved or against confirmed D1 direction;
- native compile and source/build/runtime identity alignment.

### P1 — Core support / semantic verification

#### CORE-V2-F5 — M07 flat/horizontal BB state
Priority: MEDIUM
Status: **CODE IMPLEMENTED / STATIC REGRESSION PASS / NATIVE METAEDITOR 0E0W PASS — RUNTIME TRACE PENDING**
Source: `blueprint/P3_CORE_V2_STRATEGY_AUDIT.md` CV2-02
Implementation record: `blueprint/CORE_V2_F5_IMPLEMENTATION_AUDIT.md`
Resolved mapping: `BB_FLAT` is a reachable geometric three-line horizontal state using one broker point only as numerical equality tolerance. M10 CSM remains independently source-aligned.

#### CORE-V2-F6 — Re-Entry validation-candle / entry-candle timestamp audit
Priority: MEDIUM
Status: **STATIC TIMING VERIFIED / METADATA REPAIRED / NATIVE METAEDITOR 0E0W PASS — RUNTIME ORDER-TIME TRACE PENDING**
Implementation/audit record: `blueprint/CORE_V2_F6_TIMING_VERIFICATION_AUDIT.md`
Resolved mapping: closed source-TF Re-Entry candle validates; execution may occur in the immediately following live source-TF candle; no extra full-candle delay.

#### CORE-V2-F7 — Re-Entry SL/TP / lifecycle provenance
Priority: **MEDIUM / SOURCE GOVERNANCE + FUTURE ARCHITECTURE**
Status: **SOURCE/LIFECYCLE SEMANTICS RESOLVED THROUGH PATH-A AUDIT CHAIN / EA IMPLEMENTATION DEFERRED WHILE P3 CANDIDATE IS FROZEN**
Canonical reconciliation record:
`blueprint/CORE_V2_F7_CANONICAL_RECONCILIATION_AUDIT_20260824.md`
Current source/spec conclusion:
- lifecycle-managed Re-Entry model is stronger than the old universal static outer-BB TP mapping;
- old H1/H4/D1 outer-BB TP mapping is not established as universal Core;
- hard SL remains EA_SAFETY rather than universal Core;
- implementation changes remain a future post-freeze series.

### P1 — Opposite-direction / same-pair cycle integrity
Priority: HIGH
Status: **BUG CONFIRMED / FIX IMPLEMENTED / STATIC REGRESSION PASS / NATIVE METAEDITOR 0E0W PASS — RUNTIME TRACE PENDING**
Audit record: `blueprint/P3_OPPOSITE_DIRECTION_PAIR_INTEGRITY_AUDIT.md`
Finding: M15 already blocks simultaneous contradictory eligible directions in one scan under the old path. M22 `LOCK_SAME_DIRECTION` predicate was reversed and was corrected.
Next action: focused runtime trace at the current frozen build.

### P1 — Sequential risk-budget admission
Priority: HIGH
Status: **STATIC PASS — NO CODE FIX REQUIRED; RUNTIME MULTI-DECISION TRACE PENDING**
Audit record: `blueprint/P3_SEQUENTIAL_RISK_BUDGET_ADMISSION_AUDIT.md`
Purpose: verify cumulative prospective risk admission under multiple valid decisions.

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
Observed symptom: dashboard can display stale active-trade count.
Audit M25 display source and monitored/open-order compaction so dashboard derives active count from current exact-owned open positions rather than stale lifecycle state.
No strategy logic change.

## Active P3 closure dependency
Before any new EA source patch, preserve the current P3 Step 5 closure/evidence attribution under `P3_STEP5_RUNTIME_CLOSURE_CHECKLIST.md` unless an explicit project decision ends/replaces the freeze.

Current D1/F7 contract reconciliation is documentation-only specifically so the existing runtime candidate remains attributable to its current source/build.

## Current execution order
1. Keep `CURRENT.md`, this queue, Core and contracts reconciled.
2. Complete/preserve the current P3 runtime closure evidence for the frozen candidate without opportunistic source changes.
3. After freeze release, implement the D1 strategic-owner series: M11 -> M15 -> M16.
4. Assign new unique left-aligned build ID, compile 0E0W, run static/Core regression and D1 runtime traces.
5. Re-run P3-M1 Mode 1 compliance under the reconciled D1 hierarchy.
6. Schedule the separate F7 lifecycle/TP architecture implementation series after its own pre-implementation contract/code audit.
7. Complete remaining runtime traces for F1–F6, TradeLock and cumulative risk as applicable to the active build lineage.
8. Address observability/UI items: invalid-lot diagnostics and dashboard active-count refresh.
9. Run regression/backtest gates before optimization or win-rate-based analysis.

## Governance
- GitHub records are authoritative over chat recollection.
- BBMA strategy semantics remain governed by `docs/references/`, explicit reconciliation decisions and canonical contracts.
- `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md` is the active consolidated developer-facing Core reference; unresolved HOLD/UNCERTAIN items remain excluded.
- Stronger source evidence may reopen an older implementation PASS; old PASS records remain historical evidence but cannot override the newer canonical Core.
- No optimization, score-based entry authority, win-rate gating, RSI/MACD/Stochastic/ADX/news/correlation filters, or unsupported strategy additions may enter through these queue items.
- Completed queue items must receive a dedicated audit/fix/closure record and then be marked here.

## 2026-08-25 — D1/D1O Queue Reconciliation Overlay

> This overlay supersedes older queue entries saying D1 strategic ownership is deferred or absent. Those entries remain only as historical provenance.

### Completed / closed
- D1 Step 1–9 strategic-owner implementation lineage: completed at static/native-validation level on `d1-owner-dev`.
- D1O-07 canonical LTF dedup materialized on current owner baseline.
- D1O-07 static owner-baseline audit: PASS.
- D1O-09 canonical dedup analyzer self-test: PASS.
- D1O-09 execution identity contract self-test: PASS.
- D1O-08 current owner native MT4 compile: PASS, 0E/0W.
- D1O-10 trading-disabled runtime attach smoke: PASS / `ATTACH_OK_NO_BROKER_DATA`.
- Temporary D1O validation PRs closed without merge after evidence harvest.

### Active next execution order
1. Re-run P3-M1 Mode-1 static compliance against current D1O-07 source.
2. Re-run focused cross-module regression for D1/D1O changes: M15 selection -> M16 revalidation -> M17 source SL/TP -> M22 idempotent execution -> M24 recovery identity.
3. Audit queued technical observability defects that do not change strategy (including `REJ_INVALID_LOT` diagnostics and dashboard live-trade count refresh).
4. Broker/demo runtime evidence when available: D1 owner matrix + D1 opportunity canonical dedup telemetry + validation-candle-before-order-open timing.
5. Do not promote Workbook HOLD rules or strategy-changing lifecycle/TP behavior without an explicit strategy decision gate.

### Non-blocking environment limitation
GitHub offline MT4 smoke has no broker market feed. Lack of D1 decision telemetry in that environment is not a source failure and must not block safe static/audit work.

## 2026-08-25 — NMJE D1 Watch-Only Boundary Closure
Status: **CLOSED / PASS / DOCUMENTATION-ONLY**
- D1 MHV/MLV and D1 eCSD are locked as NMJE watch/context-only states with no direct LTF execution authority.
- No higher-TF MHV/MLV -> direct LTF entry shortcut is authorized.
- M12N contract and M27 canonical pipeline are synchronized with this boundary.
- Exact REM/RRE/REE and D1 Opportunity execution contracts remain unchanged.
- Audit: `blueprint/NMJE_D1_WATCH_ONLY_BOUNDARY_RECONCILIATION_20260825.md`.

---

## Core 49-Family Revalidation Closure — CLOSED / PASS / DOCS-ONLY

- Correct canonical-family strict split: **28 COVERED / 10 PARTIAL-MIXED / 11 MISSING-HOLD**.
- All non-full families are retained by ID in the 2026-08-25 revalidation audit.
- Safe descriptive clarifications are documented; material strategy HOLDs remain non-executable.
- Historical F7 no-Momentum lifecycle conclusions are precedence-guarded against accidental future promotion.
- No MQL4 strategy change; no native compile required for this docs-only correction. Future strategy promotion from a HOLD still requires an explicit decision gate.

---

## 2026-08-25 — D1O-07 Static Re-Audit Closure

Status: **CLOSED / PASS**

Completed from the prior active execution order:
1. P3-M1 Mode-1 static compliance against current D1O-07 source — **PASS**.
2. Focused cross-module regression `M15 -> M16 -> M17 -> M22 -> M24` — **PASS**.

Evidence:
- workflow run `32817790689`;
- EA SHA-256 `c911790b45fb7a75270fdee1204a7c97313605dca194f57380441b92a66896c2`;
- `P3_M1_D1O07_MODE1_COMPLIANCE_REAUDIT_20260825.md`;
- `D1O07_CROSS_MODULE_REGRESSION_AUDIT_20260825.md`.

### Active next safe engineering order
1. `REJ_INVALID_LOT` diagnostics — observability only; no sizing/risk semantic change.
2. Dashboard active-trade count refresh — display/registry correctness only; no strategy change.
3. Broker/demo runtime D1 owner/dedup/timing evidence when market-connected environment is available.
4. Material Workbook HOLD rules remain blocked pending explicit strategy decision.

---

## 2026-08-25 — P2 Observability/UI Closure

Status: **CLOSED / PASS / CURRENT SOURCE 0E0W**

Completed:
1. `REJ_INVALID_LOT` diagnostics — **CLOSED/PASS**, observability-only.
2. Dashboard active-trade count refresh — **CLOSED/PASS**, display-only.

Evidence:
- canonical Git blob `532f15b224f7e2594ed83f85e077e76aa13f7ed3`;
- repository/LF SHA-256 `6a34cc999e18e96bcda8cec9ba90bcc6455a201da6ff1f2d957f5476fee83c1c`;
- Windows compile checkout SHA-256 `2fd43ecda4edee45e641463215be70d1c043b36941906a7507946b606cc3826b` (same blob; CRLF/LF only);
- official MT4 MetaEditor run `32823122900`, job `97725322914`: **0 errors / 0 warnings**;
- compile artifact `9554031975`;
- `P2_REJ_INVALID_LOT_DIAGNOSTICS_AUDIT_20260825.md`;
- `P2_DASHBOARD_LIVE_TRADE_COUNT_AUDIT_20260825.md`.

### Active next safe order
1. Broker/demo runtime evidence: D1 owner BUY/SELL/TRANSITION/UNRESOLVED matrix.
2. D1 Opportunity canonical dedup telemetry: same fresh LTF identity retains execution hash across D1 attribution changes; execution hash never changes direction.
3. Validation-candle-before-order-open timing evidence.
4. Continue NMJE/runtime research evidence only within its read-only contract.
5. Material Workbook HOLD rules remain blocked until an explicit strategy-decision gate.

---

## 2026-08-25 — Locked Next-Update Item: SELL Spread-Buffer Execution Normalization

Priority: **HIGH / NEXT APPROVED SOURCE UPDATE**
Status: **LOCKED / APPROVED / QUEUED / NOT YET IMPLEMENTED**
Decision record: `blueprint/decisions/M17_SELL_SPREAD_BUFFER_EXECUTION_NORMALIZATION_DECISION_20260825.md`

Locked scope:
- **BUY path unchanged**: no spread added to BUY structural hard SL.
- **SELL only**: final broker hard SL adds a frozen current-spread buffer above the existing BBMA structural SELL SL.
- SELL buffer formula: `SpreadBufferPips = max(2.0, ceil(CurrentSpreadPips))`.
- Examples: 1.1 -> 2 pip, 1.8 -> 2 pip, 2.1 -> 3 pip; minimum buffer is 2 pip.
- Use the same preflight/frozen `RiskValidationSnapshot`; do not chase live spread after entry.
- `MaxSpreadPips` remains an entry rejection filter and is **not** the SL buffer.
- Final SELL broker SL must be resolved before M21 AutoLot sizing, so AutoLot naturally decreases to preserve the configured risk percentage.
- FixedLot remains fixed; existing risk/portfolio gates stay authoritative.
- RR is recalculated from final broker SL; TP is not manufactured to preserve old RR.
- SELL TP Bid/Ask normalization is **separate / not approved by this item**.
- Classification: `EA_SAFETY / broker execution normalization`, **not BBMA Strategy Core semantics**.

Implementation gate:
1. Preserve current runtime/evidence attribution checkpoint first.
2. Implement in the next approved M17/M21 source update.
3. Keep structural SL provenance separate from broker hard-SL normalization.
4. Native MetaEditor 0E0W + focused BUY-unchanged/SELL-only static regression.
5. Broker/demo runtime evidence on at least one JPY cross and one non-JPY FX pair.

---

## 2026-08-25 — Locked Next-Update Item: Re-Entry Structural-Range SL + SELL Spread Normalization

Priority: **HIGH / NEXT APPROVED SOURCE UPDATE**
Status: **IMPLEMENTED / STATIC REGRESSION PASS / NATIVE METAEDITOR 0E0W PASS / RUNTIME TRACE PENDING**
Active decision: `blueprint/decisions/M17_REENTRY_STRUCTURAL_RANGE_SL_EXECUTION_NORMALIZATION_DECISION_20260825.md`

This item **supersedes** the earlier `SELL Spread-Buffer Execution Normalization` queue item. The earlier SELL-only decision is historical only and must not be implemented independently.

Locked implementation summary:
- Structural window = matching M12 `ReEntryData.StartCandleTime` through `ConfirmationCandle`, inclusive, on the approved `SLTPSourceComponent` timeframe.
- BUY anchor = lowest Low in that validated window; `BUY StructuralSL = StructuralLow - 1 Point`; **no spread buffer**.
- SELL anchor = highest High in that validated window; `SELL StructuralSL = StructuralHigh + 1 Point`.
- SELL broker buffer remains `SpreadBufferPips = max(2.0, ceil(CurrentSpreadPips))` from the frozen preflight snapshot.
- Do not substitute arbitrary lookback, fractal/swing detector, Top/Low BB, MA5/MA10 line, ATR or session high/low as hard-SL coordinates.
- Fail closed if the exact M12 lifecycle range cannot be matched/reconstructed.
- Resolve final hard SL before M21 AutoLot; wider valid SL therefore reduces AutoLot while preserving configured risk %, subject to broker lot constraints.
- RR is recalculated from final broker SL; TP is not moved merely to preserve old nominal RR.
- Classification: `EA_SAFETY / PROJECT EXECUTION NORMALIZATION`, not a new BBMA Strategy Core rule.

Source update is complete; only broker/demo runtime semantic evidence remains pending for this M17 item.


### M17 structural-range SL implementation closure — 2026-08-25
Status: **CLOSED AT SOURCE/STATIC/NATIVE-COMPILE LEVEL — RUNTIME TRACE PENDING**
- version: `4.52`; source blob: `4ccd444a96a34b494653143a7560516a4147b5bc`;
- implementation audit: `blueprint/M17_STRUCTURAL_RANGE_SL_EXECUTION_NORMALIZATION_IMPLEMENTATION_AUDIT_20260825.md`;
- protected/MM regression run `32849979993`: PASS;
- native MetaEditor run `32849850304`: 0 errors / 0 warnings;
- BUY uses lifecycle minimum Low - Point with no spread buffer; SELL uses lifecycle maximum High + Point + `max(2, ceil(frozen spread pips))`;
- AutoLot uses the final SL through unchanged M21 sizing;
- TP code is unchanged. Latest authoritative 2026-08-25 Core keeps material Re-Entry TP/lifecycle changes on strategy HOLD; see `blueprint/M17_TP_AUTHORITY_RECONCILIATION_AUDIT_20260825.md`;
- next M17 action: broker/demo BUY+SELL runtime evidence, including JPY/non-JPY where practical.


---

## 2026-08-25 — NMJE M12N Architecture Documentation Sync
Status: **CLOSED / PASS / DOCUMENTATION-ONLY**
- Top-level governance/current topology now explicitly records `M12 -> M12N NMJE -> M13`.
- M01–M27 numbering is preserved; M12N is a logical non-number-consuming sub-module and M27 remains orchestration owner.
- M13 routing records that NMJE observes after owner updates and before collection without altering immutable strategy snapshots.
- Exact REM/RRE/REE, D1 Opportunity, D1 watch-only boundary, M15 authority, SL/TP, risk and execution semantics are unchanged.
- EA source remains blob `4ccd444a96a34b494653143a7560516a4147b5bc`.
- Audit: `blueprint/NMJE_M12N_ARCHITECTURE_DOC_SYNC_20260825.md`.


## 2026-08-26 — v4.58 Gap-Closure Queue Overlay

> This overlay supersedes stale earlier queue entries that still describe D1 owner implementation, invalid-lot diagnostics, dashboard count, D1 TPW source implementation, or unresolved Core semantics as future work. Preserve those entries as historical provenance only.

### Closed / do not requeue without new evidence
- BBMA Core semantic classification: **0 unresolved Core semantic gaps**.
- D1 strategic owner source implementation and static/native compliance.
- D1 Opportunity family materialization/dedup static layers.
- D1 `EXTREME_TPW` TP ownership decision + dedicated contract.
- D1 TP-Wajib v4.58 source implementation: **PASS static / PASS protected surfaces / PASS native 0E0W**.
- `REJ_INVALID_LOT` observability diagnostics.
- dashboard live exact-owned trade count.
- SELL structural-SL spread-buffer issue previously closed.

### Active source identity
- v4.58 source blob: `a166ffb23aba5e6b4011a28d9de8896cd00e33a1`
- SHA-256: `ba2e5815d1b221d7bba46ed0be4793aa5bc6154e29e9b19562dfffbd28c8f0bc`
- materialization commit: `02e5434e4f59ea538976df7254bbaf2fc9f1da9d`
- both lifecycle gates remain **OFF**.

### Active queue — environment blocked
1. **D1 TPW runtime gate** — authenticated broker/demo restart, replay, BUY/SELL TPW close, duplicate-close, M20 precedence, lifecycle disambiguation.
2. **C044 runtime gate** — checkpoint/replay, failed-Momentum close, Momentum -> next Re-Entry re-arm, opposite mature Extreme supersession, M20 precedence.
3. **D1/D1O runtime telemetry** — owner matrix, stable execution hash, invariant direction, validation/order timing.
4. **P3/M17/Core runtime traces** — remaining live Tests B/C/D and F1-F6 / TradeLock / cumulative-risk geometry/sequence evidence.

### Development rule
There is currently no known repo/source/contract gap that justifies another strategy source patch before new evidence. Do not activate `EnableD1TPWLifecycle` or `EnableC044Lifecycle` without their broker/demo runtime gate. N1/N2/N3 remain parked.
