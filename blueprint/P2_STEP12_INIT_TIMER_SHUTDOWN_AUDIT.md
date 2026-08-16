# P2 Step 12 — Initialization / Timer Registration / Shutdown Lifecycle Audit

## Status
FAIL

## Finding
`OnTimer()` exists and now contains critical maintenance + shared live orchestration, but the canonical MQ4 contains no `EventSetTimer(...)` / `EventSetMillisecondTimer(...)` registration path found by repository search, and `OnInit()` only validates inputs then calls `InitializeEA()` before returning success. `OnDeinit()` clears local flags/dashboard state but does not call `EventKillTimer()`.

## Impact
Without timer registration, `OnTimer()` is dead code in normal MT4 runtime. Therefore timer-owned cleanup, daily reset fallback, and tick-independent lifecycle/protection fallback do not run. The Step 11 orchestration fix is structurally correct but cannot execute through the timer unless the timer is actually registered.

## Required Fix A
- Register one EA timer only after successful initialization, using a single explicit interval.
- Fail initialization if timer registration fails, rather than claiming full initialization.
- Call `EventKillTimer()` in `OnDeinit()` before clearing orchestration state.
- Keep `OnTimer()` logic unchanged; do not modify BBMA signal/SL/TP semantics.

## Verification
After patch:
1. Static verify exactly one timer registration path and one timer shutdown path.
2. Compile MetaEditor target: 0 errors / 0 warnings.
3. Re-audit init failure, timer callback availability, and deinit cleanup.
