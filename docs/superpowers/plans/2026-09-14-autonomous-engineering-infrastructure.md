# Autonomous Engineering Infrastructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or subagent-driven-development. Steps are tracked as independently verifiable tasks.

**Goal:** Implement the deterministic orchestration, evidence, telemetry, trace and recovery infrastructure defined in `docs/BBMA_AUTONOMOUS_ENGINEERING_INFRASTRUCTURE.md` without changing EA semantics.

**Architecture:** Dependency-free Python tooling owns task/evidence/telemetry state. GitHub Actions validates the tooling itself. Existing BBMA/MT4 workflows remain invariant owners. G40 native integration is attached only after live-device verification.

**Tech Stack:** Python 3.12 standard library, SQLite, JSON/JSONL, GitHub Actions, Windows/G40 adapters.

**Spec:** `docs/BBMA_AUTONOMOUS_ENGINEERING_INFRASTRUCTURE.md`

## Global constraints
- GitHub live state outranks chat memory.
- No Strategy-Core changes or inferred module semantics.
- No automatic merge/deploy/trading enablement.
- Native claims require G40 evidence.
- No duplicate replacement for existing specialized checks.

### Task 1: Task state, checkpoint and routing core
**Files:** create `tools/bbma_orchestrator/core.py`, package init and tests.

- [ ] Define validated task manifest schema and allowed phases/results.
- [ ] Implement atomic JSON write and append-only JSONL event recording.
- [ ] Implement checkpoint and <=40-line handoff capsule generation.
- [ ] Implement risk score and model-route decision functions.
- [ ] Implement targeted regression selector that consumes verified dependency metadata rather than inventing edges.
- [ ] Unit-test phase validation, recovery state, routing and selection.

Exit: deterministic unit tests PASS.

### Task 2: Artifact cache and evidence DAG
**Files:** create `tools/bbma_orchestrator/evidence.py`, extend tests.

- [ ] SHA-256 hash and content-addressed artifact storage.
- [ ] SQLite artifact review cache keyed by digest.
- [ ] Typed evidence node/edge storage.
- [ ] Recursive downstream stale propagation.
- [ ] Deterministic evidence-package index with file hashes.
- [ ] Unit-test cache reuse, stale propagation and injected atomic-write failure behaviour.

Exit: deterministic unit tests PASS; no semantic graph edges are fabricated.

### Task 3: Telemetry warehouse and failure-first reporting
**Files:** create `tools/bbma_orchestrator/telemetry.py`, extend tests.

- [ ] SQLite event schema with JourneyID/DecisionID/symbol/status plus raw payload.
- [ ] JSONL and CSV ingestion.
- [ ] Failure-first summary with PASS aggregation.
- [ ] Bounded lookup by JourneyID/DecisionID.
- [ ] Unit-test ingestion and anomaly summarization.

Exit: deterministic unit tests PASS.

### Task 4: Golden traces, differential builds and invariant model
**Files:** create `tools/bbma_orchestrator/trace.py`, extend tests.

- [ ] Normalize and compare lifecycle traces.
- [ ] Classify NO_DELTA / EXPECTED_DELTA / UNEXPECTED_DELTA.
- [ ] Implement read-only authoritative-vs-shadow trace comparison.
- [ ] Implement generic lifecycle transition model reflecting architecture state separation only.
- [ ] Run deterministic randomized/property-style transition sequences.
- [ ] Add mutation self-test proving an intentionally damaged transition table is detected.

Exit: deterministic unit tests PASS; model is labelled engineering invariant, not Strategy Core.

### Task 5: CLI, context pack, environment and evidence packaging
**Files:** create `tools/bbma_orchestrator/cli.py`, `__main__.py`, README; extend tests.

- [ ] Commands for manifest init/status/event/checkpoint/handoff.
- [ ] Commands for hashing/cache/evidence DAG.
- [ ] Commands for telemetry ingest/summary and trace comparison.
- [ ] Generate bounded context pack from manifest + supplied authority refs + selected validations.
- [ ] Generate reproducible environment snapshot.
- [ ] Generate immutable evidence package index.

Exit: CLI smoke tests PASS.

### Task 6: Tooling CI and event-driven validation
**Files:** create `.github/workflows/orchestrator-integrity.yml`.

- [ ] Trigger on PR/push changes limited to orchestrator tooling/spec/tests/workflow.
- [ ] Python syntax compile.
- [ ] Unit tests.
- [ ] CLI smoke test.
- [ ] Do not invoke or duplicate native EA checks.

Exit: GitHub Actions PASS on the scoped PR.

### Task 7: G40 native adapter
**Files:** create adapter only after device/worktree recovery is verified.

- [ ] Re-read G40 worktrees/processes/manifests before mutation.
- [ ] Map existing canonical native compile/test commands; do not recreate them.
- [ ] Add duplicate-process guard and bounded result collection.
- [ ] Add MetaEditor/MT4/environment identity capture.
- [ ] Prove no primary MT4 restart/trading enablement path exists.
- [ ] Run adapter dry-run then native targeted verification.

Exit: native adapter evidence PASS. Until then status is `NOT NATIVE VERIFIED`.

### Task 8: Verified dependency/traceability population
**Files:** evidence DB/config generated from authoritative audits/contracts.

- [ ] Wait for relevant B architecture/gap audit outputs where semantics/ownership are not already explicit.
- [ ] Populate only verified source/Core/contract/code/test edges.
- [ ] Leave unknown edges absent/NOT VERIFIED.
- [ ] Run stale-propagation and targeted-regression selection against the verified graph.

Exit: graph coverage report distinguishes VERIFIED vs NOT VERIFIED; no guessed ownership.

### Task 9: Autonomous operating lanes
- [ ] Encode lane identity in manifests: source/evidence, implementation, runtime, historical, transcription.
- [ ] Permit parallel work only when dependency graph shows no shared mutable owner.
- [ ] Use event-driven GitHub validation/review rather than polling where possible.
- [ ] Route agent/model by risk/uncertainty; escalate only when deterministic tooling cannot decide.

Exit: orchestrator can produce a bounded next-action/context package for each independent lane.

## Verification before completion
- Run full orchestrator test suite and syntax compilation.
- Inspect PR diff for EA/source/queue drift.
- Confirm no automatic merge/deploy/restart/trading action exists.
- Record G40-dependent items separately as `NOT NATIVE VERIFIED` if the device is unavailable.
