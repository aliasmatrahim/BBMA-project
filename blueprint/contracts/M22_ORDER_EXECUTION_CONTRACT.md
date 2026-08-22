# M22 Order Execution Contract

Status: **LOCKED FOR P0 STEP 13**

## Role
M22 is a dumb broker executor. It may submit an already-approved order and report a definite/ambiguous result. It has no BBMA strategy authority.

## Immutable upstream payload
M22 must consume, not recreate or repair:
- `decision.Pair`;
- `decision.DecisionID`;
- `decision.Direction`;
- M17-approved `EntryPrice`, `StopLoss`, and `TakeProfit`;
- M21-approved lot;
- M19/M20 approval state.

Missing or mismatched immutable fields fail closed with `REJ_INVALID_DECISION_STATE`.

## Forbidden behavior
M22 must not:
- regenerate or rewrite `DecisionID`;
- change direction or signal type;
- move/replace SL;
- manufacture/extend/replace TP;
- resize, halve, clamp, or normalize lot after M21;
- use M18 score/level/SignalMode;
- bypass M19/M20 rejection;
- automatically resend after an ambiguous broker outcome.

## Execution price
BUY uses live ASK and SELL uses live BID. The execution price may differ from the closed-candle decision entry only within the frozen allowed deviation prepared for that decision. Exceeding it rejects with `REJ_EXECUTION_DEVIATION_EXCEEDED`.

## Retry contract
`MaxRetry` is the maximum number of actual retry attempts, not `MaxRetry + 1`.

Only definite retryable broker errors may retry. Fatal validation/margin/volume errors fail immediately because upstream M17/M21 already owns those parameters.

## Ambiguous result / idempotency
An ambiguous result means the broker may have accepted the request although the terminal did not receive a definitive success response.

Before every send, and once immediately after an ambiguous result, M22 must reconcile against live orders using all of:
- symbol;
- exact EA magic;
- order direction/type;
- stable decision execution tag `BBMA|H:<SHORT_HASH(DecisionID)>` at the beginning of `OrderComment()`.

The prefix is used because brokers/MT4 may truncate comments. Matching the entire long generated comment is unsafe.

If a matching live order is found, its ticket is treated as the confirmed execution result. If no matching order is observable after an ambiguous result, M22 returns `REJ_AMBIGUOUS_RESULT` and **must not send again**. M24/recovery may reconcile an order that becomes visible later.

## Trade lock
Trade-lock checks must consider only live EA-owned positions. Stale monitored entries or foreign/manual orders cannot create an M22 trade-lock rejection.

Mode semantics are explicit:
- `LOCK_OFF` / `TradeLockMode=0`: trade-lock itself imposes no pair-direction restriction; normal portfolio/strategy gates still apply.
- `LOCK_SAME_DIRECTION` / `TradeLockMode=1`: if this EA already has a live position on the pair, a new position is allowed only in the **same direction**; an opposite BUY/SELL coexistence on that pair is rejected with `REJ_TRADE_LOCK`. Multiple same-direction positions remain subject to `MaxTradePerPair` and other portfolio limits.
- `LOCK_ONE_POSITION` / `TradeLockMode=2`: any existing live EA-owned position on the pair blocks another position on that pair.

This is an EA execution-policy lock. It does not rewrite BBMA cycle direction. A later source-valid opposite cycle may become the strategy owner, but under mode 1 its new opposite order must wait until the old opposite live position is no longer open.

## Result mapping
- confirmed ticket: `DEC_EXECUTED`, `REJ_NONE`;
- execution deviation: `DEC_REJECTED`, `REJ_EXECUTION_DEVIATION_EXCEEDED`;
- ambiguous broker outcome: `DEC_REJECTED`, `REJ_AMBIGUOUS_RESULT`;
- definite broker failure: `DEC_REJECTED`, `REJ_BROKER_ERROR`;
- duplicate already executed decision: `DEC_REJECTED`, `REJ_DUPLICATE`.

## Validation
Initialization must reject `MaxRetry <= 0`, negative `Slippage`, or negative `AllowedExecutionDeviation_MinPoints`.

## Boundary
M22 may populate `TradeInfo` only from the actual broker order after a confirmed ticket. Any lifecycle management after execution belongs downstream, primarily M23/M24.
