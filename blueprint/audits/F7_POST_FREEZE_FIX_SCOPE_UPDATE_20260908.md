# F7 Post-Freeze Fix Scope Update — 2026-09-08

This supplements the earlier #127/#132/#133 preparation. It does not authorize source mutation during the current runtime freeze.

## Newly confirmed restart-infrastructure defect
The next authorized F7 build must also address the C044 checkpoint/replay torn-write generation problem documented in `F7_C044_RESTART_ATOMICITY_AUDIT_20260908.md`.

This item is independent of Strategy-Core semantics and must not be combined with new entry/exit rules.

## Combined smallest post-freeze engineering scope
1. deterministic unique build identity + `[F7-BUILD]` (#127);
2. exact frozen `info.open_time` for EXEC telemetry (#132);
3. reconcile authorized live-vs-canonical F7 telemetry deltas and keep telemetry read-only (#133);
4. make C044 replay seed + lifecycle metadata one fail-closed committed generation;
5. keep canonical M08/M10/M12 detector ownership, M20 precedence, M22 OrderSend ownership and M23 full-close ownership unchanged.

## Additional acceptance for item 4
- simulate interruption after every write prefix when a prior complete generation already exists;
- no mixed old/new generation may load as valid;
- committed generations reproduce the same replay state after repeated restart;
- incomplete generation freezes/rejects recovery without fabricating a lifecycle event;
- physical restart replay after fix.

Do not assign a build number until the active repository is checked for collisions at implementation time.
