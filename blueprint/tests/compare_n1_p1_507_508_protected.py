#!/usr/bin/env python3
from pathlib import Path
import subprocess

BASE="17e940a42d5495075e1f17f8b741816ff662ee59"
base=subprocess.check_output(["git","show",BASE+":blueprint/source/BBMA_EA.mq4"]).decode("utf-8").replace("\r\n","\n")
cand=Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8").replace("\r\n","\n")

def body(src,signature):
    start=src.index(signature); brace=src.index("{",start); depth=0
    for i in range(brace,len(src)):
        depth+=(src[i]=="{")-(src[i]=="}")
        if depth==0:return src[start:i+1]
    raise AssertionError(signature)

protected=[
 "void CollectSignalSnapshots(",
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
 "bool SaveExecutionAmbiguityHold(",
 "bool LoadExecutionAmbiguityHold(",
 "bool LatchExecutionAmbiguity(",
 "int FindExecutionAmbiguityTicket(",
 "bool AdoptAmbiguousExecutionTicket(",
 "bool ReconcileExecutionAmbiguityHold(",
 "void NMJE_PrintClosedOutcomeShadow(",
 "void CompactMonitoredTrades(",
 "void ProcessEntry(",
 "bool RunEntryPreflightAndExecute(",
 "void ManagePositions(",
 "void RebuildExecutionHistory(",
 "void RecoverExistingOrders(",
]
for sig in protected:
    assert body(base,sig)==body(cand,sig), "protected body changed: "+sig

assert base.count("OrderSend(")==cand.count("OrderSend(")==1
assert '#property version   "5.08"' in cand
assert "V508_N1_P1_LINEAGE_PROVENANCE_20260922" in cand
assert "N1_P1_LINEAGE_PROVENANCE_231_20260922" in cand
for forbidden in ("NMJE_PassExecutionGate","REJ_NMJE_RELATION","N3_POLICY_ACTIVE","PERIOD_M5"):
    assert forbidden not in cand
print("N1_P1_508_PROTECTED_BODIES=PASS count="+str(len(protected)))
