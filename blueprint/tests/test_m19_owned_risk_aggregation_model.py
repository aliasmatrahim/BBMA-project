#!/usr/bin/env python3
"""Deterministic M19 model: only live EA-owned monitored rows contribute."""
def owned(row):
    return (row["open"] and row["pair"] == "GBPUSD" and
            row["magic"] == row["expected_magic"] and
            row["registry_magic"] == row["expected_magic"])

def total_risk(rows, new_risk):
    return sum(r["risk"] for r in rows if owned(r)) + new_risk

def basket_loss(rows, equity):
    return sum(abs(r["profit"]) for r in rows if owned(r) and r["profit"] < 0) / equity * 100

def main():
    rows = [
        {"open": True, "pair": "GBPUSD", "magic": 1001, "registry_magic": 1001, "expected_magic": 1001, "risk": 20.0, "profit": -10.0},
        {"open": True, "pair": "GBPUSD", "magic": 2002, "registry_magic": 2002, "expected_magic": 1001, "risk": 900.0, "profit": -900.0},
        {"open": False, "pair": "GBPUSD", "magic": 1001, "registry_magic": 1001, "expected_magic": 1001, "risk": 700.0, "profit": -700.0},
    ]
    assert total_risk(rows, 5.0) == 25.0
    assert basket_loss(rows, 1000.0) == 1.0
    print("M19_OWNED_RISK_AGGREGATION_MODEL=PASS")

if __name__ == "__main__":
    main()
