from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
import json
import sqlite3

from .core import utc_now
from .evidence import EvidenceDB, sha256_file

SOURCE_PHASES = (
    "DISCOVERED",
    "INGESTED",
    "INTEGRITY_VERIFIED",
    "PROVENANCE_CLASSIFIED",
    "EXTRACTED",
    "RECONCILIATION_PENDING",
    "RECONCILED",
    "REGISTERED",
)
SOURCE_PHASE_ORDER = {name: idx for idx, name in enumerate(SOURCE_PHASES)}

SOURCE_DISPOSITIONS = (
    "UNREVIEWED",
    "MATCH",
    "CORROBORATION_ONLY",
    "PARTIAL",
    "UNCLEAR",
    "SOURCE_CONFLICT",
    "ACCEPTED_CORE",
    "REJECTED",
)
NON_EXECUTABLE_DISPOSITIONS = {
    "PARTIAL",
    "UNCLEAR",
    "SOURCE_CONFLICT",
    "REJECTED",
}

@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    uri: str
    digest: str
    size: int
    media_type: str
    artifact_role: str
    provenance: str
    tier: str
    phase: str
    disposition: str
    accepted_authority: str
    authority_refs: tuple[str, ...]
    core_rule_ids: tuple[str, ...]
    affected_modules: tuple[str, ...]
    hold_items: tuple[str, ...]
    metadata: dict[str, Any]
    created_at: str
    updated_at: str

@dataclass(frozen=True)
class IngestResult:
    status: str
    record: SourceRecord
    duplicate_of: str = ""
    previous_digest: str = ""

class SourceRegistry:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._init_schema()

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> "SourceRegistry":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def _init_schema(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS sources (
                source_id TEXT PRIMARY KEY,
                uri TEXT NOT NULL,
                digest TEXT NOT NULL,
                size INTEGER NOT NULL,
                media_type TEXT NOT NULL,
                artifact_role TEXT NOT NULL,
                provenance TEXT NOT NULL,
                tier TEXT NOT NULL,
                phase TEXT NOT NULL,
                disposition TEXT NOT NULL,
                accepted_authority TEXT NOT NULL,
                authority_refs_json TEXT NOT NULL,
                core_rule_ids_json TEXT NOT NULL,
                affected_modules_json TEXT NOT NULL,
                hold_items_json TEXT NOT NULL,
                metadata_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_sources_digest ON sources(digest);
            CREATE TABLE IF NOT EXISTS source_evidence_links (
                source_id TEXT NOT NULL,
                node_id TEXT NOT NULL,
                source_digest TEXT NOT NULL,
                accepted_authority TEXT NOT NULL,
                linked_at TEXT NOT NULL,
                PRIMARY KEY (source_id, node_id)
            );
            """
        )
        self.conn.commit()

    @staticmethod
    def _json_tuple(value: str) -> tuple[str, ...]:
        return tuple(json.loads(value))

    @staticmethod
    def _dump(values: Iterable[str]) -> str:
        return json.dumps(list(values), sort_keys=False, ensure_ascii=False)
    @classmethod
    def _from_row(cls, row: tuple[Any, ...]) -> SourceRecord:
        return SourceRecord(
            source_id=row[0],
            uri=row[1],
            digest=row[2],
            size=int(row[3]),
            media_type=row[4],
            artifact_role=row[5],
            provenance=row[6],
            tier=row[7],
            phase=row[8],
            disposition=row[9],
            accepted_authority=row[10],
            authority_refs=cls._json_tuple(row[11]),
            core_rule_ids=cls._json_tuple(row[12]),
            affected_modules=cls._json_tuple(row[13]),
            hold_items=cls._json_tuple(row[14]),
            metadata=json.loads(row[15]),
            created_at=row[16],
            updated_at=row[17],
        )

    @staticmethod
    def _validate_source_id(source_id: str) -> str:
        value = source_id.strip()
        if not value:
            raise ValueError("source_id is required")
        return value
    def get(self, source_id: str) -> SourceRecord:
        source_id = self._validate_source_id(source_id)
        row = self.conn.execute(
            "SELECT * FROM sources WHERE source_id=?",
            (source_id,),
        ).fetchone()
        if row is None:
            raise KeyError(source_id)
        return self._from_row(row)

    def find_by_digest(self, digest: str) -> list[SourceRecord]:
        rows = self.conn.execute(
            "SELECT * FROM sources WHERE digest=? ORDER BY source_id",
            (digest,),
        ).fetchall()
        return [self._from_row(row) for row in rows]

    def register_discovered(
        self,
        source_id: str,
        uri: str,
        *,
        media_type: str = "",
        artifact_role: str = "UNKNOWN",
        provenance: str = "",
        tier: str = "",
        authority_refs: Iterable[str] = (),
        metadata: dict[str, Any] | None = None,
    ) -> SourceRecord:
        source_id = self._validate_source_id(source_id)
        if not uri.strip():
            raise ValueError("uri is required")
        existing = self.conn.execute(
            "SELECT * FROM sources WHERE source_id=?",
            (source_id,),
        ).fetchone()
        if existing is not None:
            record = self._from_row(existing)
            if record.uri != uri:
                raise ValueError(f"source_id {source_id} already registered with a different URI")
            return record
        now = utc_now()
        self.conn.execute(
            """
            INSERT INTO sources(
                source_id,uri,digest,size,media_type,artifact_role,provenance,tier,
                phase,disposition,accepted_authority,authority_refs_json,
                core_rule_ids_json,affected_modules_json,hold_items_json,
                metadata_json,created_at,updated_at
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                source_id,
                uri,
                "",
                0,
                media_type,
                artifact_role,
                provenance,
                tier,
                "DISCOVERED",
                "UNREVIEWED",
                "",
                self._dump(authority_refs),
                "[]",
                "[]",
                "[]",
                json.dumps(metadata or {}, sort_keys=True, ensure_ascii=False),
                now,
                now,
            ),
        )
        self.conn.commit()
        return self.get(source_id)

    def transition_phase(self, source_id: str, new_phase: str) -> SourceRecord:
        if new_phase not in SOURCE_PHASE_ORDER:
            raise ValueError(f"invalid source phase: {new_phase}")
        record = self.get(source_id)
        current = SOURCE_PHASE_ORDER[record.phase]
        target = SOURCE_PHASE_ORDER[new_phase]
        if target < current or target > current + 1:
            raise ValueError(f"invalid source phase transition {record.phase} -> {new_phase}")
        if target == current:
            return record
        self.conn.execute(
            "UPDATE sources SET phase=?,updated_at=? WHERE source_id=?",
            (new_phase, utc_now(), record.source_id),
        )
        self.conn.commit()
        return self.get(record.source_id)

    def set_disposition(
        self,
        source_id: str,
        disposition: str,
        *,
        accepted_authority: str = "",
    ) -> SourceRecord:
        if disposition not in SOURCE_DISPOSITIONS:
            raise ValueError(f"invalid source disposition: {disposition}")
        record = self.get(source_id)
        authority = ""
        if disposition == "ACCEPTED_CORE":
            authority = accepted_authority.strip()
            if not authority:
                raise ValueError("ACCEPTED_CORE requires explicit accepted authority")
            if record.phase not in {"RECONCILED", "REGISTERED"}:
                raise ValueError("ACCEPTED_CORE requires a reconciled source")
        self.conn.execute(
            """
            UPDATE sources
            SET disposition=?,accepted_authority=?,updated_at=?
            WHERE source_id=?
            """,
            (disposition, authority, utc_now(), record.source_id),
        )
        self.conn.commit()
        return self.get(record.source_id)

    def record_provenance(
        self,
        source_id: str,
        provenance: str,
        tier: str,
        authority_refs: Iterable[str] = (),
    ) -> SourceRecord:
        record = self.get(source_id)
        provenance_value = provenance.strip() or "UNVERIFIED"
        tier_value = tier.strip() or "UNVERIFIED"
        refs = tuple(ref.strip() for ref in authority_refs if ref.strip())
        self.conn.execute(
            """
            UPDATE sources
            SET provenance=?, tier=?, authority_refs_json=?, updated_at=?
            WHERE source_id=?
            """,
            (provenance_value, tier_value, self._dump(refs), utc_now(), record.source_id),
        )
        self.conn.commit()
        return self.get(record.source_id)

    def set_hold_items(self, source_id: str, hold_items: Iterable[str]) -> SourceRecord:
        record = self.get(source_id)
        holds = tuple(item.strip() for item in hold_items if item.strip())
        self.conn.execute(
            "UPDATE sources SET hold_items_json=?,updated_at=? WHERE source_id=?",
            (self._dump(holds), utc_now(), record.source_id),
        )
        self.conn.commit()
        return self.get(record.source_id)

    def link_evidence_node(self, source_id: str, node_id: str) -> str:
        record = self.get(source_id)
        node_id = node_id.strip()
        if not node_id:
            raise ValueError("node_id is required")
        if (
            record.phase not in {"RECONCILED", "REGISTERED"}
            or record.disposition != "ACCEPTED_CORE"
            or not record.accepted_authority
            or record.hold_items
        ):
            raise ValueError("source evidence link requires reconciled ACCEPTED_CORE without HOLD")
        if not record.digest:
            raise ValueError("accepted source digest is required for evidence linking")
        self.conn.execute(
            """
            INSERT INTO source_evidence_links(
                source_id,node_id,source_digest,accepted_authority,linked_at
            ) VALUES(?,?,?,?,?)
            ON CONFLICT(source_id,node_id) DO UPDATE SET
                source_digest=excluded.source_digest,
                accepted_authority=excluded.accepted_authority,
                linked_at=excluded.linked_at
            """,
            (record.source_id, node_id, record.digest, record.accepted_authority, utc_now()),
        )
        self.conn.commit()
        return node_id

    def propagate_source_change(
        self,
        source_id: str,
        new_digest: str,
        evidence_db: EvidenceDB,
    ) -> list[str]:
        record = self.get(source_id)
        new_digest = new_digest.strip()
        if not new_digest:
            raise ValueError("new_digest is required")
        if record.digest != new_digest:
            raise ValueError("new_digest must match the current source registry digest")
        links = self.conn.execute(
            """
            SELECT node_id,source_digest
            FROM source_evidence_links
            WHERE source_id=?
            ORDER BY node_id
            """,
            (record.source_id,),
        ).fetchall()
        validated_nodes: list[str] = []
        for node_id, accepted_digest in links:
            node = evidence_db.get_node(node_id)
            if node["kind"] != "source":
                raise ValueError(f"linked node {node_id} is not a source evidence node")
            if node["digest"] not in {accepted_digest, new_digest}:
                raise ValueError(f"linked source evidence digest mismatch: {node_id}")
            validated_nodes.append(node_id)

        stale: list[str] = []
        seen: set[str] = set()
        for node_id in validated_nodes:
            for descendant in evidence_db.mark_changed(node_id, new_digest):
                if descendant not in seen:
                    seen.add(descendant)
                    stale.append(descendant)
        return stale

    def failure_first_summary(self, *, limit: int = 25) -> dict[str, Any]:
        if limit < 0:
            raise ValueError("limit must be >= 0")
        records = [
            self._from_row(row)
            for row in self.conn.execute("SELECT * FROM sources ORDER BY source_id").fetchall()
        ]
        stale_ids = {
            row[0]
            for row in self.conn.execute(
                """
                SELECT DISTINCT l.source_id
                FROM source_evidence_links l
                JOIN sources s ON s.source_id=l.source_id
                WHERE l.source_digest<>s.digest
                """
            ).fetchall()
        }
        duplicate_groups = int(
            self.conn.execute(
                """
                SELECT COUNT(*) FROM (
                    SELECT digest FROM sources
                    WHERE digest<>''
                    GROUP BY digest HAVING COUNT(*)>1
                )
                """
            ).fetchone()[0]
        )
        priority = {
            "SOURCE_CONFLICT": 0,
            "UNCLEAR": 1,
            "PARTIAL": 2,
            "MISSING": 3,
            "STALE": 4,
            "RECHECK_REQUIRED": 5,
        }
        counts = {name: 0 for name in priority}
        items: list[dict[str, Any]] = []
        registered_match_count = 0
        for record in records:
            if record.phase == "REGISTERED" and record.disposition == "MATCH":
                registered_match_count += 1
            if record.disposition in {"SOURCE_CONFLICT", "UNCLEAR", "PARTIAL"}:
                category = record.disposition
            elif not record.digest:
                category = "MISSING"
            elif record.source_id in stale_ids:
                category = "STALE"
            elif record.phase != "REGISTERED" and record.disposition == "UNREVIEWED":
                category = "RECHECK_REQUIRED"
            else:
                continue
            counts[category] += 1
            items.append(
                {
                    "source_id": record.source_id,
                    "category": category,
                    "phase": record.phase,
                    "disposition": record.disposition,
                    "hold_count": len(record.hold_items),
                }
            )
        items.sort(key=lambda item: (priority[item["category"]], item["source_id"]))
        total_failure_items = len(items)
        bounded = items[:limit]
        return {
            "counts": counts,
            "items": bounded,
            "total_failure_items": total_failure_items,
            "truncated": total_failure_items > len(bounded),
            "registered_match_count": registered_match_count,
            "duplicate_digest_groups": duplicate_groups,
        }

    def ingest_file(
        self,
        source_id: str,
        path: str | Path,
        *,
        media_type: str = "",
        artifact_role: str = "UNKNOWN",
        provenance: str = "",
        tier: str = "",
        authority_refs: Iterable[str] = (),
        metadata: dict[str, Any] | None = None,
    ) -> IngestResult:
        source_id = self._validate_source_id(source_id)
        source_path = Path(path)
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
        digest = sha256_file(source_path)
        size = source_path.stat().st_size
        duplicates = [record for record in self.find_by_digest(digest) if record.source_id != source_id]
        duplicate_of = duplicates[0].source_id if duplicates else ""
        try:
            existing = self.get(source_id)
        except KeyError:
            existing = self.register_discovered(
                source_id,
                str(source_path),
                media_type=media_type,
                artifact_role=artifact_role,
                provenance=provenance,
                tier=tier,
                authority_refs=authority_refs,
                metadata=metadata,
            )

        previous_digest = existing.digest
        if previous_digest == digest:
            return IngestResult(
                status="UNCHANGED" if previous_digest else "NEW",
                record=existing,
                duplicate_of=duplicate_of,
                previous_digest=previous_digest,
            )

        now = utc_now()
        is_new = not previous_digest
        self.conn.execute(
            """
            UPDATE sources
            SET uri=?, digest=?, size=?, media_type=?, artifact_role=?, provenance=?, tier=?,
                phase=?, disposition=?, accepted_authority=?, authority_refs_json=?,
                core_rule_ids_json=?, affected_modules_json=?, hold_items_json=?,
                metadata_json=?, updated_at=?
            WHERE source_id=?
            """,
            (
                str(source_path),
                digest,
                size,
                media_type or existing.media_type,
                artifact_role or existing.artifact_role,
                provenance or existing.provenance,
                tier or existing.tier,
                "INTEGRITY_VERIFIED",
                "UNREVIEWED",
                "",
                self._dump(authority_refs or existing.authority_refs),
                "[]",
                "[]",
                "[]",
                json.dumps(metadata if metadata is not None else existing.metadata, sort_keys=True, ensure_ascii=False),
                now,
                source_id,
            ),
        )
        self.conn.commit()
        return IngestResult(
            status="DUPLICATE" if duplicate_of else "NEW" if is_new else "CHANGED",
            record=self.get(source_id),
            duplicate_of=duplicate_of,
            previous_digest=previous_digest,
        )
