# P2 Step 17 — Full Signal-to-Trade Lifecycle Cross-Module Audit

Status: FAIL — Fix A required

## Scope
End-to-end path across M06-M17 and M27, including EntryMode 1 and EntryMode 2 candidate routing, closed-M15 orchestration, final decision authority, SL/TP handoff and entry preflight.

## Finding
The strategy scan candle gate uses the configured/base pair name while the actual detector/data/execution path uses the broker-resolved symbol.

`LoadPairs()` intentionally stores:
- `g_pair_names[i] = pair` (configured/base symbol)
- `g_pair_states[i].actual_symbol = actual` (broker-resolved symbol)

`ProcessPair()` correctly uses `actual_symbol` for D1/H4/H1/M15 data, detector snapshots, candidate construction, decision.Pair and execution.

However `OnTickMain()` calls:
`IsNewCandle(g_pair_names[i], i)`

`IsNewCandle()` then calls `GetLatestClosedCandleTime(pair, PERIOD_M15)` on that base/configured name.

On brokers that expose only suffixed/prefixed symbols (for example EURUSD.a, EURUSDm, etc.), Step 14 can correctly resolve and select the actual symbol, but Step 17's candle gate may still query the non-existent base symbol. If that returns 0/no series, `ProcessPair()` is never called and the entire BBMA signal-to-trade lifecycle is silently dead for that pair.

This is a cross-module consistency defect between M26 symbol resolution and M27 scan scheduling.

## Entry Mode impact
Both EntryMode 1 and EntryMode 2 are affected equally because the defect occurs before candidate collection and M15 final authority. The candidate-mode logic itself remains consistent in the inspected scope:
- EntryMode 1 admits standalone confirmed H1 Re-Entry only.
- EntryMode 2 admits standalone H1 Re-Entry plus validated REM/RRE/REE rows.

## Required Fix A
Use the broker-resolved `actual_symbol` as the sole market-data clock key in the M27 new-candle gate. The base/configured symbol may remain for user-facing identity / PairID semantics, but must not drive `GetLatestClosedCandleTime()`.

Recommended minimal change:
`IsNewCandle(g_pair_states[i].actual_symbol, i)`
with a fail-closed empty-symbol guard in `IsNewCandle()` if desired.

No BBMA detector, EntryMode, SL/TP, risk or execution semantics should change.