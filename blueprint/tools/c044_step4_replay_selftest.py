#!/usr/bin/env python3
"""C044 Step4 deterministic replay self-test.

This is a source-bound analyzer + reference state-machine matrix. It does not
activate C044 and it does not replace native MT4 runtime evidence. It verifies
that the exact compiled v4.56 source retains the checkpoint/replay invariants
required before an activation decision can even be considered.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys

SRC_PATH = Path("blueprint/source/BBMA_EA.mq4")
EXPECTED_BLOB = "f0f80decbdbda836c12b6073f5dbc6e347662b13"
EXPECTED_VERSION = "Version 4.5.6 - C044 Deterministic Replay Stage"


def fail(msg: str) -> None:
    raise AssertionError(msg)


def require(cond: bool, msg: str) -> None:
    if not cond:
        fail(msg)


def git_blob() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD:blueprint/source/BBMA_EA.mq4"],
        text=True,
    ).strip()


def function_text(src: str, name: str) -> str:
    # Match a function definition rather than a call/prototype.
    m = re.search(r"(?m)^[^\n;]*\b" + re.escape(name) + r"\s*\([^;]*?\)\s*\{", src)
    if not m:
        fail(f"function not found: {name}")
    open_brace = src.find("{", m.start())
    if open_brace < 0:
        fail(f"opening brace not found: {name}")

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
    fail(f"closing brace not found: {name}")
    return ""


def indexed_fields(text: str, group: str, target: str) -> dict[int, str]:
    out: dict[int, str] = {}
    # Save side: GlobalVariableSet(C044ReplayGVKey(base,"R",3), ... target.Field ...)
    pat = re.compile(
        r'C044ReplayGVKey\(base,"' + re.escape(group) + r'",(\d+)\).*?'
        + re.escape(target) + r"\.(\w+)",
    )
    for line in text.splitlines():
        m = pat.search(line)
        if m:
            out[int(m.group(1))] = m.group(2)
    return out


def loaded_fields(text: str, group: str, target: str) -> dict[int, str]:
    out: dict[int, str] = {}
    pat = re.compile(
        r'ReadC044ReplayGV\(base,"' + re.escape(group) + r'",(\d+),v\).*?'
        + re.escape(target) + r"\.(\w+)\s*="
    )
    for line in text.splitlines():
        m = pat.search(line)
        if m:
            out[int(m.group(1))] = m.group(2)
    return out


def assert_checkpoint_roundtrip(src: str) -> None:
    save = function_text(src, "SaveC044ReplaySeed")
    load = function_text(src, "LoadC044ReplaySeed")
    clear = function_text(src, "ClearC044ReplaySeed")
    save_cp = function_text(src, "SaveC044Checkpoint")
    load_cp = function_text(src, "LoadC044Checkpoint")

    expected_r = {
        0: "Type", 1: "State", 2: "Direction", 3: "Timeframe",
        4: "StartBar", 5: "StartCandleTime", 6: "LastUpdateBar",
        7: "LastUpdateCandleTime", 8: "ConfirmationBar",
        9: "ConfirmationCandle", 10: "ExpiryBar", 11: "ExpiryCandleTime",
        12: "MinCandlesRequired", 13: "QualifyingCandles",
        14: "Type1ContextState", 15: "Type1OwnerSignal",
        16: "Type1OwnerCandleTime", 17: "Type1RangingStartCandleTime",
        18: "Type1PreviousClose", 19: "IsValid",
    }
    expected_e = {
        0: "Maturity", 1: "Direction", 2: "Timeframe", 3: "RawBar",
        4: "RawCandleTime", 5: "ConfirmationBar", 6: "ConfirmationCandleTime",
        7: "ConfirmationClose", 8: "LastUpdateBar", 9: "LastUpdateCandleTime",
        10: "PreviousClose", 11: "ProvisionalBodyAnchor", 12: "FrozenBodyAnchor",
        13: "RelevantMA5", 14: "RetestStartBar", 15: "RetestStartCandleTime",
        16: "RetestCompletionBar", 17: "RetestCompletionCandleTime", 18: "IsValid",
    }

    require(indexed_fields(save, "R", "info.c044_replay_reentry") == expected_r,
            "Re-Entry replay seed save map drift")
    require(loaded_fields(load, "R", "info.c044_replay_reentry") == expected_r,
            "Re-Entry replay seed load map drift")
    require(indexed_fields(save, "B", "buy") == expected_e,
            "BUY Extreme replay seed save map drift")
    require(loaded_fields(load, "B", "info.c044_replay_extreme_buy") == expected_e,
            "BUY Extreme replay seed load map drift")
    require(indexed_fields(save, "S", "sell") == expected_e,
            "SELL Extreme replay seed save map drift")
    require(loaded_fields(load, "S", "info.c044_replay_extreme_sell") == expected_e,
            "SELL Extreme replay seed load map drift")

    require("for(int i = 0; i < 20; i++)" in clear,
            "Re-Entry replay seed clear cardinality drift")
    require("for(int j = 0; j < 19; j++)" in clear,
            "Extreme replay seed clear cardinality drift")
    require("SaveC044ReplaySeed(info)" in save_cp,
            "checkpoint no longer persists replay seed")
    require("return LoadC044ReplaySeed(info);" in load_cp,
            "checkpoint no longer restores replay seed")
    require("state == C044_LIFE_FROZEN" in load_cp and
            "info.c044_replay_seed_valid = false;" in load_cp,
            "frozen checkpoint semantics drift")


def assert_source_invariants(src: str) -> None:
    require(EXPECTED_VERSION in src, "unexpected C044 Step4 build")
    require('#property version   "4.56"' in src, "unexpected property version")
    require("bool           EnableC044Lifecycle                = false;" in src,
            "C044 feature gate is not locked OFF")
    require("MULTI_CANDLE_OWNER_EVENT_GAP" not in src,
            "legacy multi-candle freeze path returned")
    require("IsC044SameDirectionReEntryEvent" not in src,
            "current-global Re-Entry inference helper returned")
    require("IsC044OppositeExtremeSupersessionEvent" not in src,
            "current-global Extreme inference helper returned")

    init = function_text(src, "InitializeC044TradeStateFromDecision")
    require("GetLatestClosedCandleTime" in init,
            "trade-open owner cursor no longer derives from latest closed owner candle")
    require("info.c044_last_processed_owner_candle = latestClosed;" in init,
            "trade-open owner cursor correction missing")
    require("CaptureC044ReplaySeed(info, pairIndex)" in init,
            "trade-open replay seed capture missing")

    process = function_text(src, "ProcessC044OwnerClosedCandle")
    for marker in (
        "DetectExtreme(pair, DIR_BUY, data, band)",
        "DetectExtreme(pair, DIR_SELL, data, band)",
        "UpdateExtremeLifecycle(info.c044_replay_extreme_buy",
        "UpdateExtremeLifecycle(info.c044_replay_extreme_sell",
        "ResolveOppositeExtremeSupersession(info.c044_replay_extreme_buy",
        "UpdateReEntryState(info.c044_replay_reentry",
        "DetectCSM(pair, info.c044_owner_timeframe",
    ):
        require(marker in process, f"canonical replay authority missing: {marker}")

    # Event precedence: opposite confirmed Extreme supersedes before the
    # WAIT_NEXT_REENTRY branch; that branch returns before outer-BB evaluation;
    # outer-BB test precedes canonical Momentum, then failed-Momentum latch.
    p_opp = process.find("if(oppositeExtremeEvent)")
    p_wait_re = process.find("if(info.c044_state == C044_LIFE_WAIT_NEXT_REENTRY)")
    p_outer = process.find("if(!IsC044DirectionSideOuterBBTest")
    p_mom = process.find("bool momentum = DetectCSM")
    p_fail = process.find("C044_EXIT_FAILED_MOMENTUM")
    require(-1 not in (p_opp, p_wait_re, p_outer, p_mom, p_fail),
            "C044 event-stage markers incomplete")
    require(p_opp < p_wait_re < p_outer < p_mom < p_fail,
            "C044 event precedence/order drift")

    for reason in (
        "REPLAY_SEED_MISSING",
        "OWNER_EVENT_CANDLE_NOT_EXACT_CLOSED_BAR",
        "OWNER_EVENT_CLOSED_DATA_UNAVAILABLE",
        "WAIT_NEXT_REENTRY_CHECKPOINT_FAILED",
        "WAIT_OUTER_TEST_CHECKPOINT_FAILED",
        "MOMENTUM_HOLD_CHECKPOINT_FAILED",
        "FAILED_MOMENTUM_LATCH_FAILED",
    ):
        require(reason in process, f"fail-closed boundary missing: {reason}")

    adv = function_text(src, "AdvanceC044OwnerEventOneCandle")
    require("if(latestClosed <= info.c044_last_processed_owner_candle)" in adv,
            "no-gap fast path missing")
    require("for(int shift = previousShift - 1; shift >= latestShift; shift--)" in adv,
            "chronological replay loop missing")
    require("datetime candleTime = iTime" in adv,
            "historical owner candle retrieval missing")
    require("REPLAY_CANDLE_ORDER_INVALID" in adv,
            "chronological order fail-closed guard missing")
    require("REPLAY_CURSOR_DID_NOT_REACH_LATEST" in adv,
            "replay cursor completion guard missing")
    require("OWNER_EVENT_CURSOR_NOT_IN_HISTORY" in adv,
            "history availability fail-closed guard missing")

    manage = function_text(src, "ManagePositions")
    emergency = manage.find("g_portfolio_emergency_close_requested")
    c044_close = manage.find("ExecuteLatchedC044Close")
    require(emergency >= 0 and c044_close >= 0 and emergency < c044_close,
            "M20 emergency precedence over C044 close drift")

    assert_checkpoint_roundtrip(src)


WAIT_OUTER = "WAIT_OUTER"
WAIT_RE = "WAIT_RE"
EXIT = "EXIT"
FROZEN = "FROZEN"


@dataclass(frozen=True)
class Event:
    candle: int
    outer: bool = False
    momentum: bool = False
    same_reentry: bool = False
    opposite_extreme: bool = False


@dataclass
class Model:
    state: str = WAIT_OUTER
    epoch: int = 100
    cursor: int = 100
    exit_reason: str = ""


def apply_event(m: Model, e: Event) -> None:
    require(e.candle > m.cursor, "reference matrix requires chronological candles")
    m.cursor = e.candle

    if e.opposite_extreme:
        m.state = EXIT
        m.exit_reason = "CYCLE_SUPERSEDED"
        return

    if m.state == WAIT_RE:
        if e.same_reentry:
            m.epoch = e.candle
            m.state = WAIT_OUTER
        # Re-Entry confirmation candle is not reused as an outer-BB test.
        return

    if m.state != WAIT_OUTER:
        return
    if e.candle <= m.epoch:
        return
    if not e.outer:
        return
    if e.momentum:
        m.state = WAIT_RE
        return
    m.state = EXIT
    m.exit_reason = "FAILED_MOMENTUM"


def replay(m: Model, events: list[Event], *, seed_valid: bool = True,
           history_ok: bool = True) -> Model:
    if m.state in (EXIT, FROZEN):
        return m
    if not seed_valid or not history_ok:
        m.state = FROZEN
        return m
    for e in events:
        apply_event(m, e)
        if m.state in (EXIT, FROZEN):
            break
    return m


def assert_reference_matrix() -> list[str]:
    passed: list[str] = []

    # 1) No gap: no candle is processed and state/cursor remain unchanged.
    m = replay(Model(), [])
    require((m.state, m.cursor, m.epoch) == (WAIT_OUTER, 100, 100),
            "no-gap matrix failed")
    passed.append("NO_GAP")

    # 2) Multi-candle chronological replay: idle -> Momentum hold -> next RE.
    # The RE candle intentionally also has outer=True; it must NOT be reused as
    # the new epoch's outer-BB test.
    m = replay(Model(), [
        Event(200, outer=False),
        Event(300, outer=True, momentum=True),
        Event(400, outer=True, same_reentry=True),
    ])
    require((m.state, m.cursor, m.epoch, m.exit_reason) ==
            (WAIT_OUTER, 400, 400, ""),
            "Momentum -> next Re-Entry re-arm matrix failed")
    passed.append("MULTI_CANDLE_MOMENTUM_REARM")

    # 3) First post-rearm outer test without canonical Momentum exits.
    m = replay(m, [Event(500, outer=True, momentum=False)])
    require((m.state, m.exit_reason, m.cursor) ==
            (EXIT, "FAILED_MOMENTUM", 500),
            "failed-Momentum exit matrix failed")
    passed.append("FAILED_MOMENTUM_EXIT")

    # 4) Opposite mature Extreme supersedes before other same-candle handling.
    m = replay(Model(), [
        Event(200, outer=True, momentum=True, same_reentry=True,
              opposite_extreme=True),
        Event(300, outer=True),
    ])
    require((m.state, m.exit_reason, m.cursor) ==
            (EXIT, "CYCLE_SUPERSEDED", 200),
            "opposite-Extreme supersession/stop matrix failed")
    passed.append("OPPOSITE_EXTREME_SUPERSESSION")

    # 5) Missing/corrupt replay seed freezes rather than inferring events.
    m = replay(Model(), [Event(200, outer=True)], seed_valid=False)
    require(m.state == FROZEN, "missing replay seed did not freeze")
    passed.append("MISSING_SEED_FAIL_FROZEN")

    # 6) Missing exact history freezes rather than skipping intermediate bars.
    m = replay(Model(), [Event(200), Event(300)], history_ok=False)
    require(m.state == FROZEN, "missing history did not freeze")
    passed.append("MISSING_HISTORY_FAIL_FROZEN")

    # 7) Input order itself is guarded; out-of-order replay cannot silently pass.
    try:
        replay(Model(), [Event(300), Event(200)])
    except AssertionError:
        passed.append("CHRONOLOGICAL_ORDER_GUARD")
    else:
        fail("out-of-order replay matrix did not fail")

    return passed


def main() -> int:
    require(SRC_PATH.exists(), "source file missing")
    blob = git_blob()
    require(blob == EXPECTED_BLOB,
            f"exact source blob mismatch: expected {EXPECTED_BLOB}, got {blob}")
    src = SRC_PATH.read_text(encoding="utf-8")

    assert_source_invariants(src)
    matrix = assert_reference_matrix()

    print("C044_STEP4_REPLAY_SELFTEST=PASS")
    print(f"SOURCE_BLOB={blob}")
    print("STATIC_INVARIANTS=PASS")
    print("CHECKPOINT_ROUNDTRIP=PASS")
    for name in matrix:
        print(f"MATRIX_{name}=PASS")
    print("FEATURE_GATE=OFF")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"C044_STEP4_REPLAY_SELFTEST=FAIL: {exc}", file=sys.stderr)
        raise
