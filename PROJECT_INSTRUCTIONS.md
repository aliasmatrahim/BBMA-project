# BBMA Professional EA — Project Instructions

**Status:** ACTIVE PROJECT GOVERNANCE  
**Platform:** MetaTrader 4 / MQL4  
**Architecture:** M01–M27  
**Logical architecture overlay:** M12N — Nested MTF Journey Engine, positioned between M12 and M13 without consuming a numeric module slot or renumbering M13–M27
**Primary Source of Truth:** GitHub

---

## 1. Project Objective

Develop a production-grade **BBMA Professional EA** for MetaTrader 4 using the agreed M01–M27 architecture.

The trading logic must remain faithful to **BBMA Core / Oma Ally methodology**. Supporting modules may manage data, validation, risk, execution, lifecycle, UI and integration, but must not silently alter the BBMA trading methodology.

The project is currently in active **EA implementation, compile/runtime validation and evidence-closure** work against the approved Blueprint/contracts. The Blueprint remains binding; if implementation exposes a genuine architecture defect, reconcile it deliberately rather than silently changing behaviour in code.

---

## 2. Non-Negotiable Trading Rules

- Preserve BBMA Core logic unless an explicit project decision approves a change.
- Do not introduce RSI, MACD, Stochastic or ADX.
- Do not introduce news filters.
- Do not introduce session filters.
- Do not introduce volatility or correlation filters as trading-signal logic.
- EA is intended for 24/5 operation subject to broker/market availability and project risk controls.
- No trailing stop unless explicitly approved by a later project decision.
- No TP2 or TP3 unless explicitly approved.
- SL and TP logic must originate from the approved BBMA architecture/rules.
- Supporting modules must not create hidden alternative trading strategies.

---

## 3. Processing Architecture

- M15 is the **sole processing clock** for the current architecture unless the Master Blueprint explicitly defines an approved exception.
- Signal processing must use **closed candles** where specified by the architecture.
- D1, H4, H1 and M15 retain their defined BBMA roles.
- Canonical logical signal flow includes `M06–M12 owner updates -> M12N NMJE read-only context/lineage -> M13 collector -> M14 validator -> M15 final authority -> M16 revalidation`.
- M12N is a logical sub-module only: M13 remains Module 13, M27 remains Module 27/orchestrator, and the project remains an M01–M27 numbered architecture.
- M12N/NMJE may observe or carry diagnostic/shadow lineage only under its active contract; it may not create, reject, rank or execute a trade unless a future strategy-changing gate is separately evidenced and explicitly approved.
- A module must not independently introduce an alternative processing clock.
- Timing assumptions must be explicit and consistent across producer and consumer modules.

---

## 4. Master Blueprint Governance

The Master Blueprint is the authoritative architecture and behaviour specification. Its locked/approved contracts continue to govern implementation and runtime work.

During Blueprint development or deliberate Blueprint revision:

1. Audit architecture first.
2. Audit module responsibility and ownership.
3. Audit producer/consumer relationships.
4. Audit signal lifecycle and state transitions.
5. Audit temporal ordering and closed-candle assumptions.
6. Audit dependencies and declaration requirements.
7. Audit risk and trade lifecycle ownership.
8. Find contradictions, missing logic and redundant responsibilities.
9. Fix the specification before implementation behaviour is changed.
10. Repeat the audit until no material unresolved issue remains.

Do not declare the Master Blueprint LOCKED merely because all 27 modules exist. It may be locked only after cross-module consistency has been reviewed. After lock, material architecture changes still require deliberate review and traceability.

---

## 5. Review Rules

When reviewing an existing module or Blueprint revision:

- Do **not** repeatedly explain items already verified as correct.
- Focus on new bugs, inconsistencies, missing logic, architectural flaws, dependency problems, ambiguous ownership and fixes that are actually required.
- Do not add features merely to make the architecture appear more sophisticated.
- Do not change confirmed BBMA rules without explicit approval.
- Distinguish clearly between a required fix and an optional improvement.
- After a fix, re-check its effect on dependent modules.
- If no new issue remains, state clearly that no further fix is required for the reviewed scope.

---

## 6. Module Ownership Rules

Each M01–M27 module must have a clear responsibility.

For every important piece of data or state, the Blueprint should make clear:

- who creates it;
- who owns it;
- who may modify it;
- who consumes it;
- when it becomes valid;
- when it expires or is invalidated.

Avoid:

- duplicate responsibility;
- circular dependencies;
- multiple modules independently making the same trading decision;
- hidden state mutation;
- candidate signals being treated as confirmed signals without an explicit transition;
- execution modules redefining detector logic;
- lifecycle modules silently recreating trading signals.

---

## 7. Signal and Trade Separation

Keep these concepts separate unless the Master Blueprint explicitly defines their transition:

**Detection → Candidate → Confirmation → Combination/Selection → Validation → Risk Approval → Execution → Position/Trade Lifecycle**

A detector should not execute trades. A collector should not reinterpret signal direction unless that is its explicit responsibility. A risk module should not invent entries. An execution module should execute approved decisions rather than recreate upstream strategy logic.

---

## 8. Development Phases

The project lifecycle follows this sequence:

**Master Blueprint Draft**  
↓  
**Architecture Audit**  
↓  
**Logic & State Audit**  
↓  
**Dependency / Cross-Module Audit**  
↓  
**MASTER BLUEPRINT LOCKED**  
↓  
**EA Implementation**  
↓  
**Compile & Static Debugging**  
↓  
**Functional / Runtime Testing**  
↓  
**Backtesting / Validation**  
↓  
**Production Candidate**

The current project has progressed beyond the initial Blueprint-lock milestone into implementation and validation. This lifecycle remains the governance sequence; it is not an instruction to return implementation work to an obsolete pre-implementation branch or phase.

---

## 9. Source-Code Organisation

The active EA implementation is maintained as one clearly structured master source file unless an approved architecture decision changes that organisation:

`blueprint/source/BBMA_EA.mq4`

Resolve the branch that owns this source from the current repository governance/branch map before auditing or changing code.

The architecture may still contain M01–M27 sections inside that file.

Do not split the project into 27 `.mqh` files merely for appearance. Physical modularisation should happen only when it improves maintainability and does not create unnecessary dependency complexity.

---

## 10. GitHub Workflow

Do **not** assume the repository default branch is the active EA implementation branch. Resolve branch ownership from the current repository `README.md`, `blueprint/CURRENT.md` and repository governance before implementation/status work.

Current branch map at this governance revision:

### `main`
Default branch for repository governance, dispatcher/tooling and GitHub Actions integration.

### `d1-owner-dev`
Active implementation/source branch containing the EA source, detailed contracts, decisions and runtime evidence.

Current EA source:

`d1-owner-dev:blueprint/source/BBMA_EA.mq4`

Branch names and ownership may evolve. When the live repository branch map changes, the live governance/current-state records take precedence over historical branch names in older notes or chat history.

Rules:

- Use a structured Issue for confirmed defects or intentional architecture changes when applicable.
- Create a scoped branch from the branch that owns the target.
- Make the smallest correct change and preserve unaffected architecture.
- Use a Draft PR for reviewable development changes when applicable.
- Run the existing specialized compile/static/runtime checks that own the affected invariants; do not create redundant generic checks when a canonical check already exists.
- Review architecture and regression impact before integration.
- Merge only when required evidence is green and material findings are resolved.
- Keep Issue, PR, decisions/contracts and release evidence linked so changes remain traceable.
- Do not overwrite a LOCKED Blueprint casually; significant post-lock changes require deliberate review.

---

## 11. Tool Responsibilities

### GitHub — Source of Truth
Use for authoritative Blueprint/code versions, branches, commits, change history and implementation work.

### Notion — Supporting Knowledge Base
May be used for architecture explanations, design decisions, meeting/research notes and human-readable project documentation. Notion must not silently become a conflicting source of truth.

### Linear — Issue / Task Tracking
May be used for concrete bugs, architectural findings, required fixes and development tasks. Close issues only after the relevant fix has been verified.

GitHub remains authoritative if information across tools conflicts.

---

## 12. Change-Control Principles

Before making a significant architectural change, determine:

1. What problem is being fixed?
2. Which module owns the problem?
3. Which downstream/upstream modules are affected?
4. Does the change alter BBMA Core behaviour?
5. Does it introduce duplicate responsibility?
6. Does it violate the processing-clock or closed-candle model?
7. Does the Blueprint need updating before code changes?

Avoid uncontrolled feature creep.

---

## 13. Definition of Blueprint Ready

The Master Blueprint is ready to lock only when, within the reviewed scope:

- M01–M27 responsibilities are defined;
- module interfaces and dependencies are coherent;
- important data ownership is unambiguous;
- signal states and transitions are coherent;
- timing assumptions are coherent;
- risk and execution responsibilities do not conflict;
- no known material architectural contradiction remains;
- no known required module is missing;
- no unresolved critical finding remains.

"Complete" means internally consistent and implementable, not merely long or detailed.

---

## 14. Definition of Implementation Ready

Production coding begins from an approved/locked Master Blueprint.

The project is now in active implementation and validation. Implementation must continue to conform to the Blueprint and active contracts. If coding or runtime evidence exposes a genuine Blueprint flaw, fix and review the Blueprint deliberately rather than silently changing architecture only in code.

The final goal is one coherent system where **Blueprint → implementation → tests** describe the same behaviour.

---

## 15. Project Priority

**Correctness and architectural consistency take priority over speed, feature count and code size.**

The immediate goal is therefore:

> Complete the current EA implementation and close compile, runtime, Strategy-Core purity, regression and release-evidence gaps against the approved M01–M27 + M12N architecture without introducing silent strategy or ownership drift.

---

## 16. Mandatory EA Patch / Build Identification

This rule is mandatory for every future EA source-code change, patch, fix, diagnostic build, cleanup, or functional modification.

- Every code change that produces a new EA build MUST update a visible identifier in the EA **About/header metadata**.
- The identifier MUST contain a clear **patch/build name or patch/build number** that uniquely distinguishes the build being compiled or tested.
- The identifier must be updated in the same code change; do not postpone it to a later patch.
- Diagnostic-only and trace-only builds are included in this requirement.
- The identifier must make it possible to match the running/tested EA to the corresponding **source file, compile result, runtime log, and GitHub commit/PR**.
- Never reuse an old patch/build identifier for code that has changed.
- Documentation-only changes that do not alter the EA source do not require a new EA build identifier.
- Before declaring a code patch complete, verify that the About/header identifier matches that patch/build.
- **MANDATORY HEADER FORMAT:** the visible `Version ... - PATCH/BUILD NAME` line in the EA source header MUST be **left-aligned**, immediately after the `//| ` prefix. Do not center it and do not add leading alignment spaces before `Version`.
- Keep the surrounding comment box tidy by padding only **after** the patch/build text when padding is desired.
- Every future source patch must verify both the identifier content **and its left alignment** before the patch is declared complete.

**Required header example:**

`//| Version 4.5.1 - P3-UI-01 Input Panel Cleanup                      |`

**Required development check:**

> EA source changed → About/header patch/build identifier updated + left-aligned → compile verification → runtime/test evidence → GitHub traceability.

---

## 17. Mandatory BBMA Source Retrieval Protocol

This protocol is **MANDATORY** before any Strategy-Core interpretation, detector/entry/exit change, Blueprint strategy repair, source-compliance claim, or conclusion that a BBMA rule/source is missing.

### 17.1 Dynamic source-router rule
Always begin with:

1. `docs/references/SOURCE_INDEX.md` — the **dynamic source router**, hierarchy and conflict policy.
2. Follow the **current retrieval sequence recorded inside `SOURCE_INDEX.md`**. Do not maintain a competing hard-coded hierarchy in this file, chat memory, old audits or assistant instructions.
3. Retrieve `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md` as the active developer-facing accepted Core consolidation, then all materially relevant evidence/provenance layers routed by `SOURCE_INDEX.md` for the rule under review.
4. Check the relevant conflict/HOLD and implementation-gap records before encoding or changing deterministic Strategy-Core behaviour.
5. Inspect relevant module/source contracts and the active Blueprint/EA implementation only **after** Strategy-Core semantics have been established.

If `SOURCE_INDEX.md` registers or reconciles an additional source layer — for example the Tier-B BBMA Home Course Workbook evidence and its explicit reconciliation decisions — include it whenever the current router and task relevance require it. A historical list in another document must not suppress a newer registered evidence layer.

### 17.2 No search-empty inference
A GitHub code-search result of zero matches is **NOT evidence that a project source does not exist**.

Before declaring any expected BBMA source, Finale episode, rule index, contract or evidence file missing:

- inspect `SOURCE_INDEX.md`;
- inspect the known canonical directory/path;
- inspect the repository tree/directory listing when necessary;
- only then report a genuinely missing artifact.

Search is a discovery aid, not the authority for file existence.

### 17.3 Strategy-Core compliance gate
Before modifying strategy behaviour, explicitly determine:

- which accepted Core rule governs the behaviour;
- which source evidence supports it;
- whether the proposed change is `KEEP`, `CLARIFY`, an implementation-gap fix, or a genuine Core change;
- whether any conflict/HOLD item exists;
- whether the change would silently reinterpret Oma Ally/BBMA methodology.

If evidence is unresolved or marked `HOLD`, do not invent deterministic trading logic. Preserve the stricter/current accepted contract until explicit resolution.

### 17.4 Source versus implementation separation
Never treat current code behaviour as proof of the BBMA rule. The evidence hierarchy establishes Strategy-Core semantics; Blueprint/code is audited **against** that semantics.

A mismatch must be classified as one of:

- source clarification;
- Blueprint/specification defect;
- implementation defect;
- unresolved source conflict.

Do not silently rewrite the source interpretation merely to fit existing code.

### 17.5 Mandatory audit trace
For material BBMA strategy reviews/fixes, retain enough traceability to identify:

> source rule → evidence/reference → Core contract → owning module(s) → Blueprint/code behaviour → finding/fix → verification.

This trace may live in the existing source contract, audit, gap register or commit documentation; avoid duplicate documents when an existing authoritative artifact already serves the purpose.

### 17.6 User re-verification must not be the control mechanism
The user must not be required to repeatedly remind the project that the EA must follow BBMA/Oma Ally rules. Source compliance is a standing project governance requirement and must be checked automatically whenever Strategy-Core behaviour is touched.

### 17.7 Conflict precedence
Apply the source precedence and conflict policy defined in `docs/references/SOURCE_INDEX.md`. Supplemental clarification must not silently overwrite a higher-precedence established rule, and implementation behaviour must never outrank clearly supported source evidence.

### 17.8 Mandatory uncertainty / gap / ambiguity hard gate
For **any** uncertainty, gap, contradiction, ambiguity, incomplete behaviour, questionable assumption, proposed improvement, lifecycle question, or unclear trading behaviour that could affect BBMA semantics, the developer/assistant MUST cross-check the BBMA source group **before** reaching a strategy conclusion or modifying code.

This hard gate applies to all BBMA-derived behaviour, including but not limited to:

- Extreme, MHV/MLV, eCSD/CSD, CSM/Momentum and Re-Entry;
- REM/RRE/REE and all combination semantics;
- signal validity, invalidation, supersession and expiry;
- cycle ownership, cycle restart/reversal and opposite Extreme;
- pending candidates and descendant invalidation;
- multi-timeframe ownership/alignment;
- entry authority and entry timing;
- SL, TP, TP Wajib and BBMA-derived exit/position-management behaviour;
- simultaneous/opposite signals and multiple/add-on entries;
- any behaviour claimed to originate from BBMA/Oma Ally methodology.

The mandatory evidence group is determined by the **current `SOURCE_INDEX.md` retrieval map and task relevance**. It normally includes the canonical Core consolidation, primary/secondary PDF evidence, relevant Finale V01–V07 evidence, relevant forum evidence when it can materially clarify the issue, and any explicitly registered/reconciled supplemental evidence layer such as the Tier-B Home Course Workbook when applicable.

Cross-check does not mean forcing all sources to agree. If they conflict or do not answer the issue deterministically, classify the item `HOLD/UNRESOLVED`, record the evidence gap, and **do not invent a BBMA trading rule**.

### 17.9 Minimum-source and reasoning discipline
- Do not rely on a single convenient source when the other canonical source groups can materially clarify the issue.
- Distinguish explicit source statements from logical implications and project inference.
- Inference may explain evidence but must not silently become a deterministic entry/exit/invalidation rule.
- Existing code, previous patch, previous assistant conclusion, backtest result or personal preference does not outrank source evidence.
- A previous project decision MUST be reopened when stronger source evidence proves or materially suggests it is wrong.
- Strategy fixes require a post-fix purity regression against the accepted Core so one correction does not introduce another deviation.
- When source evidence genuinely cannot resolve an execution choice, prefer fail-closed/conservative behaviour that does not create a new entry authority, and retain the uncertainty for explicit resolution.

**Required Strategy-Core development check:**

> Retrieve `SOURCE_INDEX.md` → follow its current routed evidence set → establish accepted rule/evidence → compare Contract/Blueprint → current Code → Runtime evidence → classify mismatch → fix only if authorized by evidence → cross-module/purity verification → preserve traceability.

---

## 18. Mandatory Source + GitHub Preflight

This preflight is **MANDATORY for every BBMA project task** that can change or evaluate architecture, strategy logic, source compliance, code behaviour, runtime behaviour, bug status, queue priority, or release readiness.

Its purpose is to force the project to use the **static evidence layer and the live GitHub layer together**, instead of relying on chat memory, one uploaded file, one code snapshot, or one repository search result.

### 18.1 Two-layer authority model
Use both layers deliberately:

#### A. Static evidence / knowledge layer
Use the curated Project Sources / source-reference set for stable evidence and governance, including where relevant:

- `PROJECT_INSTRUCTIONS.md`;
- `docs/references/SOURCE_INDEX.md`;
- `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`;
- evidence layers currently routed by `SOURCE_INDEX.md`, including relevant Finale V01–V07, original/corroborating PDFs, registered forum provenance/evidence and explicitly reconciled supplemental evidence such as the Tier-B Home Course Workbook when applicable;
- source-conflict and implementation-gap registers.

This layer answers: **What is the accepted BBMA rule, evidence, provenance, conflict status and project governance?**

#### B. Live GitHub implementation / state layer
Always retrieve the current repository state when the task depends on implementation or project status, including where relevant:

- current repository branch map / ownership and latest state;
- `blueprint/CURRENT.md`;
- `blueprint/MASTER_QUEUE.md`;
- relevant module/source contracts;
- relevant decisions/audits/verification records;
- active `blueprint/source/BBMA_EA.mq4` on the branch that currently owns implementation;
- current commits, compile/runtime evidence and changed files.

This layer answers: **What does the project currently implement, what is active now, what remains pending, and what changed most recently?**

### 18.2 Mandatory preflight sequence
Before reaching a material conclusion or making a project change:

1. Retrieve the current `PROJECT_INSTRUCTIONS.md` from GitHub.
2. Retrieve the current repository `README.md` / governance branch map and resolve which branch owns the target; do not assume `main` owns EA implementation.
3. Retrieve `docs/references/SOURCE_INDEX.md` and use it as the source router.
4. Identify the task class, affected BBMA concept(s), owning module(s), and whether the task can affect Strategy-Core semantics.
5. If Strategy-Core semantics may be affected, retrieve the relevant static evidence group required by Section 17 before inspecting code as authority.
6. Retrieve the live GitHub state relevant to the task: `CURRENT.md`, `MASTER_QUEUE.md`, owning contract(s), current EA source, and relevant audit/decision records.
7. Compare the layers in this order:

   **Original Evidence → Canonical Strategy Core → Contract / Blueprint → Current Code → Runtime / Test Evidence**

8. Classify any mismatch before fixing it. Valid classifications include:
   - source clarification;
   - unresolved source conflict / `HOLD`;
   - Blueprint/specification defect;
   - implementation defect;
   - runtime/integration defect;
   - observability/documentation defect;
   - no defect / already compliant.
9. Apply only the smallest evidence-authorized fix owned by the correct module/layer.
10. Re-check affected upstream/downstream modules and perform Strategy-Core purity regression when strategy behaviour is touched.
11. For EA source changes, apply Section 16 build identification and obtain the required compile/runtime evidence.
12. Commit the verified change to GitHub and update `CURRENT.md`, `MASTER_QUEUE.md`, audit/gap/decision records, or other tracking artifacts **only when their state actually changed**.

### 18.3 Freshness rule
Uploaded/static copies of live project-state files, code, queue records or runtime records must **never** be assumed current merely because they exist in a knowledge library or previous chat.

For current status, active queue, source code, contracts, build identity, commit state and runtime evidence:

> **GitHub live state wins.**

The static Project Sources are a stable evidence/knowledge layer, not a substitute for checking the current repository when freshness matters.

### 18.4 Comprehensive does not mean read-everything
"Use the sources comprehensively" does **not** mean reading every source file on every task.

The required behaviour is:

- always start from `SOURCE_INDEX.md`;
- follow its current routing/precedence policy;
- identify the relevant evidence groups and owning artifacts;
- retrieve **all materially relevant sources** for the task;
- do not omit a source group when it can materially change the conclusion;
- do not load unrelated sources merely to increase document count.

`SOURCE_INDEX.md` is the router; relevance determines depth.

### 18.5 No chat-memory authority
Conversation history, assistant memory, previous summaries, previous answers, and remembered code states are navigation aids only.

They may help locate the correct artifact, but they must not be treated as authoritative when the answer can be verified from the project sources or GitHub.

Before claiming that a bug is fixed, a rule is compliant, a phase is complete, or a queue item is next, verify the relevant current artifact.

### 18.6 Mandatory trace for material work
For any material audit/fix, the working conclusion should be reproducible through this chain:

> **source evidence → accepted Core rule → contract/owner → current code → runtime/test evidence → finding → fix → verification → GitHub state**

Do not create duplicate governance documents when an existing authoritative artifact can carry the trace.

### 18.7 Stop conditions
Do not proceed with a strategy/code change when:

- the relevant source evidence has not been retrieved;
- the current owning GitHub contract/source has not been checked;
- a material source conflict remains unresolved;
- the proposed fix has no clear owning module/layer;
- a previous snapshot is being used instead of current GitHub state where freshness matters.

In these cases, retrieve the missing evidence/state first or classify the item `HOLD/UNRESOLVED`.

**Required universal BBMA project check:**

> GitHub governance + branch ownership + source index preflight → relevant static evidence retrieval → live GitHub state/contracts/code retrieval → Evidence → Core → Contract → Code → Runtime comparison → classify → smallest authorized fix → cross-module/purity verification → compile/runtime evidence where required → commit/update live project state.
