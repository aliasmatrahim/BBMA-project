#!/usr/bin/env python3
"""Build exact BBMA v4.59 runtime variants without changing strategy semantics.

The canonical source must match the post-P0 v4.59 identity exactly. Runtime
variants may only flip one already-approved lifecycle gate for evidence runs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

EXPECTED_BLOB = "dc83e62748c93171d89a312e9f7a53c06d97e261"
EXPECTED_SHA256 = "0a42ee2e6c32810f655b592d8738f500e8b63b4e08c4c874e82452f75ce94b2e"
BUILD_MARKER = "Version 4.5.9 - P0 Execution Identity Persistence Fix"
VERSION_MARKER = '#property version   "4.59"'
D1_GATE_OFF = "bool           EnableD1TPWLifecycle               = false;"
D1_GATE_ON = "bool           EnableD1TPWLifecycle               = true;"
C044_GATE_OFF = "bool           EnableC044Lifecycle                = false;"
C044_GATE_ON = "bool           EnableC044Lifecycle                = true;"

PROFILES = {
    "baseline": {"name": "BASELINE", "d1_tpw": False, "c044": False},
    "r1-d1tpw": {"name": "R1_D1TPW", "d1_tpw": True, "c044": False},
    "r2-c044": {"name": "R2_C044", "d1_tpw": False, "c044": True},
}


def git_blob(repo: Path, rel: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), "hash-object", rel], text=True
    ).strip()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise ValueError(f"expected exactly one marker, found {count}: {old}")
    return text.replace(old, new, 1)


def verify_canonical(repo: Path, source: Path, raw: bytes, text: str) -> None:
    rel = source.relative_to(repo).as_posix()
    blob = git_blob(repo, rel)
    sha = sha256_bytes(raw)
    errors = []
    if blob != EXPECTED_BLOB:
        errors.append(f"blob={blob}")
    if sha != EXPECTED_SHA256:
        errors.append(f"sha256={sha}")
    if BUILD_MARKER not in text:
        errors.append("build marker missing")
    if VERSION_MARKER not in text:
        errors.append("property version marker missing")
    if text.count(D1_GATE_OFF) != 1 or D1_GATE_ON in text:
        errors.append("D1TPW baseline gate is not exact OFF")
    if text.count(C044_GATE_OFF) != 1 or C044_GATE_ON in text:
        errors.append("C044 baseline gate is not exact OFF")
    if errors:
        raise ValueError("canonical v4.59 identity/gate validation failed: " + "; ".join(errors))


def build(repo: Path, profile_key: str, output: Path, metadata: Path) -> dict:
    if profile_key not in PROFILES:
        raise ValueError(f"unsupported profile: {profile_key}")

    source = repo / "blueprint" / "source" / "BBMA_EA.mq4"
    if not source.is_file():
        raise ValueError(f"canonical source missing: {source}")
    raw = source.read_bytes()
    text = raw.decode("utf-8")
    verify_canonical(repo, source, raw, text)

    profile = PROFILES[profile_key]
    variant = text
    if profile["d1_tpw"]:
        variant = replace_once(variant, D1_GATE_OFF, D1_GATE_ON)
    if profile["c044"]:
        variant = replace_once(variant, C044_GATE_OFF, C044_GATE_ON)

    # Fail closed: only the requested approved gate may differ.
    expected = text
    if profile["d1_tpw"]:
        expected = expected.replace(D1_GATE_OFF, D1_GATE_ON, 1)
    if profile["c044"]:
        expected = expected.replace(C044_GATE_OFF, C044_GATE_ON, 1)
    if variant != expected:
        raise ValueError("variant differs from canonical outside approved gate replacement")

    output.parent.mkdir(parents=True, exist_ok=True)
    # Preserve the canonical newline bytes exactly on Windows runners. Using
    # write_text() would translate CRLF and can turn existing CRLF into CRCRLF.
    variant_raw = variant.encode("utf-8")
    output.write_bytes(variant_raw)

    record = {
        "schema": "BBMA_V459_RUNTIME_VARIANT_V1",
        "profile": profile["name"],
        "canonical_source": "blueprint/source/BBMA_EA.mq4",
        "canonical_blob": EXPECTED_BLOB,
        "canonical_sha256": EXPECTED_SHA256,
        "build": BUILD_MARKER,
        "property_version": "4.59",
        "gates": {"d1_tpw": profile["d1_tpw"], "c044": profile["c044"]},
        "variant_sha256": sha256_bytes(variant_raw),
        "semantic_scope": "canonical v4.59 plus approved lifecycle gate flip only",
    }
    metadata.parent.mkdir(parents=True, exist_ok=True)
    metadata.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return record


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--profile", required=True, choices=sorted(PROFILES))
    ap.add_argument("--output", required=True)
    ap.add_argument("--metadata", required=True)
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    record = build(repo, args.profile, Path(args.output).resolve(), Path(args.metadata).resolve())
    print(f"V459_VARIANT_BUILD=PASS PROFILE={record['profile']}")
    print(f"CANONICAL_BLOB={record['canonical_blob']}")
    print(f"CANONICAL_SHA256={record['canonical_sha256']}")
    print(f"VARIANT_SHA256={record['variant_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
