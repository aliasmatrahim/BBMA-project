from __future__ import annotations
from pathlib import Path
import hashlib, json, os, shutil, sqlite3, subprocess, sys, time

WORKTREE = Path(r"D:\BBMA\Workspace\autonomy-eff-ab-154")
ROOT = Path(r"D:\BBMA\Workspace\infra150_validation\task-154-autonomy-eff-ab")
OUT = ROOT / "benchmark"
AUTH = OUT / "authority_snapshot"
PYTHON = Path(r"D:\BBMA_SOURCE_AUDIT_VIDEOS\tools\python312\runtime\python.exe")
TOOLING_COMMIT = "b0db1b652a0f46691b5aad52299239ae42a98994"
D1_COMMIT = "23def0919386263007ead1898b94637cc17f7f36"
AUTH_FP = f"tooling={TOOLING_COMMIT};d1={D1_COMMIT};protocol=1"
TELEMETRY_DB = Path(r"D:\BBMA\Workspace\infra150_validation\task-150-telemetry-ingest\g40-telemetry-strict.db")
TASK_ROOT = ROOT

sys.path.insert(0, str(WORKTREE))
from tools.bbma_orchestrator.core import TaskStore, build_context_pack, compute_risk_score, route_model
from tools.bbma_orchestrator.evidence import ContentAddressedStore, EvidenceDB, build_evidence_package, sha256_file
from tools.bbma_orchestrator.telemetry import TelemetryStore
def jwrite(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

def run(cmd: list[str], label: str, timeout: int = 240) -> dict:
    started = time.perf_counter()
    cp = subprocess.run(cmd, cwd=WORKTREE, capture_output=True, text=True, timeout=timeout)
    elapsed = time.perf_counter() - started
    rec = {"label": label, "command": cmd, "returncode": cp.returncode,
           "duration_s": round(elapsed, 6), "stdout": cp.stdout, "stderr": cp.stderr}
    log = OUT / "logs" / f"{label}.json"
    jwrite(log, rec)
    rec["log_path"] = str(log)
    return rec

def file_record(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(data).hexdigest(),
            "size": len(data), "lines": data.count(b"\n") + (1 if data else 0)}

def context_stats(files: list[Path]) -> dict:
    records = [file_record(p) for p in files]
    return {"artifacts": len(records), "bytes": sum(x["size"] for x in records),
            "lines": sum(x["lines"] for x in records), "files": records}
def git_show_bytes(rel: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(WORKTREE), "show", f"{D1_COMMIT}:{rel}"])

def snapshot(rel: str) -> Path:
    dst = AUTH / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    data = git_show_bytes(rel)
    if not dst.exists() or dst.read_bytes() != data:
        dst.write_bytes(data)
    return dst

def export_telemetry_raw() -> tuple[Path, Path, dict]:
    raw_path = OUT / "telemetry_raw.jsonl"
    summary_path = OUT / "telemetry_summary.json"
    con = sqlite3.connect(f"file:{TELEMETRY_DB.as_posix()}?mode=ro", uri=True)
    cols = [x[1] for x in con.execute("PRAGMA table_info(events)").fetchall()]
    with raw_path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in con.execute("SELECT * FROM events ORDER BY id"):
            fh.write(json.dumps(dict(zip(cols, row)), sort_keys=True, ensure_ascii=False) + "\n")
    con.close()
    with TelemetryStore(TELEMETRY_DB) as store:
        summary = store.failure_first_summary(limit=50)
    jwrite(summary_path, summary)
    return raw_path, summary_path, summary
def prepare_inputs() -> dict:
    strategy_paths = [
        "docs/references/SOURCE_INDEX.md",
        "docs/references/video/oma_ally_finale/V06/V06_extracted_rules.md",
        "docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md",
        "blueprint/CORE_V2_F6_TIMING_VERIFICATION_AUDIT.md",
        "blueprint/contracts/M12_REENTRY_SOURCE_CONTRACT.md",
        "blueprint/contracts/M22_ORDER_EXECUTION_CONTRACT.md",
        "blueprint/contracts/M27_ORCHESTRATOR_END_TO_END_CONTRACT.md",
        "blueprint/source/BBMA_EA.mq4",
        ".github/workflows/core-v2-f6-pr-dispatch.yml",
    ]
    strategy = [snapshot(p) for p in strategy_paths]
    raw, summary, summary_obj = export_telemetry_raw()
    return {
        "strategy_paths": strategy_paths,
        "strategy_files": strategy,
        "telemetry_raw": raw,
        "telemetry_summary": summary,
        "telemetry_summary_obj": summary_obj,
    }

def pycmd(*args: str) -> list[str]:
    return [str(PYTHON), *args]
def task_definitions(prep: dict) -> dict:
    return {
        "docs_traceability": {
            "baseline_context": [WORKTREE / "README.md", WORKTREE / "docs/BBMA_TASK_ORCHESTRATOR_CONTRACT.md",
                                 WORKTREE / "docs/BBMA_AUTONOMOUS_ENGINEERING_INFRASTRUCTURE.md",
                                 WORKTREE / "config/bbma_traceability.json", WORKTREE / "config/bbma_module_graph.json"],
            "validation_kind": "traceability", "task_type": "repo", "risk": 0,
            "authority_refs": ["README.md", "docs/BBMA_TASK_ORCHESTRATOR_CONTRACT.md",
                               "config/bbma_traceability.json", "config/bbma_module_graph.json"],
            "evidence_nodes": ["CORE-V2-F1", "CORE-V2-F2", "CORE-V2-F3", "CORE-V2-F4", "CORE-V2-F5", "CORE-V2-F6"],
            "changed_modules": []},
        "telemetry_tooling": {
            "baseline_context": [WORKTREE / "tools/bbma_orchestrator/telemetry.py", WORKTREE / "tools/bbma_orchestrator/cli.py",
                                 WORKTREE / "tests/test_bbma_orchestrator.py", prep["telemetry_raw"]],
            "validation_kind": "telemetry", "task_type": "regression", "risk": compute_risk_score(code_change=True),
            "authority_refs": ["tools/bbma_orchestrator/telemetry.py", "tests/test_bbma_orchestrator.py", f"telemetry-db-sha256:{sha256_file(TELEMETRY_DB)}"],
            "evidence_nodes": [], "changed_modules": ["telemetry"]},
        "strategy_f6_readonly": {
            "baseline_context": prep["strategy_files"],
            "validation_kind": "strategy_f6", "task_type": "repo",
            "risk": compute_risk_score(strategy_core=True),
            "authority_refs": prep["strategy_paths"],
            "evidence_nodes": ["SRC_V06", "CORE_DOC", "CORE_F6", "C_M12", "C_M22", "C_M27", "CODE_F6", "TEST_DRIVER_F6", "TEST_F6"],
            "changed_modules": ["M12", "M22", "M27"]},
    }

def traceability_cmd(db: Path) -> list[str]:
    return pycmd("-m", "tools.bbma_orchestrator", "traceability-materialize",
                 "--traceability", "config/bbma_traceability.json",
                 "--module-graph", "config/bbma_module_graph.json", "--db", str(db))

def telemetry_full_cmd() -> list[str]:
    return pycmd("-m", "unittest", "discover", "-s", "tests", "-p", "test_bbma_orchestrator.py", "-v")

def telemetry_focused_cmd() -> list[str]:
    return pycmd("-m", "unittest", "discover", "-s", "tests", "-p", "test_bbma_orchestrator.py", "-k", "TelemetryTests", "-v")
def select_f6_tests(label: str) -> tuple[list[str], dict]:
    cmd = pycmd("-m", "tools.bbma_orchestrator", "select-tests",
                "--map", "config/bbma_regression_map.json",
                "--module-graph", "config/bbma_module_graph.json",
                "--traceability", "config/bbma_traceability.json",
                "--module", "M12", "--module", "M22", "--module", "M27", "--risk-score", "30")
    rec = run(cmd, label)
    selected = json.loads(rec["stdout"])["selected"] if rec["returncode"] == 0 else []
    return selected, rec

def run_validation(task: str, kind: str, mode: str, iteration: str) -> dict:
    run_dir = OUT / "runs" / task / mode / iteration
    run_dir.mkdir(parents=True, exist_ok=True)
    if kind == "traceability":
        return run(traceability_cmd(run_dir / "trace.db"), f"{task}-{mode}-{iteration}-trace")
    if kind == "telemetry":
        cmd = telemetry_full_cmd() if mode == "baseline" else telemetry_focused_cmd()
        return run(cmd, f"{task}-{mode}-{iteration}-tests", timeout=420)
    if kind == "strategy_f6":
        trace = run(traceability_cmd(run_dir / "trace.db"), f"{task}-{mode}-{iteration}-trace")
        selected, sel = select_f6_tests(f"{task}-{mode}-{iteration}-selection")
        return {"returncode": 0 if trace["returncode"] == 0 and sel["returncode"] == 0 else 1,
                "duration_s": round(trace["duration_s"] + sel["duration_s"], 6),
                "trace": trace, "selection": sel, "selected_tests": selected}
    raise ValueError(kind)
def validation_inputs(task: str, cfg: dict) -> list[Path]:
    if task == "telemetry_tooling":
        return [WORKTREE / "tools/bbma_orchestrator/telemetry.py", WORKTREE / "tools/bbma_orchestrator/cli.py",
                WORKTREE / "tests/test_bbma_orchestrator.py", TELEMETRY_DB]
    if task == "strategy_f6_readonly":
        return list(cfg["baseline_context"]) + [WORKTREE / "config/bbma_traceability.json",
                                                WORKTREE / "config/bbma_module_graph.json",
                                                WORKTREE / "config/bbma_regression_map.json"]
    return list(cfg["baseline_context"])

def make_pack(task: str, cfg: dict, iteration: str, prep: dict) -> tuple[Path, list[Path], dict]:
    manifest = TaskStore(TASK_ROOT).load()
    selected = []
    if task == "strategy_f6_readonly":
        selected, _ = select_f6_tests(f"{task}-pack-{iteration}-selection")
    validations = selected or (["TelemetryTests"] if task == "telemetry_tooling" else ["traceability-materialize"])
    pack = build_context_pack(manifest, authority_refs=cfg["authority_refs"],
                              changed_modules=cfg["changed_modules"], selected_validations=validations,
                              evidence_nodes=cfg["evidence_nodes"])
    pack_path = OUT / "contexts" / f"{task}-{iteration}.json"
    jwrite(pack_path, pack)
    extras: list[Path] = []
    if task == "telemetry_tooling": extras.append(prep["telemetry_summary"])
    sel_meta = {"selected_tests": selected}
    return pack_path, extras, sel_meta
def cache_pass(files: list[Path], store: ContentAddressedStore, db: EvidenceDB, record_pass: bool) -> dict:
    hits = misses = bytes_avoided = 0
    records = []
    for path in files:
        digest = sha256_file(path)
        dst = store.root / digest[:2] / digest
        existed = dst.exists()
        _, stored = store.put(path)
        if existed:
            hits += 1; bytes_avoided += path.stat().st_size
        else:
            misses += 1
        if record_pass:
            db.record_artifact(path, reviewed_status="PASS", authority_fingerprint=AUTH_FP,
                               metadata={"benchmark": "ISSUE-154"})
        records.append({"path": str(path), "sha256": digest, "hit": existed, "stored": str(stored)})
    return {"hits": hits, "misses": misses, "copy_bytes_avoided": bytes_avoided, "records": records}

def reusable(files: list[Path], db: EvidenceDB) -> bool:
    return all(db.can_reuse(path, AUTH_FP) for path in files)

def model_route(cfg: dict, strategy: bool = False) -> str:
    return route_model(cfg["task_type"], risk_score=cfg["risk"], strategy_core=strategy)
def baseline_run(task: str, cfg: dict, iteration: str) -> dict:
    start = time.perf_counter()
    ctx = context_stats(list(cfg["baseline_context"]))
    val = run_validation(task, cfg["validation_kind"], "baseline", iteration)
    elapsed = time.perf_counter() - start
    rec = {"task": task, "mode": "baseline", "iteration": iteration,
           "wall_clock_s": round(elapsed, 6), "model_context": ctx,
           "cache_hits": 0, "cache_misses": 0, "cache_copy_bytes_avoided": 0,
           "repeated_validation_executed": 1, "repeated_validation_avoided": 0,
           "validation_status": "PASS" if val["returncode"] == 0 else "FAIL",
           "validation": val, "risk_score": cfg["risk"],
           "model_route": model_route(cfg, task == "strategy_f6_readonly")}
    jwrite(OUT / "runs" / task / "baseline" / f"{iteration}.json", rec)
    return rec

def upgraded_run(task: str, cfg: dict, iteration: str, prep: dict,
                 store: ContentAddressedStore, db: EvidenceDB, cold_pass: dict[str, bool]) -> dict:
    start = time.perf_counter()
    inputs = validation_inputs(task, cfg)
    cache = cache_pass(inputs, store, db, record_pass=False)
    pack, extras, sel_meta = make_pack(task, cfg, iteration, prep)
    ctx = context_stats([pack, *extras])
    can_reuse = iteration == "warm" and cold_pass.get(task, False) and reusable(inputs, db)
    if can_reuse:
        val = {"returncode": 0, "duration_s": 0.0, "reused": True,
               "reason": "all validation inputs digest-match prior PASS under identical authority fingerprint"}
        status = "REUSED_PASS"
    else:
        val = run_validation(task, cfg["validation_kind"], "upgraded", iteration)
        status = "PASS" if val["returncode"] == 0 else "FAIL"
        if status == "PASS":
            cache_pass(inputs, store, db, record_pass=True)
            cold_pass[task] = True
    elapsed = time.perf_counter() - start
    rec = {"task": task, "mode": "upgraded", "iteration": iteration,
           "wall_clock_s": round(elapsed, 6), "model_context": ctx,
           "cache_hits": cache["hits"], "cache_misses": cache["misses"],
           "cache_copy_bytes_avoided": cache["copy_bytes_avoided"],
           "repeated_validation_executed": 0 if can_reuse else 1,
           "repeated_validation_avoided": 1 if can_reuse else 0,
           "validation_status": status, "validation": val,
           "risk_score": cfg["risk"], "model_route": model_route(cfg, task == "strategy_f6_readonly"),
           **sel_meta}
    jwrite(OUT / "runs" / task / "upgraded" / f"{iteration}.json", rec)
    return rec
def reduction(old: float, new: float) -> float:
    return 0.0 if old == 0 else (old - new) / old

def evaluate(runs: list[dict], tasks: dict) -> dict:
    by = {(r["task"], r["mode"], r["iteration"]): r for r in runs}
    base_warm = [by[(t, "baseline", "warm")] for t in tasks]
    up_warm = [by[(t, "upgraded", "warm")] for t in tasks]
    base_bytes = sum(r["model_context"]["bytes"] for r in base_warm)
    up_bytes = sum(r["model_context"]["bytes"] for r in up_warm)
    base_work = sum(r["repeated_validation_executed"] for r in base_warm)
    up_work = sum(r["repeated_validation_executed"] for r in up_warm)
    base_time = sum(r["wall_clock_s"] for r in base_warm)
    up_time = sum(r["wall_clock_s"] for r in up_warm)
    trace_cfg = json.loads((WORKTREE / "config/bbma_traceability.json").read_text(encoding="utf-8"))
    f6 = trace_cfg["rules"]["CORE-V2-F6"]
    regression = json.loads((WORKTREE / "config/bbma_regression_map.json").read_text(encoding="utf-8"))
    selected = by[("strategy_f6_readonly", "upgraded", "cold")].get("selected_tests", [])
    all_drivers = sorted(regression["tests"].keys())
    return {"warm_context": {"baseline_bytes": base_bytes, "upgraded_bytes": up_bytes,
                              "reduction": reduction(base_bytes, up_bytes)},
            "warm_repeated_work": {"baseline_validations": base_work, "upgraded_validations": up_work,
                                    "reduction": reduction(base_work, up_work)},
            "warm_wall_clock": {"baseline_s": round(base_time, 6), "upgraded_s": round(up_time, 6),
                                 "reduction": reduction(base_time, up_time)},
            "strategy_f6": {"status": f6["status"], "runtime": f6["stages"]["runtime"]["status"],
                            "selected_tests": selected, "all_verified_test_drivers": all_drivers,
                            "selection_reduction": reduction(len(all_drivers), len(selected))}}
def authority_state() -> dict:
    def gout(*args: str) -> str:
        return subprocess.check_output(["git", "-C", str(WORKTREE), *args], text=True).strip()
    return {"tooling_head": gout("rev-parse", "HEAD"),
            "tooling_origin": gout("rev-parse", "origin/chore/autonomous-engineering-infra-150"),
            "d1_owner": gout("rev-parse", "origin/d1-owner-dev"),
            "tracked_status": gout("status", "--porcelain", "--untracked-files=no")}

def acceptance(measure: dict, runs: list[dict], auth: dict) -> dict:
    cold_ok = all(r["validation_status"] == "PASS" for r in runs if r["iteration"] == "cold")
    warm_ok = all(r["validation_status"] in {"PASS", "REUSED_PASS"} for r in runs if r["iteration"] == "warm")
    source_ok = auth["tooling_head"] == TOOLING_COMMIT and auth["tooling_origin"] == TOOLING_COMMIT and auth["d1_owner"] == D1_COMMIT
    runtime_preserved = measure["strategy_f6"]["runtime"] == "NOT VERIFIED"
    no_tracked_change = auth["tracked_status"] == ""
    return {
        "warm_context_reduction_ge_30pct": measure["warm_context"]["reduction"] >= 0.30,
        "repeated_work_reduction_ge_20pct": measure["warm_repeated_work"]["reduction"] >= 0.20,
        "no_source_authority_regression": source_ok,
        "no_validation_gate_bypass": cold_ok and warm_ok and runtime_preserved,
        "no_strategy_runtime_promotion": runtime_preserved,
        "no_strategy_or_runtime_ownership_duplication": no_tracked_change,
        "all_required_task_classes_present": len({r["task"] for r in runs}) == 3,
    }

def write_report(results: dict) -> Path:
    m, a = results["measurements"], results["acceptance"]
    lines = ["# AUTONOMY-EFF-AB #154 Benchmark Report", "", f"Tooling head: `{TOOLING_COMMIT}`", f"D1 authority: `{D1_COMMIT}`", "",
             "## Warm-run efficiency", f"- Context bytes: {m['warm_context']['baseline_bytes']} -> {m['warm_context']['upgraded_bytes']} ({m['warm_context']['reduction']:.2%} reduction)",
             f"- Repeated validations: {m['warm_repeated_work']['baseline_validations']} -> {m['warm_repeated_work']['upgraded_validations']} ({m['warm_repeated_work']['reduction']:.2%} reduction)",
             f"- Wall clock: {m['warm_wall_clock']['baseline_s']:.3f}s -> {m['warm_wall_clock']['upgraded_s']:.3f}s ({m['warm_wall_clock']['reduction']:.2%} reduction)", ""]
    lines += ["## Required task classes"]
    for task in sorted({r["task"] for r in results["runs"]}):
        b = next(r for r in results["runs"] if r["task"] == task and r["mode"] == "baseline" and r["iteration"] == "warm")
        u = next(r for r in results["runs"] if r["task"] == task and r["mode"] == "upgraded" and r["iteration"] == "warm")
        lines.append(f"- `{task}`: context {b['model_context']['bytes']} -> {u['model_context']['bytes']} bytes; route `{u['model_route']}`; validation `{u['validation_status']}`")
    lines += ["", "## Strategy-Core safety", f"- CORE-V2-F6 overall: `{m['strategy_f6']['status']}`.",
              f"- Runtime remains: `{m['strategy_f6']['runtime']}` (not promoted by this benchmark).",
              f"- Targeted verified-map selection: {m['strategy_f6']['selected_tests']} from {m['strategy_f6']['all_verified_test_drivers']}.",
              "- Selected test drivers are measurement output only; this read-only benchmark does not claim they were executed as new Core acceptance.", "",
              "## Acceptance"]
    for key, value in a.items(): lines.append(f"- {key}: {'PASS' if value else 'FAIL'}")
    lines += ["", "Fixture preparation (authority snapshots/raw telemetry export) is excluded from timed runs and is hash-recorded in the evidence package."]
    path = OUT / "benchmark_report.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path

def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    prep = prepare_inputs()
    tasks = task_definitions(prep)
    protocol = {"schema_version": 1, "issue": 154, "tooling_commit": TOOLING_COMMIT,
                "d1_authority_commit": D1_COMMIT, "python": str(PYTHON),
                "iterations": ["cold", "warm"], "task_classes": list(tasks),
                "measurement_mapping": {"source_context_usage": "model-facing payload bytes/lines/artifact count",
                                        "cache_hit_miss": "content-addressed destination existed before put",
                                        "repeated_work_avoided": "digest+authority matched prior PASS so repeated validation command was skipped",
                                        "wall_clock": "task workflow time excluding fixture materialization"}}
    jwrite(OUT / "benchmark_protocol.json", protocol)
    cache_root = OUT / "cache"
    reuse_db = OUT / "reuse.db"
    if cache_root.exists(): shutil.rmtree(cache_root)
    if reuse_db.exists(): reuse_db.unlink()
    store = ContentAddressedStore(cache_root)
    runs: list[dict] = []
    cold_pass: dict[str, bool] = {}
    with EvidenceDB(reuse_db) as db:
        for task, cfg in tasks.items():
            runs.append(baseline_run(task, cfg, "cold"))
            runs.append(baseline_run(task, cfg, "warm"))
            runs.append(upgraded_run(task, cfg, "cold", prep, store, db, cold_pass))
            runs.append(upgraded_run(task, cfg, "warm", prep, store, db, cold_pass))
    measurements = evaluate(runs, tasks)
    auth = authority_state()
    results = {"protocol": protocol, "runs": runs, "measurements": measurements,
               "authority_state": auth, "acceptance": acceptance(measurements, runs, auth),
               "telemetry_summary": prep["telemetry_summary_obj"]}
    jwrite(OUT / "benchmark_results.json", results)
    report = write_report(results)
    authority_manifest = {"d1_commit": D1_COMMIT, "files": [file_record(p) for p in prep["strategy_files"]],
                          "telemetry_db": file_record(TELEMETRY_DB)}
    jwrite(OUT / "authority_manifest.json", authority_manifest)
    files = [Path(__file__), TASK_ROOT / "ACTIVE_TASK.json"]
    files += [p for p in OUT.rglob("*") if p.is_file() and "cache" not in p.parts and p.name not in {"evidence_package.json", "evidence_package.sha256"}]
    package_path = OUT / "evidence_package.json"
    build_evidence_package(package_path, files, metadata={"issue": 154, "label": "AUTONOMY-EFF-AB"})
    (OUT / "evidence_package.sha256").write_text(sha256_file(package_path) + "\n", encoding="ascii")
    print(json.dumps({"acceptance": results["acceptance"], "measurements": measurements,
                      "report": str(report), "evidence_package": str(package_path),
                      "evidence_package_sha256": sha256_file(package_path)}, indent=2))
    return 0 if all(results["acceptance"].values()) else 2

if __name__ == "__main__":
    raise SystemExit(main())
