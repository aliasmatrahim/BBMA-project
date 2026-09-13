from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json
import subprocess

from .core import utc_now
from .evidence import sha256_file

@dataclass(frozen=True)
class CommandSpec:
    name: str
    argv: tuple[str, ...]
    cwd: str
    timeout_seconds: int = 900

    @classmethod
    def from_dict(cls, name: str, data: dict[str, Any]) -> "CommandSpec":
        argv = data.get("argv")
        if not isinstance(argv, list) or not argv or not all(isinstance(item, str) and item for item in argv):
            raise ValueError(f"{name}: argv must be a non-empty string list")
        cwd = str(data.get("cwd", ""))
        if not cwd:
            raise ValueError(f"{name}: cwd is required")
        timeout = int(data.get("timeout_seconds", 900))
        if timeout <= 0:
            raise ValueError(f"{name}: timeout_seconds must be > 0")
        return cls(name=name, argv=tuple(argv), cwd=cwd, timeout_seconds=timeout)

class NativeAdapter:
    """Explicit-command native runner. It has no implicit restart/trading action."""

    def __init__(self, config_path: str | Path):
        self.config_path = Path(config_path)
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
            "native_status": "NOT NATIVE VERIFIED",
        }

    def _get(self, name: str) -> CommandSpec:
        try:
            return self.commands[name]
        except KeyError as exc:
            raise KeyError(f"unknown configured native command: {name}") from exc

    def _safety_check(self, spec: CommandSpec) -> None:
        joined = " ".join(spec.argv).lower()
        for token in self.forbidden_tokens:
            if token and token in joined:
                raise PermissionError(f"configured command contains forbidden token: {token}")
        cwd = Path(spec.cwd)
        if not cwd.exists():
            raise FileNotFoundError(f"configured cwd does not exist: {cwd}")

    def run(self, name: str, *, execute: bool = False) -> dict[str, Any]:
        spec = self._get(name)
        self._safety_check(spec)
        base = {
            "name": name,
            "argv": list(spec.argv),
            "cwd": spec.cwd,
            "started_at": utc_now(),
        }
        if not execute:
            return {
                **base,
                "status": "NOT RUN",
                "native_status": "NOT NATIVE VERIFIED",
                "reason": "dry-run; pass execute=True only after live-state verification",
            }
        completed = subprocess.run(
            list(spec.argv),
            cwd=spec.cwd,
            capture_output=True,
            text=True,
            timeout=spec.timeout_seconds,
            check=False,
        )
        return {
            **base,
            "finished_at": utc_now(),
            "status": "PASS" if completed.returncode == 0 else "FAIL",
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
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
