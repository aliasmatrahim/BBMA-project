# P3 — Dashboard Active-Trade Count Audit

Date: 2026-08-22
Branch: `blueprint-dev`
Status: **BUG CONFIRMED / FIX DESIGN READY / SOURCE CHANGE DEFERRED TO PRESERVE CURRENT RUNTIME CANDIDATE**

## Observed symptom
Dashboard can show a trade count larger than the number of currently active EA-owned broker orders (example reported earlier: dashboard 5 while only 3 trades were active).

## Root cause confirmed in current source
`BuildDashboardSnapshot()` renders:

`Trades: ` + `g_monitored_count`

rather than deriving the display count from a fresh broker-side exact-owned open-order view.

`g_monitored_count` is a registry count, not guaranteed to be a real-time active broker-order count.

The only compaction helper, `CompactMonitoredTrades()`, removes an entry only when:
- `OrderSelect(ticket, SELECT_BY_TICKET)` succeeds, and
- `OrderCloseTime() != 0`.

If `OrderSelect()` fails for a stale/missing ticket, the current code leaves that registry row in place. In addition, `BuildDashboardSnapshot()` itself does not compact or reconcile the monitored registry before displaying the count.

Therefore stale registry entries can survive and inflate the dashboard even when fewer exact-owned orders are actually open.

## Minimal safe fix design
Dashboard is display-only. Do not change strategy/risk/execution ownership.

Recommended fix:
1. Add a display-only helper that scans broker open orders (`OrdersTotal()` / `MODE_TRADES`).
2. Count only orders that satisfy the existing exact EA ownership predicate (`IsExactEAOwnedSelectedOrder`).
3. Use that broker-derived active count for the dashboard `Trades:` field.
4. Keep `g_monitored_count` as the internal registry count for existing ownership/recovery logic; do not repurpose it as a display truth source.

Optional hardening, separate from dashboard display:
- audit whether a failed `OrderSelect(ticket, SELECT_BY_TICKET)` in `CompactMonitoredTrades()` should retain or remove the row. Do not change this blindly because transient selection failure must not silently drop risk ownership.

## Why the dashboard fix should be broker-derived
A broker-side exact-owned open-order scan is deterministic for display and avoids making UI correctness depend on recovery/compaction timing. It also preserves the stronger fail-safe behavior of the internal monitored registry.

## Change-control decision
Do **not** modify the current EA source before P3 Step 5 Tests B–D are captured. The current build already has native 0E0W + runtime initialization PASS + Test A PASS. A dashboard-only source patch would still create a new binary candidate and force a fresh compile/deploy evidence chain.

The dashboard fix is ready to implement immediately after current runtime-candidate closure, or earlier only if the user explicitly chooses to supersede the candidate.
