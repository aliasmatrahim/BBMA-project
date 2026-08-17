# P2 Step 18 — Final Cross-Module Regression Audit

Status: FAIL — Fix B required

Compile baseline after S18 Fix A: 0 Errors / 0 Warnings (user-reported MetaEditor result)

## Scope
Final P2 static regression across initialization/input contract, broker symbol identity, signal-to-decision lifecycle, invalidation, SL/TP, risk, portfolio protection, execution, recovery and orchestration.

## Fix A Re-Audit
The original TradeLock defect is functionally closed: the canonical source now validates the TradeLockMode range and calls `IsSignalAllowed()` before broker-send work.

However the patch was applied twice in two places:

1. `ValidateInputParameters()` contains the exact same TradeLockMode range check twice consecutively.
2. `ProcessEntry()` calls `IsSignalAllowed()` twice: first through `lockPairIdx`, then again after resolving `pairIdx`/`magic`.

The second issue is more than cosmetic. Trade-lock admission should have one deterministic execution-boundary check. Duplicating a live-state predicate creates two observation points for the same admission decision and can produce inconsistent rejection behavior if broker/monitored state changes between them. It also violates the single-authority/minimal-executor architecture established during P2.

## Required Fix B
- Remove the duplicate TradeLockMode input validation line; keep exactly one range check.
- Remove the first pre-pair/magic `lockPairIdx` TradeLock block.
- Keep exactly one `IsSignalAllowed(decision, pair, magic)` call after canonical `pairIdx` and `magic` validation and before monitored-registry capacity / broker-send preparation.
- Preserve `REJ_TRADE_LOCK` as the rejection reason for that single lock gate.
- No BBMA signal, EntryMode, SL/TP, sizing, risk or portfolio formula changes.

P2 remains open until Fix B compiles 0E/0W and the final S18 re-audit passes.