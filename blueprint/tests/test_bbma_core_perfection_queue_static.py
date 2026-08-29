#!/usr/bin/env python3
"""Lock the approved BBMA core queue and excluded/KIV risk-policy boundary."""
from pathlib import Path


QUEUE = Path(
    "blueprint/implementation/BBMA_CORE_PERFECTION_QUEUE_20260829.md"
).read_text(encoding="utf-8")
NORMALIZED_QUEUE = " ".join(QUEUE.split())


def main() -> None:
    for marker in (
        "Do not add a daily-loss limit or daily-loss trading gate",
        "same-currency concurrent-exposure control as `KIV`",
        "cooldown after a loss sequence or broker failure as `KIV`",
        "KIV does not mean approved backlog",
        "Canonical BBMA truth tables and golden fixtures",
        "NMJE must not reject the sole valid M15 candidate",
        "C5 and C9 remain manual strategy/activation boundaries",
    ):
        if marker not in NORMALIZED_QUEUE:
            raise AssertionError(f"BBMA core queue directive missing: {marker}")

    print("BBMA_CORE_PERFECTION_QUEUE_STATIC=PASS")


if __name__ == "__main__":
    main()

