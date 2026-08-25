# GAP-A1 — D1 Opportunity EXTREME_TPW Ownership Reconciliation

Date: 2026-08-26
Branch: `d1-owner-dev`
Baseline: `Version 4.5.7 - N1.1 NMJE Coverage Overlay`
Status: **SOURCE SEMANTIC OWNERSHIP RESOLVED / BROKER-EXIT MAPPING STRATEGY-GATED / NO CODE CHANGE**

## Problem

`D1_OPP_EXTREME_TPW` is an approved D1 Opportunity family, but the current executable candidate uses a fresh LTF Re-Entry cluster. M17 therefore receives the Re-Entry component as `SLTPSourceComponent` and, while C044 is OFF, resolves the ordinary Re-Entry outer-BB project-policy TP.

That conflates three different identities:
1. execution/dedup identity;
2. strategy attribution identity;
3. TP semantic ownership.

## Reconciled ownership split

### Execution / dedup identity
Unchanged and locked by D1O-07:

`Pair + Direction + fresh LTF Re-Entry TF + LTF confirmation anchor`

- H1 owns the execution identity when H1+M15 are simultaneous;
- M15 owns it when M15 is the only fresh LTF Re-Entry;
- D1 CycleID and OpportunityFamily remain attribution metadata and cannot manufacture a second trade identity.

### Opportunity attribution identity
Unchanged:

`D1 CycleID + D1 OpportunityFamily + D1 source + D1 activation + authority mode`

### TP semantic owner for `D1_OPP_EXTREME_TPW`
Resolved:

**The TP semantic owner is the active D1 Extreme TP-Wajib lifecycle, not the LTF Re-Entry execution identity.**

Accepted Core gives the normal first TP-Wajib structure:
- D1 Extreme SELL -> opposite D1 MA5/MA10 Low area first;
- D1 Extreme BUY -> opposite D1 MA5/MA10 High area first;
- D1 Mid BB is farther/maximum context and does not replace the normal first objective.

Therefore the LTF Re-Entry outer-BB target cannot be described as the semantic TP-Wajib destination merely because the LTF Re-Entry owns execution/dedup identity.

## Existing canonical D1 TP-Wajib completion mapping

The active D1 Opportunity engine already implements source-aligned structural completion in `D1OpportunityTPWCompletedSince()`.

For every fully closed D1 candle after the Extreme confirmation:
- SELL Extreme: TP-Wajib structure is completed when candle `Low <= D1 MA5 Low` **or** `Low <= D1 MA10 Low`;
- BUY Extreme: TP-Wajib structure is completed when candle `High >= D1 MA5 High` **or** `High >= D1 MA10 High`.

The MA5/MA10 values are evaluated on each relevant closed D1 candle. They are not frozen to one entry-time numeric price.

This existing function is structural journey evidence. It does not itself execute a broker close.

## Why no autonomous static-TP patch is permitted

Accepted source authority defines an MA5/MA10 **area / structural completion**, but does not uniquely define a single frozen MT4 broker TP price for a later LTF entry.

A static TP implementation would have to invent at least one policy choice that is not source-locked:
- freeze the D1 MA values at Extreme confirmation vs D1 activation vs LTF execution;
- choose MA5 vs MA10 vs the first boundary of the MA5/MA10 area;
- decide whether the broker should close intrabar at the frozen line or only after source-timeframe structural completion is confirmed.

Because the existing canonical completion mapping is dynamic by closed D1 candle, a frozen static TP is not equivalent to it.

## Gap classification

The original `SLTP-01` HIGH finding is split as follows:

- **semantic ownership mismatch: CLOSED** — D1 Extreme TP-Wajib owns TP semantics; LTF Re-Entry remains execution/dedup owner;
- **exact broker-exit mechanism: STRATEGY/EXECUTION DECISION REQUIRED** — not safely derivable from current accepted sources;
- **current Re-Entry outer-BB TP for this family: known provisional/mismatched behaviour while the family remains executable with C044 OFF**.

No code is changed by this reconciliation because silently choosing a static MA target or a new lifecycle-close mechanism would be a material trading-behaviour decision.

## Safe options requiring explicit strategy decision

1. **Lifecycle-managed D1 TP-Wajib exit**
   - preserve LTF Re-Entry execution identity;
   - no competing Re-Entry outer-BB broker TP for `D1_OPP_EXTREME_TPW`;
   - position management consumes canonical closed-D1 TP-Wajib completion evidence and closes through lifecycle ownership.

2. **Frozen broker TP project policy**
   - explicitly choose the freeze time and exact MA5/MA10-area numeric mapping;
   - classify it as project execution policy if not directly source-defined.

3. **Temporarily fail-close / disable `D1_OPP_EXTREME_TPW` execution** until an exit mapping is approved.

None of these is selected by this source reconciliation record.

## Non-change guarantees

- no change to H1/M15 execution hash ownership;
- no change to D1 CycleID attribution;
- no change to REM/RRE/REE;
- no N1/N2/N3 work resumed;
- no C044 activation;
- no invented fixed-pip/RR TP;
- C044 gate remains OFF.

## Verdict

**GAP-A1 source ownership is reconciled. The remaining blocker is a genuine strategy/execution choice about how the dynamic D1 TP-Wajib structural area becomes a broker exit.**
