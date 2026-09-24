# NMJE V1 ↔ V2 Current-Owner Implementation Reconciliation — 2026-09-25

Status: **COMPLETE / NO CURRENT-OWNER CODE FIX REQUIRED / OLD V2 BRANCH NOT DIRECT-MERGEABLE**
Issue: #101
Live owner: `d1-owner-dev@f14dc3caad4127e3525744c444469d69e4a53b3a`
Owner EA: Build `5.11` / `V511_EVENT_DRIVEN_OBSERVER_20260922`
V2 P11 reference: `q9-nmje-v2-p11-lineage-refinement-101@ddaf4d5855a9f1ddadffd5effff8edab5e71848f`, Build `4.96`.

## 1. Scope and source gate

This audit resumes the 2026-09-24 V1/V2 source-inheritance reconciliation after its only governance blocker was closed by PR #272.
The source report `NMJE_V1_V2_FULL_SOURCE_RECONCILIATION_20260924.md` remains controlling for source semantics:
- V1 read-only observation/lineage semantics are source-compatible;
- V2 may extend provenance/accuracy metadata only;
- execution authority remains NONE;
- M15 remains the sole processing/final-decision clock;
- M5 remains closed-candle context/shadow only;
- P2 active ordering remains HOLD unless separately authorized.

PR #272 now explicitly routes Group-3/PRIMARY15 and the strict G40-wide supplemental layers in `SOURCE_INDEX.md`, so the prior source-routing blocker is closed.

## 2. Mechanical current-owner comparison

Machine-readable evidence: `blueprint/audits/evidence/NMJE_V1_V2_20260925/current_owner_compare.json`.
- Owner defines 43 `NMJE_*` functions; V2 P11 defines 80.
- All 43 owner NMJE functions exist in V2.
- 41/43 shared functions are normalized-body exact.
- The only two shared-body differences are `NMJE_PrintValidatedDecisionShadow` and `NMJE_PrintClosedOutcomeShadow`; V2 only expands research telemetry output.
- V2 adds 37 NMJE functions, all belonging to P2-P8/P10/P11 shadow/provenance/attribution layers.
### P1 identity substrate

Current owner already contains the P1 identity substrate required before M5 can be attached:
- `D1MajorTrendOwner.EpochStartCandleTime` is present;
- `NestedTFNode.CanonicalEventID` is present;
- `NestedJourneyState.ParentEventID` is present;
- `NMJE_BuildD1Node`, `NMJE_BuildH4Node`, `NMJE_BuildH1Node`, `NMJE_BuildM15Node`, `NMJE_BuildJourneyID` and `NMJE_ResolveParent` are normalized-body exact between owner and V2;
- D1/H4/Re-Entry/Extreme/MLV canonical EventID helpers are also normalized-body exact.

Disposition: **P1 ALREADY INTEGRATED/EQUIVALENT IN CURRENT OWNER — DO NOT REAPPLY.**

### V2-only data surfaces

V2 adds four research structs absent from owner:
- `NMJEM5RefinementState`;
- `NMJEShadowAttributionState`;
- `NMJEStructuralDensityState`;
- `NMJEEntryDisplacementState`.

V2 also adds StableRelation/provenance-stability, maturity, structural-density, M5-refinement and first/new-journey fields to `NestedJourneyState`, plus frozen research metadata to `BBMA_Decision` and post-fill research metadata to `TradeInfo`.

Current owner separately adds newer execution hardening not present in the old V2 branch, including `PendingExecutionAmbiguity` and subsequent Build 5.11 execution/risk/lifecycle work.

## 3. Authority-firewall verification
Both owner and V2 satisfy the read-only firewall:
- `NMJE_PassExecutionGate` count = 0;
- `REJ_NMJE_RELATION` count = 0;
- legacy `BlockNMJEConflict` / `BlockNMJEBuilding` exist only as inactive compatibility inputs;
- owner has no `PERIOD_M5` NMJE wiring; V2 has M5 references only in the shadow research layer.

Protected executable functions contain zero `NMJE_*` and zero M5 references in both sources:
- `CompareCanonicalCandidates`;
- `PriorityEngine_Atomic`;
- `InvalidationEngine_Atomic`;
- `ResolveApprovedInitialSLTP`;
- `CheckRiskBeforeTrade`;
- `RunEntryPreflightAndExecute`;
- `IsSignalAllowed`;
- `SendOrderWithRetry`;
- `ResolveExecutionReferencePrice`;
- `ResolveSelectedSLTPSourceComponent`;
- `IsApprovedSLTPSourceComponent`.

`ResolveApprovedInitialSLTP`, `SendOrderWithRetry`, `ResolveExecutionReferencePrice`, `ResolveSelectedSLTPSourceComponent` and `IsApprovedSLTPSourceComponent` are normalized-body exact between owner and V2.
Other protected functions differ because owner advanced through later Build 5.11 risk/execution/integration work, but none consumes NMJE/M5 metadata.

Result: **no hidden V2 execution gate, score, reject path, risk authority or second processing clock found.**

## 4. P1-P11 reconciliation matrix
| Stage | Current-owner reconciliation | Disposition |
|---|---|---|
| P1 Temporal lineage / epoch | Identity substrate already present/equivalent in Build 5.11 | **ALREADY INTEGRATED — DO NOT REAPPLY** |
| P2 Journey coherence | V2 prints equal-eligibility metadata before PriorityEngine; comparator/order untouched | **KEEP SHADOW ONLY; ACTIVE ORDERING HOLD** |
| P3 M5 micro-context | Absent in owner; V2 implements closed-M5 context only | **VALID RESEARCH CONCEPT; REMATERIALIZE FROM CURRENT OWNER IF RESUMED** |
| P4 Shadow outcome attribution | Concept remains additive, but old V2 persistence predates current owner execution/F7/C044 hardening | **REBASE/RE-AUDIT REQUIRED; DO NOT TRANSPLANT OLD PERSISTENCE** |
| P5 Conflict refinement | Diagnostic mapping is conservative; opposite confirmed M5 RE remains UNRESOLVED | **KEEP DIAGNOSTIC; TRUE-CONFLICT RULE HOLD** |
| P6 Journey maturity | Non-ordinal categorical fingerprint only | **KEEP RESEARCH METADATA; NO SCORE/GATE** |
| P7 Structural density | Bitmask/cardinality telemetry only | **KEEP RESEARCH METADATA; NO RANK/THRESHOLD** |
| P8 Provenance stability | Identity-based observer hysteresis; no bar/time delay | **KEEP CONCEPT; REMATERIALIZE/RE-AUDIT FROM OWNER** |
| P9 SL semantic-source audit | No source change; current owner semantic source resolvers remain normalized-body exact | **PASS / NO FIX** |
| P10 Entry displacement | Post-fill telemetry only; current owner execution/retry/ambiguity path is newer | **KEEP CONCEPT; REBASE AFTER CURRENT EXECUTION IDENTITY** |
| P11 First/new-journey lineage | Strict canonical JourneyID semantics remain valid research metadata | **KEEP CONCEPT; REMATERIALIZE FROM OWNER** |

## 5. Old V2 branch merge assessment

GitHub comparison of `d1-owner-dev` against `q9-nmje-v2-p11-lineage-refinement-101` reports:
- branches diverged;
- V2 branch is 64 commits ahead but **164 commits behind** current owner;
- merge base is `01f7e8305f6ba558494fc559bb3c734dfc06124a`;
- EA source delta is approximately +2247 / -104 lines relative to current owner.

Current owner also contains later execution/risk/lifecycle architecture absent from the old V2 branch, including execution-ambiguity ownership and Build 5.11 integration work.

Classification: **CONFIRMED REGRESSION RISK**.
Impact: directly merging PR #205 could overwrite or reintroduce stale versions of protected execution/risk/lifecycle logic even though the NMJE research itself passed its historical gates.
Fix: **do not direct-merge PR #205**. Retain it as verified research provenance. Any resumed V2 implementation must start from the then-current owner and rematerialize only the still-approved shadow/provenance pieces.
## 6. Current-owner verdict

**NO FIX** for current Build 5.11 NMJE authority/identity correctness.

Reasons:
- the read-only NMJE authority repair is already integrated;
- P1 provenance identity is already present and matches the accepted V2 identity substrate;
- no V2 relation/M5 field is consumed by candidate eligibility, canonical comparison, M16, risk or OrderSend;
- P9 semantic SL/TP-source ownership remains correct in the current owner;
- the remaining P2-P8/P10/P11 features are research/shadow metadata, not prerequisites for canonical BBMA correctness or current Q10 acceptance.

No Strategy-Core rule changes.
No execution/risk/lifecycle authority changes.
No M5 processing-clock or execution authority.
No P2 active ordering.

## 7. Validation / evidence

- Live owner recovered after PR #272: `f14dc3caad4127e3525744c444469d69e4a53b3a`.
- P11 research branch recovered clean at `ddaf4d5855a9f1ddadffd5effff8edab5e71848f`.
- Historical P11 checkpoint remains VERIFIED: focused/inherited tests PASS, canonical/runtime/tester MetaEditor 0E/0W, deterministic A/B exact, authority trace exact, broker actions 0.
- Current-owner vs V2 function/struct/firewall comparison is machine-recorded in `blueprint/audits/evidence/NMJE_V1_V2_20260925/current_owner_compare.json`.
- SOURCE_INDEX routing prerequisite is now closed by merged PR #272.
- No EA source bytes are changed by this reconciliation, so no new BuildID or duplicate native compile is required.
- Q3 and Q10 runtime terminals are outside scope and remain untouched.

## 8. Exit status

**NMJE V1 ↔ V2 CURRENT-OWNER RECONCILIATION = COMPLETE.**

- Accepted Core delta: `NONE`.
- Current-owner code fix: `NONE`.
- V1/P1 identity substrate: integrated/equivalent.
- V2 P2-P8/P10/P11: retained as bounded research concepts requiring fresh current-owner rematerialization if resumed.
- P2 active tie-break ordering: `HOLD / NON-EXECUTABLE`.
- M5 authority: `SHADOW CONTEXT ONLY`.
- PR #205 direct merge: `NO — SUPERSEDED IMPLEMENTATION BASE / REGRESSION RISK`.
- Production activation from this audit: `NONE`.

A future Issue #101 implementation step, if explicitly sequenced, must branch from live owner and begin with the smallest current-owner P2/P3 shadow rematerialization rather than merging historical Build 4.96 source wholesale.