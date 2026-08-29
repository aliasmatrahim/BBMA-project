#!/usr/bin/env python3
"""Classify isolated C3 MT4 Strategy Tester evidence without changing MT4."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


FAILURE_MARKERS = (
    "Symbol resolution failed",
    "[P3S1][FAIL] Broker spec",
    "No valid pairs loaded",
    "EA initialization failed",
    "initialization failed (",
)


def evaluate(log_text: str, report_exists: bool) -> dict[str, object]:
    resolved = re.findall(
        r"\[P3S1\] Symbol resolved GBPUSD -> ([^\s]+)", log_text
    )
    progress = [
        (int(ticks), int(bars))
        for ticks, bars in re.findall(
            r"GBPUSD,M15:\s+(\d+) tick events \((\d+) bars,", log_text
        )
    ]
    max_ticks = max((row[0] for row in progress), default=0)
    max_bars = max((row[1] for row in progress), default=0)
    wrong_symbol = any(symbol != "GBPUSD" for symbol in resolved)

    checks = {
        "ea_loaded": "Expert BBMA_EA GBPUSD,M15: loaded successfully" in log_text,
        "exact_symbol": "GBPUSD" in resolved and not wrong_symbol,
        "broker_spec": bool(
            re.search(r"\[P3S1\]\[PASS\] Broker spec GBPUSD\b", log_text)
        ),
        "pair_count_one": "[P3S1] LoadPairs completed count=1" in log_text,
        "initialized": (
            "[P3S1][PASS] EA initialized successfully with 1 pairs" in log_text
            or "BBMA EA V4.72 Offline Tester Symbol Compatibility initialized successfully"
            in log_text
        ),
        "processed_beyond_init": max_ticks > 1 and max_bars > 0,
        "tester_stopped": "Tester stopped" in log_text,
        "report_written": report_exists,
    }
    explicit_failure = wrong_symbol or any(
        marker in log_text for marker in FAILURE_MARKERS
    )

    if explicit_failure:
        status = "FAIL"
    elif all(checks.values()):
        status = "PASS"
    else:
        status = "INCOMPLETE"

    return {
        "status": status,
        "checks": checks,
        "wrong_symbol": wrong_symbol,
        "max_ticks": max_ticks,
        "max_bars": max_bars,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.log.is_file():
        result: dict[str, object] = {
            "status": "NOT_RUN",
            "reason": "NO_TESTER_LOG",
        }
    else:
        result = evaluate(
            args.log.read_text(encoding="utf-8", errors="replace"),
            args.report.is_file(),
        )

    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(f"C3_BUILD472_EVIDENCE={result['status']}")
        for name, value in result.get("checks", {}).items():
            print(f"{name.upper()}={'PASS' if value else 'FAIL'}")

    return {"PASS": 0, "FAIL": 1}.get(str(result["status"]), 2)


if __name__ == "__main__":
    raise SystemExit(main())
