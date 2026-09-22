#!/usr/bin/env python3
"""M19 ownership and fail-closed source contract guards."""
from pathlib import Path
SRC = Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")
def body(signature):
    start = SRC.index(signature)
    brace = SRC.index("{", start)
    depth = 0
    for i in range(brace, len(SRC)):
        depth += (SRC[i] == "{") - (SRC[i] == "}")
        if depth == 0:
            return SRC[start:i + 1]
    raise AssertionError(signature)
def main():
    total = body("double CalculateTotalRisk(")
    basket = body("double CalculateBasketLossPercent_EA(")
    assert total.count("OrderSelect(") == 1
    assert "IsLiveEAOwnedPortfolioTrade(i)" not in total, "selector failure hidden by boolean helper"
    selected = total.index("if(!OrderSelect(")
    rejected = total.index("valid = false;", selected)
    ownership = total.index("int expectedMagic")
    assert selected < rejected < ownership
    assert "g_monitored_trades[i].magic_number != expectedMagic" in total
    assert "OrderMagicNumber() != expectedMagic" in total
    assert "expectedMagic <= 0" in total and "if(pairIdx < 0) continue;" in total
    assert "if(!IsLiveEAOwnedPortfolioTrade(i)) continue;" in basket
    print("M19_OWNED_RISK_AGGREGATION_STATIC=PASS")
if __name__ == "__main__":
    main()
