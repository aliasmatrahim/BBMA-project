#!/usr/bin/env python3
"""Stage-C1 closed-M5 acquisition-only regression for Issue #101."""
from pathlib import Path
import re


SRC = Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")


def body(name: str) -> str:
    match = re.search(rf"void\s+{re.escape(name)}\s*\([^)]*\)\s*\{{(.*?)\n\}}", SRC, re.S)
    if not match:
        raise AssertionError(f"missing function: {name}")
    return match.group(1)


def main() -> None:
    for marker in (
        "datetime M5_CandleTime;",
        "bool     M5_IsClosed;",
        "TimeframeData        m5_data;",
        "InitTimeframeData(state.m5_data);",
    ):
        if marker not in SRC:
            raise AssertionError(f"missing Stage-C1 marker: {marker}")

    snapshot = body("BuildTimeframeSnapshot")
    for marker in (
        "GetLatestClosedCandleTime(pair, PERIOD_M5)",
        "IsCandleClosed(snapshot.M5_CandleTime, 300)",
    ):
        if marker not in snapshot:
            raise AssertionError(f"M5 closed-candle snapshot missing: {marker}")

    process = body("ProcessPair")
    required_load = (
        "GetDataForTimeframe(actual, PERIOD_M5, "
        "g_pair_states[pairIndex].tf_snapshot.M5_CandleTime,"
    )
    if required_load not in process:
        raise AssertionError("closed M5 data load missing from M15-driven ProcessPair")
    if "g_pair_states[pairIndex].m5_data" not in process:
        raise AssertionError("M5 data destination missing")

    # No M5 BBMA detector/lifecycle or refinement population is authorized yet.
    for forbidden in (
        "DetectExtreme(actual, DIR_BUY, g_pair_states[pairIndex].m5_data",
        "DetectExtreme(actual, DIR_SELL, g_pair_states[pairIndex].m5_data",
        "UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_m5",
        "UpdateReEntryState(g_pair_states[pairIndex].re_m5",
        "DetectCSD(actual, PERIOD_M5",
        "DetectECSD(actual, PERIOD_M5",
        "DetectCSM(actual, PERIOD_M5",
        "M5Refinement.",
        "NMJE_M5ContextEventID(",
        "NMJE_M5LineageSnapshotValid(",
    ):
        if forbidden in process:
            raise AssertionError(f"premature Stage-C1 logic: {forbidden}")

    # The orchestrator remains M15-clocked; M5 must not create a new clock.
    is_new = SRC[SRC.index("bool IsNewCandle("):SRC.index("string D10Dir(")]
    if "PERIOD_M5" in is_new or "M5_CandleTime" in is_new:
        raise AssertionError("M5 processing clock authority introduced")
    if "PERIOD_M15" not in is_new:
        raise AssertionError("M15 processing clock missing")

    print("NMJE_V2_M5_STAGE_C1_ACQUISITION_STATIC=PASS")


if __name__ == "__main__":
    main()

