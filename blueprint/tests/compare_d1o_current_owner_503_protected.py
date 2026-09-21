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
        "string GenerateDecisionID(",
        "bool IsDecisionExecuted(",
        "void BuildConfirmedReEntryCandidate(",
        "void BuildD1OpportunityCandidate(",
        "datetime GetCandidateAnchorTime(",
        "bool ResolveSelectedSLTPSourceComponent(",
        "bool IsD1OpportunityCandidateAuthorityReady(",
        "bool FreezeD1OpportunitySnapshot(",
        "void PriorityEngine_Atomic(",
        "bool ValidateDecisionD1OpportunitySnapshot(",
        "void BuildRiskValidationSnapshot(",
        "bool ValidateFrozenBrokerDistanceGeometry(",
        "bool ValidateSLTP(",
        "double CalculateBasketLossPercent_EA(",
        "double CalculateTotalRisk(",
        "bool IsD1TPWLifecycleIdentity(",
        "bool DeleteTerminalGlobalExact(",
        "bool SetTerminalGlobalExact(",
        "bool D1TPWGenerationPayloadExists(",
        "bool D1TPWCheckpointExists(",
        "void ClearD1TPWCheckpoint(",
        "bool SaveD1TPWCheckpoint(",
        "bool LoadD1TPWCheckpoint(",
        "bool IsF7LifecycleIdentity(",
        "bool C044DeleteGVExact(",
        "bool C044SetGVExact(",
        "bool LoadC044Checkpoint(",
        "bool ResolveApprovedInitialSLTP(",
        "RiskStatus CheckRiskBeforeTrade(",
        "int FindExistingExecutionTicket(",
        "int SendOrderWithRetry(",
        "void RecoverExistingOrders(",
    )

    for signature in signatures:
        a = fn(OLD, signature)
        b = fn(NEW, signature)
        assert a == b, f"protected body changed: {signature}"
        print(signature.split("(")[0].strip(),
              hashlib.sha256(a.encode()).hexdigest()[:16])

    assert fn(OLD, "int CompareCanonicalCandidates(") != fn(
        NEW, "int CompareCanonicalCandidates("
    )
    assert "IsExactExtremeTPWIdentityEnrichmentPair" not in OLD
    assert "IsExactExtremeTPWIdentityEnrichmentPair" in NEW
    print("D1O_CURRENT_OWNER_503_PROTECTED=PASS")


if __name__ == "__main__":
    main()
