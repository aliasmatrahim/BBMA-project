# P3 — Runtime Initialization Evidence

Date: 2026-08-22
Branch: `blueprint-dev`
Status: **INITIALIZATION PASS / PAIR-MAP PASS / P3S5 TEST A PASS — TEST B/C/D PENDING**

## Evidence source
User-provided native MT4 screenshots after attaching the current compile-clean EA build.

## Directly visible startup evidence
- EA log reaches `[P3S1][PASS] EA initialized successfully with 20 pairs`.
- Pair resolution and broker-spec validation complete across the configured 20-pair set in the supplied captures.
- Visible broker-spec lines report `[P3S1][PASS]` with PairID and Magic values.
- No current initialization-failure line is visible.
- Earlier `uninit reason 3` lines are followed by a clean re-initialization and are treated as chart/timeframe lifecycle events rather than current init failure.

## P3 Step 5 — Test A recovery evidence
The second supplied capture exposes the full recovery fields for multiple exact-owned open orders. Examples include GBPAUD, EURAUD, GBPUSD, EURUSD and GBPCAD. Each visible recovery line has the required form:

`[P3S5][RECOVERY] Ticket=<ticket> Pair=<pair> State=REC_IDENTITY_MISSING_FROZEN Cause=MISSING_EXECUTION_HASH HashFound=N FullMeta=N`

This directly proves the runtime classification expected for pre-existing exact-owned orders that do not carry the current `BBMA|H:` execution identity.

The current source also confirms that, after geometry/lot validation and classification, `AddToMonitoredTrades(info)` is executed before the recovery diagnostic is printed. Therefore these frozen identity-missing orders remain in EA monitored/risk/portfolio ownership rather than being silently discarded.

### Test A verdict
**PASS.** Required runtime classification fields are visible and the source ownership path preserves the recovered orders in the monitored portfolio.

## Remaining P3 Step 5 evidence
### Test B — frozen-state log suppression
**PENDING.** Current screenshots show the initialization/reconstruction burst only. Need a later Experts-log window, after several subsequent ticks/timer cycles, proving that `[P3S5][RECOVERY]` is not emitted repeatedly outside reconstruction.

### Test C — fresh M22 execution identity persistence
**PENDING.** Need one genuine new EA trade from the current build and a visible `[P3S5][EXEC_ID] ... Persist=PASS HashFound=Y HashMatch=Y ...` line.

### Test D — restart after fresh hashed trade
**PENDING.** After Test C, restart/re-attach while that fresh trade remains open and verify the execution hash is recovered without downgrading the trade to `REC_IDENTITY_MISSING_FROZEN` and without duplicate execution.

## Current runtime verdict
- Native MetaEditor: **PASS — 0 errors / 0 warnings**.
- Runtime initialization: **PASS**.
- Pair/symbol/broker-spec startup mapping: **PASS**.
- P3S5 Test A: **PASS**.
- P3S5 Test B: **PENDING**.
- P3S5 Test C: **PENDING**.
- P3S5 Test D: **PENDING**.

## Next evidence capture
Leave the EA attached and running through several subsequent cycles without restarting it. Then capture the Experts log at a later timestamp. The evidence target for Test B is that the earlier `[P3S5][RECOVERY]` burst does not keep repeating every cycle.

No strategy, risk, execution or dashboard code is changed by this evidence record.