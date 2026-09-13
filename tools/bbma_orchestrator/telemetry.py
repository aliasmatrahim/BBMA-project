from __future__ import annotations

from pathlib import Path
from typing import Any
import csv
import json
import sqlite3

from .core import utc_now

FAIL_STATUSES = {"FAIL", "ERROR", "BLOCKED", "REJECTED", "INVALID", "STALE"}

class TelemetryStore:
    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self._init_schema()

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> "TelemetryStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def _init_schema(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,
                source TEXT NOT NULL,
                event_type TEXT NOT NULL,
                journey_id TEXT NOT NULL,
                decision_id TEXT NOT NULL,
                symbol TEXT NOT NULL,
                status TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                ingested_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_events_journey ON events(journey_id);
            CREATE INDEX IF NOT EXISTS idx_events_decision ON events(decision_id);
            CREATE INDEX IF NOT EXISTS idx_events_status ON events(status);
            CREATE INDEX IF NOT EXISTS idx_events_event_type ON events(event_type);
            """
        )
        self.conn.commit()

    @staticmethod
    def _pick(payload: dict[str, Any], *names: str, default: str = "") -> str:
        lowered = {str(key).lower(): value for key, value in payload.items()}
        for name in names:
            if name.lower() in lowered and lowered[name.lower()] is not None:
                return str(lowered[name.lower()])
        return default

    def ingest_event(self, payload: dict[str, Any], source: str = "") -> int:
        ts = self._pick(payload, "ts", "timestamp", "time", default=utc_now())
        event_type = self._pick(payload, "event_type", "event", "type", default="UNKNOWN")
        journey_id = self._pick(payload, "journey_id", "journeyid")
        decision_id = self._pick(payload, "decision_id", "decisionid")
        symbol = self._pick(payload, "symbol", "pair")
        status = self._pick(payload, "status", "result", "state", default="UNKNOWN").upper()
        src = source or self._pick(payload, "source", default="unknown")
        cur = self.conn.execute(
            """
            INSERT INTO events(ts,source,event_type,journey_id,decision_id,symbol,status,payload_json,ingested_at)
            VALUES(?,?,?,?,?,?,?,?,?)
            """,
            (
                ts,
                src,
                event_type,
                journey_id,
                decision_id,
                symbol,
                status,
                json.dumps(payload, sort_keys=True, ensure_ascii=False),
                utc_now(),
            ),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def ingest_jsonl(self, path: str | Path, source: str = "") -> int:
        count = 0
        with Path(path).open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, 1):
                text = line.strip()
                if not text:
                    continue
                payload = json.loads(text)
                if not isinstance(payload, dict):
                    raise ValueError(f"line {line_no}: JSON object required")
                self.ingest_event(payload, source=source)
                count += 1
        return count

    def ingest_csv(self, path: str | Path, source: str = "") -> int:
        count = 0
        with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames:
                return 0
            for row in reader:
                self.ingest_event(dict(row), source=source)
                count += 1
        return count

    def failure_first_summary(self, limit: int = 50) -> dict[str, Any]:
        total = self.conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        pass_count = self.conn.execute(
            "SELECT COUNT(*) FROM events WHERE UPPER(status) IN ('PASS','OK','VALID','SUCCESS')"
        ).fetchone()[0]
        failures = self.conn.execute(
            """
            SELECT id,ts,source,event_type,journey_id,decision_id,symbol,status,payload_json
            FROM events
            WHERE UPPER(status) IN ('FAIL','ERROR','BLOCKED','REJECTED','INVALID','STALE')
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        by_status = dict(
            self.conn.execute(
                "SELECT status,COUNT(*) FROM events GROUP BY status ORDER BY COUNT(*) DESC"
            ).fetchall()
        )
        by_type = dict(
            self.conn.execute(
                "SELECT event_type,COUNT(*) FROM events GROUP BY event_type ORDER BY COUNT(*) DESC"
            ).fetchall()
        )
        return {
            "total": total,
            "pass_like": pass_count,
            "failure_like": sum(by_status.get(status, 0) for status in FAIL_STATUSES),
            "by_status": by_status,
            "by_event_type": by_type,
            "failures": [
                {
                    "id": row[0],
                    "ts": row[1],
                    "source": row[2],
                    "event_type": row[3],
                    "journey_id": row[4],
                    "decision_id": row[5],
                    "symbol": row[6],
                    "status": row[7],
                    "payload": json.loads(row[8]),
                }
                for row in failures
            ],
        }

    def lookup(self, *, journey_id: str = "", decision_id: str = "", limit: int = 200) -> list[dict[str, Any]]:
        if not journey_id and not decision_id:
            raise ValueError("journey_id or decision_id is required")
        clauses = []
        params: list[Any] = []
        if journey_id:
            clauses.append("journey_id=?")
            params.append(journey_id)
        if decision_id:
            clauses.append("decision_id=?")
            params.append(decision_id)
        params.append(limit)
        rows = self.conn.execute(
            f"""
            SELECT id,ts,source,event_type,journey_id,decision_id,symbol,status,payload_json
            FROM events
            WHERE {' AND '.join(clauses)}
            ORDER BY id
            LIMIT ?
            """,
            params,
        ).fetchall()
        return [
            {
                "id": row[0],
                "ts": row[1],
                "source": row[2],
                "event_type": row[3],
                "journey_id": row[4],
                "decision_id": row[5],
                "symbol": row[6],
                "status": row[7],
                "payload": json.loads(row[8]),
            }
            for row in rows
        ]
