from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Any, Iterable
import hashlib
import json
import re

TRACE_KEYS = (
    "event_type",
    "state",
    "journey_id",
    "decision_id",
    "symbol",
    "direction",
    "reason",
)

def normalize_trace(records: Iterable[dict[str, Any]], keys: Iterable[str] = TRACE_KEYS) -> list[dict[str, str]]:
    key_list = list(keys)
    normalized = []
    for record in records:
        row = {}
        lowered = {str(k).lower(): v for k, v in record.items()}
        for key in key_list:
            value = lowered.get(key.lower(), "")
            row[key] = "" if value is None else str(value)
        normalized.append(row)
    return normalized

def compare_traces(expected: Iterable[dict[str, Any]], actual: Iterable[dict[str, Any]]) -> dict[str, Any]:
    left = normalize_trace(expected)
    right = normalize_trace(actual)
    if left == right:
        return {"classification": "NO_DELTA", "first_mismatch": None, "expected_len": len(left), "actual_len": len(right)}
    limit = min(len(left), len(right))
    mismatch = None
    for idx in range(limit):
        if left[idx] != right[idx]:
            mismatch = {"index": idx, "expected": left[idx], "actual": right[idx]}
            break
    if mismatch is None:
        mismatch = {
            "index": limit,
            "expected": left[limit] if len(left) > limit else None,
            "actual": right[limit] if len(right) > limit else None,
        }
    return {
        "classification": "UNEXPECTED_DELTA",
        "first_mismatch": mismatch,
        "expected_len": len(left),
        "actual_len": len(right),
    }

def classify_build_delta(
    baseline: Iterable[dict[str, Any]],
    candidate: Iterable[dict[str, Any]],
    *,
    authorized_delta: bool = False,
) -> dict[str, Any]:
    result = compare_traces(baseline, candidate)
    if result["classification"] == "NO_DELTA":
        return result
    result["classification"] = "EXPECTED_DELTA" if authorized_delta else "UNEXPECTED_DELTA"
    return result

@dataclass
class ShadowComparison:
    authoritative: list[dict[str, str]]
    shadow: list[dict[str, str]]
    result: dict[str, Any]

def compare_shadow(
    authoritative: Iterable[dict[str, Any]],
    shadow: Iterable[dict[str, Any]],
) -> ShadowComparison:
    left = normalize_trace(authoritative)
    right = normalize_trace(shadow)
    return ShadowComparison(left, right, compare_traces(left, right))

TRACE_ARTIFACT_FIELDS = {
    "schema_version", "kind", "role", "authority_ref", "source_sha256",
    "source_path", "source_kind", "emitter", "runtime_verification",
    "record_count", "records", "trace_sha256",
}
TRACE_RECORD_FIELDS = {
    "event_type", "journey_id", "decision_id", "symbol", "status",
    "fields", "provenance",
}


def _canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def build_trace_artifact(
    records: Iterable[dict[str, Any]],
    *,
    source_sha256: str,
    emitter: str,
    role: str = "candidate",
    authority_ref: str = "",
) -> dict[str, Any]:
    _require(
        bool(re.fullmatch(r"[0-9a-fA-F]{64}", source_sha256)),
        "source_sha256 must be a 64-character hex digest",
    )
    _require(bool(emitter.strip()), "emitter is required")
    _require(role in {"candidate", "golden"}, "role must be candidate or golden")
    _require(
        role != "golden" or bool(authority_ref.strip()),
        "golden role requires authority_ref",
    )

    trace_records: list[dict[str, Any]] = []
    event_keys: set[str] = set()
    source_paths: set[str] = set()
    source_kinds: set[str] = set()
    runtime_states: set[str] = set()
    for row in records:
        _require(isinstance(row, dict), "trace input record must be an object")
        payload = row.get("payload")
        _require(isinstance(payload, dict), "trace input payload must be an object")
        _require(
            str(payload.get("source_sha256", "")).lower() == source_sha256.lower(),
            "trace record source_sha256 mismatch",
        )
        _require(payload.get("emitter") == emitter, "trace record emitter mismatch")
        for identity_field in (
            "event_type", "journey_id", "decision_id", "symbol", "status"
        ):
            _require(
                str(row.get(identity_field, ""))
                == str(payload.get(identity_field, "")),
                f"trace row/payload mismatch for {identity_field}",
            )
        fields = payload.get("fields")
        _require(isinstance(fields, dict), "trace record fields must be an object")
        event_key = payload.get("event_key")
        source_line = payload.get("source_line")
        _require(
            isinstance(event_key, str) and bool(event_key),
            "trace record event_key is required",
        )
        _require(event_key not in event_keys, "duplicate trace event_key")
        _require(
            isinstance(source_line, int) and source_line > 0,
            "trace record source_line must be positive",
        )
        event_keys.add(event_key)
        source_path = payload.get("source_path")
        source_kind = payload.get("source_kind")
        runtime_state = payload.get("runtime_verification")
        _require(
            isinstance(source_path, str) and bool(source_path),
            "trace record source_path is required",
        )
        _require(
            isinstance(source_kind, str) and bool(source_kind),
            "trace record source_kind is required",
        )
        _require(
            isinstance(runtime_state, str) and bool(runtime_state),
            "trace record runtime_verification is required",
        )
        source_paths.add(source_path)
        source_kinds.add(source_kind)
        runtime_states.add(runtime_state)
        trace_records.append(
            {
                "event_type": str(row.get("event_type", "")),
                "journey_id": str(row.get("journey_id", "")),
                "decision_id": str(row.get("decision_id", "")),
                "symbol": str(row.get("symbol", "")),
                "status": str(row.get("status", "")),
                "fields": json.loads(
                    json.dumps(fields, sort_keys=True, ensure_ascii=False)
                ),
                "provenance": {
                    "source_line": source_line,
                    "event_key": event_key,
                },
            }
        )
    _require(bool(trace_records), "trace requires at least one attributable record")
    _require(len(source_paths) == 1, "trace records must share one source_path")
    _require(len(source_kinds) == 1, "trace records must share one source_kind")
    _require(
        len(runtime_states) == 1,
        "trace records must share one runtime_verification state",
    )
    trace_records.sort(
        key=lambda item: (
            item["provenance"]["source_line"],
            item["provenance"]["event_key"],
        )
    )
    artifact: dict[str, Any] = {
        "schema_version": 1,
        "kind": "BBMA_DECISION_TRACE",
        "role": role,
        "authority_ref": authority_ref.strip(),
        "source_sha256": source_sha256.lower(),
        "source_path": next(iter(source_paths)),
        "source_kind": next(iter(source_kinds)),
        "emitter": emitter,
        "runtime_verification": next(iter(runtime_states)),
        "record_count": len(trace_records),
        "records": trace_records,
    }
    artifact["trace_sha256"] = _canonical_digest(artifact)
    return artifact


def validate_trace_artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    _require(isinstance(artifact, dict), "trace artifact must be an object")
    _require(
        set(artifact) == TRACE_ARTIFACT_FIELDS,
        "trace artifact fields mismatch",
    )
    _require(artifact["schema_version"] == 1, "unsupported trace schema_version")
    _require(artifact["kind"] == "BBMA_DECISION_TRACE", "invalid trace kind")
    _require(
        artifact["role"] in {"candidate", "golden"},
        "invalid trace role",
    )
    _require(
        isinstance(artifact["authority_ref"], str),
        "invalid trace authority_ref",
    )
    _require(
        artifact["role"] != "golden" or bool(artifact["authority_ref"].strip()),
        "golden role requires authority_ref",
    )
    _require(
        isinstance(artifact["source_sha256"], str)
        and bool(re.fullmatch(r"[0-9a-f]{64}", artifact["source_sha256"])),
        "invalid trace source_sha256",
    )
    for field in ("source_path", "source_kind", "runtime_verification"):
        _require(
            isinstance(artifact[field], str) and bool(artifact[field].strip()),
            f"invalid trace {field}",
        )
    _require(
        isinstance(artifact["emitter"], str) and bool(artifact["emitter"].strip()),
        "invalid trace emitter",
    )
    records = artifact["records"]
    _require(isinstance(records, list) and bool(records), "trace records required")
    _require(artifact["record_count"] == len(records), "trace record_count mismatch")
    event_keys: set[str] = set()
    prior_line = 0
    for record in records:
        _require(
            isinstance(record, dict) and set(record) == TRACE_RECORD_FIELDS,
            "trace record fields mismatch",
        )
        _require(isinstance(record["fields"], dict), "trace fields must be an object")
        provenance = record["provenance"]
        _require(
            isinstance(provenance, dict)
            and set(provenance) == {"source_line", "event_key"},
            "trace provenance fields mismatch",
        )
        source_line = provenance["source_line"]
        event_key = provenance["event_key"]
        _require(
            isinstance(source_line, int) and source_line > 0,
            "trace source_line must be positive",
        )
        _require(source_line >= prior_line, "trace records are not source ordered")
        _require(
            isinstance(event_key, str) and bool(event_key),
            "trace event_key is required",
        )
        _require(event_key not in event_keys, "duplicate trace event_key")
        prior_line = source_line
        event_keys.add(event_key)
    supplied_hash = artifact["trace_sha256"]
    body = dict(artifact)
    del body["trace_sha256"]
    _require(
        isinstance(supplied_hash, str)
        and supplied_hash == _canonical_digest(body),
        "trace hash mismatch",
    )
    return artifact


def compare_trace_artifacts(
    baseline: dict[str, Any],
    candidate: dict[str, Any],
    *,
    authorization_ref: str = "",
) -> dict[str, Any]:
    validate_trace_artifact(baseline)
    validate_trace_artifact(candidate)
    _require(baseline["role"] == "golden", "baseline role must be golden")
    _require(candidate["role"] == "candidate", "candidate role must be candidate")
    left = [
        {key: value for key, value in record.items() if key != "provenance"}
        for record in baseline["records"]
    ]
    right = [
        {key: value for key, value in record.items() if key != "provenance"}
        for record in candidate["records"]
    ]
    mismatch = None
    limit = min(len(left), len(right))
    for index in range(limit):
        if left[index] != right[index]:
            mismatch = {
                "index": index,
                "expected": left[index],
                "actual": right[index],
            }
            break
    if mismatch is None and len(left) != len(right):
        mismatch = {
            "index": limit,
            "expected": left[limit] if len(left) > limit else None,
            "actual": right[limit] if len(right) > limit else None,
        }
    if mismatch is None:
        classification = "NO_DELTA"
    elif authorization_ref.strip():
        classification = "EXPECTED_DELTA"
    else:
        classification = "UNEXPECTED_DELTA"
    return {
        "classification": classification,
        "first_mismatch": mismatch,
        "expected_len": len(left),
        "actual_len": len(right),
        "baseline": {
            "emitter": baseline["emitter"],
            "source_sha256": baseline["source_sha256"],
            "trace_sha256": baseline["trace_sha256"],
            "authority_ref": baseline["authority_ref"],
        },
        "candidate": {
            "emitter": candidate["emitter"],
            "source_sha256": candidate["source_sha256"],
            "trace_sha256": candidate["trace_sha256"],
        },
        "authorization_ref": authorization_ref.strip(),
    }


LIFECYCLE_STATES = (
    "NONE",
    "CANDIDATE",
    "CONFIRMED",
    "SELECTED",
    "VALIDATED",
    "RISK_APPROVED",
    "ENTRY_READY",
    "EXECUTED",
    "VOID",
    "EXPIRED",
    "SUPERSEDED",
)

DEFAULT_TRANSITIONS: dict[str, set[str]] = {
    "NONE": {"CANDIDATE"},
    "CANDIDATE": {"CONFIRMED", "VOID", "EXPIRED", "SUPERSEDED"},
    "CONFIRMED": {"SELECTED", "VOID", "EXPIRED", "SUPERSEDED"},
    "SELECTED": {"VALIDATED", "VOID", "EXPIRED", "SUPERSEDED"},
    "VALIDATED": {"RISK_APPROVED", "VOID", "EXPIRED", "SUPERSEDED"},
    "RISK_APPROVED": {"ENTRY_READY", "VOID", "EXPIRED", "SUPERSEDED"},
    "ENTRY_READY": {"EXECUTED", "VOID", "EXPIRED", "SUPERSEDED"},
    "EXECUTED": set(),
    "VOID": set(),
    "EXPIRED": set(),
    "SUPERSEDED": set(),
}

TERMINAL_STATES = {"EXECUTED", "VOID", "EXPIRED", "SUPERSEDED"}

class LifecycleModel:
    """Engineering lifecycle separation model; this is not a BBMA signal rule."""

    def __init__(self, transitions: dict[str, set[str]] | None = None):
        source = transitions if transitions is not None else DEFAULT_TRANSITIONS
        self.transitions = {key: set(values) for key, values in source.items()}
        self.state = "NONE"
        self.history = ["NONE"]

    def allowed(self) -> set[str]:
        return set(self.transitions.get(self.state, set()))

    def transition(self, new_state: str) -> None:
        if new_state not in LIFECYCLE_STATES:
            raise ValueError(f"unknown lifecycle state: {new_state}")
        if new_state not in self.allowed():
            raise ValueError(f"invalid lifecycle transition {self.state} -> {new_state}")
        self.state = new_state
        self.history.append(new_state)

def validate_transition_table(transitions: dict[str, set[str]]) -> list[str]:
    errors: list[str] = []
    for state in LIFECYCLE_STATES:
        if state not in transitions:
            errors.append(f"missing state {state}")
    for terminal in TERMINAL_STATES:
        if transitions.get(terminal):
            errors.append(f"terminal state {terminal} has outgoing transitions")
    forbidden_skips = {
        ("NONE", "CONFIRMED"),
        ("CANDIDATE", "SELECTED"),
        ("CONFIRMED", "VALIDATED"),
        ("SELECTED", "RISK_APPROVED"),
        ("VALIDATED", "ENTRY_READY"),
        ("RISK_APPROVED", "EXECUTED"),
    }
    for src, dst in forbidden_skips:
        if dst in transitions.get(src, set()):
            errors.append(f"forbidden skip {src}->{dst}")
    return errors

def randomized_lifecycle_check(seed: int = 1, iterations: int = 500) -> dict[str, int]:
    rng = Random(seed)
    valid_attempts = 0
    invalid_attempts = 0
    for _ in range(iterations):
        model = LifecycleModel()
        for _step in range(20):
            options = list(model.allowed())
            choose_valid = bool(options) and rng.random() < 0.65
            if choose_valid:
                target = rng.choice(options)
                model.transition(target)
                valid_attempts += 1
                if target in TERMINAL_STATES:
                    break
            else:
                invalid = [state for state in LIFECYCLE_STATES if state not in model.allowed()]
                target = rng.choice(invalid)
                try:
                    model.transition(target)
                except ValueError:
                    invalid_attempts += 1
                else:
                    raise AssertionError(f"invalid transition unexpectedly accepted: {model.history[-2]}->{target}")
    return {"valid_attempts": valid_attempts, "invalid_attempts": invalid_attempts}

def mutation_self_test() -> bool:
    mutated = {key: set(values) for key, values in DEFAULT_TRANSITIONS.items()}
    mutated["CANDIDATE"].add("SELECTED")
    errors = validate_transition_table(mutated)
    return any("CANDIDATE->SELECTED" in item for item in errors)
