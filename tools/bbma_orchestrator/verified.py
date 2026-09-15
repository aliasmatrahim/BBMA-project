from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


EXPECTED_MODULES = {f"M{i:02d}" for i in range(1, 28)} | {"M12N"}
APPROVED_ARCHITECTURE_INVARIANT_MODULES = frozenset({
    "M12N", "M13", "M14", "M15", "M18", "M19", "M22", "M27",
})
ALLOWED_STATUSES = {"VERIFIED", "NOT VERIFIED", "HOLD"}
COVERAGE_STATUSES = {
    "VERIFIED", "PARTIAL", "NOT VERIFIED", "HOLD", "UNRESOLVED", "SOURCE CONFLICT"
}
_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _validate_authority(authority: Any) -> tuple[str, str]:
    _require(isinstance(authority, dict), "authority must be an object")
    for field in ("repository", "branch", "commit"):
        _require(isinstance(authority.get(field), str) and authority[field].strip(),
                 f"authority {field} must be non-empty")
    _require(bool(_SHA_RE.fullmatch(authority["commit"])),
             "authority commit must be a 40-character lowercase SHA")
    return authority["repository"], authority["commit"]


def _validate_coverage(coverage: Any) -> None:
    _require(isinstance(coverage, dict), "coverage must be an object")
    for field, label in (
        ("module_identity", "module-identity"),
        ("consumer_edges", "consumer-edge"),
        ("tests", "test"),
    ):
        status = coverage.get(field)
        _require(status in COVERAGE_STATUSES,
                 f"{label} coverage status invalid: {status}")


def _validate_evidence_catalog(
    catalog: Any, authority_repository: str, authority_commit: str
) -> set[str]:
    _require(isinstance(catalog, dict) and catalog, "evidence_catalog must be non-empty")
    required = ("repository", "commit", "path", "blob_sha", "locator")
    for evidence_id, item in catalog.items():
        _require(isinstance(evidence_id, str) and evidence_id, "invalid evidence id")
        _require(isinstance(item, dict), f"evidence {evidence_id} must be an object")
        for field in required:
            _require(isinstance(item.get(field), str) and item[field],
                     f"evidence {evidence_id} missing {field}")
        _require(item["repository"] == authority_repository,
                 f"evidence {evidence_id} repository does not match authority")
        _require(item["commit"] == authority_commit,
                 f"evidence {evidence_id} commit does not match authority commit")
        _require(bool(_SHA_RE.fullmatch(item["commit"])),
                 f"evidence {evidence_id} commit must be a 40-character lowercase SHA")
        _require(bool(_SHA_RE.fullmatch(item["blob_sha"])),
                 f"evidence {evidence_id} blob_sha must be a 40-character lowercase SHA")
    return set(catalog)


def _validate_refs(refs: Any, known: set[str], label: str) -> None:
    _require(isinstance(refs, list) and refs, f"{label} must be non-empty")
    _require(all(isinstance(ref, str) for ref in refs), f"{label} must contain strings")
    missing = sorted(set(refs) - known)
    _require(not missing, f"{label} contains unknown evidence: {missing}")


def load_verified_module_graph(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        graph = json.load(handle)

    _require(isinstance(graph, dict), "graph must be an object")
    _require(graph.get("schema_version") == 1, "unsupported graph schema_version")
    authority_repository, authority_commit = _validate_authority(graph.get("authority"))
    _validate_coverage(graph.get("coverage"))
    known_unknowns = graph.get("known_unknowns")
    _require(isinstance(known_unknowns, list)
             and all(isinstance(item, str) and item.strip() for item in known_unknowns),
             "known_unknowns must be a list of non-empty strings")
    if any(status != "VERIFIED" for status in graph["coverage"].values()):
        _require(bool(known_unknowns),
                 "known_unknowns must explain non-VERIFIED coverage")

    known_evidence = _validate_evidence_catalog(
        graph.get("evidence_catalog"), authority_repository, authority_commit
    )
    modules = graph.get("modules")
    _require(isinstance(modules, dict), "modules must be an object")
    module_ids = set(modules)
    _require(module_ids == EXPECTED_MODULES,
             f"module set mismatch: missing={sorted(EXPECTED_MODULES - module_ids)} "
             f"extra={sorted(module_ids - EXPECTED_MODULES)}")
    for module_id, module in modules.items():
        _require(isinstance(module, dict), f"module {module_id} must be an object")
        _require(module.get("module_id") == module_id, f"module id mismatch for {module_id}")
        _require(module.get("status") in ALLOWED_STATUSES,
                 f"invalid status for {module_id}")
        if graph["coverage"]["module_identity"] == "VERIFIED":
            _require(module["status"] == "VERIFIED",
                     f"module-identity coverage contradicts {module_id} status")
        _require(isinstance(module.get("ownership"), str) and module["ownership"].strip(),
                 f"missing ownership for {module_id}")
        _validate_refs(module.get("evidence"), known_evidence,
                       f"module evidence for {module_id}")

        consumers = module.get("consumers")
        _require(isinstance(consumers, list), f"consumers for {module_id} must be a list")
        seen: set[str] = set()
        for consumer in consumers:
            _require(isinstance(consumer, dict),
                     f"consumer edge for {module_id} must be an object")
            target = consumer.get("module")
            _require(target in module_ids, f"unknown consumer {target} from {module_id}")
            _require(target != module_id, f"self consumer edge for {module_id}")
            _require(target not in seen, f"duplicate consumer {target} from {module_id}")
            seen.add(target)
            _require(isinstance(consumer.get("relationship"), str)
                     and consumer["relationship"].strip(),
                     f"missing relationship for {module_id}->{target}")
            _validate_refs(consumer.get("evidence"), known_evidence,
                           f"consumer evidence for {module_id}->{target}")

    return graph


TRACE_STAGES = (
    "source_evidence",
    "core_rule",
    "contract",
    "module",
    "code",
    "test",
    "runtime",
)
TRACE_STATUSES = {
    "VERIFIED", "PARTIAL", "NOT VERIFIED", "HOLD", "UNRESOLVED", "SOURCE CONFLICT"
}
TRACE_EVIDENCE_KINDS = {"source", "core_rule", "contract", "code", "test", "runtime"}
TRACE_STAGE_KIND = {
    "source_evidence": "source",
    "core_rule": "core_rule",
    "contract": "contract",
    "code": "code",
    "test": "test",
    "runtime": "runtime",
}
TRACE_CORE_RULE_IDS = {f"CORE-V2-F{i}" for i in range(1, 7)}


def _validate_trace_catalog(
    catalog: Any, authority_repository: str, authority_commit: str
) -> set[str]:
    known = _validate_evidence_catalog(catalog, authority_repository, authority_commit)
    for evidence_id, item in catalog.items():
        _require(item.get("kind") in TRACE_EVIDENCE_KINDS,
                 f"trace evidence {evidence_id} has invalid kind")
    return known


def _verify_git_evidence_catalog(
    catalog: dict[str, Any], authority_commit: str, repository_hint: str | Path
) -> None:
    hint = Path(repository_hint).resolve().parent
    root_result = subprocess.run(
        ["git", "-C", str(hint), "rev-parse", "--show-toplevel"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    _require(
        root_result.returncode == 0,
        "unable to locate Git repository for traceability evidence",
    )
    repository_root = root_result.stdout.decode("utf-8", errors="replace").strip()
    tree_result = subprocess.run(
        ["git", "-C", repository_root, "ls-tree", "-r", "-z", "--full-tree", authority_commit],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    _require(
        tree_result.returncode == 0,
        f"unable to resolve traceability authority commit {authority_commit}",
    )
    blobs: dict[str, str] = {}
    for raw_entry in tree_result.stdout.split(b"\0"):
        if not raw_entry:
            continue
        metadata, raw_path = raw_entry.split(b"\t", 1)
        _mode, object_type, object_sha = metadata.decode("ascii").split()
        if object_type == "blob":
            blobs[raw_path.decode("utf-8", errors="surrogateescape")] = object_sha
    for evidence_id, item in catalog.items():
        actual = blobs.get(item["path"])
        _require(
            actual is not None,
            f"evidence {evidence_id} path missing at authority commit: {item['path']}",
        )
        _require(
            actual == item["blob_sha"],
            f"evidence {evidence_id} blob mismatch: "
            f"expected={item['blob_sha']} actual={actual}",
        )


def load_verified_traceability(
    path: str | Path, module_graph_path: str | Path
) -> dict[str, Any]:
    module_graph = load_verified_module_graph(module_graph_path)
    with Path(path).open("r", encoding="utf-8") as handle:
        traceability = json.load(handle)

    _require(isinstance(traceability, dict), "traceability must be an object")
    _require(traceability.get("schema_version") == 1,
             "unsupported traceability schema_version")
    authority_repository, authority_commit = _validate_authority(
        traceability.get("authority")
    )
    _require(traceability["authority"] == module_graph["authority"],
             "traceability authority must match module graph authority")
    coverage = traceability.get("coverage")
    _require(isinstance(coverage, dict) and set(coverage) == set(TRACE_STAGES),
             "traceability coverage must contain every stage")
    for stage, status in coverage.items():
        _require(status in TRACE_STATUSES,
                 f"traceability coverage status invalid for {stage}")
    known_unknowns = traceability.get("known_unknowns")
    _require(isinstance(known_unknowns, list)
             and all(isinstance(item, str) and item.strip() for item in known_unknowns),
             "traceability known_unknowns must be non-empty strings")
    if any(status != "VERIFIED" for status in coverage.values()):
        _require(bool(known_unknowns),
                 "known_unknowns must explain non-VERIFIED traceability coverage")
    known_evidence = _validate_trace_catalog(
        traceability.get("evidence_catalog"), authority_repository, authority_commit
    )
    _verify_git_evidence_catalog(
        traceability["evidence_catalog"], authority_commit, module_graph_path
    )
    rules = traceability.get("rules")
    _require(isinstance(rules, dict) and rules, "traceability rules must be non-empty")
    rule_ids = set(rules)
    _require(
        rule_ids == TRACE_CORE_RULE_IDS,
        f"traceability rule set mismatch: missing={sorted(TRACE_CORE_RULE_IDS - rule_ids)} "
        f"extra={sorted(rule_ids - TRACE_CORE_RULE_IDS)}",
    )
    for rule_id, rule in rules.items():
        _require(isinstance(rule, dict), f"rule {rule_id} must be an object")
        _require(isinstance(rule.get("title"), str) and rule["title"].strip(),
                 f"rule {rule_id} title must be non-empty")
        _require(rule.get("status") in TRACE_STATUSES,
                 f"rule {rule_id} status is invalid")
        stages = rule.get("stages")
        _require(isinstance(stages, dict) and set(stages) == set(TRACE_STAGES),
                 f"rule {rule_id} must contain every traceability stage")
        for stage_name in TRACE_STAGES:
            stage = stages[stage_name]
            _require(isinstance(stage, dict),
                     f"rule {rule_id} stage {stage_name} must be an object")
            status = stage.get("status")
            _require(status in TRACE_STATUSES,
                     f"rule {rule_id} stage {stage_name} status is invalid")
            refs = stage.get("evidence")
            _require(isinstance(refs, list)
                     and all(isinstance(ref, str) for ref in refs),
                     f"rule {rule_id} stage {stage_name} evidence must be a list")
            _require(len(refs) == len(set(refs)),
                     f"rule {rule_id} stage {stage_name} has duplicate evidence")
            missing = sorted(set(refs) - known_evidence)
            _require(not missing,
                     f"rule {rule_id} stage {stage_name} has unknown evidence: {missing}")
            expected_kind = TRACE_STAGE_KIND.get(stage_name)
            if expected_kind:
                wrong = [ref for ref in refs
                         if traceability["evidence_catalog"][ref]["kind"] != expected_kind]
                _require(not wrong,
                         f"rule {rule_id} stage {stage_name} evidence kind mismatch: {wrong}")
            if stage_name == "module":
                modules = stage.get("modules")
                _require(isinstance(modules, list) and modules,
                         f"rule {rule_id} module stage must name modules")
                unknown_modules = sorted(set(modules) - set(module_graph["modules"]))
                _require(not unknown_modules,
                         f"rule {rule_id} has unknown modules: {unknown_modules}")
                if status == "VERIFIED":
                    unverified = [module for module in modules
                                  if module_graph["modules"][module]["status"] != "VERIFIED"]
                    _require(not unverified,
                             f"rule {rule_id} cites unverified modules: {unverified}")
            elif status == "VERIFIED":
                _require(bool(refs),
                         f"rule {rule_id} verified {stage_name} stage needs evidence")
            if status != "VERIFIED":
                _require(isinstance(stage.get("gap"), str) and stage["gap"].strip(),
                         f"rule {rule_id} non-VERIFIED {stage_name} stage needs a gap")
        if rule["status"] == "VERIFIED":
            _require(all(stage["status"] == "VERIFIED" for stage in stages.values()),
                     f"rule {rule_id} cannot be VERIFIED with incomplete stages")
    return traceability


REGRESSION_COVERAGE_FIELDS = {
    "module_identity",
    "consumer_edges",
    "test_assignments",
    "mandatory_global",
}


def load_verified_regression_map(
    path: str | Path,
    module_graph_path: str | Path,
    traceability_path: str | Path,
) -> dict[str, Any]:
    module_graph = load_verified_module_graph(module_graph_path)
    traceability = load_verified_traceability(traceability_path, module_graph_path)
    with Path(path).open("r", encoding="utf-8") as handle:
        regression_map = json.load(handle)

    _require(isinstance(regression_map, dict), "regression map must be an object")
    _require(regression_map.get("schema_version") == 1,
             "unsupported regression map schema_version")
    _validate_authority(regression_map.get("authority"))
    _require(regression_map["authority"] == module_graph["authority"],
             "regression map authority must match module graph authority")
    _require(regression_map["authority"] == traceability["authority"],
             "regression map authority must match traceability authority")

    coverage = regression_map.get("coverage")
    _require(isinstance(coverage, dict)
             and set(coverage) == REGRESSION_COVERAGE_FIELDS,
             "regression coverage fields mismatch")
    for field, status in coverage.items():
        _require(status in TRACE_STATUSES,
                 f"regression coverage status invalid for {field}")
    _require(coverage["module_identity"] == module_graph["coverage"]["module_identity"],
             "regression module coverage must match module graph")
    _require(coverage["consumer_edges"] == module_graph["coverage"]["consumer_edges"],
             "regression consumer coverage must match module graph")

    known_unknowns = regression_map.get("known_unknowns")
    _require(isinstance(known_unknowns, list)
             and all(isinstance(item, str) and item.strip() for item in known_unknowns),
             "regression known_unknowns must be non-empty strings")
    if any(status != "VERIFIED" for status in coverage.values()):
        _require(bool(known_unknowns),
                 "known_unknowns must explain incomplete regression coverage")

    mandatory_global = regression_map.get("mandatory_global")
    _require(isinstance(mandatory_global, list)
             and all(isinstance(item, str) for item in mandatory_global),
             "mandatory_global must be a list of strings")
    _require(len(mandatory_global) == len(set(mandatory_global)),
             "mandatory_global has duplicates")
    _require(coverage["mandatory_global"] == "NOT VERIFIED"
             and not mandatory_global,
             "mandatory global regression requires verified authority")

    tests = regression_map.get("tests")
    _require(isinstance(tests, dict) and tests,
             "regression tests must be a non-empty object")
    verified_rule_ids = {
        rule_id
        for rule_id, rule in traceability["rules"].items()
        if rule["stages"]["test"]["status"] == "VERIFIED"
    }
    mapped_rule_ids: set[str] = set()
    for test_id, item in tests.items():
        _require(isinstance(item, dict), f"regression test {test_id} must be an object")
        _require(item.get("status") == "VERIFIED",
                 f"regression test {test_id} must be VERIFIED")
        rule_id = item.get("core_rule_id")
        _require(rule_id in verified_rule_ids,
                 f"regression test {test_id} has no VERIFIED traceability test stage")
        _require(rule_id not in mapped_rule_ids,
                 f"duplicate regression mapping for {rule_id}")
        mapped_rule_ids.add(rule_id)
        refs = item.get("evidence")
        expected_refs = traceability["rules"][rule_id]["stages"]["test"]["evidence"]
        _require(refs == expected_refs,
                 f"regression test {test_id} evidence mismatch for {rule_id}")
        _require(test_id in refs,
                 f"regression test {test_id} must identify its verified driver evidence")
        driver = traceability["evidence_catalog"].get(test_id, {})
        _require(driver.get("kind") == "test"
                 and driver.get("path", "").startswith(".github/workflows/"),
                 f"regression test {test_id} driver is not an attributable workflow")
    _require(mapped_rule_ids == verified_rule_ids,
             f"regression rule coverage mismatch: "
             f"missing={sorted(verified_rule_ids - mapped_rule_ids)} "
             f"extra={sorted(mapped_rule_ids - verified_rule_ids)}")
    expected_test_coverage = (
        "VERIFIED" if verified_rule_ids == set(traceability["rules"]) else "PARTIAL"
    )
    _require(coverage["test_assignments"] == expected_test_coverage,
             "regression test-assignment coverage mismatch")

    modules = regression_map.get("modules")
    _require(isinstance(modules, dict), "regression modules must be an object")
    module_ids = set(modules)
    _require(module_ids == set(module_graph["modules"]),
             f"regression module set mismatch: "
             f"missing={sorted(set(module_graph['modules']) - module_ids)} "
             f"extra={sorted(module_ids - set(module_graph['modules']))}")
    assignments = {test_id: set() for test_id in tests}
    for module_id, item in modules.items():
        _require(isinstance(item, dict) and set(item) == {"tests", "consumers"},
                 f"regression module {module_id} fields mismatch")
        consumers = item["consumers"]
        module_tests = item["tests"]
        _require(isinstance(consumers, list)
                 and all(isinstance(consumer, str) for consumer in consumers),
                 f"regression consumers for {module_id} must be strings")
        _require(len(consumers) == len(set(consumers)),
                 f"regression consumers for {module_id} have duplicates")
        expected_consumers = [
            edge["module"] for edge in module_graph["modules"][module_id]["consumers"]
        ]
        _require(consumers == expected_consumers,
                 f"regression consumer set mismatch for {module_id}")
        _require(isinstance(module_tests, list)
                 and all(isinstance(test_id, str) for test_id in module_tests),
                 f"regression tests for {module_id} must be strings")
        _require(len(module_tests) == len(set(module_tests)),
                 f"regression tests for {module_id} have duplicates")
        unknown_tests = sorted(set(module_tests) - set(tests))
        _require(not unknown_tests,
                 f"regression module {module_id} has unknown tests: {unknown_tests}")
        for test_id in module_tests:
            assignments[test_id].add(module_id)

    for test_id, item in tests.items():
        rule_id = item["core_rule_id"]
        expected_modules = set(
            traceability["rules"][rule_id]["stages"]["module"]["modules"]
        )
        _require(assignments[test_id] == expected_modules,
                 f"regression assignment mismatch for {test_id}: "
                 f"expected={sorted(expected_modules)} actual={sorted(assignments[test_id])}")
    return regression_map


def materialize_traceability(
    traceability_path: str | Path,
    module_graph_path: str | Path,
    db_path: str | Path,
) -> dict[str, int]:
    from .evidence import EvidenceDB

    traceability = load_verified_traceability(traceability_path, module_graph_path)
    status_map = {
        "VERIFIED": "VALID",
        "PARTIAL": "NOT VERIFIED",
        "NOT VERIFIED": "NOT VERIFIED",
        "HOLD": "HOLD",
        "UNRESOLVED": "HOLD",
        "SOURCE CONFLICT": "HOLD",
    }
    node_count = 0
    edge_count = 0
    with EvidenceDB(db_path) as db:
        for rule_id in sorted(traceability["rules"]):
            stages = traceability["rules"][rule_id]["stages"]
            node_ids: list[str] = []
            for stage_name in TRACE_STAGES:
                stage = stages[stage_name]
                node_id = f"trace:{rule_id}:{stage_name}"
                evidence_records = [
                    {"evidence_id": ref, **traceability["evidence_catalog"][ref]}
                    for ref in stage["evidence"]
                ]
                payload = json.dumps(
                    {"stage": stage, "evidence_records": evidence_records},
                    sort_keys=True,
                    separators=(",", ":"),
                )
                digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
                metadata = {
                    "rule_id": rule_id,
                    "stage": stage_name,
                    "evidence": stage["evidence"],
                    "evidence_records": evidence_records,
                }
                if stage_name == "module":
                    metadata["modules"] = stage["modules"]
                if "gap" in stage:
                    metadata["gap"] = stage["gap"]
                db.add_node(
                    node_id,
                    "module" if stage_name == "module" else TRACE_STAGE_KIND[stage_name],
                    digest,
                    status=status_map[stage["status"]],
                    metadata=metadata,
                )
                node_ids.append(node_id)
                node_count += 1
            for source, target in zip(node_ids, node_ids[1:]):
                db.add_edge(source, target)
                edge_count += 1
    return {
        "rules": len(traceability["rules"]),
        "nodes": node_count,
        "edges": edge_count,
    }


ARCHITECTURE_COVERAGE_FIELDS = {
    "ownership_boundaries",
    "runtime_enforcement",
}


def validate_architecture_invariants(
    catalog: dict[str, Any], module_graph: dict[str, Any]
) -> dict[str, Any]:
    _require(isinstance(catalog, dict), "architecture catalog must be an object")
    _require(
        set(catalog) == {
            "schema_version", "authority", "coverage", "invariants",
            "known_unknowns",
        },
        "architecture catalog fields mismatch",
    )
    _require(
        catalog["schema_version"] == 1,
        "unsupported architecture catalog schema_version",
    )
    _validate_authority(catalog["authority"])
    _require(
        isinstance(module_graph, dict)
        and catalog["authority"] == module_graph.get("authority"),
        "architecture authority must match module graph authority",
    )
    coverage = catalog["coverage"]
    _require(
        isinstance(coverage, dict)
        and set(coverage) == ARCHITECTURE_COVERAGE_FIELDS,
        "architecture coverage fields mismatch",
    )
    _require(
        coverage["ownership_boundaries"] == "VERIFIED",
        "ownership-boundary catalog must be VERIFIED",
    )
    _require(
        coverage["runtime_enforcement"] == "NOT VERIFIED",
        "runtime enforcement must remain NOT VERIFIED",
    )
    known_unknowns = catalog["known_unknowns"]
    _require(
        isinstance(known_unknowns, list)
        and bool(known_unknowns)
        and all(isinstance(item, str) and item.strip() for item in known_unknowns),
        "architecture known_unknowns must be non-empty strings",
    )
    invariants = catalog["invariants"]
    modules = module_graph.get("modules")
    evidence_catalog = module_graph.get("evidence_catalog")
    _require(isinstance(invariants, dict) and invariants,
             "architecture invariants must be non-empty")
    _require(isinstance(modules, dict), "module graph modules must be an object")
    _require(
        isinstance(evidence_catalog, dict),
        "module graph evidence_catalog must be an object",
    )
    seen_modules: set[str] = set()
    for invariant_id, item in invariants.items():
        _require(
            isinstance(invariant_id, str) and invariant_id.startswith("ARCH-"),
            "invalid architecture invariant id",
        )
        _require(
            isinstance(item, dict)
            and set(item) == {"module", "ownership", "evidence"},
            f"architecture invariant {invariant_id} fields mismatch",
        )
        module_id = item["module"]
        _require(module_id in modules,
                 f"architecture invariant {invariant_id} has unknown module")
        _require(module_id not in seen_modules,
                 f"duplicate architecture boundary for {module_id}")
        _require(invariant_id.startswith(f"ARCH-{module_id}-"),
                 f"architecture invariant id does not match {module_id}")
        module = modules[module_id]
        _require(module.get("status") == "VERIFIED",
                 f"architecture module {module_id} is not VERIFIED")
        _require(item["ownership"] == module.get("ownership"),
                 f"architecture ownership mismatch for {module_id}")
        _require(item["evidence"] == module.get("evidence"),
                 f"architecture evidence mismatch for {module_id}")
        contract_refs = [
            ref for ref in item["evidence"]
            if ref != "EA_HEADERS"
            and isinstance(evidence_catalog.get(ref), dict)
            and isinstance(evidence_catalog[ref].get("path"), str)
            and bool(re.fullmatch(
                r"blueprint/contracts/[^/]+\.md",
                evidence_catalog[ref]["path"],
            ))
        ]
        _require(
            bool(contract_refs),
            f"architecture boundary {module_id} lacks standalone contract evidence",
        )
        seen_modules.add(module_id)
    _require(
        seen_modules == APPROVED_ARCHITECTURE_INVARIANT_MODULES,
        "approved architecture invariant module set mismatch",
    )
    return catalog


def load_verified_architecture_invariants(
    path: str | Path, module_graph_path: str | Path
) -> dict[str, Any]:
    module_graph = load_verified_module_graph(module_graph_path)
    _verify_git_evidence_catalog(
        module_graph["evidence_catalog"],
        module_graph["authority"]["commit"],
        module_graph_path,
    )
    with Path(path).open("r", encoding="utf-8") as handle:
        catalog = json.load(handle)
    return validate_architecture_invariants(catalog, module_graph)


def architecture_invariant_mutation_check(
    path: str | Path, module_graph_path: str | Path
) -> dict[str, int]:
    catalog = load_verified_architecture_invariants(path, module_graph_path)
    module_graph = load_verified_module_graph(module_graph_path)
    detected = 0
    for item in catalog["invariants"].values():
        mutated = json.loads(json.dumps(module_graph))
        module_id = item["module"]
        mutated["modules"][module_id]["ownership"] += " [MUTATED]"
        try:
            validate_architecture_invariants(catalog, mutated)
        except ValueError:
            detected += 1
    mutation_count = len(catalog["invariants"])
    _require(detected == mutation_count,
             "architecture mutation self-check did not detect every mutation")
    return {"mutations": mutation_count, "detected": detected}
