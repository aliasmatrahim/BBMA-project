# T05 evaluator draft interface

Status HOLD / NOT VERIFIED. Coding continues with compile, regression and runtime tests deferred by user instruction. Candidate Build 6.17, revision `T05_SCHEDULER_SNAPSHOT_DISPATCH_001_20261112`.

## Scheduler delivery and binding

`ObserveCustomClosedBars` builds the owner frame, completes its batch successfully, then calls `DispatchCustomEvaluationSnapshot`. Priming/no-event batches and failed observations do not dispatch. The per-pair diagnostic result is cleared at the start of every observation and during pair initialization; a previous witness is never retained as the current result.

`CustomDispatch.mqh` requires the actual pair symbol, batch symbol, frame symbol and committed clock symbol to match the resolved custom universe. The clock must be idle with the same ticket and requested-TF watermarks. Each enabled slot emits BUY and SELL result rows; symbols outside its resolved scope receive `SLOT_SYMBOL_EXCLUDED` with an empty witness.

Configuration revision is the exact admitted payload, captured before observing the batch and compared against the current canonical serialization before and after evaluation. It includes the parsed slot formulas, slot IDs/enabled flags, use/availability matrix, resolved universe and resolved slot subsets. The existing short hash remains telemetry only. `BuildCustomResolvedConfigurationPayload` is shared by initialization and dispatch so the two paths cannot serialize different configuration definitions. Changed configuration requires successful initialization; dispatch does not re-admit it or grant availability.

`g_custom_evaluation_snapshots[pairIndex]` stores symbol, observation time, batch ticket, exact config revision and at most ten slot/direction results. Each result holds satisfied/reason and its witness. This is a transient diagnostic receipt, not a candidate queue, persistent reservation, M15 selection or entry approval. Future consumers must validate the whole receipt and its revision, not extract and reuse an unbound witness. No execution caller is connected.

## Fresh-event adapter

`CustomFreshEvents.mqh` is included through `CustomDispatch.mqh` after canonical owner types. Its `EvaluateCustomSlot(slot, batch, sourceFrame, direction, witness, reason)` wrapper builds normalized inputs and calls `EvaluateCustomSlotSnapshot`. Dispatch also rechecks canonical use-matrix admission before calling it.

The owner frame remains explicit because `CustomEventBatch` contains candle observations/events while immutable owner views live in `CustomOwnerFrame`.

M12 projection publishes `concreteSignal` from the actual `ReEntryData.Type` and `entryEventTime` from `ConfirmationCandle` after successful source export. The adapter resolves wildcard RE into RE1–RE4 and preserves opaque physical event IDs. Conflicting explicit subtypes fail closed.

A RE identity is fresh only when owner readability, structural validity, execution availability, entry eligibility and source entry window all pass. Confirmation must match the batch's latest closed candle, source EntryCandle must match currentOpen, and that TF event must have continuousBoundary. Repeated RE/wildcard views produce one fresh ID. Recovery-only views and priming batches produce no fresh identity.

Current producer projections still keep custom entry eligibility/execution availability closed. Fresh-event adapters for EXT/MHV/MLV/CSA/CSAK/MOM remain unimplemented pending their accepted source entry contracts. Scheduler wiring does not make these signals fresh.

## Evaluator

The evaluator consumes parsed AND/OR groups without calling detectors. It selects concrete components, requires simultaneous trigger eligibility with a fresh anchor, and publishes the witness atomically. OR ordering uses owner IDs; anchor ordering uses confirmation time, timeframe, concrete signal and owner ID. Simultaneous fresh alternatives are retained for later reservation. `CustomWitnessContainsSource` searches only selected components.

## Remaining work

- Define and bind non-RE source entry-event contracts, one signal at a time; retain unavailable rows until accepted.
- Bind transient T05 receipts into the T06 M15 authority/arbitration interface without changing the sole processing clock.
- Implement persistent dedup/reservation through T07 and fixed SL/TP source handling through T08.
- When validation resumes: native strict compile; exact-symbol/suffix and slot-exclusion cases; changed formula/matrix/subset/config revision; failed/priming/no-event/aborted/stale-ticket batches; pair/reinit isolation; RE subtype/freshness and cross-module regression; scheduler/runtime acceptance.

No compile or tests were run for Build 6.17. The candidate has not been deployed or merged. T04-B/E and T05 acceptance remain HOLD. Custom auto-entry remains OFF.
