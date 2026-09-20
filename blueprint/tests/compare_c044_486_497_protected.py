#!/usr/bin/env python3
from pathlib import Path
import hashlib
import sys

OLD = Path(sys.argv[1]).read_text(encoding="utf-8")
NEW = Path(sys.argv[2]).read_text(encoding="utf-8")


def fn(src, signature):
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
    signatures = (
        "bool IsF7LifecycleIdentity(",
        "bool ResolveApprovedInitialSLTP(",
        "bool ProcessC044OwnerClosedCandle(",
        "bool AdvanceC044OwnerEventOneCandle(",
        "void AdvanceC044OwnerEventsForPair(",
        "bool LatchC044Exit(",
        "bool ExecuteLatchedC044Close(",
        "bool InitializeC044TradeStateFromDecision(",
        "bool SaveC044ReplaySeed(",
        "bool SaveC044Checkpoint(",
        "void RecoverExistingOrders(",
        "void PriorityEngine_Atomic(",
        "void InvalidationEngine_Atomic(",
        "RiskStatus CheckRiskBeforeTrade(",
        "bool RunEntryPreflightAndExecute(",
        "int SendOrderWithRetry(",
    )
    for signature in signatures:
        a = fn(OLD, signature)
        b = fn(NEW, signature)
        assert a == b, f"protected body changed: {signature}"
        print(signature.split("(")[0].strip(),
              hashlib.sha256(a.encode()).hexdigest()[:16])

    assert fn(OLD, "bool LoadC044Checkpoint(") != fn(
        NEW, "bool LoadC044Checkpoint("
    )
    print("C044_486_497_PROTECTED=PASS")


if __name__ == "__main__":
    main()
