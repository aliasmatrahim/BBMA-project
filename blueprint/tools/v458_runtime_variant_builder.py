#!/usr/bin/env python3
"""Build source-bound v4.58 broker-runtime test variants without modifying canonical EA source.

The builder reads the canonical source as a raw Git blob, verifies its exact identity,
and emits TEST-ONLY variants. Only lifecycle feature gates may change; canonical
source is never written by this tool.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

CANONICAL_PATH = "blueprint/source/BBMA_EA.mq4"
EXPECTED_BLOB = "a166ffb23aba5e6b4011a28d9de8896cd00e33a1"
EXPECTED_SHA256 = "ba2e5815d1b221d7bba46ed0be4793aa5bc6154e29e9b19562dfffbd28c8f0bc"
BUILD_MARKER = "Version 4.5.8 - D1 TP-Wajib Lifecycle Stage"
VERSION_MARKER = '#property version   "4.58"'
# Exact canonical declarations are intentionally spacing-sensitive. If source
# layout/identity changes, this builder must fail closed and be re-audited.
D1_GATE_OFF = "bool           EnableD1TPWLifecycle               = false;"
D1_GATE_ON =  "bool           EnableD1TPWLifecycle               = true;"
C044_GATE_OFF = "bool           EnableC044Lifecycle                = false;"
C044_GATE_ON =  "bool           EnableC044Lifecycle                = true;"

PROFILES = {
    "baseline": {"d1_tpw": False, "c044": False},
    "r1-d1tpw": {"d1_tpw": True, "c044": False},
    "r2-c044": {"d1_tpw": False, "c044": True},
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha(repo_root: Path, path: str = CANONICAL_PATH) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", f"HEAD:{path}"], cwd=repo_root, text=True
    ).strip()


def read_raw_git_source(repo_root: Path, path: str = CANONICAL_PATH) -> tuple[bytes, str]:
    blob = git_blob_sha(repo_root, path)
    data = subprocess.check_output(["git", "cat-file", "blob", blob], cwd=repo_root)
    return data, blob


def verify_canonical(data: bytes, blob: str) -> str:
    if blob != EXPECTED_BLOB:
        raise ValueError(f"canonical blob mismatch: {blob} != {EXPECTED_BLOB}")
    digest = sha256_bytes(data)
    if digest != EXPECTED_SHA256:
        raise ValueError(f"canonical sha256 mismatch: {digest} != {EXPECTED_SHA256}")
    text = data.decode("utf-8")
    for marker in (BUILD_MARKER, VERSION_MARKER, D1_GATE_OFF, C044_GATE_OFF):
        if marker not in text:
            raise ValueError(f"missing canonical marker: {marker}")
    if text.count(D1_GATE_OFF) != 1 or text.count(C044_GATE_OFF) != 1:
        raise ValueError("lifecycle gate occurrence count is not exactly one")
    return text


def build_variant_from_text(text: str, profile: str) -> tuple[str, list[dict[str, str]]]:
    if profile not in PROFILES:
        raise ValueError(f"unsupported profile: {profile}")
    if text.count(D1_GATE_OFF) != 1 or text.count(C044_GATE_OFF) != 1:
        raise ValueError("input does not contain exactly one OFF gate for each lifecycle")

    out = text
    changes: list[dict[str, str]] = []
    if PROFILES[profile]["d1_tpw"]:
        out = out.replace(D1_GATE_OFF, D1_GATE_ON, 1)
        changes.append({"from": D1_GATE_OFF, "to": D1_GATE_ON})
    if PROFILES[profile]["c044"]:
        out = out.replace(C044_GATE_OFF, C044_GATE_ON, 1)
        changes.append({"from": C044_GATE_OFF, "to": C044_GATE_ON})

    expected_changes = 0 if profile == "baseline" else 1
    if len(changes) != expected_changes:
        raise ValueError("unexpected semantic change count")
    if profile == "r1-d1tpw" and C044_GATE_OFF not in out:
        raise ValueError("R1 must keep C044 OFF")
    if profile == "r2-c044" and D1_GATE_OFF not in out:
        raise ValueError("R2 must keep D1 TPW OFF")
    return out, changes


def build(repo_root: Path, profile: str, output: Path, metadata: Path | None = None) -> dict:
    data, blob = read_raw_git_source(repo_root)
    text = verify_canonical(data, blob)
    variant, changes = build_variant_from_text(text, profile)
    variant_bytes = variant.encode("utf-8")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(variant_bytes)
    payload = {
        "schema": "BBMA_V458_RUNTIME_VARIANT_V1",
        "test_only": True,
        "profile": profile,
        "canonical_path": CANONICAL_PATH,
        "canonical_blob": blob,
        "canonical_sha256": sha256_bytes(data),
        "variant_sha256": sha256_bytes(variant_bytes),
        "gates": PROFILES[profile],
        "changes": changes,
        "active_source_modified": False,
    }
    if metadata:
        metadata.parent.mkdir(parents=True, exist_ok=True)
        metadata.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo-root", type=Path, default=Path("."))
    p.add_argument("--profile", required=True, choices=sorted(PROFILES))
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--metadata", type=Path)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    payload = build(args.repo_root.resolve(), args.profile, args.output, args.metadata)
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
