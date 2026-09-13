from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


EXPECTED_MODULES = {f"M{i:02d}" for i in range(1, 28)} | {"M12N"}
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
