#!/usr/bin/env python3
from dataclasses import dataclass

@dataclass
class Trade:
    ticket: int
    magic: int
    open_time: int
    execution_hash: str

@dataclass
class Attr:
    journey: str
    parent: str
    relation: int
    m5_present: bool = False
    m5_event: str = ""
    m5_reason: str = ""
    m5_relation: int = 5
    m5_direction: int = 0
    m5_context: int = 0
    m5_start: int = 0
    m5_closed: int = 0

def chunks(value: str):
    assert len(value) == 16
    return [value[i:i+4] for i in range(0, 16, 4)]

def save(store, trade: Trade, attr: Attr):
    base = f"BBXA1|T{trade.ticket}|"
    for k in list(store):
        if k.startswith(base):
            del store[k]
    store[base+"M"] = trade.magic
    store[base+"O"] = trade.open_time
    store[base+"R"] = attr.relation
    store[base+"M5"] = int(attr.m5_present)
    store[base+"MC"] = attr.m5_context
    for pfx,val in (("X",trade.execution_hash),("J",attr.journey),("P",attr.parent)):
        for i,x in enumerate(chunks(val)):
            store[base+pfx+str(i)] = x
    if attr.m5_present:
        store[base+"MR"] = attr.m5_relation
        store[base+"MD"] = attr.m5_direction
        store[base+"MS"] = attr.m5_start
        store[base+"MT"] = attr.m5_closed
        for pfx,val in (("E",attr.m5_event),("Q",attr.m5_reason)):
            for i,x in enumerate(chunks(val)):
                store[base+pfx+str(i)] = x
    store[base+"V"] = 1

def load(store, trade: Trade):
    base = f"BBXA1|T{trade.ticket}|"
    for k in ("V","M","O","R","M5","MC"):
        if base+k not in store:
            return None
    if store[base+"V"] != 1 or store[base+"M"] != trade.magic or store[base+"O"] != trade.open_time:
        return None
    def join(pfx):
        ks=[base+pfx+str(i) for i in range(4)]
        return None if any(k not in store for k in ks) else "".join(store[k] for k in ks)
    if join("X") != trade.execution_hash:
        return None
    j,p=join("J"),join("P")
    if not j or not p:
        return None
    out=Attr(j,p,store[base+"R"],bool(store[base+"M5"]),m5_context=store[base+"MC"])
    if out.m5_present:
        for k in ("MR","MD","MS","MT"):
            if base+k not in store:
                return None
        out.m5_event, out.m5_reason = join("E"), join("Q")
        if not out.m5_event or not out.m5_reason:
            return None
        out.m5_relation=store[base+"MR"]; out.m5_direction=store[base+"MD"]
        out.m5_start=store[base+"MS"]; out.m5_closed=store[base+"MT"]
        if out.m5_direction not in (1,2) or out.m5_context <= 0 or out.m5_start <= 0 or out.m5_closed < out.m5_start:
            return None
    return out

def main():
    t=Trade(42,868813,1700000000,"0123456789ABCDEF")
    a=Attr("1111222233334444","AAAABBBBCCCCDDDD",2)
    store={}
    save(store,t,a)
    assert load(store,t)==a

    bad=dict(store); bad.pop("BBXA1|T42|V")
    assert load(bad,t) is None
    assert load(store,Trade(42,868814,t.open_time,t.execution_hash)) is None
    assert load(store,Trade(42,t.magic,t.open_time,"FEDCBA9876543210")) is None

    m=Attr("1111222233334444","AAAABBBBCCCCDDDD",3,True,
           "9999888877776666","1234123412341234",4,1,2,1700000100,1700000400)
    store={}
    save(store,t,m)
    assert load(store,t)==m
    bad=dict(store); bad["BBXA1|T42|MT"]=1700000001
    assert load(bad,t) is None
    print("Q9_NMJE_P4_PERSISTENCE_MODEL=PASS")

if __name__=="__main__":
    main()
