# T05 evaluator draft interface

Status HOLD / NOT VERIFIED. Coding continues with compile, regression and runtime tests deferred by user instruction. Candidate Build 6.18, revision `T05_EXT_FRESH_ENTRY_EVENT_001_20261113`.

## Scheduler delivery and binding

`ObserveCustomClosedBars` builds the owner frame, completes its batch successfully, then calls `DispatchCustomEvaluationSnapshot`. Priming/no-event batches and failed observations do not dispatch. The per-pair diagnostic result is cleared at the start of every observation and during pair initialization; a previous witness is never retained as the current result.

`CustomDispatch.mqh` requires the actual pair/batch/frame/clock symbols and committed clock ticket/watermarks to match. Each enabled slot emits BUY and SELL result rows; symbols outside its resolved scope receive `SLOT_SYMBOL_EXCLUDED` with an empty witness.

Configuration revision is the exact admitted payload, captured before observing the batch and compared against the current canonical serialization before and after evaluation. It includes parsed slot formulas, slot IDs/enabled flags, the use/availability matrix, resolved universe and resolved slot subsets. The short hash remains telemetry only. `BuildCustomResolvedConfigurationPayload` is shared by initialization and dispatch so both paths use the same serializer. Changed configuration requires successful initialization; dispatch does not re-admit it or grant availability.

`g_custom_evaluation_snapshots[pairIndex]` stores symbol, observation time, batch ticket, exact config revision and at most ten slot/direction results. Each result holds satisfied/reason and its witness. This is a transient diagnostic receipt, not a candidate queue, reservation, M15 selection or entry approval. Future consumers must validate the whole receipt and its revision. No execution caller is connected.

## Entry-event contract: EXT

Source route: SOURCE_INDEX → accepted Core section 5 / F2 maturity decision → M08 source contract → approved Custom MTF v1 signal registry → current M08 owner. Accepted Core distinguishes RAW, REVERSAL_CONFIRMED and RETEST/ENTRY_READY. EXT as Context may use reversal-confirmed owner state. EXT as Trigger requires exact RETEST/ENTRY_READY; RAW and reversal-only are rejected.

The owner remains the only detector/lifecycle. `ProjectCustomExtremeView` now exposes the existing `RetestCompletionCandleTime` as `entryEventTime`, while preserving the reversal `confirmation` field and stable lifecycle `eventId`. Fresh EXT requires this completion time to equal the batch's latest closed source candle, the M08 state to equal `EXT_MAT_RETEST_READY`, the following actual source bar to be open, and the scheduler event to be a continuous boundary. It uses the observed `currentOpen`; it does not calculate the next open by fixed seconds or introduce a TTL. A stale RETEST_READY owner stays available for Context only and is not a fresh Trigger.

Mapping classification: the RETEST_READY requirement is accepted source/project policy. Emitting its close as the physical trigger event and limiting the event to the next observed continuous source candle is the minimal closed-bar engineering mapping for the custom scheduler. It is not claimed as verbatim founder timing. The canonical standalone Extreme execution/SLTP contract remains H1/Entry Mode 2; this projection does not extend that canonical policy. M15 remains final custom authority at T06.

The physical fresh EXT identity reuses the opaque M08 lifecycle ID: one lifecycle can complete its retest only once; the identity includes symbol, TF, direction, raw candle and reversal confirmation. The explicit retest timestamp is checked separately against the batch. This event declaration does not set `executionAvailable`; the existing owner projections leave it false and all custom signal×TF availability cells remain closed. Therefore a fresh event record cannot by itself produce a usable Trigger witness or an entry.

## Entry-event adapter: RE (existing)

M12 projection publishes concrete RE subtype and `ConfirmationCandle`. The adapter resolves RE wildcard into RE1–RE4 and preserves the opaque physical event ID. It currently declares fresh RE only when existing source window and availability/eligibility gates pass; those availability flags remain closed on current projections.

## Still pending

- Fresh events for MHV/MLV, CSA/CSAK and MOM; keep each unavailable until its source entry-event contract is mapped and accepted.
- Bind transient T05 receipts into T06 M15 authority/arbitration. Keep canonical M15 cadence/signatures and D1/H4 owner gates.
- Implement persistent dedup/reservation through T07 and fixed SL/TP source handling through T08.
- When validation resumes: native strict compile; EXT raw/reversal/retest-ready/stale/recovery boundaries; RE subtype cases; simultaneous batch and exact next-open cases; symbol/config binding; cross-module regression and scheduler runtime.

No compile or tests were run for Build 6.18. The candidate has not been deployed or merged. T04-B/E and T05 acceptance remain HOLD. Custom auto-entry remains OFF.
