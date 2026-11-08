# Custom closed-bar observation and owner projections — Build 5.97

Scope: T04 observation milestone. This is not the completed custom producer, selection or execution pipeline.

## Event kernel

M27 calls the custom observer after any canonical ProcessPair refresh for that symbol. It also calls the observer when no new M15 candle exists and for custom-only states. Existing M15 final authority is unchanged; observation creates no candidate or order.

The clock takes actual broker bar timestamps and quote time. It never derives a candle by rounding wall time and never reads bar-zero prices for signal decisions. Current-bar open time is continuity metadata only. Requested TFs must have positive closed/current open timestamps with a nominally closed candle and a quote in the current actual bar. This is bar-identity readiness; indicator warm-up remains M06's is_valid/is_closed owner-data contract.

First observation, newly requested TF and symbol-key change prime watermarks without emitting historical triggers. Changed closed identities are emitted once in D1/H4/H1/M30/M15/M5/M1 order. Begin/Complete uses a ticket, pending symbol and busy guard; aborted observations do not consume watermarks, and stale completion tickets cannot commit another batch. Time rollback rejects without advancing state. Missing bar history or quote leaves the observation WAIT.

`continuousBoundary` is conservative engineering continuity metadata: the previous observed current bar must become the closed bar, and its nominal period end must equal the new actual open. Gaps/weekends/DST boundaries can make it false. It is neither a BBMA expiry/TTL nor execution authority. Owner entry windows and recovery replay remain separate source-owned work. Observation watermarks are not physical trigger reservations or consumed-order identity.

## Canonical owner views

Read-only adapters project the existing M12 confirmed-ReEntry exporter and M08 reversal-confirmed Extreme exporter. They select existing D1/H4/H1/M15 slots. Native targeted owner assertions currently use H1; coverage of each remaining slot/TF still needs its acceptance evidence. No detector, lifecycle updater, M12N authority, ranking or risk calculation is called by these adapters.

A view requires matching symbol/pair index, direction, timeframe, positive expected closed-bar identity, ready closed M06 data and a matching owner update watermark. Re-Entry subtype selection is preserved; RAW Extreme does not become a mature component. Stable context-owner identities retain canonical formation/confirmation metadata rather than the batch receipt time. They are not yet execution dedup anchor IDs.

All views explicitly keep entryEligible=false and executionAvailable=false. Structural validity is copied through canonical exporters; it can outlive EntryCandle metadata without a generic TTL. This does not verify a live entry-window gate. The separately routed PR #301 remains open/unmerged at recovery and is not silently adopted here.

M1/M5/M30 producer slots and custom adapters for MOM/CSA/CSAK/MHV/MLV remain unavailable in this milestone. Unsupported rows return a reason; they never become Valid/entry-ready merely because syntax parsing succeeds. The existing canonical producers remain authoritative and unchanged.

## Publication and limits

A mapped symbol's nonempty event batch publishes a bounded read-only owner frame. Failed quote/history observation hides the frame; duplicate tick/timer observations do not relabel its timestamp. All semantic input availability cells remain closed and all custom slots default OFF. Native integration tests use bar/quote fixtures and prevalidated owner snapshots and do not invoke the trading controller.

This milestone has no seven-TF owner advancement, formula witness evaluation, trigger reservation, runtime order proof, timer-housekeeping parity or multi-symbol broker-execution acceptance. Full T04 requires per-TF owner producer expansion/recovery/availability evidence before T05+ can use executable views.

## Build 5.98 — auxiliary producer and diagnostic-window addendum

This addendum supersedes the earlier statement that every custom view is projection-only. M27 may now advance symbol-local M1/M5/M30 RE and Extreme lifecycle slots through the existing M06 `GetDataForTimeframe`, M08 `DetectExtreme`/`UpdateExtremeLifecycle`/opposite supersession, and M12 `UpdateReEntryState`. There is one lifecycle slot per symbol/direction/TF. Existing D1/H4/H1/M15 producers are not called again here. The M5 data snapshot is shared with existing M06/NMJE consumers; NMJE observation cadence and authority remain unchanged.

Auxiliary production is requested only for enabled RE/RE1–4/EXT rows. The actual latest closed identity is required. A per-slot watermark prevents repeat advancement. The readiness adapter requires valid closed data, positive finite indicators, positive OHLC/point, ordered nonzero BB width and at least 51 bars behind the snapshot index for EMA50/previous-bar dependencies. This is an **engineering data-readiness bound**, not a BBMA signal threshold or coverage certification. Missing data does not publish a current frame or consume the batch; successfully advanced source owners can be reused on retry without repeat advancement.

A skipped nominal source candle sets `recoveryRequired`; no structural owner is invalidated/expired because of the gap. Its view stays unavailable (`WAIT_OWNER_RECOVERY`) until a future source-owned replay/recovery implementation is verified. This deliberately includes weekend/session/DST gaps. A cold snapshot does not certify historical owner reconstruction. These are remaining T04 recovery limitations; no execution availability is granted.

The auxiliary reader projects RE/RE1–4 and mature EXT from those slots. MHV and MLV on M15 project **the same canonical M09 owner/exporter**, with one context identity and separate requested labels. No M09 detector is added; other-TF MHV/MLV remain unavailable. Custom-only symbols still lack canonical D1/H4/H1/M15 producer advancement and therefore do not acquire those owners by allocation alone. MOM/CSA/CSAK remain unwired.

`entryWindowOpen` is a read-only RE diagnostic. Accepted Core §8.6 and the separately reviewed PR301 establish the next-source-candle mapping: valid confirmed owner, positive confirmation/EntryCandle, `EntryCandle == ConfirmationCandle + source period`, and actual current source-bar open equal to EntryCandle. Bar-zero **prices** are not read. Late/missing windows do not mutate structural validity. The additional metadata consistency check is a fail-closed engineering guard. This does not modify the canonical `BuildConfirmedReEntryCandidate`, merge PR301, enable a custom candidate, or prove broker order timing. `entryEligible` and `executionAvailable` remain false everywhere; every semantic input availability cell remains false.

Native producer acceptance calls actual M06/M08/M12 in an isolated tester; selector and MHV projections also use explicitly initialized owner fixtures. No trading controller is invoked by these harnesses. The M30 test history is an explicitly derived **OHLC fixture** from complete 30-M1-bar buckets in existing unit history, with incomplete buckets omitted and source/output hashes recorded. It is not raw tick data, market coverage evidence, or a P&L test. The discovered archived M30 file ended in June and was rejected for the August fixture.

## Build 5.99 — anchored contiguous-history replay

This addendum replaces the blanket sticky hold for missed **observations** when available source history proves a contiguous interval from an existing auxiliary owner watermark. It does not certify cold-start owner reconstruction or market/session coverage.

`ReadCustomAuxClosedData` owns the existing auxiliary readiness adapter. `AdvanceCustomAuxLifecycle` calls the same M08/M12 engines for ordinary advancement and replay. There is no second detector/lifecycle implementation. `ReplayCustomAuxOwnerSource` requires exact existing anchor and target timestamps, checks child-owner watermarks do not exceed the anchor, and processes closed source candles oldest to newest. Every nominal intervening candle must be present and M06-ready. Missing anchors, unready history, rollback, and unresolved weekend/session/DST gaps remain unavailable; there is no calendar assumption, bar synthesis, structural expiry or owner reset.

Work is limited to 256 replay bars per observer pass. This is an **engineering work bound**, not signal age/expiry. A validated chunk commits atomically, retains `recoveryRequired` and hides its views until the latest observation is reached. A failed chunk publishes none of its staged lifecycle/data changes. Later passes continue from the last committed exact source watermark. This keeps long replay work from repeatedly blocking one event. Full timer/protection responsiveness under backlog still requires runtime validation.

Cold snapshots and the final replayed source identity are marked `contextOnlyThrough`; their views set `recoveryOnly=true` and `entryWindowOpen=false`. Duplicate reads retain that marking. A subsequent genuinely new source candle is processed normally; all execution/eligibility flags remain false regardless. Future T05/T06/T07 must reject a recovery-only view as a physical fresh trigger, even if it is structurally useful context. No historical replay is an order reservation or execution event.

M5 data remains the shared M06 snapshot. A partial replay can temporarily hold an older M5 snapshot, but custom views remain unavailable and the canonical M15 path refreshes M5 before its existing read-only NMJE observation. No NMJE callback or trade controller is added to replay. D1/H4/H1/M15 producers, selection, risk, order management and canonical PR301 dependency are unchanged.

Acceptance compares every declared scalar field of both RE and Extreme directional owners against the same native source engines fed the same closed candles one by one, for M1/M5/M30. It separately checks duplicate handling, context-only marking, resumption, invalid provenance/anchor, bounded chunks and unavailable warm-up. M30 still uses the declared Build5.98 derived OHLC fixture. This is native replay/helper evidence, not full custom-order, live reinit, cold-start recovery, session-gap resolution or multi-symbol broker execution evidence.
