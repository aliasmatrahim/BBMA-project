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

The Master Blueprint has already advanced into implementation. The current development priority is therefore to keep **Blueprint → implementation → compile/static tests → runtime/backtest evidence** aligned while closing only confirmed implementation, integration, provenance, lifecycle and validation gaps.

The active implementation owner is `d1-owner-dev`. Strategy/source references must be resolved through `docs/references/SOURCE_INDEX.md`; current code/status/queue/runtime claims must be resolved from live GitHub state rather than historical chat or stale branch assumptions.

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

The Master Blueprint remains the authoritative architecture/behaviour specification and must stay aligned with implementation.

When Blueprint or architecture work is required:

1. Audit architecture first.
2. Audit module responsibility and ownership.
3. Audit producer/consumer relationships.
4. Audit signal lifecycle and state transitions.
5. Audit temporal ordering and closed-candle assumptions.
6. Audit dependencies and declaration requirements.
7. Audit risk and trade lifecycle ownership.
8. Find contradictions, missing logic and redundant responsibilities.
9. Fix the specification deliberately before or together with the implementation correction when the specification is actually wrong.
10. Repeat the audit until no material unresolved issue remains in scope.

Do not reopen or redesign already-locked architecture merely because implementation/testing has moved into a later phase. Reopen a Blueprint decision only when stronger evidence or a confirmed implementation/architecture contradiction requires it.

---

## 5. Review Rules

When reviewing an existing module, Blueprint revision or implementation:

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

For every important piece of data or state, the Blueprint/contract should make clear:

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

Historical project progression remains:

**Master Blueprint Draft → Architecture Audit → Logic & State Audit → Dependency/Cross-Module Audit → Master Blueprint Locked → EA Implementation → Compile & Static Debugging → Functional Testing → Backtesting/Validation → Production Candidate**

The project is now in the **implementation / integration / validation** portion of that progression. Therefore:

- do not treat Blueprint drafting as the current default workstream;
- current fixes must start from the active implementation owner and current contracts/evidence;
- isolated branches/PRs are used for confirmed fixes, audits and validation packages;
- native MetaEditor compile/static tests are required where source changes occur;
- runtime/backtest/demo evidence remains a separate acceptance layer and must not be inferred from static correctness;
- production readiness is not claimed while required runtime/provenance/acceptance gates remain open.

---

## 9. Source-Code Organisation

The canonical active EA implementation path is:

`blueprint/source/BBMA_EA.mq4`

The M01–M27 architecture remains clearly sectioned inside the implementation. Do not split the project into 27 `.mqh` files merely for appearance. Physical modularisation should happen only when it improves maintainability and does not create unnecessary dependency complexity.

Historical filenames or copies are evidence/provenance only unless the active branch/router explicitly designates them as current implementation authority.

---

## 10. GitHub Workflow

### `main`
Reserved for approved/stable project state.

### `d1-owner-dev`
Active implementation owner branch. Current canonical implementation, governance routing and accepted integration state are resolved from this branch unless a newer explicit owner decision changes ownership.

### Scoped branches / Draft PRs
Confirmed fixes, audits, runtime tooling and evidence packages should use a scoped branch/PR when isolation is required. A scoped branch does not become canonical merely because it contains newer commits.

### `blueprint-dev` and historical branches
Historical Blueprint/development branches remain provenance/reference unless an explicit current decision reactivates them. Do not infer current ownership from an old branch name.

Rules:

- Development changes must be traceable through commits/PRs.
- Resolve the current owner branch before editing.
- Check for newer open PRs, scoped branches and explicit supersession decisions when freshness matters.
- Do not overwrite locked Blueprint or unrelated work casually.
- Keep experimental development away from stable project state.
- Do not merge source/runtime changes until their required validation gates actually pass.

### Autonomous merge policy

The user has granted **standing authorization** for validated BBMA merges. A separate per-PR confirmation is not required when the assistant determines that all scope-required gates have passed and no genuine user gate remains.

Autonomous merge is allowed for documentation/governance/tooling/tests/audit/evidence/status work and for EA/source/behaviour-bearing fixes when **all** of the following are true:

- the exact PR head SHA has passed every validation gate required for its scope;
- the intended target/current owner branch has been resolved from live GitHub state;
- any Strategy-Core or behaviour-bearing change implements an already accepted source rule, contract or explicit project decision rather than inventing/adjudicating new semantics;
- native compile, static, targeted regression, cross-module and runtime evidence required by the scope are complete and attributable to the exact candidate;
- no required CI/check is pending or failing;
- no unresolved review blocker, `HOLD`, `UNCERTAIN`, `UNRESOLVED`, source conflict or material classification ambiguity remains;
- the merge does not silently broaden scope, change unrelated authority, or bypass a failed/unverified exit criterion.

A genuine user gate still requires consultation before proceeding when any of the following applies:

- Strategy-Core/source semantics are genuinely new, conflicting, ambiguous or not already authorized by accepted evidence/decision;
- a required compile/static/regression/runtime/CI gate is unavailable, failed, or cannot be attributed to the exact candidate;
- force-update, force-push, branch deletion, destructive overwrite or another irreversible/destructive Git action is required;
- production/trading activation, primary MT4 restart, live-account action, credentials, physical verification or another operationally irreversible action is required;
- the requested merge would knowingly carry unresolved scope drift or an authority change outside the accepted contract/decision.

The standing authorization removes the repeated **merge-confirmation** gate; it does **not** remove Strategy-Core adjudication, validation, runtime, safety or provenance gates. After every autonomous merge, verify that the intended owner branch contains the exact merged change and record the PR/commit result.


---

## 11. Tool Responsibilities

### GitHub — Source of Truth
Use for authoritative Blueprint/code versions, branches, commits, change history, contracts, current state, Issues/PRs and implementation work.

### Notion — Supporting Knowledge Base
May be used for architecture explanations, design decisions, meeting/research notes and human-readable project documentation. Notion must not silently become a conflicting source of truth.

### Linear — Issue / Task Tracking
May be used for concrete bugs, architectural findings, required fixes and development tasks. Close issues only after the relevant fix has been verified.

GitHub remains authoritative if information across tools conflicts. `BBMA_MASTER_INSTRUCTIONS.md` governs tool orchestration but does not replace this architecture/strategy governance.

---

## 12. Change-Control Principles

Before making a significant architectural or behavioural change, determine:

1. What problem is being fixed?
2. Which module/layer owns the problem?
3. Which downstream/upstream modules are affected?
4. Does the change alter BBMA Core behaviour?
5. Does it introduce duplicate responsibility?
6. Does it violate the processing-clock or closed-candle model?
7. Does the Blueprint/contract need updating before code changes?

Avoid uncontrolled feature creep.

---

## 13. Definition of Blueprint Ready

The Master Blueprint is ready/locked only when, within the reviewed scope:

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

Production coding proceeds from the locked/accepted Blueprint and active contracts.

Implementation must conform to them. If coding/testing exposes a genuine Blueprint flaw, fix and review the Blueprint deliberately rather than silently changing architecture only in code.

The final goal is one coherent system where **evidence → Core → Blueprint/contracts → implementation → tests/runtime** describe compatible behaviour.

---

## 15. Project Priority

**Correctness, source fidelity, architectural consistency and attributable evidence take priority over speed, feature count and code size.**

The immediate goal is now:

> Close confirmed implementation/runtime/provenance gaps on the active owner lineage, keep M01–M27 and M12N authority boundaries intact, obtain required 0E0W/static/runtime/backtest evidence, reconcile source research without inventing new BBMA rules, and progress toward a fully attributable production candidate.

Do not add a new rule merely to improve historical profitability or fill an evidence gap. Unresolved Strategy-Core evidence remains `HOLD/UNRESOLVED` until properly reconciled.

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

### 17.1 Required retrieval order
Always inspect the authoritative project sources in this order:

1. `docs/references/SOURCE_INDEX.md` — source map, hierarchy and conflict policy.
2. `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md` — active consolidated developer-facing Core specification.
3. `docs/references/video/oma_ally_finale/BBMA_FINALE_MASTER_RULE_INDEX.md` — reconciled Finale V01–V07 evidence.
4. Relevant `docs/references/video/oma_ally_finale/V01` … `V07` `extracted_rules.md` and/or `summary.md` when the rule requires timestamped or episode-level evidence.
5. `docs/references/BBMA_OMA_ALLY_RULE_INDEX.md` and the recorded primary/secondary PDF evidence.
6. Relevant BBMA/Oma Ally forum evidence when the issue requires clarification, corroboration, historical teaching context or resolution beyond the PDF/Finale layer.
7. Relevant source-conflict, implementation-gap and source-contract files.
8. Current Master Blueprint / active EA implementation only **after** the Strategy-Core evidence has been established.

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
Apply the source precedence and conflict policy defined in `docs/references/SOURCE_INDEX.md`. Finale clarification must not silently overwrite an established PDF rule, and implementation behaviour must never outrank clearly supported source evidence.

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

The mandatory evidence group is:

1. **BBMA PDF evidence** — primary operational PDF plus secondary corroborating PDF where relevant;
2. **BBMA Finale V01–V07** — Master Rule Index plus timestamped episode-level extracted rules/summary where relevant;
3. **BBMA/Oma Ally forum evidence** — relevant thread/post evidence used as corroboration/clarification, with provenance retained;
4. **Canonical Core consolidation** — `BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`, which contains only accepted/reconciled rules.

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

> Retrieve canonical sources → cross-check PDF + Finale + relevant forum + Core consolidation → establish accepted rule/evidence → compare Blueprint/code → classify mismatch → fix only if authorized by evidence → cross-module/purity verification → preserve traceability.

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
- `BBMA_FINALE_MASTER_RULE_INDEX.md` and relevant V01–V07 extracted evidence;
- original/corroborating PDF evidence;
- source-conflict and implementation-gap registers;
- registered forum provenance/evidence.

This layer answers: **What is the accepted BBMA rule, evidence, provenance, conflict status and project governance?**

#### B. Live GitHub implementation / state layer
Always retrieve the current repository state when the task depends on implementation or project status, including where relevant:

- active branch and latest repository state;
- `blueprint/CURRENT.md`;
- `blueprint/MASTER_QUEUE.md`;
- relevant module/source contracts;
- relevant decisions/audits/verification records;
- active `blueprint/source/BBMA_EA.mq4`;
- current commits, open/scoped PRs, compile/runtime evidence and changed files.

This layer answers: **What does the project currently implement, what is active now, what remains pending, and what changed most recently?**

### 18.2 Mandatory preflight sequence
Before reaching a material conclusion or making a project change:

1. Retrieve the current `PROJECT_INSTRUCTIONS.md` from GitHub.
2. Retrieve `docs/references/SOURCE_INDEX.md` and use it as the source router.
3. Identify the task class, affected BBMA concept(s), owning module(s), and whether the task can affect Strategy-Core semantics.
4. If Strategy-Core semantics may be affected, retrieve the relevant static evidence group required by Section 17 before inspecting code as authority.
5. Retrieve the live GitHub state relevant to the task: `CURRENT.md`, `MASTER_QUEUE.md`, owning contract(s), current EA source, relevant recent PRs/commits/comments, and relevant audit/decision records.
6. Compare the layers in this order:

   **Original Evidence → Canonical Strategy Core → Contract / Blueprint → Current Code → Runtime / Test Evidence**

7. Classify any mismatch before fixing it. Valid classifications include:
   - source clarification;
   - unresolved source conflict / `HOLD`;
   - Blueprint/specification defect;
   - implementation defect;
   - runtime/integration defect;
   - observability/documentation defect;
   - no defect / already compliant.
8. Apply only the smallest evidence-authorized fix owned by the correct module/layer.
9. Re-check affected upstream/downstream modules and perform Strategy-Core purity regression when strategy behaviour is touched.
10. For EA source changes, apply Section 16 build identification and obtain the required compile/runtime evidence.
11. Commit the verified change to GitHub and update `CURRENT.md`, `MASTER_QUEUE.md`, audit/gap/decision records, or other tracking artifacts **only when their state actually changed**.

### 18.3 Freshness rule
Uploaded/static copies of live project-state files, code, queue records or runtime records must **never** be assumed current merely because they exist in a knowledge library or previous chat.

For current status, active queue, source code, contracts, build identity, commit state and runtime evidence:

> **GitHub live state wins.**

The static Project Sources are a stable evidence/knowledge layer, not a substitute for checking the current repository when freshness matters.

### 18.4 Comprehensive does not mean read-everything
"Use the sources comprehensively" does **not** mean reading every source file on every task.

The required behaviour is:

- always start from `SOURCE_INDEX.md`;
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

> GitHub governance + source index preflight → relevant static evidence retrieval → live GitHub state/contracts/code retrieval → Evidence → Core → Contract → Code → Runtime comparison → classify → smallest authorized fix → cross-module/purity verification → compile/runtime evidence where required → commit/update live project state.

---

## 19. Mandatory Live-Status Authority Protocol

This protocol is mandatory whenever the user/task asks for `latest`, `current`, `next`, `status`, active test/workstream, runtime step, release state, branch ownership, or asks to continue/resume prior work.

### 19.1 Resolution sequence
Resolve status in this order before answering or scheduling the next step:

1. Read the current repository/governance branch map and resolve the active owner branch.
2. Read `blueprint/CURRENT.md` and `blueprint/MASTER_QUEUE.md` from that resolved owner when those files exist and are current.
3. Inspect recent open/scoped PRs and recent repository commits, sorted by update/commit time.
4. Inspect relevant Issue/PR comments for explicit `supersede`, `stop`, `replace`, `defer`, `resume`, `activate`, `no merge`, or equivalent owner sequencing decisions.
5. Check exact runtime/test evidence when the status claim depends on execution rather than planning.

Do not stop at the first authoritative-looking historical record.

### 19.2 Four facts must stay separate
For test/runtime status, distinguish explicitly when relevant:

- **latest project/test-plan update**;
- **latest actual test attempt**;
- **latest valid PASS/accepted evidence**;
- **next required test/action**.

These may point to different timestamps/builds/branches. Never collapse them into one vague `latest` claim.

### 19.3 Attribution requirement
Before calling a code/test/runtime item `latest/current`, identify enough of the following to make the claim reproducible where available:

- owner/scoped branch;
- head SHA;
- EA build/version/source identity;
- relevant PR/Issue;
- evidence timestamp/run timestamp.

A newer explicit owner sequencing decision supersedes older scheduling text without rewriting or invalidating historical PASS/FAIL evidence.

### 19.4 Conflict handling
If current records materially conflict and cannot be reconciled from repository evidence:

`STATUS CONFLICT / VERIFICATION REQUIRED`

Do not guess from chat memory, an older CURRENT/queue snapshot, or the first search result.

Chat/project memory is navigation only, never live-status authority.

### 19.5 Concise status answer template
When the user asks for confirmation/status, expose the minimum useful authority chain:

`CURRENT: <active workstream/build/branch> | LAST ATTEMPT: <result/time> | LAST VALID PASS: <evidence or none> | NEXT: <required action> | AUTHORITY: <branch/PR/SHA>`

Use plain language when the user does not need developer detail, but do not omit a material uncertainty or pending verification.

---

## 20. Current Implementation / Runtime Sequencing Boundary

The governance update itself does not promote any pending strategy/runtime work. Current substantive work remains governed by its own Issue/PR/evidence gates.

In particular:

- NMJE remains read-only unless a separately approved execution policy exists;
- F7/C044 infrastructure fixes require unique build identity, static/model proof and native 0E0W before source promotion;
- C10 runtime closure requires exact attributable Build 4.81 evidence and cannot be substituted by a different build/test mode;
- source research/transcription may clarify evidence but cannot directly create a production rule without Section 17 reconciliation;
- no primary MT4 restart, trading-authority change or production activation is implied by documentation/governance maintenance.
