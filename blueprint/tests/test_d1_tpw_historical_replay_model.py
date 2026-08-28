#!/usr/bin/env python3
"""Synthetic firewall for the offline D1TPW historical replay engine."""
from pathlib import Path
import sys


sys.path.insert(0, str(Path("blueprint/tools").resolve()))
from d1_tpw_weekend_historical_replay import Bar, aggregate_d1, completion_at, first_completion, replay_summary  # noqa: E402


def main() -> None:
    h4 = []
    base = 1704067200
    price = 1.1000
    for day in range(20):
        for slot in range(6):
            timestamp = base + day * 86400 + slot * 14400
            drift = day * 0.0002
            high = price + drift + 0.0003
            low = price + drift - 0.0003
            if day == 14:
                high += 0.0100
            if day == 16:
                low -= 0.0100
            h4.append(Bar(timestamp, price + drift, high, low, price + drift))
    days = aggregate_d1(h4)
    assert len(days) == 20
    assert completion_at(days, 14, "BUY")
    assert completion_at(days, 16, "SELL")

    buy_terminal = first_completion(days, 13, "BUY")
    sell_terminal = first_completion(days, 15, "SELL")
    assert buy_terminal == 14 and sell_terminal == 16
    assert first_completion(days, 13, "BUY", 13) == buy_terminal
    assert first_completion(days, 15, "SELL", 15) == sell_terminal

    summary = replay_summary(days)
    assert summary["trajectories"] > 0
    assert summary["completions"] > 0
    assert summary["restart_checks"] >= summary["completions"]
    print("D1_TPW_HISTORICAL_REPLAY_MODEL=PASS")


if __name__ == "__main__":
    main()

