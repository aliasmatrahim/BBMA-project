# BBMA Finale — Strategy Core Implementation Gap Register

## Purpose
Separate **source knowledge changes** from **active EA implementation gaps**. A source rule can already be correct in the BBMA Core specification while the current code still implements it incompletely.

Original audit basis (historical pre-Build-5.15 snapshot):
- `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md`
- current Core contracts (`M08`, `M10`, `M12`, `M15`, `M17`)
- BBMA Finale V01–V07 evidence
- active `blueprint/source/BBMA_EA.mq4` on the status-owner branch identified by `blueprint/CURRENT.md`

Rows below are historical KIV findings. Their active-behavior claims must be read with the current-owner reconciliation below; they are not an authoritative Build 5.15 backlog.

## Current-owner reconciliation — 2026-10-26

Baseline reviewed: Build 5.15 at `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de`. This reconciliation supersedes only stale status claims; it does not certify all source fidelity.

| Historical item | Current-owner finding | Disposition |
|---|---|---|
| IG-01 MLV outer-BB invalidation | `UpdateCanonicalMLVState` calls canonical void logic for outer-BB/Momentum continuation before direction takeover. The old `MarkMLVVoid` / `DetectMLV_State` names are absent from the pinned source. | **STALE FINDING — no patch from this row** |
| IG-02 fixed MLV pattern construction | The active canonical lifecycle uses a reversal-confirmed parent, body-edge accumulation and a frozen marked body; the old `bar +2` / fixed-point candidate path is absent. | **STALE FINDING — no patch from this row** |
| IG-03 raw MHV detector | The old `DetectMHV` entry point is absent. The active MHV/MLV lifecycle models parent Extreme, TP-Wajib, post-TP loss phase, invalidation and retest. | **STALE FINDING — no patch from this row** |
| IG-04 BB_FLAT unreachable | M07 contains a geometric horizontal-band branch. M27 calls the BB-shape builder. | **STALE FINDING — add M07 contract/attributable runtime evidence separately** |
| IG-09/IG-10 standalone Extreme / TPW | M27 builds a standalone H1 Extreme candidate through M15, subject to lifecycle and owner gates. This invalidates the old “withheld/non-executable” status; exact TPW/runtime semantics still need their own trace. | **STALE STATUS — TPW conformance remains open** |
| IG-05–IG-08, IG-11 | Not revalidated end-to-end against every Build 5.15 input and lifecycle path in this update. | **RECHECK REQUIRED — do not treat old KEEP/VERIFY labels as current verification** |

Separate confirmed issues: M06 incomplete-history validity remains a Build 5.15 owner bug; its repair is candidate-scoped in Draft PR #293. M12 unreadable-refresh admission was reproduced against Build 5.15; Build 5.22 candidate freshness gates have portable exact-source evidence and a strict native compile pass, but the candidate is unmerged and qualified-history/runtime verification remains open. The active owner is unchanged.

Additional current-owner reconciliation: source MODULE 11J was absent from the older graph and regression map; it is now mapped to the approved D1O-01 execution decision and Build 5.15 code. D1O-01 is a project execution extension, not independent original-source provenance. The 23 M01 inputs, 68 M01/M02 type declarations, 37 M03 globals and detected cross-module function calls are statically inventoried in Draft PR #294. BlockNMJEConflict and BlockNMJEBuilding have no code readers, but their source comments explicitly mark them inactive legacy compatibility inputs because NMJE is observation-only; they are not wired into trading behavior. Nested field ownership, tests and runtime remain open.

| ID | Area | Current active behavior (historical snapshot) | Source/Core expectation | Assessment at original audit | Priority |
|---|---|---|---|---|---|
| IG-01 | M09 MLV outer-BB invalidation | `MarkMLVVoid()` exists, but the active source only contains its definition; `DetectMLV_State()` does not call it when a candidate/confirmed MLV closes outside the relevant outer BB | Existing PDF Core and Finale V05 both say MHV/MLV becomes void when price closes outside the relevant outer BB / turns into momentum | **CORRECT — genuine implementation gap** | **HIGH** |
| IG-02 | M09 MLV pattern construction | Candidate is hard-wired to current High/Low vs bar `+2`, `< point*10` tolerance, and a synthetic `point*5` neckline; candidate type is only `DoubleTop`/`DoubleBottom` | Existing Core emphasizes highest/lowest **body** marking and retest; double/triple morphology is descriptive, and the sources do not define those fixed point thresholds | **CORRECT / RE-DESIGN SOURCE ENCODING** | **HIGH** |
| IG-03 | M09 raw `DetectMHV()` | Uses close vs MA5 and MA5 slope only; does not encode prior Extreme/TP context, inside-outer-BB validity or retest structure | PDF + Finale describe MHV/MLV as a loss-of-volume setup after Extreme/TP with outer-BB validity and retest context | **CORRECT or demote/remove legacy detector** | **MEDIUM-HIGH** |
| IG-04 | M07 `BB_FLAT` state | `DetectBBState()` returns SQUEEZE below 0.9, EXPANDING above 1.1, and CONTRACTING for 0.9–1.1; the remaining `BB_FLAT` return is effectively unreachable for valid positive ratios | Finale V02 gives flat/horizontal BB explicit semantic importance | **CORRECT auxiliary classification** | **MEDIUM** |
| IG-05 | M10 CSM / momentum | Requires outer-BB close + width expansion + directional Mid/outer movement | PDF Core and Finale both require expanding/directional BB context for momentum | **KEEP — no fix** | NONE |
| IG-06 | M10 eCSD/CSD | eCSD crosses relevant MA5/10; CSD crosses MA5/10 + Mid BB; raw signals are not directly executable | Matches PDF Core and Finale V03/V05/V06 | **KEEP — no fix** | NONE |
| IG-07 | M12 MA5/MA10 Re-Entry close-side rule | BUY confirmation closes on/above MA5/10 Low cluster; SELL confirmation closes on/below MA5/10 High cluster | Matches Finale statement that a Re-Entry may penetrate MA5 but should not close through/clear both MAs | **KEEP — verify all type paths only** | LOW/VERIFY |
| IG-08 | M12 Re-Entry first/second-candle semantics | Confirmation metadata and `EntryPrice` are stored from the fully closed validation candle; actual broker execution is later at live ASK/BID | Finale says first Re-Entry candle validates and second candle is entry | **VERIFY SEMANTICS — not proven gap** | **MEDIUM VERIFY** |
| IG-09 | M08 standalone Extreme lifecycle | M08 intentionally detects raw Extreme signal only; standalone Extreme is withheld from Mode 2 | Existing Core and Finale both require reversal + retest before standalone Extreme entry; Finale still contains unresolved exceptions | **KEEP WITHHELD — no implementation expansion yet** | NONE |
| IG-10 | Extreme TP Wajib | Current executable Mode 1/2 decisions source TP from Re-Entry components; standalone Extreme is non-executable | Finale clarifies normal standalone Extreme TP Wajib toward opposite MA5/MA10 first | **DORMANT SPEC CLARIFICATION, not current live TP bug** | LOW/FUTURE |
| IG-11 | REM/RRE/REE signatures | Current M13/M14 exact signatures match the PDF-derived contracts | Finale does not provide unambiguous subtitle-only evidence to replace them | **KEEP — no fix** | NONE |

## Historical high-value findings and current disposition
### P1 — M09 source alignment (historical finding reconciled in CP12)
The original pre-Build-5.15 audit correctly identified a mismatch in its snapshot. The pinned Build 5.15 owner now contains one canonical M15 MHV/MLV lifecycle: outer-BB/prior-Momentum invalidation, body-edge tracking and freeze, retest, and parent/cycle supersession. IG-01–IG-03 are stale status claims against this owner and are not patch instructions. CP12 records a static Core §6 mapping; focused parity and runtime remain unverified. Do not reopen this as a source-code repair without new evidence.

### P2 — BB flat classification (historical finding reconciled in CP10)
The pinned Build 5.15 owner contains a geometric BB_FLAT branch and M07's contract is documented. The labels have no downstream reader and do not gate M10 CSM. No current signal mismatch was confirmed; focused parity/runtime remains unverified. Do not recreate the historical branch fix.

### VERIFY — Re-Entry timing before changing anything
Do not add a new waiting candle yet. The current architecture processes closed source candles and executes later at the live market price. A timestamp audit should answer whether the current market entry already occurs on the second Re-Entry candle as Finale describes. Only if execution is demonstrably one candle too early should M12/M15 timing be altered.

## Non-findings
Finale does **not** justify changing the following merely for the sake of change:
- M10 expanding-BB momentum rule;
- eCSD/CSD semantics;
- Type 2 three-candle confluence;
- current exact REM/RRE/REE signatures;
- prohibition on raw direction/Extreme execution;
- Mode 1/Mode 2 eligibility contract.


## Issue #292 implementation update — 2026-10-27

The historical M09/M07 rows above were already reconciled against owner Build 5.15: IG-01 to IG-04 are stale status claims for that source, not patch instructions. The owner contains the canonical `UpdateCanonicalMLVState` lifecycle and geometric `BB_FLAT` branch. Do not recreate those old fixes.

The separate M12 invalid-refresh admission finding was reproduced against owner Build 5.15. Build 5.22 candidate checks all frozen component timeframes (Re-Entry, Extreme, MHV and MLV) at M15 and M16; portable exact-source probes pass. CP08 verifies strict native compile on G40 with 0 errors / 0 warnings. The qualified-history gate is NOT VERIFIED, so Strategy Tester and broker/runtime remain NOT RUN. Owner source remains unchanged; the candidate is unmerged.
## CP11 owner reconciliation — Core §5 Extreme lifecycle (2026-10-26)

- Core V2 §5.4 / the user-approved F2 decision and Build 5.15 owner code now agree on the accepted maturity path: M08 RAW → first subsequent closed reversal-direction candle → REVERSAL_CONFIRMED → retest phase/anchor freeze → first valid body-anchor or MA5 interaction → RETEST_READY.
- M15 constructs standalone H1 Extreme only from RETEST_READY, Mode 2, and the active same-direction H4 owner; M11 D1 strategic filtering and M16 exact owner revalidation remain downstream gates. M17 contains the Q5 structural-wick SL and opposite-MA TPW execution mapping.
- The D1O Extreme-TPW path is separate project extension work. `EnableD1TPWLifecycle=false`; M17 fails closed for a D1 TPW identity when disabled, and M23 D1 TPW lifecycle functions are gated. Do not treat it as an enabled trade path.
- The old “standalone withheld” and “TPW dormant” claims in the historical IG-09/IG-10 rows are superseded for static owner scope. No focused test, native compile, Strategy Tester or broker/runtime was run in CP11; those validations remain NOT VERIFIED / NOT RUN.


## CP12 owner reconciliation — Core §6 MHV/MLV (2026-10-26)

- Build 5.15 M09 has a single canonical M15 lifecycle and consumes only a reversal-confirmed M15 Extreme parent. Static trace matches the accepted Core §6 sequence and the F1 mapping: normal TP-Wajib, post-TP loss phase, body accumulation/freeze, retest/context, pre-takeover invalidation, same-cycle direction takeover and opposite-cycle supersession. No fixed candle/session expiry is applied.
- M13/M14 preserve the exact REM signature H4 RE + H1 Extreme + M15 MHV/MLV; Core §6 formation/frozen-body maturity is sufficient and a retest is not required for REM. M16 checks the exact persistent M15 component identity.
- M12N is read-only and exposes only the M15 MLV overlay. No H4/H1 MHV owner or H4_MHV_WATCH implementation was found in the pinned source. C039/C040 document read-only HTF observer/context semantics, but explicitly do not authorize MQL4 changes by themselves. The behavior is absent from the pinned owner and needs its own scoped contract/task; it is not evidence of a canonical M09/Core §6 mismatch.
- Historical IG-01–IG-03 and P1 are closed as current-owner patch targets. No standalone M09 contract is linked; this remains a documentation gap. CP12 adds no code and runs no tests/compile/runtime. The Build 5.22 stale-MLV source gate is candidate freshness evidence only, not M09 lifecycle parity.
- Focused M09/TP-Wajib parity, attributable runtime and Strategy Tester remain NOT VERIFIED / NOT RUN. The Strategy Tester remains gated on qualified G40 history.

## CP13 owner reconciliation — Core §7 eCSD/CSD (2026-10-26)

- The accepted Core/PDF/Finale direction semantics match the Build 5.15 M10 predicates at the static level: eCSD crosses the relevant MA5/MA10 pair; CSD adds the Mid-BB cross; CSM remains a separate outside-BB Momentum signal. M10's body-spanning cross formula and directional MA pairing are engineering mappings.
- M12 classifies CSM > CSD > eCSD and gives CSM/CSD Type 3/4 Re-Entry ownership only as candidate precursors; later MA5/MA50 or MA5/MA10 retrace confirms. M13 suppresses same-direction same-candle eCSD when CSD is valid. The stale M10 contract sentence asking M13 to decide this precedence is corrected.
- M27's H4 owner classifier uses CSM > CSD > eCSD; exact latest-closed M15 inputs route to M09/M13, and M09 independently rejects invalid/unclosed data before takeover. M11J's approved D1O-01 CSD opportunity is context, aligned to D1 strategic owner and gated by a fresh LTF Re-Entry; the D1 eCSD logger reports the inclusive raw predicate as watch-only and may overlap with CSD. M15 remains final and M16 revalidates.
- No raw CSD/eCSD direct-entry path was found. CP13 statically closes the Core §7 owner-path comparison; it does not convert historical IG-05/IG-06 'KEEP' labels into test/runtime evidence. The known M06 incomplete-history defect remains on owner Build 5.15; Build 5.20 repair is candidate-scoped. M08 uses a local CSM-equivalent invalidation helper, not a direct M10 call; focused helper parity remains NOT VERIFIED.
- CP13 changes the M10 contract and audit records only. No EA source, tests, compile, Strategy Tester or runtime changed/ran. Core §7 is statically mapped; focused precedence/retrace/runtime evidence remains NOT VERIFIED.
 
## CP14 owner reconciliation — Core §8 Re-Entry (2026-10-26)

- Build 5.15 M12 statically maps the accepted Type1–4 forms, shared close-side validation, and closed-candle confirmation. Type1 geometry and the <2 points proximity tolerance remain engineering mappings; no generic expiry is added.
- The empty-owner start sequence is Type3→Type4→Type2→Type1. The reviewed PDF/Core/Finale/contract evidence does not define Type2/3/4 overlap precedence, and the code does not prove mutual exclusion. This is UNRESOLVED, not a confirmed runtime overlap; do not alter arbitration without authoritative evidence or an explicit project decision.
- F6 audit correction: M11J D1O-01 uses D1 EntryCandle as ActivationTime, then requires fresh lower-timeframe Re-Entry readiness strictly after activation. This is not a general order timer and does not add an ordinary entry candle wait.
- M27 → M13/M14 → M15/M16 → M17/risk/M22 handoffs were statically traced. No test, compile, Strategy Tester or broker/runtime was run for CP14. Qualified G40 history remains NOT VERIFIED.
