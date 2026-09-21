#!/usr/bin/env python3

BUY = 1
SELL = -1

def validate_broker_geometry(direction, bid_pts, ask_pts, sl_pts, tp_pts,
                             stop_level_pts, freeze_level_pts, validate_tp=True):
    assert stop_level_pts >= 0
    assert freeze_level_pts >= 0
    required = max(stop_level_pts, freeze_level_pts)
    close = bid_pts if direction == BUY else ask_pts

    if direction == BUY:
        if sl_pts >= close or (close - sl_pts) < required:
            return "REJ_INVALID_SL"
        if validate_tp and (tp_pts <= close or (tp_pts - close) < required):
            return "REJ_INVALID_TP"
        return "PASS"

    if direction == SELL:
        if sl_pts <= close or (sl_pts - close) < required:
            return "REJ_INVALID_SL"
        if validate_tp and (tp_pts >= close or (close - tp_pts) < required):
            return "REJ_INVALID_TP"
        return "PASS"

    return "REJ_MARKET_PRICE_INVALID"


def validate_targetless_minrr(min_rr):
    return "PASS" if min_rr == 0 else "REJ_INVALID_RR"


def main():
    # Targetless lifecycle cannot silently bypass an enabled RR filter.
    assert validate_targetless_minrr(0) == "PASS"
    assert validate_targetless_minrr(0.01) == "REJ_INVALID_RR"

    # Exact required distance is valid.
    assert validate_broker_geometry(BUY, 110000, 110020, 109980, 110020, 20, 10) == "PASS"
    assert validate_broker_geometry(SELL, 110000, 110020, 110040, 110000, 20, 10) == "PASS"

    # BUY SL may be below Ask/Entry yet still be above Bid: reject wrong trigger side.
    assert validate_broker_geometry(BUY, 110000, 110020, 110010, 110040, 5, 0) == "REJ_INVALID_SL"

    # SELL SL may be above Bid/Entry yet still be below Ask: reject wrong trigger side.
    assert validate_broker_geometry(SELL, 110000, 110020, 110010, 109980, 5, 0) == "REJ_INVALID_SL"

    # FreezeLevel is independently frozen and the stricter broker guard wins.
    assert validate_broker_geometry(BUY, 110000, 110020, 109975, 110050, 10, 30) == "REJ_INVALID_SL"
    assert validate_broker_geometry(BUY, 110000, 110020, 109970, 110030, 10, 30) == "PASS"

    # Trigger-side TP checks are direction-aware too.
    assert validate_broker_geometry(BUY, 110000, 110020, 109950, 109990, 5, 0) == "REJ_INVALID_TP"
    assert validate_broker_geometry(SELL, 110000, 110020, 110070, 110030, 5, 0) == "REJ_INVALID_TP"

    # Targetless mode validates SL only and keeps TP absent.
    assert validate_broker_geometry(BUY, 110000, 110020, 109950, 0, 20, 10, False) == "PASS"

    print("M17_BROKER_DISTANCE_MODEL=PASS")


if __name__ == "__main__":
    main()
