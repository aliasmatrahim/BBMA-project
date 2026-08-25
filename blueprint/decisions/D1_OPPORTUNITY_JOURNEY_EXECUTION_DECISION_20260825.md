# D1O-01 — D1 BBMA Opportunity Journey Execution Decision

Date: 2026-08-25  
Status: **APPROVED EXECUTION EXTENSION**

## Authorization
The user explicitly authorized activation of the previously KIV D1 BBMA Opportunity Journey strategy and continuous implementation. This is a project execution extension built from accepted BBMA Core stages; its exact software predicates are project rules and must not be misrepresented as verbatim source wording.

## Core separation
Two authorities remain distinct:

1. **D1 Strategic Owner** — existing MA50 major-trend context.
2. **D1 BBMA Opportunity Journey** — a BBMA lifecycle parent that can authorize a search for a fresh lower-timeframe setup.

Opportunity context is never a direct order trigger. M15 remains the sole final new-entry authority and M16 remains fail-closed validation.

## Active opportunity families

### D1_OPP_EXTREME_TPW
- Requires a reversal-confirmed D1 Extreme; RAW Extreme is insufficient.
- Extreme and its normal TP-Wajib path are one journey, not two opportunities.
- The journey is inactive once normal TP Wajib has structurally completed.
- This is the only tactical family allowed to oppose the MA50 strategic-owner direction.
- Tactical execution requires stronger LTF confirmation: recovered/valid aligned H4 directional owner plus a fresh confirmed H1 Re-Entry in the opportunity direction.

### D1_OPP_CSD
- Requires source-valid confirmed D1 CSD.
- D1 eCSD remains WATCH ONLY and cannot activate execution by itself.
- Candidate direction must align with an execution-ready D1 Strategic Owner.
- Actual entry still requires a fresh confirmed LTF Re-Entry.

### D1_OPP_RE_ENTRY
- Confirmed D1 Re-Entry is the primary/strongest opportunity family.
- Further Re-Entry belongs to this same family.
- Candidate direction must align with an execution-ready D1 Strategic Owner.
- Exact REM/RRE/REE signatures remain unchanged.

### D1_OPP_MOMENTUM_RETRACE
- Requires source-valid D1 Momentum/CSM.
- Momentum is never chased directly.
- A fresh lower-timeframe Re-Entry after the D1 opportunity activation time is mandatory.
- Candidate direction must align with an execution-ready D1 Strategic Owner.

## Watch-only states
- D1 MHV/MLV: WATCH ONLY; no independent directional execution authority.
- D1 eCSD: WATCH ONLY; no independent ordinary execution authority.

## Temporal safety
A D1 event becomes usable only after its source D1 candle has closed. LTF setup readiness must occur strictly after the D1 opportunity activation time; no H1/M15 setup that was already complete before the D1 event became knowable may be reused.

## LTF execution and deduplication
- Phase 1 execution uses confirmed H1 and M15 Re-Entry structures only; no raw LTF Extreme/CSD/eCSD/Momentum becomes a direct entry.
- H1 confirmed Re-Entry may qualify under a normal D1 opportunity.
- M15 confirmed Re-Entry additionally requires an active, recovered, same-direction H4 directional owner.
- Extreme/TPW tactical opportunity requires H4 alignment plus H1 confirmed Re-Entry; M15-only is insufficient.
- If H1 and M15 are both fresh in the same processing cycle, they are canonicalized into one opportunity cluster; H1 owns structural SL/TP source preference.
- A later genuinely fresh LTF Re-Entry with a new confirmation anchor/sequence identity may create another trade, subject to existing portfolio/risk caps.
- Duplicate opportunity sequence identity must never execute twice.

Opportunity identity basis:

`D1 CycleID + OpportunityFamily + fresh LTF Re-Entry confirmation identity`

## Existing behavior preserved
- `EntryMode=MODE_1_RE_ENTRY_ONLY` retains the previous selective strategy behavior.
- D1 Opportunity execution is enabled only under `MODE_2_ALL_VALIDATED_BBMA`.
- Existing REM/RRE/REE signatures are unchanged.
- Existing strategic-owner rules for legacy candidates are unchanged.
- Existing `MaxTradePerPair`, `MaxTotalTrade`, `MaxActivePair`, spread, drawdown, total-risk, lot, SL/TP and broker execution gates remain final.
- Existing M17 SL/TP formula remains structural: source Re-Entry wick plus one broker point for SL, opposite Bollinger destination for TP. Opportunity entries may use H1 or M15 Re-Entry as the source TF according to the selected cluster.
- No confidence score, weighting, voting or hidden ranking is introduced.

## Validation gates
1. Static ownership guards confirm no change to exact REM/RRE/REE construction.
2. Native MT4 MetaEditor compile must be 0 errors / 0 warnings.
3. Runtime smoke must show no fatal MT4 signatures before production use.
4. Existing N2 telemetry continues recording validated decisions and closed outcomes for post-activation measurement.