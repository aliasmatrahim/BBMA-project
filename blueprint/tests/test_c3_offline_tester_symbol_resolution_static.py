#!/usr/bin/env python3
"""Bind the C3 tester-only shortcut and live-equivalence boundary to build 4.72."""
from hashlib import sha256
from pathlib import Path
import re


SOURCE_PATH = Path("blueprint/source/BBMA_EA.mq4")
SRC = SOURCE_PATH.read_text(encoding="utf-8")
EXPECTED_SOURCE_SHA256 = "0f461312d7d26d724c9738eddf88f1a226148f01eae894ce52d942e963f31e99"
EXPECTED_LIVE_TAIL_SHA256 = "5b70b45e537efb8ba6ea65bf7acc83ca4e4b192f5da8489303f015e76d1a0a23"


def function_body(name: str) -> str:
    declaration = re.search(rf"(?m)^[A-Za-z_][^\r\n]*\b{re.escape(name)}\s*\(", SRC)
    if declaration is None:
        raise AssertionError(f"missing function: {name}")
    brace = SRC.find("{", declaration.start())
    depth = 0
    for index in range(brace, len(SRC)):
        if SRC[index] == "{":
            depth += 1
        elif SRC[index] == "}":
            depth -= 1
            if depth == 0:
                return SRC[brace:index + 1]
    raise AssertionError(f"unterminated function: {name}")


def main() -> None:
    digest = sha256(SOURCE_PATH.read_bytes()).hexdigest()
    if digest != EXPECTED_SOURCE_SHA256:
        raise AssertionError(f"EA source drift: {digest}")

    for marker in (
        "Version 4.7.2 - Offline Tester Symbol Compatibility",
        '#property version   "4.72"',
        "BBMA EA V4.72 Offline Tester Symbol Compatibility",
    ):
        if marker not in SRC:
            raise AssertionError(f"missing build marker: {marker}")

    body = function_body("FindActualSymbol")
    live_marker = "   // 1) Exact broker symbol wins when it exists and can be selected."
    if live_marker not in body:
        raise AssertionError("missing original live-resolution boundary")
    tester_prefix, live_tail = body.split(live_marker, 1)
    live_tail = live_marker + live_tail

    required_tester = (
        'string requested = StringTrimLeft(StringTrimRight(symbol))',
        'if(requested == "") return ""',
        "if(IsTesting() && requested == Symbol())",
        "return requested;",
    )
    cursor = -1
    for marker in required_tester:
        found = tester_prefix.find(marker, cursor + 1)
        if found < 0:
            raise AssertionError(f"missing/ordered tester marker: {marker}")
        cursor = found
    for forbidden in ("SymbolSelect(", "SymbolsTotal(", "RemoveSuffix("):
        if forbidden in tester_prefix:
            raise AssertionError(f"tester shortcut gained broker-catalogue authority: {forbidden}")

    live_digest = sha256(live_tail.encode("utf-8")).hexdigest()
    if live_digest != EXPECTED_LIVE_TAIL_SHA256:
        raise AssertionError(f"live resolver drift: {live_digest}")

    load_pairs = function_body("LoadPairs")
    required_order = (
        "string actual = FindActualSymbol(pair)",
        "g_pair_states[g_pair_count].point = GetPointSize(actual)",
        "ValidateBrokerSpecificationWithRetry(actual, g_pair_states[g_pair_count])",
        "g_pair_states[g_pair_count].pair_enabled = true",
    )
    positions = [load_pairs.find(marker) for marker in required_order]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        raise AssertionError("downstream broker-spec fail-closed order drift")

    if len(re.findall(r"\bOrderSend\s*\(", SRC)) != 1:
        raise AssertionError("OrderSend ownership drift")
    if not re.search(r"(?m)^bool\s+EnableD1TPWLifecycle\s*=\s*false\s*;", SRC):
        raise AssertionError("D1TPW activated")
    if not re.search(r"(?m)^bool\s+EnableC044Lifecycle\s*=\s*false\s*;", SRC):
        raise AssertionError("C044 activated")

    print("C3_OFFLINE_TESTER_SYMBOL_RESOLUTION_STATIC=PASS live_path=UNCHANGED")


if __name__ == "__main__":
    main()
