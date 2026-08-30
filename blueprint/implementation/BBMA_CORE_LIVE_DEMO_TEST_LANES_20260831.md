# BBMA Core Live/Demo Test Lanes — 2026-08-31

Status: **PREPARED / DEMO OBSERVATION FIRST / NO LIVE-MONEY OR EXECUTION ACTIVATION**

## Fixed safety boundary

- Use a dedicated demo account and isolated terminal/profile only.
- Production/live-money accounts are prohibited.
- `EnableD1TPWLifecycle=false` and `EnableC044Lifecycle=false` remain mandatory.
- NMJE/M5 remains shadow metadata with no selection, rejection, sizing,
  execution, or close authority.
- W1, M30 and primary M1 remain excluded. No daily-loss gate is introduced;
  same-currency exposure control and cooldown remain KIV only.
- An observation run must not create, modify or close an order. Any broker
  action requires a separate activation branch, visible build increment,
  minimum-lot plan and explicit user approval.

## Lane A — EA-only immediate checks

These checks test the EA itself. They do not require a BBMA setup or signal.

1. Bind branch, commit, source/EX4 hashes, visible build, account mode, server,
   symbol mapping and input fingerprint.
2. Confirm exact pair resolution, broker specification, digits, point, tick
   size, stop/freeze levels and current spread.
3. Confirm D1, H4, H1 and M15 history availability and fail-closed behavior for
   missing or stale history.
4. Confirm initialization, dashboard/log health, Global Variable namespace and
   one closed-M15 scheduler cycle without an order action.
5. Restart with zero open orders and prove clean initialization without phantom
   recovery, duplicate registry rows or lifecycle resurrection.
6. Measure cycle runtime, log growth and terminal stability for at least two
   M15 closes. This waits for clock time, not for a BBMA signal.

Expected duration after terminal setup: immediate through 30 minutes.

## Lane B — Connected-market observation checks

These require demo connectivity and live ticks, but not a canonical BBMA signal.
Order authority remains off.

1. Observe tick flow, spread changes, history refresh and broker specification
   stability during normal market operation.
2. Confirm closed-candle ownership across D1/H4/H1/M15 and the existing M15
   processing clock; M5 is sampled only as NMJE shadow evidence.
3. Observe reconnect and terminal restart with no open order; ambiguity or
   incomplete history must fail closed.
4. Preserve Experts/Journal logs at session transitions, spread expansion or
   a natural disconnect when those events occur.

Expected duration: 30 minutes to one market session. Session/disconnect evidence
may take longer, but does not block Lane A acceptance.

## Lane C — Signal-dependent shadow checks

These must wait for organic BBMA structure. They cannot be forced or replaced
with a manual order.

1. Capture D1 owner epoch, H4 journey, H1 setup and M15 decision lineage.
2. Record accepted and rejected candidates, invalidation reason, semantic
   SL/TP source, displacement, maturity, conflict, density, stability and event
   phase.
3. Compare the canonical M15 decision with NMJE/M5 shadow classification.
4. Record frequency, coverage and uncertainty without changing selection or
   execution behavior.

Expected duration: several sessions to multiple weeks. Absence of a signal is
`WAITING_FOR_ORGANIC_SIGNAL`, not PASS or FAIL.

## Lane D — Organic demo-execution checks

This lane is **not authorized by this document**. It requires an organic signal
plus a separate activation branch/build and explicit user approval immediately
before order authority is enabled.

- One approved pair, one position, minimum valid fixed lot and dedicated IDs.
- Prove M17 geometry, M21 sizing, M19/M20 guards, sole M22 `OrderSend`, broker
  acknowledgement, durable identity and hard-SL protection.
- D1TPW restart/close-idempotency verification is a later sub-lane and may take
  days because both an organic D1 Extreme TPW decision and a qualifying fully
  closed D1 candle are required.
- NMJE execution authority and C044 remain off throughout D1TPW verification.

## Lane E — Controlled resilience tests

Digits, tick size, stop/freeze level, invalid price, spread expansion, requote,
disconnect, partial history and duplicate-action prevention should first use
offline fixtures or Strategy Tester evidence. A connected-demo fault test that
could send, modify or close an order belongs to Lane D and needs its approval.

## Result separation

Each result must be one of:

- `PASS` — all evidence for that exact lane/check is complete;
- `FAIL_CLOSED` — unsafe or ambiguous state was rejected without broker action;
- `INCONCLUSIVE` — the run started but evidence was incomplete;
- `WAITING_FOR_SETUP` — terminal/account/history preparation is incomplete; or
- `WAITING_FOR_ORGANIC_SIGNAL` — Lane C/D structure has not occurred.

Lane A/B evidence must never be delayed or re-labelled merely because Lane C/D
has no signal. Conversely, Lane A/B PASS cannot authorize Lane D.

