#!/usr/bin/env python3
from pathlib import Path

SRC = Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")

def body(signature: str) -> str:
    start = SRC.index(signature)
    brace = SRC.index("{", start)
    depth = 0
    for i in range(brace, len(SRC)):
        if SRC[i] == "{":
            depth += 1
        elif SRC[i] == "}":
            depth -= 1
            if depth == 0:
                return SRC[start:i+1]
    raise AssertionError(signature)

def main() -> None:
    dash = body("void BuildDashboardSnapshot(")
    count = body("int CountDashboardLiveEAOwnedTrades(")
    refresh = body("void RefreshDashboardLiveTradeCount(")
    deinit = body("void OnDeinit(")

    assert 'string(BBMA_BUILD_TAG)' in dash, "dashboard must render canonical build tag"
    assert 'V4.5.9 P0 EXEC_ID Persistence Fix' not in dash, "historical dashboard identity must be removed"

    assert "OrdersTotal()" in count
    assert "MODE_TRADES" in count
    assert "IsExactEAOwnedSelectedOrder" in count
    assert "g_monitored_count" not in count

    assert "BuildDashboardSnapshot();" in refresh
    assert "UpdateDashboard();" in refresh
    for forbidden in ("CompactMonitoredTrades(", "OrderSend(", "OrderClose(", "OrderModify("):
        assert forbidden not in refresh

    assert 'Comment("");' in deinit
    print("M25_DASHBOARD_BUILD_IDENTITY=PASS")

if __name__ == "__main__":
    main()
