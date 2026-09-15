# BBMA Autonomous Engineering Infrastructure

Status: **IMPLEMENTATION SPEC — Issue #150**  
Depends on: **PR #149 / `docs/BBMA_TASK_ORCHESTRATOR_CONTRACT.md`**  
Scope: governance/tooling/validation infrastructure only. No Strategy-Core or EA behaviour change.

## Goal
Build a quota-efficient, interruption-safe engineering control plane that makes BBMA development state-driven, evidence-driven and progressively autonomous without transferring Strategy-Core authority to tooling.

## Non-negotiable boundaries
- GitHub live state remains authoritative.
- Strategy work still follows `SOURCE_INDEX -> routed evidence -> accepted Core -> contracts/Blueprint -> code -> validation`.
- Existing specialized repository/MT4 checks keep ownership of their invariants; this layer selects/coordinates them instead of duplicating them.
- No automatic merge, deployment, production trading, destructive reset or Strategy-Core invention.
- Native compile/runtime claims require G40/MetaEditor/MT4 evidence. Cloud-only execution must report `NOT NATIVE VERIFIED`.
- Semantic dependency/ownership maps are populated only from verified contracts/audits; unknown edges remain unknown rather than guessed.

## Architecture
The infrastructure is split into five deterministic components:

1. **Task state plane** — active manifest, append-only event log, checkpoints, handoff capsule and resume boundary.
2. **Evidence plane** — SHA-256 artifact cache, content-addressed storage, evidence DAG and downstream staleness propagation.
3. **Validation plane** — model/risk routing, diff-impact inputs, targeted regression selection, environment identity and evidence packaging.
4. **Observability plane** — SQLite telemetry warehouse, failure-first summaries, golden trace comparison and build differential classification.
5. **Invariant plane** — generic lifecycle state-machine checks, randomized/property-style sequences, mutation self-tests and fault-injection of infrastructure writes.

## Quota policy
Spend model reasoning only where uncertainty exists. Deterministic inspection, hashing, event recording, trace comparison, telemetry aggregation and test selection run in tooling/G40. Context sent to a model should be a bounded context pack, not project history.

## Active-task manifest
A manifest records at minimum:
- task/roadmap ID, title and lane;
- phase/result;
- owner branch/commit/worktree;
- latest verified step and next safe action;
- blockers/HOLD state;
- validation statuses;
- artifact identities;
- risk score and model route;
- update timestamp.

Allowed phase progression is `PENDING -> PREFLIGHT -> IN_PROGRESS -> VALIDATION -> CLOSED`. Closure classifications follow the Task Orchestrator Contract.

## Checkpoint and handoff
Checkpoints are emitted after expensive/high-risk boundaries. A handoff capsule is an ultra-compact recovery view containing identity, latest verified boundary, current state, do-not-redo scope and exact next action. Resume always verifies live state before mutation.

## Evidence cache and DAG
Artifacts are identified by SHA-256. A prior reviewed result may be reused only when the artifact digest and applicable authority context still match.

Evidence nodes use typed IDs such as `source`, `core_rule`, `contract`, `code`, `test`, `compile`, `runtime`, `build` and `artifact`. Edges represent evidence dependency, not trading semantics. When a node changes, only downstream nodes are marked `STALE`; unaffected evidence remains valid.

This implements the provenance chain:

`source evidence -> accepted Core -> contract -> code -> test -> compile -> runtime -> build`

without asserting that every chain is already populated.

## Context packs
A task context pack contains only the manifest, relevant authority references, current diff/changed modules supplied by the caller, required evidence nodes, selected validations and unresolved blockers. Historical reasoning already captured by a contract/decision/test is not copied unless it is materially required.

## Model and risk routing
Routing uses the lowest adequate level:
- mechanical normalization/hash/reporting: light/routine;
- deterministic repo/docs comparison: medium;
- implementation/cross-module debugging/regression: high;
- Strategy-Core conflict, ownership conflict or difficult causal runtime analysis: high/xhigh.

Risk score inputs include Strategy-Core impact, execution authority, persistence/restart impact, multi-symbol state, code-change breadth and unresolved ambiguity. Routing never overrides an explicit user/roadmap requirement.

## Targeted regression selection
The selector consumes caller-supplied verified module/dependency metadata plus mandatory global invariants. It never invents module edges. High-risk or release-candidate work can escalate to the full configured suite.

## Telemetry warehouse
Runtime/test events are normalized into SQLite with timestamp, source, event type, JourneyID, DecisionID, symbol, status and raw JSON payload. Failure-first summaries return anomalies/failures first and aggregate PASS volume rather than streaming raw logs into ChatGPT.

The native log adapter ingests the authoritative NMJE `[N1-NMJE]`, `[N2-NMJE-DEC]` and `[N2-NMJE-OUT]` formats from explicitly labelled MT4 Expert, Strategy Tester or runtime-smoke files. Every record carries source-file SHA-256, line number, emitter/build marker and raw text; repeated ingestion is idempotent. Ingestion status is `OBSERVED` with `runtime_verification: NOT VERIFIED`, so importing a log cannot manufacture runtime PASS.

## Golden traces and differential builds
Golden traces compare normalized lifecycle events, not only P/L. Build comparison returns:
- `NO_DELTA` when traces are equivalent;
- `EXPECTED_DELTA` only when a caller explicitly authorizes the behavioural delta;
- `UNEXPECTED_DELTA` otherwise.

A shadow trace is read-only evidence. It cannot create/reject/rank/execute a trade.

## Lifecycle property model
The infrastructure model tests separation of candidate, confirmed, selected, validated, risk-approved, entry-ready, executed and terminal states. It is an engineering invariant model, not a new BBMA signal rule. Invalid backward/skipping transitions are rejected unless an explicit transition is defined by the model.

Randomized sequences, mutation self-tests and injected atomic-write failures prove that the test harness itself detects invalid lifecycle or persistence behaviour.

## Reproducible environment and release candidate identity
Environment snapshots record OS/Python/tool metadata supplied by the runner. Native G40 adapters later add exact MetaEditor/MT4 paths, versions, terminal identity and candidate MQ4/EX4 hashes.

Release-candidate evidence packages are immutable indexes of hashes/config/results. Any source/candidate hash change creates a new identity; old evidence is not silently reused.

## Parallel lanes
Independent lanes may run concurrently: source/evidence, implementation, runtime, historical-data and transcription. They share evidence/state through artifacts, not hidden chat assumptions. Strategy-Core adjudication remains a single authority chain and is never decided by majority vote among agents.

## Event-driven operation
Repository events should trigger bounded validation/review rather than periodic polling where possible. CI for this tooling runs only when the orchestration package/tests/workflow/spec change. Existing specialized EA workflows remain separate owners.

## Native G40 adapter boundary
The native adapter may:
- snapshot Git/worktree/process state;
- invoke explicitly configured existing compile/test/runtime commands;
- collect bounded result summaries and artifact hashes;
- refuse duplicate long-running jobs when a matching active process/marker exists.

It may not restart the primary MT4 terminal, enable trading, overwrite uncommitted work or claim native PASS without attributable output.

## Completion model
Implementation can be mechanically complete while native acceptance remains open. Therefore every subsystem records both deterministic test status and, where applicable, `NOT NATIVE VERIFIED` until G40 evidence exists.
