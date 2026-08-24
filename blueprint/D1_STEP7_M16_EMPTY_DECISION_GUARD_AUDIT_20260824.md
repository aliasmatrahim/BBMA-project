# D1 Step 7 — M16 Empty-Decision Guard Audit

Date: 2026-08-24  
Branch: `d1-owner-dev`  
Build: `Version 4.5.1 - D1-07 M16 Empty Decision Guard`  
Status: **IMPLEMENTED / STATIC PASS / NATIVE METAEDITOR 0E0W PASS**

## Runtime evidence
User broker/demo Experts output showed repeated `[D1-03][M16_D1_REJECT]` records with blank `DecisionID`, `FrozenState=D1_OWNER_UNRESOLVED`, `FrozenDir=DIR_NONE`, and `FrozenCandle=1970.01.01`, while the same pairs had valid M11 `[OWNER]` BUY/SELL-confirmed snapshots.

## Root cause
`BBMA_Decision` is zero-initialized in M27. `ENUM_DECISION_STATE` value zero is `DEC_CREATED`. When M15 selected no candidate, the empty decision therefore still satisfied the old `DecisionState == DEC_CREATED` gate and was incorrectly sent into M16. Because M15 had never frozen a D1 snapshot, M16 correctly rejected the empty object, producing a false runtime rejection trace.

## Fix
M27 now calls `InvalidationEngine_Atomic()` only when both:
- `decision.Valid == true` (M15 actually selected/created a decision); and
- `decision.DecisionState == DEC_CREATED`.

This matches the M15/M16 contracts: M16 revalidates an M15-created pending decision; it must not process a zero/default object.

## Strategy / architecture impact
- No BBMA detector, D1 owner formula, D1 gate, candidate selection, SL/TP, risk, money-management, order execution, or live-position lifecycle rule changed.
- Real D1 snapshot mismatch/transition/unresolved rejection remains fail-closed for actual selected decisions.
- The fix removes false `1970 / blank DecisionID` M16 rejection noise and prevents an empty object from being recorded as a strategy invalidation path.

## Verification
Focused static invariant check: **PASS**.  
Native MT4 MetaEditor: **0 errors / 0 warnings; EX4 produced**.
