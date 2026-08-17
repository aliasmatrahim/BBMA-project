# P2 Step 17 — Full Signal-to-Trade Lifecycle Re-Audit

Status: PASS
Compile verification: 0 Errors / 0 Warnings (user-reported MetaEditor result)

## Re-Audit Scope
End-to-end cross-module path from broker-resolved symbol scheduling through closed-candle data, BBMA detection/state ownership, candidate construction, Entry Mode gating, priority/invalidation, SL/TP validation, risk/lot/portfolio gates and immutable execution.

## Result
Step 17 Fix A closes the identified symbol-clock defect. `OnTickMain()` now calls `IsNewCandle(g_pair_states[i].actual_symbol, i)`, matching the broker-resolved symbol already used by `ProcessPair()`, market-data reads, BBMA detectors, SL/TP resolution, risk validation and execution.

The lifecycle therefore uses one symbol identity from scheduling through execution, including broker suffix/prefix variants accepted by the Step 14 resolver.

Entry Mode behavior remains unchanged:
- EntryMode 1: standalone confirmed H1 Re-Entry only.
- EntryMode 2: standalone H1 Re-Entry plus validated REM/RRE/REE combinations.

M15 remains the final direction authority, M16 revalidates owner snapshots/expiry, M17 owns structural SL/TP validation, M21 sizes only, M19/M20 apply live risk/portfolio gates and M22 executes without reinterpreting the approved strategy payload.

No residual Step 17 defect was found in this static cross-module scope.

Final: P2 Step 17 PASS (static re-audit + compile 0E/0W).