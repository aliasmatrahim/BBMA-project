#!/usr/bin/env python3
"""Stage-C1 closed-M5 acquisition and clock-boundary regression."""
from pathlib import Path
import re


SRC = Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")


def body(name: str) -> str:
    # Static regression checks function bodies, not their return type. Keep the
    # parser tolerant of void/bool/etc. so a harmless signature form does not
    # masquerade as an acquisition-contract failure.
    match = re.search(
        rf"\b[A-Za-z_][A-Za-z0-9_]*\s+{re.escape(name)}\s*\([^)]*\)\s*\{{(.*?)\n\}}",
        SRC,
        re.S,
    )
    if not match:
        raise AssertionError(f"missing function: {name}")
    return match.group(1)


def main() -> None:
    for marker in (
        "datetime M5_CandleTime;",
        "bool     M5_IsClosed;",
        "TimeframeData        m5_data;",
    ):
        if marker not in SRC:
            raise AssertionError(f"missing Stage-C1 marker: {marker}")

    # Stage C1 owns the acquisition path, not a separate PairState initializer.
    # GetDataForTimeframe must initialize every destination before loading it,
    # including PairState.m5_data used below from the M15-driven ProcessPair.
    loader = body("GetDataForTimeframe")
    if "InitTimeframeData(data);" not in loader:
        raise AssertionError("timeframe loader no longer initializes its destination")

    # Bind the frozen closed-M5 snapshot to the exact source statements. These
    # fields are unique to TimeframeSnapshot and do not need a fragile parser
    # assumption about the helper's return type/declaration formatting.
    for marker in (
        "snapshot.M5_CandleTime = GetLatestClosedCandleTime(pair, PERIOD_M5);",
        "snapshot.M5_IsClosed = IsCandleClosed(snapshot.M5_CandleTime, 300);",
    ):
        if marker not in SRC:
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

    # Stage C2 may run canonical shadow detectors, but ProcessPair itself must
    # not populate lineage or create any decision/authority coupling.
    for forbidden in (
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
