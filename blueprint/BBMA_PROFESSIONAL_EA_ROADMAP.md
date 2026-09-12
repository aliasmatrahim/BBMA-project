# BBMA Professional EA — Roadmap hingga Siap

Version: 1.0
Status: WORKING ROADMAP — UNCOMMITTED
Authority: Existing BBMA Core, approved contracts/blueprint and live repository state
Rule: Every task must identify its roadmap ID before execution.

## Mandatory flow
A Source & Evidence Finalisation -> B Architecture & Gap Confirmation -> C Controlled Core Implementation -> D Technical Validation -> E Operational Readiness -> F Release Candidate Gate -> G Controlled Deployment.

No later phase may be treated as complete when its predecessor has unresolved blocking evidence.

## A. Source & Evidence Finalisation
Owner: Terra Medium for mechanical work; Astra High for content adjudication.

A1. Finalize corrected subtitle.
A2. QA timestamp, file integrity and UNCLEAR register.
A3. BBMA video evidence extraction.
A4. Core reconciliation: MATCH / PARTIAL / UNCLEAR.
A5. Update provenance, conflict/HOLD and gap register.

### A4 small Astra subtasks
A4.0 Read-only preflight and evidence index.
A4.1 Adjudicate root unresolved windows: d00Pm6BRL_8, dZ6tmEwlrfA, qSoxRNSVwe4 and QzGMRtkHwUw.
A4.2 Adjudicate sZ_ib-DyOqQ windows: 122.00–126.00 and 161.00–170.00.
A4.3 Adjudicate VMDF27J0MxU windows: 57.00–74.00 and 108.00–115.00.
A4.4 Adjudicate W004 duplicate: GROUP3/0XoRUraiyLk/W004.
A4.5 Consolidate A4 decisions and unresolved limitations.
A4.6 Astra handoff review; XHigh only for unresolved source conflict.

A4 checkpoint rule:
Save a new checkpoint after A4.0, A4.1, A4.2, A4.3, A4.4 and A4.5.## B. Architecture & Gap Confirmation
Owner: Astra High; XHigh only for architecture or production-safety conflict.

B1. Full preflight live repository.
B1.1 Confirm repository, branch, working tree and uncommitted changes.
B1.2 Read README, CURRENT, MASTER_QUEUE and SOURCE_INDEX.
B1.3 Identify canonical EA, contracts, blueprint and latest evidence.
B1.4 Record exact baseline before diagnosis.

B2. Strategy-Core gap audit M01–M27 + M12N.
B2.1 Audit M01–M05.
B2.2 Audit M06–M10.
B2.3 Audit M11–M16 including M12N.
B2.4 Audit M17–M22.
B2.5 Audit M23–M27.
B2.6 Cross-module lifecycle and isolation review.

B3. Confirm genuine Core/code mismatch.
B3.1 Separate code mismatch from evidence, telemetry and test gaps.
B3.2 Mark already-fixed and duplicate/non-actionable items.
B3.3 Do not implement fixes in B phase.

B4. Reconcile blueprint, contracts and lifecycle ownership.
B4.1 Signal creation, persistence, confirmation and emission.
B4.2 Execution request, expiry, reset and duplicate prevention.
B4.3 JourneyID, DecisionID, restart persistence and pair isolation.
B4.4 F7 context-to-outcome ownership.

B5. Prioritise confirmed gaps only.
B5.1 P0: duplicate trade, leakage, wrong lifecycle, state corruption.
B5.2 P1: confirmed Core behaviour, chronology, expiry or identity defect.
B5.3 P2: telemetry, reporting or test coverage gap.

B checkpoint rule:
Save a new checkpoint after each module group and before any C-phase implementation.

## C. Controlled Core Implementation
Owner: Astra High; bounded change only after B confirmation.

C1. Scoped fix per confirmed module.
C2. Preserve signal lifecycle.
C3. Prevent duplicate logic and cross-pair state leakage.
C4. Add build identity, traceability and queue evidence only where approved.
C5. Review diff and preserve unrelated user changes.

No C task may add unapproved rules, filters, entry, exit, SL/TP or lifecycle behaviour.## D. Technical Validation
Owner: Terra Medium for mechanical checks; Astra High for unresolved diagnosis.

D1. Strict MQL4 compile.
D2. Static and cross-module regression audit.
D3. Strategy Tester scenario validation.
D4. Closed-candle chronology plus state/log/order validation.
D5. F7 execution-lifecycle runtime closure.
D6. Record actual command, output and PASS/FAIL/NOT RUN.
D7. Never claim runtime verified without genuine runtime evidence.

## E. Operational Readiness
Owner: Terra Medium.

E1. Risk/MM, execution and dashboard separation audit.
E2. Demo forward validation.
E3. Genuine entry, exit and telemetry outcomes.
E4. Resolve confirmed runtime defects only.
E5. Preserve HOLD/UNCLEAR items outside execution.

## F. Release Candidate Gate
Owner: Astra XHigh.

F1. Compile clean.
F2. Regression clean.
F3. Tester and runtime evidence sufficient.
F4. HOLD/UNCLEAR excluded from execution.
F5. Version, changelog and release evidence complete.
F6. No release-ready claim without all gate evidence.

## G. Controlled Deployment
Owner: Terra Medium; Astra High for critical defect diagnosis.

G1. User review and explicit approval.
G2. Deploy to chosen demo/live environment.
G3. Post-deployment runtime watch.
G4. No automatic deployment.

## Model routing
- Luna Medium: mechanical/read-only enumeration, metadata, path, counts, manifests and checkpoint saving.
- Terra Medium: routine QA, compile/static/test execution and operational evidence.
- Astra High: A4 adjudication, B2–B5 diagnosis and bounded C implementation.
- Astra XHigh: unresolved source conflict, release gate or production-safety decision only.

## Persistence and quota protection
- Each task must name its roadmap ID.
- Long work must be split into independently completable subtasks.
- Save a checkpoint at the start, after each subtask and before quota-sensitive work.
- Use new checkpoint files; never overwrite historical reports.
- If interrupted, record last completed ID and resume from the next ID.
- No automatic commit, merge, PR, deployment or project-history update.
## Explicit model-level labels

Every task prompt must include exactly one primary model level.

| Roadmap area | Model level | Usage |
|---|---|---|
| A1–A3 mechanical source/evidence work | Luna Medium | Enumeration, QA, metadata, path, counts and checkpoint files. |
| A4 content reconciliation | Astra High | Evidence-based MATCH/PARTIAL/UNCLEAR adjudication. |
| A4 source conflict escalation | Astra XHigh | Only when source-to-source conflict cannot be resolved clearly. |
| A5 provenance/conflict/HOLD/gap update | Astra High | Consolidate approved A4 results; no silent conflict resolution. |
| B1 repository preflight | Astra High | Live branch, working tree, canonical source and evidence baseline. |
| B2 module gap audit | Astra High | M01–M27 + M12N diagnosis in small module groups. |
| B3 genuine mismatch confirmation | Astra High | Separate code mismatch from evidence/telemetry/test gaps. |
| B4 lifecycle/contract/blueprint reconciliation | Astra High | Ownership, chronology, persistence and isolation diagnosis. |
| B5 confirmed-gap prioritisation | Astra High | P0/P1/P2 prioritisation only for proven gaps. |
| B-phase architecture safety escalation | Astra XHigh | Only for unresolved architecture or production-safety conflict. |
| C controlled implementation | Astra High | One bounded confirmed fix per task; review diff after each fix. |
| D1–D5 routine validation | Terra Medium | Compile, static checks, tester and operational evidence. |
| D unresolved diagnosis | Astra High | Only when validation failure cause is unclear. |
| E operational readiness | Terra Medium | Risk/MM separation, demo evidence and telemetry collection. |
| F release candidate gate | Astra XHigh | Final release evidence and gate decision. |
| G deployment execution | Terra Medium | Only after explicit user approval; critical defect diagnosis uses Astra High. |

## Prompt header requirement

Every new prompt must start with:
- ROADMAP ID: exact ID such as A4.1, A5.1 or B2.1.
- MODEL LEVEL: Luna Medium / Terra Medium / Astra High / Astra XHigh.
- TASK TYPE: MECHANICAL, DIAGNOSIS, IMPLEMENTATION, VALIDATION or GATE.
- CHECKPOINT OUTPUT: exact new file path before work begins.

## Current active step

ROADMAP ID: A4.1
MODEL LEVEL: Astra High
TASK TYPE: DIAGNOSIS / CONTENT ADJUDICATION
STATUS: PENDING — not started
PREPARATION STATUS: Luna mechanical evidence packaging complete

## Mandatory execution rule

Do not send a combined large Astra prompt when subtasks are separable. Complete and save each A4 checkpoint before starting the next one.