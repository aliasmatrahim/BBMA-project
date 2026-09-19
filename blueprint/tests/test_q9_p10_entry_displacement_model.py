#!/usr/bin/env python3

BUY=1
SELL=2

def norm(direction, from_price, to_price, pip):
    if pip <= 0 or from_price <= 0 or to_price <= 0:
        return 0.0
    if direction == BUY:
        return (to_price-from_price)/pip
    if direction == SELL:
        return (from_price-to_price)/pip
    return 0.0

def valid(present, source_signal=0, tf=0, candle=0, src=0, pre=0, broker=0):
    if not present:
        return True
    if source_signal not in (7, 8):  # model-only RE / Extreme domain
        return False
    return tf>0 and candle>0 and src>0 and pre>0 and broker>0

def load(store):
    if "DP" not in store:
        return None
    if store["DP"] <= 0.5:
        return "INVALID"
    keys=("DSG","DTF","DCT","DSP","DPP","DBP","D12","D2B","D1B")
    if any(k not in store for k in keys):
        return "INVALID"
    return {k:store[k] for k in keys}

def main():
    pip=0.0001

    # BUY: higher execution is positive/extended.
    s=1.1000; p=1.1010; b=1.1012
    assert round(norm(BUY,s,p,pip),8)==10.0
    assert round(norm(BUY,p,b,pip),8)==2.0
    assert round(norm(BUY,s,b,pip),8)==12.0
    assert round(norm(BUY,s,p,pip)+norm(BUY,p,b,pip),8)==round(norm(BUY,s,b,pip),8)

    # SELL: lower execution is positive/extended.
    s=1.2000; p=1.1990; b=1.1987
    assert round(norm(SELL,s,p,pip),8)==10.0
    assert round(norm(SELL,p,b,pip),8)==3.0
    assert round(norm(SELL,s,b,pip),8)==13.0

    # Retracement is negative for both directions.
    assert norm(BUY,1.1000,1.0990,pip) < 0
    assert norm(SELL,1.2000,1.2010,pip) < 0

    # Pre-P10 records are backward-readable as displacement unavailable.
    assert load({}) is None

    # Optional displacement payload is all-or-none.
    assert load({"DP":1.0}) == "INVALID"
    full={"DP":1.0,"DSG":7,"DTF":60,"DCT":1000,
          "DSP":1.1,"DPP":1.101,"DBP":1.1012,
          "D12":10.0,"D2B":2.0,"D1B":12.0}
    assert load(full)["D1B"]==12.0

    assert valid(False)
    assert valid(True,7,60,1000,1.1,1.101,1.1012)
    assert not valid(True,0,60,1000,1.1,1.101,1.1012)
    print("Q9_P10_ENTRY_DISPLACEMENT_MODEL=PASS")

if __name__=="__main__":
    main()
