# NMJE N3 Step 5 — Recovery / Replay Equivalence Gate

Date: 2026-08-27
Branch: `nmje-n3-hardening-dev`
Status: STATIC GATE ACTIVE / EXECUTION INACTIVE

## Scope
Prove that future NMJE recovery can reproduce lineage only from the same source-owned closed-candle provenance used during uninterrupted processing. This stage does not modify M24 trading/lifecycle behavior and does not activate an execution gate.

## Existing recovery model reused
The EA already demonstrates the required engineering pattern in recovery-sensitive paths:
- exact closed-bar lookup with `iBarShift(..., true)`;
- replay oldest -> newest through missed closed candles;
- persisted source-owned replay seeds where required;
- explicit cursor/order checks;
- freeze/unresolved state when identity/history is missing or inconsistent;
- no guessing across missing history.

NMJE recovery must follow that same pattern rather than infer a parent/journey from current price.

## Identity equivalence requirements
For identical closed-candle/source-owner history before and after restart:
1. Re-Entry event identity remains derived from structural `StartCandleTime` + type/direction/TF.
2. Extreme event identity remains derived from `RawCandleTime` + direction/TF.
3. MHV/MLV identity remains tied to canonical parent Extreme provenance.
4. D1/H4 owner identity remains source-candle-owned.
5. `JourneyID`, `ParentEventID`, relation and update candle must reproduce identically for the same processing epoch.
6. If any required owner provenance cannot be reconstructed exactly, new-entry NMJE lineage is `UNRESOLVED`; no replacement identity may be manufactured.

## Current proof layer
`blueprint/tests/test_nmje_n3_recovery_failclosed_static.py` verifies that the staging source retains exact-history/fail-closed recovery primitives and that no NMJE execution-authority marker is present.

## Explicit non-goals
- no trade rejection based on NMJE relation;
- no automatic live-trade close;
- no new M24 trading semantics;
- no scoring, voting, confidence or universal nesting requirement;
- no inferred lineage from current tick/time.

## Boundary after this gate
Static recovery architecture can be hardened further without activation. Actual broker-connected restart/replay equivalence evidence and any future execution policy remain separate runtime/approval gates.
