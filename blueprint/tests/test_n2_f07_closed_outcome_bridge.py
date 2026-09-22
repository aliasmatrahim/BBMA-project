#!/usr/bin/env python3
"""N2 closed-outcome bridge guard for F07 closed-before-reconcile orders."""
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
    reconcile = body("bool ReconcileExecutionAmbiguityHold(")
    compact = body("void CompactMonitoredTrades(")

    # Normal monitored close path remains the canonical outcome logger.
    assert "NMJE_PrintClosedOutcomeShadow(g_monitored_trades[i]);" in compact

    # F07 closed-before-reconcile must preserve exact available identity
    # before the persistent HOLD object is cleared.
    assert "string decisionID = g_execution_ambiguity.DecisionID;" in reconcile
    assert "int magicNumber = g_execution_ambiguity.MagicNumber;" in reconcile
    assert "if(!isOpen)" in reconcile
    assert "OrderSelect(" not in reconcile
    assert "REC_AMBIGUOUS_EXECUTION_FROZEN" in reconcile
    assert "NMJE_PrintClosedOutcomeShadow(" in reconcile

    clear_pos = reconcile.index("if(!ClearExecutionAmbiguityHold())")
    outcome_pos = reconcile.index("NMJE_PrintClosedOutcomeShadow(")
    assert clear_pos < outcome_pos

    # Telemetry bridge must never fabricate a monitored row or broker action.
    assert "AddToMonitoredTrades(" not in reconcile
    for broker_write in ("OrderSend(", "OrderClose(", "OrderModify(", "OrderDelete("):
        assert broker_write not in reconcile

    print("N2_F07_CLOSED_OUTCOME_BRIDGE=PASS")

if __name__ == "__main__":
    main()
