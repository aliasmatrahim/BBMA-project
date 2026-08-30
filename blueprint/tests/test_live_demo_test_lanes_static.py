#!/usr/bin/env python3
"""Fail-closed guard for the live/demo test-lane separation."""
from pathlib import Path


DOC = Path("blueprint/implementation/BBMA_CORE_LIVE_DEMO_TEST_LANES_20260831.md")
SOURCE = Path("blueprint/source/BBMA_EA.mq4")


def main() -> None:
    doc = DOC.read_text(encoding="utf-8")
    source = SOURCE.read_text(encoding="utf-8")

    required = (
        "Lane A — EA-only immediate checks",
        "Lane B — Connected-market observation checks",
        "Lane C — Signal-dependent shadow checks",
        "Lane D — Organic demo-execution checks",
        "Lane E — Controlled resilience tests",
        "WAITING_FOR_SETUP",
        "WAITING_FOR_ORGANIC_SIGNAL",
        "explicit user approval",
        "Production/live-money accounts are prohibited",
        "NMJE/M5 remains shadow metadata",
        "W1, M30 and primary M1 remain excluded",
        "No daily-loss gate is introduced",
    )
    for token in required:
        assert token in doc, token

    assert "bool           EnableD1TPWLifecycle               = false;" in source
    assert "bool           EnableC044Lifecycle                = false;" in source
    assert source.count("OrderSend(") == 1

    print("LIVE_DEMO_TEST_LANES_STATIC=PASS lanes=5 authority=OFF")


if __name__ == "__main__":
    main()

