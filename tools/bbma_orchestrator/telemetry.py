from __future__ import annotations

from pathlib import Path
from typing import Any
import csv
import hashlib
import json
import re
import sqlite3

from blueprint.tools.n2_nmje_decision_correlator import (
    N1_RE,
    N2_RE,
    decode_identity_token as decode_decision_token,
)
from blueprint.tools.n2_nmje_outcome_log_extractor import (
    OUT_RE,
    decode_identity_token as decode_outcome_token,
)
from .core import utc_now

FAIL_STATUSES = {"FAIL", "ERROR", "BLOCKED", "REJECTED", "INVALID", "STALE"}
MT4_SOURCE_KINDS = ("mt4-expert", "strategy-tester", "runtime-smoke")
KNOWN_MT4_MARKERS = ("N1-NMJE", "N2-NMJE-DEC", "N2-NMJE-OUT")
_LOG_PREFIX_RE = re.compile(
    r"^(?P<severity>\d+)\t(?P<clock>\d{1,2}:\d{2}:\d{2}(?:\.\d+)?)\t"
    r"(?P<emitter>.*?):\s*"
)
_LOG_DATE_RE = re.compile(r"^(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})$")
_KEY_RE = re.compile(r"[A-Za-z0-9_]+")
_N1_REQUIRED = {
    "REL": "relation", "P": "parent", "J": "journey",
    "D1": "d1", "H4": "h4", "H1": "h1", "M15": "m15", "R": "reason",
}
_N1_ADDITIVE = {"SUB", "MAT", "PRETAIN", "PSEL", "PHASE", "PDUR", "PE"}
_N2_REQUIRED = {
    "SIG": "signal", "DIR": "direction", "REL": "relation",
    "P": "parent", "J": "journey", "DID": "decision_id",
}
_N2_OPTIONAL = {
    "PE": "parent_event", "DIDH": "decision_hash", "AUTH": "authority",
    "OFAM": "opportunity_family", "OC": "opportunity_cycle",
    "LTF": "ltf_cluster", "OSH": "opportunity_sequence_hash",
}
_OUT_KEYS = {"PAIR", "TICKET", "DID", "DIDH", "NET", "CLOSE", "REC"}


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _log_context(path: Path, line: str) -> dict[str, str]:
    prefix = _LOG_PREFIX_RE.match(line)
    clock = prefix.group("clock") if prefix else ""
    emitter = prefix.group("emitter") if prefix else ""
    severity = prefix.group("severity") if prefix else ""
    date = _LOG_DATE_RE.match(path.stem)
    timestamp = clock
    if date and clock:
        timestamp = (
            f"{date.group('year')}-{date.group('month')}-{date.group('day')}T{clock}"
        )
    return {
        "ts": timestamp,
        "log_clock": clock,
        "emitter": emitter,
        "severity": severity,
    }


def _event_payload(
    *, path: Path, digest: str, line_no: int, raw_line: str,
    source_kind: str, marker: str, fields: dict[str, Any],
) -> dict[str, Any]:
    context = _log_context(path, raw_line)
    event_key = hashlib.sha256(
        f"{digest}:{line_no}:{marker}".encode("utf-8")
    ).hexdigest()
    payload: dict[str, Any] = {
        **context,
        "status": "OBSERVED",
        "marker": marker,
        "source_kind": source_kind,
        "source_path": str(path.resolve()),
        "source_sha256": digest,
        "source_line": line_no,
        "event_key": event_key,
        "runtime_verification": "NOT VERIFIED",
        "raw_line": raw_line,
        "fields": fields,
    }
    return payload


def _strict_fields(
    line: str, marker: str, *, pair_first: bool, allowed: set[str],
    required: set[str], allow_empty: set[str] | None = None,
) -> tuple[str, dict[str, str], str] | None:
    record = line[line.index(f"[{marker}]"):]
    parts = record.split()
    value_tokens = parts[2:] if pair_first else parts[1:]
    pair = parts[1] if pair_first and len(parts) > 1 else ""
    if pair_first and (not pair or "=" in pair):
        return None
    values: dict[str, str] = {}
    for token in value_tokens:
        if "=" not in token:
            return None
        key, value = token.split("=", 1)
        if (
            not _KEY_RE.fullmatch(key)
            or key in values
            or key not in allowed
            or (not value and key not in (allow_empty or set()))
        ):
            return None
        values[key] = value
    if not required.issubset(values):
        return None
    return pair, values, record


def _parse_n1(line: str) -> dict[str, str] | None:
    parsed = _strict_fields(
        line, "N1-NMJE", pair_first=True,
        allowed=set(_N1_REQUIRED) | _N1_ADDITIVE,
        required=set(_N1_REQUIRED),
    )
    if parsed is None:
        return None
    pair, values, record = parsed
    additive = bool(_N1_ADDITIVE.intersection(values))
    if additive and "PE" not in values:
        return None
    canonical = N1_RE.fullmatch(record)
    if canonical and not additive:
        return {key: value or "" for key, value in canonical.groupdict().items()}
    fields = {"pair": pair}
    fields.update({name: values[key] for key, name in _N1_REQUIRED.items()})
    for key in _N1_ADDITIVE:
        if key in values:
            fields[key.lower()] = values[key]
    return fields


def _parse_n2_decision(line: str) -> dict[str, str] | None:
    parsed = _strict_fields(
        line, "N2-NMJE-DEC", pair_first=True,
        allowed=set(_N2_REQUIRED) | set(_N2_OPTIONAL),
        required=set(_N2_REQUIRED), allow_empty={"OC"},
    )
    if parsed is None:
        return None
    pair, values, record = parsed
    current = bool({"PE", "LTF", "OSH"}.intersection(values))
    if current and not {"PE", "DIDH", "OSH"}.issubset(values):
        return None
    canonical = N2_RE.fullmatch(record)
    if canonical and not current:
        return {key: value or "" for key, value in canonical.groupdict().items()}
    fields = {"pair": pair}
    fields.update({name: values[key] for key, name in _N2_REQUIRED.items()})
    fields.update({name: values.get(key, "") for key, name in _N2_OPTIONAL.items()})
    return fields


def _parse_outcome(line: str) -> dict[str, str] | None:
    parsed = _strict_fields(
        line, "N2-NMJE-OUT", pair_first=False,
        allowed=_OUT_KEYS, required=_OUT_KEYS,
    )
    if parsed is None:
        return None
    _, _, record = parsed
    match = OUT_RE.fullmatch(record)
    if match is None:
        return None
    return {key: value or "" for key, value in match.groupdict().items()}


def parse_mt4_telemetry(path: str | Path, source_kind: str) -> list[dict[str, Any]]:
    if source_kind not in MT4_SOURCE_KINDS:
        raise ValueError(
            f"unsupported source_kind {source_kind!r}; expected one of {MT4_SOURCE_KINDS}"
        )
    log_path = Path(path)
    digest = _sha256_file(log_path)
    events: list[dict[str, Any]] = []
    with log_path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            raw_line = line.rstrip("\r\n")
            markers = [
                name for name in KNOWN_MT4_MARKERS if f"[{name}]" in raw_line
            ]
            if not markers:
                continue
            if len(markers) != 1:
                raise ValueError(
                    f"line {line_no}: malformed ambiguous telemetry markers"
                )
            marker = markers[0]
            parser = {
                "N1-NMJE": _parse_n1,
                "N2-NMJE-DEC": _parse_n2_decision,
                "N2-NMJE-OUT": _parse_outcome,
            }[marker]
            fields = parser(raw_line)
            if fields is None:
                raise ValueError(f"line {line_no}: malformed [{marker}] telemetry")
            payload = _event_payload(
                path=log_path, digest=digest, line_no=line_no, raw_line=raw_line,
                source_kind=source_kind, marker=marker, fields=fields,
            )
            if marker == "N1-NMJE":
                payload.update(
                    event_type="N1_NMJE_OBSERVATION",
                    journey_id=fields["journey"], decision_id="", symbol=fields["pair"],
                )
            elif marker == "N2-NMJE-DEC":
                decision_id = decode_decision_token(fields["decision_id"])
                fields["decision_id"] = decision_id
                payload.update(
                    event_type="N2_NMJE_DECISION",
                    journey_id=fields["journey"], decision_id=decision_id,
                    symbol=fields["pair"],
                )
            else:
                decision_id = (
                    decode_outcome_token(fields["decision_id"])
                    if fields["decision_id"] != "-" else ""
                )
                fields["decision_id"] = decision_id
                payload.update(
                    event_type="N2_NMJE_OUTCOME", journey_id="",
                    decision_id=decision_id, symbol=fields["pair"],
                    identity_state=(
                        "FULL_DECISION_ID" if decision_id
                        else "HASH_ONLY_NOT_ATTRIBUTED"
                    ),
                )
            events.append(payload)
    if _sha256_file(log_path) != digest:
        raise ValueError(f"source changed during ingestion: {log_path}")
    return events


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
                event_key TEXT NOT NULL DEFAULT '',
                payload_json TEXT NOT NULL,
                ingested_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_events_journey ON events(journey_id);
            CREATE INDEX IF NOT EXISTS idx_events_decision ON events(decision_id);
            CREATE INDEX IF NOT EXISTS idx_events_status ON events(status);
            CREATE INDEX IF NOT EXISTS idx_events_event_type ON events(event_type);
            """
        )
        columns = {
            row[1] for row in self.conn.execute("PRAGMA table_info(events)").fetchall()
        }
        if "event_key" not in columns:
            self.conn.execute(
                "ALTER TABLE events ADD COLUMN event_key TEXT NOT NULL DEFAULT ''"
            )
        self.conn.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_events_event_key "
            "ON events(event_key) WHERE event_key <> ''"
        )
        self.conn.commit()

    @staticmethod
    def _pick(payload: dict[str, Any], *names: str, default: str = "") -> str:
        lowered = {str(key).lower(): value for key, value in payload.items()}
        for name in names:
            if name.lower() in lowered and lowered[name.lower()] is not None:
                return str(lowered[name.lower()])
        return default

    def ingest_event(
        self, payload: dict[str, Any], source: str = "",
        event_key: str = "", *, commit: bool = True,
    ) -> int:
        ts = self._pick(payload, "ts", "timestamp", "time", default=utc_now())
        event_type = self._pick(payload, "event_type", "event", "type", default="UNKNOWN")
        journey_id = self._pick(payload, "journey_id", "journeyid")
        decision_id = self._pick(payload, "decision_id", "decisionid")
        symbol = self._pick(payload, "symbol", "pair")
        status = self._pick(payload, "status", "result", "state", default="UNKNOWN").upper()
        src = source or self._pick(payload, "source", default="unknown")
        cur = self.conn.execute(
            """
            INSERT OR IGNORE INTO events(
                ts,source,event_type,journey_id,decision_id,symbol,status,
                event_key,payload_json,ingested_at
            )
            VALUES(?,?,?,?,?,?,?,?,?,?)
            """,
            (
                ts,
                src,
                event_type,
                journey_id,
                decision_id,
                symbol,
                status,
                event_key,
                json.dumps(payload, sort_keys=True, ensure_ascii=False),
                utc_now(),
            ),
        )
        if commit:
            self.conn.commit()
        return int(cur.lastrowid) if cur.rowcount else 0

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

    def ingest_mt4_log(
        self, path: str | Path, *, source_kind: str, source: str = "",
    ) -> int:
        events = parse_mt4_telemetry(path, source_kind)
        inserted = 0
        with self.conn:
            for payload in events:
                row_id = self.ingest_event(
                    payload,
                    source=source or source_kind,
                    event_key=str(payload["event_key"]),
                    commit=False,
                )
                inserted += int(row_id != 0)
        return inserted

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

    def attributable_events(
        self, *, source_sha256: str, emitter: str, limit: int = 10000,
    ) -> list[dict[str, Any]]:
        if not re.fullmatch(r"[0-9a-fA-F]{64}", source_sha256):
            raise ValueError("source_sha256 must be a 64-character hex digest")
        if not emitter.strip():
            raise ValueError("emitter is required")
        if limit < 1:
            raise ValueError("limit must be positive")
        selected: list[dict[str, Any]] = []
        rows = self.conn.execute(
            """
            SELECT id,ts,source,event_type,journey_id,decision_id,symbol,status,
                   event_key,payload_json
            FROM events
            ORDER BY id
            """
        )
        for row in rows:
            payload = json.loads(row[9])
            if (
                payload.get("source_sha256", "").lower() != source_sha256.lower()
                or payload.get("emitter") != emitter
            ):
                continue
            if payload.get("event_key") != row[8]:
                raise ValueError(f"event {row[0]} provenance event_key mismatch")
            selected.append(
                {
                    "id": row[0],
                    "ts": row[1],
                    "source": row[2],
                    "event_type": row[3],
                    "journey_id": row[4],
                    "decision_id": row[5],
                    "symbol": row[6],
                    "status": row[7],
                    "payload": payload,
                }
            )
            if len(selected) > limit:
                raise ValueError(
                    f"attributable event selection exceeds limit {limit}"
                )
        if not selected:
            raise ValueError(
                "no attributable events for exact source_sha256 and emitter"
            )
        return selected

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
