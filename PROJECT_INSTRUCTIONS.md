# BBMA Professional EA — Project Instructions

**Status:** ACTIVE PROJECT GOVERNANCE  
**Platform:** MetaTrader 4 / MQL4  
**Architecture:** M01–M27  
**Primary Source of Truth:** GitHub

---

## 1. Project Objective

Develop a production-grade **BBMA Professional EA** for MetaTrader 4 using the agreed M01–M27 architecture.

The trading logic must remain faithful to **BBMA Core / Oma Ally methodology**. Supporting modules may manage data, validation, risk, execution, lifecycle, UI and integration, but must not silently alter the BBMA trading methodology.

The immediate development priority is to complete, audit and lock the **Master Blueprint** before full EA implementation.

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
- A module must not independently introduce an alternative processing clock.
- Timing assumptions must be explicit and consistent across producer and consumer modules.

---

## 4. Master Blueprint Governance

The Master Blueprint is the authoritative specification for architecture and behaviour before production coding.

During Blueprint development:

1. Audit architecture first.
2. Audit module responsibility and ownership.
3. Audit producer/consumer relationships.
4. Audit signal lifecycle and state transitions.
5. Audit temporal ordering and closed-candle assumptions.
6. Audit dependencies and declaration requirements.
7. Audit risk and trade lifecycle ownership.
8. Find contradictions, missing logic and redundant responsibilities.
9. Fix the specification before implementation.
10. Repeat the audit until no material unresolved issue remains.

Do not declare the Master Blueprint LOCKED merely because all 27 modules exist. It may be locked only after cross-module consistency has been reviewed.

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

The project follows this order:

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
**Functional Testing**  
↓  
**Backtesting / Validation**  
↓  
**Production Candidate**

Do not skip directly from an incomplete Blueprint to production implementation.

---

## 9. Source-Code Organisation

During initial implementation, prefer one clearly structured master EA file:

`BBMA_PROFESSIONAL_EA.mq4`

The architecture may still contain M01–M27 sections inside that file.

Do not split the project into 27 `.mqh` files merely for appearance. Physical modularisation should happen only when it improves maintainability and does not create unnecessary dependency complexity.

---

## 10. GitHub Workflow

### `main`
Reserved for approved/stable project state.

### `blueprint-dev`
Working branch for Master Blueprint development, audit and correction.

### Future `ea-dev`
May be created when implementation begins after the Master Blueprint is locked.

Rules:

- Development changes should be traceable through commits.
- Do not overwrite a LOCKED Master Blueprint casually.
- Significant Blueprint changes after lock require deliberate review.
- Keep experimental development away from stable project state.

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

Production coding begins from the LOCKED Master Blueprint.

Implementation must conform to the Blueprint. If coding exposes a genuine Blueprint flaw, fix and review the Blueprint deliberately rather than silently changing architecture only in code.

The final goal is one coherent system where **Blueprint → implementation → tests** describe the same behaviour.

---

## 15. Project Priority

**Correctness and architectural consistency take priority over speed, feature count and code size.**

The immediate goal is therefore:

> Build a complete, internally consistent and implementation-ready Master Blueprint for BBMA Professional EA M01–M27, then lock it before full production coding begins.

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
