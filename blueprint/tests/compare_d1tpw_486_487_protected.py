#!/usr/bin/env python3
from pathlib import Path
import hashlib
import sys

BASE = Path(sys.argv[1])
CUR = Path(sys.argv[2])


def function(src, signature):
    start = src.index(signature)
    brace = src.index("{", start)
    depth = 0
    for i in range(brace, len(src)):
        if src[i] == "{":
            depth += 1
        elif src[i] == "}":
            depth -= 1
            if depth == 0:
                return src[start:i + 1]
    raise AssertionError(signature)


def main():
    old = BASE.read_text(encoding="utf-8")
    new = CUR.read_text(encoding="utf-8")
    signatures = (
        "bool IsD1TPWCompletionAtShift(",
        "bool D1OpportunityTPWCompletedSince(",
        "void UpdateD1OpportunityJourney(",
        "void BuildD1OpportunityCandidate(",
        "bool IsD1TPWLifecycleIdentity(",
        "bool ResolveApprovedInitialSLTP(",
        "bool ValidateDecisionD1OpportunitySnapshot(",
        "void InvalidationEngine_Atomic(",
        "bool ProcessD1TPWClosedCandle(",
        "bool AdvanceD1TPWLifecycleForTrade(",
        "void AdvanceD1TPWLifecycleForPair(",
        "bool ExecuteLatchedD1TPWClose(",
        "void ManagePositions(",
        "bool InitializeD1TPWTradeStateFromDecision(",
        "bool C044CheckpointExists(",
        "bool SaveC044ReplaySeed(",
        "bool LoadC044ReplaySeed(",
        "bool SaveC044Checkpoint(",
        "bool LoadC044Checkpoint(",
        "RiskStatus CheckRiskBeforeTrade(",
        "bool RunEntryPreflightAndExecute(",
        "int SendOrderWithRetry(",
    )
    for sig in signatures:
        a = function(old, sig)
        b = function(new, sig)
        assert a == b, f"protected body changed: {sig}"
        digest = hashlib.sha256(a.encode()).hexdigest()[:16]
        print(sig.split("(")[0].strip(), digest)
    print("D1TPW_486_487_PROTECTED=PASS")


if __name__ == "__main__":
    main()
