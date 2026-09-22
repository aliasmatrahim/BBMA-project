#!/usr/bin/env python3
"""F05 source guard for monitored-order selection uncertainty."""
from pathlib import Path

SRC=Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")

def body(signature):
    start=SRC.index(signature)
    brace=SRC.index("{",start)
    depth=0
    for i in range(brace,len(SRC)):
        depth += (SRC[i]=="{")-(SRC[i]=="}")
        if depth==0:
            return SRC[start:i+1]
    raise AssertionError(signature)

def main():
    assert "ENUM_PORTFOLIO_OWNERSHIP_STATE" in SRC
    assert "PORT_OWNERSHIP_UNKNOWN" in SRC
    assert "PORT_OWNERSHIP_EXCLUDED" in SRC
    assert "PORT_OWNERSHIP_LIVE_OWNED" in SRC
    assert "GetLiveEAOwnedPortfolioTradeState(" in SRC
    assert "bool IsLiveEAOwnedPortfolioTrade(" not in SRC

    helper=body("ENUM_PORTFOLIO_OWNERSHIP_STATE GetLiveEAOwnedPortfolioTradeState(")
    basket=body("double CalculateBasketLossPercent_EA(")
    limits=body("PortfolioStatus CheckPortfolioLimits(")
    lock=body("bool IsSignalAllowed(")
    manage=body("void ManagePortfolio(")
    risk=body("RiskStatus CheckRiskBeforeTrade(")

    assert "return PORT_OWNERSHIP_UNKNOWN;" in helper
    assert "bool &valid" in basket.split("{",1)[0]
    assert "PORT_OWNERSHIP_UNKNOWN" in basket
    assert "valid = false;" in basket
    assert "OrderSelect(" not in basket

    assert "PORT_OWNERSHIP_UNKNOWN" in limits
    assert "status.allowed = false;" in limits
    assert lock.count("PORT_OWNERSHIP_UNKNOWN") >= 2
    assert "return false;" in lock

    assert "bool basketValid = true;" in risk
    assert "Unable to calculate basket loss safely" in risk
    assert "REJ_BASKET_LOSS" in risk

    assert "bool basketValid = true;" in manage
    assert "static bool basketObservationUncertainLogged = false;" in manage
    assert "if(!basketObservationUncertainLogged)" in manage
    assert "Portfolio basket observation uncertain" in manage
    assert "basketObservationUncertainLogged = false;" in manage
    assert "g_portfolio_emergency_close_requested = true;" in manage

    # TradeLock mode0 remains unrestricted by this repair.
    off=lock.index("if(TradeLockMode == LOCK_ONE_POSITION)")
    assert "PORT_OWNERSHIP_UNKNOWN" not in lock[:off]

    assert '#property version   "5.06"' in SRC
    assert "V506_F05_SELECTION_UNCERTAINTY_FAIL_CLOSED_20260922" in SRC
    assert "F05_SELECTION_UNCERTAINTY_FAIL_CLOSED_226_20260922" in SRC
    print("F05_SELECTION_UNCERTAINTY_STATIC=PASS")

if __name__ == "__main__":
    main()
