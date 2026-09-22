#!/usr/bin/env python3
from pathlib import Path
import subprocess

BASE="a4cd2363c5f9d3fe9655177d41056a7f3fdfcecb"
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
 "bool LatchExecutionAmbiguity(",
 "int FindExecutionAmbiguityTicket(",
 "bool ReconcileExecutionAmbiguityHold(",
 "void NMJE_PrintClosedOutcomeShadow(",
 "void CompactMonitoredTrades(",
 "void ProcessEntry(",
 "bool RunEntryPreflightAndExecute(",
 "void ManagePositions(",
 "void RebuildExecutionHistory(",
 "void RecoverExistingOrders(",
 "void UpdateNestedJourneyObservation(",
 "void NMJE_PrintValidatedDecisionShadow(",
]
for sig in protected:
    assert body(base,sig)==body(cand,sig), "protected body changed: "+sig

adopt_base=body(base,"bool AdoptAmbiguousExecutionTicket(")
adopt_cand=body(cand,"bool AdoptAmbiguousExecutionTicket(")
expected=adopt_base.replace(
    '   info.decision_id = "";',
    '   // N2/#233: preserve exact same-session identity when F07 still owns it.\n'
    '   // Restart recovery leaves DecisionID empty; no identity is reconstructed.\n'
    '   info.decision_id = g_execution_ambiguity.DecisionID;'
)
assert adopt_cand==expected, "AdoptAmbiguousExecutionTicket changed beyond intended DecisionID carry"

load_base=body(base,"bool LoadExecutionAmbiguityHold(")
load_cand=body(cand,"bool LoadExecutionAmbiguityHold(")
assert load_cand==load_base, "LoadExecutionAmbiguityHold must remain exact Build 5.08 restart behavior"

assert base.count("OrderSend(")==cand.count("OrderSend(")==1
assert '#property version   "5.09"' in cand
assert "V509_N2_F07_OPEN_DECISIONID_20260922" in cand
assert "N2_F07_OPEN_DECISIONID_233_20260922" in cand
assert '[F7-BUILD] EA=BBMA_EA Build=5.09 BuildTag=' in cand
for forbidden in ("NMJE_PassExecutionGate","REJ_NMJE_RELATION","N3_POLICY_ACTIVE","PERIOD_M5"):
    assert forbidden not in cand
print("N2_509_PROTECTED_BODIES=PASS count="+str(len(protected)))
