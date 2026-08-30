#!/usr/bin/env python3
"""Static firewall for dormant D1TPW restart-safe checkpoint hardening."""
from pathlib import Path
import re


SRC = Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")


def function_body(name: str) -> str:
    match = re.search(rf"\b{re.escape(name)}\s*\([^)]*\)\s*\{{", SRC, re.S)
    if not match:
        raise AssertionError(f"missing function: {name}")
    start = match.end() - 1
    depth = 0
    for index in range(start, len(SRC)):
        if SRC[index] == "{":
            depth += 1
        elif SRC[index] == "}":
            depth -= 1
            if depth == 0:
                return SRC[start + 1:index]
    raise AssertionError(f"unterminated function: {name}")


def require(text: str, *markers: str) -> None:
    for marker in markers:
        if marker not in text:
            raise AssertionError(f"missing marker: {marker}")


def main() -> None:
    require(
        SRC,
        'bool           EnableD1TPWLifecycle               = false;',
        'bool           EnableC044Lifecycle                = false;',
        'Version 4.7.2 - Offline Tester Symbol Compatibility',
        '#property version   "4.72"',
        'string               d1_tpw_cycle_hash;',
    )

    exists = function_body("D1TPWCheckpointExists")
    save = function_body("SaveD1TPWCheckpoint")
    load = function_body("LoadD1TPWCheckpoint")
    initialize = function_body("InitializeD1TPWTradeStateFromDecision")
    advance_pair = function_body("AdvanceD1TPWLifecycleForPair")
    close = function_body("ExecuteLatchedD1TPWClose")

    require(
        exists,
        'GlobalVariableCheck(base + "V")',
        '(int)GlobalVariableGet(base + "V") != 2',
        'NMJELoadHex16(base, "P", pairHash)',
        'NMJELoadHex16(base, "C", cycleHash)',
        'NMJELoadHex16(base, "E", executionHash)',
    )
    require(
        save,
        'GlobalVariableDel(base + "V")',
        'NMJEStoreHex16(base, "P", pairHash)',
        'NMJEStoreHex16(base, "C", info.d1_tpw_cycle_hash)',
        'NMJEStoreHex16(base, "E", info.execution_hash)',
        'GlobalVariableSet(base + "V", 2.0)',
    )
    if save.index('GlobalVariableSet(base + "V", 2.0)') < save.index(
        'NMJEStoreHex16(base, "E", info.execution_hash)'
    ):
        raise AssertionError("D1TPW version commit marker is not written last")
    for field in ('"D"', '"X"', '"LP"', '"L"', '"XL"', '"F"', '"OT"', '"MG"'):
        marker = f"GlobalVariableSet(base + {field}"
        if marker not in save or "== 0" not in save[save.index(marker):save.index(marker) + 180]:
            raise AssertionError(f"unchecked D1TPW checkpoint write: {field}")

    require(
        load,
        'pairHash != SHORT_HASH(info.pair, 16)',
        'executionHash != info.execution_hash',
        '(frozen && latched)',
        'info.d1_tpw_cycle_hash = cycleHash;',
        'iTime(info.pair, PERIOD_D1, extremeShift) != extremeCandle',
        'iTime(info.pair, PERIOD_D1, cursorShift) != lastProcessed',
    )
    require(
        initialize,
        'StringLen(decision.D1OpportunityCycleID) != 16',
        'info.d1_tpw_cycle_hash = decision.D1OpportunityCycleID;',
        'info.d1_tpw_last_processed_d1_candle = latestClosed;',
    )

    require(advance_pair, '!EnableD1TPWLifecycle')
    require(close, '!EnableD1TPWLifecycle', 'OrderClose(', 'ClearD1TPWCheckpoint(info);')
    process_pair = function_body("ProcessPair")
    require(process_pair, 'AdvanceD1TPWLifecycleForPair(pairIndex);')
    on_tick = function_body("OnTickMain")
    require(on_tick, 'if(IsNewCandle(', 'ProcessPair(i);')
    if "PERIOD_M5" in advance_pair or "OrderSend" in advance_pair:
        raise AssertionError("D1TPW authority escaped M15 lifecycle boundary")

    print("D1_TPW_CHECKPOINT_HARDENING_STATIC=PASS")


if __name__ == "__main__":
    main()
