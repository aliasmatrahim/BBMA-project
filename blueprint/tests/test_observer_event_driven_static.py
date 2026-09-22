#!/usr/bin/env python3
from pathlib import Path

SRC=Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")

def body(sig):
    start=SRC.index(sig); brace=SRC.index("{",start); depth=0
    for i in range(brace,len(SRC)):
        depth+=(SRC[i]=="{")-(SRC[i]=="}")
        if depth==0:return SRC[start:i+1]
    raise AssertionError(sig)

def main():
    for marker in (
        "Version 5.1.1 - Event-Driven Observer",
        '#property version   "5.11"',
        '#define BBMA_BUILD_TAG      "V511_EVENT_DRIVEN_OBSERVER_20260922"',
        '#define BBMA_SOURCE_REV_TAG "OBSERVER_EVENT_DRIVEN_237_20260922"',
        "string               g_observer_keys[];",
        "string               g_observer_last_messages[];",
        "int                  g_observer_record_count;",
        "bool ObserverShouldEmit(",
        "void ObserverPrintChanged(",
    ):
        assert marker in SRC, f"missing marker: {marker}"

    should=body("bool ObserverShouldEmit(")
    assert "DebugLevel >= DBG_FULL" in should
    assert "g_observer_keys[i]" in should and "key" in should
    assert "g_observer_last_messages[i]" in should and "message" in should
    assert "ArrayResize(g_observer_keys" in should
    assert "ArrayResize(g_observer_last_messages" in should

    n1=body("void UpdateNestedJourneyObservation(")
    assert 'Print("[N1-NMJE]' not in n1
    assert n1.count('ObserverPrintChanged("N1|"') == 3

    d10=body("void PrintSignalBottleneckDiagnostic(")
    assert 'Print("[D1-10' not in d10
    assert 'ObserverPrintChanged("D10A|" + pair' in d10
    assert 'ObserverPrintChanged("D10B|" + pair' in d10
    assert 'ObserverPrintChanged("D10C|" + pair' in d10

    m15=body("void PriorityEngine_Atomic(")
    assert "DebugLevel >= DBG_SIGNAL" in m15
    assert 'ObserverPrintChanged("M15_SELECT_M1|" + decision.Pair' in m15
    assert 'ObserverPrintChanged("M15_SELECT_M2|" + decision.Pair' in m15

    m16=body("void InvalidationEngine_Atomic(")
    assert 'ObserverPrintChanged("M16_PASS_M1|" + decision.Pair' in m16
    assert 'ObserverPrintChanged("M16_PASS_M2|" + decision.Pair' in m16
    assert '[P3M2][M16_REJECT]' in m16  # rejection remains directly visible

    pair=body("void ProcessPair(")
    assert 'Print("[P3M2][DECISION_FINAL]' in pair

    n2=body("void NMJE_PrintValidatedDecisionShadow(")
    assert 'Print("[N2-NMJE-DEC]' in n2

    entry=body("void ProcessEntry(")
    assert '[P3M2][EXEC]' in entry

    print("OBSERVER_EVENT_DRIVEN_STATIC=PASS")

if __name__=="__main__":
    main()
