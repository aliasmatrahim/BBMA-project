#!/usr/bin/env python3
"""Static guard for NMJE N3 Step-1 M09 single-writer invariant."""
from pathlib import Path
import sys

TARGET = Path("blueprint/source/BBMA_EA.mq4")

FORBIDDEN = [
    "InstallMHVSupersessionParent(",
    "TryAdvanceMHVSupersessionCandidate(",
]
REQUIRED = [
    "TryAdvanceMHVSupersessionFromCanonicalParent(",
    "UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_m15_buy_lifecycle",
    "UpdateExtremeLifecycle(g_pair_states[pairIndex].extreme_m15_sell_lifecycle",
    "ResolveOppositeExtremeSupersession(g_pair_states[pairIndex].extreme_m15_buy_lifecycle",
    "ENUM_MLV_STATE UpdateCanonicalMLVState(",
]


def main() -> int:
    if not TARGET.exists():
        print(f"FAIL target missing: {TARGET}")
        return 2
    text = TARGET.read_text(encoding="utf-8")
    failures = 0
    for token in FORBIDDEN:
        if token in text:
            print(f"FAIL forbidden legacy M09 Extreme writer remains: {token}")
            failures += 1
    for token in REQUIRED:
        if token not in text:
            print(f"FAIL required invariant missing: {token}")
            failures += 1

    # M09 may reference parent fields read-only but must not assign parent.*.
    marker_start = text.find("ENUM_DIRECTION GetMHVParentExtremeDirection")
    marker_end = text.find("//+------------------------------------------------------------------+\n//| MODULE 10:", marker_start)
    if marker_start < 0 or marker_end < 0:
        print("FAIL unable to isolate M09 section")
        failures += 1
    else:
        m09 = text[marker_start:marker_end]
        suspicious = [line.strip() for line in m09.splitlines()
                      if "parent." in line and "=" in line and
                      not any(op in line for op in ["==", "!=", ">=", "<="])]
        if suspicious:
            print("FAIL M09 appears to assign canonical parent fields:")
            for line in suspicious:
                print("  " + line)
            failures += 1

    if failures:
        print(f"RESULT: FAIL ({failures} issue(s))")
        return 1
    print("RESULT: PASS — M08 is sole Extreme writer; M09 consumes canonical parent only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
