# Build 4.83 NMJE Read-Only Runtime Closure — 2026-09-17

Issue: #141
PR: #142
Candidate: Build 4.83 `fix/nmje-readonly-authority-141`
Owner base reconciled through `0d8c8ac71aeb9947d48f89239f46a88c31981182`.

## Exact candidate identity
- MQ4 SHA-256: `FC6DEF0B225F473DDF81E5A3B027546256C8D76D462D1F6AC9230586A556D087`
- EX4 SHA-256: `F2D081839DE63EF416906D851C45FE68614D6E141E144660C4FD15B953F2E962`
- Native MetaEditor verification: `0 errors, 0 warnings`.
- Isolated runtime folder: `D:\BBMA\MT4_NMJE_141_Demo`.
- Expert name: `BBMA_EA_NMJE_141_483`.

## Runtime safety configuration
- MetaQuotes-Demo / EURUSD M15.
- `MaxTradePerPair=0`, `MaxTotalTrade=0`, `TradeLockMode=2`.
- `ExpertsTrades=false` at terminal config.
- `BlockNMJEConflict=true` and `BlockNMJEBuilding=true` intentionally retained to prove they are legacy/inactive inputs after the authority repair.
- Primary MT4 was not restarted or modified.

## Attributable runtime evidence
The exact candidate initialized successfully, resolved broker symbol/spec, recovered D1 owner context and emitted one live NMJE observation:
`[N1-NMJE] EURUSD REL=BUILDING ... R=H4_LOCAL_OPPOSES_D1`.

The same exact runtime emitted `[F7-TELEM] ... Init=1 Connected=1 ...` and was gracefully closed to flush logs.

Runtime log counters:
- `[N1-NMJE]`: 1
- `[NMJE-GATE]`: 0
- broker execution / `DEC_EXECUTED` / `OrderSend`: 0

The absence of `[NMJE-GATE]` is not used alone as proof of execution neutrality. That authority property is proven statically/TDD: `RunEntryPreflightAndExecute()` no longer calls `NMJE_PassExecutionGate`, while N1/N2 observer telemetry remains in source. Runtime proves the observer path is still alive and connected after the repair.

## Identity caveat owned elsewhere
A legacy informational log line still says `BBMA EA V4.5.9 ...`. It is stale text and is not used for Build 4.83 attribution. Runtime attribution uses the isolated deployment path plus exact MQ4/EX4 hashes above. Canonical build-marker hardening remains owned by Issue #127/Q2 and is not expanded into #141.

## Result
**#141 candidate runtime gate: VERIFIED for read-only authority restoration.**

This does not authorize merge or production activation. PR #142 remains the integration vehicle.
