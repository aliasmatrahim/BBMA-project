# P3 — Opposite-Direction / Same-Pair Cycle Integrity Audit + TradeLock Fix

Date: 2026-08-22
Branch: `blueprint-dev`
Status: **BUG CONFIRMED / FIX IMPLEMENTED / STATIC REGRESSION PASS — METAEDITOR + RUNTIME TRACE PENDING**

## Trigger
Runtime observation showed BUY and SELL positions coexisting on one pair while `TradeLockMode=1`.

## Static audit
### Strategy decision layer
M15 already fails closed when eligible BUY and SELL candidates coexist in the **same atomic scan**: it creates `CONFLICT_DIRECTION_VIOLATION` rather than choosing an invented winner. Therefore the observed coexistence is not explained by same-scan M15 candidate selection.

Across later candles/cycles, a source-valid opposite BBMA cycle may legitimately become the new strategy owner while an older broker position is still open. Whether a new opposite order may coexist is therefore an **execution-policy** question owned by TradeLock, not a reason to corrupt the BBMA cycle state.

### Confirmed implementation defect
`LOCK_SAME_DIRECTION` previously rejected an existing trade when:
`existing.direction == decision.Direction`.

That behavior did the opposite of the mode name: it blocked same-direction additions while allowing an opposite position on the same pair. This directly explains BUY+SELL coexistence under mode 1.

## Fix
For `TradeLockMode=1`, M22 now rejects when:
`existing.direction != decision.Direction`.

Result:
- same-direction additions are permitted, subject to `MaxTradePerPair` and all other gates;
- opposite-direction coexistence for the same EA/pair is blocked;
- mode 2 continues to block any second position on the pair;
- mode 0 remains unrestricted by TradeLock.

Only live EA-owned monitored positions participate, preserving the locked M22 ownership contract.

## Boundary
No BBMA signal, direction, owner handover, F1-F6 lifecycle, EntryMode signature, SL/TP or risk calculation was changed. A valid opposite cycle may still become strategy-authoritative; mode 1 simply prevents its broker order from hedging against an older still-open EA position.

## Static regression
- M15 same-scan BUY/SELL conflict guard remains present;
- `LOCK_SAME_DIRECTION` now checks `existing.direction != decision.Direction`;
- legacy reversed comparison is absent;
- `LOCK_ONE_POSITION` behavior is unchanged;
- only live EA-owned positions are considered.

## Remaining verification
1. Native MetaEditor: **0 errors / 0 warnings**.
2. Runtime mode 1: BUY open + new BUY valid -> may pass TradeLock (subject to other gates).
3. Runtime mode 1: BUY open + new SELL valid -> `REJ_TRADE_LOCK`.
4. Runtime mode 2: any existing pair trade -> `REJ_TRADE_LOCK`.
5. Runtime mode 0: opposite coexistence is not blocked by TradeLock itself.
