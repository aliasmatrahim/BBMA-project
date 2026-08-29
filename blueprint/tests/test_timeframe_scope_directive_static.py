#!/usr/bin/env python3
"""Lock the user-directed W1/M30/primary-M1 exclusion as intentional scope."""
from pathlib import Path


NMJE = Path("blueprint/contracts/NMJE_V2_M5_ACCURACY_HARDENING_CONTRACT.md").read_text(encoding="utf-8")
D1TPW = Path("blueprint/contracts/D1_TPW_LIFECYCLE_HARDENING_CONTRACT.md").read_text(encoding="utf-8")
PLAN = Path("blueprint/implementation/NMJE_V2_M5_WORKSTREAM_PLAN_20260828.md").read_text(encoding="utf-8")


def main() -> None:
    for marker in (
        "W1 and M30 are intentionally",
        "M1 is intentionally excluded from primary NMJE authority",
        "not backlog or missing work",
        "new explicit",
        "strategy-scope approval",
    ):
        if marker not in NMJE:
            raise AssertionError(f"NMJE timeframe directive missing: {marker}")

    for marker in (
        "W1, M30, and primary M1 remain intentional exclusions, not backlog",
        "new explicit user strategy-scope approval",
    ):
        if marker not in D1TPW:
            raise AssertionError(f"D1TPW timeframe directive missing: {marker}")

    for marker in (
        "any W1, M30, or primary M1 addition",
        "intentional exclusions, not",
        "new explicit user strategy-scope approval",
    ):
        if marker not in PLAN:
            raise AssertionError(f"workstream directive missing: {marker}")

    print("TIMEFRAME_SCOPE_DIRECTIVE_STATIC=PASS")


if __name__ == "__main__":
    main()

