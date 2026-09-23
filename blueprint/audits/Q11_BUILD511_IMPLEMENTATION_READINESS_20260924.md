# Q11 Build 5.11 Dashboard / Observer Implementation Readiness

Date: 2026-09-24  
Issue: #270  
Status: **PREPARATION READY / IMPLEMENTATION DEFERRED / NO EA SOURCE CHANGE**

## 1. Purpose

This record prepares Q11 against the current exact Build 5.11 owner state.

It does **not** authorize dashboard source materialization, observer replacement, Strategy-Core change, runtime restart, broker action, or production promotion.

Current candidate identity:

- owner baseline: `d1-owner-dev@2302dacc1ff77e01674fc0c85ae6b3ac437ae0fd`
- Build: `5.11`
- Build tag: `V511_EVENT_DRIVEN_OBSERVER_20260922`
- canonical normalized MQ4 SHA-256: `50E4A01A5768B5B5E9A80CABAE21B7260A2912AA058E67E5273386177970D038`

Q10 final acceptance remains incomplete at R5. Q11 therefore remains deferred unless explicitly reprioritized.

## 2. Current owner state already integrated

Q11 is **not greenfield** and must not redo completed downstream work.

Current Build 5.11 already contains:

1. M25 minimal dashboard:
   - Build/time/balance/equity;
   - exact-owned live trade count;
   - protection reference;
   - per-pair final `last_decision` signal, direction, state and rejection reason.
2. Exact-owned live-count helper:
   - `CountDashboardLiveEAOwnedTrades()`;
   - broker `MODE_TRADES` scan;
   - ownership delegated to `IsExactEAOwnedSelectedOrder()`.
3. Event-driven observer:
   - `ObserverShouldEmit()`;
   - `ObserverPrintChanged()`;
   - changed-only diagnostics, presentation/telemetry only.
4. N1/N2 research telemetry and current read-only nested journey state.
5. D1 strategic-owner and D1 Opportunity state already owned outside M25.

The completed Build 5.10/5.11 M25/Observer lineage and later cross-module audit are baseline, not work to recreate.

## 3. Governing authority boundaries

### M25 / M26 contract

M25 is presentation/observability only. It may read already-owned state and render it. It may not:

- score, rank, promote or demote a setup;
- alter M15 selection;
- alter Entry/SL/TP/lot;
- mutate M19/M20 risk/protection;
- mutate M23/M24 lifecycle/recovery;
- create broker actions.

Displayed live trade count must come from the current broker open-order pool plus exact EA ownership, not raw `g_monitored_count`.

### M27 contract

M18/M25 are observability-only and cannot gate or reorder execution.

Canonical execution ownership remains:

`M15 selection -> M16 revalidation -> M17 SL/TP -> M21 sizing -> M19 risk -> M20 protection -> M22 execution`.

Q11 may not call, recreate, shortcut or shadow-own any of those authorities.

## 4. Historical dashboard materializer verdict

Historical `dashboard-chain-*` branches are **REFERENCE / PROVENANCE ONLY**.

Useful display concepts may be reconsidered, but the historical source transformation must not be cherry-picked directly into Build 5.11.

### Rejected historical logic

The following historical ideas are not acceptable as current M25 implementation because they duplicate strategy ownership:

- local `DashREConfirmed()`-style confirmation;
- local Extreme readiness/maturity calculation;
- local MLV/MHV readiness calculation;
- reconstruction of REM/RRE/REE as an independent setup authority;
- local BUY/SELL rank or equal-rank arbitration;
- score / quality / PriorityTier display implying execution quality;
- any local candidate promotion/demotion;
- any dashboard-derived signal eligibility.

If a value is not already owned by current authoritative state, Q11 must display `-`, `NONE`, `UNRESOLVED`, or omit the field. It must not infer it.

## 5. Authoritative display-owner map

The minimum safe future rich view is:

`PAIR | D1 | H4 | NMJE | D1O | DECISION | POSITION`

All values are read-only projections of existing owners.

| Display field | Authoritative source | Allowed rendering | Forbidden inference |
|---|---|---|---|
| Pair | `g_pair_states[i].actual_symbol` | exact configured broker symbol | symbol heuristics |
| D1 owner | `g_pair_states[i].d1_major_trend_owner` | owner state/direction; optional owner candle | recomputing EMA50/price-side rule in M25 |
| H4 owner | `g_pair_states[i].h4_direction_owner` | current local owner direction/state | rebuilding H4 setup |
| NMJE | `g_nested_journeys[i]` | Relation, JourneyID or compact reason; read-only | relation scoring/gating |
| D1O | `g_pair_states[i].d1_opportunity` and/or matching read-only nested overlay | active family/direction/cycle state | creating opportunity or tactical authority |
| Final decision | `g_pair_states[i].last_decision` | Valid, SignalType, Direction, DecisionState, RejectionReason; optional D1 authority/family fields | rebuilding selected setup from detector state |
| Live positions | broker `OrdersTotal()` + `IsExactEAOwnedSelectedOrder()` | exact-owned BUY/SELL counts/tickets | raw `g_monitored_count` as broker-live count |
| Recovery/identity diagnostic | matching existing `TradeInfo` row only | ticket/hash/recovery state when already present | mutating/reconstructing identity |
| Balance/equity | `AccountBalance()/AccountEquity()` | display only | risk decision |
| Protection reference | `g_protection_reference_equity` | display only | recalculating M19/M20 state |

### Decision-state rule

`DEC_VALIDATED` and `DEC_EXECUTED` must remain visually distinct.

A valid/validated decision must never receive an executed marker merely because it passed strategy validation.

Execution display requires attributable broker/execution state, not a display-side assumption.

## 6. Position aggregation rule

If Q11 shows per-pair positions:

1. scan broker `MODE_TRADES`;
2. accept only `IsExactEAOwnedSelectedOrder()`;
3. aggregate all exact-owned live BUY/SELL positions for that pair;
4. retain separate BUY and SELL counts;
5. if a deterministic display signature is required, sort by unique broker ticket before serialization;
6. do not use order-pool enumeration order as display identity.

This is presentation determinism only.

It must not change TradeLock, portfolio counting, lifecycle registry or execution identity.

## 7. Recommended first materialization shape

### Q11-A — pure formatter/read helpers

Recommended first implementation keeps the existing `Comment()` dashboard rather than introducing chart objects.

Purpose:

- expand `BuildDashboardSnapshot()` only from authoritative state;
- add small pure read/format helpers where necessary;
- no state mutation;
- no new timer ownership;
- no broker action;
- no duplicated strategy formula.

This is the lowest-regression path.

### Q11-B — authoritative pair rows

Add compact current-owner fields only:

`PAIR D1 H4 NMJE D1O DECISION POSITION`

The display may abbreviate enum text, but abbreviation is formatting, not semantic remapping.

### Q11-C — exact-owned position aggregation

Add deterministic per-pair position summary from exact broker-owned positions.

Recommended examples:

- `-`
- `B1`
- `S2`
- `B1/S1`

Do not encode quality or recommendation.

### Q11-D — optional chart-object presentation

Only if a later UI requirement justifies moving from `Comment()` to `OBJ_LABEL`:

- use a dedicated object prefix;
- deterministic row keys;
- ticket-sorted position signature;
- explicit `OnDeinit()` cleanup;
- `ShowDashboard=false` leaves no stale objects/comment;
- reattach/recompile creates no duplicates.

This slice should remain separate from Q11-A/B/C.

### Q11-E — native/runtime closure

After materialization:

- source-scope guard;
- static authority guard;
- native MetaEditor 0 errors / 0 warnings;
- targeted regression;
- broker/demo display lifecycle validation;
- cross-module purity review.

## 8. Refresh policy

Current dashboard snapshot is rebuilt by current strategy/display triggers and live-trade-count refresh.

Time/balance/equity/protection text may therefore be temporarily stale between rebuilds. This is an **ENGINEERING DISPLAY-FRESHNESS IMPROVEMENT**, not a Strategy-Core defect.

If later freshness is required, use a pure display refresh that only re-reads presentation data.

It must not:

- create another strategy clock;
- run detectors;
- mutate PairState/NMJE/lifecycle state;
- call M15 selection, M16, M17, M19, M20, M21, M22, M23 or M24.

M15 remains the sole Strategy-Core processing clock.

## 9. Observer boundary

Current Build 5.11 observer is baseline and should not be replaced.

Q11 may reuse changed-only emission for display-adjacent diagnostics, subject to:

- no execution/risk/strategy authority;
- critical decision/execution/recovery diagnostics remain attributable;
- `DBG_FULL` behavior is preserved;
- observer cache/state is diagnostic only;
- no GlobalVariable trade-state ownership.

No observer refactor should be bundled into a simple dashboard formatting change unless a confirmed defect requires it.

## 10. Forbidden Q11 calls / behavior

Future M25/Q11 code must fail review if it introduces any of the following:

- `OrderSend`, `OrderClose`, `OrderModify`, `OrderDelete`;
- detector invocation for display reconstruction;
- M13/M14/M15 candidate construction/selection;
- M16 executable revalidation;
- M17 SL/TP resolution;
- M19/M20 risk/protection decisions;
- M21 sizing;
- M22 execution;
- M23/M24 lifecycle or recovery mutation;
- write access to trade/recovery GlobalVariables;
- local strategy ranking, score, vote, confidence or quality tier;
- live-candle Strategy-Core inference;
- local reimplementation of D1/H4 owner or D1O rules.

## 11. Acceptance matrix

| ID | Case | PASS condition |
|---|---|---|
| Q11-00 | Source scope | delta limited to M25/display helpers and minimal M26 cleanup only if object lifecycle requires it |
| Q11-01 | Broker-action firewall | dashboard/observer surface contains no OrderSend/Close/Modify/Delete authority |
| Q11-02 | Strategy-authority firewall | no detector, combination, selection, validation, risk, sizing or execution call is introduced |
| Q11-03 | Owner projection | D1/H4/NMJE/D1O/decision fields are read from authoritative current owners without recomputation |
| Q11-04 | Decision lifecycle display | VALIDATED and EXECUTED are distinct; display cannot manufacture execution |
| Q11-05 | Exact-owned position view | displayed live count/aggregation matches broker MODE_TRADES exact ownership |
| Q11-06 | Position 0->1->0 | display follows natural open/close without strategy/lifecycle mutation |
| Q11-07 | Deterministic position signature | if signatures/objects are used, unchanged ticket set does not redraw merely because pool enumeration order changes |
| Q11-08 | ShowDashboard=false | no Q11 display remains active/stale |
| Q11-09 | remove/reattach | no stale or duplicate objects; required only for object-based UI |
| Q11-10 | Observer regression | changed-only behavior and debug/critical-log boundaries remain intact |
| Q11-11 | Native compile | exact materialized MQ4 compiles MetaEditor 0 errors / 0 warnings |
| Q11-12 | Cross-module purity | no Strategy Core, risk/MM, execution, lifecycle or recovery semantic delta |
| Q11-13 | Multi-pair isolation | each row uses its own PairState/NestedJourney/position ownership; no cross-symbol leakage |
| Q11-14 | Restart view | recovered live positions display from current authoritative broker/recovery state without fabricating full DecisionID |
| Q11-15 | Build identity | any EA source change gets a unique new build/source revision tag and attributable compile/runtime evidence |

## 12. Static guard targets

A future materialization should include fail-closed checks that:

1. changed source scope is bounded;
2. dashboard section contains no broker-action calls;
3. dashboard section contains no detector/selection/risk/lifecycle calls;
4. no historical `DashREConfirmed`, `DashExtremeReady`, `DashMLVReady`, rank/score helper or semantic equivalent appears;
5. `CountDashboardLiveEAOwnedTrades()` continues to use exact broker ownership;
6. observer bodies protected by Build 5.11 regression remain unchanged unless the task explicitly targets an observer defect;
7. current protected M01-M24 strategy/risk/execution/lifecycle bodies remain byte/semantic unchanged for a dashboard-only patch.

## 13. Reuse from historical preparation

The following concepts may be reused **only as engineering display mechanics**:

- multi-position BUY/SELL aggregation;
- deterministic ticket sorting for a display signature;
- explicit validated-vs-executed visual distinction;
- chart-object cleanup on deinit if chart objects are later introduced;
- ShowDashboard=false cleanup;
- reattach duplicate-object checks.

The historical setup/rank/readiness computation is rejected.

## 14. Entry condition after Q10

If Q10 closes with the same normalized source SHA
`50E4A01A5768B5B5E9A80CABAE21B7260A2912AA058E67E5273386177970D038`:

- this readiness package may be used directly as Q11 implementation baseline;
- do not repeat the full historical dashboard audit;
- perform a short live-delta recheck of M25/M26/M27 + relevant state structs before coding.

If Q10 requires any EA source change before final closure:

- re-read the new source identity;
- delta-audit only affected state owners, M25/M26/M27, observer and ownership helpers;
- update this package before implementation.

## 15. Current verdict

**Q11 IMPLEMENTATION READINESS = PREPARED.**

No current EA bug requires an opportunistic dashboard fix.

The safe future implementation is a read-only projection of authoritative Build 5.11 state, preferably starting with the existing `Comment()` surface.

Historical rich-dashboard strategy reconstruction/ranking logic is not reusable as executable source.

Q11 remains deferred behind Q10 final acceptance unless explicitly reprioritized.
