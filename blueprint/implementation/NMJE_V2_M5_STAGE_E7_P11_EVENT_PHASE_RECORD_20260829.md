# NMJE v2 / M5 Stage-E7 P11 Event-Phase Lineage Record — 2026-08-29

## Scope

Classify an observed canonical parent journey as first event, same-journey
continuation/re-arm, genuinely new journey, or unresolved provenance. P11 is
identity metadata only and never prefers the newest or earliest event.

## Deterministic classification

- `UNRESOLVED`: no valid prior checkpoint, backward/equal-candle identity
  mismatch, or incomplete current Journey/Parent/D1 identity.
- `FIRST`: a later closed-M15 observation changes from a durable no-parent
  checkpoint to a complete canonical parent journey.
- `CONTINUATION`: a later closed-M15 observation has the exact same JourneyID,
  ParentEventID, and D1 canonical EventID as the prior checkpoint.
- `NEW_JOURNEY`: a later closed-M15 observation has a complete identity that
  differs from a prior complete parent journey.
- Same-candle replay restores the previously persisted phase only when all
  three identity hashes match exactly.

This avoids falsely labelling an already-active journey as first after restart.

## Durability and attribution

- A pair/strategy/instance checkpoint persists has-parent state, event phase,
  M15 update candle, JourneyID hash, ParentEventID hash, and D1 EventID hash.
- Checkpoint version is written last and incomplete/corrupt data fails closed.
- Phase and checkpoint durability freeze with each selected decision, persist
  under exact execution identity, survive recovery, and join closed outcomes.
- Attribution version 3 adds P11 while versions 1 and 2 remain readable with
  phase unresolved.
- Multiple trades per pair keep independent ticket/execution attribution even
  when they share the same journey.

## Authority boundary

- Event phase is absent from candidate creation, eligibility, comparison, M16
  authority, risk, lot sizing, OrderSend, lifecycle, D1TPW, and C044.
- No first-event preference, continuation rejection, newest/earliest bias,
  wait, cooldown, delay, score, or hard gate is introduced.
- M15 remains the sole final-decision clock; M22 remains OrderSend owner.
- NMJE execution authority, D1TPW, and C044 remain disabled.
- PR remains draft; no activation or merge authorization.

## Build and evidence

- Header: `Version 4.7.0 - NMJE v2 Event Phase Lineage`
- Property: `4.70`
- Full N3 and M5 Stage A-E7 regression/static suite PASS.
- Python compile and N3 static guard PASS.
- Native MT4 MetaEditor: `Result: 0 errors, 0 warnings, 487 msec elapsed`;
  EX4 refreshed at 592,386 bytes.

