#!/usr/bin/env python3
"""Build 5.07 N2/F07 scope guard against merged Build 5.06."""
from pathlib import Path
import subprocess

BASE="49206bc1fd148c4faf6f34e733b95e6e9e4f2bf1"
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
 "void UpdateNestedJourneyObservation(",
 "void NMJE_PrintValidatedDecisionShadow(",
 "void NMJE_PrintClosedOutcomeShadow(",
 "void CompactMonitoredTrades(",
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
 "void ProcessEntry(",
 "bool RunEntryPreflightAndExecute(",
 "void ManagePositions(",
 "void RebuildExecutionHistory(",
 "void RecoverExistingOrders(",
]
for sig in protected:
    assert body(base,sig)==body(cand,sig), "protected body changed: "+sig

assert body(base,"bool ReconcileExecutionAmbiguityHold(") != body(
    cand,"bool ReconcileExecutionAmbiguityHold(")
assert base.count("OrderSend(")==1
assert cand.count("OrderSend(")==1
assert '#property version   "5.07"' in cand
assert "V507_N2_F07_CLOSED_OUTCOME_BRIDGE_20260922" in cand
assert "N2_F07_CLOSED_OUTCOME_BRIDGE_229_20260922" in cand
print("N2_507_PROTECTED_BODIES=PASS count="+str(len(protected)))
