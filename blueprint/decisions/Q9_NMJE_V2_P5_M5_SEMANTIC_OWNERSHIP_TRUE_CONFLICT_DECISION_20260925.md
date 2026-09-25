# Q9 NMJE V2 P5 — M5 Semantic Ownership + True-Conflict Adjudication — 2026-09-25

Status: **DECIDED / SEMANTIC OWNERSHIP BOUNDARY RESOLVED / TRUE-CONFLICT HOLD / NO EA CODE CHANGE**

Issue: #101  
Base: `d1-owner-dev@ce2d6c06d225f964a5eddc2291697d14f0efafb2`

## 1. Scope

This decision adjudicates only:
1. who may own M5 BBMA semantic state for NMJE V2; and
2. whether current source evidence is sufficient to classify an opposite M5 child as genuine `NESTED_CONFLICT`.

It does not activate P2 ordering, add an M5 processing clock, create/reject/rank a trade, or alter Strategy Core/risk/execution authority.

## 2. Source route used

Mandatory source order was followed:
- `docs/references/SOURCE_INDEX.md`;
- `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`;
- primary/secondary PDF rule indexes and accepted Finale V01-V07 reconciliation;
- original Finale V05/V06 subtitle evidence for the material MTF passages;
- authenticated Home Course reconciliation;
- G40-wide Group-3/PRIMARY15 + Tier-A/B/C reconciliation closures;
- active M12N/M15/M16 contracts;
- current Build 5.13 source and runtime evidence.

Historical P5 Build 4.90 contract was reviewed as provenance only and was not treated as current implementation authority.

## 3. Evidence findings

### 3.1 M5 as lower-timeframe BBMA structure — SOURCE-SUPPORTED

Accepted Core V2 §9 states that the BBMA structural principle scales across:
- D1/H4/H1;
- H4/H1/M15;
- H1/M15/M5;
- M15/M5/M1.

Finale V05 explicitly teaches smaller-timeframe completion and examples that include M5. V06 likewise teaches that a higher-timeframe Re-Entry is completed/read through smaller-timeframe setup/signal structure.

Therefore:
**M5 may contain genuine BBMA semantic structures such as Extreme, MHV/MLV, direction and Re-Entry.**

This does not itself grant M5 execution authority.

### 3.2 Opposite-looking lower-TF direction is not automatically reversal — SOURCE-SUPPORTED

Core V2 §9 explicitly states that an opposite-looking lower-timeframe direction signal must not automatically be treated as an independent reversal when it is structurally part of higher-timeframe Re-Entry context.

Original Finale V05 around 00:34:48–00:36:37 demonstrates an opposite-looking lower-TF BUY direction inside a larger SELL Re-Entry context and explains that the lower-TF direction can be completing the higher-timeframe Re-Entry.

Therefore:
**opposite child direction alone is insufficient evidence for genuine structural conflict.**

### 3.3 Mixed-direction shortcut wording exists, but hard rejection is not accepted

Finale V05 around 00:52:09 teaches a shortcut that prefers all-up/all-down timeframe alignment and says to leave mixed chains. The reconciled rule `OA-F-V05-018` is explicitly:
**CLARIFY / HOLD for hard coding**.

It cannot override the stronger accepted Core interpretation that lower-TF opposition may be part of higher-TF Re-Entry completion.

Therefore the shortcut is not a universal M5 reject/conflict rule.

### 3.4 Supplemental G40 evidence adds no stronger conflict authority

The completed G40-wide reconciliation classifies recursive lower-timeframe support as bounded/corroborative MTF only:
- no child-to-parent state synthesis;
- no new timeframe owner;
- no second processing clock;
- no independent M5 create/reject/rank/execute authority;
- accepted Core delta = NONE.

No reconciled Group-3/PRIMARY15, Tier-A, Tier-B or Tier-C evidence supplies a deterministic universal M5 true-conflict rule.

## 4. Semantic ownership decision

**M5 BBMA semantics must NOT be detected or invented inside NMJE/M12N.**

If M5 semantic state is materialized in a future implementation:
- Extreme semantics remain owned by M08;
- MHV/MLV semantics remain owned by M09;
- eCSD/CSD/CSM semantics remain owned by M10;
- Re-Entry semantics remain owned by M12.

Any M5 support must be an explicit extension/generalization of the canonical owner contract/implementation, with no duplicate detector/lifecycle owner.

NMJE may only consume the resulting source-owned M5 snapshot as read-only context.

Processing remains:
**closed M5 semantic owner state -> sampled by NMJE on the sole closed-M15 processing cycle -> diagnostics/shadow only**.

M15 remains the sole final new-entry authority.

## 5. P5 bounded diagnostic mapping

Once a canonical source-owned M5 semantic snapshot exists, the historical bounded P5 mapping remains acceptable as **diagnostic-only**:

- same-direction confirmed M5 Re-Entry -> `ALIGNED`;
- same-direction candidate M5 Re-Entry -> `SUPPORTING`;
- opposite candidate M5 Re-Entry -> `BUILDING`;
- opposite confirmed M5 Re-Entry -> `UNRESOLVED`;
- same-direction active M5 Extreme -> `SUPPORTING`;
- opposite active M5 Extreme -> `BUILDING`.

This mapping does not create `NESTED_CONFLICT` and has no candidate/risk/execution authority.

## 6. True-conflict adjudication

Classification: **HOLD / UNRESOLVED / NON-EXECUTABLE**.

Current source evidence does not provide a deterministic universal condition that separates:
- temporary lower-TF retracement/opposition that completes a higher-TF journey; from
- a genuinely independent M5 structural reversal that should become `NESTED_CONFLICT`.

A raw/pre-direction Extreme or MHV/MLV cannot be classified as conflict merely because its nominal direction differs.

An opposite confirmed M5 Re-Entry is also not sufficient, by itself, to prove true conflict.

## 7. Release criteria for future true-conflict work

P5 true-conflict may leave HOLD only if all are satisfied:
1. canonical M5 semantic owner coverage exists under M08/M09/M10/M12 without duplicate logic;
2. M5 state uses fully closed candles and stable event/parent provenance;
3. stronger authoritative evidence or an explicit project decision defines a deterministic boundary between retracement/completion and genuine structural conflict;
4. the rule does not create a second processing clock;
5. any future use that rejects, delays, ranks or otherwise changes an eligible trade receives a separate explicit strategy-policy authorization and attributable regression/runtime evidence.

## 8. Current Build 5.13 code disposition

Current code intentionally records:
- latest closed M5 OHLC snapshot;
- `M5SemanticResolved=false`;
- `M5DiagnosticRelation=NESTED_UNRESOLVED`;
- reason `M5_SIGNAL_SEMANTICS_NOT_MATERIALIZED_TRUE_CONFLICT_HOLD`.

This is the correct fail-closed implementation for the present owner coverage.

Classification: **NO FIX**.

No Build bump, native compile or Strategy Tester rerun is required because this adjudication changes no EA source bytes.

## 9. Final P5 status

- M5 lower-TF BBMA semantics: **SOURCE-SUPPORTED conceptually**.
- M5 semantic owner: **canonical signal owners only; NMJE read-only consumer**.
- Current M5 semantic implementation: **NOT MATERIALIZED**.
- Temporary/opposite child activity: **must not automatically become conflict**.
- P5 diagnostic subtype mapping: **accepted for future shadow use once M5 owner state exists**.
- Universal M5 true conflict: **HOLD / NON-EXECUTABLE**.
- Accepted Strategy-Core delta: **NONE**.
- Current EA code fix: **NONE**.
