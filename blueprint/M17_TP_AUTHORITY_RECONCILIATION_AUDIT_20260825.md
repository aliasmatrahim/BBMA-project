# M17 TP Authority Reconciliation Audit — 2026-08-25

Branch: `d1-owner-dev`
Status: **AUDIT COMPLETE / NO TP CODE CHANGE AUTHORIZED / MATERIAL STRATEGY HOLD PRESERVED**

## Scope

Reconcile the current M17 Re-Entry-owned static TP implementation against the latest authoritative 2026-08-25 Strategy Core / Home Course reconciliation after completion of the separately approved M17 structural-range hard-SL update.

This record does **not** change EA source behavior.

## Authority order

For executable promotion this audit follows:

`Primary source evidence -> BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2 -> HOME_COURSE_19P_CROSS_SOURCE_RECONCILIATION_20260825 -> HOME_COURSE_49_FAMILY_CORE_REVALIDATION_20260825 -> current contracts/code`.

The 2026-08-25 reconciliation is later and more specific than the exploratory 2026-08-24 F7 lifecycle audits. Their precedence notices explicitly prevent older provisional `RESOLVED` lifecycle conclusions from becoming executable authority.

## Current source behavior

Current M17 still resolves a non-zero Bollinger destination from the approved Re-Entry source component:
- BUY -> source-timeframe upper BB;
- SELL -> source-timeframe lower BB.

The currently mapped source timeframes remain:
- standalone Re-Entry -> H1, with the approved D1 Opportunity H1/M15 identity exception preserved by current code;
- REM -> H4 Re-Entry component;
- RRE/REE -> D1 Re-Entry component.

This audit does not modify that implementation.

## Latest authoritative reconciliation

The 2026-08-25 cross-source gate classifies:
- Candle Arah outer-BB destination as **PARTIAL/HOLD as a predictive/universal target claim**;
- `Re-Entry -> no Momentum => mandatory TP/reversal` as a **MATERIAL STRATEGY HOLD**;
- pre-Re-Entry/post-direction outer-BB hold/no-TP exceptions as **MATERIAL STRATEGY HOLDS**.

The 49-family revalidation preserves the same boundary:
- C034 outer-BB destination = PARTIAL/HOLD;
- C035 strong direction reaches outer BB before Re-Entry/no Momentum -> hold/no-TP = HOLD;
- C044 Re-Entry -> no Momentum => universal mandatory TP/reversal exit = HOLD.

Therefore neither of the following may be silently promoted as universal BBMA Core now:
1. current static outer-BB broker TP for every Re-Entry-owned trade;
2. historical F7 dynamic no-Momentum mandatory close/reversal lifecycle.

## Proven rule kept separate

Normal Extreme TP-Wajib remains a distinct accepted Core concept. The accepted normal first TP-Wajib area is the opposite MA5/MA10 area, with Mid BB as farther/maximum context. This does not authorize reusing that Extreme TP formula as a universal Re-Entry TP.

## Executable decision for the current build

**NO TP SOURCE CHANGE.**

For version 4.52:
- retain the existing static outer-BB TP implementation for continuity as the current **project execution-policy payload**, not as a newly promoted universal Oma Ally/Core law;
- do not add SELL TP spread normalization in this step;
- do not remove broker TP;
- do not enable post-Re-Entry no-Momentum dynamic close;
- do not alter M23/M24 lifecycle ownership;
- do not invent a new MinRR reward model.

This is a conservative change-control decision: the approved M17 source change in this build is the structural hard-SL / broker-side SELL SL normalization only.

## Strategy-decision boundary

A future TP architecture change is blocked by a genuine material strategy decision. Any of these would require explicit approval plus a new implementation series:
- remove the current static Re-Entry-owned broker TP;
- replace it with lifecycle-only profit taking;
- enable universal no-Momentum mandatory close/reversal behavior;
- define coexistence/precedence between a static TP and lifecycle close;
- normalize SELL TP to Bid-chart structure using spread;
- change MinRR treatment because the deterministic entry-time reward target changes.

Until that decision is made, current TP behavior is frozen and must not be described as stronger source authority than the evidence supports.

## Final verdict

**TP AUTHORITY: HOLD AT CURRENT EXECUTION BEHAVIOR / NO NEW CODE AUTHORITY.**

The M17 structural-SL implementation may close independently. TP remains a separately governed strategy item and is not a blocker to validating the approved SL correction.
