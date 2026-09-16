from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

from .source_library import SourceRecord, SourceRegistry

ARTIFACT_ROLES = ("RAW", "CORRECTED", "DERIVED", "UNKNOWN")
_RAW_SUFFIXES = {".csv", ".docx", ".html", ".json", ".md", ".mp3", ".mp4", ".pdf", ".txt", ".wav"}

def discover_paths(
    roots: Iterable[str | Path],
    patterns: Sequence[str] = ("*",),
) -> list[Path]:
    """Discover only caller-supplied filesystem roots in stable order."""
    selected: dict[str, Path] = {}
    for root_value in roots:
        root = Path(root_value)
        if root.is_file():
            candidates = [root]
        elif root.is_dir():
            candidates = [
                candidate
                for pattern in patterns
                for candidate in root.rglob(pattern)
                if candidate.is_file()
            ]
        else:
            candidates = []
        for candidate in candidates:
            selected[str(candidate)] = candidate
    return [selected[key] for key in sorted(selected, key=str.casefold)]

def classify_artifact_role(path: str | Path, explicit_role: str = "") -> str:
    role = explicit_role.strip().upper()
    if role:
        if role not in ARTIFACT_ROLES:
            raise ValueError(f"invalid artifact role: {explicit_role}")
        return role
    name = Path(path).name.casefold()
    if "corrected" in name:
        return "CORRECTED"
    if "derived" in name or "summary" in name:
        return "DERIVED"
    if Path(path).suffix.casefold() in _RAW_SUFFIXES:
        return "RAW"
    return "UNKNOWN"

def record_provenance(
    registry: SourceRegistry,
    source_id: str,
    provenance: str,
    tier: str,
    authority_refs: Iterable[str] = (),
) -> SourceRecord:
    """Record metadata only; discovery never advances lifecycle or authority."""
    return registry.record_provenance(source_id, provenance, tier, authority_refs)
