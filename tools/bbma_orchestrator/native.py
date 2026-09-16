from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
import csv
import io
import json
import os
import re
import subprocess

from .core import utc_now
from .evidence import sha256_file

@dataclass(frozen=True)
class CommandSpec:
    name: str
    argv: tuple[str, ...]
    cwd: str
    timeout_seconds: int = 900
    enabled: bool = True
    blocked_reason: str = ""
    expected_inputs: tuple[tuple[str, str], ...] = ()
    exclusive_process_names: tuple[str, ...] = ()
    result_kind: str = ""
    result_log_path: str = ""
    result_artifacts: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, name: str, data: dict[str, Any]) -> "CommandSpec":
        argv = data.get("argv")
        if not isinstance(argv, list) or not argv or not all(
            isinstance(item, str) and item for item in argv
        ):
            raise ValueError(f"{name}: argv must be a non-empty string list")
        cwd = str(data.get("cwd", ""))
        if not cwd:
            raise ValueError(f"{name}: cwd is required")
        timeout = int(data.get("timeout_seconds", 900))
        if timeout <= 0:
            raise ValueError(f"{name}: timeout_seconds must be > 0")
        enabled = data.get("enabled", True)
        blocked_reason = data.get("blocked_reason", "")
        if not isinstance(enabled, bool):
            raise ValueError(f"{name}: enabled must be boolean")
        if not enabled and not isinstance(blocked_reason, str):
            raise ValueError(f"{name}: blocked_reason must be a string")
        if not enabled and not blocked_reason.strip():
            raise ValueError(f"{name}: disabled command needs blocked_reason")

        expected_inputs = cls._expected_inputs(name, data.get("expected_inputs", []))
        exclusive = data.get("exclusive_process_names", [])
        if not isinstance(exclusive, list) or not all(
            isinstance(item, str) and item.strip() for item in exclusive
        ):
            raise ValueError(f"{name}: exclusive_process_names must be strings")
        result = cls._result_contract(name, data.get("result_contract", {}))
        return cls(
            name=name,
            argv=tuple(argv),
            cwd=cwd,
            timeout_seconds=timeout,
            enabled=enabled,
            blocked_reason=blocked_reason,
            expected_inputs=expected_inputs,
            exclusive_process_names=tuple(item.lower() for item in exclusive),
            result_kind=result[0],
            result_log_path=result[1],
            result_artifacts=result[2],
        )

    @staticmethod
    def _expected_inputs(
        name: str, items: Any
    ) -> tuple[tuple[str, str], ...]:
        if not isinstance(items, list):
            raise ValueError(f"{name}: expected_inputs must be a list")
        parsed = []
        for item in items:
            if not isinstance(item, dict):
                raise ValueError(f"{name}: expected input must be an object")
            path = item.get("path")
            digest = item.get("sha256")
            if not isinstance(path, str) or not path:
                raise ValueError(f"{name}: expected input path is required")
            if not isinstance(digest, str) or not re.fullmatch(
                r"[0-9a-fA-F]{64}", digest
            ):
                raise ValueError(f"{name}: expected input sha256 is invalid")
            parsed.append((path, digest.lower()))
        return tuple(parsed)

    @staticmethod
    def _result_contract(
        name: str, result: Any
    ) -> tuple[str, str, tuple[str, ...]]:
        if not isinstance(result, dict):
            raise ValueError(f"{name}: result_contract must be an object")
        if not result:
            return "", "", ()
        if result.get("kind") != "metaeditor_0e0w":
            raise ValueError(f"{name}: unsupported result contract")
        log_path = result.get("log_path")
        artifacts = result.get("artifacts")
        if not isinstance(log_path, str) or not log_path:
            raise ValueError(f"{name}: result log_path is required")
        if not isinstance(artifacts, list) or not artifacts or not all(
            isinstance(item, str) and item for item in artifacts
        ):
            raise ValueError(f"{name}: result artifacts must be non-empty strings")
        return "metaeditor_0e0w", log_path, tuple(artifacts)


def active_process_names() -> set[str]:
    if os.name == "nt":
        completed = subprocess.run(
            ["tasklist", "/FO", "CSV", "/NH"],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError("unable to enumerate active Windows processes")
        return {
            row[0].lower()
            for row in csv.reader(io.StringIO(completed.stdout))
            if row
        }
    completed = subprocess.run(
        ["ps", "-A", "-o", "comm="],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError("unable to enumerate active processes")
    return {Path(line.strip()).name.lower() for line in completed.stdout.splitlines()}


class NativeAdapter:
    """Explicit-command native runner. It has no implicit restart/trading action."""

    def __init__(
        self,
        config_path: str | Path,
        process_names_provider: Callable[[], set[str]] = active_process_names,
    ):
        self.config_path = Path(config_path)
        self.process_names_provider = process_names_provider
        data = json.loads(self.config_path.read_text(encoding="utf-8"))
        self.commands = {
            name: CommandSpec.from_dict(name, spec)
            for name, spec in data.get("commands", {}).items()
        }
        self.forbidden_tokens = tuple(
            token.lower()
            for token in data.get(
                "forbidden_tokens",
                [
                    "force-push",
                    "git reset --hard",
                    "terminal restart",
                    "enable trading",
                    "autotrading on",
                ],
            )
        )

    def names(self) -> list[str]:
        return sorted(self.commands)

    def describe(self, name: str) -> dict[str, Any]:
        spec = self._get(name)
        return {
            "name": spec.name,
            "argv": list(spec.argv),
            "cwd": spec.cwd,
            "timeout_seconds": spec.timeout_seconds,
            "enabled": spec.enabled,
            "blocked_reason": spec.blocked_reason,
            "expected_inputs": self._input_identities(spec),
            "exclusive_process_names": list(spec.exclusive_process_names),
            "result_contract": {
                "kind": spec.result_kind,
                "log_path": spec.result_log_path,
                "artifacts": list(spec.result_artifacts),
            },
            "native_status": "NOT NATIVE VERIFIED",
        }

    def _get(self, name: str) -> CommandSpec:
        try:
            return self.commands[name]
        except KeyError as exc:
            raise KeyError(f"unknown configured native command: {name}") from exc

    @staticmethod
    def _resolve(cwd: str, item: str) -> Path:
        path = Path(item)
        return path if path.is_absolute() else Path(cwd) / path

    def _input_identities(self, spec: CommandSpec) -> list[dict[str, Any]]:
        rows = []
        for item, expected in spec.expected_inputs:
            path = self._resolve(spec.cwd, item)
            actual = sha256_file(path) if path.is_file() else ""
            rows.append({
                "path": str(path),
                "exists": path.is_file(),
                "expected_sha256": expected,
                "actual_sha256": actual,
                "matches": actual == expected,
            })
        return rows

    def _safety_check(self, spec: CommandSpec) -> None:
        if not spec.enabled:
            raise PermissionError(spec.blocked_reason)
        joined = " ".join(spec.argv).lower()
        for token in self.forbidden_tokens:
            if token and token in joined:
                raise PermissionError(
                    f"configured command contains forbidden token: {token}"
                )
        cwd = Path(spec.cwd)
        if not cwd.exists():
            raise FileNotFoundError(f"configured cwd does not exist: {cwd}")
        mismatches = [
            row["path"] for row in self._input_identities(spec) if not row["matches"]
        ]
        if mismatches:
            raise ValueError(f"configured input identity mismatch: {mismatches}")

    def _duplicate_check(self, spec: CommandSpec) -> None:
        active = {item.lower() for item in self.process_names_provider()}
        conflicts = sorted(set(spec.exclusive_process_names) & active)
        if conflicts:
            raise RuntimeError(f"matching process already active: {conflicts}")

    def _result_mtimes(self, spec: CommandSpec) -> dict[str, int | None]:
        paths = [spec.result_log_path, *spec.result_artifacts]
        return {
            str(path): path.stat().st_mtime_ns if path.is_file() else None
            for item in paths
            for path in [self._resolve(spec.cwd, item)]
        }

    def _verify_result(
        self, spec: CommandSpec, previous_mtimes: dict[str, int | None]
    ) -> dict[str, Any]:
        if not spec.result_kind:
            return {}
        log_path = self._resolve(spec.cwd, spec.result_log_path)
        if not log_path.is_file():
            raise FileNotFoundError(f"native result log missing: {log_path}")
        current_mtimes = self._result_mtimes(spec)
        stale = [
            path for path, before in previous_mtimes.items()
            if before is not None and current_mtimes.get(path) == before
        ]
        if stale:
            raise RuntimeError(f"native result outputs not refreshed: {stale}")
        raw = log_path.read_bytes()
        encoding = "utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig"
        text = raw.decode(encoding, errors="replace")
        matches = re.findall(
            r"(?i)(\d+)\s+errors?,\s*(\d+)\s+warnings?", text
        )
        if not matches:
            raise ValueError("MetaEditor result summary missing")
        errors, warnings = (int(item) for item in matches[-1])
        if errors or warnings:
            raise RuntimeError(
                f"MetaEditor result is not 0E0W: {errors} errors / {warnings} warnings"
            )
        artifacts = artifact_identity([
            self._resolve(spec.cwd, item) for item in spec.result_artifacts
        ])
        missing = [item["path"] for item in artifacts if not item["exists"]]
        if missing:
            raise FileNotFoundError(f"native result artifacts missing: {missing}")
        return {
            "metaeditor_errors": errors,
            "metaeditor_warnings": warnings,
            "result_log": artifact_identity([log_path])[0],
            "artifacts": artifacts,
        }

    def run(self, name: str, *, execute: bool = False) -> dict[str, Any]:
        spec = self._get(name)
        self._safety_check(spec)
        base = {
            "name": name,
            "argv": list(spec.argv),
            "cwd": spec.cwd,
            "started_at": utc_now(),
            "inputs": self._input_identities(spec),
        }
        if not execute:
            return {
                **base,
                "status": "NOT RUN",
                "native_status": "NOT NATIVE VERIFIED",
                "reason": "dry-run; pass execute=True only after live-state verification",
            }
        self._duplicate_check(spec)
        previous_mtimes = self._result_mtimes(spec) if spec.result_kind else {}
        completed = subprocess.run(
            list(spec.argv),
            cwd=spec.cwd,
            capture_output=True,
            text=True,
            timeout=spec.timeout_seconds,
            check=False,
        )
        result = {}
        verification_error = ""
        if spec.result_kind:
            try:
                result = self._verify_result(spec, previous_mtimes)
            except (FileNotFoundError, RuntimeError, ValueError) as exc:
                verification_error = str(exc)
            status = "PASS" if not verification_error else "FAIL"
        else:
            status = "PASS" if completed.returncode == 0 else "FAIL"
        return {
            **base,
            **result,
            "finished_at": utc_now(),
            "status": status,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "verification_error": verification_error,
            "native_status": "EXECUTED",
        }

def git_snapshot(repo_path: str | Path) -> dict[str, Any]:
    repo = Path(repo_path)
    if not repo.exists():
        raise FileNotFoundError(repo)

    def run(*args: str) -> str:
        proc = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
        return proc.stdout.strip()

    return {
        "captured_at": utc_now(),
        "repo": str(repo.resolve()),
        "branch": run("branch", "--show-current"),
        "commit": run("rev-parse", "HEAD"),
        "status_porcelain": run("status", "--porcelain=v1"),
        "worktrees": run("worktree", "list", "--porcelain"),
    }

def artifact_identity(paths: list[str | Path]) -> list[dict[str, Any]]:
    out = []
    for item in paths:
        path = Path(item)
        out.append(
            {
                "path": str(path),
                "exists": path.exists(),
                "size": path.stat().st_size if path.exists() else None,
                "sha256": sha256_file(path) if path.exists() and path.is_file() else "",
            }
        )
    return out
