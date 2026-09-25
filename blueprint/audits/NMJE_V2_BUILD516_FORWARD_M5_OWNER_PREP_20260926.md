# NMJE V2 Build 5.16 — Current-Owner Demo Forward Evidence + Canonical M5 Owner Preparation — 2026-09-26

Status: **IMPLEMENTED / STATIC+NATIVE+TARGETED+TESTER PASS / DEMO INSTANCE ATTACHED / BROKER-FORWARD OUTCOME EVIDENCE PENDING**

Issue: #101  
Owner base: `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de`  
Scoped branch: `q9-nmje-v2-build516-forward-m5-prep-101`

## Build identity

- Build: `5.16`
- Build tag: `V516_NMJE_FORWARD_M5_OWNER_PREP_20260926`
- Source revision: `NMJE_FORWARD_M5_OWNER_PREP_001_20260926`
- MQ4 SHA-256: `98E2C669C90DEAF42A2EE8CAA5AFE2551C0AEBE8E59B61DC2EF261CD406ACD96`
- Native EX4 SHA-256: `6230BE87E4F9FFA3BB44310158F66AF995D7646F28FB5319256148920F23023F`
- Tester harness EX4 SHA-256: `85DDDA614598D8164E5F523364FCE45E58EBBE770741CC54595B3009309F8BD2`

## Scope

Build 5.16 prepares the shortest safe path toward future full NMJE V1/V2 activation without activating a new trading policy.

1. Current-owner P2 counterfactual evidence can run in Strategy Tester or explicitly enabled demo only.
2. Real-account forward evidence is hard blocked by `NMJE_IsForwardEvidenceEnabled()`.
3. M5 semantic state is materialized through the canonical M08/M09/M10/M12 owner functions.
4. NMJE remains a read-only consumer of M5 semantic owner state.
5. M15 remains the sole processing clock.
6. P2 active ordering remains HOLD.
7. P5 true `NESTED_CONFLICT` remains HOLD.
8. No alternate broker order is created.

## Canonical M5 owner preparation

A symbol-local `M5SemanticOwnerState` now owns M5 copies of:
- M08 Extreme lifecycle;
- M09 MHV/MLV lifecycle;
- M10 CSD/eCSD/CSM direction snapshots;
- M12 Re-Entry lifecycle.

The M5 owners are updated oldest-to-newest for newly closed M5 candles from the M15-owned processing cycle. Missing/ambiguous closed-candle continuity fails closed.

NMJE P3 does not call any detector. It consumes the canonical owner state and applies only the already-approved bounded P5 diagnostic mapping:
- same-direction confirmed M5 Re-Entry -> ALIGNED;
- same-direction candidate M5 Re-Entry -> SUPPORTING;
- opposite candidate M5 Re-Entry -> BUILDING;
- opposite confirmed M5 Re-Entry -> UNRESOLVED;
- same-direction active M5 Extreme -> SUPPORTING;
- opposite active M5 Extreme -> BUILDING.

Multiple simultaneously mapped M5 semantic states remain UNRESOLVED because no precedence is source-owned.

## Authority firewall

Protected executable functions are normalized-body exact to Build 5.15 owner base:
- `CompareCanonicalCandidates`
- `PriorityEngine_Atomic`
- `InvalidationEngine_Atomic`
- `CheckRiskBeforeTrade`
- `IsSignalAllowed`
- `ResolveExecutionReferencePrice`
- `ResolveSelectedSLTPSourceComponent`
- `IsApprovedSLTPSourceComponent`
- `SendOrderWithRetry`
- `RunEntryPreflightAndExecute`

Broker primitive count remains exact: `OrderSend=1 / OrderClose=3`.

Canonical C044 state-machine functions are unchanged.

## Validation

### Static / targeted

- `git diff --check`: PASS.
- Build 5.16 targeted regression: PASS.
- Full repository Python suite: **72/72 PASS**.
- One traceability defect was found during the first suite run: the F7 build line still said 5.15. It was corrected to 5.16; no strategy semantics changed.

### Native compile

Exact production source:
- MetaEditor: **0 errors / 0 warnings**.
- log: `evidence/NMJE_V2_BUILD516_20260926/native_compile_rev002.log`.

Tester harness:
- MetaEditor: **0 errors / 0 warnings**.
- log: `evidence/NMJE_V2_BUILD516_20260926/harness_compile_rev002.log`.

### Isolated Strategy Tester

GBPUSD M15, 2026-08-01 through 2026-09-01:
- clean deinit;
- 14 executions;
- **14/14 execution trace exact to Build 5.15**;
- 2,016 M5 canonical-owner observation rows;
- M5 semantic resolved: 1,123 rows;
- M5 diagnostic relations:
  - BUILDING 307;
  - UNRESOLVED 1,026;
  - SUPPORTING 287;
  - ALIGNED 272;
  - N/A 124;
- genuine `NESTED_CONFLICT` activation rows: **0**;
- P2 counterfactual: 3 sets / 9 OPEN / 9 OUT;
- fatal runtime faults: **0**.

The high UNRESOLVED count is expected fail-closed behavior: 769 rows contain multiple canonical mapped states without a source-owned precedence, and 257 rows are opposite confirmed M5 Re-Entry where true-conflict remains HOLD.

## Demo-forward checkpoint

A separate dormant MetaQuotes-Demo portable terminal was used so Q3 and Q10 remain untouched.

- terminal root: `D:\BBMA\MT4_Q5_180_Demo`
- Build 5.16 attached successfully on GBPUSD M15;
- 20-pair fixed list;
- `MaxActivePair=1`;
- `EnableNMJEForwardEvidence=true`;
- StrategyID `93`;
- InstanceID `95`;
- dedicated process PID at attach: `15204`.

At this checkpoint the terminal has confirmed config load and expert attach. A fresh current-session broker login/closed outcome has not yet been observed, so this is **NOT BROKER-FORWARD VERIFIED** and no N3 activation claim is made.

## Remaining activation blockers

### P0 / REQUIRED FOR NMJE EXECUTION POLICY
- current-owner Build 5.16 real broker-connected demo decision/outcome evidence;
- attributable P2 alternative evidence across broader pairs/periods;
- explicit P2 execution/tie-break policy decision;
- P5 true-conflict decision if conflict is to become executable.

### P1 / REQUIRED BEFORE ACTIVE AUTHORITY
- protected-surface implementation of the approved N3 policy;
- default-OFF activation switch;
- restart/recovery validation for any M5 semantic state that becomes execution-relevant;
- native compile, regression and broker/demo validation of the active-policy build.

## Exit decision

**Build 5.16 preparation scope is complete.**

Classification:
- canonical M5 semantic-owner preparation: **VALIDATED**;
- V2 demo-forward evidence plumbing: **VALIDATED / DEMO-ONLY**;
- Strategy-Core execution delta: **NONE**;
- P2 ordering: **HOLD / NON-EXECUTABLE**;
- P5 true conflict: **HOLD / NON-EXECUTABLE**;
- N3 execution policy: **INACTIVE**;
- real broker-forward outcome evidence: **VERIFICATION REQUIRED**.
