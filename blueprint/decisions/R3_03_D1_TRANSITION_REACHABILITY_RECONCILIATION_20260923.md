# R3-03 D1_TRANSITION Reachability Reconciliation — 2026-09-23

Issue: #248  
Q10: #109  
Baseline owner: `d1-owner-dev@a162a2b3d8c7337e1347f7d8f8f0b2f469c34618`  
EA candidate: Build 5.11 / `V511_EVENT_DRIVEN_OBSERVER_20260922`

## Classification

**SOURCE/CONTRACT CLARIFICATION + ACCEPTANCE DEFECT FIX / NO EA SOURCE CHANGE**

This decision resolves the reachability HOLD exposed by Q10 R3-03. It does not change the BBMA D1 strategic-owner hierarchy, introduce a new indicator, change MA50 type, change the processing clock, or create new execution authority.

## Source findings

The accepted source chain supports all of the following:

- MA50 is the BBMA trend / structural reference.
- The project uses MA50 as EMA50, period 50, applied to Close.
- D1 is the accepted strategic major-trend timeframe in the scoped project hierarchy.
- Primary source wording describes price above MA50 with an ascending MA50 as bullish and price below MA50 with a descending MA50 as bearish.
- The source does not define a software state named `D1_TRANSITION`, an EMA slope lookback other than the project mapping, a pip/ATR threshold, an N-day confirmation delay, or a deterministic non-equality transition algorithm.

Therefore the explicit `D1_TRANSITION` state remains a project fail-closed mapping rather than verbatim BBMA source semantics.

## Reachability proof for the current mapping

For the project EMA applied to Close:

`EMA_t = alpha * Close_t + (1-alpha) * EMA_(t-1)`, where `0 < alpha < 1`.

Therefore:

`EMA_t - EMA_(t-1) = alpha * (Close_t - EMA_(t-1))`

and:

`Close_t - EMA_t = (1-alpha) * (Close_t - EMA_(t-1))`.

Both expressions have the same sign. Hence, for valid non-equality data:

- `Close_t > EMA_t` iff `EMA_t > EMA_(t-1)`;
- `Close_t < EMA_t` iff `EMA_t < EMA_(t-1)`.

Consequently, with the current immediate adjacent-bar EMA50 mapping:

- `Close1 > EMA50_1` and `EMA50_1 > EMA50_2` are not independent conditions;
- `Close1 < EMA50_1` and `EMA50_1 < EMA50_2` are not independent conditions;
- the documented examples “close above EMA50 while EMA50 falls” and “close below EMA50 while EMA50 rises” are not reachable non-equality market states under this mapping.

Historical Build 5.11 evidence is consistent with the proof: 66,408 GBPUSD D1-owner observations contain BUY/SELL only, and the targeted scans recorded in #248 found no non-equality transition candidate.

## Reconciled semantic classification

The following remains accepted and unchanged:

1. D1/MA50 is the scoped strategic major-trend owner.
2. Fully closed D1 data is mandatory.
3. Confirmed BUY and SELL remain the current M11 output names and execution directions.
4. `D1_OWNER_UNRESOLVED` remains the fail-closed state for missing/invalid required history.
5. Any `D1_TRANSITION` value presented to downstream execution remains fail-closed with `DIR_NONE`.
6. `D1_TRANSITION` is not a broker-close rule.
7. H4 cannot create a substitute D1 strategic owner.
8. REM/RRE/REE signatures remain unchanged.

The following is corrected:

- The immediate one-bar EMA50 slope clause is an **engineering mapping that is algebraically redundant with same-bar price side for non-equality EMA(Close) data**. It must not be treated as an independent market dimension capable of producing the old non-equality transition examples.
- Under the current mapping, a naturally reachable valid `D1_TRANSITION` is limited to equality/flat degeneracy permitted by exact input arithmetic. Such equality can be extremely rare or absent in finite broker history.
- No source authority exists to invent a wider observable transition zone merely to satisfy test coverage.

## Explicitly rejected fixes

Do not close R3-03 by:

- replacing EMA50 with SMA/SMMA;
- changing EMA50 period or applied price;
- using a longer slope lookback;
- adding a pip/percentage/ATR tolerance;
- adding an N-day confirmation rule;
- freezing the previous executable D1 direction;
- using H4/LTF direction as fallback;
- synthesizing broker history to manufacture a natural transition.

Any such change would create new Strategy-Core/project semantics and requires a separate source decision.

## EA implementation verdict

**NO EA FIX REQUIRED.**

Current Build 5.11 M11:

- uses `MODE_EMA`, `PRICE_CLOSE`, period 50;
- uses the latest fully closed D1 candle and immediately previous D1 EMA50;
- classifies the otherwise-valid fallback as `D1_TRANSITION` with `DIR_NONE`;
- permits new-entry strategic execution only for confirmed BUY/SELL owner states.

The current conjunction may remain in code because it is behaviorally equivalent to price-side classification for non-equality EMA(Close) data and preserves the source-facing descriptive contract. Removing it is unnecessary churn and would not improve runtime behavior.

## R3-03 acceptance correction

R3-03 remains a mandatory case, but its evidence mode changes from **natural four-class occurrence** to **deterministic-by-construction reachability + fail-closed verification**.

R3-03 PASS requires attributable proof that:

1. canonical source uses EMA50 period 50, `MODE_EMA`, `PRICE_CLOSE`;
2. M11 uses immediate adjacent fully closed D1 EMA50 observations;
3. the immediate EMA(Close) sign-coupling invariant holds;
4. the M11 fallback transition branch assigns `DIR_NONE`;
5. D1 strategic execution readiness accepts only confirmed BUY/SELL states;
6. historical evidence contains no contradiction to that invariant.

Natural observation of a non-equality `D1_TRANSITION` is **not required** and must not be used as a release blocker.

If a real future broker/runtime sample contradicts the invariant while the exact canonical formula is unchanged, classify it as data/implementation verification failure, not as proof of a new BBMA transition rule.

## R3 closure correction

The historical R3 closure wording requiring all four owner classes to appear naturally is superseded only for R3-03.

Required coverage becomes:

- BUY: positive attributable observation;
- SELL: positive attributable observation;
- TRANSITION: deterministic-by-construction reachability/fail-closed proof under this decision; natural equality occurrence optional;
- UNRESOLVED: positive fail-closed evidence as required by the matrix;
- all DecisionID/hash/direction/dedup requirements remain unchanged.

## Q10 consequence

After the updated deterministic R3-03 checks pass against exact Build 5.11:

- R3-03 may be recorded `PASS / DETERMINISTIC_BY_CONSTRUCTION`;
- the #248 HOLD is resolved;
- Phase H may advance with R5-19 remaining the already-defined conditional safe-only INCOMPLETE;
- Phase L MetaQuotes-Demo becomes eligible under the existing hybrid policy, but is not executed by this documentation/tooling reconciliation itself.

## Supersession scope

This record supersedes only the **reachability interpretation and natural-observation acceptance requirement** in:

- `HOME_COURSE_D1_TRANSITION_MAJOR_TREND_OWNER_DECISION.md`;
- `M11_D1_MAJOR_TREND_OWNER_CONTRACT.md`;
- `R3_R6_CONSOLIDATED_BROKER_RUNTIME_ACCEPTANCE_MATRIX_PREP_20260826.md`;
- `Q10_R3_TRANSITION_ACCEPTANCE_HOLD_CORRECTION_20260923.md`.

It does not revoke the D1 strategic-owner hierarchy or the fail-closed execution policy.

## Final verdict

**R3-03 is resolvable without changing EA Strategy-Core execution behavior.**

The confirmed defect is the project expectation that an immediate EMA(Close) price/slope disagreement should be naturally observable. Correct the contract and Q10 acceptance tooling; retain Build 5.11 EA source unchanged.
