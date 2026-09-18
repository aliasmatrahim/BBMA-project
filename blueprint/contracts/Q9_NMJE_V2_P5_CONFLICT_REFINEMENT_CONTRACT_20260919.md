# Q9 NMJE v2 P5 Conflict Refinement Contract — 2026-09-19

Issue: #101  
Base: retrospective P2/P3 source reconciliation PR #195  
Target: Build 4.90 / `V490_Q9_P5_CONFLICT_REFINEMENT_20260919`  
Status: SHADOW-DIAGNOSTIC ONLY / NO ACTIVATION

## Source boundary

Accepted N1/M12N rules remain controlling:
- lower-timeframe activity may be part of a higher-timeframe journey;
- opposite-looking child activity does not automatically prove an independent reversal;
- `NESTED_CONFLICT` requires resolved authoritative states that cannot coexist under accepted parent/child interpretation;
- raw/pre-direction Extreme or MHV must not be labelled conflict merely because nominal direction differs;
- uncertain provenance/semantics must fail closed.

Group-3 and PRIMARY15 are corroboration only for this P5 work. They do not add a new executable BBMA rule.

## P5 bounded mapping

For M5 shadow refinement only:
- same-direction confirmed M5 Re-Entry remains diagnostic `ALIGNED`;
- same-direction candidate M5 Re-Entry remains diagnostic `SUPPORTING`;
- opposite candidate M5 Re-Entry remains diagnostic `BUILDING`;
- opposite confirmed M5 Re-Entry is `UNRESOLVED` because current source/owner scope does not prove a universal genuine structural conflict;
- same-direction active M5 Extreme remains diagnostic `SUPPORTING`;
- opposite active M5 Extreme is `BUILDING`, never automatic `CONFLICT`.

No P5 branch may manufacture a genuine M5 conflict without stronger authoritative child-owner evidence.

## Authority invariants

P5 cannot:
- create/reject/rank/delay a candidate;
- change comparator/PriorityEngine/M16;
- create a second processing clock;
- alter risk, lot, SL/TP or broker execution;
- activate P2 tie-break ordering.

M15 remains sole processing/final-decision clock. M5 remains observation/refinement only.

## HOLD

A universal rule converting opposite confirmed M5 Re-Entry into genuine `NESTED_CONFLICT` remains HOLD/UNRESOLVED. The safe current mapping is diagnostic `NESTED_UNRESOLVED`.

No HOLD item is executable.
