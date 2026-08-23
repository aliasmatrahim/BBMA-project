# P3 — Input Parameter Audit & UI Mapping

Date: 2026-08-23
Branch: `blueprint-dev`
Source reviewed: `blueprint/source/BBMA_EA.mq4`
Status: **AUDIT PASS — READY FOR UI PATCH**

## Objective
Reduce the MT4 Inputs window to settings a normal user may reasonably need, convert fixed-choice inputs to dropdown enums, keep advanced execution/identity settings separated, and lock Strategy-Core/internal switches away from normal user editing without changing current defaults or trading behaviour.

## A. USER-FACING — keep visible
Recommended order in MT4 Inputs:

### 01 — Trading Setup
- `EntryMode = 2`
  - proposed dropdown:
    - `MODE_1_RE_ENTRY_ONLY = 1` — Re-Entry only / more selective
    - `MODE_2_ALL_VALIDATED_BBMA = 2` — Re-Entry + validated REM/RRE/REE

### 02 — Pair Selection
- `PairList = "EURUSD,USDJPY,GBPUSD,AUDUSD,USDCAD,USDCHF,NZDUSD"`

### 03 — Trade Limits
- `MaxTradePerPair = 2`
- `MaxTotalTrade = 10`
- `MaxActivePair = 7`

### 04 — Money Management
- `MMMode = 1`
  - proposed dropdown:
    - `MM_AUTO_LOT = 1`
    - `MM_FIXED_LOT = 2`
- `AutoLotPercent = 1.0`
- `FixedLot = 0.01`
- `MaxAutoLot = 1.0`

### 05 — Trade Control
- `TradeLockMode = 0`
  - proposed dropdown:
    - `LOCK_OFF = 0` — normal execution policy
    - `LOCK_SAME_DIRECTION = 1` — when a live EA trade exists on the pair, new trade must be same direction
    - `LOCK_ONE_POSITION = 2` — maximum one live EA position per pair

### 06 — Risk Protection
- `MaxSpreadPips = 10.0`
- `MaxDrawdownPercent = 20.0`
- `BasketLossPercent = 10.0`
- `MaxTotalRiskPercent = 5.0`

### 07 — Display
- `ShowDashboard = true`

Recommended normal-user visible total: **15 inputs**.

## B. ADVANCED — keep visible but place at bottom
These are legitimate operational settings, but normal users should rarely change them.

### 08 — Advanced Safety / Execution
- `MinRRRatio = 1.5`
- `MaxSLPips = 100.0`
- `Slippage = 3`
- `DebugLevel = 0`
  - proposed dropdown:
    - `DBG_OFF = 0`
    - `DBG_ERROR = 1`
    - `DBG_SIGNAL = 2`
    - `DBG_TRADE = 3`
    - `DBG_FULL = 4`
- `StrategyID = 1`
- `InstanceID = 0`

`StrategyID` and `InstanceID` are not cosmetic: they participate in magic-number identity. They should not be silently hard-coded unless multi-instance policy is redesigned.

Recommended advanced total: **6 inputs**.

## C. HIDE / LOCK INTERNAL
These should not be normal-user tuning controls. Preserve current values unless a separately audited architecture change authorizes otherwise.

### Strategy-Core / engine integrity switches
- `EnableBBShapeEngine = true`
- `EnableExtremeClassifier = true`
- `EnableMLVStateEngine = true`
- `EnableReEntryEngine = true`
- `EnableSignalScoring = true`
- `EnableRE_Type1 = true`
- `EnableRE_Type2 = true`
- `EnableRE_Type3 = true`
- `EnableRE_Type4 = true`

Reason: disabling these can alter or partially disable the accepted BBMA processing architecture. They are developer controls, not normal trading preferences.

### Internal lifecycle / compatibility parameters
- `MaxWaitBars_Extreme = 5`
- `MaxWaitBars_MLV = 5` — legacy compatibility; canonical MHV/MLV has no strategy TTL
- `MaxWaitBars_CSD = 5`
- `MaxWaitBars_ReEntry = 5`
- `MaxWaitBars_Combined = 5`
- `MaxWaitBars_Global = 10`

Reason: these affect component freshness/lifecycle policy and should not be exposed as casual optimization knobs. Preserve accepted defaults. Any future change requires source/contract review.

### Deprecated / display-only controls
- `SignalMode = 1` — deprecated for M15 entry authority
- `ScoreDisplayThresholdManual = 60` — deprecated trading threshold / display compatibility only
- `BasketProfitPercent = 5.0` — display compatibility only; not execution TP

### Internal execution/retry controls
- `MaxRetry = 3`
- `BERetryInterval = 60`
- `AllowedExecutionDeviation_MinPoints = 5`

Reason: implementation safety mechanics; hide from normal user. `AllowedExecutionDeviation_MinPoints` remains an internal broker-execution floor, not a strategy preference.

## D. Dropdown conversion rule
Only fixed-choice values should become enums. Proposed conversions:
- `EntryMode`: `int` -> enum input
- `MMMode`: `int` -> enum input
- `TradeLockMode`: already has an enum type defined; change input declaration to use that enum
- `DebugLevel`: already has `ENUM_DEBUG_LEVEL`; change input declaration to use that enum

The numeric values MUST remain identical so existing comparisons and saved semantics do not change.

## E. UI wording rule
Keep descriptions short enough for MT4 Inputs. Do not market Mode 1/2 as "better", "safer", or assign win-rate claims. Use behaviour-based wording only.

Recommended labels/descriptions:
- Mode 1: `Re-Entry only | selective`
- Mode 2: `RE + REM/RRE/REE | more opportunities`
- Auto Lot: `Lot derived from risk %`
- Fixed Lot: `Use FixedLot`
- Lock Off: `No optional live-position lock`
- Same Direction: `Existing pair trades constrain new direction`
- One Position: `Max 1 live EA trade / pair`

## F. Non-negotiable patch constraints
The UI patch must:
1. preserve every current default value;
2. preserve enum numeric values;
3. not change BBMA detector/entry/exit logic;
4. not change risk formulas;
5. not change magic-number generation;
6. not silently remove StrategyID/InstanceID identity capability;
7. update the source build/patch header;
8. require a fresh native MetaEditor compile result (`0E0W`) because source declarations change.

## Verdict
**READY FOR PATCH.**

Recommended final MT4 layout: **15 normal inputs + 6 Advanced inputs**, with all Strategy-Core toggles, lifecycle internals, deprecated controls and implementation-only controls hidden/locked at their existing values.
