#!/usr/bin/env python3
"""F07 scope guard: protected owner bodies must remain exact Build 5.04."""
from pathlib import Path
import subprocess

BASE="e9f239583a130e5168f75413d2610ec4f6a98674"
base=subprocess.check_output(
    ["git","show",BASE+":blueprint/source/BBMA_EA.mq4"]
).decode("utf-8").replace("\r\n","\n")
cand=Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8").replace("\r\n","\n")

def body(src, signature):
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
 "double CalculateLotSize(",
 "double CalculateBasketLossPercent_EA(",
 "double CalculateTotalRisk(",
 "RiskStatus CheckRiskBeforeTrade(",
 "void FinalPortfolioGuard(",
 "void ManagePortfolio(",
 "bool IsSignalAllowed(",
 "int SendOrderWithRetry(",
 "int FindExistingExecutionTicket(",
 "void RebuildExecutionHistory(",
 "void RecoverExistingOrders(",
]
for sig in protected:
    assert body(base,sig)==body(cand,sig), "protected body changed: "+sig

assert base.count("OrderSend(")==1
assert cand.count("OrderSend(")==1
assert '#property version   "5.05"' in cand
assert "V505_F07_EXECUTION_AMBIGUITY_HOLD_20260922" in cand
assert "F07_EXECUTION_AMBIGUITY_HOLD_224_20260922" in cand
print("F07_505_PROTECTED_BODIES=PASS count="+str(len(protected)))
