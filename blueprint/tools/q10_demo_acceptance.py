#!/usr/bin/env python3
"""Q10 demo acceptance orchestrator for the frozen BBMA Build 5.11 candidate.

Safety properties:
- binds runtime preparation to an exact frozen source/native EX4/settings identity;
- never stores or accepts broker credentials;
- refuses non-demo or disconnected account evidence;
- refuses candidate execution against a terminal path that is the declared primary terminal;
- persists resumable stage state using PASS/FAIL/INCOMPLETE/BLOCKED only;
- never converts marker presence into a stage PASS without explicit case assertions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

STATUS_VALUES = {"PASS", "FAIL", "INCOMPLETE", "BLOCKED"}
DEFAULT_MANIFEST = (
    Path(__file__).resolve().parents[1]
    / "runtime"
    / "q10_demo_acceptance"
    / "FINAL_BUILD511_CANDIDATE.json"
)
DEFAULT_MATRIX = (
    Path(__file__).resolve().parents[1]
    / "runtime"
    / "q10_demo_acceptance"
    / "FINAL_BUILD511_STAGE_MATRIX.json"
)
DEFAULT_HYBRID_POLICY = (
    Path(__file__).resolve().parents[1]
    / "runtime"
    / "q10_demo_acceptance"
    / "FINAL_BUILD511_HYBRID_EVIDENCE_POLICY.json"
)
DEMO_MARKER = "[Q10-DEMO-ID]"
ACCOUNT_REDACTIONS = (
    re.compile(r"(?i)\b(account|login)\s*[:=]\s*\d+"),
    re.compile(r"(?i)\b(accountnumber|account_number)\s*[:=]\s*\d+"),
)

STAGE_MARKERS = {
    "R3": (
        "[D1-03][OWNER]",
        "[D1O",
        "D1_OPP_EXTREME_TPW",
        "[P3M2][DECISION_FINAL]",
    ),
    "R4": (
        "[P3M2][M16_PASS]",
        "[P3M2][PREFLIGHT_PASS]",
        "[P3M2][EXEC]",
        "ValidateCandle=",
        "OrderOpen=",
        "SL=",
    ),
    "R5": (
        "TradeLock",
        "REJ_TOTAL_RISK",
        "[P3S5][EXEC_ID]",
        "[F7-TELEM]",
        "REC_",
        "[P3M2][PREFLIGHT",
        "[P3M2][EXEC]",
    ),
    "R6": (
        "[N1-NMJE]",
        "[N2-NMJE-DEC]",
        "[N2-NMJE-OUT]",
        "N3_POLICY_ACTIVE",
        "N3_EXECUTION_POLICY",
    ),
}


class Q10Error(RuntimeError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest().upper()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def normalized_source_sha256(path: Path) -> str:
    raw = path.read_bytes().replace(b"\r\n", b"\n")
    return sha256_bytes(raw)


def git_output(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), *args], text=True, stderr=subprocess.STDOUT
    ).strip()


def verify_candidate(repo: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    source = repo / manifest["source_path"]
    if not source.is_file():
        raise Q10Error(f"candidate source missing: {source}")

    actual_source_sha = normalized_source_sha256(source)
    if actual_source_sha != manifest["source_sha256"]:
        raise Q10Error(
            f"candidate source SHA mismatch: expected={manifest['source_sha256']} "
            f"actual={actual_source_sha}"
        )

    text = source.read_text(encoding="utf-8")
    required = (
        f'#property version   "{manifest["property_version"]}"',
        f'#define BBMA_BUILD_TAG      "{manifest["build_tag"]}"',
        f'#define BBMA_SOURCE_REV_TAG "{manifest["source_rev_tag"]}"',
    )
    missing = [x for x in required if x not in text]
    if missing:
        raise Q10Error("candidate build markers missing: " + "; ".join(missing))

    freeze = manifest["candidate_freeze_commit"]
    source_at_freeze = subprocess.check_output(
        ["git", "-C", str(repo), "show", f"{freeze}:{manifest['source_path']}"]
    )
    freeze_sha = sha256_bytes(source_at_freeze.replace(b"\r\n", b"\n"))
    if freeze_sha != manifest["source_sha256"]:
        raise Q10Error(
            f"freeze commit source mismatch: expected={manifest['source_sha256']} "
            f"actual={freeze_sha}"
        )

    head = git_output(repo, "rev-parse", "HEAD")
    source_diff = subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "diff",
            "--exit-code",
            f"{freeze}..{head}",
            "--",
            manifest["source_path"],
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if source_diff.returncode != 0:
        raise Q10Error(
            "candidate source changed after freeze commit; refusing Q10 runtime preparation"
        )

    return {
        "status": "PASS",
        "head": head,
        "freeze_commit": freeze,
        "source_sha256": actual_source_sha,
        "source_neutral_after_freeze": True,
        "build": manifest["build"],
        "build_tag": manifest["build_tag"],
    }


def verify_runtime_artifacts(
    terminal_root: Path,
    native_ex4: Path,
    settings_file: Path,
    manifest: dict[str, Any],
    primary_terminal: Path | None = None,
) -> dict[str, Any]:
    root = terminal_root.resolve()
    terminal = (root / "terminal.exe").resolve()
    if not terminal.is_file():
        raise Q10Error(f"dedicated terminal.exe missing: {terminal}")
    experts_dir = root / "MQL4" / "Experts"
    if not experts_dir.is_dir():
        raise Q10Error(f"dedicated Experts directory missing: {experts_dir}")

    ex4 = native_ex4.resolve()
    settings = settings_file.resolve()
    if not ex4.is_file():
        raise Q10Error(f"native candidate EX4 missing: {ex4}")
    if not settings.is_file():
        raise Q10Error(f"candidate settings missing: {settings}")

    try:
        ex4.relative_to(root)
    except ValueError as exc:
        raise Q10Error("candidate EX4 must reside under the dedicated terminal root") from exc
    try:
        settings.relative_to(root)
    except ValueError as exc:
        raise Q10Error("candidate settings must reside under the dedicated terminal root") from exc

    if primary_terminal is not None and terminal == primary_terminal.resolve():
        raise Q10Error("dedicated terminal path equals declared primary terminal path")

    ex4_sha = sha256_file(ex4)
    settings_sha = sha256_file(settings)
    if ex4_sha != manifest["native_ex4_sha256"]:
        raise Q10Error(
            f"native EX4 SHA mismatch: expected={manifest['native_ex4_sha256']} actual={ex4_sha}"
        )
    if settings_sha != manifest["settings_sha256"]:
        raise Q10Error(
            f"settings SHA mismatch: expected={manifest['settings_sha256']} actual={settings_sha}"
        )

    return {
        "status": "PASS",
        "terminal": str(terminal),
        "terminal_root": str(root),
        "native_ex4": str(ex4),
        "native_ex4_sha256": ex4_sha,
        "settings_file": str(settings),
        "settings_sha256": settings_sha,
    }


def parse_probe_line(line: str) -> dict[str, str]:
    pos = line.find(DEMO_MARKER)
    if pos < 0:
        raise Q10Error("not a Q10 demo identity line")
    payload = line[pos + len(DEMO_MARKER) :]
    if payload.startswith("|"):
        payload = payload[1:]
    out: dict[str, str] = {}
    for part in payload.split("|"):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def verify_probe_artifact(
    terminal_root: Path,
    probe_ex4: Path,
    manifest: dict[str, Any],
    primary_terminal: Path | None = None,
) -> dict[str, Any]:
    root = terminal_root.resolve()
    terminal = (root / "terminal.exe").resolve()
    if not terminal.is_file():
        raise Q10Error(f"dedicated terminal.exe missing: {terminal}")
    experts_dir = root / "MQL4" / "Experts"
    if not experts_dir.is_dir():
        raise Q10Error(f"dedicated Experts directory missing: {experts_dir}")

    probe = probe_ex4.resolve()
    if not probe.is_file():
        raise Q10Error(f"demo identity probe EX4 missing: {probe}")
    try:
        probe.relative_to(root)
    except ValueError as exc:
        raise Q10Error("demo probe EX4 must reside under the dedicated terminal root") from exc

    if primary_terminal is not None and terminal == primary_terminal.resolve():
        raise Q10Error("dedicated terminal path equals declared primary terminal path")

    actual = sha256_file(probe)
    if actual != manifest["demo_probe_ex4_sha256"]:
        raise Q10Error(
            f"demo probe EX4 SHA mismatch: expected={manifest['demo_probe_ex4_sha256']} actual={actual}"
        )
    return {
        "status": "PASS",
        "terminal": str(terminal),
        "probe_ex4": str(probe),
        "probe_ex4_sha256": actual,
    }


def generate_probe_launch_config(
    terminal_root: Path,
    probe_ex4: Path,
    output_ini: Path,
    symbol: str,
    period: str,
    manifest: dict[str, Any],
    primary_terminal: Path | None = None,
) -> dict[str, Any]:
    runtime = verify_probe_artifact(
        terminal_root, probe_ex4, manifest, primary_terminal
    )
    config = "\n".join(
        [
            "Profile=default",
            "ExpertsEnable=true",
            "ExpertsDllImport=false",
            "ExpertsExpImport=false",
            "ExpertsTrades=false",
            f"Symbol={symbol}",
            f"Period={period}",
            f"Expert={probe_ex4.stem}",
            "",
        ]
    )
    lowered = config.lower()
    if "login=" in lowered or "password=" in lowered:
        raise Q10Error("credential field unexpectedly present in probe config")
    output_ini.parent.mkdir(parents=True, exist_ok=True)
    output_ini.write_text(config, encoding="utf-8", newline="\n")
    terminal = terminal_root.resolve() / "terminal.exe"
    return {
        "status": "PASS",
        "command": f'"{terminal}" /portable "{output_ini}"',
        "config_path": str(output_ini.resolve()),
        "config_sha256": sha256_file(output_ini),
        "contains_credentials": False,
        "experts_trades": False,
        "runtime": runtime,
    }


def inspect_demo_log(log_path: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    if not log_path.is_file():
        return {
            "status": "BLOCKED",
            "reason": "DEMO_LOG_MISSING",
            "log_path": str(log_path),
        }

    last: dict[str, str] | None = None
    marker_count = 0
    with log_path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if DEMO_MARKER in line and "|Demo=" in line:
                marker_count += 1
                last = parse_probe_line(line)

    if last is None:
        return {
            "status": "BLOCKED",
            "reason": "DEMO_IDENTITY_MARKER_MISSING",
            "log_path": str(log_path),
            "log_sha256": sha256_file(log_path),
        }

    demo = last.get("Demo", "").upper() == "Y"
    connected = last.get("Connected", "").upper() == "Y"
    server = last.get("Server", "")
    company = last.get("Company", "")
    haystack = f"{server} {company}".lower()
    provider_allowed = any(
        token.lower() in haystack for token in manifest["broker_tokens"]
    )

    reasons = []
    if not demo:
        reasons.append("ACCOUNT_NOT_DEMO")
    if not connected:
        reasons.append("NOT_CONNECTED")
    if not provider_allowed:
        reasons.append("DEMO_PROVIDER_NOT_ALLOWED")

    return {
        "status": "PASS" if not reasons else "BLOCKED",
        "reason": "OK" if not reasons else ",".join(reasons),
        "marker_count": marker_count,
        "demo": demo,
        "connected": connected,
        "trade_allowed_observed": last.get("TradeAllowed", "").upper() == "Y",
        "server": server,
        "company": company,
        "terminal_build": last.get("TerminalBuild", ""),
        "log_path": str(log_path),
        "log_sha256": sha256_file(log_path),
    }


def require_path_under(path: Path, root: Path, label: str) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise Q10Error(f"{label} must reside under the dedicated terminal root") from exc
    return resolved


def initial_state(
    manifest: dict[str, Any],
    matrix: dict[str, Any],
    candidate: dict[str, Any],
    demo: dict[str, Any],
    runtime: dict[str, Any] | None,
) -> dict[str, Any]:
    stages = {
        stage: {"status": "INCOMPLETE", "evidence": []}
        for stage in matrix["stage_order"]
    }
    return {
        "schema": "BBMA_Q10_STATE_V1",
        "issue": manifest["issue"],
        "candidate": candidate,
        "candidate_manifest_sha256": sha256_file(DEFAULT_MANIFEST)
        if DEFAULT_MANIFEST.is_file()
        else None,
        "demo_auth": demo,
        "runtime_artifacts": runtime,
        "stage_order": matrix["stage_order"],
        "stages": stages,
    }


def next_stage(state: dict[str, Any]) -> dict[str, str]:
    if state.get("demo_auth", {}).get("status") != "PASS":
        return {"status": "BLOCKED", "next": "AUTH"}
    for stage in state["stage_order"]:
        status = state["stages"][stage]["status"]
        if status == "FAIL":
            return {"status": "FAIL", "next": stage}
        if status != "PASS":
            return {"status": status, "next": stage}
    return {"status": "PASS", "next": "COMPLETE"}


def redact_line(line: str) -> str:
    out = line.rstrip("\r\n")
    for pattern in ACCOUNT_REDACTIONS:
        out = pattern.sub(lambda m: f"{m.group(1)}=<redacted>", out)
    return out


def collect_stage_log(
    stage: str,
    log_path: Path,
    out_dir: Path,
    state: dict[str, Any],
) -> dict[str, Any]:
    if state.get("demo_auth", {}).get("status") != "PASS":
        raise Q10Error("demo authentication gate is not PASS")
    runtime = state.get("runtime_artifacts")
    if not runtime or runtime.get("status") != "PASS":
        raise Q10Error("runtime artifacts are not bound to the authenticated demo terminal")
    if stage not in STAGE_MARKERS:
        raise Q10Error(f"unsupported stage: {stage}")
    log_path = require_path_under(
        log_path, Path(runtime["terminal_root"]), "runtime log"
    )
    if not log_path.is_file():
        raise Q10Error(f"runtime log missing: {log_path}")

    markers = STAGE_MARKERS[stage]
    counts = {m: 0 for m in markers}
    matched: list[str] = []
    with log_path.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if any(marker in line for marker in markers):
                cleaned = redact_line(line)
                matched.append(cleaned)
                for marker in markers:
                    if marker in line:
                        counts[marker] += 1

    out_dir.mkdir(parents=True, exist_ok=True)
    excerpt = out_dir / f"{stage}_matched.log"
    excerpt.write_text("\n".join(matched) + ("\n" if matched else ""), encoding="utf-8")
    bundle = {
        "schema": "BBMA_Q10_STAGE_BUNDLE_V1",
        "stage": stage,
        "candidate_source_sha256": state["candidate"]["source_sha256"],
        "candidate_build_tag": state["candidate"]["build_tag"],
        "demo_evidence_sha256": state["demo_auth"].get("log_sha256"),
        "raw_log_path": str(log_path),
        "raw_log_sha256": sha256_file(log_path),
        "matched_excerpt": str(excerpt),
        "matched_excerpt_sha256": sha256_file(excerpt),
        "marker_counts": counts,
        "marker_lines": len(matched),
    }
    bundle_path = out_dir / f"{stage}_bundle.json"
    write_json(bundle_path, bundle)
    return bundle


def _resolved_evidence_path(value: str, base_dir: Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = base_dir / path
    return path.resolve()


def validate_bundle_integrity(stage: str, bundle: dict[str, Any]) -> dict[str, Any]:
    if bundle.get("schema") != "BBMA_Q10_STAGE_BUNDLE_V1":
        raise Q10Error("invalid stage bundle schema")
    if bundle.get("stage") != stage:
        raise Q10Error(
            f"stage bundle mismatch: expected={stage} actual={bundle.get('stage')}"
        )
    if not bundle.get("candidate_source_sha256") or not bundle.get("candidate_build_tag"):
        raise Q10Error("stage bundle missing candidate identity")
    if not bundle.get("demo_evidence_sha256"):
        raise Q10Error("stage bundle missing demo identity hash")

    for path_key, hash_key in (
        ("raw_log_path", "raw_log_sha256"),
        ("matched_excerpt", "matched_excerpt_sha256"),
    ):
        path = Path(str(bundle.get(path_key, ""))).resolve()
        expected = str(bundle.get(hash_key, "")).upper()
        if not path.is_file():
            raise Q10Error(f"bundle evidence missing: {path_key}={path}")
        actual = sha256_file(path)
        if not expected or actual != expected:
            raise Q10Error(
                f"bundle evidence hash mismatch: {path_key} expected={expected} actual={actual}"
            )
    return bundle


def validate_case_evidence(
    evidence: Any,
    assertions_dir: Path,
    bundle: dict[str, Any],
    case_id: str,
) -> list[dict[str, str]]:
    if not isinstance(evidence, list) or not evidence:
        raise Q10Error(f"{case_id} PASS/FAIL requires attributable evidence")

    known = {}
    for path_key, hash_key in (
        ("raw_log_path", "raw_log_sha256"),
        ("matched_excerpt", "matched_excerpt_sha256"),
    ):
        known[str(Path(bundle[path_key]).resolve())] = str(bundle[hash_key]).upper()

    validated: list[dict[str, str]] = []
    for ref in evidence:
        if isinstance(ref, str):
            path_text = ref
            expected = None
        elif isinstance(ref, dict):
            path_text = str(ref.get("path", ""))
            expected = str(ref.get("sha256", "")).upper() or None
        else:
            raise Q10Error(f"{case_id} has invalid evidence reference type")

        if not path_text:
            raise Q10Error(f"{case_id} has empty evidence path")
        path = _resolved_evidence_path(path_text, assertions_dir)
        if not path.is_file():
            raise Q10Error(f"{case_id} evidence missing: {path}")
        actual = sha256_file(path)
        if expected is not None and actual != expected:
            raise Q10Error(
                f"{case_id} evidence SHA mismatch: expected={expected} actual={actual}"
            )
        known_expected = known.get(str(path))
        if known_expected is None:
            raise Q10Error(
                f"{case_id} evidence is not registered in the collected stage bundle: {path}"
            )
        if actual != known_expected:
            raise Q10Error(
                f"{case_id} evidence no longer matches the collected bundle: {path}"
            )
        validated.append({"path": str(path), "sha256": actual})
    return validated


def validate_hybrid_policy(
    policy: dict[str, Any], matrix: dict[str, Any]
) -> None:
    if policy.get("schema") != "BBMA_Q10_HYBRID_EVIDENCE_POLICY_V2":
        raise Q10Error("invalid hybrid evidence policy schema")
    if policy.get("candidate") != matrix.get("candidate"):
        raise Q10Error("hybrid policy candidate mismatch")
    for stage in matrix["stage_order"]:
        if stage not in policy.get("stages", {}):
            raise Q10Error(f"hybrid policy missing stage: {stage}")
        matrix_ids = {row["id"] for row in matrix["stages"][stage]["cases"]}
        spec = policy["stages"][stage]
        historical = set(spec.get("historical_required_cases", []))
        live_only = set(spec.get("live_only_cases", []))
        live_reconfirm = set(spec.get("live_reconfirm_cases", []))
        if historical & live_only:
            raise Q10Error(f"hybrid policy overlap in {stage}")
        if historical | live_only != matrix_ids:
            raise Q10Error(f"hybrid policy case partition mismatch in {stage}")
        if not live_reconfirm <= historical:
            raise Q10Error(f"hybrid policy live reconfirm mismatch in {stage}")


def required_case_ids(
    stage: str,
    matrix: dict[str, Any],
    policy: dict[str, Any] | None = None,
    evidence_mode: str = "FULL",
) -> set[str]:
    if stage not in matrix["stages"]:
        raise Q10Error(f"unknown stage: {stage}")
    if evidence_mode == "FULL":
        return {
            row["id"]
            for row in matrix["stages"][stage]["cases"]
            if row.get("required", False)
        }
    if evidence_mode != "LIVE_RECONFIRM":
        raise Q10Error(f"unsupported evidence mode: {evidence_mode}")
    if policy is None:
        raise Q10Error("LIVE_RECONFIRM requires hybrid evidence policy")
    validate_hybrid_policy(policy, matrix)
    spec = policy["stages"][stage]
    live_cases = set(spec["live_only_cases"]) | set(spec["live_reconfirm_cases"])
    mandatory = {
        row["id"]
        for row in matrix["stages"][stage]["cases"]
        if row.get("required", False)
    }
    return live_cases & mandatory


def validate_phase_h_for_live(
    phase_h: dict[str, Any], policy: dict[str, Any], matrix: dict[str, Any]
) -> None:
    validate_hybrid_policy(policy, matrix)
    if phase_h.get("candidate") != policy.get("candidate"):
        raise Q10Error("Phase H candidate mismatch")
    if phase_h.get("fail_count") != 0 or phase_h.get("fail_cases"):
        raise Q10Error("Phase H contains FAIL")
    if phase_h.get("hold_cases"):
        raise Q10Error("Phase H contains unresolved HOLD")
    if phase_h.get("mandatory_safe_work_remaining"):
        raise Q10Error("Phase H mandatory safe work remains")
    incomplete = set(phase_h.get("incomplete_cases", []))
    conditional = set(phase_h.get("conditional_incomplete_cases", []))
    if incomplete - conditional:
        raise Q10Error("Phase H has non-conditional INCOMPLETE cases")
    matrix_defs = {
        row["id"]: row
        for stage in matrix["stage_order"]
        for row in matrix["stages"][stage]["cases"]
    }
    for case_id in conditional:
        if case_id not in matrix_defs:
            raise Q10Error(f"Phase H conditional case unknown: {case_id}")
        if matrix_defs[case_id].get("required", False):
            raise Q10Error(f"Phase H conditional case is mandatory: {case_id}")
    if phase_h.get("phase_l_allowed") is not True:
        raise Q10Error("Phase H does not allow Phase L")
    if phase_h.get("phase_l_blocker") not in (None, ""):
        raise Q10Error("Phase H has a Phase L blocker")


def prepare_live_state(
    prior_state: dict[str, Any],
    phase_h_path: Path,
    policy_path: Path,
    matrix: dict[str, Any],
    manifest: dict[str, Any],
    repo_root: Path,
    primary_terminal: Path,
) -> dict[str, Any]:
    if prior_state.get("demo_auth", {}).get("status") != "PASS":
        raise Q10Error("prior demo authentication is not PASS")
    if prior_state.get("runtime_artifacts", {}).get("status") != "PASS":
        raise Q10Error("prior runtime artifacts are not PASS")

    policy = load_json(policy_path)
    phase_h = load_json(phase_h_path)
    validate_phase_h_for_live(phase_h, policy, matrix)

    candidate = verify_candidate(repo_root.resolve(), manifest)
    previous_candidate = prior_state.get("candidate", {})
    if previous_candidate.get("source_sha256") != candidate.get("source_sha256"):
        raise Q10Error("prior state candidate source mismatch")
    if previous_candidate.get("build_tag") != candidate.get("build_tag"):
        raise Q10Error("prior state candidate build mismatch")

    runtime_before = prior_state["runtime_artifacts"]
    runtime = verify_runtime_artifacts(
        Path(runtime_before["terminal_root"]),
        Path(runtime_before["native_ex4"]),
        Path(runtime_before["settings_file"]),
        manifest,
        primary_terminal=primary_terminal,
    )

    demo_log = require_path_under(
        Path(prior_state["demo_auth"]["log_path"]),
        Path(runtime["terminal_root"]),
        "demo identity log",
    )
    if sha256_file(demo_log) != str(prior_state["demo_auth"]["log_sha256"]).upper():
        raise Q10Error("prior demo identity log hash changed")
    demo = inspect_demo_log(demo_log, manifest)
    if demo.get("status") != "PASS":
        raise Q10Error("demo authentication no longer PASS")

    state = initial_state(manifest, matrix, candidate, demo, runtime)
    state["schema"] = "BBMA_Q10_STATE_V2"
    state["phase"] = "LIVE_RECONFIRM"
    state["hybrid_policy_sha256"] = sha256_file(policy_path)
    state["phase_h"] = {
        "path": str(phase_h_path.resolve()),
        "sha256": sha256_file(phase_h_path),
        "status": phase_h.get("phase_h_status"),
        "pass_count": phase_h.get("pass_count"),
        "incomplete_count": phase_h.get("incomplete_count"),
        "fail_count": phase_h.get("fail_count"),
    }
    return state


def analyze_assertions(
    stage: str,
    assertions_path: Path,
    matrix: dict[str, Any],
    bundle: dict[str, Any],
    policy: dict[str, Any] | None = None,
    evidence_mode: str = "FULL",
) -> dict[str, Any]:
    if stage not in matrix["stages"]:
        raise Q10Error(f"unknown stage: {stage}")
    validate_bundle_integrity(stage, bundle)
    assertions = load_json(assertions_path)
    rows = assertions.get("cases", {})
    if not isinstance(rows, dict):
        raise Q10Error("assertions cases must be an object")
    defined = {x["id"]: x for x in matrix["stages"][stage]["cases"]}
    unknown = sorted(set(rows) - set(defined))
    if unknown:
        raise Q10Error("unknown case IDs: " + ", ".join(unknown))

    required_ids = required_case_ids(stage, matrix, policy, evidence_mode)
    results: dict[str, Any] = {}
    any_fail = False
    missing_required = False
    for case_id, case_def in defined.items():
        row = rows.get(case_id, {})
        status = row.get("status", "INCOMPLETE")
        if status not in STATUS_VALUES:
            raise Q10Error(f"invalid status for {case_id}: {status}")
        evidence = row.get("evidence", [])
        if status in {"PASS", "FAIL"}:
            evidence = validate_case_evidence(
                evidence, assertions_path.resolve().parent, bundle, case_id
            )
        elif evidence:
            evidence = validate_case_evidence(
                evidence, assertions_path.resolve().parent, bundle, case_id
            )
        if status == "FAIL":
            any_fail = True
        case_required = case_id in required_ids
        if case_required and status != "PASS":
            missing_required = True
        results[case_id] = {
            "status": status,
            "required": case_required,
            "evidence": evidence,
        }

    if any_fail:
        overall = "FAIL"
    elif missing_required:
        overall = "INCOMPLETE"
    else:
        overall = "PASS"

    return {
        "schema": "BBMA_Q10_STAGE_ANALYSIS_V1",
        "stage": stage,
        "status": overall,
        "evidence_mode": evidence_mode,
        "required_case_ids": sorted(required_ids),
        "candidate_source_sha256": bundle["candidate_source_sha256"],
        "candidate_build_tag": bundle["candidate_build_tag"],
        "bundle_sha256": sha256_bytes(
            json.dumps(bundle, sort_keys=True).encode("utf-8")
        ),
        "cases": results,
    }


def record_stage(
    state: dict[str, Any], stage: str, status: str, evidence: str | None
) -> dict[str, Any]:
    if status not in STATUS_VALUES:
        raise Q10Error(f"invalid status: {status}")
    if stage not in state["stages"]:
        raise Q10Error(f"unknown stage: {stage}")
    if not evidence:
        raise Q10Error("stage recording requires an attributable analysis artifact")

    evidence_path = Path(evidence).resolve()
    if not evidence_path.is_file():
        raise Q10Error(f"stage analysis missing: {evidence_path}")
    analysis = load_json(evidence_path)
    if analysis.get("schema") != "BBMA_Q10_STAGE_ANALYSIS_V1":
        raise Q10Error("invalid stage analysis schema")
    if analysis.get("stage") != stage:
        raise Q10Error("stage analysis stage mismatch")
    if analysis.get("status") != status:
        raise Q10Error("stage status does not match analysis artifact")
    if analysis.get("candidate_source_sha256") != state["candidate"]["source_sha256"]:
        raise Q10Error("stage analysis candidate source mismatch")
    if analysis.get("candidate_build_tag") != state["candidate"]["build_tag"]:
        raise Q10Error("stage analysis candidate build mismatch")
    if state.get("phase") == "LIVE_RECONFIRM" and analysis.get("evidence_mode") != "LIVE_RECONFIRM":
        raise Q10Error("live state requires LIVE_RECONFIRM analysis")

    state["stages"][stage]["status"] = status
    state["stages"][stage].setdefault("evidence", []).append(
        {"path": str(evidence_path), "sha256": sha256_file(evidence_path)}
    )
    return state


def generate_launch_config(
    stage: str,
    state: dict[str, Any],
    terminal_root: Path,
    native_ex4: Path,
    settings_file: Path,
    output_ini: Path,
    symbol: str,
    period: str,
    manifest: dict[str, Any],
    primary_terminal: Path | None = None,
) -> dict[str, Any]:
    if state.get("demo_auth", {}).get("status") != "PASS":
        raise Q10Error("refusing launch config: demo authentication is not PASS")
    if stage not in state["stage_order"]:
        raise Q10Error(f"unknown stage: {stage}")

    expected = next_stage(state)
    if expected["status"] == "FAIL":
        raise Q10Error(f"refusing launch after failed stage: {expected['next']}")
    if expected["next"] != stage:
        raise Q10Error(
            f"stage ordering violation: next formal stage is {expected['next']}, requested {stage}"
        )

    bound = state.get("runtime_artifacts")
    if not bound or bound.get("status") != "PASS":
        raise Q10Error("runtime artifacts are not bound to the authenticated demo terminal")

    runtime = verify_runtime_artifacts(
        terminal_root=terminal_root,
        native_ex4=native_ex4,
        settings_file=settings_file,
        manifest=manifest,
        primary_terminal=primary_terminal,
    )
    if Path(bound["terminal_root"]).resolve() != Path(runtime["terminal_root"]).resolve():
        raise Q10Error("runtime terminal differs from authenticated demo terminal")
    if str(bound.get("native_ex4_sha256", "")).upper() != runtime["native_ex4_sha256"]:
        raise Q10Error("runtime EX4 differs from authenticated demo state")
    if str(bound.get("settings_sha256", "")).upper() != runtime["settings_sha256"]:
        raise Q10Error("runtime settings differ from authenticated demo state")
    expert_name = native_ex4.stem
    config = "\n".join(
        [
            "Profile=default",
            "ExpertsEnable=true",
            "ExpertsDllImport=false",
            "ExpertsExpImport=false",
            "ExpertsTrades=true",
            f"Symbol={symbol}",
            f"Period={period}",
            f"Expert={expert_name}",
            f"ExpertParameters={settings_file.name}",
            "",
        ]
    )
    lowered = config.lower()
    if "login=" in lowered or "password=" in lowered:
        raise Q10Error("credential field unexpectedly present in generated config")

    output_ini.parent.mkdir(parents=True, exist_ok=True)
    output_ini.write_text(config, encoding="utf-8", newline="\n")
    terminal = terminal_root.resolve() / "terminal.exe"
    command = f'"{terminal}" /portable "{output_ini}"'
    return {
        "status": "PASS",
        "stage": stage,
        "command": command,
        "config_path": str(output_ini.resolve()),
        "config_sha256": sha256_file(output_ini),
        "runtime": runtime,
        "contains_credentials": False,
    }


def cmd_verify(args: argparse.Namespace) -> int:
    manifest = load_json(Path(args.manifest))
    result = verify_candidate(Path(args.repo_root).resolve(), manifest)
    print(json.dumps(result, indent=2))
    return 0


def cmd_probe_launch(args: argparse.Namespace) -> int:
    manifest = load_json(Path(args.manifest))
    result = generate_probe_launch_config(
        Path(args.terminal_root),
        Path(args.probe_ex4),
        Path(args.output_ini),
        args.symbol,
        args.period,
        manifest,
        Path(args.primary_terminal) if args.primary_terminal else None,
    )
    if args.output_plan:
        write_json(Path(args.output_plan), result)
    print(json.dumps(result, indent=2))
    return 0


def cmd_inspect_demo(args: argparse.Namespace) -> int:
    manifest = load_json(Path(args.manifest))
    result = inspect_demo_log(Path(args.log), manifest)
    if args.output:
        write_json(Path(args.output), result)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "PASS" else 2


def cmd_init_state(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest)
    matrix_path = Path(args.matrix)
    manifest = load_json(manifest_path)
    matrix = load_json(matrix_path)
    candidate = verify_candidate(Path(args.repo_root).resolve(), manifest)
    demo = inspect_demo_log(Path(args.demo_log), manifest)
    runtime = None
    supplied_runtime = [args.terminal_root, args.native_ex4, args.settings]
    if any(supplied_runtime) and not all(supplied_runtime):
        raise Q10Error("terminal-root, native-ex4 and settings must be supplied together")
    if all(supplied_runtime):
        runtime = verify_runtime_artifacts(
            Path(args.terminal_root),
            Path(args.native_ex4),
            Path(args.settings),
            manifest,
            Path(args.primary_terminal) if args.primary_terminal else None,
        )
    if demo["status"] == "PASS":
        if runtime is None:
            raise Q10Error("authenticated demo state requires bound runtime artifacts")
        require_path_under(
            Path(args.demo_log), Path(runtime["terminal_root"]), "demo identity log"
        )
        if not args.primary_terminal:
            raise Q10Error("authenticated demo state requires primary-terminal guard")
    state = initial_state(manifest, matrix, candidate, demo, runtime)
    state["candidate_manifest_sha256"] = sha256_file(manifest_path)
    state["matrix_sha256"] = sha256_file(matrix_path)
    write_json(Path(args.output), state)
    print(json.dumps(next_stage(state), indent=2))
    return 0 if demo["status"] == "PASS" else 2


def cmd_init_live(args: argparse.Namespace) -> int:
    manifest_path = Path(args.manifest)
    matrix_path = Path(args.matrix)
    policy_path = Path(args.hybrid_policy)
    prior_state = load_json(Path(args.prior_state))
    manifest = load_json(manifest_path)
    matrix = load_json(matrix_path)
    state = prepare_live_state(
        prior_state=prior_state,
        phase_h_path=Path(args.phase_h),
        policy_path=policy_path,
        matrix=matrix,
        manifest=manifest,
        repo_root=Path(args.repo_root),
        primary_terminal=Path(args.primary_terminal),
    )
    state["candidate_manifest_sha256"] = sha256_file(manifest_path)
    state["matrix_sha256"] = sha256_file(matrix_path)
    write_json(Path(args.output), state)
    print(json.dumps(next_stage(state), indent=2))
    return 0


def cmd_next(args: argparse.Namespace) -> int:
    state = load_json(Path(args.state))
    result = next_stage(state)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] in {"PASS", "INCOMPLETE"} else 2


def cmd_record(args: argparse.Namespace) -> int:
    path = Path(args.state)
    state = load_json(path)
    state = record_stage(state, args.stage, args.status, args.evidence)
    write_json(path, state)
    print(json.dumps(next_stage(state), indent=2))
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    state = load_json(Path(args.state))
    manifest = load_json(Path(args.manifest))
    result = generate_launch_config(
        args.stage,
        state,
        Path(args.terminal_root),
        Path(args.native_ex4),
        Path(args.settings),
        Path(args.output_ini),
        args.symbol,
        args.period,
        manifest,
        Path(args.primary_terminal) if args.primary_terminal else None,
    )
    if args.output_plan:
        write_json(Path(args.output_plan), result)
    print(json.dumps(result, indent=2))
    return 0


def cmd_collect(args: argparse.Namespace) -> int:
    state = load_json(Path(args.state))
    bundle = collect_stage_log(
        args.stage, Path(args.log), Path(args.output_dir), state
    )
    print(json.dumps(bundle, indent=2))
    return 0


def cmd_analyze(args: argparse.Namespace) -> int:
    matrix = load_json(Path(args.matrix))
    bundle = load_json(Path(args.bundle))
    policy = None
    if args.evidence_mode == "LIVE_RECONFIRM":
        policy = load_json(Path(args.hybrid_policy))
    result = analyze_assertions(
        args.stage,
        Path(args.assertions),
        matrix,
        bundle,
        policy=policy,
        evidence_mode=args.evidence_mode,
    )
    if args.output:
        write_json(Path(args.output), result)
    print(json.dumps({"stage": args.stage, "status": result["status"]}, indent=2))
    return 0 if result["status"] == "PASS" else 2


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    p.add_argument("--matrix", default=str(DEFAULT_MATRIX))
    p.add_argument("--hybrid-policy", default=str(DEFAULT_HYBRID_POLICY))
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("verify-candidate")
    s.add_argument("--repo-root", required=True)
    s.set_defaults(func=cmd_verify)

    s = sub.add_parser("generate-probe-launch")
    s.add_argument("--terminal-root", required=True)
    s.add_argument("--probe-ex4", required=True)
    s.add_argument("--output-ini", required=True)
    s.add_argument("--output-plan")
    s.add_argument("--primary-terminal", required=True)
    s.add_argument("--symbol", default="GBPUSD")
    s.add_argument("--period", default="M15")
    s.set_defaults(func=cmd_probe_launch)

    s = sub.add_parser("inspect-demo")
    s.add_argument("--log", required=True)
    s.add_argument("--output")
    s.set_defaults(func=cmd_inspect_demo)

    s = sub.add_parser("init-state")
    s.add_argument("--repo-root", required=True)
    s.add_argument("--demo-log", required=True)
    s.add_argument("--output", required=True)
    s.add_argument("--terminal-root")
    s.add_argument("--native-ex4")
    s.add_argument("--settings")
    s.add_argument("--primary-terminal")
    s.set_defaults(func=cmd_init_state)

    s = sub.add_parser("init-live-state")
    s.add_argument("--repo-root", required=True)
    s.add_argument("--prior-state", required=True)
    s.add_argument("--phase-h", required=True)
    s.add_argument("--primary-terminal", required=True)
    s.add_argument("--output", required=True)
    s.set_defaults(func=cmd_init_live)

    s = sub.add_parser("next-stage")
    s.add_argument("--state", required=True)
    s.set_defaults(func=cmd_next)

    s = sub.add_parser("record-stage")
    s.add_argument("--state", required=True)
    s.add_argument("--stage", required=True)
    s.add_argument("--status", required=True, choices=sorted(STATUS_VALUES))
    s.add_argument("--evidence", required=True)
    s.set_defaults(func=cmd_record)

    s = sub.add_parser("generate-launch")
    s.add_argument("--state", required=True)
    s.add_argument("--stage", required=True)
    s.add_argument("--terminal-root", required=True)
    s.add_argument("--native-ex4", required=True)
    s.add_argument("--settings", required=True)
    s.add_argument("--output-ini", required=True)
    s.add_argument("--output-plan")
    s.add_argument("--primary-terminal", required=True)
    s.add_argument("--symbol", default="GBPUSD")
    s.add_argument("--period", default="M15")
    s.set_defaults(func=cmd_generate)

    s = sub.add_parser("collect-log")
    s.add_argument("--state", required=True)
    s.add_argument("--stage", required=True)
    s.add_argument("--log", required=True)
    s.add_argument("--output-dir", required=True)
    s.set_defaults(func=cmd_collect)

    s = sub.add_parser("analyze-bundle")
    s.add_argument("--stage", required=True)
    s.add_argument("--bundle", required=True)
    s.add_argument("--assertions", required=True)
    s.add_argument("--evidence-mode", choices=("FULL", "LIVE_RECONFIRM"), default="FULL")
    s.add_argument("--output")
    s.set_defaults(func=cmd_analyze)
    return p


def main() -> int:
    try:
        args = build_parser().parse_args()
        return args.func(args)
    except (Q10Error, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(f"Q10=FAIL_CLOSED {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
