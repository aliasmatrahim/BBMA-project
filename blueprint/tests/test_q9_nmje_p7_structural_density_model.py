#!/usr/bin/env python3
from dataclasses import dataclass

E=1
T=2
H=4
D=8
R=16
M=32
ALL=E|T|H|D|R|M

def count(mask):
    return sum(1 for bit in (E,T,H,D,R,M) if mask & bit)

def prefix(mask):
    out=0
    for bit in (E,T,H,D,R,M):
        if not (mask & bit):
            break
        out |= bit
    return out

def component_mask(kind):
    if kind=="EXTREME":
        return E
    if kind=="MLV":
        return E|T|H
    if kind=="RE":
        return R
    if kind in ("CSD","ECSD"):
        return D
    if kind=="CSM":
        return M
    return 0

@dataclass
class Density:
    present:bool=False
    mask:int=0
    prefix_mask:int=0
    stage_count:int=0

def valid(x):
    if not x.present:
        return x.mask==0 and x.prefix_mask==0 and x.stage_count==0
    if x.mask<=0 or x.mask>ALL:
        return False
    return x.prefix_mask==prefix(x.mask) and x.stage_count==count(x.mask)

def save(store,x):
    if not x.present:
        return
    assert valid(x)
    store["SDM"]=x.mask
    store["SDP"]=x.prefix_mask
    store["SDC"]=x.stage_count

def load(store):
    keys=("SDM","SDP","SDC")
    has=[k in store for k in keys]
    if any(has) and not all(has):
        return None
    if not any(has):
        return Density()
    x=Density(True,store["SDM"],store["SDP"],store["SDC"])
    return x if valid(x) else None

def main():
    # Exact component evidence never manufactures unrelated stages.
    assert component_mask("EXTREME")==E
    assert component_mask("RE")==R
    assert component_mask("CSD")==D
    assert component_mask("CSM")==M

    # Canonical F1 mature MLV proves prior Extreme + TPW + MHV.
    assert component_mask("MLV")==E|T|H

    # REM-like MLV + RE support is dense but has a direction gap, so
    # contiguous sequence prefix stops at MHV. It is not invalid.
    rem_like=component_mask("MLV")|component_mask("RE")
    assert rem_like==E|T|H|R
    assert count(rem_like)==4
    assert prefix(rem_like)==E|T|H

    # Direction closes the next stage; Momentum is not inferred.
    with_direction=rem_like|D
    assert count(with_direction)==5
    assert prefix(with_direction)==E|T|H|D|R

    # A later-stage observation alone never backfills missing intermediate stages.
    sparse=E|M
    assert count(sparse)==2
    assert prefix(sparse)==E

    # Full observed cycle is cardinality six, not a score.
    full=Density(True,ALL,ALL,6)
    assert valid(full)

    # P7 persistence is additive/backward-readable.
    legacy={}
    assert load(legacy)==Density()

    store={}
    save(store,full)
    assert load(store)==full

    # Partial/corrupt optional metadata fails closed.
    assert load({"SDM":ALL}) is None
    assert load({"SDM":ALL,"SDP":ALL}) is None
    assert load({"SDM":64,"SDP":0,"SDC":1}) is None
    assert load({"SDM":E|T|H|R,"SDP":E|T|H|R,"SDC":4}) is None
    assert load({"SDM":E|T|H,"SDP":E|T|H,"SDC":2}) is None
    print("Q9_NMJE_P7_STRUCTURAL_DENSITY_MODEL=PASS")

if __name__=="__main__":
    main()
