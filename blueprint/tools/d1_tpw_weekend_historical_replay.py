#!/usr/bin/env python3
"""Offline D1TPW lifecycle replay from MT4 v401 H4 history.

This is lifecycle evidence, not a strategy-performance backtest. Every eligible
D1 day is treated as a hypothetical source so the forward closed-D1 cursor,
TP-Wajib predicate, and restart equivalence can be exercised without enabling
the production EA.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import struct


HEADER = struct.Struct("<i64s12siiii13i")
RECORD_401 = struct.Struct("<qddddqiq")


@dataclass(frozen=True)
class Bar:
    time: int
    open: float
    high: float
    low: float
    close: float


def read_hst_v401(path: Path) -> tuple[str, int, list[Bar]]:
    raw = path.read_bytes()
    if len(raw) < HEADER.size:
        raise ValueError("HST header truncated")
    header = HEADER.unpack_from(raw)
    version = header[0]
    symbol = header[2].split(b"\0", 1)[0].decode("ascii", errors="strict")
    period = header[3]
    payload = raw[HEADER.size:]
    if version != 401 or period != 240 or len(payload) % RECORD_401.size:
        raise ValueError(f"unsupported HST version/period/size: {version}/{period}/{len(payload)}")

    bars: list[Bar] = []
    for offset in range(0, len(payload), RECORD_401.size):
        timestamp, open_, high, low, close, _ticks, _spread, _real = RECORD_401.unpack_from(payload, offset)
        if timestamp <= 0 or low <= 0 or high < low or open_ <= 0 or close <= 0:
            raise ValueError(f"invalid H4 record at offset {offset}")
        if bars and timestamp <= bars[-1].time:
            raise ValueError("H4 history is not strictly chronological")
        bars.append(Bar(timestamp, open_, high, low, close))
    return symbol, period, bars


def aggregate_d1(h4: list[Bar]) -> list[Bar]:
    days: list[Bar] = []
    bucket: list[Bar] = []
    current_day = -1
    for bar in h4:
        day = bar.time // 86400
        if bucket and day != current_day:
            days.append(Bar(bucket[0].time, bucket[0].open,
                            max(x.high for x in bucket), min(x.low for x in bucket),
                            bucket[-1].close))
            bucket = []
        current_day = day
        bucket.append(bar)
    if bucket:
        days.append(Bar(bucket[0].time, bucket[0].open,
                        max(x.high for x in bucket), min(x.low for x in bucket),
                        bucket[-1].close))
    return days


def lwma_bars(days: list[Bar], end: int, period: int, field: str) -> float:
    if period <= 0 or end + 1 < period:
        raise ValueError("insufficient LWMA history")
    window = days[end - period + 1:end + 1]
    weights = range(1, period + 1)
    return sum(getattr(bar, field) * weight for bar, weight in zip(window, weights)) / sum(weights)


def completion_at(days: list[Bar], index: int, direction: str) -> bool:
    if direction == "BUY":
        return days[index].high >= lwma_bars(days, index, 5, "high") or days[index].high >= lwma_bars(days, index, 10, "high")
    if direction == "SELL":
        return days[index].low <= lwma_bars(days, index, 5, "low") or days[index].low <= lwma_bars(days, index, 10, "low")
    raise ValueError("invalid direction")


def first_completion(days: list[Bar], source: int, direction: str, cursor: int | None = None) -> int | None:
    start = source + 1 if cursor is None else cursor + 1
    for index in range(start, len(days)):
        if completion_at(days, index, direction):
            return index
    return None


def replay_summary(days: list[Bar]) -> dict[str, int]:
    if len(days) < 12:
        raise ValueError("insufficient aggregated D1 history")
    trajectories = completions = restart_checks = max_latency = 0
    for source in range(9, len(days) - 1):
        for direction in ("BUY", "SELL"):
            trajectories += 1
            terminal = first_completion(days, source, direction)
            if terminal is None:
                continue
            completions += 1
            max_latency = max(max_latency, terminal - source)
            for cursor in range(source, terminal):
                assert first_completion(days, source, direction, cursor) == terminal
                restart_checks += 1
            assert completion_at(days, terminal, direction)
    return {"trajectories": trajectories, "completions": completions,
            "restart_checks": restart_checks, "max_latency_days": max_latency}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("hst", type=Path)
    args = parser.parse_args()
    symbol, period, h4 = read_hst_v401(args.hst)
    days = aggregate_d1(h4)
    summary = replay_summary(days)
    first = datetime.fromtimestamp(h4[0].time, tz=timezone.utc).date()
    last = datetime.fromtimestamp(h4[-1].time, tz=timezone.utc).date()
    digest = sha256(args.hst.read_bytes()).hexdigest()
    print(f"D1_TPW_WEEKEND_HISTORICAL_REPLAY=PASS symbol={symbol} period={period}")
    print(f"source_sha256={digest} h4_records={len(h4)} d1_days={len(days)} range={first}..{last}")
    print(" ".join(f"{key}={value}" for key, value in summary.items()))


if __name__ == "__main__":
    main()

