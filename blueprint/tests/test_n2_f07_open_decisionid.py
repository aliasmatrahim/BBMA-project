#!/usr/bin/env python3
from pathlib import Path

SRC = Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")

def body(signature: str) -> str:
    start = SRC.index(signature)
    brace = SRC.index("{", start)
    depth = 0
    for i in range(brace, len(SRC)):
        if SRC[i] == "{":
            depth += 1
        elif SRC[i] == "}":
            depth -= 1
            if depth == 0:
                return SRC[brace + 1:i]
    raise AssertionError(f"unterminated function: {signature}")

def main() -> None:
    adopt = body("bool AdoptAmbiguousExecutionTicket(")
    assert "info.decision_id = g_execution_ambiguity.DecisionID;" in adopt, (
        "same-session F07 open adoption must preserve exact available DecisionID"
    )
    assert 'info.decision_id = "";' not in adopt, (
        "open adoption must not discard an exact same-session DecisionID"
    )

    load = body("bool LoadExecutionAmbiguityHold(")
    assert "ZeroMemory(g_execution_ambiguity);" in load
    assert "DecisionID =" not in load, (
        "restart recovery must not reconstruct or load a full DecisionID"
    )
    assert "TEST_ONLY" not in load

    reconcile = body("bool ReconcileExecutionAmbiguityHold(")
    assert "string decisionID = g_execution_ambiguity.DecisionID;" in reconcile
    assert "outcomeInfo.decision_id = decisionID;" in reconcile

    print("N2_F07_OPEN_DECISIONID=PASS")

if __name__ == "__main__":
    main()
