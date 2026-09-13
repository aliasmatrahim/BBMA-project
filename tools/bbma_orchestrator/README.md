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

The summary is failure-first so large PASS volumes do not need to be sent to ChatGPT.

## Golden/shadow traces

```bash
python -m tools.bbma_orchestrator trace-compare \
  --baseline baseline.json --candidate candidate.json

python -m tools.bbma_orchestrator shadow-compare \
  --authoritative authoritative.json --shadow shadow.json
```

Shadow comparison is explicitly read-only and reports `trade_authority: NONE`.

## Verified module graph

`config/bbma_module_graph.json` records the immutable `d1-owner-dev` evidence used for M01-M27 and M12N identities, ownership, and directly supported consumer edges. Load it through `load_verified_module_graph()`; the loader rejects missing modules, unresolved evidence references, authority/evidence commit mismatches, invalid coverage claims, unknown/self consumers, duplicate edges, and malformed Git object IDs.

Module identity is VERIFIED. Consumer-edge coverage is PARTIAL: an absent edge means NOT VERIFIED, never evidence that no dependency exists. Regression assignments remain NOT VERIFIED until their separate authority mapping is populated.

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
      "argv": ["C:\\path\\to\\wrapper.ps1"],
      "cwd": "D:\\path\\to\\verified-worktree",
      "timeout_seconds": 900
    }
  }
}
```

```bash
python -m tools.bbma_orchestrator native-describe --config native.json --name compile
python -m tools.bbma_orchestrator native-run --config native.json --name compile
```

The second command is still dry-run. `--execute` is required after live-state verification.

The repository intentionally does not ship a guessed G40/MetaEditor path or a command that restarts MT4. Native PASS remains unavailable until exact live G40 configuration is verified.

## Tests

```bash
python -m compileall tools/bbma_orchestrator
python -m unittest discover -s tests -p "test_bbma_orchestrator.py" -v
```

The suite covers atomic persistence, recovery capsules, evidence staleness, failure-first telemetry, lifecycle property-style checks, mutation self-detection, golden traces, shadow comparison and native-adapter fail-closed behaviour.
