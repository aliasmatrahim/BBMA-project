#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[2]
TOOLS = REPO / "blueprint" / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import v459_user_test_control as tool


def settings(root: Path) -> dict:
    terminal = root / "terminal.exe"
    editor = root / "metaeditor.exe"
    data = root / "data"
    terminal.write_text("test", encoding="utf-8")
    editor.write_text("test", encoding="utf-8")
    data.mkdir()
    profiles = {stage: f"BBMA_V459_{stage}" for stage in tool.STAGES}
    for name in profiles.values():
        (data / "profiles" / name).mkdir(parents=True)
    (data / "profiles" / "BBMA_V459_DEMO_PREFLIGHT").mkdir(parents=True)
    return {
        "schema": tool.SETTINGS_SCHEMA,
        "terminal_path": str(terminal),
        "metaeditor_path": str(editor),
        "data_path": str(data),
        "work_root": str(root / "work"),
        "portable_mode": True,
        "require_demo_account": True,
        "auto_restart_on_checkpoint": True,
        "preflight_profile": "BBMA_V459_DEMO_PREFLIGHT",
        "monitor_minutes": 480,
        "startup_timeout_seconds": 180,
        "clean_shutdown_timeout_seconds": 45,
        "poll_seconds": 5,
        "profiles": profiles,
    }


def assert_rejected(callable_):
    try:
        callable_()
    except ValueError:
        return
    raise AssertionError("expected fail-closed rejection")


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        config = settings(root)
        assert tool.validate_settings(config) == config

        credentialed = dict(config)
        credentialed["password"] = "do-not-store"
        assert_rejected(lambda: tool.validate_settings(credentialed))
        not_demo = dict(config)
        not_demo["require_demo_account"] = False
        assert_rejected(lambda: tool.validate_settings(not_demo))

        state = tool.initial_state()
        assert tool.select_stage("AUTO", state) == "R1"
        assert_rejected(lambda: tool.select_stage("R2", state))
        state["stages"]["R1"]["status"] = "PASS"
        assert tool.select_stage("AUTO", state) == "R2"
        assert tool.select_stage("R2", state) == "R2"
        for stage in tool.STAGES:
            state["stages"][stage]["status"] = "PASS"
        assert tool.select_stage("AUTO", state) == "COMPLETE"

        logs = root / "runtime.log"
        logs.write_text(
            "[V459-OBS][START] TS=1\n"
            "[V459-OBS][ENV] TS=1 Demo=Y Connected=Y TradeAllowed=Y\n"
            "[V459-OBS][OPEN] TS=1 Ticket=10\n"
            "[V459-OBS][GV] TS=1 Name=D1TPW|S1|I0|T10|LP Value=1\n",
            encoding="utf-8",
        )
        scan = tool.scan_logs([logs], "R1")
        assert scan["demo"] and scan["connected"] and scan["trade_allowed"]
        assert scan["checkpoint_seen"] and scan["open_order_seen"]
        logs.write_text(logs.read_text(encoding="utf-8") + "[V459-OBS][ENV] TS=2 Demo=N Connected=Y TradeAllowed=Y\n", encoding="utf-8")
        unsafe = tool.scan_logs([logs], "R1")
        assert unsafe["live_account_seen"] and not unsafe["demo"]

        pass_cases = {case: {"status": "PASS", "detail": "ok", "evidence": ["x"]} for case in tool.CASES_BY_STAGE["R1"]}
        report = {"reports": [{"cases": pass_cases}]}
        assert tool.summarize(report, "R1")["status"] == "PASS"
        report["reports"][0]["cases"]["R1_IDEMPOTENCY"]["status"] = "FAIL"
        assert tool.summarize(report, "R1")["status"] == "FAIL"

        runner = (REPO / "blueprint" / "runtime" / "v459_user_test_runner.ps1").read_text(encoding="utf-8")
        observer = (REPO / "blueprint" / "runtime" / "V459_Runtime_Observer.mq4").read_text(encoding="utf-8")
        assert "require_demo_account" in runner and "Demo=N" in runner
        assert "CloseMainWindow" in runner and ".Kill(" not in runner
        assert "Demo=" in observer and "IsDemo()" in observer
        for forbidden in ("OrderSend(", "OrderClose(", "OrderModify(", "OrderDelete("):
            assert forbidden not in observer

    print("V459_USER_TEST_CONTROL_SELFTEST=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
