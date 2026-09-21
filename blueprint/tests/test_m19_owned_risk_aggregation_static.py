#!/usr/bin/env python3
from pathlib import Path

SRC = Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")

def body(signature):
    start = SRC.index(signature)
    brace = SRC.index("{", start)
    depth = 0
    for i in range(brace, len(SRC)):
        if SRC[i] == "{":
            depth += 1
        elif SRC[i] == "}":
            depth -= 1
            if depth == 0:
                return SRC[start:i + 1]
    raise AssertionError(signature)

def main():
    total = body("double CalculateTotalRisk(")
    basket = body("double CalculateBasketLossPercent_EA(")
    assert "if(!IsLiveEAOwnedPortfolioTrade(i)) continue;" in total
    assert "if(!IsLiveEAOwnedPortfolioTrade(i)) continue;" in basket
    assert total.count("IsLiveEAOwnedPortfolioTrade(i)") == 1
    assert basket.count("IsLiveEAOwnedPortfolioTrade(i)") == 1
    print("M19_OWNED_RISK_AGGREGATION_STATIC=PASS")

if __name__ == "__main__":
    main()
