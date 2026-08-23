# P3-FINAL-DELTA — Full P0→P3 Post-Source Expansion Revalidation

Date: 2026-08-23  
Branch: `blueprint-dev`  
Audit type: **STATIC DELTA REVALIDATION — AUDIT FIRST / NO STRATEGY CODE FIX IN THIS PASS**  
Verdict: **REPAIR REQUIRED BEFORE RUNTIME CLOSURE**

## 1. Objective
Revalidate P0, P1, P2 and P3 after expansion of the BBMA source set, especially BBMA Finale V01–V07 and the later mandatory source-governance rules.

This is not a restart from zero. Existing audits/fixes are treated as prior evidence, but no earlier PASS is immune from reopening when the expanded source set or current code proves a material mismatch.

## 2. Mandatory source group used
Evidence order follows `PROJECT_INSTRUCTIONS.md` Section 17:

1. Primary/secondary BBMA PDFs via `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md` and canonical Core consolidation.
2. BBMA Finale V01–V07 via `BBMA_FINALE_MASTER_RULE_INDEX.md`, episode extracted rules/summaries and conflict register.
3. Relevant BBMA/Oma Ally forum evidence as corroboration/clarification only.
4. `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md` as the accepted developer-facing consolidation.
5. Only after semantics are established: module contracts, audit records and current `BBMA_EA.mq4`.

Relevant forum corroboration checked during this pass includes:
- ForexFactory BBMA discussions describing MHV after Extreme/TP and reverse/retest behavior;
- multi-timeframe R/E/M combination teaching;
- Extreme reversal-confirmation + retest entry descriptions.

Forum evidence does not override the PDF/Finale hierarchy.

---

# 3. FD-00 — Source integrity / governance preflight

## FD-00A — Finale raw/corrected archive not fully committed to GitHub
**Severity:** MEDIUM / GOVERNANCE  
**Classification:** SOURCE ARCHIVAL GAP — NOT A STRATEGY LOGIC DEFECT

`VIDEO_SOURCE_INDEX.md` confirms all V01–V07 original and AI-corrected SRT hashes and says the full 14 SRT files exist in the generated source pack, but the 14 raw/corrected SRT files are still pending direct/manual GitHub upload. GitHub currently holds the derived `extracted_rules` / `summary` layers and master indexes.

Effect:
- current Core evidence is still traceable through hashes/timestamps/derived artifacts;
- however GitHub alone is not yet a complete self-contained archive of the raw Finale subtitle evidence.

Required repair later:
- archive `V01_original.srt` ... `V07_original.srt` and corrected counterparts in their episode folders when file-upload mechanics permit;
- verify SHA-256 against `VIDEO_SOURCE_INDEX.md`;
- original SRT remains immutable.

## FD-00B — SOURCE_INDEX retrieval map lags the mandatory forum rule
**Severity:** LOW-MEDIUM / GOVERNANCE  
**Classification:** DOCUMENTATION CONSISTENCY GAP

`PROJECT_INSTRUCTIONS.md` Section 17 explicitly requires PDF + Finale + relevant forum + Core cross-check for uncertainty/gap work. `SOURCE_INDEX.md` still gives its canonical retrieval sequence without a dedicated forum step before conflict/contracts.

Required repair later:
- synchronize `SOURCE_INDEX.md` with Section 17 without changing the established source precedence: **PDF primary → Finale clarification → forum corroboration**.

---

# 4. FD-P0 — Architecture / contract delta revalidation

## Passed
- M06 producer ownership remains separated from detector/entry authority.
- M08/M09/M10/M12 remain strategy-state owners rather than execution modules.
- M13 collector / M14 validation / M15 final authority / M16 invalidation separation remains architecturally sound.
- M17+ remains downstream of strategy authority.
- M19/M20/M21/M22 remain rejection/safety/execution overlays and do not own BBMA signal direction.
- M27 remains orchestrator.

## FD-P0-01 — Several P0 source contracts are stale relative to later F1–F6/Finale decisions
**Severity:** MEDIUM  
**Classification:** SPECIFICATION / CONTRACT DRIFT

Examples found:
- `M08_EXTREME_SOURCE_CONTRACT.md` still says a deterministic reversal/retest lifecycle was not precise enough to lock, while F2 later resolved and implemented that lifecycle.
- `M12_REENTRY_SOURCE_CONTRACT.md` still lists already-resolved M06/M10/upstream blockers and pre-F3 lifecycle assumptions.
- `M15_FINAL_SIGNAL_AUTHORITY_CONTRACT.md` still states standalone Extreme is withheld because its reversal/retest lifecycle has not been locked, but F2 now explicitly locks `RETEST/ENTRY-READY EXTREME` as standalone entry maturity.
- `M16_CONFLICT_INVALIDATION_CONTRACT.md` still describes older project expiry/ownership assumptions that now conflict with the later structural-lifecycle direction of F1/F2/F3/F4.

Effect:
- code and later decision records can be newer than the module source contracts;
- future audits may read an obsolete contract and reach the wrong conclusion.

Required repair later:
- after strategy defects below are resolved, synchronize the affected contracts to the final accepted Core rather than preserving historical blocker text as current requirements.

---

# 5. FD-P1 — Integration / ownership delta revalidation

## Passed
- P3-M2-07B.2 opposite-Extreme arbitration remains the correct ownership model: RAW opposite Extreme is candidate-only; reversal-confirmed opposite Extreme supersedes the old same-TF Extreme/cycle.
- BUY and SELL Extreme lifecycles are resolved before M13/M14 candidate construction.
- M09 F1 MHV/MLV uses its own stage-aware supersession rather than being retroactively erased by a parent-object change.
- Live broker position direction is not used as Strategy-Core cycle ownership.
- M16 exact component identity validation remains the proper downstream ownership check.

## FD-P0/P1-02 — M16 still injects arbitrary fixed age expiry into Extreme ownership
**Severity:** HIGH / STRATEGY PURITY  
**Classification:** IMPLEMENTATION DEFECT + OWNERSHIP LEAK

Current source still contains:

`expiry = extreme.CandleTime + (MaxWaitBars_Extreme * extreme.Timeframe * 60)`

and invalidates the persistent Extreme component when that project window expires.

Why this is now suspect under the expanded source/Core:
- F2 defines Extreme validity through RAW → reversal-confirmed → retest-ready, with structural VOID priority;
- F1/P3-M2-07B defines cycle termination through opposite reversal-confirmed Extreme supersession;
- the Core implementation guard explicitly rejects invented arbitrary candle-count lifecycle conditions;
- no accepted PDF/Finale/forum rule found in this audit establishes a universal **5-bar Extreme death rule**.

Impact:
- a still-source-valid H1/H4 Extreme can disappear solely due to age;
- REM/REE can be rejected even though structural invalidation/supersession has not occurred;
- M16 is therefore able to override M08/F2 structural ownership with an unsourced timer.

Required repair later:
- resolve Extreme lifetime structurally from accepted VOID/supersession events;
- remove or demote `MaxWaitBars_Extreme` from Strategy-Core authority unless direct source evidence is produced.

---

# 6. FD-P2 — Functional / cross-module delta revalidation

## Passed
- exact REM remains H4 Re-Entry + H1 Extreme + M15 MHV/MLV;
- exact RRE remains D1 Re-Entry + H4 Re-Entry + H1 Extreme;
- exact REE remains D1 Re-Entry + H4 Extreme + H1 Extreme;
- M13 does not reinterpret direction;
- M14 validates signature + same-direction consistency;
- M15 opposite BUY/SELL candidate pool remains fail-closed rather than inventing a winner;
- M18 score remains non-authoritative metadata;
- F1 MHV/MLV no-fixed-expiry structural lifecycle remains intact.

## FD-P2/P3-03 — Re-Entry Types 2/3/4 still use generic `MaxWaitBars_ReEntry = 5` expiry
**Severity:** HIGH  
**Classification:** UNSUPPORTED STRATEGY TTL / IMPLEMENTATION GAP

Current M12 source:
- exempts only Type 1 from generic expiry;
- assigns Type 2/3/4 `ExpiryCandleTime = StartCandleTime + MaxWaitBars_ReEntry * timeframe * 60`;
- converts active candidate/confirmed state to `RE_STATE_EXPIRED` when that fixed window elapses.

Source/Core comparison:
- Type 2 source explicitly requires a minimum three-candle MA5/10 + Mid-BB confluence; it does not supply a universal five-bar death rule.
- Type 3 is CSM → later MA5/MA50 retrace.
- Type 4 is CSD → later MA5/MA10 retrace.
- no accepted source reviewed in this pass establishes a generic 5-bar expiry for Type 2/3/4.
- the project purity contract already warns that legacy `MaxWaitBars_*` fields must not silently invalidate a source-valid Core owner merely because an arbitrary candle count elapsed.

Impact:
- valid BBMA Type 2/3/4 setup progression can be killed by project age rather than structural failure/supersession;
- this affects Mode 1 directly and combination components in Mode 2.

Required repair later:
- perform one focused source-resolution pass on Type 2/3/4 lifetime/invalidation;
- replace unsupported timer expiry with source/structure-owned reset rules, or keep an item HOLD if the source cannot resolve a particular lifetime edge case;
- do not simply change `5` to another optimized number.

---

# 7. FD-P3 — Strategy / entry-compliance delta revalidation

## Passed
- no RSI, MACD, Stochastic, ADX, news, session, correlation, ATR/volatility or AI score authority is active in the BBMA decision path.
- risk/portfolio/broker overlays remain downstream rejection-only policy.
- M17 SL/TP provenance remains properly disclosed as layered Core/Finale/forum/project-engineering rather than falsely claimed as verbatim PDF law.
- F6 first-validation / next-live-candle execution semantics remain source-compatible statically.
- opposite Extreme does not force-close an older broker trade without explicit source authority.

## FD-P3-04 — Mode 2 entry universe is now internally inconsistent after F2
**Severity:** HIGH  
**Classification:** CONTRACT / IMPLEMENTATION MISMATCH — DECISION REQUIRED

`ENTRY_MODE_CONTRACT.md` defines Mode 2 as **ALL_VALIDATED_BBMA_ENTRIES** and originally excluded standalone Extreme because the source-required reversal/retest lifecycle had **not yet been deterministically locked**.

That prerequisite changed later:
- F2 now explicitly defines `RETEST/ENTRY-READY EXTREME` as the maturity required for a standalone Extreme entry;
- canonical Core V2 repeats that standalone Extreme entry eligibility exists at that maturity;
- Finale/forum corroboration describes reversal confirmation followed by retest as the Extreme entry stage.

Current M15/Mode-2 implementation still admits only:
- H1 Re-Entry;
- REM;
- RRE;
- REE.

Standalone retest-ready Extreme is still excluded.

This produces two possible valid project resolutions, but the present state cannot be called internally consistent:

**Option A — preserve the name/meaning `ALL_VALIDATED_BBMA_ENTRIES`:**
include the source-valid standalone Extreme after its F2 retest-ready maturity and full downstream validation.

**Option B — deliberately keep the smaller executable family:**
rename/redefine Mode 2 so it no longer claims to contain all validated BBMA entry opportunities.

No code decision is made in this audit pass. The current `M2-01 Entry universe PASS` must be reopened until this is resolved.

## FD-P3-05 — Prior P3 PASS records require targeted reopening
**Severity:** MEDIUM / STATUS GOVERNANCE

Because FD-P2/P3-03 and FD-P3-04 were not incorporated into earlier closure claims:
- `P3-M1` static compliance must be revalidated after Type 2/3/4 lifetime repair;
- `M2-01 Entry universe` must be reopened;
- `M2-10 Strategy purity regression` must be reopened for fixed-TTL review;
- `M2-12 Final Mode-2 Offline Gate` cannot be treated as final closure until the repair pass and re-audit complete.

This does **not** discard the valid work in those audits. Only the affected scopes are reopened.

---

# 8. Documentation/status drift found during delta audit

## FD-DOC-01 — Finale implementation gap register is historical/stale in places
**Severity:** MEDIUM / GOVERNANCE

`BBMA_FINALE_CORE_IMPLEMENTATION_GAP_REGISTER.md` still lists old gaps such as M09 alignment and BB_FLAT as active future repairs even though F1/F5 and subsequent integrated re-audit record them as fixed/static PASS.

Required repair later:
- convert resolved items to `RESOLVED` with links to F1/F5/F6 artifacts;
- keep only genuinely open gaps active.

## FD-DOC-02 — Current compile/status labels lag current build
The older M2-12 and P3-M2-07B documents still say the then-current M2-11.1 build required compile. The project has since moved to `P3-UI-01 Input Panel Cleanup`, and the user reported native MetaEditor **0E0W** for that build.

This is status drift, not a strategy defect. Any strategy repair after this audit will require a fresh compile again.

---

# 9. Phase verdicts after full delta revalidation

| Phase | Delta verdict | Meaning |
|---|---|---|
| P0 Architecture | **PASS WITH CONTRACT DRIFT + 1 OWNERSHIP DEFECT** | module boundaries remain sound; contracts need synchronization; M16 Extreme timer must be repaired |
| P1 Integration | **PASS WITH HIGH FINDING** | atomic cycle/owner routing is sound; M16 timer can override structural Extreme ownership |
| P2 Functional | **FAIL / REPAIR REQUIRED** | Type 2/3/4 fixed Re-Entry TTL is unsupported and affects real setup lifecycle |
| P3 Strategy Compliance | **FAIL / REOPEN TARGETED SCOPES** | Mode 2 universe is inconsistent after F2; timer-based validity needs purity repair |

Overall result:

**P3-FINAL-DELTA = AUDIT COMPLETE / REPAIR REQUIRED BEFORE RUNTIME VALIDATION.**

No evidence from this pass requires restarting P0–P3 from scratch. The required work is a focused repair/reconciliation pass.

---

# 10. Consolidated repair order

Do not patch randomly. Repair upstream ownership first, then downstream entry universe/documentation.

### R1 — Strategy lifetime resolution
Cross-check PDF + Finale + relevant forum specifically for:
- Extreme lifetime after reversal-confirmed maturity;
- Type 2 candidate lifetime;
- Type 3 CSM→retrace lifetime;
- Type 4 CSD→retrace lifetime.

Goal: remove unsupported generic age expiry without inventing another timer.

### R2 — Code repair for R1
Affected likely owners:
- M08/M16 Extreme persistent validity;
- M12 Type 2/3/4 lifecycle;
- M16 exact-owner validation where it consumes expiry metadata.

### R3 — Mode 2 entry-universe decision
Resolve whether `ALL_VALIDATED_BBMA_ENTRIES` now includes F2 `RETEST/ENTRY-READY EXTREME`, or rename/redefine Mode 2 to intentionally exclude it.

### R4 — Contract/document synchronization
Update:
- M08/M12/M15/M16 contracts;
- Finale implementation-gap register;
- SOURCE_INDEX forum retrieval step;
- M1/M2 status records affected by the repairs.

### R5 — Purity + cross-module regression
Re-run targeted:
- P0 ownership;
- P1 integration;
- P2 lifecycle/combination;
- P3 Mode 1 + Mode 2 + purity.

### R6 — Fresh native compile
Required after source changes:

`0 errors / 0 warnings`

### R7 — Runtime validation
Only after R1–R6 are clean.

---

# 11. No-fix statement for unaffected areas
No new repair is required by this audit for:
- M06 indicator settings/producer ownership;
- M10 CSM/eCSD/CSD semantics;
- F1 canonical MHV/MLV structural lifecycle;
- exact REM/RRE/REE signatures;
- opposite-Extreme atomic cycle supersession logic from P3-M2-07B.2;
- M18 score neutralization;
- M19/M20/M21/M22 separation as downstream safety/execution layers;
- the layered provenance classification of the current M17 SL/TP execution policy.

These should not be rewritten merely because P3-FINAL-DELTA found issues elsewhere.
