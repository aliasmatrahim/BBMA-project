# P2 — Dashboard Live Trade Count Audit / Closure

Date: 2026-08-25
Branch: `d1-owner-dev`
Build lineage: `Version 4.5.1 - D1O-07 Canonical LTF Dedup`
Status: **CLOSED / PASS / DISPLAY-ONLY / NATIVE METAEDITOR 0E0W**

## Problem

Dashboard `Trades:` previously displayed raw `g_monitored_count`.

That value is a monitored-registry length, not guaranteed to equal the current number of open exact-owned broker positions. A closed row may remain in the registry until a later compaction path, producing a stale count such as dashboard `5` while only `3` EA-owned trades are actually open.

## Root cause

`BuildDashboardSnapshot()` used:

`IntegerToString(g_monitored_count)`

The registry is lifecycle/recovery infrastructure and may intentionally retain rows between compaction events. It is therefore not the correct display source of truth for a live open-trade count.

## Fix

Marker: `P2-DASHCOUNT-01`.

Added `CountDashboardLiveEAOwnedTrades()`.

The helper scans the current broker `MODE_TRADES` pool and counts only orders accepted by existing central ownership function `IsExactEAOwnedSelectedOrder()`.

That ownership function requires the selected order to be:
- still open;
- BUY or SELL;
- exact configured symbol;
- exact configured magic number.

`BuildDashboardSnapshot()` now uses this live exact-owned count rather than raw registry length.

The dashboard banner was also aligned from stale `D1-09` wording to current `D1O-07` wording.

## Refresh behavior

Added `RefreshDashboardLiveTradeCount()`.

It tracks the last displayed live count and rebuilds/updates presentation only when that count changes. `OnTimer()` invokes the refresh after normal `OnTickMain()` processing, allowing a closed trade to disappear from the displayed count without waiting for a later registry compaction/new-entry event.

## Hard authority guard

This change is display-only:
- no monitored-registry compaction is performed by the dashboard;
- no recovery/lifecycle state is mutated;
- no order is opened/closed/modified;
- no strategy candidate, D1/NMJE state, SL/TP, risk or lot-sizing authority changes;
- existing exact ownership helper is reused instead of inventing a second ownership rule.

## Materialization evidence

GitHub Actions materialization run: `32822882959`
Job: `97724594290`
Conclusion: **success**

Materialized source/contract commit: `2a04940` — `P2: refresh dashboard from broker live exact-owned count`.

## Final combined native compile evidence

GitHub Actions run: `32823122900`
Job: `97725322914`
Conclusion: **success**

EA SHA-256 compiled:
`2fd43ecda4edee45e641463215be70d1c043b36941906a7507946b606cc3826b`

Official MT4 MetaEditor result:
- errors: **0**;
- warnings: **0**;
- `P2_OBSERVABILITY_NATIVE_METAEDITOR=PASS`.

Artifact:
- `p2-observability-native-compile-evidence`;
- ID `9554031975`;
- digest `sha256:c95048cb6cd584f84efaaa2e52365c30505e1dacf1c286a0987146157119425d`.

## Verdict

**PASS.** Dashboard `Trades:` now represents live exact-owned open positions rather than potentially stale registry length, with no strategy or broker-behavior change.
