# NMJE v2 / M5 Accuracy Hardening Contract

Status: ISOLATED PREPARATION / SHADOW-ONLY / NO ACTIVATION  
Authority source: Issue #101  
Baseline: `D1 -> H4 -> H1 -> M15` locked at `3dd5245e5779b8e0b912010a3120370e609a4222`

## Objective

Improve trade accuracy through deterministic lineage, provenance stability, shadow attribution, and equal-eligibility arbitration. The workstream must not increase authority, create a broad hard signal filter, or reduce legitimate opportunity frequency without a later explicit strategy-policy decision and attributable evidence.

## Canonical hierarchy

`D1 -> H4 -> H1 -> M15 -> M5`

- D1: strategic owner.
- H4: higher owner and journey context.
- H1: setup context.
- M15: sole processing and final decision clock.
- M5: closed-candle lower-TF confirmation/refinement context only.

W1 is not implemented. M30 is excluded. M1 is excluded from primary NMJE authority.

## Authority firewall

M5 must not:

- create, reject, rank, execute, close, modify, or delete trades;
- become a second processing clock;
- override the sole valid M15 candidate;
- turn a temporary child conflict into an automatic higher-TF/M15 invalidation;
- introduce RSI, MACD, Stochastic, ADX, news/session, volatility, correlation, or ML signal logic.

M15/M16 remain final entry/revalidation authorities. M22 remains OrderSend owner. NMJE execution authority remains disabled.

## Deterministic lineage

Every applicable child must bind to immutable parent identity:

`M5 event -> M15 setup -> H1 journey -> H4 owner -> D1 owner epoch`

Required invariants:

- stable EventID / ParentEventID / JourneyID across ordinary candle refreshes;
- no silent child migration after a parent owner transition;
- restart/recovery restores the exact parent epoch or fails closed;
- D1 identity remains anchored to `EpochStartCandleTime`;
- first-event, continuation/re-arm, and genuinely new-journey identities remain distinguishable.

## Relationship model

Preserve canonical top-level relations:

- `BUILDING`
- `SUPPORTING`
- `ALIGNED`
- `CONFLICT`
- `UNRESOLVED`

Use deterministic `Reason` subtypes for temporary retracement, child conflict, parent conflict, owner transition, and true structural conflict. Hysteresis begins as provenance/state stability, not delayed entry or time-based suppression.

## Accuracy queue

Implementation order follows Issue #101:

1. P1 temporal lineage / epoch correctness.
2. P2 journey coherence tie-break metadata.
3. P3 M5 micro-context refinement.
4. P4 shadow challenger and exact outcome attribution.
5. P5 conflict classification.
6. P6 journey maturity metadata.
7. P7 structural density / sequence completeness.
8. P8 parent/child hysteresis and provenance stability.
9. P9 SL semantic-source audit.
10. P10 entry displacement telemetry.
11. P11 first-event / continuation-event lineage refinement.

P2, P6, and P7 may arbitrate only between two or more already-eligible candidates. They must not reject the sole valid candidate.

## Activation policy

All refinements begin as correctness, metadata, shadow, deterministic tests, or equal-eligibility tie-break work. Any hard rejection gate, eligible-trade reduction, M15 decision delay, or authority change requires a separate explicit strategy-policy approval plus attributable deterministic/static/backtest evidence.

## Current workstream state

`execution_policy = NONE`  
`automatic_policy_authorized = false`  
`m5_execution_authority = false`  
`m5_processing_clock_authority = false`  
`source_modification_authorized = stage_c2_shadow_classification`  
`activation_authorized = false`

Stage A contract and deterministic fixtures are complete. Stage B authorizes
only provenance structure, deterministic identity, and fail-closed lineage
validation helpers. It does not authorize M5 data collection, processing-loop
wiring, candidate influence, rejection, ranking, execution, or activation.

Stage C1 additionally authorizes acquisition of the latest fully closed M5
candle through the existing M15-driven `ProcessPair` cycle. It does not
authorize a second processing clock, candidate influence, or activation.

Stage C2 additionally authorizes canonical Re-Entry and Extreme detector state
on that frozen closed-M5 sample, deterministic `M5Refinement` lineage binding,
and shadow-only relation classification. It does not authorize M5 CSD/eCSD/CSM,
candidate creation, rejection, ranking, execution, persistence/recovery, D1TPW,
C044, or any decision-path influence.

