# BBMA Repository Governance

## Purpose

GitHub is the operational source of truth for the BBMA Professional EA. This document governs how defects, architecture decisions, code changes, validation evidence, and releases move through the repository.

This governance layer does not replace the detailed contracts, decisions, runtime records, or strategy references already maintained in the project.

## Current branch roles

### `main`
The default branch currently carries repository-level dispatcher/tooling, GitHub Actions workflows, and governance entry points. Pull-request and issue templates must live on the default branch to be applied repository-wide.

### `d1-owner-dev`
The current active implementation branch contains the EA source and the detailed development source of truth, including:

- `blueprint/source/BBMA_EA.mq4`
- `PROJECT_INSTRUCTIONS.md`
- `blueprint/contracts/`
- `blueprint/decisions/`
- `blueprint/CURRENT.md`
- `blueprint/MASTER_QUEUE.md`
- runtime/audit/test evidence
- `blueprint/source/EA_RELEASE_IDENTITY.json`
- development verification/release history

Branch roles may evolve. When they do, update this document and the default-branch README in the same governance change.

## Source-of-truth hierarchy

When sources appear to disagree, resolve them deliberately rather than silently choosing one.

1. Explicit approved project decisions and active Project Instructions.
2. Active module/source contracts and locked strategy/reference evidence.
3. Current project status/queue and accepted audit records.
4. Current implementation source and release identity.
5. Historical patches, experiments, superseded evidence, and archived material.

A code change that intentionally changes an item higher in this hierarchy must update the governing decision/contract first or in the same PR.

## Standard change flow

### 1. Issue
Create a structured Issue for a confirmed/suspected defect or an intentional architecture/strategy change.

Do not mix unrelated defects and redesign requests in one Issue.

### 2. Scoped branch
Create a branch from the branch that actually owns the target being changed. Keep one technical purpose per branch.

Examples:

- `fix/m13-temporal-dedup`
- `fix/m16-pool-compaction`
- `arch/m15-final-authority`
- `chore/repo-governance-foundation`

Do not make feature work directly on `main`.

### 3. Smallest correct change
Preserve unaffected behavior and existing module ownership. Avoid broad rewrites when a targeted fix is sufficient.

### 4. Draft pull request
Open a Draft PR early enough that the diff, discussion, and CI evidence become part of the permanent record.

The PR must state:

- affected modules;
- concrete problem;
- exact solution;
- architecture impact;
- compile/static/runtime evidence actually produced;
- regression considerations;
- source-of-truth documents changed, if any.

### 5. Automated validation
Use the existing specialized workflows. Do not add another generic workflow when an existing canonical check already covers the invariant.

Evidence must be recorded as PASS/FAIL/NOT RUN. Never describe an unexecuted check as PASS.

For EA source changes, native MetaEditor compile evidence is preferred over syntax-only inference whenever the established workflow supports it.

### 6. Review
Review only the changed scope plus required upstream/downstream effects.

Priority order:

1. correctness;
2. deterministic runtime behavior;
3. architecture/ownership consistency;
4. regression safety;
5. compile compatibility;
6. maintainability/performance.

Review outcome should be explicit: MERGE, HOLD, or DO NOT MERGE.

### 7. Merge and close
Merge only after required evidence is green and unresolved material review findings are closed. Link the PR to its Issue so the reason, implementation, evidence, and result remain traceable.

## Architecture gates

A normal bug fix must not silently:

- redefine BBMA methodology;
- introduce RSI, MACD, Stochastic, ADX, news, session, or correlation logic as trading-signal logic;
- create a second processing clock where M15 is authoritative;
- mix live-candle state into a closed-candle contract;
- treat CANDIDATE as CONFIRMED;
- let risk modules generate entries;
- let execution modules recreate detector/selection logic;
- transfer module ownership without updating the relevant contract/decision;
- allow one pair's state to contaminate another pair.

Intentional changes to these boundaries require the Architecture Change Issue form and corresponding decision/contract updates.

## Runtime and state gates

Where relevant, PR validation must consider:

- array/pool bounds and capacity;
- stale state and initialization/reset;
- index validity after compaction;
- expiry/invalidation and duplicate suppression;
- restart/recovery behavior;
- symbol-specific digits, point/pip, spread, lot limits and StopLevel;
- magic-number ownership/collision safety;
- OrderSend/OrderModify error paths;
- history/data availability;
- MQL4 compatibility.

## Release/history policy

Do not create a parallel changelog if the active release identity and development verification/release history already record the same information. Extend the canonical release/history mechanism instead.

A release identity change must be traceable to the PR and validation evidence that produced it.

## Branch protection

The desired policy for `main` is PR-only integration with required checks appropriate to the changed scope. At the time this document was introduced, `main` was not branch-protected.

Repository settings should be updated to prevent accidental direct pushes once the exact required-check/ruleset configuration is selected. Do not claim branch protection is active until GitHub reports it as enabled.

## ChatGPT shorthand workflow

Within the BBMA project, commands may remain short because repository evidence is authoritative.

Examples:

- `check M13`
- `deep check M12-16`
- `fix issue 105`
- `compare PR81 PR82 PR83`
- `runtime M19`
- `compile`
- `regression`
- `code only`

Short instructions do not relax correctness, architecture, or validation requirements.
