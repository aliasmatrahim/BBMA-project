#!/usr/bin/env python3
"""F05 scope guard against merged Build 5.05."""
from pathlib import Path
import subprocess

BASE="2e524cdfe8829da774698cb96c8fc848518250d3"
base=subprocess.check_output(
    ["git","show",BASE+":blueprint/source/BBMA_EA.mq4"]
).decode("utf-8").replace("\r\n","\n")
cand=Path("blueprint/source/BBMA_EA.mq4").read_text(
    encoding="utf-8").replace("\r\n","\n")

def body(src,signature):
    start=src.index(signature)
    brace=src.index("{",start)
    depth=0
    for i in range(brace,len(src)):
        depth += (src[i]=="{")-(src[i]=="}")
        if depth==0:
            return src[start:i+1]
    raise AssertionError(signature)

protected=[
 "int CompareCanonicalCandidates(",
 "void PriorityEngine_Atomic(",
 "void InvalidationEngine_Atomic(",
 "bool ResolveExecutionReferencePrice(",
 "bool ResolveApprovedInitialSLTP(",
 "bool ValidateSLTP(",
 "double CalculateTotalRisk(",
 "double CalculateLotSize(",
 "void FinalPortfolioGuard(",
 "bool BrokerConfirmsNoLiveEAOwnedOrders(",
 "int FindExistingExecutionTicket(",
 "int SendOrderWithRetry(",
 "string ExecutionAmbiguityGVBase(",
 "bool SaveExecutionAmbiguityHold(",
 "bool LoadExecutionAmbiguityHold(",
 "bool LatchExecutionAmbiguity(",
 "int FindExecutionAmbiguityTicket(",
 "bool AdoptAmbiguousExecutionTicket(",
 "bool ReconcileExecutionAmbiguityHold(",
 "void ManagePositions(",
 "void RebuildExecutionHistory(",
 "void RecoverExistingOrders(",
]
for sig in protected:
    assert body(base,sig)==body(cand,sig), "protected body changed: "+sig

assert base.count("OrderSend(")==1
assert cand.count("OrderSend(")==1
assert '#property version   "5.06"' in cand
assert "V506_F05_SELECTION_UNCERTAINTY_FAIL_CLOSED_20260922" in cand
assert "F05_SELECTION_UNCERTAINTY_FAIL_CLOSED_226_20260922" in cand
print("F05_506_PROTECTED_BODIES=PASS count="+str(len(protected)))
