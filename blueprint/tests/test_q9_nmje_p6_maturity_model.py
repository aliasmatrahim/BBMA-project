#!/usr/bin/env python3
from dataclasses import dataclass

NONE=0
OWNER_ONLY=1
EXT_DEV=2
EXT_MATURE=3
MHV_DEV=4
MHV_MATURE=5
DIRECTION=6
RE_CAND=7
RE_CONF=8
MOMENTUM=9
TRANSITION=10
UNRESOLVED=11

VALID=set(range(12))

@dataclass
class Attr:
    maturity:int=UNRESOLVED
    m5_present:bool=False
    m5_maturity:int=UNRESOLVED
    m5_context:int=0
    m5_state:int=0

def m5_state_valid(context,state):
    if context==1:
        return state in (1,2)  # RE candidate/confirmed
    if context==2:
        return state in (1,2,3,4)  # Extreme RAW/REV/RETEST_PHASE/READY
    return False

def load_p6(store):
    out=Attr()
    if "JM" in store:
        if store["JM"] not in VALID:
            return None
        out.maturity=store["JM"]
    out.m5_present=bool(store.get("M5",0))
    if out.m5_present:
        has_m="M5M" in store
        has_s="M5S" in store
        if has_m != has_s:
            return None
        out.m5_context=store.get("MC",0)
        if has_m:
            if store["M5M"] not in VALID:
                return None
            if not m5_state_valid(out.m5_context,store["M5S"]):
                return None
            out.m5_maturity=store["M5M"]
            out.m5_state=store["M5S"]
    return out

def save_p6(attr):
    assert attr.maturity in VALID
    store={"JM":attr.maturity,"M5":int(attr.m5_present),"MC":attr.m5_context}
    if attr.m5_present:
        assert attr.m5_maturity in VALID
        assert m5_state_valid(attr.m5_context,attr.m5_state)
        store["M5M"]=attr.m5_maturity
        store["M5S"]=attr.m5_state
    return store

def main():
    # New P6 record round trip.
    a=Attr(RE_CONF,True,EXT_MATURE,2,4)
    assert load_p6(save_p6(a))==a

    # Pre-P6 P4 record remains readable: missing additive keys degrade only
    # research metadata to UNRESOLVED/state 0.
    legacy={"M5":1,"MC":1}
    x=load_p6(legacy)
    assert x is not None
    assert x.maturity==UNRESOLVED
    assert x.m5_maturity==UNRESOLVED
    assert x.m5_state==0

    # Partial/corrupt P6 metadata fails closed.
    assert load_p6({"M5":1,"MC":1,"M5M":RE_CONF}) is None
    assert load_p6({"JM":99,"M5":0,"MC":0}) is None
    assert load_p6({"M5":1,"MC":2,"M5M":EXT_MATURE,"M5S":99}) is None
    print("Q9_NMJE_P6_MATURITY_MODEL=PASS")

if __name__=="__main__":
    main()
