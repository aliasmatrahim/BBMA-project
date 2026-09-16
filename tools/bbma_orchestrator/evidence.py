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
            """
        )
        self.conn.commit()

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
