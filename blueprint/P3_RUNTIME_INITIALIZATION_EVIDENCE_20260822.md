# P3 — Runtime Initialization Evidence

Date: 2026-08-22
Branch: `blueprint-dev`
Status: **INITIALIZATION PASS / PAIR-MAP EVIDENCE PASS — P3S5 RECOVERY DETAIL PARTIAL, NEXT CAPTURE REQUIRED**

## Evidence source
User-provided native MT4 screenshot after attaching the current compile-clean EA build.

## Directly visible evidence
- EA log reaches `[P3S1][PASS] EA initialized successfully with 20 pairs`.
- Visible pair-resolution lines show requested symbols resolving successfully to broker symbols.
- Visible broker-spec lines report `[P3S1][PASS]` together with PairID and Magic values for multiple pairs, including EURUSD, GBPUSD, USDJPY, USDCHF, USDCAD, AUDUSD, NZDUSD, EURJPY, GBPJPY, AUDJPY, CADJPY, CHFJPY and NZDJPY.
- No initialization-failure line is visible in the supplied screenshot.
- Earlier `uninit reason 3` lines are followed by a clean re-initialization and are treated as prior chart/timeframe lifecycle noise rather than evidence of current init failure.

## P3 Step 5 recovery evidence
A `[P3S5][RECOVERY]` line is visible at the bottom of the screenshot for ticket `484106108`, pair `GBPAUD`, but the right-hand fields are cut off by the log viewport. Therefore the screenshot does **not** yet prove the required Test A state/cause/hash fields.

## Current runtime verdict
- Native compile: PASS (0 errors / 0 warnings), recorded separately.
- Runtime initialization: **PASS**.
- Pair/symbol/broker-spec startup mapping: **PASS for the visible evidence**.
- P3S5 Test A recovery classification: **PENDING FULL LINE**.
- P3S5 Test B log-suppression: **PENDING**.
- P3S5 Tests C/D fresh execution hash + restart recovery: **PENDING**.

## Next evidence capture
Capture the full `[P3S5][RECOVERY]` line by horizontally scrolling the Experts log to the right or widening the Message column. The required fields are the complete `State=... Cause=... HashFound=... FullMeta=...` portion. Then leave the EA running for several subsequent cycles and capture enough log to determine whether the recovery diagnostic repeats or remains initialization-only.

No strategy, risk, execution or dashboard code is changed by this record.