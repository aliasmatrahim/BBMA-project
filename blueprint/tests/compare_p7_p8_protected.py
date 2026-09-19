from pathlib import Path
import hashlib
p7=Path(r"D:\BBMA\Workspace\q9-nmje-v2-p7-structural-density-101\blueprint\source\BBMA_EA.mq4").read_text(encoding="utf-8")
p8=Path(r"D:\BBMA\Workspace\q9-nmje-v2-p8-provenance-stability-101\blueprint\source\BBMA_EA.mq4").read_text(encoding="utf-8")
def body(s,sig):
    st=s.index(sig); b=s.index("{",st); d=0
    for i in range(b,len(s)):
        if s[i]=="{": d+=1
        elif s[i]=="}":
            d-=1
            if d==0:return s[b:i+1]
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
"RiskStatus CheckRiskBeforeTrade(",
"bool RunEntryPreflightAndExecute(",
"bool IsSignalAllowed(",
"int SendOrderWithRetry(",
]
for sig in sigs:
    a=body(p7,sig).replace("\r\n","\n")
    b=body(p8,sig).replace("\r\n","\n")
    assert a==b,sig
    print("PASS",sig,hashlib.sha256(a.encode()).hexdigest()[:16])
print("Q9_P8_PROTECTED_AUTHORITY_BODY_COMPARE=PASS")
