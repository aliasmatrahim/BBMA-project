#!/usr/bin/env python3
"""C1-B closed-candle price-predicate fixtures derived from build 4.71."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


BUY = "BUY"
SELL = "SELL"


def raw_extreme(direction: str, ma5_high: float, ma10_high: float,
                ma5_low: float, ma10_low: float, top: float, low: float) -> bool:
    if direction == SELL:
        return ma5_high > top or ma10_high > top
    if direction == BUY:
        return ma5_low < low or ma10_low < low
    return False


def reversal(direction: str, open_: float, close: float) -> bool:
    if direction == SELL:
        return close < open_
    if direction == BUY:
        return close > open_
    return False


def body_cross(direction: str, open_: float, close: float, level: float) -> bool:
    if min(open_, close, level) <= 0:
        return False
    if direction == BUY:
        return open_ <= level and close > level
    if direction == SELL:
        return open_ >= level and close < level
    return False


def csm(direction: str, close: float, current: tuple[float, float, float, float],
        previous: tuple[float, float, float, float]) -> bool:
    top, mid, low, width = current
    prev_top, prev_mid, prev_low, prev_width = previous
    expanding = width > prev_width
    if direction == BUY:
        return expanding and mid > prev_mid and top > prev_top and close > top
    if direction == SELL:
        return expanding and mid < prev_mid and low < prev_low and close < low
    return False


def ecsd(direction: str, open_: float, close: float, ma5_high: float,
         ma10_high: float, ma5_low: float, ma10_low: float) -> bool:
    if direction == BUY:
        return body_cross(BUY, open_, close, ma5_high) and body_cross(
            BUY, open_, close, ma10_high
        )
    if direction == SELL:
        return body_cross(SELL, open_, close, ma5_low) and body_cross(
            SELL, open_, close, ma10_low
        )
    return False


def csd(direction: str, open_: float, close: float, ma5_high: float,
        ma10_high: float, ma5_low: float, ma10_low: float, mid: float) -> bool:
    return ecsd(
        direction, open_, close, ma5_high, ma10_high, ma5_low, ma10_low
    ) and body_cross(direction, open_, close, mid)


def cluster_touch(direction: str, high: float, low: float, close: float,
                  ma5: float, ma10: float) -> bool:
    if direction == BUY:
        return low <= max(ma5, ma10) and close >= ma5 and close >= ma10
    if direction == SELL:
        return high >= min(ma5, ma10) and close <= ma5 and close <= ma10
    return False


def ma5_or_ma50_touch(direction: str, high: float, low: float, close: float,
                      ma5: float, ma50: float) -> bool:
    if direction == BUY:
        return ((low <= ma5 and close >= ma5) or
                (low <= ma50 and close >= ma50))
    if direction == SELL:
        return ((high >= ma5 and close <= ma5) or
                (high >= ma50 and close <= ma50))
    return False


def type1_close_failure(direction: str, close: float, ma5: float,
                        ma10: float) -> bool:
    if direction == BUY:
        return close < min(ma5, ma10)
    if direction == SELL:
        return close > max(ma5, ma10)
    return True


def structural_retrace(direction: str, previous_close: float,
                       current_close: float, has_cluster_touch: bool) -> bool:
    if has_cluster_touch:
        return True
    if direction == BUY:
        return current_close < previous_close
    if direction == SELL:
        return current_close > previous_close
    return False


def extreme_retest_start(direction: str, previous_close: float,
                         current_close: float) -> bool:
    if direction == SELL:
        return current_close > previous_close
    if direction == BUY:
        return current_close < previous_close
    return False


def extreme_retest_interaction(direction: str, high: float, low: float,
                               frozen_anchor: float, relevant_ma5: float) -> bool:
    body_touch = ((direction == SELL and high >= frozen_anchor) or
                  (direction == BUY and low <= frozen_anchor))
    ma5_touch = low <= relevant_ma5 <= high
    return body_touch or ma5_touch


def mhv_tpw_complete(parent_direction: str, high: float, low: float,
                     ma5_high: float, ma10_high: float,
                     ma5_low: float, ma10_low: float) -> bool:
    if parent_direction == SELL:
        return low <= ma5_low or low <= ma10_low
    if parent_direction == BUY:
        return high >= ma5_high or high >= ma10_high
    return False


def mhv_loss_phase(close: float, top: float, low: float,
                   prior_move_csm: bool) -> bool:
    return low <= close <= top and not prior_move_csm


def mhv_move_away(direction: str, previous_close: float,
                  current_close: float) -> bool:
    if direction == BUY:
        return current_close > previous_close
    if direction == SELL:
        return current_close < previous_close
    return False


def mhv_retest(direction: str, high: float, low: float,
               frozen_marked_body: float) -> bool:
    if direction == BUY:
        return low <= frozen_marked_body
    if direction == SELL:
        return high >= frozen_marked_body
    return False


@dataclass(frozen=True)
class Case:
    name: str
    predicate: Callable[[], bool]
    expected: bool


def main() -> None:
    buy_band = (1.2000, 1.1500, 1.1000, 0.1000)
    buy_prev = (1.1900, 1.1400, 1.1050, 0.0850)
    sell_band = (1.2000, 1.1500, 1.1000, 0.1000)
    sell_prev = (1.1950, 1.1600, 1.1100, 0.0850)

    cases = [
        Case("raw_sell_above", lambda: raw_extreme(SELL, 1.201, 1.190, 1.0, 1.0, 1.200, 1.100), True),
        Case("raw_sell_equal", lambda: raw_extreme(SELL, 1.200, 1.190, 1.0, 1.0, 1.200, 1.100), False),
        Case("raw_buy_below", lambda: raw_extreme(BUY, 1.3, 1.3, 1.099, 1.110, 1.200, 1.100), True),
        Case("raw_buy_equal", lambda: raw_extreme(BUY, 1.3, 1.3, 1.100, 1.110, 1.200, 1.100), False),
        Case("reversal_sell", lambda: reversal(SELL, 1.200, 1.190), True),
        Case("reversal_sell_equal", lambda: reversal(SELL, 1.200, 1.200), False),
        Case("reversal_buy", lambda: reversal(BUY, 1.190, 1.200), True),
        Case("reversal_buy_equal", lambda: reversal(BUY, 1.200, 1.200), False),
        Case("cross_buy", lambda: body_cross(BUY, 1.100, 1.200, 1.150), True),
        Case("cross_buy_close_equal", lambda: body_cross(BUY, 1.100, 1.150, 1.150), False),
        Case("cross_sell", lambda: body_cross(SELL, 1.200, 1.100, 1.150), True),
        Case("cross_sell_close_equal", lambda: body_cross(SELL, 1.200, 1.150, 1.150), False),
        Case("csm_buy", lambda: csm(BUY, 1.205, buy_band, buy_prev), True),
        Case("csm_buy_width_equal", lambda: csm(BUY, 1.205, buy_band, (1.190, 1.140, 1.105, 0.100)), False),
        Case("csm_sell", lambda: csm(SELL, 1.095, sell_band, sell_prev), True),
        Case("csm_sell_inside", lambda: csm(SELL, 1.105, sell_band, sell_prev), False),
        Case("ecsd_buy", lambda: ecsd(BUY, 1.100, 1.220, 1.150, 1.160, 1.0, 1.0), True),
        Case("csd_buy", lambda: csd(BUY, 1.100, 1.220, 1.150, 1.160, 1.0, 1.0, 1.180), True),
        Case("csd_buy_mid_not_crossed", lambda: csd(BUY, 1.100, 1.170, 1.150, 1.160, 1.0, 1.0, 1.180), False),
        Case("ecsd_sell", lambda: ecsd(SELL, 1.220, 1.100, 1.0, 1.0, 1.160, 1.150), True),
        Case("csd_sell", lambda: csd(SELL, 1.220, 1.100, 1.0, 1.0, 1.160, 1.150, 1.180), True),
        Case("csd_sell_mid_not_crossed", lambda: csd(SELL, 1.170, 1.100, 1.0, 1.0, 1.160, 1.150, 1.180), False),
        Case("cluster_buy", lambda: cluster_touch(BUY, 1.130, 1.105, 1.120, 1.100, 1.110), True),
        Case("cluster_buy_no_low_touch", lambda: cluster_touch(BUY, 1.130, 1.115, 1.120, 1.100, 1.110), False),
        Case("cluster_sell", lambda: cluster_touch(SELL, 1.195, 1.170, 1.180, 1.200, 1.190), True),
        Case("cluster_sell_no_high_touch", lambda: cluster_touch(SELL, 1.185, 1.170, 1.180, 1.200, 1.190), False),
        Case("ma5_ma50_buy_ma50", lambda: ma5_or_ma50_touch(BUY, 1.2, 1.09, 1.11, 1.12, 1.10), True),
        Case("ma5_ma50_buy_none", lambda: ma5_or_ma50_touch(BUY, 1.2, 1.13, 1.14, 1.12, 1.10), False),
        Case("ma5_ma50_sell_ma5", lambda: ma5_or_ma50_touch(SELL, 1.21, 1.1, 1.18, 1.20, 1.22), True),
        Case("ma5_ma50_sell_none", lambda: ma5_or_ma50_touch(SELL, 1.19, 1.1, 1.18, 1.20, 1.22), False),
        Case("type1_buy_failure", lambda: type1_close_failure(BUY, 1.089, 1.100, 1.090), True),
        Case("type1_buy_boundary", lambda: type1_close_failure(BUY, 1.090, 1.100, 1.090), False),
        Case("type1_sell_failure", lambda: type1_close_failure(SELL, 1.201, 1.200, 1.190), True),
        Case("type1_sell_boundary", lambda: type1_close_failure(SELL, 1.200, 1.200, 1.190), False),
        Case("retrace_buy_progression", lambda: structural_retrace(BUY, 1.200, 1.190, False), True),
        Case("retrace_sell_progression", lambda: structural_retrace(SELL, 1.190, 1.200, False), True),
        Case("retrace_touch_override", lambda: structural_retrace(BUY, 1.190, 1.200, True), True),
        Case("retrace_buy_wrong_way", lambda: structural_retrace(BUY, 1.190, 1.200, False), False),
        Case("extreme_retest_start_sell", lambda: extreme_retest_start(SELL, 1.180, 1.190), True),
        Case("extreme_retest_start_buy", lambda: extreme_retest_start(BUY, 1.190, 1.180), True),
        Case("extreme_retest_wrong_sell", lambda: extreme_retest_start(SELL, 1.190, 1.180), False),
        Case("extreme_retest_wrong_buy", lambda: extreme_retest_start(BUY, 1.180, 1.190), False),
        Case("extreme_interaction_sell_body", lambda: extreme_retest_interaction(SELL, 1.201, 1.180, 1.200, 1.170), True),
        Case("extreme_interaction_buy_body", lambda: extreme_retest_interaction(BUY, 1.220, 1.099, 1.100, 1.230), True),
        Case("extreme_interaction_ma5", lambda: extreme_retest_interaction(BUY, 1.220, 1.180, 1.100, 1.200), True),
        Case("extreme_interaction_none", lambda: extreme_retest_interaction(SELL, 1.190, 1.180, 1.200, 1.170), False),
        Case("mhv_tpw_sell_parent", lambda: mhv_tpw_complete(SELL, 1.3, 1.09, 1.25, 1.24, 1.10, 1.11), True),
        Case("mhv_tpw_buy_parent", lambda: mhv_tpw_complete(BUY, 1.21, 1.0, 1.20, 1.19, 1.1, 1.1), True),
        Case("mhv_tpw_sell_not_complete", lambda: mhv_tpw_complete(SELL, 1.3, 1.12, 1.25, 1.24, 1.10, 1.11), False),
        Case("mhv_tpw_buy_not_complete", lambda: mhv_tpw_complete(BUY, 1.18, 1.0, 1.20, 1.19, 1.1, 1.1), False),
        Case("mhv_loss_inside", lambda: mhv_loss_phase(1.15, 1.20, 1.10, False), True),
        Case("mhv_loss_prior_csm", lambda: mhv_loss_phase(1.15, 1.20, 1.10, True), False),
        Case("mhv_loss_outside", lambda: mhv_loss_phase(1.21, 1.20, 1.10, False), False),
        Case("mhv_move_buy", lambda: mhv_move_away(BUY, 1.18, 1.19), True),
        Case("mhv_move_sell", lambda: mhv_move_away(SELL, 1.19, 1.18), True),
        Case("mhv_move_buy_wrong", lambda: mhv_move_away(BUY, 1.19, 1.18), False),
        Case("mhv_retest_buy", lambda: mhv_retest(BUY, 1.22, 1.10, 1.11), True),
        Case("mhv_retest_sell", lambda: mhv_retest(SELL, 1.20, 1.10, 1.19), True),
        Case("mhv_retest_buy_none", lambda: mhv_retest(BUY, 1.22, 1.12, 1.11), False),
    ]

    failures = []
    for case in cases:
        actual = case.predicate()
        if actual is not case.expected:
            failures.append(f"{case.name}: expected={case.expected} actual={actual}")
    if failures:
        raise AssertionError("; ".join(failures))

    print(f"BBMA_CORE_CANDLE_PRICE_EQUIVALENCE=PASS cases={len(cases)}")


if __name__ == "__main__":
    main()

