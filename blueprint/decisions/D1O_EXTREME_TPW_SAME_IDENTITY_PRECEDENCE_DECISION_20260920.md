# D1O EXTREME_TPW Same-Identity Lifecycle Precedence Decision

Date: 2026-09-20
Issue: #214
Status: **APPROVED USER DECISION / SCOPED EXECUTION-SEMANTIC CLARIFICATION**

## Problem

A valid standalone H1 Re-Entry and a valid `D1_OPP_EXTREME_TPW` candidate can resolve to the exact same canonical execution identity:

`Pair + Direction + H1 + ConfirmationCandle`.

D1O-07 already locks that fresh LTF Re-Entry identity as the single execution/dedup identity. The D1 Extreme TP-Wajib contract separately locks D1 Extreme as the TP semantic owner for `D1_OPP_EXTREME_TPW`.

Without an explicit precedence rule, current candidate ordering can retain the standalone attribution and therefore assign generic C044 lifecycle semantics to an execution identity that simultaneously has valid EXTREME_TPW attribution.

## User decision

**Option A — exact same-identity enrichment.**

When and only when:
- standalone H1 Re-Entry is otherwise valid;
- `D1_OPP_EXTREME_TPW` is otherwise valid;
- both resolve to the exact same BUY/SELL H1 Re-Entry confirmation identity;

they are one canonical executable identity, not two independent trades.

## Ownership

For that exact overlap:
- H1 Re-Entry remains **entry / execution / dedup identity owner**;
- H1 Re-Entry remains **hard-SL structural owner**;
- D1 Extreme / `D1_OPP_EXTREME_TPW` owns **TP semantics**;
- D1 TP-Wajib lifecycle owns the **normal strategy exit lifecycle**;
- M15 remains the sole final new-entry authority;
- M20 emergency precedence remains unchanged;
- M22 remains a dumb/idempotent executor;
- no second SequenceHash, DecisionID, execution hash, ticket or order may be created.

This is identity enrichment, not identity replacement.

## Exact scope

This decision does **not** create generic D1 Opportunity priority.

It does not give new precedence to:
- `D1_OPP_CSD`;
- `D1_OPP_RE_ENTRY`;
- `D1_OPP_MOMENTUM_RETRACE`.

It does not change standalone H1/H4 ownership outside the exact same-identity EXTREME_TPW overlap.

A different direction, timeframe, confirmation anchor or sequence identity remains a different candidate and continues through the existing canonical ordering rules.

## Gate behavior

The dedicated D1 TP-Wajib lifecycle gate remains authoritative.

While that feature gate is OFF, an enriched `D1_OPP_EXTREME_TPW` identity must continue to fail closed before execution. It must not silently fall back to:
- generic C044 lifecycle;
- static Re-Entry outer-BB TP;
- standalone attribution merely to preserve trade frequency.

## Implementation boundary

The smallest implementation is an M15 canonical tie-break for exact same-identity overlap.

Forbidden implementation changes:
- no new detector;
- no new signal family;
- no second execution identity;
- no change to D1O family activation;
- no change to H1/M15 confirmation rules;
- no change to DecisionID generation;
- no change to M16 authority revalidation;
- no change to M17 formulas;
- no change to risk/MM;
- no change to M22/M24 execution/recovery identity;
- no production activation from this decision alone.

Validation must prove order-independent selection of EXTREME_TPW attribution for the exact overlap and no behavior change outside that scope.
