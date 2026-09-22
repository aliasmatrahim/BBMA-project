# F07 Execution Ambiguity Hold Decision — 2026-09-22

Status: **LOCKED / ENGINEERING EXECUTION-SAFETY POLICY**
Issue: **#224** (downstream Issue #101 F07)
Baseline: `d1-owner-dev@e9f239583a130e5168f75413d2610ec4f6a98674` / Build 5.04

## Classification
This is an **engineering execution-safety mapping**, not a BBMA Strategy-Core rule.
It does not create, reject, rank or reinterpret BBMA candidates and does not change M15 direction ownership, M17 geometry, M21 sizing, M19 risk thresholds, M20 portfolio limits or TradeLock semantics.

## Trigger
M22 has an ambiguous outcome when the broker may have accepted an order but no exact matching ticket can yet be confirmed. The existing contract already forbids resend after that outcome.

A second ambiguity path exists when M22 returns a positive ticket but the immediate `OrderSelect(ticket)` required for confirmed materialization fails. In both cases actual exposure is unknown.

## Locked policy
1. An unresolved execution ambiguity creates one **EA-wide new-entry HOLD**.
2. The HOLD is persistent across restart using terminal GlobalVariables under the instance-scoped `BBXA|S<StrategyID>|I<InstanceID>|` namespace.
3. The active marker is persisted first. Partial persistence therefore reloads fail-closed as an active unresolved HOLD.
4. Existing `M20 ManagePortfolio() -> M23 ManagePositions()` protection/lifecycle runs before ambiguity reconciliation on every operational tick.
5. Any tick that begins with an active HOLD is reconciliation-only after protection/lifecycle: even if exact reconciliation succeeds and clears the HOLD, no new strategy scan/preflight/order may proceed until the next operational tick has first processed the newly materialized broker state through M20/M23.
6. While the HOLD remains active, no new strategy scan/preflight/order may proceed, including later pairs in the same scan cycle.
7. M22 never automatically resends the ambiguous request.
8. There is no timeout, elapsed-bar release, risk reservation formula or assumption that a missing ticket means no fill.
9. Reconciliation is identity-only: exact pair + exact EA magic + direction/order type + `BBMA|H:<SHORT_HASH(DecisionID)>`.
10. A matching live order is admitted to the monitored registry from broker truth and is classified `REC_AMBIGUOUS_EXECUTION_FROZEN`. No full DecisionID, signal type, sequence or lifecycle owner is fabricated. Existing broker SL/TP/lot remain authoritative. M20 emergency handling stays available; ordinary strategy lifecycle is frozen.
11. A matching closed historical order is tombstoned for idempotency and needs no monitored live row.
12. The HOLD may clear only after the matching broker order/history is found and durable execution identity/tombstone state is established. Persistence/registry failure keeps the HOLD active.
13. If no matching broker evidence ever appears, the HOLD does **not** auto-clear. Resumption requires explicit operator reconciliation/intervention outside the automatic execution path.
14. Restart recovery may discover the broker order first; the F07 HOLD is still loaded afterwards and is cleared only by the same exact identity reconciliation.
15. TradeLock F03, shared-helper F05, later re-presentation F08 research beyond the exact HOLD path, and registry mismatch F10 remain separate scopes.

## Ownership
- **M22**: ambiguous-result detection and HOLD latching.
- **M27**: protection-first orchestration and new-entry admission freeze while HOLD is active.
- **F07 reconciliation helper**: exact identity discovery and safety-frozen materialization only.
- **M24**: restart reconstruction remains restart-owned and may not fabricate strategy identity or clear an unresolved F07 HOLD by assumption.
- **M23**: emergency action retains precedence; `REC_AMBIGUOUS_EXECUTION_FROZEN` blocks ordinary lifecycle action.

## Failure policy
Any incomplete F07 persistence, order-selection uncertainty during reconciliation, registry-capacity failure, execution-identity persistence failure or HOLD-cleanup failure is fail-closed: the HOLD remains active.

## Validation requirements
- deterministic policy model;
- static authority/source guard;
- protected-body comparison against Build 5.04;
- native MetaEditor 0E0W;
- exact tester-adapter invariant + 0E0W;
- normal-path isolated smoke exact-equal to Build 5.04;
- targeted active-HOLD test showing strategy scans/orders are suppressed while protection orchestration remains ahead of the HOLD gate;
- exact tester GlobalVariables restoration;
- no primary MT4 restart or broker live/demo activation.
