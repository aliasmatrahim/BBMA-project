# P2 Step 16 — Risk Sizing / SL / Lot / Portfolio Exposure Re-Audit

Status: PASS
Compile verification: 0 Errors / 0 Warnings (user-reported MetaEditor result)

## Re-Audit Scope
End-to-end cross-module chain: M17 structural SL/TP -> M21 lot sizing -> M19 prospective total-risk -> M20 portfolio guard/protection -> M22 immutable execution.

## Result
Step 16 Fix A closes the identified exposure-undercount defect. `CalculateTotalRisk()` now treats a monitored ticket that cannot be selected from broker state as unknown risk: it sets `valid=false` and aborts prospective total-risk calculation. Only a ticket that is definitively selected and closed is ignored.

Downstream `CheckRiskBeforeTrade()` already rejects `riskValid == false` with `REJ_TOTAL_RISK`, so unknown monitored exposure cannot be admitted as zero exposure.

M21 remains sizing-only and uses the frozen execution/risk snapshot; M20 remains a portfolio/protection gate; M22 remains execution-only and does not resize or re-risk the decision.

No residual Step 16 defect was found in this scope. BBMA signal semantics, structural SL/TP ownership, and lot-risk formula remain unchanged.

Final: P2 Step 16 PASS (static cross-module re-audit + compile 0E/0W).