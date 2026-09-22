#!/usr/bin/env python3
"""F07 persistent execution-ambiguity hold source guards."""
from pathlib import Path

SRC = Path("blueprint/source/BBMA_EA.mq4").read_text(encoding="utf-8")

def body(signature: str) -> str:
    start = SRC.index(signature)
    brace = SRC.index("{", start)
    depth = 0
    for i in range(brace, len(SRC)):
        depth += (SRC[i] == "{") - (SRC[i] == "}")
        if depth == 0:
            return SRC[start:i + 1]
    raise AssertionError(signature)

def main():
    for marker in (
        "struct PendingExecutionAmbiguity",
        "PendingExecutionAmbiguity g_execution_ambiguity",
        "string ExecutionAmbiguityGVBase(",
        "bool SaveExecutionAmbiguityHold(",
        "bool LoadExecutionAmbiguityHold(",
        "bool LatchExecutionAmbiguity(",
        "bool ReconcileExecutionAmbiguityHold(",
        "bool ClearExecutionAmbiguityHold(",
    ):
        assert marker in SRC, marker

    latch = body("bool LatchExecutionAmbiguity(")
    find_ticket = body("int FindExecutionAmbiguityTicket(")
    adopt = body("bool AdoptAmbiguousExecutionTicket(")
    reconcile = body("bool ReconcileExecutionAmbiguityHold(")
    process = body("void ProcessEntry(")
    preflight = body("bool RunEntryPreflightAndExecute(")
    manage = body("void ManagePositions(")
    init = body("int InitializeEA(")
    ontick = body("void OnTickMain(")

    assert "GlobalVariablesFlush()" in SRC
    assert "SHORT_HASH(decision.DecisionID)" in latch
    assert "OrderSend(" not in reconcile
    assert "OrderSend(" not in find_ticket
    assert "FindExistingExecutionTicket(" in find_ticket
    assert "AddToMonitoredTrades(" in adopt
    assert "UpsertExecutionHashTombstone(" in adopt
    assert "REC_AMBIGUOUS_EXECUTION_FROZEN" in adopt
    assert "REC_AMBIGUOUS_EXECUTION_FROZEN" in manage
    assert "LoadExecutionAmbiguityHold()" in init
    assert "g_execution_ambiguity.Active" in preflight

    # Both ambiguity exits must latch before returning rejection.
    assert process.count("LatchExecutionAmbiguity(") >= 2
    assert "REJ_AMBIGUOUS_RESULT" in process

    # Protection/lifecycle runs first; ambiguity reconciliation blocks only new scans.
    m20 = ontick.index("ManagePortfolio();")
    m23 = ontick.index("ManagePositions();")
    recon = ontick.index("ReconcileExecutionAmbiguityHold()")
    scan = ontick.index("g_is_scanning = true;")
    assert m20 < m23 < recon < scan
    assert "bool hadExecutionAmbiguityHold = g_execution_ambiguity.Active;" in ontick
    assert "if(hadExecutionAmbiguityHold)" in ontick
    assert "ReconcileExecutionAmbiguityHold();\n      return;" in ontick

    # A reconciliation-success tick still cannot admit new exposure. The
    # materialized broker order must pass protection/lifecycle on the next tick.
    assert ontick.index("if(hadExecutionAmbiguityHold)") < ontick.index("g_is_scanning = true;")

    # No automatic time-based release or resend.
    assert "TimeCurrent()" not in reconcile
    assert "Sleep(" not in reconcile
    assert "OrderSend(" not in reconcile

    print("F07_EXECUTION_AMBIGUITY_HOLD_STATIC=PASS")

if __name__ == "__main__":
    main()
