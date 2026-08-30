#!/usr/bin/env python3
"""Pure-Python control and validation helpers for the MT4 v4.59 user-test runner."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SETTINGS_SCHEMA = "BBMA_V459_USER_TEST_SETTINGS_V1"
STATE_SCHEMA = "BBMA_V459_USER_TEST_STATE_V1"
REPORT_SCHEMA = "BBMA_V459_USER_TEST_STAGE_REPORT_V1"
STAGES = ("R1", "R2", "R3", "R4", "R5", "R6")
PROFILE_BY_STAGE = {
    "R1": "R1_D1TPW",
    "R2": "R2_C044",
    "R3": "BASELINE",
    "R4": "BASELINE",
    "R5": "BASELINE",
    "R6": "BASELINE",
}
CASES_BY_STAGE = {
    "R1": (
        "P0_EXEC_ID_DURABLE",
        "P0_RESTART_RECOVERY",
        "P0_EXEC_ID_UNIQUENESS",
        "R1_CHECKPOINT_RESTART",
        "R1_TPW_COMPLETION_CLOSE",
        "R1_IDEMPOTENCY",
    ),
    "R2": (
        "R2_CHECKPOINT_RESTART",
        "R2_FAILED_MOMENTUM_CLOSE",
        "R2_MOMENTUM_REARM",
        "R2_CYCLE_SUPERSESSION",
        "R2_M20_PRECEDENCE",
    ),
    "R3": ("R3_D1_OWNER_MATRIX", "R3_D1O_IDENTITY"),
    "R4": ("R4_VALIDATION_TIMING", "R4_M17_SL_GEOMETRY"),
    "R5": ("R5_TRADELOCK", "R5_CUMULATIVE_RISK", "R5_P3_BCD"),
    "R6": ("R6_N2_CHAIN", "N3_FIREWALL"),
}
FORBIDDEN_SETTING_KEYS = {"login", "password", "account", "token", "secret", "apikey", "api_key"}


def load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON object required: {path}")
    return payload


def _walk_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key).lower()
            yield from _walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_keys(child)


def validate_settings(payload: dict, *, check_paths: bool = True, check_profiles: bool = True) -> dict:
    if payload.get("schema") != SETTINGS_SCHEMA:
        raise ValueError(f"settings schema must be {SETTINGS_SCHEMA}")
    bad_keys = sorted(set(_walk_keys(payload)) & FORBIDDEN_SETTING_KEYS)
    if bad_keys:
        raise ValueError("credentials are forbidden in settings: " + ", ".join(bad_keys))
    if payload.get("require_demo_account") is not True:
        raise ValueError("require_demo_account must remain true")

    required_paths = ("terminal_path", "metaeditor_path", "data_path", "work_root")
    paths = {}
    for key in required_paths:
        raw = payload.get(key)
        if not isinstance(raw, str) or not raw.strip():
            raise ValueError(f"missing path setting: {key}")
        paths[key] = Path(raw).expanduser()
    if check_paths:
        for key in ("terminal_path", "metaeditor_path"):
            if not paths[key].is_file():
                raise ValueError(f"file not found for {key}: {paths[key]}")
        if not paths["data_path"].is_dir():
            raise ValueError(f"MT4 data_path not found: {paths['data_path']}")

    profiles = payload.get("profiles")
    if not isinstance(profiles, dict) or set(profiles) != set(STAGES):
        raise ValueError("profiles must contain exactly R1, R2, R3, R4, R5 and R6")
    for stage in STAGES:
        name = profiles[stage]
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9._ -]{1,64}", name):
            raise ValueError(f"invalid MT4 profile name for {stage}")
        if check_profiles:
            profile_dir = paths["data_path"] / "profiles" / name
            if not profile_dir.is_dir():
                raise ValueError(f"MT4 profile missing for {stage}: {profile_dir}")
    preflight = payload.get("preflight_profile")
    if not isinstance(preflight, str) or not re.fullmatch(r"[A-Za-z0-9._ -]{1,64}", preflight):
        raise ValueError("invalid MT4 preflight_profile name")
    if preflight in profiles.values():
        raise ValueError("preflight_profile must be separate from all trading profiles")
    if check_profiles:
        profile_dir = paths["data_path"] / "profiles" / preflight
        if not profile_dir.is_dir():
            raise ValueError(f"observer-only MT4 preflight profile missing: {profile_dir}")

    for key, low, high in (
        ("monitor_minutes", 1, 10080),
        ("startup_timeout_seconds", 15, 900),
        ("clean_shutdown_timeout_seconds", 10, 300),
        ("poll_seconds", 2, 60),
    ):
        value = payload.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or not low <= value <= high:
            raise ValueError(f"{key} must be an integer from {low} to {high}")
    if not isinstance(payload.get("portable_mode"), bool):
        raise ValueError("portable_mode must be true or false")
    if not isinstance(payload.get("auto_restart_on_checkpoint"), bool):
        raise ValueError("auto_restart_on_checkpoint must be true or false")
    return payload


def initial_state() -> dict:
    return {
        "schema": STATE_SCHEMA,
        "stages": {stage: {"status": "PENDING", "last_report": None} for stage in STAGES},
    }


def normalize_state(payload: dict | None) -> dict:
    if payload is None:
        return initial_state()
    if payload.get("schema") != STATE_SCHEMA or not isinstance(payload.get("stages"), dict):
        raise ValueError("invalid user-test state file")
    out = initial_state()
    for stage in STAGES:
        row = payload["stages"].get(stage, {})
        status = row.get("status", "PENDING")
        if status not in ("PENDING", "PASS", "FAIL", "INCOMPLETE", "BLOCKED"):
            raise ValueError(f"invalid state for {stage}: {status}")
        out["stages"][stage] = {"status": status, "last_report": row.get("last_report")}
    return out


def select_stage(requested: str, state: dict) -> str:
    requested = requested.upper()
    if requested != "AUTO":
        if requested not in STAGES:
            raise ValueError("stage must be AUTO or R1 through R6")
        index = STAGES.index(requested)
        unfinished = [s for s in STAGES[:index] if state["stages"][s]["status"] != "PASS"]
        if unfinished:
            raise ValueError(f"strict ordering blocks {requested}; incomplete predecessor: {unfinished[0]}")
        return requested
    for stage in STAGES:
        if state["stages"][stage]["status"] != "PASS":
            return stage
    return "COMPLETE"


def decode_log(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16", errors="ignore")
    for encoding in ("utf-8-sig", "utf-16-le", "cp1252"):
        try:
            text = raw.decode(encoding)
            if "\x00" not in text:
                return text
        except UnicodeDecodeError:
            pass
    return raw.decode("utf-8", errors="ignore")


def scan_logs(paths: list[Path], stage: str) -> dict:
    text = "\n".join(decode_log(path) for path in paths if path.is_file())
    env = [line for line in text.splitlines() if "[V459-OBS][ENV]" in line]
    latest = env[-1] if env else ""
    checkpoint_prefix = "D1TPW|" if stage == "R1" else "C044|" if stage == "R2" else None
    return {
        "observer_seen": "[V459-OBS][START]" in text,
        "demo": "Demo=Y" in latest,
        "live_account_seen": "Demo=N" in latest,
        "connected": "Connected=Y" in latest,
        "trade_allowed": "TradeAllowed=Y" in latest,
        "start_epochs": text.count("[V459-OBS][START]"),
        "open_order_seen": "[V459-OBS][OPEN]" in text,
        "checkpoint_seen": bool(checkpoint_prefix and checkpoint_prefix in text and "[V459-OBS][GV]" in text),
        "environment_line": latest,
    }


def aggregate_cases(payload: dict) -> dict[str, dict]:
    reports = payload.get("reports")
    if not isinstance(reports, list) or not reports:
        raise ValueError("analyzer multi-report has no reports")
    grouped: dict[str, list[dict]] = {}
    for report in reports:
        for case, row in report.get("cases", {}).items():
            grouped.setdefault(case, []).append(row)
    priority = {"FAIL": 4, "PASS": 3, "BLOCKED": 2, "INCOMPLETE": 1}
    out = {}
    for case, rows in grouped.items():
        out[case] = max(rows, key=lambda row: priority.get(row.get("status", ""), 0))
    return out


def summarize(payload: dict, stage: str) -> dict:
    cases = aggregate_cases(payload)
    selected = {case: cases.get(case, {"status": "INCOMPLETE", "detail": "missing analyzer result", "evidence": []}) for case in CASES_BY_STAGE[stage]}
    statuses = [row["status"] for row in selected.values()]
    if "FAIL" in statuses:
        status = "FAIL"
    elif all(value == "PASS" for value in statuses):
        status = "PASS"
    elif "BLOCKED" in statuses:
        status = "BLOCKED"
    else:
        status = "INCOMPLETE"
    return {"schema": REPORT_SCHEMA, "stage": stage, "status": status, "cases": selected}


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    p_validate = sub.add_parser("validate")
    p_validate.add_argument("settings")
    p_validate.add_argument("--allow-missing-profiles", action="store_true")
    p_validate.add_argument("--skip-path-checks", action="store_true")
    p_plan = sub.add_parser("plan")
    p_plan.add_argument("settings")
    p_plan.add_argument("state")
    p_plan.add_argument("--stage", default="AUTO")
    p_scan = sub.add_parser("scan")
    p_scan.add_argument("--stage", required=True, choices=STAGES)
    p_scan.add_argument("log", nargs="+")
    p_summary = sub.add_parser("summarize")
    p_summary.add_argument("report")
    p_summary.add_argument("--stage", required=True, choices=STAGES)
    args = parser.parse_args()

    if args.command == "validate":
        payload = validate_settings(load_json(Path(args.settings)), check_paths=not args.skip_path_checks, check_profiles=not args.allow_missing_profiles)
        print(json.dumps({"status": "PASS", "schema": payload["schema"]}))
        return 0
    if args.command == "plan":
        settings = validate_settings(load_json(Path(args.settings)))
        state_path = Path(args.state)
        state = normalize_state(load_json(state_path) if state_path.is_file() else None)
        stage = select_stage(args.stage, state)
        plan = {"stage": stage, "profile": None if stage == "COMPLETE" else PROFILE_BY_STAGE[stage], "mt4_profile": None if stage == "COMPLETE" else settings["profiles"][stage]}
        print(json.dumps(plan))
        return 0
    if args.command == "scan":
        print(json.dumps(scan_logs([Path(p) for p in args.log], args.stage)))
        return 0
    payload = load_json(Path(args.report))
    print(json.dumps(summarize(payload, args.stage), indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"V459_USER_TEST_CONTROL=FAIL: {exc}", file=sys.stderr)
        raise SystemExit(2)
