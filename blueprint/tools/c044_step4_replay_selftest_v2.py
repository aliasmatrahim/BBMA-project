#!/usr/bin/env python3
"""Corrected entrypoint for C044 Step4 replay selftest.

The v1 analyzer's function extractor could match an `if(Function(...)) {` call
as a function definition. This wrapper replaces only that extractor; all test
assertions and lifecycle matrix remain unchanged.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import sys

BASE = Path(__file__).with_name("c044_step4_replay_selftest.py")
spec = importlib.util.spec_from_file_location("c044_step4_replay_selftest_base", BASE)
if spec is None or spec.loader is None:
    raise SystemExit("unable to load base C044 selftest")
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def function_text(src: str, name: str) -> str:
    # Only accept real MQL4 function definitions with an explicit return type.
    return_type = r"(?:bool|void|string|int|double|datetime|ENUM_[A-Za-z0-9_]+)"
    pattern = (
        r"(?m)^\s*" + return_type + r"\s+" + re.escape(name)
        + r"\s*\([^;]*?\)\s*\{"
    )
    m = re.search(pattern, src)
    if not m:
        raise AssertionError(f"function not found: {name}")
    open_brace = src.find("{", m.start())
    if open_brace < 0:
        raise AssertionError(f"opening brace not found: {name}")

    depth = 0
    i = open_brace
    in_string = False
    in_char = False
    in_line_comment = False
    in_block_comment = False
    escaped = False
    while i < len(src):
        c = src[i]
        n = src[i + 1] if i + 1 < len(src) else ""

        if in_line_comment:
            if c == "\n":
                in_line_comment = False
            i += 1
            continue
        if in_block_comment:
            if c == "*" and n == "/":
                in_block_comment = False
                i += 2
                continue
            i += 1
            continue
        if in_string:
            if escaped:
                escaped = False
            elif c == "\\":
                escaped = True
            elif c == '"':
                in_string = False
            i += 1
            continue
        if in_char:
            if escaped:
                escaped = False
            elif c == "\\":
                escaped = True
            elif c == "'":
                in_char = False
            i += 1
            continue

        if c == "/" and n == "/":
            in_line_comment = True
            i += 2
            continue
        if c == "/" and n == "*":
            in_block_comment = True
            i += 2
            continue
        if c == '"':
            in_string = True
            i += 1
            continue
        if c == "'":
            in_char = True
            i += 1
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return src[m.start() : i + 1]
        i += 1
    raise AssertionError(f"closing brace not found: {name}")


mod.function_text = function_text

if __name__ == "__main__":
    try:
        sys.exit(mod.main())
    except Exception as exc:
        print(f"C044_STEP4_REPLAY_SELFTEST=FAIL: {exc}", file=sys.stderr)
        raise
