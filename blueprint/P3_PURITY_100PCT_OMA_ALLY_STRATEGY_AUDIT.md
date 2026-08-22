# P3-PURITY — 100% Oma Ally Strategy Purity Audit

Date: 2026-08-22
Branch reviewed: `blueprint-dev`
Scope: end-to-end trading-authority purity from accepted BBMA Core through execution admission. This audit distinguishes strategy semantics from EA safety and broker engineering.

## User mandate
The BBMA strategy/system must remain source-faithful to Oma Ally. No RSI, MACD, Stochastic, ADX, news/session/correlation filter, AI score, arbitrary quality score, or other unsourced strategy condition may create, rank, reverse, or invalidate a BBMA setup.

## Classification
- `OMA_ALLY_CORE` — directly accepted BBMA/Oma Ally strategy semantics.
- `SOURCE_DERIVED_MAPPING` — deterministic machine mapping needed to encode source concepts; must not invent external trading logic.
- `EA_SAFETY` — account/risk/portfolio protection applied only after a BBMA decision already exists.
- `BROKER_ENGINEERING` — broker/MT4 execution validity and idempotency controls.
- `LEGACY_UNUSED` — compatibility fields/functions with zero trading authority.
- `UNAUTHORIZED_STRATEGY_FILTER` — non-source logic that changes which BBMA setup wins, becomes valid, changes direction, or reaches execution while pretending to be strategy logic.

## Executive verdict
**PASS WITH EXECUTION-OVERLAY DISCLOSURE.**

At the current static-contract/source level, no active `UNAUTHORIZED_STRATEGY_FILTER` is identified in the BBMA signal-selection authority. The Core path M06–M17 remains source-owned/source-derived, and legacy scoring is explicitly neutralized.

However, the EA does **not** execute every otherwise-valid BBMA setup unconditionally. M17/M19/M20/M21/M22 contain explicit EA-safety / broker-execution admission gates that can reject a valid BBMA decision. These are not Oma Ally strategy rules and must never be described as such.

Therefore two claims must remain distinct:
1. **Strategy purity:** BBMA signal/setup/direction authority is Oma Ally source-faithful — PASS statically.
2. **Take-every-valid-BBMA-trade behavior:** NOT TRUE while safety/risk/broker gates are enabled, because valid BBMA decisions may be rejected downstream.

## Gate-by-gate classification

| Area | Current role | Classification | Purity result |
|---|---|---|---|
| M06 indicators | BB20/MA5/MA10/MA50 data | OMA_ALLY_CORE | PASS |
| M07 BB state | deterministic support for momentum semantics | SOURCE_DERIVED_MAPPING | PASS |
| M08 Extreme | strict Extreme + maturity lifecycle | OMA_ALLY_CORE + SOURCE_DERIVED_MAPPING | PASS |
| M09 MHV/MLV | source-owned lifecycle/body/retest model | OMA_ALLY_CORE + SOURCE_DERIVED_MAPPING | PASS |
| M10 eCSD/CSD/CSM | direction/momentum semantics | OMA_ALLY_CORE | PASS |
| M12 Re-Entry Type 1–4 | Re-Entry setup authority | OMA_ALLY_CORE + SOURCE_DERIVED_MAPPING | PASS |
| M13/M14 | REM/RRE/REE exact construction/validation | OMA_ALLY_CORE | PASS |
| M15 | final eligible candidate authority | OMA_ALLY_CORE / architecture authority | PASS |
| M16 | owner/freshness/invalidation | SOURCE_DERIVED_MAPPING | PASS |
| M17 TP mapping | BBMA-derived structural destination with Finale/forum corroboration and project mapping | SOURCE_DERIVED_MAPPING / corroborated execution policy | PASS WITH PROVENANCE |
| M17 hard SL | source-structure-informed broker protection | EA_SAFETY + BROKER_ENGINEERING | NOT CORE, allowed overlay |
| M18 scoring | neutral metadata only; Score=0, Level=NONE | LEGACY_UNUSED / observability | PASS |
| M19 spread/DD/basket/total-risk gates | post-strategy risk rejection | EA_SAFETY | changes execution admission, not strategy |
| M20 max pairs/trades/basket-loss | portfolio admission/protection | EA_SAFETY | changes execution admission, not strategy |
| M21 lot sizing / broker lot validity | sizing only | EA_SAFETY + BROKER_ENGINEERING | PASS boundary |
| M22 price deviation/retry/trade-lock/idempotency | broker execution/admission | BROKER_ENGINEERING + EA_SAFETY | changes execution admission, not strategy |
| M23/M24 lifecycle/recovery | execution management/recovery | EA_SAFETY + BROKER_ENGINEERING | outside signal Core |

## Explicit check for forbidden strategy additions
No active evidence was found that the final strategy authority uses:
- RSI;
- MACD;
- Stochastic;
- ADX;
- news filter;
- session filter;
- correlation filter;
- ATR/volatility filter as entry authority;
- EMA200 or other foreign trend filter;
- AI/ML score;
- M18 A+/A/B/C/D numeric score;
- SAFE/NORMAL/AGGRESSIVE score threshold;
- arbitrary signal-count threshold.

If any such condition is introduced later into M08–M16/M15 selection authority, it is automatically `UNAUTHORIZED_STRATEGY_FILTER` unless separately proven as accepted Oma Ally source semantics.

## Legacy scoring finding
M18 previously contained arbitrary scoring weights. The locked M18 contract now neutralizes numeric quality scoring:
- `Score = 0`;
- `Level = LEVEL_NONE`;
- `SignalMode`, `ScoreDisplayThresholdManual`, and `EnableSignalScoring` have no trading authority.

Status: `LEGACY_UNUSED / OBSERVABILITY`. No strategy impurity is currently certified from these fields.

## Behavior-changing overlays that must be disclosed
The following can cause `VALID BBMA DECISION -> NO TRADE` even though they are not strategy filters:

### M17 execution/risk geometry guards
- invalid/unresolvable SL/TP geometry;
- destination already crossed/stale;
- `MaxSLPips` rejection cap;
- `MinRRRatio` rejection filter;
- broker StopLevel/FreezeLevel constraints.

Purity classification: `EA_SAFETY / BROKER_ENGINEERING`, not Oma Ally setup semantics.

### M19 risk gates
- `MaxSpreadPips`;
- `MaxDrawdownPercent`;
- `BasketLossPercent`;
- `MaxTotalRiskPercent`.

Purity classification: `EA_SAFETY`. These may reject a valid BBMA decision but cannot create or reinterpret one.

### M20 portfolio gates
- `MaxActivePair`;
- `MaxTradePerPair`;
- `MaxTotalTrade`;
- emergency basket-loss protection.

Purity classification: `EA_SAFETY`.

### M21 sizing/broker-volume gates
- risk-based lot below broker minimum;
- lot above broker/effective maximum;
- invalid lot step;
- invalid FixedLot;
- invalid broker snapshot.

Purity classification: `EA_SAFETY / BROKER_ENGINEERING`.

### M22 execution gates
- frozen execution-deviation cap;
- trade-lock mode;
- duplicate/idempotency protection;
- definite/ambiguous broker errors;
- broker price validity.

Purity classification: `BROKER_ENGINEERING / EA_SAFETY`.

## Important semantic distinction
A safety overlay is acceptable only when it follows this direction:

`source-valid BBMA decision -> safety/broker check -> execute OR reject`

It becomes strategy impurity if it does this:

`non-BBMA metric -> change signal validity/direction/ranking -> M15 decision`

The current contracts explicitly prohibit M18/M19/M20/M21/M22 from changing BBMA signal type or direction.

## Potential policy tension: 100% strategy vs 100% trade-taking
The current architecture satisfies **100% strategy-purity intent** better than **100% trade-taking intent**.

Examples:
- A perfect H1 Re-Entry may be rejected because spread is too high.
- A valid REM may be rejected because prospective total risk exceeds the configured cap.
- A valid Re-Entry may be rejected because its calculated risk lot is below broker minimum.
- A source-valid decision may be rejected by `MinRRRatio` or `MaxSLPips` even though those thresholds are project safety policies, not Oma Ally setup rules.
- A later valid opposite cycle may be blocked from opening while an old opposite position remains open under TradeLockMode 1.

These are intentional execution-policy differences. They must not be hidden under a claim that "every official BBMA trade is always taken".

## Highest-purity concern
`MinRRRatio` and `MaxSLPips` are the two overlays most likely to be mistaken for strategy rules because they evaluate source-derived SL/TP geometry before entry. They must remain explicitly documented as **rejection-only EA policy** and must never feed back into M12–M16 signal validity, type, direction, priority, or source ownership.

No code removal is authorized by this audit alone because these controls were explicitly designed as EA-management/safety inputs. If the project mandate is later changed from "100% Oma Ally strategy with EA safety management" to "take every source-valid BBMA setup regardless of project risk filters", those inputs would need a separate policy decision.

## Wait/expiry purity check
Generic wait-bar inputs remain visible for compatibility, but canonical MHV/MLV has no strategy TTL and owner/cycle validity is structural. Any remaining generic expiry that can invalidate a source-valid Core owner solely because an arbitrary candle count elapsed must be treated as a future purity defect unless the active owner contract explicitly authorizes that expiry.

Current Core audits already moved MHV/MLV and key owner lifetimes away from arbitrary strategy TTL. Runtime/static follow-up should continue to verify that legacy `MaxWaitBars_*` fields do not silently regain final trading authority.

## Final result
### Strategy-Core purity
**STATIC PASS.** No active unauthorized foreign indicator/filter or arbitrary score authority is identified in the accepted M06–M17 signal path.

### Execution-policy purity
**PASS WITH DISCLOSURE.** M19–M22 and parts of M17 are deliberate EA-safety/broker overlays and can reject otherwise-valid BBMA decisions.

### Items to monitor
1. `MinRRRatio` must remain rejection-only EA policy.
2. `MaxSLPips` must remain rejection-only EA policy.
3. legacy `MaxWaitBars_*` must not become arbitrary Core owner expiry.
4. M18 score/tier fields must remain neutral/non-authoritative.
5. TradeLock/portfolio/risk gates must never feed back into strategy direction or signal ranking.

## Closure statement
The current EA is not found to contain an active unauthorized strategy enhancement such as RSI/ADX/AI scoring or non-BBMA trend logic. The remaining differences from a literal manual BBMA trader are downstream automation/risk/broker policies, not additions to the BBMA signal system. Runtime proof is still required before declaring end-to-end live purity fully verified.