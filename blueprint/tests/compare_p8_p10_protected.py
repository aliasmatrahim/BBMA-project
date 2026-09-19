from pathlib import Path
import hashlib

p8=Path(r"D:\BBMA\Workspace\q9-nmje-v2-p8-provenance-stability-101\blueprint\source\BBMA_EA.mq4").read_text(encoding="utf-8")
p10=Path(r"D:\BBMA\Workspace\q9-nmje-v2-p10-entry-displacement-101\blueprint\source\BBMA_EA.mq4").read_text(encoding="utf-8")

def body(src,sig):
    start=src.index(sig)
    brace=src.index("{",start)
    depth=0
    for i in range(brace,len(src)):
        if src[i]=="{": depth+=1
        elif src[i]=="}":
            depth-=1
            if depth==0: return src[brace:i+1]
    raise RuntimeError(sig)

sigs=[
"void BuildPossibleCombinations(",
"void ValidateSequence(",
"void BuildConfirmedReEntryCandidate(",
"void BuildStandaloneExtremeCandidate(",
"void BuildD1OpportunityCandidate(",
"int CompareCanonicalCandidates(",
"void PriorityEngine_Atomic(",
"void InvalidationEngine_Atomic(",
"bool ResolveExecutionReferencePrice(",
"bool ResolveApprovedInitialSLTP(",
"RiskStatus CheckRiskBeforeTrade(",
"bool RunEntryPreflightAndExecute(",
"bool IsSignalAllowed(",
"int SendOrderWithRetry(",
]
for sig in sigs:
    a=body(p8,sig).replace("\r\n","\n")
    b=body(p10,sig).replace("\r\n","\n")
    assert a==b,sig
    print("PROTECTED_BODY_PASS",sig.strip(),hashlib.sha256(a.encode()).hexdigest()[:16])
print("Q9_P10_PROTECTED_AUTHORITY_BODY_COMPARE=PASS")
