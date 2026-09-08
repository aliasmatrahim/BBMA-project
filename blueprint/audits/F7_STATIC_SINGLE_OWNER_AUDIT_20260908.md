# F7 Static Single-Owner Audit — 2026-09-08

Status: **STATIC REVIEW / NO EA SOURCE CHANGE**.

## Canonical producer reuse
F7 owner-event replay does not introduce separate BBMA detector formulas:
- Extreme is evaluated through canonical `DetectExtreme()` and `UpdateExtremeLifecycle()` / `ResolveOppositeExtremeSupersession()`;
- Re-Entry is evaluated through canonical `UpdateReEntryState()`;
- Momentum/CSM uses canonical `DetectCSM()`.

F7 owns only the post-entry lifecycle state (`MOMENTUM_PENDING`, `WAIT_NEXT_REENTRY`, `EXIT_LATCHED`, `FROZEN`) for an already-executed source-backed Re-Entry position.

## Event precedence
For each exact closed owner-timeframe candle:
1. canonical replay states advance;
2. opposite mature Extreme supersession is checked first;
3. if waiting, exact same-direction confirmed Re-Entry may re-arm;
4. if pending, same-direction CSM holds, then opposite CSM exits, then weaker reverse-colour failed-Momentum exits;
5. otherwise checkpoint persists.

This is consistent with the recorded F7 implementation contract and avoids a duplicated detector owner.

## Execution/close ownership
- M22 remains the normal `OrderSend` owner.
- F7 does not send replacement orders during re-arm.
- M20 emergency condition is processed before normal F7 close handling.
- M23-side `ExecuteLatchedC044Close()` performs the full broker close for an already-latched F7 exit.

## Registry ownership note
Canonical `F7TelemetryHeartbeat()` is read-only. The known live-only variant that calls `CompactMonitoredTrades()` from heartbeat remains rejected under Issue #133 because compaction can emit outcome, clear lifecycle checkpoint and remove registry state.

## Result
No new duplicate Strategy-Core detector or second execution authority was found in the reviewed canonical F7 path.

Separate restart-persistence defect remains open: checkpoint/replay writes are not one generation-atomic commit (`F7_C044_RESTART_ATOMICITY_AUDIT_20260908.md`).
