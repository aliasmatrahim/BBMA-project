# P2 Step 16 — Risk Sizing / SL / Lot / Total Portfolio Exposure Audit

Status: FAIL — Fix A required

## Finding
`CalculateTotalRisk()` is fail-open on broker-selection uncertainty. For each monitored trade it does:

```mql4
if(!OrderSelect(g_monitored_trades[i].ticket, SELECT_BY_TICKET))
   continue;
```

That means a transient `OrderSelect()` failure silently removes that possibly-live position from total EA risk. The prospective new order can then be admitted using an understated portfolio-risk value.

This conflicts with the fail-closed protection model already used elsewhere in the project (for example emergency-release broker enumeration). For a hard `MaxTotalRiskPercent` gate, unknown existing risk must never be treated as zero.

## Scope
Cross-module path audited:
M17 normalized structural SL -> M21 lot sizing -> M19 `CalculateTotalRisk()` / `CheckRiskBeforeTrade()` -> M20 prospective guard -> M22 execution.

The new-trade sizing path itself remains coherent: M21 sizes from the frozen Entry/SL/equity/tick specification and rounds lot downward to broker lot step. The defect is specifically existing-portfolio enumeration uncertainty inside M19.

## Required Fix A
Make `CalculateTotalRisk()` fail-closed:
- if any monitored ticket cannot be selected, set `valid=false` and reject prospective entry;
- only ignore a ticket when the broker definitively reports it closed;
- derive current existing risk from broker-selected live order state where possible, while retaining exact EA ownership checks;
- do not alter BBMA signal logic, structural SL/TP, or lot-sizing formula.
