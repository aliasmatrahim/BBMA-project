# BBMA Orchestrator Tooling

Dependency-free control-plane utilities for Issue #150.

This package does **not** implement BBMA trading rules. It manages engineering state, evidence, telemetry summaries, trace comparisons and native-command orchestration around the authoritative project workflow.

## Core commands

```bash
python -m tools.bbma_orchestrator init \
  --root .bbma-task \
  --task-id B1.3-P3 \
  --roadmap-id B1.3 \
  --title "Latest evidence inventory" \
  --lane source \
  --task-type repo

python -m tools.bbma_orchestrator status --root .bbma-task
python -m tools.bbma_orchestrator checkpoint --root .bbma-task --label after-audit
python -m tools.bbma_orchestrator handoff --root .bbma-task
```

`ACTIVE_TASK.json` is the current state. `TASK_EVENTS.jsonl` is append-only chronology. Checkpoints are immutable continuation snapshots.

## Context packs

```bash
python -m tools.bbma_orchestrator context-pack \
  --root .bbma-task \
  --output context.json \
  --authority README.md \
  --authority blueprint/CURRENT.md \
  --validation orchestrator-integrity
```

Only explicitly supplied authority references, modules, validations and evidence nodes are included. The tool does not import historical chat context.

## Profitability experiment evidence gate

Use the G1 data gate first, then validate and register the manifest in the existing SQLite evidence inventory:

```bash
python -m tools.bbma_orchestrator dataset-validate \
  --manifest ./evidence/run-001/run-manifest.json \\\
  --evidence-root ./evidence/run-001 \\\
  --output dataset-validation.json \\\
  --max-gap-seconds 60
python -m tools.bbma_orchestrator experiment-validate \\\
  --manifest ./evidence/run-001/run-manifest.json \\\
  --evidence-root ./evidence/run-001 \\\
  --validation-complete
python -m tools.bbma_orchestrator experiment-register \\\
  --manifest ./evidence/run-001/run-manifest.json \\\
  --evidence-root ./evidence/run-001 \\\
  --db ./evidence/evidence.sqlite \\\
  --validation-complete
```

For bar CSVs, use `timestamp,bid_open,bid_high,bid_low,bid_close,ask_open,ask_high,ask_low,ask_close`. For tick CSVs, use `timestamp,bid,ask` and declare a preregistered `--max-gap-seconds`. Timestamp values must be timezone-aware ISO-8601. Bar timestamps use `BAR_OPEN`; tick timestamps use `TICK_TIME`. Missing bar intervals fail unless the exact gap is covered by an explicit `dataset.allowed_gap_windows` entry. The validator never interpolates or repairs data.

`experiment-register` enforces unique `run_id`, stores manifest/artifact lineage in the existing EvidenceDB DAG, groups matching setup fingerprints, and supports explicit `parent_run_id` links. Re-registering the exact same manifest is idempotent; reusing a run ID for different manifest bytes fails closed. Evidence nodes remain `NOT VERIFIED`; no runtime or trade authority is granted.

The commands exit non-zero on invalid evidence. `EVIDENCE_ACCEPTED` means evidence integrity only; profitability, data-source authenticity, BBMA Core compliance and runtime acceptance remain separate decisions. See `blueprint/research/PROFITABILITY_EXPERIMENT_EVIDENCE_CONTRACT_V1.md` and `blueprint/research/PROFITABILITY_EXPERIMENT_GAP_AUDIT_G0_G5.md`.

## Evidence and cache

```bash
python -m tools.bbma_orchestrator hash some-file
python -m tools.bbma_orchestrator cache-put --store .bbma-cache some-file
python -m tools.bbma_orchestrator evidence-node --db evidence.db \
  --node-id source:example --kind source --digest abc --status VALID
```

Evidence edges mean provenance/dependency only. They are not trading semantics. A changed node marks only downstream evidence stale.

## Telemetry

```bash
python -m tools.bbma_orchestrator ingest-jsonl \
  --db telemetry.db --path runtime.jsonl --source mt4

python -m tools.bbma_orchestrator telemetry-summary \
  --db telemetry.db --limit 50
```

For native MT4/tester logs:

```bash
python -m tools.bbma_orchestrator ingest-mt4-log \
  --db telemetry.db --path 20260910.log \
  --source-kind mt4-expert --source g40:terminal-id:20260910
```

`ingest-mt4-log` accepts an explicit `mt4-expert`, `strategy-tester`, or
`runtime-smoke` source kind. It reuses the authoritative NMJE N1/N2 formats,
requires identity-bearing fields for current additive formats, stores the file
hash, line, emitter/build marker and raw record, and is idempotent by source
hash plus line and marker. A recognized malformed marker rejects the whole file
before partial publish.

Ingestion records `OBSERVED` and `runtime_verification: NOT VERIFIED`; it never
promotes a log to runtime PASS. The summary is failure-first so large PASS
volumes do not need to be sent to ChatGPT.

## Golden/shadow traces

```bash
python -m tools.bbma_orchestrator trace-compare \
  --baseline baseline.json --candidate candidate.json

python -m tools.bbma_orchestrator shadow-compare \
  --authoritative authoritative.json --shadow shadow.json
```

For attributable telemetry artifacts:

```bash
python -m tools.bbma_orchestrator trace-export-telemetry \
  --db telemetry.db --source-sha256 <log-sha256> \
  --emitter "<exact build emitter>" --output candidate-trace.json

python -m tools.bbma_orchestrator trace-diff-artifacts \
  --baseline approved-golden.json --candidate candidate-trace.json
```

Export requires an exact source-file SHA-256 and emitter, preserves source-line
and event-key provenance, and writes a tamper-evident trace hash. The default
role is `candidate`. Creating a `golden` role requires an external
`--authority-ref`; comparing against a candidate-role baseline fails closed.
A changed artifact is `EXPECTED_DELTA` only when
`--authorization-ref <evidence>` is explicitly supplied. Runtime verification
is copied from telemetry and is never promoted by export or comparison.

Shadow comparison is explicitly read-only and reports `trade_authority: NONE`.

## Verified module graph

`config/bbma_module_graph.json` records the immutable `d1-owner-dev` evidence used for M01-M27 and M12N identities, ownership, and directly supported consumer edges. Load it through `load_verified_module_graph()`; the loader rejects missing modules, unresolved evidence references, authority/evidence commit mismatches, invalid coverage claims, unknown/self consumers, duplicate edges, and malformed Git object IDs.

Module identity is VERIFIED. Consumer-edge coverage is PARTIAL: an absent edge means NOT VERIFIED, never evidence that no dependency exists. Regression assignments remain NOT VERIFIED until their separate authority mapping is populated.

## Evidence-bound architecture invariants

`config/bbma_architecture_invariants.json` selects only explicit ownership
boundaries backed by standalone contracts in the accepted module graph.

```bash
python -m tools.bbma_orchestrator architecture-invariants \
  --catalog config/bbma_architecture_invariants.json \
  --module-graph config/bbma_module_graph.json
```

The command verifies the authority commit and Git blobs, exact module ownership
and evidence bindings, then exhaustively mutates every catalogued ownership
boundary to prove the guard detects drift. It reports runtime enforcement as
`NOT VERIFIED`; static validation cannot create native/runtime PASS. Catalog
coverage is intentionally non-exhaustive, so absence is not proof that another
module has no invariant.

## Verified Core traceability

`config/bbma_traceability.json` maps the attributable `CORE-V2-F1` through `CORE-V2-F6` chains across source evidence, Core rule, contract, module, code, static test record and runtime. Every catalog item is pinned to the accepted `d1-owner-dev` commit and Git blob.

```bash
python -m tools.bbma_orchestrator traceability-materialize \
  --traceability config/bbma_traceability.json \
  --module-graph config/bbma_module_graph.json \
  --db evidence.db
```

The loader accepts exactly F1-F6, rejects authority drift, resolves every catalog `commit:path` against the local Git object database, rejects blob mismatches, and rejects evidence-kind mismatches, duplicate or missing evidence references, unknown modules, and unsupported VERIFIED claims. Materialization reuses the existing evidence DAG, binds each node digest to the resolved immutable evidence records, and preserves each incomplete stage as `NOT VERIFIED` or `HOLD`.

Runtime for F1-F6 remains `NOT VERIFIED`. F4 code coverage remains `SOURCE CONFLICT`: the pinned implementation-pending decision and the later current-code-implemented re-audit have no explicit adjudication artifact; its test coverage also remains `PARTIAL` until an attributable executable combined-regression command/result is mapped. F5 has no standalone active M07 contract. F7 is an umbrella with multiple provenance/lifecycle decisions and retained HOLD boundaries, so it is not flattened into an invented singular chain.

## Targeted regression selection

The selector consumes a verified external map:

```json
{
  "mandatory_global": ["global-invariant"],
  "modules": {
    "M12": {"tests": ["m12-regression"], "consumers": ["M13"]},
    "M13": {"tests": ["m13-regression"], "consumers": []}
  }
}
```

Unknown modules produce no guessed dependency tests. Populate real edges only from accepted project contracts/audits.

## Native adapter

Native commands come from an explicit JSON config and default to dry-run:

```json
{
  "commands": {
    "compile": {
      "argv": ["C:\\path\\to\\metaeditor.exe", "/compile:candidate.mq4"],
      "cwd": "D:\\path\\to\\isolated-evidence",
      "timeout_seconds": 900,
      "enabled": true,
      "expected_inputs": [
        {"path": "candidate.mq4", "sha256": "<64-hex-sha256>"}
      ],
      "exclusive_process_names": ["metaeditor.exe"],
      "result_contract": {
        "kind": "metaeditor_0e0w",
        "log_path": "compile.log",
        "artifacts": ["candidate.ex4"]
      }
    }
  }
}
```

```bash
python -m tools.bbma_orchestrator native-describe --config native.json --name compile
python -m tools.bbma_orchestrator native-run --config native.json --name compile
```

The second command is still dry-run. `--execute` is required after live-state
verification. Execution fails closed if a command is disabled, an expected input
hash drifts, an exclusive process is already active, or the declared result
contract is not satisfied. MetaEditor PASS requires an attributable 0-error,
0-warning log (UTF-8 or BOM-marked UTF-16) and every declared artifact; its raw
process return code is retained separately.

Host-specific executable paths, hashes and source copies belong in task evidence,
not in this repository. Existing specialized validation workflows remain external
owners: the registry records their identities instead of copying their logic.
Commands that would restart or launch MT4 must remain disabled with an explicit
`blocked_reason` until current authority and user authorization are both present.

### G40 source-manifest planning

`source_g40.scan_manifest(...)` and `source_g40.plan_resume(...)` are read-only.
They inspect manifest JSON plus sibling `chunk_###.done` markers and return a
bounded plan; they never launch transcription/media jobs and never grant Core
authority. `ASR-DRAFT` remains `core_eligible: false` even when processing is
mechanically complete. Unknown/incomplete schemas fail closed to `REVIEW_REQUIRED`.

Any later resume command must still be declared explicitly through the native
adapter. Start disabled and bind only the reviewed missing units, for example:

```json
{
  "commands": {
    "source-resume": {
      "argv": ["<explicit-local-runner>", "--units", "<reviewed-missing-units>"],
      "cwd": "<isolated-source-workspace>",
      "timeout_seconds": 3600,
      "enabled": false,
      "blocked_reason": "Review source_g40 resume plan and authorize execution first"
    }
  }
}
```

## Tests

```bash
python -m compileall tools/bbma_orchestrator
python -m unittest discover -s tests -p "test_*.py" -v
```

The suite covers atomic persistence, recovery capsules, evidence staleness, failure-first telemetry, lifecycle and evidence-bound BBMA architecture property checks, mutation self-detection, golden traces, shadow comparison, native-adapter fail-closed behaviour, and the separate profitability experiment manifest contract. The experiment validator checks provenance/schema and does not claim profitability or runtime PASS.
