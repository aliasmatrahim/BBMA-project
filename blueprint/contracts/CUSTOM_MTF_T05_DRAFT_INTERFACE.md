# T05 evaluator draft interface

Status HOLD / NOT VERIFIED. Coding continues with compile, regression and runtime tests deferred by user instruction. Candidate Build 6.16, revision `T05_RE_FRESH_EVENT_ADAPTER_001_20261112`.

## Connected adapter

`CustomFreshEvents.mqh` is included by `BBMA_EA.mq4` after canonical owner types. Its `EvaluateCustomSlot(slot, batch, sourceFrame, direction, witness, reason)` wrapper builds normalized inputs and calls the existing `EvaluateCustomSlotSnapshot`.

The owner frame remains explicit because the current `CustomEventBatch` contains candle observations and events, while the immutable owner views live in a separate `CustomOwnerFrame`.

M12 projection now publishes `concreteSignal` from the actual `ReEntryData.Type` and `entryEventTime` from `ConfirmationCandle` after a successful source export. The adapter resolves a RE wildcard into RE1–RE4 using these fields. It preserves the opaque physical event ID. Conflicting explicit subtypes fail closed.

A RE identity is fresh only when owner readability, structural validity, execution availability, entry eligibility and the source entry window are all satisfied. The confirmation must match the batch's latest closed candle, the source EntryCandle must match currentOpen, and that TF event must have continuousBoundary. Repeated RE/wildcard views produce one fresh ID. Recovery-only views and priming batches produce no fresh identity.

The adapter preserves all owner availability flags. Current producer projections still keep custom entry eligibility/execution availability closed. Fresh-event adapters for EXT/MHV/MLV/CSA/CSAK/MOM remain pending their own accepted source entry contracts.

## Evaluator

The evaluator consumes the parsed AND/OR groups without calling detectors. It selects concrete components, requires simultaneous trigger eligibility with a fresh anchor, and publishes the witness atomically. OR ordering uses owner IDs; anchor ordering uses confirmation time, timeframe, concrete signal and owner ID. Simultaneous fresh alternatives are retained for later reservation. `CustomWitnessContainsSource` searches only selected components.

## Remaining work

- Bind the wrapper to the scheduler's slot symbol scope and validated configuration revision through the approved T04/T06 interfaces. No scheduler or execution caller invokes the new wrapper yet.
- Provide accepted non-RE freshness adapters while preserving unavailable rows.
- Implement persistent dedup/reservation through T07 and fixed SL/TP source handling through T08.
- Run native strict compile, wildcard/subtype/freshness harness cases, targeted regression and scheduler/runtime acceptance when validation resumes.

No compile or tests were run for Build 6.16. The candidate has not been deployed or merged. T04-B/E and T05 acceptance remain HOLD.
