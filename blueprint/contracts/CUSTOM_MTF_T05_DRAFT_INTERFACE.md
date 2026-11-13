# T05 evaluator draft interface

Status HOLD / NOT VERIFIED. Coding continues with compile, regression and runtime tests deferred by user instruction. Candidate Build 6.20, revision `T05_M10_MOM_FRESH_CANDLE_EVENT_001_20261113`.

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


## Setup-formation event: MHV/MLV (one M09 owner)

Source route: `SOURCE_INDEX → accepted Core section 6 → Finale master MHV/MLV rules + PDF-derived pages 7–8 → F1 MHV/MLV lifecycle decision → current M09 owner`.

Accepted semantics treat MHV and MLV as aliases for one canonical same-timeframe/cycle M09 lifecycle. MHV/MLV is setup/context, not standalone direct-entry authority. The physical formation event is the first valid closed move-away candle that establishes `MLV_FORMATION_ESTABLISHED` and freezes the marked body. The existing owner sets `ConfirmationCandleTime` to that candle; `ExportSourceMHVSignal` preserves it as the confirmation timestamp. A later retest is a separate optional lifecycle transition, not a second formation event. REM's M15 component maturity remains formation-established plus frozen body; its standalone policy is unchanged.

The read-only adapter now declares a fresh formation event only when the projected owner is the same M09 owner, state is exactly `MLV_FORMATION_ESTABLISHED`, confirmation equals the latest closed source bar, and the same-timeframe scheduler batch records that closed bar plus its actual following open across a continuous boundary. It rejects recovery-only views, stale formation timestamps and later retest/direction states. MHV/MLV alias views retain the same opaque owner event ID, so duplicate projections deduplicate.

Mapping classification: the lifecycle event timestamp and frozen-body state come from the accepted F1 project mapping. Tying that closed event to the actual next observed open/continuous scheduler boundary is an engineering mapping; it is not claimed as founder-quoted timing. No calculated future open, generic TTL, new detector or separate MHV/MLV owner is added.

This is a **setup-formation receipt**, not an `entryEventTime`. It does not set `entryEligible`, `entryWindowOpen` or `executionAvailable`. `CustomViewCurrent` therefore continues to fail closed for MHV/MLV Trigger use while availability is OFF; the receipt alone cannot produce a trigger witness, T06 selection or entry. All 77 availability cells and custom auto-entry remain OFF. M09 source-epoch/recovery acceptance remains HOLD under SIG-06/T04-E evidence.



## Fresh-event audit: CSA/CSAK — HOLD

Source route: `SOURCE_INDEX → accepted Core §7 / M10 close-only user decision → Finale V05/V06 direction rules + primary PDF pp.7–8 → M10 contract and SIG-02/SIG-03 acceptance → current M10 snapshots and custom projection`. The registered Forex Factory forum set is supplemental and supplies no authoritative CSA/CSAK event-window rule.

The direction predicates are already resolved:
- CSA = valid closed Close strictly beyond MidBB in the requested direction.
- CSAK = valid closed Close strictly beyond the relevant MA5/MA10 pair and MidBB.
- Open is not a predicate; equality fails. CSA is not an alias for MA-only eCSD, and CSAK maps to the strong CSD predicate.

SIG-02/SIG-03 accept these as bounded M10 read-only snapshots. `ReadCustomOwnerView` projects them with source-bar identity and an observation `eventId` containing that candle time. The projection is `recoveryOnly=true`; it does not set entry eligibility, entry window or execution availability. Existing acceptance explicitly leaves physical trigger reservation/dedup to T05–T07.

**No fresh executable event boundary is accepted.** The close-only user decision says a repeated matching observation must not become a fresh executable event solely because the predicate remains true, and it does not define a prior-cross edge, first-event reset, generic TTL or expiry. Treating each new closed bar with the same true predicate as a fresh event would therefore invent repeat-trigger semantics; using a first false-to-true transition would invent an unapproved event edge. The per-candle observation ID and a continuous scheduler boundary alone do not resolve that choice.

Classification: **HOLD / UNRESOLVED — event freshness and consumption contract only.** The CSA/CSAK predicates and read-only snapshot owner are accepted; this is not a formula conflict or an Open ambiguity. Do not add a `CustomFreshCSA[K]Event` adapter or make either signal Trigger-eligible until an already-authorized event lifecycle/consumption contract defines what constitutes a new event. Do not add a previous-bar cross, reset, expiry or TTL as a substitute. Current availability and custom auto-entry stay OFF.



## Fresh-event adapter: MOM (read-only momentum-candle receipt)

Source route: `SOURCE_INDEX → accepted Core §4 → primary PDF pp.2/5 + secondary PDF p.18 → Finale V02 rules 001–005 → M10 source contract and SIG-04 acceptance → current M10 snapshot/custom projection`.

The accepted M10 predicate remains a valid closed candle beyond the relevant outer BB with expanding width and directional Mid/outer BB movement. The source describes a momentum candle or candles; the M10 owner evaluates and identifies each closed source candle separately. `ReadCustomOwnerView` already carries the exact source bar in both `confirmation` and its opaque `eventId` (`symbol|MOM|TF|direction|sourceBar`).

The read-only adapter now declares a fresh MOM candle receipt only when the current owner view is readable and direction-valid, `confirmation == sourceBar`, and the scheduler batch has the same timeframe/closed source bar plus the actual observed next open across a continuous boundary. A repeated read of the same source candle keeps the same event ID; a later qualifying closed momentum candle has its own source-bar identity. This is a per-candle engineering mapping of the source's “momentum candle(s)” wording, not a founder-quoted trigger timing rule. It adds no run-start edge, reset, fixed-time calculation or TTL.

This receipt preserves the M10 projection's `recoveryOnly=true` and `executionAvailable=false`. It does not set `entryEventTime`, `entryEligible` or `entryWindowOpen`. `CustomViewCurrent` still blocks MOM Context/Trigger evaluation while those gates are closed; receipt creation alone cannot produce a witness, T06 selection or entry. Persistent event reservation/consumption remains T07 work; T05 deduplicates identical event IDs only within the current frame. All 77 availability cells and custom auto-entry remain OFF.


## Entry-event adapter: RE (existing)

M12 projection publishes concrete RE subtype and `ConfirmationCandle`. The adapter resolves RE wildcard into RE1–RE4 and preserves the opaque physical event ID. It currently declares fresh RE only when existing source window and availability/eligibility gates pass; those availability flags remain closed on current projections.

## Still pending

- CSA/CSAK predicates and read-only snapshots are accepted, but fresh-event identity/consumption remains HOLD as recorded above; both Trigger paths remain unavailable. MOM has a read-only per-candle receipt but no Context/Trigger authority. MHV/MLV formation receipts do not make MHV/MLV Trigger eligible.
- Bind transient T05 receipts into T06 M15 authority/arbitration. Keep canonical M15 cadence/signatures and D1/H4 owner gates.
- Implement persistent dedup/reservation through T07 and fixed SL/TP source handling through T08.
- When validation resumes: native strict compile; EXT raw/reversal/retest-ready/stale/recovery boundaries; RE subtype cases; simultaneous batch and exact next-open cases; symbol/config binding; cross-module regression and scheduler runtime.

No compile, regression or runtime checks were run for Build 6.20 under the user-directed HOLD. The candidate has not been deployed or merged. T04-B/E and T05 acceptance remain HOLD. Custom auto-entry remains OFF.
