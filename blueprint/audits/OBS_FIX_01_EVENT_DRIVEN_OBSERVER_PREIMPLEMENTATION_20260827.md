# OBS-FIX-01 — Event-Driven Runtime Observer Preimplementation Audit

Date: 2026-08-27  
Status: PREIMPLEMENTATION / ISOLATED / DO NOT DEPLOY DURING CURRENT R1  
Scope: observability tooling only

## 1. Safety boundary

This work is isolated on branch `obs-fix-01-event-driven-dev`, created from canonical `d1-owner-dev` head `d53bb6b5eb3627d44f737d5112b32a9f8b5d0d8b`.

The currently running R1 EA and Observer instance must not be replaced, restarted, reconfigured, or interrupted by this work. R1 Issue #96 remains the active broker-runtime evidence boundary.

`blueprint/source/BBMA_EA.mq4` is outside the permitted scope of OBS-FIX-01 preparation. No BBMA detection, candidate, confirmation, combination, validation, risk, execution, SL/TP, lot-sizing, lifecycle, or recovery authority may be changed here.

## 2. Problem confirmed

Observer v1.00 emits a full snapshot on every timer interval: environment, every relevant GlobalVariable, every exact-owned open order, recent owned order history, and a snapshot-end marker. With a short polling interval and a large history window, unchanged state is repeatedly reprinted and the MT4 Experts tab becomes difficult to use for runtime evidence collection.

OBS-FIX-01 changes the emission model, not the observation authority:

- polling remains timer-based;
- default output becomes event-only / silent when unchanged;
- identical consecutive observer records are suppressed;
- verbose repeated polling output is explicit opt-in;
- initial history detail replay is explicit opt-in;
- order/GV/environment/history transitions remain attributable.

## 3. Observer visibility boundary

The standalone Observer can directly inspect only terminal-visible state available to it, including:

- terminal connection / trade-allowed environment;
- relevant terminal GlobalVariables for the selected StrategyID/InstanceID namespace;
- exact-owned live BUY/SELL orders in the MT4 trade pool;
- exact-owned closed BUY/SELL orders in the selected history window.

The Observer does **not** have direct access to private in-memory EA objects such as an unexported candidate, internal setup-completion state, or a rejected/validated decision unless the EA already exposes that event through terminal-visible state or its own logging.

Therefore OBS-FIX-01 must never fabricate internal EA decision/setup events. Existing EA execution-critical logs remain the authority for decision-final, validation/rejection, execution-attempt/result, lifecycle, and recovery events that are not externally observable by the standalone Observer.

Adding new EA-source telemetry solely to satisfy the Observer is explicitly out of scope while R1 evidence is being collected.

## 4. Prepared v1.10 behaviour

Default inputs are prepared as:

- `ObserverDebugLevel=0` — event-only emission;
- `EmitInitialHistoryDetails=false` — do not replay historical detail at startup;
- `SnapshotSeconds` remains polling cadence, but unchanged polls are silent.

Prepared state caches track:

- environment signature;
- sorted relevant-GV records;
- sorted open-order records;
- sorted recent-history records;
- last printed observer record.

Prepared event markers include:

- `START`
- `ENV`
- `GV_CHANGE` and changed/new `GV` records
- `OPEN_CHANGE` and changed/new `OPEN` records
- `HIST_CHANGE` and newly attributable `HIST` records
- `BASELINE_END`
- `CHANGE_END`
- `POLL_END` only in verbose mode
- `STOP`

No broker-write API is permitted.

## 5. Important history semantics

History is a rolling-window observation surface. A record can disappear because it aged outside `HistoryLookbackHours`; that is not a new trade event.

Accordingly:

- startup history detail is suppressed by default;
- a history-set size/signature change may be summarized;
- only newly present/changed history records are emitted as detailed `HIST` events after baseline;
- disappearance caused by rolling-window expiry must not be described as a broker close event.

## 6. Acceptance matrix

| ID | Case | Expected result | Evidence class |
|---|---|---|---|
| OBS-00 | unchanged state across repeated timer polls | no new observer output in default event-only mode | runtime |
| OBS-01 | connection or trade-allowed state changes | one attributable `ENV` transition plus change boundary | runtime |
| OBS-02 | relevant GV added or value changes | `GV_CHANGE` plus only new/changed GV detail | runtime |
| OBS-03 | relevant GV removed | count/signature change visible without invented value detail | runtime |
| OBS-04 | exact-owned order opens | `OPEN_CHANGE` plus one attributable order detail including ticket/pair/type/magic/open/SL/TP/lots/comment | runtime |
| OBS-05 | live owned order geometry/comment changes | changed `OPEN` record emitted once | runtime |
| OBS-06 | owned order closes | live pool change plus newly attributable history detail after close reaches history pool | runtime |
| OBS-07 | history record ages outside lookback | history-set change may be summarized; no fabricated close event | runtime |
| OBS-08 | identical consecutive observer record | duplicate suppressed | static + runtime |
| OBS-09 | `ObserverDebugLevel>0` | poll diagnostics may repeat deliberately and `POLL_END` identifies unchanged poll | runtime |
| OBS-10 | startup with existing history | summary baseline only by default; detail only if explicitly enabled | runtime |
| OBS-11 | OnTick activity | no observer logging or polling from `OnTick()` | static + runtime |
| OBS-12 | broker-write surface | no `OrderSend`, `OrderClose`, `OrderModify`, or `OrderDelete` in Observer | static |
| OBS-13 | current live R1 session | no replacement/restart/reconfiguration caused by this branch | governance |
| OBS-14 | native MetaEditor compile | 0 errors / 0 warnings before any future deployment | native |
| OBS-15 | EA-internal decision/setup state not externally exported | Observer remains silent rather than inventing an event; EA logs remain authority | architecture/runtime |

## 7. Verification gates

Before any future Observer replacement is considered:

1. static OBS-FIX-01 guard must pass;
2. source diff must remain Observer/test/audit/workflow only and exclude `blueprint/source/BBMA_EA.mq4`;
3. native MetaEditor compile must be 0 errors / 0 warnings;
4. event-only runtime cases OBS-00..OBS-12 and OBS-15 must be attributable;
5. current R1 evidence must first be preserved and its freeze boundary explicitly released;
6. no existing R1 evidence may be invalidated by changing Observer mid-run.

Until these gates are met, this branch is PREPARED ONLY / DO NOT DEPLOY / DO NOT MERGE TO CANONICAL.
