# TP Source Authority & Execution Mapping Audit — 2026-08-25

Status: **AUDIT COMPLETE / SOURCE AUTHORITY MATRIX LOCKED / NO TP STRATEGY CODE CHANGE AUTHORIZED BY THIS AUDIT ALONE**
Branch authority: `d1-owner-dev`
Scope: TP provenance, structural destination vs broker TP, timeframe ownership, Bid/Ask execution geometry, and downstream RR implications.

## 1. Purpose

Establish exactly which current/future TP behaviours are source-owned BBMA Core, which are only project execution policy, and which remain HOLD before any TP code redesign.

Mandatory evidence order used:

`Primary Oma Ally PDF -> accepted Finale V01–V07 clarification -> Home Course cross-source reconciliation -> authoritative Strategy Core V2 -> M17 contract/code -> supplemental community evidence -> broker execution mechanics`.

This audit deliberately separates:
1. **structural destination** taught by BBMA;
2. **exit authority** (whether reaching that structure mandates closure);
3. **broker TP price** sent to MT4;
4. **execution-side normalization** needed because MT4 charts are Bid-based while SELL exits trigger on Ask.

## 2. Authoritative source findings

### 2.1 Normal Extreme TP-Wajib — CORE CONFIRMED

Accepted source hierarchy supports:
- normal Extreme SELL -> opposite MA5/MA10 Low area as the normal first TP-Wajib area;
- normal Extreme BUY -> opposite MA5/MA10 High area as the normal first TP-Wajib area;
- Mid BB is farther/maximum context, not a replacement for the normal first objective.

Authority:
- `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md` F-03;
- `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`;
- primary PDF / Finale evidence indexed by those canonical records.

Classification: **BBMA_STRATEGY_CORE / HIGH CONFIDENCE**.

### 2.2 Directional outer-BB destination — CONTEXT SUPPORTED, NOT UNIVERSAL HARD-TP AUTHORITY

Home Course material supports the pedagogical idea that directional movement has a Top-BB / Low-BB destination. However the 2026-08-25 cross-source reconciliation explicitly keeps the predictive/universal interpretation PARTIAL/HOLD.

Authority:
- `docs/references/HOME_COURSE_19P_CROSS_SOURCE_RECONCILIATION_20260825.md` item 10.

Classification: **STRUCTURAL CONTEXT / NOT UNIVERSAL MANDATORY BROKER TP**.

### 2.3 Re-Entry / REM / RRE / REE static outer-BB TP — NOT CERTIFIED CORE

Current M17 maps:
- standalone H1 Re-Entry -> H1 directional outer BB;
- REM -> H4 directional outer BB;
- RRE -> D1 directional outer BB;
- REE -> D1 directional outer BB.

The exact static table is internally deterministic and historically community-corroborated, but the strict F7 provenance audit found no complete primary-PDF/Finale/Core authority establishing it as a universal mandatory TP formula.

Authority:
- `blueprint/CORE_V2_F7_M17_SLTP_PROVENANCE_AUDIT.md`;
- `blueprint/F7_R_SLTP_EVIDENCE_REASONING_RECONSTRUCTION_AUDIT.md` retained as layered historical reasoning only.

Classification of current executable table: **PROJECT_EXECUTION_POLICY / COMMUNITY-CORROBORATED / NOT BBMA-CORE-CERTIFIED**.

### 2.4 Post-Re-Entry Momentum/no-Momentum lifecycle exit — HOLD

Historical F7 work explored lifecycle-managed Re-Entry exits. Later 2026-08-25 reconciliation restored the material deterministic claims to HOLD because the stronger source hierarchy does not yet authorize a universal automatic close rule.

Authority:
- precedence notice in `blueprint/CORE_V2_F7_STATIC_TP_VS_LIFECYCLE_EXIT_COEXISTENCE_AUDIT_20260824.md`;
- `docs/references/HOME_COURSE_19P_CROSS_SOURCE_RECONCILIATION_20260825.md` items 16–18.

Classification: **HOLD / NOT EXECUTABLE WITHOUT EXPLICIT STRATEGY DECISION**.

## 3. TP Source Authority Matrix

| Setup / exit context | Structural destination evidence | Mandatory static broker TP authority | Current executable status | Provenance grade |
|---|---|---|---|---|
| Normal Extreme BUY | Opposite MA5/MA10 High first; Mid BB farther | Source-supported TP-Wajib lifecycle | Separate Core semantics; not the current Re-Entry M17 table | **CORE** |
| Normal Extreme SELL | Opposite MA5/MA10 Low first; Mid BB farther | Source-supported TP-Wajib lifecycle | Separate Core semantics; not the current Re-Entry M17 table | **CORE** |
| Direction BUY | Top BB as structural destination context | Not proven universal mandatory close | Context only | **PARTIAL / CONTEXT** |
| Direction SELL | Low BB as structural destination context | Not proven universal mandatory close | Context only | **PARTIAL / CONTEXT** |
| H1 Re-Entry BUY/SELL | Outer-BB destination is plausible/corroborated | Not certified universal Core | Current M17 project policy | **PROJECT POLICY** |
| REM BUY/SELL | H4 owner/destination logic is MTF-derived | Exact H4 outer-BB hard TP not certified Core | Current M17 project policy | **PROJECT POLICY** |
| RRE BUY/SELL | D1 owner/destination logic is MTF-derived | Exact D1 outer-BB hard TP not certified Core | Current M17 project policy | **PROJECT POLICY** |
| REE BUY/SELL | D1 owner/destination logic is MTF-derived | Exact D1 outer-BB hard TP not certified Core | Current M17 project policy | **PROJECT POLICY** |
| Re-Entry -> no Momentum close | Home Course lifecycle evidence | Cross-source deterministic authority unresolved | Disabled | **HOLD** |
| Pre-Re-Entry outer-BB hold exception | Home Course evidence | Universal deterministic management authority unresolved | Disabled | **HOLD** |
| MHV/MLV universal static TP | No single accepted universal formula | Not established | Disabled | **HOLD / DO NOT INVENT** |

## 4. Structural target is not the same as broker TP

A target such as `D1 Low BB` is a **Bid-chart structural coordinate**. A broker TP is an order price whose trigger side depends on direction.

Current MT4 execution geometry used by the project:
- BUY opens at Ask and closes/TP triggers on Bid;
- SELL opens at Bid and closes/TP triggers on Ask;
- MT4 chart/candle indicator structure is Bid-based.

Therefore:
- BUY structural Top-BB target is naturally aligned with BUY broker TP trigger side;
- SELL structural Low-BB target is **not** trigger-side aligned if the same numeric Bid-derived level is sent directly as broker TP.

If structural semantics are explicitly chosen as `close when Bid reaches the structural SELL target`, the broker-side approximation at entry/preflight is:

`SELL BrokerTP ~= StructuralBidTarget + frozen spread`

This is **broker execution normalization**, not a new BBMA target rule.

However spread can change after entry. A frozen-spread conversion preserves entry-time geometry only and cannot guarantee exact later Bid-touch equivalence under spread widening/narrowing.

## 5. Current code verdict

Current M17 code is contract-compliant with its existing static outer-BB mapping. There is no coding defect merely because provenance is weaker than previously implied.

The defect is documentation/governance if the H1/H4/D1 outer-BB table is described as explicit universal Oma Ally Core.

Therefore until a strategy decision changes exit authority:
- current structural TP table may remain temporarily as **PROJECT_EXECUTION_POLICY**;
- it must not be promoted to `PDF_CORE` or universal `BBMA_STRATEGY_CORE`;
- lifecycle exits remain disabled/HOLD;
- no fixed-pip or RR-manufactured substitute target may be introduced.

## 6. RR / money-management consequence

Any broker-side TP normalization changes actual reward distance. `MinRRRatio`, when enabled, must be evaluated from the final broker Entry/SL/TP geometry actually sent after normalization.

A TP must never be pushed farther merely to preserve a previous nominal RR. Likewise lot sizing remains owned by SL/risk, not by target-distance manipulation.

## 7. Safe autonomous engineering sequence

The following work is authorized without inventing new strategy semantics:
1. implement the separately user-approved Re-Entry structural-range hard-SL decision;
2. update M17 provenance wording so current static Re-Entry/REM/RRE/REE TP is labelled project policy, not universal Core;
3. preserve current TP code semantics during the SL patch;
4. add/retain diagnostics that distinguish structural target from broker target;
5. compile 0E0W and run static regression;
6. keep SELL TP Bid/Ask normalization as an explicit pending TP execution decision because it changes broker target price even though it is engineering-motivated.

## 8. Strategy decision gate that remains

Before a final TP redesign, one strategy-level question remains genuinely non-derivable from current accepted sources:

**For Re-Entry-owned trades (standalone H1, REM, RRE, REE), should production execution retain a static directional outer-BB TP as explicit project policy, or should static TP be removed/replaced only after a future source-authorized lifecycle exit rule is promoted?**

Until that decision is made, the safe state is:
- preserve the current static table as project policy;
- do not claim it as universal BBMA Core;
- do not enable HOLD lifecycle closes;
- do not silently alter TP price for SELL spread normalization.

## 9. Final verdict

- **Extreme TP-Wajib:** source-authoritative Core.
- **Directional outer BB:** valid structural context, not universal mandatory TP authority.
- **Current H1/H4/D1 Re-Entry-owned outer-BB hard TP table:** deterministic project execution policy with community/derived support, but not certified universal Core.
- **Post-Re-Entry lifecycle close:** HOLD under current 2026-08-25 precedence.
- **SELL TP Bid/Ask normalization:** technically valid execution concern, but pending explicit TP execution decision because it changes broker TP price.

No TP strategy code change is authorized by this audit alone.
