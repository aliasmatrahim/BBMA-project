# P2 Step 13 — Runtime State Reset / Reinitialization Consistency Audit

## Status
FAIL — one deterministic reset defect remains.

## Finding
`InitPairState()` does not fully reset the `PairState` object before reuse. It explicitly resets selected scalar/state-machine members, but leaves several runtime-bearing members untouched, including timeframe snapshots/data, candle buffers, Bollinger snapshots, EMA history, signal memory, last signal/decision, last trade bar, trade ticket array, and timeframe snapshot structure.

`LoadPairs()` does call `InitPairState()` for every active slot, so `InitPairState()` is the canonical reset boundary for pair runtime state. A partial initializer means correctness depends on the object already being zero/new memory rather than on the initializer contract itself.

This is especially unsafe for any same-process reinitialization/reload path or future explicit re-run of `InitializeEA()`: stale signal/candle/decision state can survive slot reuse and contaminate the first closed-candle processing pass.

A second related gap exists at the EA-global level: risk-cache fields (`g_last_risk_check_time`, `g_cached_risk_allowed`, `g_cached_risk_reason`, `g_cached_balance`) are declared as mutable runtime cache but are not explicitly reset in `InitializeEA()`.

## Required Fix A
1. Make `InitPairState()` a complete deterministic reset boundary by zeroing the whole `PairState` first, then reapply required non-zero enum/timeframe defaults.
2. Explicitly reset EA-level transient risk cache fields in `InitializeEA()` before live recovery/scanning becomes operational.
3. Do not alter recovered broker truth, BBMA signal semantics, entry rules, SL/TP, or risk formulas.

## Compile requirement
After Fix A, compile canonical MQ4 in MetaEditor and require 0 errors / 0 warnings before re-audit.
