#!/usr/bin/env python3
from pathlib import Path
import hashlib
import sys

BASE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("../q9-nmje-v2-p10-entry-displacement-101/blueprint/source/BBMA_EA.mq4")
CUR = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("blueprint/source/BBMA_EA.mq4")

def function_body(src: str, signature: str) -> str:
    start = src.index(signature)
    brace = src.index("{", start)
    depth = 0
    for i in range(brace, len(src)):
        if src[i] == "{":
            depth += 1
        elif src[i] == "}":
            depth -= 1
            if depth == 0:
                return src[brace:i + 1]
    raise AssertionError(signature)

def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def main() -> None:
    old = BASE.read_text(encoding="utf-8")
    new = CUR.read_text(encoding="utf-8")
    signatures = (
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
    )
    for sig in signatures:
        a = function_body(old, sig)
        b = function_body(new, sig)
        assert a == b, f"protected body changed: {sig}"
        print(sig.split("(")[0].strip(), digest(a)[:16])
    print("Q9_P10_P11_PROTECTED=PASS")

if __name__ == "__main__":
    main()
