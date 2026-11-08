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
