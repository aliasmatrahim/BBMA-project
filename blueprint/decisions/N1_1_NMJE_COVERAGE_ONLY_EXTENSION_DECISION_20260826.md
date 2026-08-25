# N1.1 — NMJE Coverage-Only Extension Decision

Date: 2026-08-26  
Branch: `d1-owner-dev`  
Status: **APPROVED ENGINEERING COVERAGE EXTENSION / NO STRATEGY OR EXECUTION CHANGE**

## Purpose
Close the observability gaps identified by `NMJE_D1_M15_COVERAGE_AUDIT_20260826.md` while preserving the N1 invariant:

`TRADE BEHAVIOUR BEFORE NMJE == TRADE BEHAVIOUR AFTER NMJE`

N1.1 is an engineering/read-only extension of M12N/NMJE. It does not grant nested context any execution authority.

## Locked scope
N1.1 may:
1. expose current `D1OpportunityJourney` as read-only overlay metadata;
2. expose already-owned Re-Entry and Extreme lifecycle states as secondary node metadata, including M15 Re-Entry and M15 Extreme;
3. expose current M15 MHV/MLV state as secondary metadata beside other simultaneous M15 states;
4. extend `NMJE_HasChildActivity()` to recognize already-owned M15 Re-Entry and M15 Extreme state;
5. extend SUPPORTING/BUILDING observation only where the state already exists and without creating a strategy detector;
6. add compact N1.1 diagnostic output for the added overlays;
7. preserve the existing primary node and JourneyID/parent rules for compatibility.

## Hard prohibitions
N1.1 must NOT:
- call or reimplement `DetectExtreme`, MHV/MLV detection, `DetectCSD`, `DetectECSD`, `DetectCSM`, Re-Entry detection, D1 MA50 formula or combination detection from NMJE;
- add a new `NESTED_PARENT_*` kind for D1 Opportunity;
- change parent preference `H4 RE -> H4 owner -> D1 RE -> D1 strategic owner`;
- create/reject/rank an M15 candidate;
- modify EntryMode behavior;
- alter exact REM/RRE/REE signatures;
- alter M15 final authority or M16 revalidation;
- alter SL/TP, M19/M20 risk, M21 lot sizing, M22 execution, M23 lifecycle or M24 recovery;
- introduce confidence score, weighting, voting or hidden priority;
- infer missing producer state.

## Coverage mapping
### D1
Keep the primary D1 node behavior unchanged. Add secondary read-only visibility for:
- D1 Re-Entry BUY/SELL states;
- D1 Extreme BUY/SELL maturity;
- active D1 Opportunity family/direction/source/activation/tactical/TPW/CycleID metadata.

D1 Opportunity remains an overlay, not a parent kind.

### H4
Preserve current primary node behavior. Secondary metadata may expose simultaneous H4 Re-Entry and Extreme states already owned by the EA.

### H1
Preserve current primary node behavior. Secondary metadata may expose simultaneous H1 Re-Entry and Extreme states already owned by the EA.

### M15
Preserve current MHV/MLV primary-node behavior for compatibility. Add secondary read-only visibility for:
- M15 Re-Entry BUY/SELL;
- M15 Extreme BUY/SELL maturity;
- M15 MHV/MLV BUY/SELL lifecycle state.

Transient M15 CSD/eCSD/CSM snapshots are outside N1.1 because there is no dedicated immutable NMJE snapshot interface for them yet. They remain a future observability item, not an execution gap.

## Relation semantics
N1.1 remains conservative:
- existing confirmed H1 Re-Entry `ALIGNED/CONFLICT` authority remains unchanged;
- M15 Re-Entry and M15 Extreme may make child activity visible as `BUILDING`/supporting context when existing rules do not already resolve the relation;
- opposite-looking M15 activity must not automatically become `CONFLICT` merely from raw direction;
- N1.1 does not create any entry eligibility from relation state.

## Provenance tags
- recursive/nested BBMA principle: `[BBMA-ORIGINAL]` / source-supported principle;
- Re-Entry, Extreme, TP-Wajib, MHV/MLV lifecycle concepts: `[BBMA-ORIGINAL]` at their canonical strategy layer;
- D1 Opportunity execution families where separately approved: preserve their existing provenance, including `D1_OPP_EXTREME_TPW` as `[BBMA-SOURCE-CONSISTENT][PROJECT-EXTENSION]`;
- NMJE overlays, node fields, JourneyID and diagnostics: `[ENGINEERING-ONLY]`;
- no new strategy semantics are authorized here.

## Verification gates
1. exact v4.56 source baseline identity verified before patch;
2. source version receives a new unique build identifier;
3. C044 gate remains OFF;
4. M12N forbidden detector/execution-call scan PASS;
5. M13/M14/M15/M16/M17/M19/M20/M21/M22/M23/M24 protected-surface regression PASS;
6. exact REM/RRE/REE signatures unchanged;
7. existing N2 `[N2-NMJE-DEC]` decision identity fields remain compatible;
8. native MT4 MetaEditor = 0 errors / 0 warnings;
9. no broker runtime is required to prove the read-only source boundary, although future real N2 outcome evidence still requires broker/runtime logs.
