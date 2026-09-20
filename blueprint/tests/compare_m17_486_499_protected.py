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
    protected = (
        "bool ResolveApprovedInitialSLTP(",
        "bool ValidateDirectionalSLTPGeometry(",
        "bool ResolveSourceOwnedStructuralAnchor(",
        "bool ResolveStandaloneExtremeStructuralAnchor(",
        "bool ResolveStandaloneExtremeTPWajib(",
        "bool IsD1TPWLifecycleIdentity(",
        "bool IsF7LifecycleIdentity(",
        "void InvalidationEngine_Atomic(",
        "double CalculateLotSize(",
        "RiskStatus CheckRiskBeforeTrade(",
        "int FindExistingExecutionTicket(",
        "int SendOrderWithRetry(",
        "void RecoverExistingOrders(",
    )

    for signature in protected:
        a = fn(OLD, signature)
        b = fn(NEW, signature)
        assert a == b, f"protected body changed: {signature}"
        print(signature.split("(")[0].strip(),
              hashlib.sha256(a.encode()).hexdigest()[:16])

    assert fn(OLD, "bool ValidateSLTP(") != fn(NEW, "bool ValidateSLTP(")
    assert fn(OLD, "void BuildRiskValidationSnapshot(") != fn(
        NEW, "void BuildRiskValidationSnapshot("
    )
    assert "ValidateFrozenBrokerDistanceGeometry" not in OLD
    assert "ValidateFrozenBrokerDistanceGeometry" in NEW
    assert "bool ValidateStopLevel(" in OLD
    assert "bool ValidateStopLevel(" not in NEW
    assert "bool ValidateFreezeLevel(" in OLD
    assert "bool ValidateFreezeLevel(" not in NEW
    print("M17_486_499_PROTECTED=PASS")


if __name__ == "__main__":
    main()
