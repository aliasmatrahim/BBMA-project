from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable

from .evidence import sha256_file

_DONE_RE = re.compile(r"^chunk_(\d+)\.done$")
_ASR_DRAFT_STATUSES = {"ASR-DRAFT", "ASR_DRAFT"}
_COMPLETE_STATUSES = {"COMPLETE", "COMPLETED"}


def _status(value: Any) -> str:
    return str(value or "").strip().upper()


def _unit_count(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def _completed_units(payload: dict[str, Any]) -> list[int]:
    value = payload.get("completed_units", ())
    if not isinstance(value, (list, tuple, set)):
        return []
    return sorted({item for item in value if isinstance(item, int) and not isinstance(item, bool) and item >= 0})


def classify_manifest_state(payload: dict[str, Any]) -> dict[str, Any]:
    declared_status = _status(payload.get("declared_status", payload.get("status", "")))
    total_units = _unit_count(payload.get("total_units", payload.get("chunks")))
    completed_units = _completed_units(payload)
    completion_marker = bool(payload.get("completion_marker", payload.get("completed")))

    if total_units is not None and any(unit >= total_units for unit in completed_units):
        processing_state = "REVIEW_REQUIRED"
    elif total_units is not None:
        if total_units > 0 and len(completed_units) == total_units:
            processing_state = "COMPLETE"
        elif completed_units:
            processing_state = "PARTIAL"
        elif total_units == 0 and declared_status in _COMPLETE_STATUSES:
            processing_state = "COMPLETE"
        else:
            processing_state = "PENDING"
    elif declared_status in _COMPLETE_STATUSES and completion_marker:
        processing_state = "COMPLETE"
    else:
        processing_state = "REVIEW_REQUIRED"

    semantic_authority = (
        "ASR_DRAFT_ONLY" if declared_status in _ASR_DRAFT_STATUSES else "NO_CORE_AUTHORITY"
    )
    return {
        "processing_state": processing_state,
        "semantic_authority": semantic_authority,
        "core_eligible": False,
    }


def scan_manifest(path: str | Path) -> dict[str, Any]:
    manifest_path = Path(path)
    if not manifest_path.is_file():
        raise FileNotFoundError(manifest_path)
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("manifest must contain a JSON object")

    total_units = _unit_count(payload.get("chunks"))
    completed_units: list[int] = []
    chunks_dir = manifest_path.parent / "chunks"
    if chunks_dir.is_dir():
        for marker in chunks_dir.glob("chunk_*.done"):
            match = _DONE_RE.match(marker.name)
            if match:
                completed_units.append(int(match.group(1)))
    completed_units = sorted(set(completed_units))
    missing_units = (
        [unit for unit in range(total_units) if unit not in completed_units]
        if total_units is not None
        else []
    )

    source_id = str(
        payload.get("video_dir")
        or payload.get("video_id")
        or manifest_path.parent.parent.name
    )
    scanned = {
        "source_id": source_id,
        "manifest_path": str(manifest_path),
        "manifest_sha256": sha256_file(manifest_path),
        "declared_status": _status(payload.get("status", "")),
        "total_units": total_units,
        "completed_units": completed_units,
        "missing_units": missing_units,
        "completion_marker": bool(payload.get("completed")),
    }
    scanned.update(classify_manifest_state(scanned))
    return scanned


def plan_resume(manifests: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    plans: list[dict[str, Any]] = []
    for manifest in sorted(
        manifests,
        key=lambda item: (str(item.get("source_id", "")), str(item.get("manifest_path", ""))),
    ):
        state = str(manifest.get("processing_state", "")).strip().upper()
        if not state:
            state = classify_manifest_state(manifest)["processing_state"]
        if state == "COMPLETE":
            action = "SKIP_COMPLETE"
            missing_units: list[int] = []
        elif state == "PARTIAL":
            action = "RESUME_MISSING"
            missing_units = list(manifest.get("missing_units", ()))
        elif state == "PENDING":
            action = "START_EXPLICIT"
            missing_units = list(manifest.get("missing_units", ()))
        else:
            action = "REVIEW_REQUIRED"
            missing_units = list(manifest.get("missing_units", ()))
        plans.append(
            {
                "source_id": str(manifest.get("source_id", "")),
                "manifest_path": str(manifest.get("manifest_path", "")),
                "processing_state": state,
                "action": action,
                "missing_units": missing_units,
                "semantic_authority": str(
                    manifest.get("semantic_authority", "NO_CORE_AUTHORITY")
                ),
                "core_eligible": False,
            }
        )
    return plans
