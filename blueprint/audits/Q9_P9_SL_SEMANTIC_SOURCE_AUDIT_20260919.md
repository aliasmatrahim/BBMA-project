# Q9 P9 — SL Semantic-Source Refinement Audit — 2026-09-19

Issue: #101  
Branch: `q9-nmje-v2-p9-sl-semantic-source-audit-101`  
Base: verified P8 head `f3bf90ea184eb63b15aac8bce8fe3eaeb083ce26`  
EA identity: unchanged Build 4.93 / `V493_Q9_P8_PROVENANCE_STABILITY_20260919`  
Classification: **NO FIX / AUDIT PASS**

## Objective

Audit that the final M17 SL/TP structural source belongs to the actual M15-selected BBMA candidate/combination, and that multiple valid structural components cannot change the final owner merely because of component processing order.

This audit does not redefine BBMA SL/TP formulas. Numeric wick/range/broker-buffer geometry remains project/EA engineering mapping unless separately source-authorized.

## Source / authority basis

Mandatory source route:
1. `docs/references/SOURCE_INDEX.md`;
2. `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`;
3. accepted component/MTF decisions;
4. current Build 4.93 source.

Relevant accepted Core:
- Re-Entry is the principal setup/entry zone in the normal cycle.
- Exact MTF signatures remain:
  - REM = H4 Re-Entry + H1 Extreme + M15 MHV/MLV;
  - RRE = D1 Re-Entry + H4 Re-Entry + H1 Extreme;
  - REE = D1 Re-Entry + H4 Extreme + H1 Extreme.
- D1 MA50 strategic gating is separate from combination component identity and does not add a new REM component.
- Higher-TF Re-Entry may be completed/read through lower-TF structures without making the lower-TF completion an independent owner.

Relevant approved D1O clarification:
`blueprint/decisions/D1O_CANONICAL_LTF_DEDUP_CLARIFICATION_20260825.md`
explicitly locks:
- H1 owns execution identity when H1+M15 are both present in the same D1-opportunity cluster;
- H1 remains the structural SL/TP source preference;
- M15 is supporting completion/timing metadata in that dual-component case;
- M15 owns only when it is the sole fresh LTF Re-Entry.

Core also explicitly rejects personal MA10+allowance methodology as a universal BBMA SL rule and classifies non-universal SL/TP broker formulas as project/EA-safety mappings.

## Current owner-resolution matrix

| M15-selected candidate | Valid structural components | Current frozen SL/TP source | Audit result |
| --- | --- | --- | --- |
| Standalone Re-Entry | H1 Re-Entry | H1 Re-Entry | PASS |
| Standalone Extreme | H1 retest-ready Extreme | H1 Extreme | PASS |
| REM | H4 Re-Entry + H1 Extreme + M15 MHV/MLV | H4 Re-Entry | PASS |
| RRE | D1 Re-Entry + H4 Re-Entry + H1 Extreme | D1 Re-Entry | PASS |
| REE | D1 Re-Entry + H4 Extreme + H1 Extreme | D1 Re-Entry | PASS |
| D1 opportunity: H1 + M15 fresh RE cluster | H1 Re-Entry + M15 Re-Entry | H1 Re-Entry | PASS |
| D1 opportunity: M15-only fresh RE | M15 Re-Entry | M15 Re-Entry | PASS |

## Processing-order audit

`ResolveSelectedSLTPSourceComponent()` does not use generic “first component wins” behavior.

For normal candidates it resolves by:
- selected `SequenceType`;
- required semantic component type;
- exact expected timeframe;
- matching direction;
- valid source candle identity.

Explicit mapping:
- standalone Re-Entry -> H1;
- REM -> H4;
- RRE/REE -> D1;
- standalone Extreme -> H1 Extreme.

For D1 opportunity clusters, the resolver performs an explicit H1 pass followed by an M15 pass. Therefore component-array order cannot override the approved H1 preference.

The candidate builders also constrain the component universe:
- normal REM/RRE/REE signatures contain only one component matching the required source type/timeframe;
- D1 opportunity contains at most one H1 Re-Entry and one M15 Re-Entry.

Result: **no accidental processing-order owner selection found**.

## Downstream identity / geometry audit

After M15 selects the candidate:
1. `PriorityEngine_Atomic()` freezes the exact selected candidate components.
2. `ResolveSelectedSLTPSourceComponent()` freezes the semantic SL/TP source into `decision.SLTPSourceComponent`.
3. M16 revalidates every decision component against current authoritative lifecycle identity.
4. `RunEntryPreflightAndExecute()` calls M17 only after `DEC_VALIDATED`.
5. `IsApprovedSLTPSourceComponent()` independently rechecks source component type/timeframe/direction for the selected signal family.
6. `ResolveMatchingReEntryLifecycle()` requires exact source direction + timeframe + confirmation candle identity.
7. `ResolveSourceOwnedStructuralAnchor()` reconstructs only that source Re-Entry lifecycle window from `StartCandleTime` through `ConfirmationCandle`.
8. Standalone Extreme uses its exact H1 Extreme lifecycle identity and exact raw-to-retest-completion window.
9. Risk/MM receives the already-finalized M17 stop through the frozen execution/risk snapshot; risk does not select or replace the strategy source.

No fallback was found that substitutes:
- another valid combination component;
- array position;
- ATR/volatility stop;
- generic swing lookback;
- risk/MM-derived SL source.

## Formula boundary

This audit validates **semantic owner selection**, not universal source authority for every numeric M17 formula.

Project/engineering mappings retained unchanged include:
- source-owned lifecycle-window low/high reconstruction;
- standalone Extreme raw-to-retest structural window;
- tick-size normalization;
- SELL broker-side spread buffer;
- downstream broker stop-level validation.

No new BBMA rule is inferred from those formulas.

## Validation reuse

No EA source changed in P9.

The exact base source remains the already-verified P8 Build 4.93 candidate:
- canonical MQ4 SHA-256:
  `C041423D53E0425D3070BB5F1C1BB8DC083A0DF65874CC848C1A30040E55E17E`;
- exact runtime-name EX4 SHA-256:
  `CF9C02B041CC409F651F496F04E35A96D68523DE1D8AC4F0FFAC3BC6F1CACE2A`;
- native MetaEditor: 0 errors / 0 warnings;
- P8 deterministic Strategy Tester and authority regression: PASS.

Because P9 changes no EA bytes and finds no defect, recompiling/retesting an identical binary would be duplicate work rather than new evidence.

G40 Remote Desktop Commander reported the device online during recovery, but command execution was timing out. No Q3/Q6 process was restarted, replaced or duplicated.

## Result

**P9 SL semantic-source audit: PASS / NO FIX.**

The selected candidate's approved structural source is already frozen deterministically and independently of incidental component processing order.

No Build 4.94 is justified.  
No EA/Core/risk/execution change.  
No merge / no production activation.

Next Issue #101 item after P9 is P10 — Entry Displacement Telemetry.
