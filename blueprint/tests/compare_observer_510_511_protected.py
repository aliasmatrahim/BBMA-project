#!/usr/bin/env python3
from pathlib import Path
import subprocess

BASE="0cb24d250ce77c7629ef83d11b6c9db9c0773b1c"
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
 "bool ResolveExecutionReferencePrice(",
 "bool ResolveApprovedInitialSLTP(",
 "bool ValidateSLTP(",
 "double CalculateTotalRisk(",
 "double CalculateLotSize(",
 "void FinalPortfolioGuard(",
 "int FindExistingExecutionTicket(",
 "int SendOrderWithRetry(",
 "bool SaveExecutionAmbiguityHold(",
 "bool LatchExecutionAmbiguity(",
 "int FindExecutionAmbiguityTicket(",
 "bool AdoptAmbiguousExecutionTicket(",
 "bool ReconcileExecutionAmbiguityHold(",
 "void NMJE_PrintValidatedDecisionShadow(",
 "void NMJE_PrintClosedOutcomeShadow(",
 "void CompactMonitoredTrades(",
 "void ProcessEntry(",
 "bool RunEntryPreflightAndExecute(",
 "void ManagePositions(",
 "void RebuildExecutionHistory(",
 "void RecoverExistingOrders(",
 "int CountDashboardLiveEAOwnedTrades(",
 "void BuildDashboardSnapshot(",
 "void UpdateDashboard(",
 "void RefreshDashboardLiveTradeCount(",
 "int InitializeEA(",
 "void OnDeinit("
]
for sig in protected:
    assert body(base,sig)==body(cand,sig), "protected body changed: "+sig

for sig in (
 "void UpdateNestedJourneyObservation(",
 "void PriorityEngine_Atomic(",
 "void InvalidationEngine_Atomic(",
 "void PrintSignalBottleneckDiagnostic("
):
    assert body(base,sig)!=body(cand,sig), "intended observer body did not change: "+sig

assert base.count("OrderSend(")==cand.count("OrderSend(")==1
assert '#property version   "5.11"' in cand
assert "V511_EVENT_DRIVEN_OBSERVER_20260922" in cand
assert "OBSERVER_EVENT_DRIVEN_237_20260922" in cand
assert '[F7-BUILD] EA=BBMA_EA Build=5.11 BuildTag=' in cand
for forbidden in ("NMJE_PassExecutionGate","REJ_NMJE_RELATION","N3_POLICY_ACTIVE","PERIOD_M5"):
    assert forbidden not in cand
print("OBSERVER_511_PROTECTED_BODIES=PASS count="+str(len(protected)))
