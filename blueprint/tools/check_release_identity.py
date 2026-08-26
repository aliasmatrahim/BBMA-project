#!/usr/bin/env python3
"""Fail-fast guard for BBMA EA user-facing release identity.

Engineering-only. This script does not inspect or change trading semantics.
The canonical release identity lives in blueprint/source/EA_RELEASE_IDENTITY.json.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / "blueprint/source/EA_RELEASE_IDENTITY.json"


def fail(message: str) -> None:
    print(f"RELEASE_IDENTITY_GUARD=FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def require_once(source: str, needle: str, label: str) -> None:
    count = source.count(needle)
    if count != 1:
        fail(f"{label}: expected exactly 1 occurrence, found {count}: {needle!r}")


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    product = str(manifest["product_name"]).strip()
    display_version = str(manifest["display_version"]).strip()
    property_version = str(manifest["property_version"]).strip()
    stage = str(manifest["release_stage"]).strip()
    source_path = REPO_ROOT / str(manifest["source_path"])

    if not re.fullmatch(r"\d+\.\d+\.\d+", display_version):
        fail(f"invalid display_version format: {display_version!r}")
    if not re.fullmatch(r"\d+\.\d+", property_version):
        fail(f"invalid property_version format: {property_version!r}")

    major, minor, patch = display_version.split(".")
    expected_property = f"{major}.{minor}{patch}"
    if property_version != expected_property:
        fail(
            "manifest version mapping mismatch: "
            f"display {display_version!r} requires property {expected_property!r}, "
            f"found {property_version!r}"
        )

    source = source_path.read_text(encoding="utf-8")
    runtime_title = f"{product} V{display_version} {stage}"

    header_re = re.compile(
        rf"^//\|\s*Version\s+{re.escape(display_version)}\s+-\s+{re.escape(stage)}\s*\|\s*$",
        re.MULTILINE,
    )
    header_matches = header_re.findall(source)
    if len(header_matches) != 1:
        fail(
            "header identity mismatch: expected exactly one "
            f"'Version {display_version} - {stage}' header, found {len(header_matches)}"
        )

    property_re = re.compile(
        rf'^#property\s+version\s+"{re.escape(property_version)}"\s*$',
        re.MULTILINE,
    )
    property_matches = property_re.findall(source)
    if len(property_matches) != 1:
        fail(
            "#property version mismatch: expected exactly one "
            f"{property_version!r}, found {len(property_matches)}"
        )

    require_once(
        source,
        f"=== {runtime_title} ===",
        "dashboard runtime title",
    )
    require_once(
        source,
        f"{runtime_title} initialized successfully",
        "OnInit runtime title",
    )

    # Any quoted user-facing version identity must use the canonical runtime title.
    # Internal provenance comments such as D1O-07 are intentionally ignored.
    quoted_literals = re.findall(r'"(?:[^"\\]|\\.)*"', source)
    version_literals = [literal for literal in quoted_literals if f"{product} V" in literal]
    if not version_literals:
        fail("no user-facing versioned runtime string literals found")

    stale = [literal for literal in version_literals if runtime_title not in literal]
    if stale:
        preview = "; ".join(stale[:5])
        fail(f"stale/mixed user-facing runtime identity detected: {preview}")

    print(
        "RELEASE_IDENTITY_GUARD=PASS "
        f"display={display_version} property={property_version} stage={stage!r} "
        f"runtime_literals={len(version_literals)}"
    )


if __name__ == "__main__":
    main()
