# NMJE v2 / M5 Stage-C2 Shadow Classification Record — 2026-08-28

## Scope

Run the existing canonical BBMA Re-Entry and Extreme lifecycle engines against
the one fully closed M5 sample acquired by the M15 processing cycle. Bind the
selected context to the already-resolved NMJE parent and journey identities,
then expose the result as diagnostics only.

## Materialized state

- `PairState` owns independent M5 buy/sell Re-Entry and Extreme lifecycle state.
- Re-Entry has selection priority over Extreme; ambiguity fails closed.
- Context identity uses `M5CTX`, direction, stable family code, and event start.
- `ParentEventID` and `JourneyID` are copied only after the 4-TF parent resolves.
- Confirmed aligned Re-Entry maps to `ALIGNED`; candidate/same-direction and
  same-direction Extreme map to `SUPPORTING`.
- Opposite candidate Re-Entry maps to retracement `BUILDING`.
- Opposite confirmed Re-Entry or Extreme maps to temporary `CONFLICT` reason.

## Authority boundary

- M15 remains the sole processing and final decision clock.
- M5 does not enter combination collection, PriorityEngine, M16 invalidation,
  risk, preflight, ProcessEntry, OrderSend, D1TPW, or C044 owner paths.
- M5 does not create CSD, eCSD, CSM, MLV, candidates, rejections, rankings, or
  trade actions.
- `M5Refinement` cannot reject the sole valid M15 candidate.
- NMJE execution authority remains disabled; D1TPW and C044 remain disabled.

## Build and evidence target

- Header: `Version 4.6.3 - NMJE v2 M5 Shadow Classification`
- Property: `4.63`
- Required: Stage A/B/C1/C2, N3 epoch/authority/identity/recovery/replay/static,
  Python compile checks, and native MT4 MetaEditor `0 errors, 0 warnings`.
- PR remains draft; no activation or merge authorization.

