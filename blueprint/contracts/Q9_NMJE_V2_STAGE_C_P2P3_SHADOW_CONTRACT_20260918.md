# Q9 NMJE v2 Stage-C / P2-P3 Shadow Contract — 2026-09-18

Issue: #101
Stack base: verified Q9 P1 Build 4.87A
Target build: 4.88 / V488_Q9_NMJE_M5_SHADOW_20260918
Status: ISOLATED / SHADOW-ONLY / NO ACTIVATION

## Scope

Stage C materializes the latest fully closed M5 sample only during the existing M15 processing cycle and derives read-only M5 Re-Entry/Extreme context using the existing canonical detector/lifecycle helpers.

The M5 result is stored only in NMJE shadow provenance:
- EventID;
- ParentEventID;
- JourneyID;
- direction/context family;
- closed M5 candle;
- canonical relation;
- reason.

## P2 boundary

Issue #101 authorizes journey-coherence metadata for equal-eligibility arbitration, but no deterministic ordering between ALIGNED/SUPPORTING/BUILDING/CONFLICT is locked by the current source contract.

Therefore Build 4.88 records coherence metadata only when two or more candidates are already eligible under the existing canonical eligibility + D1 authority rules.

It does not:
- score candidates;
- reorder candidates;
- change CompareCanonicalCandidates;
- reject a sole valid candidate;
- delay M15 selection;
- change PriorityEngine or M16 semantics.

Activation of a coherence tie-break ordering remains HOLD/UNRESOLVED pending an explicit deterministic policy decision.

## P3 boundary

M5 is context/refinement only:
- no M5 processing clock;
- no M5 CSD/eCSD/CSM/MLV candidate family;
- no M5 candidate creation;
- no M5 rejection/ranking/execution authority;
- no M5 risk or lifecycle authority.

Temporary M5 conflict is diagnostic only and cannot invalidate a valid M15 decision.

## Validation gate

Require:
- focused Stage-C/P2 static PASS;
- Q9 P1/read-only/identity/order/firewall regressions PASS;
- protected M13/M14/M15/M16/M17/M22 implementation unchanged;
- native MetaEditor 0 errors / 0 warnings;
- isolated runtime proves exact build identity, closed-M5 shadow telemetry, M15 clock behavior and zero broker actions;
- no merge or activation without explicit authorization.
