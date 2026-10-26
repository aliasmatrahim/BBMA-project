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

Separate confirmed issue: M06 incomplete-history validity remains a Build 5.15 bug. Candidate repair and tests are in Draft PR #293; the active owner is unchanged. M12 unreadable-refresh admission remains **VERIFICATION REQUIRED** under Issue #292.

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

## Highest-value future repairs
### P1 — M09 source alignment
The strongest actionable finding is M09. This is supported by **both** the pre-existing PDF Core and Finale, so it is not a speculative video-only change.

A future repair should first define one canonical MHV/MLV owner/state model and then ensure:
- outer-BB close voids candidate/confirmed state immediately on the source timeframe;
- highest/lowest body and retest ownership are explicit;
- no arbitrary fixed point tolerance is presented as an Oma Ally rule;
- pattern morphology is not restricted to an invented single double-top/bottom formula unless explicitly classified as engineering interpretation;
- the legacy raw `DetectMHV()` cannot contradict the persistent MLV/MHV owner.

### P2 — BB flat classification
Fix the auxiliary state enum so `BB_FLAT` is reachable and semantically distinct. This is lower priority than M09 because the active M10 CSM detector already uses direct expansion/directional tests and is currently source-aligned.

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

The separate M12 invalid-refresh admission finding was reproduced against owner Build 5.15 and is blocked in candidate Build 5.21; it remains unmerged and uncompiled. CP07 then found that Build 5.21 only checked Re-Entry component source snapshots. Build 5.22 candidate now checks all frozen component timeframes (Re-Entry, Extreme and MHV/MLV) at M15 and M16. Portable exact-source regression passes; native strict compile, Strategy Tester and broker/runtime remain NOT TESTED. Owner source remains unchanged.
