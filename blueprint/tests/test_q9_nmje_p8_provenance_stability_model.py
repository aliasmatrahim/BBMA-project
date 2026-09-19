#!/usr/bin/env python3
from dataclasses import dataclass

NA=0
BUILDING=1
SUPPORTING=2
ALIGNED=3
CONFLICT=4
UNRESOLVED=5

@dataclass
class M5:
    present: bool=False
    relation: int=UNRESOLVED
    event: str=""
    stable_relation: int=UNRESOLVED
    stable_event: str=""

@dataclass
class Journey:
    parent_kind: str=""
    parent: str=""
    journey: str=""
    relation: int=NA
    evidence: str=""
    stable_relation: int=NA
    stable_evidence: str=""
    transitioned: bool=False
    previous_parent: str=""
    m5: M5=None

    def __post_init__(self):
        if self.m5 is None:
            self.m5=M5()

def apply(previous: Journey, current: Journey):
    current.stable_relation=current.relation
    current.stable_evidence=current.evidence
    previous_has=bool(previous.parent and previous.journey)
    current_has=bool(current.parent and current.journey)

    if previous_has and not current_has:
        current.transitioned=True
        current.previous_parent=previous.parent
        current.stable_evidence=""
        return "PARENT_CONTEXT_LOST"
    if not current_has:
        current.stable_evidence=""
        return "NO_CURRENT_PARENT"

    same=(previous_has and previous.parent_kind==current.parent_kind and
          previous.parent==current.parent and previous.journey==current.journey)
    if previous_has and not same:
        current.transitioned=True
        current.previous_parent=previous.parent
        return "PARENT_TRANSITION_CURRENT_EVIDENCE" if current.evidence else "PARENT_TRANSITION_RAW_INIT"
    if current.evidence:
        return "CURRENT_CANONICAL_EVIDENCE"
    if same and previous.stable_evidence:
        current.stable_relation=previous.stable_relation
        current.stable_evidence=previous.stable_evidence
        return "HOLD_LAST_PROVEN_RELATION"
    return "NO_PRIOR_PROVEN_RELATION"

def m5_stable_evidence(context,state,event):
    if not event:
        return False
    if context=="RE":
        return state=="CONFIRMED"
    if context=="EXT":
        return state in ("REVERSAL_CONFIRMED","RETEST_PHASE","RETEST_READY")
    return False

def apply_m5(previous: Journey, current: Journey, context="",state=""):
    same=(previous.parent and previous.parent_kind==current.parent_kind and
          previous.parent==current.parent and previous.journey==current.journey)
    m=current.m5
    m.stable_relation=m.relation
    m.stable_event=""
    if m.present and m5_stable_evidence(context,state,m.event):
        m.stable_event=m.event
        return "CURRENT_M5_CANONICAL_EVIDENCE"
    if same and previous.m5.stable_event:
        m.stable_relation=previous.m5.stable_relation
        m.stable_event=previous.m5.stable_event
        return "HOLD_LAST_PROVEN_M5_RELATION"
    if not same and previous.m5.stable_event:
        return "PARENT_TRANSITION_CLEARS_M5_STABILITY"
    return "CURRENT_M5_DEVELOPING" if m.present else "NO_CURRENT_M5_CONTEXT"

def main():
    # Proven relation seeds stability.
    prev=Journey("H4_OWNER","PE1","J1",ALIGNED,"EV1",ALIGNED,"EV1")
    cur=Journey("H4_OWNER","PE1","J1",BUILDING,"")
    assert apply(prev,cur)=="HOLD_LAST_PROVEN_RELATION"
    assert cur.relation==BUILDING                 # raw relation remains current
    assert cur.stable_relation==ALIGNED          # stable observer holds last proof
    assert cur.stable_evidence=="EV1"

    # A new attributable canonical event advances stable relation immediately.
    cur2=Journey("H4_OWNER","PE1","J1",SUPPORTING,"EV2")
    assert apply(cur,cur2)=="CURRENT_CANONICAL_EVIDENCE"
    assert cur2.stable_relation==SUPPORTING
    assert cur2.stable_evidence=="EV2"

    # Parent identity transition never carries the old stable relation.
    cur3=Journey("H4_RE","PE2","J2",BUILDING,"")
    assert apply(cur2,cur3)=="PARENT_TRANSITION_RAW_INIT"
    assert cur3.transitioned
    assert cur3.previous_parent=="PE1"
    assert cur3.stable_relation==BUILDING
    assert cur3.stable_evidence==""

    # Loss of current parent clears carry-forward and records the transition.
    lost=Journey(relation=UNRESOLVED)
    assert apply(cur3,lost)=="PARENT_CONTEXT_LOST"
    assert lost.transitioned
    assert lost.previous_parent=="PE2"
    assert lost.stable_evidence==""

    # Candidate/RAW M5 context is raw-only; it does not replace last proof.
    p=Journey("H4_OWNER","PE1","J1")
    p.m5=M5(True,ALIGNED,"M5CONF",ALIGNED,"M5CONF")
    c=Journey("H4_OWNER","PE1","J1")
    c.m5=M5(True,BUILDING,"M5CAND")
    assert apply_m5(p,c,"RE","CANDIDATE")=="HOLD_LAST_PROVEN_M5_RELATION"
    assert c.m5.present is True
    assert c.m5.relation==BUILDING
    assert c.m5.stable_relation==ALIGNED
    assert c.m5.stable_event=="M5CONF"

    # Confirmed M5 RE and reversal-confirmed+ Extreme are stable evidence.
    n=Journey("H4_OWNER","PE1","J1")
    n.m5=M5(True,SUPPORTING,"M5NEW")
    assert apply_m5(c,n,"RE","CONFIRMED")=="CURRENT_M5_CANONICAL_EVIDENCE"
    assert n.m5.stable_event=="M5NEW"

    for st in ("REVERSAL_CONFIRMED","RETEST_PHASE","RETEST_READY"):
        x=Journey("H4_OWNER","PE1","J1")
        x.m5=M5(True,SUPPORTING,"X"+st)
        assert apply_m5(n,x,"EXT",st)=="CURRENT_M5_CANONICAL_EVIDENCE"

    raw=Journey("H4_OWNER","PE1","J1")
    raw.m5=M5(True,BUILDING,"XRAW")
    assert apply_m5(n,raw,"EXT","RAW")=="HOLD_LAST_PROVEN_M5_RELATION"

    # Parent transition clears M5 stable carry-forward and never manufactures
    # current M5 presence.
    z=Journey("H4_RE","PE9","J9")
    z.m5=M5(False,UNRESOLVED,"")
    assert apply_m5(n,z)=="PARENT_TRANSITION_CLEARS_M5_STABILITY"
    assert z.m5.present is False
    assert z.m5.stable_event==""

    print("Q9_NMJE_P8_PROVENANCE_STABILITY_MODEL=PASS")

if __name__=="__main__":
    main()
