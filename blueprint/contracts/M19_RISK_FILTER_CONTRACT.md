# M19 Risk Filter Contract

## Role
M19 is **FILTER ONLY**. It evaluates live broker/account/order risk after a decision has already been formed and validated by M15–M17.

M19 may reject a decision. It may not:
- create or reinterpret a BBMA signal;
- change BUY/SELL direction;
- rank RE_ENTRY/REM/RRE/REE;
- alter Entry/SL/TP;
- consume M18 score/level/SignalMode as trading authority;
- execute, close, modify or recover orders.

## Clock boundary
Strategy semantics remain closed-candle and M15-owned. Risk state is intentionally live at the pre-trade check because spread, equity, floating P/L, broker specification and open-order exposure are execution-time conditions.

## Spread
`MaxSpreadPips` is compared in **pips**, using the project `GetPipValue()` helper. No points-vs-pips double conversion is permitted.

Failure maps to `REJ_SPREAD_HIGH`. Invalid pip/broker specification fails closed as `REJ_BROKER_SPEC_INVALID`.

## Drawdown
Drawdown is measured against `g_protection_reference_equity` using live `AccountEquity()`:

`max(0, protection_reference_equity - account_equity) / protection_reference_equity * 100`

This is distinct from basket floating loss. Positive positions therefore offset negative positions when measuring actual equity drawdown.

Failure maps to `REJ_DD_LIMIT`.

## Basket loss
Basket loss remains the sum of negative floating P/L (profit + swap + commission) for EA-monitored open orders divided by `g_protection_reference_equity`.

A monitored-row broker selection failure is an **UNKNOWN** observation, not zero exposure and not proof that the row is closed/missing/foreign. If basket state cannot be resolved safely during pre-trade validation, M19 fails closed instead of understating floating loss.

Failure, including unresolved basket observation, maps to `REJ_BASKET_LOSS`.

## Total risk
`MaxTotalRiskPercent` is an **EA-wide prospective exposure cap**, not a same-pair cap.

Existing open monitored trades are measured using each trade's own symbol tick value and tick size. The proposed trade is then added using its approved M17 Entry/SL and calculated lot.

Closed/stale monitored entries do not contribute. Breakeven/zero-distance protected trades contribute zero risk. If an open position has risk that cannot be calculated safely, M19 fails closed instead of understating exposure.

The percentage denominator is the frozen pre-trade equity in `RiskValidationSnapshot`.

Failure maps to `REJ_TOTAL_RISK`.

## Rejection propagation
`RiskStatus` carries an explicit `ENUM_REJECTION_REASON`. Callers must propagate the actual M19 failure reason and must not collapse spread, drawdown or basket-loss failures into `REJ_TOTAL_RISK`.

## Ownership boundary
M19 consumes the already-approved M17 risk payload. It does not repair invalid SL/TP and does not manufacture fallback geometry. Invalid/unresolvable strategy payload must already have failed before M19.
