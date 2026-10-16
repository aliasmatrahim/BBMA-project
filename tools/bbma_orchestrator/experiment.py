from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any
import hashlib
import json
import re

SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-fA-F]{40}$")
RUN_STATUSES = {"INVALID_RUN", "RUN_FAILED", "VALIDATION_FAILED", "EVIDENCE_ACCEPTED"}
HYPOTHESIS_RESULTS = {"NOT_EVALUATED", "SUPPORTED", "NOT_SUPPORTED", "INCONCLUSIVE"}
_REQUIRED = {
    "hypothesis": ("id", "statement", "preregistered_at", "parameter_sha256", "parameters_frozen"),
    "build": ("build_id", "source_commit", "source_sha256", "ex4_sha256", "set_sha256"),
    "dataset": (
        "dataset_id", "sha256", "symbol", "timeframe", "source_type", "price_basis",
        "synthetic_ticks", "timezone", "start", "end", "warmup_start",
        "evaluation_start", "evaluation_end", "data_as_of", "timestamp_convention", "closed_candles_only",
    ),
    "environment": ("broker", "terminal_build", "tester_mode"),
    "costs": ("spread_model", "commission_model", "swap_included", "slippage_model"),
    "protocol": ("partition", "frozen_at", "parameter_freeze_sha256", "oos_tuning_performed"),
}
_HASH_FIELDS = {
    ("hypothesis", "parameter_sha256"),
    ("build", "source_sha256"),
    ("build", "ex4_sha256"),
    ("build", "set_sha256"),
    ("dataset", "sha256"),
    ("protocol", "parameter_freeze_sha256"),
}
_TIME_FIELDS = {
    ("hypothesis", "preregistered_at"),
    ("dataset", "start"),
    ("dataset", "end"),
    ("dataset", "warmup_start"),
    ("dataset", "evaluation_start"),
    ("dataset", "evaluation_end"),
    ("dataset", "data_as_of"),
    ("protocol", "frozen_at"),
}


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _parse_time(value: Any) -> datetime | None:
    if not _nonempty(value):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed


def validate_manifest(manifest: Any) -> list[str]:
    """Return deterministic validation errors; an empty list means schema checks passed."""
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["manifest: expected object"]
    if isinstance(manifest.get("schema_version"), bool) or not isinstance(manifest.get("schema_version"), int) or manifest.get("schema_version") != 1:
        errors.append("schema_version: expected 1")
    if not _nonempty(manifest.get("run_id")):
        errors.append("run_id: required non-empty string")

    for section, fields in _REQUIRED.items():
        obj = manifest.get(section)
        if not isinstance(obj, dict):
            errors.append(f"{section}: expected object")
            continue
        for field in fields:
            value = obj.get(field)
            if field in {"parameters_frozen", "synthetic_ticks", "closed_candles_only", "swap_included", "oos_tuning_performed"}:
                if not isinstance(value, bool):
                    errors.append(f"{section}.{field}: expected boolean")
            elif not _nonempty(value) and not isinstance(value, bool):
                errors.append(f"{section}.{field}: required non-empty value")

    for section, field in sorted(_HASH_FIELDS):
        obj = manifest.get(section)
        if isinstance(obj, dict) and not SHA256_RE.fullmatch(str(obj.get(field, ""))):
            errors.append(f"{section}.{field}: expected SHA-256 hex")

    parsed: dict[tuple[str, str], datetime] = {}
    for section, field in sorted(_TIME_FIELDS):
        obj = manifest.get(section)
        if isinstance(obj, dict):
            value = _parse_time(obj.get(field))
            if value is None:
                errors.append(f"{section}.{field}: expected timezone-aware ISO-8601 timestamp")
            else:
                parsed[(section, field)] = value

    build = manifest.get("build")
    if isinstance(build, dict) and not COMMIT_RE.fullmatch(str(build.get("source_commit", ""))):
        errors.append("build.source_commit: expected full 40-character Git commit SHA")

    dataset = manifest.get("dataset")
    if isinstance(dataset, dict):
        if dataset.get("price_basis") not in {"BID_ASK_TICKS", "BID_ASK_BARS"}:
            errors.append("dataset.price_basis: expected BID_ASK_TICKS or BID_ASK_BARS")
        if dataset.get("synthetic_ticks") is not False:
            errors.append("dataset.synthetic_ticks: reconstructed/synthetic ticks are not accepted")
        if dataset.get("closed_candles_only") is not True:
            errors.append("dataset.closed_candles_only: must be true")
        expected_convention = "TICK_TIME" if dataset.get("price_basis") == "BID_ASK_TICKS" else "BAR_OPEN"
        if dataset.get("timestamp_convention") != expected_convention:
            errors.append(f"dataset.timestamp_convention: expected {expected_convention}")
        as_of = parsed.get(("dataset", "data_as_of"))
        evaluation_end = parsed.get(("dataset", "evaluation_end"))
        if as_of and evaluation_end and as_of < evaluation_end:
            errors.append("dataset.data_as_of: must be at or after evaluation_end")
        chronology = [
            ("dataset", "warmup_start"), ("dataset", "start"),
            ("dataset", "evaluation_start"), ("dataset", "evaluation_end"),
        ]
        values = [parsed.get(item) for item in chronology]
        if all(values):
            data_end = parsed.get(("dataset", "end"))
            if not (values[0] <= values[1] <= values[2] < values[3] and data_end and values[3] <= data_end):
                errors.append("dataset: expected warmup_start <= start <= evaluation_start < evaluation_end <= end")

    hypothesis = manifest.get("hypothesis")
    protocol = manifest.get("protocol")
    if isinstance(hypothesis, dict) and hypothesis.get("parameters_frozen") is not True:
        errors.append("hypothesis.parameters_frozen: must be true")
    if isinstance(protocol, dict):
        if protocol.get("partition") not in {"IS", "VALIDATION", "OOS"}:
            errors.append("protocol.partition: expected IS, VALIDATION, or OOS")
        if protocol.get("oos_tuning_performed") is not False:
            errors.append("protocol.oos_tuning_performed: must be false")
        freeze_time = parsed.get(("protocol", "frozen_at"))
        evaluation_start = parsed.get(("dataset", "evaluation_start"))
        if protocol.get("partition") == "OOS" and freeze_time and evaluation_start and freeze_time > evaluation_start:
            errors.append("protocol.frozen_at: must not be after OOS evaluation_start")
        if isinstance(hypothesis, dict):
            if hypothesis.get("parameter_sha256") != protocol.get("parameter_freeze_sha256"):
                errors.append("protocol.parameter_freeze_sha256: must match hypothesis.parameter_sha256")
            preregistered = parsed.get(("hypothesis", "preregistered_at"))
            if preregistered and freeze_time and preregistered > freeze_time:
                errors.append("hypothesis.preregistered_at: must not be after protocol.frozen_at")

    costs = manifest.get("costs")
    if isinstance(costs, dict) and costs.get("swap_included") is not True:
        errors.append("costs.swap_included: must be true")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("artifacts: expected non-empty list")
    else:
        kinds: set[str] = set()
        for index, artifact in enumerate(artifacts):
            prefix = f"artifacts[{index}]"
            if not isinstance(artifact, dict):
                errors.append(f"{prefix}: expected object")
                continue
            for field in ("kind", "path", "sha256"):
                if not _nonempty(artifact.get(field)):
                    errors.append(f"{prefix}.{field}: required non-empty string")
            if _nonempty(artifact.get("kind")):
                kinds.add(artifact["kind"])
            if not SHA256_RE.fullmatch(str(artifact.get("sha256", ""))):
                errors.append(f"{prefix}.sha256: expected SHA-256 hex")
        for required_kind in ("source", "ex4", "set", "parameters", "dataset", "trade_history", "tester_report", "tester_log", "validation_report", "dataset_validation_report"):
            if required_kind not in kinds:
                errors.append(f"artifacts: missing required kind {required_kind}")
    return errors


def verify_artifacts(manifest: dict[str, Any], evidence_root: str | Path) -> list[str]:
    """Verify artifact paths and SHA-256 values without permitting root escape."""
    root = Path(evidence_root).resolve()
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["manifest: expected object"]
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        return ["artifacts: expected list"]
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict) or not _nonempty(artifact.get("path")):
            errors.append(f"artifacts[{index}]: invalid artifact path")
            continue
        path = (root / artifact["path"]).resolve()
        if path != root and root not in path.parents:
            errors.append(f"artifacts[{index}].path: escapes evidence root")
            continue
        if not path.is_file():
            errors.append(f"artifacts[{index}].path: file missing")
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest.lower() != str(artifact.get("sha256", "")).lower():
            errors.append(f"artifacts[{index}].sha256: mismatch")
            continue
        if artifact.get("kind") in {"validation_report", "dataset_validation_report"}:
            try:
                report = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                errors.append(f"artifacts[{index}]: validation report must be UTF-8 JSON")
                continue
            if not isinstance(report, dict):
                errors.append(f"artifacts[{index}].validation_report: expected JSON object")
                continue
            expected = {
                "validation_status": "PASS",
                "run_id": manifest.get("run_id"),
                "build_id": manifest.get("build", {}).get("build_id") if isinstance(manifest.get("build"), dict) else None,
                "dataset_sha256": manifest.get("dataset", {}).get("sha256") if isinstance(manifest.get("dataset"), dict) else None,
                "parameter_sha256": manifest.get("hypothesis", {}).get("parameter_sha256") if isinstance(manifest.get("hypothesis"), dict) else None,
            }
            if artifact.get("kind") == "dataset_validation_report":
                expected["dataset_status"] = "VALID"
                expected["validator_version"] = "G1-DATASET-VALIDATOR-1.0"
            for field, value in expected.items():
                if report.get(field) != value:
                    errors.append(f"artifacts[{index}].{artifact.get('kind')}.{field}: mismatch or non-PASS")
    return errors


def classify_run_status(
    manifest_errors: list[str],
    artifact_errors: list[str],
    *,
    process_exit_code: int,
    validation_complete: bool,
) -> str:
    """Classify evidence validity only; never infer profitability."""
    if manifest_errors or artifact_errors:
        return "INVALID_RUN"
    if process_exit_code != 0:
        return "RUN_FAILED"
    if not validation_complete:
        return "VALIDATION_FAILED"
    return "EVIDENCE_ACCEPTED"
