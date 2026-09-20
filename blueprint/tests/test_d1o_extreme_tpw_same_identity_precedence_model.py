#!/usr/bin/env python3

EXTREME_TPW = "EXTREME_TPW"
D1_REENTRY = "RE_ENTRY"


def same_identity(a, b):
    return (
        a["signal"] == b["signal"] == "RE_ENTRY"
        and a["direction"] == b["direction"]
        and a["tf"] == b["tf"]
        and a["confirm"] == b["confirm"]
        and a["seq"] == b["seq"]
    )


def prefer_extreme_tpw_enrichment(a, b):
    if not same_identity(a, b):
        return 0
    a_ext = a.get("uses_d1o") and a.get("family") == EXTREME_TPW
    b_ext = b.get("uses_d1o") and b.get("family") == EXTREME_TPW
    if a_ext == b_ext:
        return 0
    return 1 if a_ext else -1


def candidate(*, uses_d1o=False, family=None, confirm=100, direction="BUY",
              tf="H1", seq="ABC"):
    return {
        "signal": "RE_ENTRY",
        "direction": direction,
        "tf": tf,
        "confirm": confirm,
        "seq": seq,
        "uses_d1o": uses_d1o,
        "family": family,
    }


def main():
    standalone = candidate()
    extreme = candidate(uses_d1o=True, family=EXTREME_TPW)

    assert prefer_extreme_tpw_enrichment(extreme, standalone) == 1
    assert prefer_extreme_tpw_enrichment(standalone, extreme) == -1

    # No generic D1 Opportunity precedence.
    normal_d1o = candidate(uses_d1o=True, family=D1_REENTRY)
    assert prefer_extreme_tpw_enrichment(normal_d1o, standalone) == 0
    assert prefer_extreme_tpw_enrichment(standalone, normal_d1o) == 0

    # A different structural identity is not enrichment and keeps normal ordering.
    later_extreme = candidate(uses_d1o=True, family=EXTREME_TPW, confirm=200, seq="DEF")
    assert prefer_extreme_tpw_enrichment(later_extreme, standalone) == 0

    # Direction mismatch cannot be the same identity.
    sell_extreme = candidate(uses_d1o=True, family=EXTREME_TPW, direction="SELL")
    assert prefer_extreme_tpw_enrichment(sell_extreme, standalone) == 0

    print("D1O_EXTREME_TPW_PRECEDENCE_MODEL=PASS")


if __name__ == "__main__":
    main()
