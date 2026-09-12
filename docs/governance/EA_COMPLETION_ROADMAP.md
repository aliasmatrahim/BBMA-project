# EA Completion Roadmap

## Purpose

This is the delivery roadmap for BBMA Professional EA from source-evidence finalisation to controlled deployment. It is a governance and progress document, **not** BBMA Strategy-Core authority.

The live repository, current source routing in `docs/references/SOURCE_INDEX.md`, accepted Core, active contracts, canonical EA source, and runtime/test evidence remain authoritative. A roadmap item may be marked `COMPLETE`, `IN PROGRESS`, `BLOCKED / HOLD`, or `NO FIX REQUIRED`; it must not create a Core rule merely to complete a checklist.

## Mandatory model-routing policy

Every roadmap item must pass the Model Routing Gate in `docs/governance/MODEL_ROUTING_POLICY.md` before substantive analysis or mutation. The gate must be re-evaluated whenever new evidence materially changes semantic, architecture, authority, lifecycle, or regression risk.

Routing is based on **decision risk, not task size**.

Allowed gate results:

- `MODEL GATE: SOL HIGH DEFAULT — PROCEED`
- `MODEL GATE: ASTRA RECOMMENDED — OPTIONAL ESCALATION`
- `MODEL GATE: ⚠️ ASTRA REQUIRED — JANGAN STEP DOWN`

When Astra becomes mandatory, Sol may continue safe evidence collection, indexing, diffing, compile/static/runtime evidence gathering, or other mechanical work, but must not finalize the disputed semantic/architecture adjudication or implement an unresolved authority change.

## Model convention

Phase-level model labels are only allocation guidance. The per-item Model Routing Gate and `MODEL_ROUTING_POLICY.md` control escalation.

- `Terra Medium`: mechanical/clerical evidence work, routine QA, compile invocation and low-risk documentation where no semantic adjudication is required.
- `Sol High`: default substantive model for BBMA audit, architecture review, implementation, regression analysis and runtime diagnosis when current evidence/contracts determine the answer.
- `Astra High/XHigh`: escalation tier. It is **required** only when a hard trigger in `MODEL_ROUTING_POLICY.md` is active; otherwise it may be recommended but is not mandatory.
- `Luna`: mechanical/clerical work only; never final BBMA Core adjudication or EA strategy mutation.

## Update convention

Every work update must identify the phase letter, phase title, recommended model, precise item when applicable, and current Model Routing Gate.

Example: `A3 — Source & Evidence Finalisation [Sol High] — BBMA Video Evidence Extraction — MODEL GATE: SOL HIGH DEFAULT — PROCEED`  
Example escalation: `B4 — Architecture & Gap Confirmation — MODEL GATE CHANGED: SOL HIGH → ⚠️ ASTRA REQUIRED — JANGAN STEP DOWN`

## Mandatory resume/preflight sequence

Before beginning or resuming a roadmap item:

`live GitHub governance/branch → CURRENT.md → MASTER_QUEUE.md → roadmap item → MODEL_ROUTING_POLICY.md → SOURCE_INDEX.md when strategy-relevant → relevant evidence/Core/contracts → current code → runtime/test evidence → Model Routing Gate → work`

A new chat must re-read/re-evaluate the gate from repository state. Chat memory is navigation aid only.

## Completion Tree

```text
BBMA Professional EA — Roadmap hingga siap
│
├─ A. Source & Evidence Finalisation [Terra Medium / Sol High]
│  ├─ A1. Finalize corrected subtitle
│  ├─ A2. QA timestamp, file integrity & UNCLEAR register
│  ├─ A3. BBMA video evidence extraction
│  ├─ A4. Core reconciliation: MATCH / PARTIAL / UNCLEAR
│  └─ A5. Update provenance, conflict/HOLD & gap register
│
├─ B. Architecture & Gap Confirmation [Sol High default; Astra hard-gate escalation]
│  ├─ B1. Full preflight live repository
│  ├─ B2. Strategy-Core gap audit M01–M27 + M12N
│  ├─ B3. Confirm genuine Core/code mismatch
│  ├─ B4. Reconcile blueprint, contracts & lifecycle ownership
│  └─ B5. Prioritise confirmed gaps only
│
├─ C. Controlled Core Implementation [Sol High default; Astra hard-gate escalation]
│  ├─ C1. Scoped fix per module
│  ├─ C2. Preserve signal lifecycle
│  ├─ C3. Prevent duplicate logic / cross-pair state leakage
│  └─ C4. Build identity, traceability & queue evidence
│
├─ D. Technical Validation [Terra Medium / Sol High; Astra only on hard trigger]
│  ├─ D1. Strict MQL4 compile
│  ├─ D2. Static + cross-module regression audit
│  ├─ D3. Strategy Tester scenario validation
│  ├─ D4. Closed-candle chronology & state/log/order validation
│  └─ D5. F7 execution-lifecycle runtime closure
│
├─ E. Operational Readiness [Sol High default]
│  ├─ E1. Risk/MM, execution & dashboard separation audit
│  ├─ E2. Demo forward validation
│  ├─ E3. Genuine entry/exit/telemetry outcomes
│  └─ E4. Resolve confirmed runtime defects only
│
├─ F. Release Candidate Gate [Sol High default; Astra required for unresolved semantic/architecture dispute]
│  ├─ F1. Compile clean
│  ├─ F2. Regression clean
│  ├─ F3. Tester + runtime evidence sufficient
│  ├─ F4. HOLD/UNCLEAR excluded from execution
│  └─ F5. Version, changelog & release evidence complete
│
└─ G. Controlled Deployment [Terra Medium / Sol High; Astra on hard-trigger defect]
   ├─ G1. User review / approval
   ├─ G2. Deploy to chosen demo/live environment
   └─ G3. Post-deployment runtime watch
```

## Per-item Model Routing Gate

The default below is not permission to skip the mandatory gate. Any item must be escalated immediately if a hard Astra trigger appears.

| Item | Default | Item-specific gate note |
| --- | --- | --- |
| A1 | Terra Medium | Escalate to Sol for technical BBMA wording; Astra only if correction requires unresolved semantic adjudication. |
| A2 | Terra Medium | Sol for provenance/integrity contradiction; Astra only if contradiction changes semantic interpretation. |
| A3 | Sol High | Evidence extraction only; Astra required only if extraction itself leaves multiple materially plausible BBMA meanings that must be adjudicated. |
| A4 | Sol High | Astra required for unresolved cross-source conflict or multiple plausible Core interpretations affecting accepted/executable semantics. |
| A5 | Sol High | Astra required if updating conflict/HOLD/gap status would effectively promote unresolved evidence into accepted Core. |
| B1 | Sol High | Repository/state preflight is deterministic; Astra is not required merely because the repository is large. |
| B2 | Sol High | Astra required when the audit exposes unresolved source conflict or non-deterministic authority semantics. |
| B3 | Sol High | Astra required when mismatch classification changes canonical Core/contract meaning and cannot be resolved deterministically. |
| B4 | Sol High | Astra required for cross-module authority/lifecycle contradiction where ownership must be redefined or moved. |
| B5 | Sol High | Astra required only if prioritisation depends on unresolved semantic/architecture adjudication. |
| C1 | Sol High | Accepted-contract implementation stays Sol; Astra required if the fix needs a new/changed Core or architecture authority decision. |
| C2 | Sol High | Astra required if lifecycle ownership or transitions are genuinely disputed across modules. |
| C3 | Sol High | Sol handles confirmed duplicate/state-isolation bugs; Astra required only if ownership resolution is non-deterministic. |
| C4 | Sol High | Build identity/traceability is deterministic; no Astra by default. |
| D1 | Terra Medium | Native compile/dependency validation is mechanical; escalate to Sol for unresolved compile diagnosis. |
| D2 | Sol High | Astra required only when regression diagnosis reveals a non-deterministic Core/ownership conflict. |
| D3 | Sol High | Tester evidence must not invent rules; Astra required if interpreting failures would decide unresolved BBMA semantics. |
| D4 | Sol High | Astra required if chronology/state evidence exposes conflicting processing-clock or lifecycle authority with no deterministic contract answer. |
| D5 | Sol High | Astra required if F7 closure requires unresolved entry/exit/lifecycle authority adjudication rather than mechanism validation. |
| E1 | Sol High | Astra required only if separation audit exposes genuine authority redesign across strategy/risk/execution/UI. |
| E2 | Sol High | Forward validation is evidence work; Astra required only for unresolved semantic interpretation, not for ordinary outcome analysis. |
| E3 | Sol High | Outcome/telemetry attribution remains Sol unless evidence creates a non-deterministic Core/authority question. |
| E4 | Sol High | Confirmed runtime bug fixes remain Sol; Astra required for unresolved architecture/semantic root cause that changes authority. |
| F1 | Terra Medium | Compile cleanliness is mechanical; unresolved semantic issues cannot be waived by a clean compile. |
| F2 | Sol High | Astra required if a release-significant regression has multiple plausible semantic/architecture causes after full evidence retrieval. |
| F3 | Sol High | Astra required when sufficiency depends on unresolved Strategy-Core or authority adjudication. |
| F4 | Sol High | Astra required if any HOLD/UNCLEAR item is proposed for promotion; otherwise exclusion verification remains Sol. |
| F5 | Terra Medium | Version/changelog/evidence packaging is mechanical; Sol for traceability conflict. |
| G1 | Sol High | User approval remains required where governance says so; Astra only if approval is blocked by unresolved hard-trigger analysis. |
| G2 | Terra Medium | Deployment is mechanical after gates pass; Astra cannot substitute for missing release/deployment authorization. |
| G3 | Sol High | Routine watch/diagnosis stays Sol; Astra required if a critical defect activates a hard semantic/architecture trigger. |

## Eighteen delivery points

1. **A1 — Finalize Corrected Subtitle**
2. **A2 — QA Timestamp & UNCLEAR Register**
3. **A3 — BBMA Video Evidence Extraction**
4. **A4 — Core Reconciliation: MATCH / PARTIAL / UNCLEAR**
5. **A5 — Update Source Index, Provenance & Conflict/HOLD Register**
6. **B1 — Full EA Preflight: Governance → Core → Contracts → Source → Runtime Evidence**
7. **B2 — Strategy-Core Gap Audit M01–M27 + M12N**
8. **B5 — Prioritise Confirmed Gaps Only**
9. **B4 — Blueprint & Lifecycle Contract Reconciliation**
10. **C1 — Scoped Implementation Fixes per Module**
11. **D1 — Strict MQL4 Compile & Dependency Validation**
12. **D2 — Cross-Module Regression Audit**
13. **D3 — Strategy Tester Validation**
14. **D5 — F7 / Execution-Lifecycle Runtime Closure**
15. **E1 — Risk/MM, Execution & Dashboard Separation Audit**
16. **E2 — Demo Forward Validation**
17. **F — Release Candidate Gate**
18. **G — Controlled Deployment**

## Safeguards

- No `HOLD`, `UNCERTAIN`, `UNRESOLVED` or `REJECT` item may enter executable Strategy Core.
- Detector, lifecycle, risk and execution retain separate ownership.
- Any EA source change requires a unique build identifier, compile evidence, targeted regression, and traceable runtime/test evidence.
- Draft PRs are not merged or deployed automatically.
- A model upgrade does not create authority: Astra cannot invent a rule, override source precedence, bypass accepted contracts, replace compile/runtime evidence, or authorize merge/deployment/trading.
- If a hard Astra trigger appears mid-task, use `MODEL GATE CHANGED: SOL HIGH → ⚠️ ASTRA REQUIRED — JANGAN STEP DOWN` before final adjudication continues.
