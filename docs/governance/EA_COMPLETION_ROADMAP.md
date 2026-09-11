# EA Completion Roadmap

## Purpose

This is the delivery roadmap for BBMA Professional EA from source-evidence finalisation to controlled deployment. It is a governance and progress document, **not** BBMA Strategy-Core authority.

The live repository, current source routing in `docs/references/SOURCE_INDEX.md`, accepted Core, active contracts, canonical EA source, and runtime/test evidence remain authoritative. A roadmap item may be marked `COMPLETE`, `IN PROGRESS`, `BLOCKED / HOLD`, or `NO FIX REQUIRED`; it must not create a Core rule merely to complete a checklist.

## Model convention

The recommended model and reasoning effort are embedded in each phase title. They are a work-allocation guide, not an authority override:

- `Terra Medium`: default daily work.
- `Astra High/XHigh`: Core, architecture, implementation, unresolved defect diagnosis, and release gates.
- `Luna`: mechanical/clerical work only; never Core audit or EA changes.

## Update convention

Every work update must identify the phase letter, phase title, recommended model, followed by the precise item when applicable.

Example: `A3 — Source & Evidence Finalisation [Terra Medium] — BBMA Video Evidence Extraction`  
Example: `D4 — Technical Validation [Terra Medium / Astra High for unresolved diagnosis] — Closed-Candle Chronology & State/Log/Order Validation`

## Completion Tree

```text
BBMA Professional EA — Roadmap hingga siap
│
├─ A. Source & Evidence Finalisation [Terra Medium]
│  ├─ A1. Finalize corrected subtitle
│  ├─ A2. QA timestamp, file integrity & UNCLEAR register
│  ├─ A3. BBMA video evidence extraction
│  ├─ A4. Core reconciliation: MATCH / PARTIAL / UNCLEAR
│  └─ A5. Update provenance, conflict/HOLD & gap register
│
├─ B. Architecture & Gap Confirmation [Astra High/XHigh]
│  ├─ B1. Full preflight live repository
│  ├─ B2. Strategy-Core gap audit M01–M27 + M12N
│  ├─ B3. Confirm genuine Core/code mismatch
│  ├─ B4. Reconcile blueprint, contracts & lifecycle ownership
│  └─ B5. Prioritise confirmed gaps only
│
├─ C. Controlled Core Implementation [Astra High]
│  ├─ C1. Scoped fix per module
│  ├─ C2. Preserve signal lifecycle
│  ├─ C3. Prevent duplicate logic / cross-pair state leakage
│  └─ C4. Build identity, traceability & queue evidence
│
├─ D. Technical Validation [Terra Medium / Astra High for unresolved diagnosis]
│  ├─ D1. Strict MQL4 compile
│  ├─ D2. Static + cross-module regression audit
│  ├─ D3. Strategy Tester scenario validation
│  ├─ D4. Closed-candle chronology & state/log/order validation
│  └─ D5. F7 execution-lifecycle runtime closure
│
├─ E. Operational Readiness [Terra Medium]
│  ├─ E1. Risk/MM, execution & dashboard separation audit
│  ├─ E2. Demo forward validation
│  ├─ E3. Genuine entry/exit/telemetry outcomes
│  └─ E4. Resolve confirmed runtime defects only
│
├─ F. Release Candidate Gate [Astra XHigh]
│  ├─ F1. Compile clean
│  ├─ F2. Regression clean
│  ├─ F3. Tester + runtime evidence sufficient
│  ├─ F4. HOLD/UNCLEAR excluded from execution
│  └─ F5. Version, changelog & release evidence complete
│
└─ G. Controlled Deployment [Terra Medium / Astra High for critical defect]
   ├─ G1. User review / approval
   ├─ G2. Deploy to chosen demo/live environment
   └─ G3. Post-deployment runtime watch
```

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
