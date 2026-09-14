from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
import json
import os
import tempfile

PHASES = ("PENDING", "PREFLIGHT", "IN_PROGRESS", "VALIDATION", "CLOSED")
RESULTS = (
    "PASS",
    "FAIL",
    "BLOCKED",
    "NOT VERIFIED",
    "NOT RUN",
    "HOLD",
    "UNRESOLVED",
    "SOURCE CONFLICT",
)
PHASE_ORDER = {name: idx for idx, name in enumerate(PHASES)}

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def atomic_write_json(path: str | Path, data: dict[str, Any], *, inject_failure: bool = False) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=str(target.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        if inject_failure:
            raise RuntimeError("injected failure before atomic publish")
        os.replace(tmp_name, target)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)

@dataclass
class ValidationState:
    name: str
    status: str
    evidence: str = ""
    command: str = ""
    error: str = ""

    def validate(self) -> None:
        if self.status not in RESULTS:
            raise ValueError(f"invalid validation status: {self.status}")

@dataclass
class TaskManifest:
    task_id: str
    roadmap_id: str
    title: str
    lane: str
    phase: str = "PENDING"
    result: str = "NOT VERIFIED"
    branch: str = ""
    commit: str = ""
    worktree: str = ""
    latest_verified_step: str = ""
    next_safe_action: str = ""
    blockers: list[str] = field(default_factory=list)
    hold_items: list[str] = field(default_factory=list)
    artifacts: dict[str, str] = field(default_factory=dict)
    validations: list[ValidationState] = field(default_factory=list)
    risk_score: int = 0
    model_route: str = "MEDIUM"
    do_not_redo: list[str] = field(default_factory=list)
    updated_at: str = field(default_factory=utc_now)

    def validate(self) -> None:
        if not self.task_id.strip():
            raise ValueError("task_id is required")
        if self.phase not in PHASES:
            raise ValueError(f"invalid phase: {self.phase}")
        if self.result not in RESULTS:
            raise ValueError(f"invalid result: {self.result}")
        if not 0 <= int(self.risk_score) <= 100:
            raise ValueError("risk_score must be 0..100")
        for item in self.validations:
            item.validate()
        if self.phase != "CLOSED" and self.result == "PASS":
            raise ValueError("PASS is valid only for CLOSED tasks")

    def transition(self, new_phase: str) -> None:
        if new_phase not in PHASES:
            raise ValueError(f"invalid phase: {new_phase}")
        current = PHASE_ORDER[self.phase]
        target = PHASE_ORDER[new_phase]
        if target < current or target > current + 1:
            raise ValueError(f"invalid phase transition {self.phase} -> {new_phase}")
        self.phase = new_phase
        self.updated_at = utc_now()

    def record_validation(
        self,
        name: str,
        status: str,
        evidence: str = "",
        command: str = "",
        error: str = "",
    ) -> None:
        state = ValidationState(name=name, status=status, evidence=evidence, command=command, error=error)
        state.validate()
        self.validations = [v for v in self.validations if v.name != name] + [state]
        self.updated_at = utc_now()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TaskManifest":
        payload = dict(data)
        payload["validations"] = [ValidationState(**v) for v in payload.get("validations", [])]
        obj = cls(**payload)
        obj.validate()
        return obj

class TaskStore:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.manifest_path = self.root / "ACTIVE_TASK.json"
        self.events_path = self.root / "TASK_EVENTS.jsonl"
        self.checkpoints_dir = self.root / "checkpoints"

    def save(self, manifest: TaskManifest, *, inject_failure: bool = False) -> None:
        manifest.validate()
        manifest.updated_at = utc_now()
        atomic_write_json(self.manifest_path, manifest.to_dict(), inject_failure=inject_failure)

    def load(self) -> TaskManifest:
        with self.manifest_path.open("r", encoding="utf-8") as handle:
            return TaskManifest.from_dict(json.load(handle))

    def append_event(self, manifest: TaskManifest, event: str, details: dict[str, Any] | None = None) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        entry = {
            "ts": utc_now(),
            "task_id": manifest.task_id,
            "phase": manifest.phase,
            "result": manifest.result,
            "event": event,
            "details": details or {},
        }
        with self.events_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(entry, sort_keys=True, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())

    def checkpoint(self, manifest: TaskManifest, label: str) -> Path:
        safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in label).strip("_") or "checkpoint"
        path = self.checkpoints_dir / f"{manifest.task_id}_{safe}_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}.json"
        atomic_write_json(path, manifest.to_dict())
        self.append_event(manifest, "CHECKPOINT", {"path": str(path), "label": label})
        return path

    def handoff_capsule(self, manifest: TaskManifest) -> str:
        lines = [
            f"Task: {manifest.task_id}",
            f"Roadmap: {manifest.roadmap_id}",
            f"Lane: {manifest.lane}",
            f"State: {manifest.phase} / {manifest.result}",
            f"Branch: {manifest.branch or '-'}",
            f"Commit: {manifest.commit or '-'}",
            f"LastVerified: {manifest.latest_verified_step or '-'}",
            f"Next: {manifest.next_safe_action or '-'}",
            f"Model: {manifest.model_route}",
            f"Risk: {manifest.risk_score}",
            f"Blockers: {'; '.join(manifest.blockers) if manifest.blockers else 'NONE'}",
            f"HOLD: {'; '.join(manifest.hold_items) if manifest.hold_items else 'NONE'}",
            f"DoNotRedo: {'; '.join(manifest.do_not_redo) if manifest.do_not_redo else 'NONE'}",
        ]
        if len(lines) > 40:
            raise AssertionError("handoff capsule exceeded 40 lines")
        return "\n".join(lines) + "\n"

def compute_risk_score(
    *,
    strategy_core: bool = False,
    execution_authority: bool = False,
    persistence_restart: bool = False,
    multi_symbol_state: bool = False,
    code_change: bool = False,
    broad_diff: bool = False,
    unresolved_ambiguity: bool = False,
    runtime_causal: bool = False,
) -> int:
    weights = {
        "strategy_core": 30,
        "execution_authority": 20,
        "persistence_restart": 15,
        "multi_symbol_state": 10,
        "code_change": 10,
        "broad_diff": 5,
        "unresolved_ambiguity": 20,
        "runtime_causal": 10,
    }
    flags = locals()
    return min(100, sum(weights[name] for name, enabled in flags.items() if name in weights and enabled))

def route_model(
    task_type: str,
    *,
    risk_score: int = 0,
    strategy_core: bool = False,
    architecture_conflict: bool = False,
    runtime_causal: bool = False,
    explicit_route: str = "",
) -> str:
    if explicit_route:
        return explicit_route
    if strategy_core or architecture_conflict or runtime_causal or risk_score >= 70:
        return "HIGH/XHIGH"
    if task_type in {"implementation", "debug", "regression"} or risk_score >= 40:
        return "HIGH"
    if task_type in {"mechanical", "format", "hash", "manifest"} and risk_score < 20:
        return "LIGHT"
    return "MEDIUM"

class RegressionSelector:
    def __init__(
        self,
        dependency_map: dict[str, dict[str, list[str]]],
        mandatory_global: Iterable[str] = (),
        *,
        strict: bool = False,
    ):
        self.dependency_map = dependency_map
        self.mandatory_global = tuple(dict.fromkeys(mandatory_global))
        self.strict = strict

    def select(
        self,
        changed_modules: Iterable[str],
        *,
        risk_score: int = 0,
        release_candidate: bool = False,
    ) -> list[str]:
        selected = list(self.mandatory_global)
        pending = list(dict.fromkeys(changed_modules))
        unknown = sorted(set(pending) - set(self.dependency_map))
        if self.strict and unknown:
            raise ValueError(f"unknown changed modules: {unknown}")
        visited: set[str] = set()
        while pending:
            module = pending.pop(0)
            if module in visited:
                continue
            visited.add(module)
            item = self.dependency_map.get(module, {})
            selected.extend(item.get("tests", []))
            pending.extend(
                consumer
                for consumer in item.get("consumers", [])
                if consumer not in visited
            )
        if release_candidate or risk_score >= 80:
            for item in self.dependency_map.values():
                selected.extend(item.get("tests", []))
        return list(dict.fromkeys(selected))

def build_context_pack(
    manifest: TaskManifest,
    *,
    authority_refs: Iterable[str] = (),
    changed_modules: Iterable[str] = (),
    selected_validations: Iterable[str] = (),
    evidence_nodes: Iterable[str] = (),
) -> dict[str, Any]:
    return {
        "task": {
            "task_id": manifest.task_id,
            "roadmap_id": manifest.roadmap_id,
            "title": manifest.title,
            "lane": manifest.lane,
            "phase": manifest.phase,
            "result": manifest.result,
            "branch": manifest.branch,
            "commit": manifest.commit,
            "latest_verified_step": manifest.latest_verified_step,
            "next_safe_action": manifest.next_safe_action,
            "blockers": manifest.blockers,
            "hold_items": manifest.hold_items,
            "risk_score": manifest.risk_score,
            "model_route": manifest.model_route,
        },
        "authority_refs": list(dict.fromkeys(authority_refs)),
        "changed_modules": list(dict.fromkeys(changed_modules)),
        "selected_validations": list(dict.fromkeys(selected_validations)),
        "evidence_nodes": list(dict.fromkeys(evidence_nodes)),
        "generated_at": utc_now(),
    }
