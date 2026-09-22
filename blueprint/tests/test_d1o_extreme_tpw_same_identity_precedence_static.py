#!/usr/bin/env python3
from pathlib import Path

SRC = Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")


def body(signature):
    start = SRC.index(signature)
    brace = SRC.index("{", start)
    depth = 0
    for i in range(brace, len(SRC)):
        if SRC[i] == "{":
            depth += 1
        elif SRC[i] == "}":
            depth -= 1
            if depth == 0:
                return SRC[start:i + 1]
    raise AssertionError(signature)


def main():
    # Accept the verified owner and its scoped M19-only successor.
    identities = (
        ("Version 5.0.3 - D1O EXTREME_TPW Identity Enrichment",
         '#property version   "5.03"',
         "V503_D1O_EXTREME_TPW_IDENTITY_ENRICHMENT_20260921",
         "D1O_EXTREME_TPW_IDENTITY_ENRICHMENT_214_20260921"),
        ("Version 5.0.4 - M19 Selection Failure Fail-Closed",
         '#property version   "5.04"',
         "V504_M19_SELECTION_FAIL_CLOSED_20260921",
         "M19_SELECTION_FAIL_CLOSED_101_20260921"),
        ("Version 5.0.5 - Persistent Execution Ambiguity Hold",
         '#property version   "5.05"',
         "V505_F07_EXECUTION_AMBIGUITY_HOLD_20260922",
         "F07_EXECUTION_AMBIGUITY_HOLD_224_20260922"),
        ("Version 5.0.6 - Selection Uncertainty Fail-Closed",
         '#property version   "5.06"',
         "V506_F05_SELECTION_UNCERTAINTY_FAIL_CLOSED_20260922",
         "F05_SELECTION_UNCERTAINTY_FAIL_CLOSED_226_20260922"),
    )
    assert any(all(marker in SRC for marker in markers) for markers in identities)

    helper = body("bool IsExactExtremeTPWIdentityEnrichmentPair(")
    for marker in (
        "SIGNAL_RE_ENTRY",
        "D1_OPP_EXTREME_TPW",
        "SequenceHash",
        "GetCandidateAnchorTime",
        "SequenceStartTime",
        "PERIOD_H1",
        "ComponentCount",
    ):
        assert marker in helper, marker

    compare = body("int CompareCanonicalCandidates(")
    assert "IsExactExtremeTPWIdentityEnrichmentPair(a, b)" in compare
    assert "a.UsesD1Opportunity" in compare
    assert "b.UsesD1Opportunity" in compare
    assert "D1_OPP_EXTREME_TPW" in compare

    # Scope must not become a generic D1 Opportunity priority rule.
    assert "if(a.UsesD1Opportunity && !b.UsesD1Opportunity) return 1;" not in compare
    assert "if(b.UsesD1Opportunity && !a.UsesD1Opportunity) return -1;" not in compare

    assert SRC.count("OrderSend(") == 1
    print("D1O_EXTREME_TPW_PRECEDENCE_STATIC=PASS")


if __name__ == "__main__":
    main()
