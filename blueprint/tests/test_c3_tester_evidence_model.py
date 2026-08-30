#!/usr/bin/env python3
"""Deterministic cases for the read-only C3 Strategy Tester evidence parser."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from tempfile import TemporaryDirectory


TOOL = Path("blueprint/tools/c3_tester_evidence.py")
SPEC = importlib.util.spec_from_file_location("c3_tester_evidence", TOOL)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


PASS_LOG = """
Expert BBMA_EA GBPUSD,M15: loaded successfully
[P3S1] Symbol resolved GBPUSD -> GBPUSD
[P3S1][PASS] Broker spec GBPUSD PID=1 Magic=2
[P3S1] LoadPairs completed count=1
[P3S1][PASS] EA initialized successfully with 1 pairs
BBMA EA V4.72 Offline Tester Symbol Compatibility initialized successfully
GBPUSD,M15: 3847840 tick events (2487 bars, 3847840 bar states) processed
Tester stopped
"""


def main() -> None:
    cases = 0

    result = MODULE.evaluate(PASS_LOG, True)
    assert result["status"] == "PASS"
    assert result["max_ticks"] == 3_847_840
    assert result["max_bars"] == 2_487
    cases += 1

    assert MODULE.evaluate(PASS_LOG, False)["status"] == "INCOMPLETE"
    cases += 1

    old_failure = """
Expert BBMA_EA GBPUSD,M15: loaded successfully
[P3S1][FAIL] Symbol resolution failed for GBPUSD
[P3S1] LoadPairs completed count=0
EA initialization failed
Tester stopped
"""
    assert MODULE.evaluate(old_failure, True)["status"] == "FAIL"
    cases += 1

    broker_failure = PASS_LOG.replace(
        "[P3S1][PASS] Broker spec GBPUSD PID=1 Magic=2",
        "[P3S1][FAIL] Broker spec GBPUSD Point=0",
    )
    assert MODULE.evaluate(broker_failure, True)["status"] == "FAIL"
    cases += 1

    wrong_symbol = PASS_LOG.replace(
        "Symbol resolved GBPUSD -> GBPUSD",
        "Symbol resolved GBPUSD -> GBPUSD.a",
    )
    assert MODULE.evaluate(wrong_symbol, True)["status"] == "FAIL"
    assert MODULE.evaluate(wrong_symbol, True)["wrong_symbol"]
    cases += 1

    first_event_only = PASS_LOG.replace(
        "3847840 tick events (2487 bars, 3847840 bar states)",
        "1 tick events (0 bars, 3847840 bar states)",
    )
    assert MODULE.evaluate(first_event_only, True)["status"] == "INCOMPLETE"
    cases += 1

    startup_only = "Tester: start with configuration file"
    assert MODULE.evaluate(startup_only, False)["status"] == "INCOMPLETE"
    cases += 1

    with TemporaryDirectory() as temporary_directory:
        root = Path(temporary_directory)
        marker = root / "run.marker"
        log = root / "tester.log"
        report = root / "report.html"

        assert MODULE.classify_paths(log, report, marker) == {
            "status": "NOT_RUN",
            "reason": "NO_RUN_MARKER",
        }
        cases += 1

        marker.write_text("run", encoding="utf-8")
        log.write_text(PASS_LOG, encoding="utf-8")
        report.write_text("report", encoding="utf-8")
        os.utime(log, ns=(1_000_000_000, 1_000_000_000))
        os.utime(report, ns=(3_000_000_000, 3_000_000_000))
        os.utime(marker, ns=(2_000_000_000, 2_000_000_000))
        stale_log = MODULE.classify_paths(log, report, marker)
        assert stale_log == {"status": "NOT_RUN", "reason": "STALE_TESTER_LOG"}
        cases += 1

        os.utime(log, ns=(3_000_000_000, 3_000_000_000))
        os.utime(report, ns=(1_000_000_000, 1_000_000_000))
        stale_report = MODULE.classify_paths(log, report, marker)
        assert stale_report["status"] == "INCOMPLETE"
        assert not stale_report["provenance"]["report_fresh"]
        cases += 1

        os.utime(report, ns=(3_000_000_000, 3_000_000_000))
        fresh_evidence = MODULE.classify_paths(log, report, marker)
        assert fresh_evidence["status"] == "PASS"
        assert fresh_evidence["provenance"] == {
            "log_fresh": True,
            "report_fresh": True,
        }
        cases += 1

    print(f"C3_TESTER_EVIDENCE_MODEL=PASS cases={cases}")


if __name__ == "__main__":
    main()
