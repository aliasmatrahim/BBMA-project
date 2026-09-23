# Q10 Hybrid Acceptance Decision — Historical Tester Then Live Reconfirmation

Date: 2026-09-23
Issue: #109
Baseline: `d1-owner-dev@5aebad7c744d32c9e5de5c5b7b3d484b40e43846`
Candidate: Build 5.11 / `V511_EVENT_DRIVEN_OBSERVER_20260922`

## Decision

The user explicitly directed Q10 to use **both** historical Strategy Tester evidence and MetaQuotes-Demo runtime evidence, with **live demo placed last for reconfirmation**.

This decision supersedes the earlier Q10 restriction that every mandatory R3-R6 case had to be positively observed in broker/demo runtime before later historical coverage work could proceed.

It does not change any BBMA Strategy Core rule, detector, selector, validator, risk/MM rule, execution rule, lifecycle rule or EA source behavior.

## Two-phase authority

### Phase H — Historical coverage

Use the exact frozen Build 5.11 candidate in the already-verified engineering Strategy Tester environment to:

- find rare market-state scenarios without waiting for them to occur live;
- verify deterministic Strategy/Core/state chronology;
- verify closed-candle behavior;
- verify structural SL calculations, frozen-snapshot arithmetic, TradeLock/risk logic and fail-closed paths where the tester exposes the required inputs;
- verify deterministic identity/hash/N1/N2/N3 invariants where broker-specific facts are not required;
- reuse already-VERIFIED Build 5.11 historical logs before starting any new tester run.

Phase H may advance across R3-R6 independently of the live Q10 state machine.

Historical evidence remains labelled:

`ENGINEERING HISTORICAL EVIDENCE / NOT FINAL TICK-ACCURATE`.

It must not be relabelled as live broker evidence.

### Phase L — Final live reconfirmation

MetaQuotes-Demo remains the last authority for cases whose PASS condition materially depends on:

- authenticated broker/demo session identity;
- actual broker ticket or OrderOpenTime;
- server-side accepted/rejected order geometry;
- live spread/stop/freeze behavior;
- persisted live ticket recovery across restart;
- broker comment replacement/blank behavior;
- actual broker history/outcome reconciliation;
- other behavior that Strategy Tester cannot faithfully prove.

The existing live state machine remains:

`AUTH -> R3 -> R4 -> R5 -> R6`.

It is not weakened or bypassed by Phase H.

## Final PASS rule

Q10 can reach final PASS only when:

1. all mandatory historical-required cases are positively covered with exact Build 5.11 evidence, subject to existing conditional/safety exceptions;
2. no historical case is FAIL;
3. all mandatory live-only cases and selected live-reconfirm cases are positively demonstrated on attributable MetaQuotes-Demo evidence, subject to existing conditional/safety exceptions in the matrix;
4. historical and live evidence do not contradict each other;
5. exact source/EX4/settings identity remains bound throughout.

If live evidence contradicts tester evidence, the live contradiction is not overwritten. The result is FAIL or VERIFICATION REQUIRED until resolved.

## Case authority

Machine-readable authority is defined in:

`blueprint/runtime/q10_demo_acceptance/FINAL_BUILD511_HYBRID_EVIDENCE_POLICY.json`.

Each case has one primary closure authority:

- `historical_required_cases` for deterministic Strategy/Core/state coverage; or
- `live_only_cases` for broker/runtime-dependent behavior.

A selected subset of historical cases is additionally listed in `live_reconfirm_cases`. Those cases are deliberately repeated after Phase H so the final MetaQuotes-Demo phase reconfirms representative stage behavior without waiting for every rare historical state to recur live.

This classification changes **evidence authority and sequencing only**. It does not alter the case PASS/FAIL semantics in the existing R3-R6 matrix.

## Safety

- no optimization/filter/rule tuning from historical performance;
- no live account;
- no manufactured broker loss or unsafe emergency action;
- no tester result may claim broker-specific facts it cannot observe;
- no later phase may silently erase an earlier FAIL;
- primary MT4 remains outside Q10 dedicated-terminal control.
