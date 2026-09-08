# F7 Post-Freeze Fix Package Preparation — 2026-09-08

## Status
PREPARATION ONLY / NO EA SOURCE CHANGE / DO NOT DEPLOY DURING CURRENT RUNTIME FREEZE.

## Baseline
- Active implementation owner at preparation time: `d1-owner-dev` / `c3318c20970b9c4413b75b46e01976a6e511bf92`.
- Canonical source: `blueprint/source/BBMA_EA.mq4`.
- Related confirmed issues: #127, #132, #133.
- Strategy Core, risk/MM, candidate selection and M22 OrderSend authority are out of scope.

## Package A — Issue #127 deterministic runtime build identity
On the next authorized unique F7 build:
1. assign a globally unique build/version identity; do not reuse 4.61/4.62/4.63/4.64/4.79/4.80/4.81;
2. synchronize header, `#property version`, dashboard/init label and F7 telemetry identity;
3. emit one `[F7-BUILD]` record per genuine initialization/reload;
4. include non-circular deterministic source/build identifiers such as BuildTag + Git/source revision tag + unique binary/build tag;
5. capture actual MQ4 SHA-256 and EX4 SHA-256 externally in compile/deployment evidence rather than pretending the binary can self-hash deterministically before it exists.

Acceptance: marker appears once per init in the active Data Folder and unambiguously maps to the externally recorded source/EX4 hashes.

## Package B — Issue #132 exact EXEC open-time telemetry
Current source freezes the exact new-ticket open time into `info.open_time` immediately after successful `OrderSelect(ticket, SELECT_BY_TICKET)`, then `AddToMonitoredTrades(info)` may change MT4 global selected-order state before `[P3M1/P3M2][EXEC]` is printed.

Smallest fix:
- replace only the two EXEC telemetry `TimeToString(OrderOpenTime())` reads with `TimeToString(info.open_time)`;
- do not alter OrderSend timing, broker selection, decision identity, SL/TP, lot or risk.

Acceptance: static proof that EXEC open-time telemetry no longer depends on ambient selected-order state, followed by one exact-ticket runtime trace satisfying the F6 timing contract.

## Package C — Issue #133 live-delta reconciliation
Exact live-vs-canonical delta classification:
- move `F7ProspectiveContextTelemetry` into successful `ProcessEntry()` after `DEC_EXECUTED`: RETAIN CANDIDATE / observability-only;
- add broker ticket to helper and `[F7-PROSPECTIVE]`: RETAIN CANDIDATE / observability-only;
- remove old post-preflight call from `ProcessPair()`: paired relocation;
- `CompactMonitoredTrades()` inside `F7TelemetryHeartbeat()`: REJECT AS OWNER PLACEMENT / telemetry must remain read-only.

The compaction helper is not read-only: it can emit closed outcomes, clear lifecycle checkpoints and remove monitored state. Future reconciled source should place ordinary registry cleanup under M23/authoritative lifecycle housekeeping, not heartbeat telemetry.

Candidate minimal ownership mapping after freeze:
`ManagePositions()` completes lifecycle/close handling -> authoritative closed-registry compaction/cleanup -> return; `F7TelemetryHeartbeat()` only counts/prints state.

This is an engineering ownership correction, not a BBMA strategy rule.

## Protected surfaces
The post-freeze implementation must prove unchanged:
- M15 remains sole processing/final-decision clock;
- M22 remains sole normal OrderSend authority;
- M19/M20/M21 risk/MM semantics unchanged;
- M06-M12 detectors and M13-M16 selection/validation unchanged;
- M12N/NMJE remains read-only/non-execution authority;
- F7 source lifecycle semantics are not expanded by this package.

## Validation order after freeze release
1. scoped branch from current owner branch;
2. materialize only confirmed authorized deltas above;
3. assign next unique build identity;
4. static/cross-module ownership checks;
5. native MetaEditor 0 errors / 0 warnings;
6. targeted regression for EXEC telemetry, F7 build marker, prospective telemetry placement and registry cleanup;
7. runtime reload proves `[F7-BUILD]` identity;
8. exact-ticket F6 timing trace;
9. F7 close -> prompt registry cleanup/outcome emission without heartbeat mutation;
10. focused F7 lifecycle/restart matrix: failed Momentum, Momentum hold, Re-Entry re-arm, opposite CSM, opposite mature Extreme supersession, restart recovery and duplicate-close prevention.

## Gate
Do not implement/deploy this source package until the current runtime freeze is explicitly released. Preparation of this document does not authorize a primary MT4 reload, merge or production claim.