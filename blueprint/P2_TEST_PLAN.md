# P2 Functional / Strategy Tester Verification Plan

## Gate
P1 Release Candidate is locked at canonical SHA-256:
`30363d08437b85f253e6baf3e9c82af0d59d70727639ac0e6420a7677f975bc9`

P2 MUST NOT silently modify BBMA strategy semantics. Any defect discovered is recorded first, repaired on `blueprint-dev`, recompiled to 0 errors / 0 warnings, and re-audited before continuing.

## P2 Step 1 — Runtime Smoke / Initialization
Goal: prove the P1 RC can initialize and execute its basic tick lifecycle in MT4 Strategy Tester without runtime/init faults.

Checks:
1. `OnInit()` returns successfully with valid default/test inputs.
2. Pair configuration and magic ownership initialize correctly.
3. Required D1/H4/H1/M15 market data can be loaded.
4. No array-out-of-range, zero-divide, invalid pointer/object, or repeated runtime errors appear in Journal/Experts.
5. M24 recovery does not fabricate ownership/state when tester begins with no owned positions.
6. M20/M23 lifecycle executes before strategy scan as locked.
7. EA remains running through multiple closed M15 candles.
8. No trade-result claim is required in Step 1; this is a runtime smoke gate, not profitability testing.

Evidence required from manual MT4 Strategy Tester:
- Tester configuration screenshot/report (symbol, timeframe, model, date range, inputs).
- Journal/Experts output covering initialization and several M15 closes.
- Any runtime error code/message if present.

Pass condition:
- Initialization succeeds and no structural/runtime fault prevents normal continued operation.

## Planned subsequent gates
- P2 Step 2: signal/detector observability and closed-candle timing.
- P2 Step 3: Entry Mode 1 eligibility (H1 Re-Entry only).
- P2 Step 4: Entry Mode 2 eligibility (H1 Re-Entry + validated REM/RRE/REE).
- P2 Step 5: M17 SL/TP provenance/direction/runtime validation.
- P2 Step 6: M21 sizing + M19/M20 prospective risk gates.
- P2 Step 7: M22 execution/idempotency and duplicate prevention.
- P2 Step 8: M23 lifecycle / broker-side SL/TP preservation.
- P2 Step 9: M24 restart/recovery behavior.
- P2 Step 10: emergency protection / liquidation ownership.
- P2 Step 11: deterministic regression matrix across representative pairs/periods.
- P2 Finalization: evidence review and release decision.

## Current status
P2 Step 1: READY FOR MANUAL MT4 STRATEGY TESTER RUN.
