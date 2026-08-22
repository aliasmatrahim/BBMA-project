# P3 — Sequential Cumulative Risk-Budget Admission Audit

Date: 2026-08-22
Branch: `blueprint-dev`
Status: **STATIC PASS — NO CODE FIX REQUIRED; METAEDITOR/RUNTIME MULTI-DECISION TRACE PENDING**

## Question
When several valid decisions are processed close together, does each newly executed trade consume the portfolio risk budget before the next decision is admitted?

## Static result
**PASS.** The current execution architecture is sequential and prospective:

1. `OnTickMain()` serializes strategy scanning with `g_is_scanning` and iterates pairs one at a time.
2. Each validated decision obtains its final lot before `CheckRiskBeforeTrade()`.
3. `CalculateTotalRisk()` sums risk from the existing monitored live EA portfolio and then adds the proposed trade risk (`newRisk`).
4. The prospective total is compared against `MaxTotalRiskPercent` using current equity.
5. Only an allowed decision reaches `ProcessEntry()`.
6. After a broker-confirmed execution, M22 immediately calls `AddToMonitoredTrades(info)` before marking the decision execution complete.
7. Therefore the next pair processed in the same serialized scan sees the newly executed position in `g_monitored_count`, so its prospective risk calculation includes that consumed budget.

## Failure behavior
If existing live-trade risk cannot be resolved safely, the risk calculation fails closed rather than silently treating unknown risk as zero. A rejected/failed order is not added as executed portfolio risk. Ambiguous execution remains governed by M22/M24 idempotency/recovery rules.

## No fix required
No static race or stale-budget defect was found in the current single-threaded scan/admission path. Adding a separate reservation ledger would duplicate the already-sequential execution model and is not justified by current evidence.

## Remaining runtime verification
Run a controlled case where two or more pairs generate valid decisions in one scan window and capture:
- equity and `MaxTotalRiskPercent`;
- existing risk before decision A;
- A proposed/final risk and execution result;
- existing risk observed by decision B after A executes;
- B prospective total and admit/reject result.

Expected: if A consumes enough budget, B must reject with `REJ_TOTAL_RISK`; if A fails/does not execute, B must not reserve phantom risk.
