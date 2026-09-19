# NMJE v2 / M5 Accuracy Hardening Contract — Current Owner

Status: **Q9 ISOLATED / PROVENANCE-FIRST / SHADOW-ONLY / NO ACTIVATION**
Authority: Issue #101 + active M12N/N3 contracts
Baseline: `d1-owner-dev@01f7e8305f6ba558494fc559bb3c734dfc06124a`, Build `4.86`

## Objective

Improve deterministic lineage and future M5 context accuracy without creating a new BBMA strategy rule or changing existing candidate eligibility.

Canonical hierarchy:

`D1 -> H4 -> H1 -> M15 -> M5`

- D1 = strategic owner.
- H4 = structural/journey context.
- H1 = setup context.
- M15 = sole processing and final decision clock.
- M5 = future closed-candle refinement/context only.

## Authority firewall

NMJE/M5 must not:
- create a signal or candidate;
- reject the sole valid M15 candidate;
- independently rank or delay candidates;
- become a second processing clock;
- risk-approve or execute;
- alter M13 REM/RRE/REE signatures;
- redefine M11/M15/M16/M17/M22 ownership;
- add RSI, MACD, Stochastic, ADX, news/session, volatility/correlation, ML or other non-BBMA signal logic.

Current execution policy:

`execution_policy = NONE`
`automatic_policy_authorized = false`
`m5_execution_authority = false`
`m5_processing_clock_authority = false`
`activation_authorized = false`

## P1 — temporal lineage / epoch correctness

Every applicable observed event must have deterministic provenance. The target lineage is:

`M5 event -> M15 event -> H1 event -> H4/D1 parent -> D1 owner epoch`

P1 rules:
- identity is metadata only;
- identity inputs come only from existing canonical owner provenance;
- no wall-clock/random/market-snapshot value may be introduced solely to generate an ID;
- Re-Entry identity uses its source-owned start/type/direction/timeframe;
- Extreme identity uses its source-owned RAW anchor;
- MHV/MLV identity uses its source-owned parent provenance;
- H4 owner identity uses its source-owned owner anchor;
- D1 owner identity uses an epoch anchor that does not rotate on an ordinary same-owner snapshot refresh;
- when exact lineage cannot be proven, context must remain unresolved rather than inventing a parent.

P1 does not authorize M5 observation yet. It only establishes the identity substrate needed before M5 can be safely attached.

## P2–P11 boundary

P2 journey coherence, P3 M5 micro-context, P4 outcome attribution, P5 conflict subtype, P6 maturity, P7 structural density, P8 hysteresis, P9 SL semantic-source audit, P10 displacement telemetry and P11 first/continuation lineage remain downstream.

Any step that can change eligible-trade count, delay an otherwise executable M15 decision, or change execution authority requires a separate explicit strategy-policy decision and attributable evidence.

## Validation

Each source-bearing Q9 stage requires:
- unique build/header identity;
- read-only NMJE authority tests;
- identity-domain and replay/provenance tests;
- protected M13/M15/M16/M17/M22 surface audit;
- native MT4 MetaEditor 0E/0W;
- runtime evidence where the stage introduces runtime-populated metadata.

No PASS claim may substitute static evidence for native compile/runtime evidence.
