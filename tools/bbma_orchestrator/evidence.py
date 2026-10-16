from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
import hashlib
import json
import os
import shutil
import sqlite3

from .core import atomic_write_json, utc_now

VALID_NODE_KINDS = {
    "source",
    "core_rule",
    "contract",
    "module",
    "code",
    "test",
    "compile",
    "runtime",
    "build",
    "artifact",
    "decision",
    "queue",
    "report",
}
VALID_NODE_STATUS = {"VALID", "STALE", "NOT VERIFIED", "HOLD", "FAIL"}

def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

@dataclass(frozen=True)
class ArtifactRecord:
    digest: str
    path: str
    size: int
    reviewed_status: str
    authority_fingerprint: str
    metadata: dict[str, Any]

class EvidenceDB:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._init_schema()

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> "EvidenceDB":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def _init_schema(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS artifacts (
                digest TEXT PRIMARY KEY,
                path TEXT NOT NULL,
                size INTEGER NOT NULL,
                reviewed_status TEXT NOT NULL,
                authority_fingerprint TEXT NOT NULL,
                metadata_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS nodes (
                node_id TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                digest TEXT NOT NULL,
                status TEXT NOT NULL,
                metadata_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS edges (
                src TEXT NOT NULL,
                dst TEXT NOT NULL,
                PRIMARY KEY (src, dst),
                FOREIGN KEY (src) REFERENCES nodes(node_id) ON DELETE CASCADE,
                FOREIGN KEY (dst) REFERENCES nodes(node_id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS experiment_runs (
                run_id TEXT PRIMARY KEY,
                manifest_sha256 TEXT NOT NULL,
                fingerprint TEXT NOT NULL,
                hypothesis_id TEXT NOT NULL,
                build_id TEXT NOT NULL,
                dataset_sha256 TEXT NOT NULL,
                parameter_sha256 TEXT NOT NULL,
                run_status TEXT NOT NULL,
                hypothesis_result TEXT NOT NULL,
                parent_run_id TEXT,
                metadata_json TEXT NOT NULL,
                registered_at TEXT NOT NULL,
                FOREIGN KEY (parent_run_id) REFERENCES experiment_runs(run_id)
            );
            CREATE INDEX IF NOT EXISTS idx_experiment_runs_fingerprint
                ON experiment_runs(fingerprint);
            """
        )
        self.conn.commit()

    def register_experiment(
        self,
        manifest: dict[str, Any],
        manifest_path: str | Path,
        evidence_root: str | Path,
        *,
        run_status: str,
        hypothesis_result: str = "NOT_EVALUATED",
    ) -> dict[str, Any]:
        """Register a validated run in the existing evidence DAG without granting runtime authority."""
        if not isinstance(manifest, dict):
            raise ValueError("manifest must be an object")
        run_id = manifest.get("run_id")
        if not isinstance(run_id, str) or not run_id.strip():
            raise ValueError("run_id is required")
        if run_status not in {"INVALID_RUN", "RUN_FAILED", "VALIDATION_FAILED", "EVIDENCE_ACCEPTED"}:
            raise ValueError("invalid experiment run status")
        if hypothesis_result not in {"NOT_EVALUATED", "SUPPORTED", "NOT_SUPPORTED", "INCONCLUSIVE"}:
            raise ValueError("invalid hypothesis result")
        hypothesis = manifest.get("hypothesis", {})
        build = manifest.get("build", {})
        dataset = manifest.get("dataset", {})
        costs = manifest.get("costs", {})
        environment = manifest.get("environment", {})
        protocol = manifest.get("protocol", {})
        if not all(isinstance(value, dict) for value in (hypothesis, build, dataset, costs, environment, protocol)):
            raise ValueError("manifest identity sections must be objects")
        manifest_file = Path(manifest_path).resolve()
        root = Path(evidence_root).resolve()
        if not manifest_file.is_file():
            raise FileNotFoundError(manifest_file)
        manifest_digest = sha256_file(manifest_file)
        try:
            manifest_on_disk = json.loads(manifest_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("manifest file must be valid UTF-8 JSON") from exc
        if manifest_on_disk != manifest:
            raise ValueError("manifest object does not match manifest file bytes")
        fingerprint_payload = {
            "hypothesis_id": hypothesis.get("id"),
            "parameter_sha256": hypothesis.get("parameter_sha256"),
            "build_id": build.get("build_id"),
            "source_commit": build.get("source_commit"),
            "source_sha256": build.get("source_sha256"),
            "ex4_sha256": build.get("ex4_sha256"),
            "set_sha256": build.get("set_sha256"),
            "dataset_sha256": dataset.get("sha256"),
            "symbol": dataset.get("symbol"),
            "timeframe": dataset.get("timeframe"),
            "environment": environment,
            "costs": costs,
            "partition": protocol.get("partition"),
        }
        fingerprint = hashlib.sha256(json.dumps(fingerprint_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
        parent_run_id = manifest.get("parent_run_id")
        artifacts = manifest.get("artifacts")
        if not isinstance(artifacts, list) or not artifacts:
            raise ValueError("manifest artifacts must be a non-empty list")
        resolved_artifacts: list[tuple[str, str, Path, int]] = []
        artifact_errors: list[str] = []
        seen_kinds: set[str] = set()
        for item in artifacts:
            if not isinstance(item, dict) or not isinstance(item.get("kind"), str) or not isinstance(item.get("path"), str):
                raise ValueError("invalid artifact record")
            kind = item["kind"]
            if kind in seen_kinds:
                raise ValueError(f"duplicate artifact kind: {kind}")
            seen_kinds.add(kind)
            path = (root / item["path"]).resolve()
            if path != root and root not in path.parents:
                artifact_errors.append(f"artifact path escapes evidence root: {kind}")
                continue
            if not path.is_file():
                artifact_errors.append(f"artifact missing: {kind}")
                continue
            digest = sha256_file(path)
            if digest.lower() != str(item.get("sha256", "")).lower():
                artifact_errors.append(f"artifact hash mismatch: {kind}")
                continue
            resolved_artifacts.append((kind, digest, path, path.stat().st_size))

        existing = self.conn.execute(
            "SELECT manifest_sha256,fingerprint,run_status,hypothesis_result FROM experiment_runs WHERE run_id=?",
            (run_id,),
        ).fetchone()
        if existing:
            if existing[0] != manifest_digest:
                raise ValueError(f"run_id collision: {run_id} already belongs to a different manifest")
            if existing[2] == "EVIDENCE_ACCEPTED" and artifact_errors:
                raise ValueError("registered evidence drift: " + "; ".join(artifact_errors))
            return {"run_id": run_id, "created": False, "manifest_sha256": manifest_digest,
                    "fingerprint": existing[1], "run_status": existing[2],
                    "hypothesis_result": existing[3], "lineage_node": f"experiment:{run_id}",
                    "artifact_errors": artifact_errors}
        if run_status == "EVIDENCE_ACCEPTED" and artifact_errors:
            raise ValueError("cannot accept evidence with artifact errors: " + "; ".join(artifact_errors))
        if parent_run_id:
            parent = self.conn.execute("SELECT 1 FROM experiment_runs WHERE run_id=?", (parent_run_id,)).fetchone()
            if parent is None:
                raise KeyError(f"parent experiment not registered: {parent_run_id}")

        now = utc_now()
        metadata = {
            "hypothesis_id": hypothesis.get("id"),
            "build_id": build.get("build_id"),
            "dataset_id": dataset.get("dataset_id"),
            "dataset_sha256": dataset.get("sha256"),
            "parameter_sha256": hypothesis.get("parameter_sha256"),
            "partition": protocol.get("partition"),
            "evidence_only": True,
            "trade_authority": "NONE",
            "artifact_errors": artifact_errors,
        }
        run_node = f"experiment:{run_id}"
        try:
            self.conn.execute("BEGIN IMMEDIATE")
            self.conn.execute(
                """INSERT INTO experiment_runs
                (run_id,manifest_sha256,fingerprint,hypothesis_id,build_id,dataset_sha256,
                 parameter_sha256,run_status,hypothesis_result,parent_run_id,metadata_json,registered_at)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                (run_id, manifest_digest, fingerprint, str(hypothesis.get("id", "")),
                 str(build.get("build_id", "")), str(dataset.get("sha256", "")),
                 str(hypothesis.get("parameter_sha256", "")), run_status, hypothesis_result,
                 parent_run_id, json.dumps(metadata, sort_keys=True), now),
            )
            self.conn.execute(
                "INSERT INTO nodes(node_id,kind,digest,status,metadata_json,updated_at) VALUES(?,?,?,?,?,?)",
                (run_node, "report", manifest_digest, "NOT VERIFIED",
                 json.dumps({**metadata, "run_status": run_status, "hypothesis_result": hypothesis_result}, sort_keys=True), now),
            )
            for kind, digest, path, size in resolved_artifacts:
                artifact_node = f"experiment-artifact:{run_id}:{kind}"
                artifact_meta = {"run_id": run_id, "kind": kind, "path": str(path), "fingerprint": fingerprint}
                self.conn.execute(
                    """INSERT INTO artifacts(digest,path,size,reviewed_status,authority_fingerprint,metadata_json,updated_at)
                    VALUES(?,?,?,?,?,?,?) ON CONFLICT(digest) DO NOTHING""",
                    (digest, str(path), size, "NOT VERIFIED", fingerprint, json.dumps(artifact_meta, sort_keys=True), now),
                )
                self.conn.execute(
                    "INSERT INTO nodes(node_id,kind,digest,status,metadata_json,updated_at) VALUES(?,?,?,?,?,?)",
                    (artifact_node, "artifact", digest, "NOT VERIFIED", json.dumps(artifact_meta, sort_keys=True), now),
                )
                self.conn.execute("INSERT INTO edges(src,dst) VALUES(?,?)", (artifact_node, run_node))
            if parent_run_id:
                self.conn.execute("INSERT INTO edges(src,dst) VALUES(?,?)", (f"experiment:{parent_run_id}", run_node))
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        return {"run_id": run_id, "created": True, "manifest_sha256": manifest_digest,
                "fingerprint": fingerprint, "run_status": run_status,
                "hypothesis_result": hypothesis_result, "lineage_node": run_node,
                "artifact_nodes": [f"experiment-artifact:{run_id}:{kind}" for kind, _, _, _ in resolved_artifacts]}

    def find_experiment_runs(self, fingerprint: str) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            """SELECT run_id,manifest_sha256,fingerprint,hypothesis_id,build_id,dataset_sha256,
            parameter_sha256,run_status,hypothesis_result,parent_run_id,registered_at
            FROM experiment_runs WHERE fingerprint=? ORDER BY registered_at,run_id""",
            (fingerprint,),
        ).fetchall()
        keys = ("run_id", "manifest_sha256", "fingerprint", "hypothesis_id", "build_id",
                "dataset_sha256", "parameter_sha256", "run_status", "hypothesis_result",
                "parent_run_id", "registered_at")
        return [dict(zip(keys, row)) for row in rows]

    def get_experiment_run(self, run_id: str) -> dict[str, Any]:
        row = self.conn.execute(
            """SELECT run_id,manifest_sha256,fingerprint,hypothesis_id,build_id,dataset_sha256,
            parameter_sha256,run_status,hypothesis_result,parent_run_id,metadata_json,registered_at
            FROM experiment_runs WHERE run_id=?""",
            (run_id,),
        ).fetchone()
        if row is None:
            raise KeyError(run_id)
        return {
            "run_id": row[0], "manifest_sha256": row[1], "fingerprint": row[2],
            "hypothesis_id": row[3], "build_id": row[4], "dataset_sha256": row[5],
            "parameter_sha256": row[6], "run_status": row[7], "hypothesis_result": row[8],
            "parent_run_id": row[9], "metadata": json.loads(row[10]), "registered_at": row[11],
        }

    def record_artifact(
        self,
        path: str | Path,
        *,
        reviewed_status: str = "NOT VERIFIED",
        authority_fingerprint: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> ArtifactRecord:
        p = Path(path)
        digest = sha256_file(p)
        size = p.stat().st_size
        meta = metadata or {}
        self.conn.execute(
            """
            INSERT INTO artifacts(digest,path,size,reviewed_status,authority_fingerprint,metadata_json,updated_at)
            VALUES(?,?,?,?,?,?,?)
            ON CONFLICT(digest) DO UPDATE SET
                path=excluded.path,
                size=excluded.size,
                reviewed_status=excluded.reviewed_status,
                authority_fingerprint=excluded.authority_fingerprint,
                metadata_json=excluded.metadata_json,
                updated_at=excluded.updated_at
            """,
            (digest, str(p), size, reviewed_status, authority_fingerprint, json.dumps(meta, sort_keys=True), utc_now()),
        )
        self.conn.commit()
        return ArtifactRecord(digest, str(p), size, reviewed_status, authority_fingerprint, meta)

    def can_reuse(self, path: str | Path, authority_fingerprint: str) -> bool:
        digest = sha256_file(path)
        row = self.conn.execute(
            "SELECT reviewed_status,authority_fingerprint FROM artifacts WHERE digest=?",
            (digest,),
        ).fetchone()
        return bool(row and row[0] == "PASS" and row[1] == authority_fingerprint)

    def add_node(
        self,
        node_id: str,
        kind: str,
        digest: str,
        *,
        status: str = "NOT VERIFIED",
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if kind not in VALID_NODE_KINDS:
            raise ValueError(f"invalid evidence node kind: {kind}")
        if status not in VALID_NODE_STATUS:
            raise ValueError(f"invalid evidence node status: {status}")
        self.conn.execute(
            """
            INSERT INTO nodes(node_id,kind,digest,status,metadata_json,updated_at)
            VALUES(?,?,?,?,?,?)
            ON CONFLICT(node_id) DO UPDATE SET
                kind=excluded.kind,
                digest=excluded.digest,
                status=excluded.status,
                metadata_json=excluded.metadata_json,
                updated_at=excluded.updated_at
            """,
            (node_id, kind, digest, status, json.dumps(metadata or {}, sort_keys=True), utc_now()),
        )
        self.conn.commit()

    def add_edge(self, src: str, dst: str) -> None:
        missing = [
            node
            for node in (src, dst)
            if self.conn.execute("SELECT 1 FROM nodes WHERE node_id=?", (node,)).fetchone() is None
        ]
        if missing:
            raise KeyError(f"missing evidence nodes: {', '.join(missing)}")
        if src == dst:
            raise ValueError("self edge is not allowed")
        if self._reachable(dst, src):
            raise ValueError(f"edge {src}->{dst} would create a cycle")
        self.conn.execute("INSERT OR IGNORE INTO edges(src,dst) VALUES(?,?)", (src, dst))
        self.conn.commit()

    def _reachable(self, start: str, target: str) -> bool:
        frontier = [start]
        seen: set[str] = set()
        while frontier:
            node = frontier.pop()
            if node == target:
                return True
            if node in seen:
                continue
            seen.add(node)
            frontier.extend(row[0] for row in self.conn.execute("SELECT dst FROM edges WHERE src=?", (node,)))
        return False

    def descendants(self, node_id: str) -> list[str]:
        out: list[str] = []
        frontier = [node_id]
        seen = {node_id}
        while frontier:
            node = frontier.pop(0)
            for (child,) in self.conn.execute("SELECT dst FROM edges WHERE src=? ORDER BY dst", (node,)):
                if child not in seen:
                    seen.add(child)
                    out.append(child)
                    frontier.append(child)
        return out

    def mark_changed(self, node_id: str, new_digest: str) -> list[str]:
        row = self.conn.execute("SELECT digest FROM nodes WHERE node_id=?", (node_id,)).fetchone()
        if row is None:
            raise KeyError(node_id)
        if row[0] == new_digest:
            return []
        self.conn.execute(
            "UPDATE nodes SET digest=?,status='NOT VERIFIED',updated_at=? WHERE node_id=?",
            (new_digest, utc_now(), node_id),
        )
        stale = self.descendants(node_id)
        if stale:
            self.conn.executemany(
                "UPDATE nodes SET status='STALE',updated_at=? WHERE node_id=?",
                [(utc_now(), item) for item in stale],
            )
        self.conn.commit()
        return stale

    def get_node(self, node_id: str) -> dict[str, Any]:
        row = self.conn.execute(
            "SELECT node_id,kind,digest,status,metadata_json,updated_at FROM nodes WHERE node_id=?",
            (node_id,),
        ).fetchone()
        if row is None:
            raise KeyError(node_id)
        return {
            "node_id": row[0],
            "kind": row[1],
            "digest": row[2],
            "status": row[3],
            "metadata": json.loads(row[4]),
            "updated_at": row[5],
        }

    def coverage(self) -> dict[str, int]:
        rows = self.conn.execute("SELECT status,COUNT(*) FROM nodes GROUP BY status").fetchall()
        return {status: count for status, count in rows}

class ContentAddressedStore:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, path: str | Path) -> tuple[str, Path]:
        src = Path(path)
        digest = sha256_file(src)
        dst = self.root / digest[:2] / digest
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            tmp = dst.with_suffix(".tmp")
            shutil.copy2(src, tmp)
            os.replace(tmp, dst)
        return digest, dst

def build_evidence_package(
    output_path: str | Path,
    files: Iterable[str | Path],
    *,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    records = []
    for item in sorted((Path(p) for p in files), key=lambda p: str(p)):
        records.append(
            {
                "path": str(item),
                "sha256": sha256_file(item),
                "size": item.stat().st_size,
            }
        )
    package = {
        "schema_version": 1,
        "created_at": utc_now(),
        "metadata": metadata or {},
        "files": records,
    }
    atomic_write_json(output_path, package)
    return package
