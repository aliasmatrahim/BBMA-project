# SL/TP Reconciliation Matrix — Latest Baseline 2026-08-26

**Branch:** `d1-owner-dev`  
**EA baseline:** `Version 4.5.8 - D1 TP-Wajib Lifecycle Stage`  
**Purpose:** Reconcile the latest source-backed SL/TP and lifecycle-exit semantics against the current implementation, with special attention to the user's concern that TP can be materially smaller than SL.

## Evidence hierarchy used

1. `docs/references/SOURCE_INDEX.md`
2. `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`
3. Primary operational PDF `Oma ally BBMA - AL.pdf`
4. BBMA Finale V01–V07 reconciled evidence already incorporated into Core V2
5. Tier-B BBMA Home Course Workbook evidence and reconciled project decisions
6. Current `d1-owner-dev` EA implementation

This matrix does not manufacture new BBMA rules where the source is silent.

## Executive verdict

The 4.5.8 baseline materially closes the earlier `D1_OPP_EXTREME_TPW` mismatch: D1 Extreme TP-Wajib is now targetless at broker entry and is owned by a D1 lifecycle that waits for the opposite MA5/MA10 TP-Wajib interaction before latching a close. Therefore the earlier 4.5.6 finding that D1 `EXTREME_TPW` could inherit a Re-Entry outer-BB TP is no longer current for 4.5.8.

However, the user's broader concern remains valid for non-D1-TPW entries. The project still does not have a fully source-locked universal SL formula for every Re-Entry / REM / RRE / REE family, and static outer-BB TP remains only a provisional/static destination when the general lifecycle engine is not enabled. Source evidence strongly supports lifecycle-sensitive continuation/exit after Re-Entry.

## Source-backed family matrix

| Family / phase | Source-backed TP / exit semantics | Source-backed SL semantics | 4.5.8 implementation | Status |
|---|---|---|---|---|
| Extreme standalone / TP-Wajib | Mandatory profit-taking after Extreme. Primary PDF: MA5/MA10 or Mid BB; reconciled Core/Home Course: opposite MA5/MA10 is normal first TP-Wajib, Mid BB farther/maximum context. | Primary PDF explicitly permits SL a few pips beyond the highest shadow/wick in Extreme context. | D1 `EXTREME_TPW` now uses no broker TP and M23 D1 lifecycle closes on opposite MA5/MA10 completion. Protective SL still comes from selected Re-Entry structural owner. | TP lifecycle **ALIGNED for D1 opportunity**; SL ownership **PARTIAL / provenance gap** |
| MHV/MLV entry | TP is negotiable/conditional. Workbook: if next candle closes outside BB, momentum exists -> hold; if it closes inside BB -> close because market may reverse. After MHV -> direction -> Re-Entry -> no Momentum, TP is mandatory. | No universal explicit canonical broker-SL formula found across the reviewed higher-precedence sources. | MHV is setup/context and is not a direct standalone execution family in current Mode 1/2 path. | **NO direct code mismatch for standalone entry**, but lifecycle evidence matters downstream |
| Re-Entry | Re-Entry is the setup/entry zone. Workbook strongly supports `Re-Entry -> Momentum -> later Re-Entry` continuation and `Re-Entry -> no Momentum -> TP/close`. Directional destination is commonly the direction-side outer BB, but this is not a universal instruction to always place one fixed TP and ignore subsequent Momentum state. | Source does not clearly establish the current universal `StartCandleTime..ConfirmationCandle` extreme +/- implementation buffer as canonical for all Re-Entries. | When C044 is OFF, static direction-side outer BB TP is used. When C044 is ON, TP is zero and M23 lifecycle handles failed-Momentum exit / continuation to next Re-Entry. | TP **PARTIAL when C044 OFF**, **closer to source when C044 ON**; SL **HOLD / project mapping** |
| REM | Exact signature: H4 Re-Entry + H1 Extreme + M15 MHV. Exit semantics inherit the owning Re-Entry / cycle context rather than a separate source-explicit REM TP formula. | No separate source-explicit universal REM hard-SL formula found. | SL/TP source owner = H4 Re-Entry. Static outer-BB TP when C044 OFF; targetless lifecycle when C044 ON. | **PARTIAL** |
| RRE | Exact signature: D1 Re-Entry + H4 Re-Entry + H1 Extreme. Exit semantics inherit the owning Re-Entry / cycle context. | No separate source-explicit universal RRE hard-SL formula found. | SL/TP source owner = D1 Re-Entry. Static outer-BB TP when C044 OFF; targetless lifecycle when C044 ON. | **PARTIAL** |
| REE | Exact signature: D1 Re-Entry + H4 Extreme + H1 Extreme. Exit semantics inherit the D1 Re-Entry / cycle context. | No separate source-explicit universal REE hard-SL formula found. | SL/TP source owner = D1 Re-Entry. Static outer-BB TP when C044 OFF; targetless lifecycle when C044 ON. | **PARTIAL** |
| D1 Opportunity `EXTREME_TPW` | Extreme remains TP semantic owner; opposite MA5/MA10 first TP-Wajib area. | No source-backed reason to replace the protective SL owner with a fabricated D1 TP target-derived SL. | 4.5.8 rejects legacy outer-BB TP fallback for this family; it sets broker TP=0 and M23 closes on D1 opposite MA5/MA10 completion. | **TP FIXED / ALIGNED**; SL still **PARTIAL** |
| D1 Opportunity normal families | They remain Re-Entry execution clusters under D1 opportunity attribution. | Same Re-Entry SL provenance limitation. | H1 preferred / M15 fallback Re-Entry source; static outer-BB TP unless general lifecycle enabled. | **PARTIAL** |

## 4.5.8 implementation finding — previous SLTP-01 status changed

### Previous finding
4.5.6 could represent `D1_OPP_EXTREME_TPW` as a Re-Entry execution cluster and then resolve a Re-Entry-owned static outer-BB TP.

### 4.5.8 state
`ResolveApprovedInitialSLTP()` now identifies a D1 TP-Wajib lifecycle and explicitly refuses to execute that identity if `EnableD1TPWLifecycle` is unavailable. When enabled, the decision is targetless (`TakeProfit = 0.0`). M23 then advances a D1 closed-candle lifecycle and closes only after the source-defined opposite MA5/MA10 TP-Wajib interaction is detected. M24 persists/reconstructs this identity and cursor.

**Result:** previous D1 `EXTREME_TPW` TP ownership defect is **CLOSED at source/implementation design level for 4.5.8**, subject to compile/runtime verification.

## Why TP can still look much smaller than SL

The source does not impose a universal minimum reward:risk ratio such as 1:2 or 1:3. BBMA destinations are structural. Therefore an individual setup can naturally present a nearby structural TP and a wider protective SL.

But a poor apparent RR can arise from three different causes and must not be treated as one issue:

1. **Legitimate BBMA geometry** — structural TP is genuinely nearby.
2. **Wrong / overly-wide SL owner** — current generic Re-Entry lifecycle-window anchor may be wider than a source-supported protective invalidation point.
3. **Incomplete exit model** — static outer-BB TP may under-represent a valid Re-Entry -> Momentum -> next Re-Entry continuation journey.

The project must identify which case applies before rejecting or stretching a TP.

## Reconciliation decisions

### R1 — Do not manufacture TP merely to improve RR
**LOCKED.** `MinRRRatio` may remain a safety filter only. It must not move or invent BBMA TP.

### R2 — D1 Extreme TP-Wajib
**LOCKED for current D1 opportunity implementation.** Opposite MA5/MA10 is the first mandatory objective; Mid BB is farther context. The 4.5.8 targetless lifecycle approach is source-faithful because the close is triggered from the actual D1 TP-Wajib interaction rather than a legacy Re-Entry outer-BB TP.

### R3 — Re-Entry continuation / exit
**SOURCE-SUPPORTED LIFECYCLE PRINCIPLE.** After Re-Entry, same-direction Momentum supports continuation and a later Re-Entry; absence of Momentum at the relevant direction-side BB context supports TP/close. This is stronger than one universal fixed static TP.

### R4 — Generic hard SL for Re-Entry / REM / RRE / REE
**HOLD / NOT SOURCE-LOCKED.** The current lifecycle-window extreme + implementation safety buffer is deterministic and broker-safe, but the reviewed sources do not establish it as the universal canonical BBMA SL formula for every execution family.

### R5 — RR-based trade rejection
**OPTIONAL ENGINEERING FILTER, not Strategy-Core.** A minimum RR threshold can reject a structurally valid trade if the user enables it, but this changes opportunity acceptance and must not be described as an Oma Ally rule. Default `0` preserves BBMA structural behavior.

## Direct answer to the TP-vs-SL concern

The project should **not** fix small TP by mechanically increasing TP. The next unresolved source question is primarily the protective SL provenance for generic Re-Entry/REM/RRE/REE, plus whether the general C044 lifecycle should ultimately replace the static outer-BB TP path after its verification gate.

Therefore the correct follow-up is:

1. keep D1 TP-Wajib 4.5.8 implementation as the new baseline;
2. do not reopen its old outer-BB mismatch unless runtime evidence proves a defect;
3. resolve generic Re-Entry protective SL ownership/provenance before changing SL distance;
4. complete/verify the general Re-Entry lifecycle path (`Re-Entry -> Momentum -> next Re-Entry` / `no Momentum -> close`) before calling static outer-BB TP the final universal TP model;
5. only then evaluate actual family-level RR distributions and decide whether an optional engine-level RR rejection is desirable.

## Queue recommendation

- `SLTP-R1` — **KIV / SOURCE RESOLUTION:** generic Re-Entry/REM/RRE/REE protective SL provenance.
- `SLTP-R2` — **KIV / AFTER C044 VERIFICATION:** general targetless lifecycle replacement of static outer-BB TP where authorized.
- `SLTP-R3` — **VERIFY:** D1 TP-Wajib 4.5.8 compile/runtime/recovery behavior.
- `SLTP-R4` — **KEEP:** MinRR as optional filter only; do not use it to generate TP.

No EA source patch is authorized by this matrix yet, because changing the generic SL before source provenance is closed would replace one project mapping with another guessed mapping.