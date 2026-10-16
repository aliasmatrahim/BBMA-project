from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from pathlib import Path

from .core import (
    RegressionSelector,
    TaskManifest,
    TaskStore,
    build_context_pack,
    compute_risk_score,
    route_model,
    utc_now,
    atomic_write_json,
    build_closeout,
)
from .evidence import ContentAddressedStore, EvidenceDB, build_evidence_package, sha256_file
from .experiment import classify_run_status, validate_manifest, verify_artifacts
from .dataset_validator import write_dataset_validation_report
from .telemetry import MT4_SOURCE_KINDS, TelemetryStore
from .trace import (
    build_trace_artifact,
    classify_build_delta,
    compare_shadow,
    compare_trace_artifacts,
)
from .native import NativeAdapter, git_snapshot, artifact_identity
from .verified import (
    architecture_invariant_mutation_check,
    load_verified_architecture_invariants,
    load_verified_regression_map,
    materialize_traceability,
)

def _json_print(data) -> None:
    print(json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False))

def _load_json(path: str | Path):
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)

def cmd_init(args: argparse.Namespace) -> None:
    risk = compute_risk_score(
        strategy_core=args.strategy_core,
        execution_authority=args.execution_authority,
        persistence_restart=args.persistence_restart,
        multi_symbol_state=args.multi_symbol_state,
        code_change=args.code_change,
        broad_diff=args.broad_diff,
        unresolved_ambiguity=args.unresolved_ambiguity,
        runtime_causal=args.runtime_causal,
    )
    route = route_model(
        args.task_type,
        risk_score=risk,
        strategy_core=args.strategy_core,
        architecture_conflict=args.architecture_conflict,
        runtime_causal=args.runtime_causal,
        explicit_route=args.model_route,
    )
    manifest = TaskManifest(
        task_id=args.task_id,
        roadmap_id=args.roadmap_id,
        title=args.title,
        lane=args.lane,
        branch=args.branch,
        commit=args.commit,
        latest_verified_step=args.latest_verified_step,
        next_safe_action=args.next_safe_action,
        risk_score=risk,
        model_route=route,
    )
    store = TaskStore(args.root)
    store.save(manifest)
    store.append_event(manifest, "INIT")
    _json_print(manifest.to_dict())

def cmd_status(args: argparse.Namespace) -> None:
    _json_print(TaskStore(args.root).load().to_dict())

def cmd_event(args: argparse.Namespace) -> None:
    store = TaskStore(args.root)
    manifest = store.load()
    details = json.loads(args.details) if args.details else {}
    store.append_event(manifest, args.event, details)
    print("event recorded")

def cmd_transition(args: argparse.Namespace) -> None:
    store = TaskStore(args.root)
    manifest = store.load()
    manifest.transition(args.phase)
    if args.result:
        manifest.result = args.result
    if args.latest_verified_step:
        manifest.latest_verified_step = args.latest_verified_step
    if args.next_safe_action:
        manifest.next_safe_action = args.next_safe_action
    manifest.validate()
    store.save(manifest)
    store.append_event(manifest, "TRANSITION", {"phase": args.phase, "result": manifest.result})
    _json_print(manifest.to_dict())

def cmd_validation(args: argparse.Namespace) -> None:
    store = TaskStore(args.root)
    manifest = store.load()
    manifest.record_validation(args.name, args.status, args.evidence, args.command, args.error)
    store.save(manifest)
    store.append_event(manifest, "VALIDATION", {"name": args.name, "status": args.status})
    _json_print(manifest.to_dict())

def cmd_checkpoint(args: argparse.Namespace) -> None:
    store = TaskStore(args.root)
    manifest = store.load()
    print(store.checkpoint(manifest, args.label))

def cmd_handoff(args: argparse.Namespace) -> None:
    store = TaskStore(args.root)
    print(store.handoff_capsule(store.load()), end="")

def cmd_context(args: argparse.Namespace) -> None:
    store = TaskStore(args.root)
    manifest = store.load()
    pack = build_context_pack(
        manifest,
        authority_refs=args.authority,
        changed_modules=args.module,
        selected_validations=args.validation,
        evidence_nodes=args.evidence_node,
    )
    atomic_write_json(args.output, pack)
    _json_print(pack)

def cmd_hash(args: argparse.Namespace) -> None:
    _json_print({"path": args.path, "sha256": sha256_file(args.path), "size": Path(args.path).stat().st_size})

def cmd_cache_put(args: argparse.Namespace) -> None:
    store = ContentAddressedStore(args.store)
    digest, path = store.put(args.path)
    _json_print({"sha256": digest, "stored_path": str(path)})

def cmd_evidence_node(args: argparse.Namespace) -> None:
    with EvidenceDB(args.db) as db:
        db.add_node(args.node_id, args.kind, args.digest, status=args.status)
        _json_print(db.get_node(args.node_id))

def cmd_evidence_edge(args: argparse.Namespace) -> None:
    with EvidenceDB(args.db) as db:
        db.add_edge(args.src, args.dst)
    print("edge recorded")

def cmd_evidence_stale(args: argparse.Namespace) -> None:
    with EvidenceDB(args.db) as db:
        stale = db.mark_changed(args.node_id, args.digest)
        _json_print({"changed": args.node_id, "stale_descendants": stale, "coverage": db.coverage()})

def cmd_traceability_materialize(args: argparse.Namespace) -> None:
    _json_print(materialize_traceability(
        args.traceability, args.module_graph, args.db
    ))

def cmd_architecture_invariants(args: argparse.Namespace) -> None:
    catalog = load_verified_architecture_invariants(
        args.catalog, args.module_graph
    )
    mutation = architecture_invariant_mutation_check(
        args.catalog, args.module_graph
    )
    _json_print(
        {
            "invariants": len(catalog["invariants"]),
            "detected_mutations": mutation["detected"],
            "runtime_enforcement": catalog["coverage"]["runtime_enforcement"],
        }
    )

def cmd_evidence_package(args: argparse.Namespace) -> None:
    package = build_evidence_package(args.output, args.files, metadata={"label": args.label})
    _json_print(package)

def cmd_closeout(args: argparse.Namespace) -> None:
    current = TaskStore(args.root)
    candidates = [TaskStore(root) for root in args.candidate_root]
    _json_print(build_closeout(current, candidates, args.output, extra_files=args.file))

def cmd_ingest_jsonl(args: argparse.Namespace) -> None:
    with TelemetryStore(args.db) as store:
        count = store.ingest_jsonl(args.path, source=args.source)
        _json_print({"ingested": count, "summary": store.failure_first_summary(limit=args.limit)})

def cmd_ingest_csv(args: argparse.Namespace) -> None:
    with TelemetryStore(args.db) as store:
        count = store.ingest_csv(args.path, source=args.source)
        _json_print({"ingested": count, "summary": store.failure_first_summary(limit=args.limit)})

def cmd_ingest_mt4_log(args: argparse.Namespace) -> None:
    with TelemetryStore(args.db) as store:
        count = store.ingest_mt4_log(
            args.path, source=args.source, source_kind=args.source_kind
        )
        _json_print({"ingested": count, "summary": store.failure_first_summary(limit=args.limit)})

def cmd_telemetry_summary(args: argparse.Namespace) -> None:
    with TelemetryStore(args.db) as store:
        _json_print(store.failure_first_summary(limit=args.limit))

def cmd_trace_export_telemetry(args: argparse.Namespace) -> None:
    with TelemetryStore(args.db) as store:
        records = store.attributable_events(
            source_sha256=args.source_sha256,
            emitter=args.emitter,
            limit=args.limit,
        )
    artifact = build_trace_artifact(
        records,
        source_sha256=args.source_sha256,
        emitter=args.emitter,
        role=args.role,
        authority_ref=args.authority_ref,
    )
    atomic_write_json(args.output, artifact)
    _json_print(
        {
            "output": str(Path(args.output).resolve()),
            "role": artifact["role"],
            "record_count": artifact["record_count"],
            "trace_sha256": artifact["trace_sha256"],
            "runtime_verification": artifact["runtime_verification"],
        }
    )

def cmd_trace_diff_artifacts(args: argparse.Namespace) -> None:
    baseline = _load_json(args.baseline)
    candidate = _load_json(args.candidate)
    _json_print(
        compare_trace_artifacts(
            baseline, candidate, authorization_ref=args.authorization_ref
        )
    )

def cmd_trace_compare(args: argparse.Namespace) -> None:
    baseline = _load_json(args.baseline)
    candidate = _load_json(args.candidate)
    _json_print(classify_build_delta(baseline, candidate, authorized_delta=args.authorized_delta))

def cmd_shadow_compare(args: argparse.Namespace) -> None:
    authoritative = _load_json(args.authoritative)
    shadow = _load_json(args.shadow)
    result = compare_shadow(authoritative, shadow)
    _json_print(
        {
            "result": result.result,
            "authoritative": result.authoritative,
            "shadow": result.shadow,
            "trade_authority": "NONE",
        }
    )

def cmd_select_tests(args: argparse.Namespace) -> None:
    if bool(args.module_graph) != bool(args.traceability):
        raise ValueError("--module-graph and --traceability must be supplied together")
    if args.module_graph:
        mapping = load_verified_regression_map(
            args.map, args.module_graph, args.traceability
        )
    else:
        mapping = _load_json(args.map)
        verified_fields = {
            "schema_version", "authority", "coverage", "tests", "known_unknowns"
        }
        if verified_fields.intersection(mapping):
            raise ValueError(
                "verified regression map requires --module-graph and --traceability"
            )
    selector = RegressionSelector(
        mapping.get("modules", mapping),
        mapping.get("mandatory_global", []),
        strict=bool(args.module_graph),
    )
    selected = selector.select(args.module, risk_score=args.risk_score, release_candidate=args.release_candidate)
    _json_print({"selected": selected})

def cmd_env_snapshot(args: argparse.Namespace) -> None:
    data = {
        "captured_at": utc_now(),
        "platform": platform.platform(),
        "python": sys.version,
        "python_executable": sys.executable,
        "cwd": os.getcwd(),
        "environment": {name: os.environ.get(name, "") for name in args.env},
        "native_status": "NOT NATIVE VERIFIED" if args.native_unverified else "NOT RUN",
    }
    atomic_write_json(args.output, data)
    _json_print(data)

def cmd_native_describe(args: argparse.Namespace) -> None:
    adapter = NativeAdapter(args.config)
    _json_print(adapter.describe(args.name))

def cmd_native_run(args: argparse.Namespace) -> None:
    adapter = NativeAdapter(args.config)
    result = adapter.run(args.name, execute=args.execute)
    _json_print(result)
    if args.execute and result["status"] == "FAIL":
        raise SystemExit(1)

def cmd_git_snapshot(args: argparse.Namespace) -> None:
    _json_print(git_snapshot(args.repo))

def cmd_artifact_identity(args: argparse.Namespace) -> None:
    _json_print({"artifacts": artifact_identity(args.files)})

def cmd_dataset_validate(args: argparse.Namespace) -> None:
    manifest_path = Path(args.manifest).resolve()
    manifest = _load_json(str(manifest_path))
    if not isinstance(manifest, dict):
        raise SystemExit("manifest must be a JSON object")
    root = Path(args.evidence_root).resolve()
    if not isinstance(manifest.get("artifacts"), list):
        raise SystemExit("manifest artifacts must be a list")
    dataset_artifacts = [item for item in manifest["artifacts"] if isinstance(item, dict) and item.get("kind") == "dataset"]
    if len(dataset_artifacts) != 1:
        raise SystemExit("manifest must contain exactly one dataset artifact")
    dataset_relative_path = dataset_artifacts[0].get("path")
    if not isinstance(dataset_relative_path, str) or not dataset_relative_path.strip():
        raise SystemExit("dataset artifact must declare a non-empty relative path")
    dataset_path = (root / dataset_relative_path).resolve()
    if dataset_path != root and root not in dataset_path.parents:
        raise SystemExit("dataset artifact path escapes evidence root")
    if not isinstance(args.output, str) or not args.output.strip():
        raise SystemExit("output path is required")
    output_path = Path(args.output)
    output_path = (root / output_path).resolve() if not output_path.is_absolute() else output_path.resolve()
    if output_path == root:
        raise SystemExit("output must be a file path inside the evidence root")
    if output_path == manifest_path:
        raise SystemExit("validation report cannot overwrite the run manifest")
    if output_path == dataset_path:
        raise SystemExit("validation report cannot overwrite the dataset")
    for existing_artifact in manifest["artifacts"]:
        if not isinstance(existing_artifact, dict) or existing_artifact.get("kind") == "dataset_validation_report":
            continue
        existing_path = existing_artifact.get("path")
        if isinstance(existing_path, str) and (root / existing_path).resolve() == output_path:
            raise SystemExit("validation report cannot overwrite another evidence artifact")
    if output_path != root and root not in output_path.parents:
        raise SystemExit("validation report path must remain inside evidence root")
    result = write_dataset_validation_report(
        dataset_path, manifest, output_path, max_gap_seconds=args.max_gap_seconds
    )
    digest = sha256_file(output_path)
    artifact = {"kind": "dataset_validation_report", "path": str(output_path.relative_to(root)), "sha256": digest}
    manifest["artifacts"] = [
        item for item in manifest.get("artifacts", [])
        if not isinstance(item, dict) or item.get("kind") != "dataset_validation_report"
    ]
    manifest["artifacts"].append(artifact)
    atomic_write_json(manifest_path, manifest)
    _json_print({
        "dataset_status": result.get("dataset_status"),
        "validation_status": result.get("validation_status"),
        "rows": result.get("rows", 0),
        "gap_count": result.get("gap_count", 0),
        "errors": result.get("errors", []),
        "report_path": str(output_path),
        "report_sha256": digest,
        "manifest_path": str(manifest_path),
    })
    if result.get("validation_status") != "PASS":
        raise SystemExit(2)

def cmd_experiment_register(args: argparse.Namespace) -> None:
    manifest_path = Path(args.manifest).resolve()
    manifest = _load_json(str(manifest_path))
    root = Path(args.evidence_root).resolve()
    manifest_errors = validate_manifest(manifest)
    artifact_errors = verify_artifacts(manifest, root)
    run_status = classify_run_status(
        manifest_errors,
        artifact_errors,
        process_exit_code=args.process_exit_code,
        validation_complete=args.validation_complete,
    )
    with EvidenceDB(args.db) as db:
        registered = db.register_experiment(
            manifest, manifest_path, root, run_status=run_status
        )
        matching = db.find_experiment_runs(registered["fingerprint"])
    _json_print({
        **registered,
        "same_configuration_run_ids": [item["run_id"] for item in matching],
        "manifest_errors": manifest_errors,
        "artifact_errors": artifact_errors,
        "evidence_only": True,
        "trade_authority": "NONE",
    })
    if run_status != "EVIDENCE_ACCEPTED":
        raise SystemExit(2)

def cmd_experiment_validate(args: argparse.Namespace) -> None:
    manifest = _load_json(args.manifest)
    manifest_errors = validate_manifest(manifest)
    artifact_errors = verify_artifacts(manifest, args.evidence_root)
    status = classify_run_status(
        manifest_errors,
        artifact_errors,
        process_exit_code=args.process_exit_code,
        validation_complete=args.validation_complete,
    )
    _json_print({
        "run_status": status,
        "hypothesis_result": "NOT_EVALUATED",
        "manifest_errors": manifest_errors,
        "artifact_errors": artifact_errors,
        "interpretation": "Evidence validity only; no profitability or runtime PASS is inferred.",
    })
    if status != "EVIDENCE_ACCEPTED":
        raise SystemExit(2)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="bbma-orchestrator")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init")
    p.add_argument("--root", required=True)
    p.add_argument("--task-id", required=True)
    p.add_argument("--roadmap-id", default="")
    p.add_argument("--title", required=True)
    p.add_argument("--lane", required=True)
    p.add_argument("--branch", default="")
    p.add_argument("--commit", default="")
    p.add_argument("--latest-verified-step", default="")
    p.add_argument("--next-safe-action", default="")
    p.add_argument("--task-type", default="repo")
    p.add_argument("--model-route", default="")
    for flag in (
        "strategy_core",
        "execution_authority",
        "persistence_restart",
        "multi_symbol_state",
        "code_change",
        "broad_diff",
        "unresolved_ambiguity",
        "runtime_causal",
        "architecture_conflict",
    ):
        p.add_argument("--" + flag.replace("_", "-"), action="store_true")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("status")
    p.add_argument("--root", required=True)
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("event")
    p.add_argument("--root", required=True)
    p.add_argument("--event", required=True)
    p.add_argument("--details", default="")
    p.set_defaults(func=cmd_event)

    p = sub.add_parser("transition")
    p.add_argument("--root", required=True)
    p.add_argument("--phase", required=True)
    p.add_argument("--result", default="")
    p.add_argument("--latest-verified-step", default="")
    p.add_argument("--next-safe-action", default="")
    p.set_defaults(func=cmd_transition)

    p = sub.add_parser("validation")
    p.add_argument("--root", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--status", required=True)
    p.add_argument("--evidence", default="")
    p.add_argument("--command", default="")
    p.add_argument("--error", default="")
    p.set_defaults(func=cmd_validation)

    p = sub.add_parser("checkpoint")
    p.add_argument("--root", required=True)
    p.add_argument("--label", required=True)
    p.set_defaults(func=cmd_checkpoint)

    p = sub.add_parser("handoff")
    p.add_argument("--root", required=True)
    p.set_defaults(func=cmd_handoff)

    p = sub.add_parser("context-pack")
    p.add_argument("--root", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--authority", action="append", default=[])
    p.add_argument("--module", action="append", default=[])
    p.add_argument("--validation", action="append", default=[])
    p.add_argument("--evidence-node", action="append", default=[])
    p.set_defaults(func=cmd_context)

    p = sub.add_parser("hash")
    p.add_argument("path")
    p.set_defaults(func=cmd_hash)

    p = sub.add_parser("cache-put")
    p.add_argument("--store", required=True)
    p.add_argument("path")
    p.set_defaults(func=cmd_cache_put)

    p = sub.add_parser("evidence-node")
    p.add_argument("--db", required=True)
    p.add_argument("--node-id", required=True)
    p.add_argument("--kind", required=True)
    p.add_argument("--digest", required=True)
    p.add_argument("--status", default="NOT VERIFIED")
    p.set_defaults(func=cmd_evidence_node)

    p = sub.add_parser("evidence-edge")
    p.add_argument("--db", required=True)
    p.add_argument("--src", required=True)
    p.add_argument("--dst", required=True)
    p.set_defaults(func=cmd_evidence_edge)

    p = sub.add_parser("evidence-stale")
    p.add_argument("--db", required=True)
    p.add_argument("--node-id", required=True)
    p.add_argument("--digest", required=True)
    p.set_defaults(func=cmd_evidence_stale)

    p = sub.add_parser("traceability-materialize")
    p.add_argument("--traceability", required=True)
    p.add_argument("--module-graph", required=True)
    p.add_argument("--db", required=True)
    p.set_defaults(func=cmd_traceability_materialize)

    p = sub.add_parser("architecture-invariants")
    p.add_argument("--catalog", required=True)
    p.add_argument("--module-graph", required=True)
    p.set_defaults(func=cmd_architecture_invariants)

    p = sub.add_parser("experiment-register")
    p.add_argument("--manifest", required=True)
    p.add_argument("--evidence-root", required=True)
    p.add_argument("--db", required=True)
    p.add_argument("--process-exit-code", type=int, default=0)
    p.add_argument("--validation-complete", action="store_true")
    p.set_defaults(func=cmd_experiment_register)

    p = sub.add_parser("dataset-validate")
    p.add_argument("--manifest", required=True)
    p.add_argument("--evidence-root", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--max-gap-seconds", type=int)
    p.set_defaults(func=cmd_dataset_validate)

    p = sub.add_parser("experiment-validate")
    p.add_argument("--manifest", required=True)
    p.add_argument("--evidence-root", required=True)
    p.add_argument("--process-exit-code", type=int, default=0)
    p.add_argument("--validation-complete", action="store_true")
    p.set_defaults(func=cmd_experiment_validate)

    p = sub.add_parser("evidence-package")
    p.add_argument("--output", required=True)
    p.add_argument("--label", default="")
    p.add_argument("files", nargs="+")
    p.set_defaults(func=cmd_evidence_package)

    p = sub.add_parser("closeout")
    p.add_argument("--root", required=True)
    p.add_argument("--candidate-root", action="append", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--file", action="append", default=[])
    p.set_defaults(func=cmd_closeout)

    for name, func in (("ingest-jsonl", cmd_ingest_jsonl), ("ingest-csv", cmd_ingest_csv)):
        p = sub.add_parser(name)
        p.add_argument("--db", required=True)
        p.add_argument("--path", required=True)
        p.add_argument("--source", default="")
        p.add_argument("--limit", type=int, default=50)
        p.set_defaults(func=func)

    p = sub.add_parser("ingest-mt4-log")
    p.add_argument("--db", required=True)
    p.add_argument("--path", required=True)
    p.add_argument("--source-kind", required=True, choices=MT4_SOURCE_KINDS)
    p.add_argument("--source", default="")
    p.add_argument("--limit", type=int, default=50)
    p.set_defaults(func=cmd_ingest_mt4_log)

    p = sub.add_parser("telemetry-summary")
    p.add_argument("--db", required=True)
    p.add_argument("--limit", type=int, default=50)
    p.set_defaults(func=cmd_telemetry_summary)

    p = sub.add_parser("trace-export-telemetry")
    p.add_argument("--db", required=True)
    p.add_argument("--source-sha256", required=True)
    p.add_argument("--emitter", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--role", choices=("candidate", "golden"), default="candidate")
    p.add_argument("--authority-ref", default="")
    p.add_argument("--limit", type=int, default=10000)
    p.set_defaults(func=cmd_trace_export_telemetry)

    p = sub.add_parser("trace-diff-artifacts")
    p.add_argument("--baseline", required=True)
    p.add_argument("--candidate", required=True)
    p.add_argument("--authorization-ref", default="")
    p.set_defaults(func=cmd_trace_diff_artifacts)

    p = sub.add_parser("trace-compare")
    p.add_argument("--baseline", required=True)
    p.add_argument("--candidate", required=True)
    p.add_argument("--authorized-delta", action="store_true")
    p.set_defaults(func=cmd_trace_compare)

    p = sub.add_parser("shadow-compare")
    p.add_argument("--authoritative", required=True)
    p.add_argument("--shadow", required=True)
    p.set_defaults(func=cmd_shadow_compare)

    p = sub.add_parser("select-tests")
    p.add_argument("--map", required=True)
    p.add_argument("--module-graph", default="")
    p.add_argument("--traceability", default="")
    p.add_argument("--module", action="append", default=[])
    p.add_argument("--risk-score", type=int, default=0)
    p.add_argument("--release-candidate", action="store_true")
    p.set_defaults(func=cmd_select_tests)

    p = sub.add_parser("env-snapshot")
    p.add_argument("--output", required=True)
    p.add_argument("--env", action="append", default=[])
    p.add_argument("--native-unverified", action="store_true")
    p.set_defaults(func=cmd_env_snapshot)

    p = sub.add_parser("native-describe")
    p.add_argument("--config", required=True)
    p.add_argument("--name", required=True)
    p.set_defaults(func=cmd_native_describe)

    p = sub.add_parser("native-run")
    p.add_argument("--config", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--execute", action="store_true")
    p.set_defaults(func=cmd_native_run)

    p = sub.add_parser("git-snapshot")
    p.add_argument("--repo", required=True)
    p.set_defaults(func=cmd_git_snapshot)

    p = sub.add_parser("artifact-identity")
    p.add_argument("files", nargs="+")
    p.set_defaults(func=cmd_artifact_identity)

    return parser

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if (
        args.command == "select-tests"
        and bool(args.module_graph) != bool(args.traceability)
    ):
        parser.error("--module-graph and --traceability must be supplied together")
    args.func(args)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
