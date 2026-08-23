# F7 Re-Entry Lifecycle Execution Contract

Status: **CANONICAL / IMPLEMENTATION-READY SPECIFICATION — CODE CHANGE DEFERRED UNTIL P3 RUNTIME FREEZE CLOSES**

Date: 2026-08-24

## 1. Purpose

This contract is the single implementation-facing consolidation of the accepted CORE-V2-F7 Path-A decisions for executable Re-Entry-owned trades.

It supersedes the old assumption that every executable Re-Entry-owned position must carry a static outer-BB broker TP. It does **not** alter the currently frozen P3 EA source. The current build remains the runtime-evidence candidate until P3 Step 5 closes.

The accepted source/spec chain is:

`Re-Entry -> Momentum/CSM -> later Re-Entry -> Momentum/CSM -> ... -> opposite Extreme / cycle restart`

with the direct Home Course lifecycle rule:

`Re-Entry -> no Momentum -> TP / close / rotation`

The exact engineering state-machine, persistence, replay and broker-idempotency mappings below are project implementation mappings of those accepted semantics, not claims of verbatim Oma Ally Boolean formulas.

## 2. Covered executable decision types and lifecycle owner

| Executable decision | Lifecycle owner | Owner timeframe |
|---|---|---:|
| standalone `SIGNAL_RE_ENTRY` | H1 Re-Entry | H1 |
| `SIGNAL_REM` | H4 Re-Entry | H4 |
| `SIGNAL_RRE` | D1 Re-Entry | D1 |
| `SIGNAL_REE` | D1 Re-Entry | D1 |

Lower-timeframe supporting components may participate in setup construction/validation but are not direct broker-close owners of a higher-timeframe parent position.

The original owner Re-Entry candle identity is immutable entry provenance. Later owner-timeframe Re-Entries may re-arm lifecycle management but do not replace the original trade provenance.

## 3. Initial broker payload

For all currently executable Re-Entry-owned trades under strict Path A:

- `EntryPrice` = approved live execution reference;
- `StopLoss` = non-zero protective hard SL under `EA_SAFETY`;
- `TakeProfit` = `0.0`;
- static TP policy = **ABSENT BY DESIGN**;
- exit policy = **BBMA RE-ENTRY LIFECYCLE**;
- `MinRRRatio` = structurally bypassed/inactive for these decisions;
- `MaxSLPips` remains an EA safety rejection cap on the protective SL;
- no synthetic/static reward distance is manufactured.

`TP == 0.0` is valid only when an explicit lifecycle/no-static-TP policy marker is present. A zero TP without that policy marker remains invalid/ambiguous and must fail closed.

The current exact hard-SL mapping remains:
- BUY -> exact owner Re-Entry source-candle LOW minus one broker point;
- SELL -> exact owner Re-Entry source-candle HIGH plus one broker point.

Classification: **EA_SAFETY**. The source contains limited Extreme-context wick-stop support, but the exact owner-Re-Entry-candle mapping and one-point buffer are project engineering protection and are not universal BBMA Core SL formulas.

## 4. Required decision / trade metadata

### 4.1 Decision payload

Future decision payload must carry explicitly:
- `ExitPolicy = REENTRY_LIFECYCLE` or equivalent;
- `HasStaticTakeProfit = false`;
- `LifecycleOwnerType = SIGNAL_RE_ENTRY`;
- exact `LifecycleOwnerTimeframe`;
- exact `OriginalOwnerReEntryCandleTime`;
- verified owner-cycle identity/provenance (`CycleStartTime` or equivalent);
- protective-stop source component identity.

The old `SLTPSourceComponent` name may be retained temporarily for compatibility, but implementation/documentation must no longer imply that it also proves a static TP.

### 4.2 Per-ticket lifecycle state

Minimum persistent per-ticket metadata:
- `ExecutionHash`;
- broker ticket;
- pair + magic + direction;
- signal type;
- lifecycle/no-static-TP policy marker;
- lifecycle owner type/timeframe;
- `OriginalOwnerReEntryCandleTime`;
- owner-cycle identity/provenance;
- `LifecycleState`;
- `ActiveEpochReEntryCandleTime`;
- `LastProcessedOwnerCandleTime`;
- `LifecycleStateEventCandleTime`;
- `ExitReason` when latched;
- actual broker `OrderOpenTime()`.

Original entry provenance is immutable. `ActiveEpochReEntryCandleTime` is mutable and advances when a later owner Re-Entry re-arms the held position.

## 5. Canonical lifecycle states

Use the minimum durable state model:

- `LIFE_NONE` — no authorized F7 lifecycle identity;
- `LIFE_MOMENTUM_PENDING` — valid owner Re-Entry epoch exists; waiting for continuation/failure evidence;
- `LIFE_WAIT_NEXT_REENTRY` — same-direction owner-TF Momentum/CSM succeeded; hold and wait for the next valid same-direction owner Re-Entry;
- `LIFE_EXIT_LATCHED` — an authorized lifecycle close event has occurred and remains immutable until broker closure is reconciled.

`MOMENTUM_CONFIRMED` may be retained as event/diagnostic wording, but the durable post-success state is `LIFE_WAIT_NEXT_REENTRY` because that is the next source-owned expectation.

## 6. Event ownership and precedence

M23/M24 must consume source-owned events. They must not implement duplicate BBMA detectors.

Event owners:
- M10 -> canonical same/opposite CSM/Momentum;
- M12 -> valid same-direction owner-timeframe Re-Entry;
- M08/F2 -> owner-timeframe opposite Extreme maturity / reversal confirmation;
- M20 -> emergency close request.

For each new fully closed owner-timeframe candle, after M20 emergency precedence and provided no exit is already latched, apply:

1. **owner-TF opposite `REVERSAL-CONFIRMED EXTREME`** -> `LIFE_EXIT_LATCHED / EXIT_CYCLE_SUPERSEDED` from any ordinary state;
2. if `LIFE_MOMENTUM_PENDING`:
   - source-valid opposite CSM -> `LIFE_EXIT_LATCHED / EXIT_OPPOSITE_CSM`;
   - source-valid same-direction CSM -> `LIFE_WAIT_NEXT_REENTRY`;
   - otherwise first approved reverse-direction confirmation candle -> `LIFE_EXIT_LATCHED / EXIT_NO_MOMENTUM_REVERSE`;
   - otherwise remain pending;
3. if `LIFE_WAIT_NEXT_REENTRY`:
   - valid same-direction owner-TF Re-Entry -> set `ActiveEpochReEntryCandleTime` to that confirmation candle and return to `LIFE_MOMENTUM_PENDING`;
   - ordinary reverse candle, neutral candle, further same-direction CSM, outer-BB reach, or elapsed time -> HOLD / remain waiting.

The Re-Entry validation candle itself is never evaluated as its own post-Re-Entry no-Momentum failure candle.

No fixed candle count, timer, pip threshold, ATR/ADX rule, session expiry, trailing stop, breakeven, TP2 or TP3 is introduced.

## 7. Reverse-confirmation mapping while pending

The accepted minimum deterministic mapping remains:
- BUY position -> reverse confirmation candle is bearish: `Close < Open`;
- SELL position -> reverse confirmation candle is bullish: `Close > Open`.

This reverse-colour mapping applies only inside an active `LIFE_MOMENTUM_PENDING` epoch and only before same-direction CSM has succeeded in that epoch.

A normal reverse candle while `LIFE_WAIT_NEXT_REENTRY` is **not** a close command.

## 8. Re-arm contract

After same-direction Momentum:

`LIFE_WAIT_NEXT_REENTRY -> later valid same-direction owner-TF Re-Entry -> LIFE_MOMENTUM_PENDING`

Re-arm rules:
- standalone H1 position -> next valid H1 Re-Entry;
- REM -> next valid H4 Re-Entry;
- RRE -> next valid D1 Re-Entry;
- REE -> next valid D1 Re-Entry;
- a new full REM/RRE/REE combination is not required merely to manage the existing position;
- the same owner Re-Entry event may re-arm several still-open same-direction tickets from the same surviving owner cycle;
- re-arm does not itself authorize a new broker order; new entries remain owned by M13/M14/M15/M16/M17/M19/M20/M22.

## 9. Final cycle exit

Raw opposite Extreme is a new-cycle candidate only.

The final old-cycle close boundary is:

`OPPOSITE REVERSAL-CONFIRMED EXTREME ON THE LIFECYCLE-OWNER TIMEFRAME`

Transition:

`any ordinary lifecycle state -> EXIT_CYCLE_SUPERSEDED -> LIFE_EXIT_LATCHED`

Owner timeframe:
- H1 standalone Re-Entry -> H1 Extreme lifecycle;
- REM -> H4 Extreme lifecycle;
- RRE -> D1 Extreme lifecycle;
- REE -> D1 Extreme lifecycle.

This final close is based on the already accepted F1/F2 cycle-supersession boundary. Lower-timeframe Extremes do not directly close the higher-timeframe parent position.

Outside an active pending epoch, `any opposite CSM -> close` is **not** promoted into a universal extra exit rule. An impossible chronological sequence that appears to produce such a conflict must fail frozen / emit diagnostics rather than create a new strategy rule.

## 10. D1 Extreme support dependency

RRE/REE final-cycle exit requires D1 Extreme lifecycle state that does not exist in the frozen code.

Implementation must add D1 BUY/SELL `ExtremeLifecycleData` using the existing M08/F2 Extreme lifecycle semantics. This is support-state only:
- D1 RAW Extreme -> candidate only;
- D1 reversal-confirmed opposite Extreme -> cycle-supersession event;
- adding D1 lifecycle tracking does **not** enable standalone D1 Extreme entries.

Canonical implementation specification:
`blueprint/contracts/M08_D1_EXTREME_LIFECYCLE_SUPPORT_SPEC.md`.

## 11. M22 pre-send persistence and crash window

Because a targetless trade depends on durable lifecycle identity, the execution hash alone is insufficient if owner metadata is lost immediately after broker acceptance.

Before `OrderSend()`, M22 must persist a **PREPARED lifecycle intent record** keyed by the expected `SHORT_HASH(DecisionID)` containing only immutable upstream-approved metadata:
- execution hash;
- pair/magic/direction/signal type;
- exit policy / no-static-TP flag;
- owner timeframe;
- original owner Re-Entry candle;
- owner-cycle provenance;
- protective SL;
- schema/version + committed marker.

M22 does not invent these values; it only persists the upstream payload.

After a confirmed broker ticket, or after M24 later reconciles an ambiguous accepted order by the same execution hash, bind:
- ticket;
- actual `OrderOpenTime()`;
- actual broker Entry/SL/TP/lot;
- initial `LIFE_MOMENTUM_PENDING` state;

and promote the record to **OPEN_COMMITTED**.

If the send definitely failed and no live/history order with that hash exists, the PREPARED record may be safely retired. If the send result is ambiguous, retain PREPARED for M24 reconciliation; do not resend blindly.

This two-phase checkpoint is engineering reliability, not BBMA strategy semantics.

## 12. M22 broker execution contract

For explicit `REENTRY_LIFECYCLE` decisions:
- protective `SL > 0` required;
- `TP == 0.0` allowed and expected;
- negative TP invalid;
- positive TP in lifecycle/no-static-TP mode is payload inconsistency and fails closed;
- M22 never manufactures a TP;
- execution deviation, stable `BBMA|H:` identity, retry, ambiguous-result reconciliation, trade-lock and frozen-lot rules remain unchanged.

Legacy/static-target positions from older builds must not be silently converted into the new lifecycle policy merely because a newer EA version is attached.

## 13. M23 close idempotency

Once an exit is authorized:
- set `LIFE_EXIT_LATCHED`;
- persist immutable `ExitReason` and trigger owner-candle time before/with the close attempt;
- close the full current broker `OrderLots()` only;
- before each attempt, reselect exact ticket and verify exact symbol + magic + expected direction + live status;
- BUY closes using current BID; SELL using current ASK;
- if the order is already closed, treat the latch as satisfied; do not call `OrderClose()` again;
- after an ambiguous/failing close result, reselect/reconcile broker truth;
- if still live and error is retryable, keep the same exit latch and retry later;
- never replace the original exit reason/candle with later signals;
- M20 emergency liquidation has higher operational precedence and may satisfy the close first.

No partial close, breakeven migration or trailing stop is permitted.

## 14. M24 recovery and replay

M24 remains recovery infrastructure. It must not invent BBMA events.

Recovery sequence for a live exact-owned order:
1. verify symbol + magic + market-order type + live ticket;
2. recover `BBMA|H:<execution hash>`;
3. load committed PREPARED/OPEN lifecycle identity by hash;
4. verify signal type, direction, owner TF, owner Re-Entry candle and exit policy;
5. accept targetless geometry only for explicit lifecycle mode: BUY `SL < Entry && TP == 0`, SELL `SL > Entry && TP == 0`;
6. reconstruct lifecycle chronologically from the open boundary using the same source-owned event semantics;
7. if enough evidence cannot be proven, freeze ordinary lifecycle while preserving M19/M20 accounting and emergency close authority.

Replay start boundary:
- candle is strictly later than the active epoch's Re-Entry validation candle; and
- for the first epoch, candle must fully close after actual broker `OrderOpenTime()`.

Replay must reproduce all repeated epochs:

`PENDING -> CSM -> WAIT_NEXT_REENTRY -> Re-Entry -> PENDING -> ...`

and the owner-TF opposite reversal-confirmed Extreme final supersession.

M24 must reuse/replay canonical M08/M10/M12 semantics through a single owner-event interface/state replay. It must not create independent simplified Re-Entry/CSM/Extreme formulas.

If required source history is unavailable, use a lifecycle-frozen recovery classification/diagnostic such as `LIFECYCLE_HISTORY_INSUFFICIENT`; do not infer a static TP or guessed state.

## 15. Legacy-position migration guard

A position opened under an earlier static-TP build is not automatically an F7 lifecycle position.

Lifecycle management requires positive proof of the explicit F7 exit-policy identity/checkpoint. Without that proof:
- preserve broker Entry/SL/TP/lot;
- include in risk/emergency accounting;
- do not remove its existing TP;
- do not apply F7 ordinary lifecycle closes;
- keep it in the appropriate legacy/degraded/frozen recovery classification until naturally closed or explicitly migrated by a separately approved policy.

This prevents a new build from changing the management contract of already-open older trades silently.

## 16. Module ownership summary

- **M08/F2**: Extreme maturity/cycle boundary, including new D1 support.
- **M10**: CSM/Momentum producer.
- **M12**: Re-Entry producer.
- **M13/M14/M15/M16**: combination/selection/validity and immutable owner component preservation.
- **M17**: protective payload + lifecycle owner validation; no static Re-Entry TP.
- **M21**: lot from Entry/SL; unchanged.
- **M19**: risk/exposure from Entry/SL/lot; unchanged.
- **M20**: portfolio/emergency decision; highest operational close precedence.
- **M22**: dumb broker executor + durable prepared/open lifecycle identity persistence; TP=0 allowed only in explicit lifecycle mode.
- **M23**: per-ticket recurring lifecycle reducer + idempotent full broker close.
- **M24**: restart reconciliation/replay/fail-frozen recovery.
- **M27/M15 orchestration**: remains the sole processing clock; owner-TF state advances only when a new closed owner-TF candle is observed.

## 17. Implementation order after P3 runtime freeze

1. add/lock F7 payload and lifecycle enums/fields;
2. implement D1 Extreme lifecycle support;
3. redesign M17 protective/no-static-TP validation and disable MinRR for current executable lifecycle types;
4. implement M22 TP=0 path + PREPARED/OPEN lifecycle checkpoint;
5. implement M23 recurring reducer + exit latch + idempotent close;
6. implement M24 targetless geometry + repeated-epoch replay + lifecycle-frozen recovery;
7. recheck M19/M20/M21 invariants;
8. update dashboard/diagnostics only as required to expose lifecycle/recovery state;
9. assign a new unique left-aligned EA build/header identifier;
10. native MetaEditor compile 0 errors / 0 warnings;
11. static cross-module + Strategy-Core purity audit;
12. fresh runtime validation.

## 18. Minimum runtime acceptance matrix

Must include:
- TP=0 order acceptance with non-zero hard SL;
- initial Re-Entry -> same-direction CSM -> wait/hold;
- wait -> later owner Re-Entry -> re-arm;
- re-armed pending -> no Momentum + reverse confirmation -> close;
- pending -> opposite CSM -> close;
- repeated Momentum/Re-Entry epochs;
- opposite reversal-confirmed Extreme -> cycle-supersession close;
- REM H4 lifecycle owner;
- RRE/REE D1 owner + D1 Extreme lifecycle;
- restart in PENDING;
- restart in WAIT_NEXT_REENTRY;
- restart after re-arm;
- restart with EXIT_LATCHED;
- crash/ambiguous send between PREPARED and OPEN_COMMITTED reconciliation;
- lifecycle history insufficient -> ordinary lifecycle frozen, emergency still active;
- duplicate-close/idempotency behavior;
- M20 emergency-close precedence;
- legacy positive-TP position is not silently migrated.

## 19. Final canonical rule

For current executable Re-Entry-owned trades under Path A:

`BROKER PAYLOAD = ENTRY + PROTECTIVE EA_SAFETY SL + TP 0`

`POSITION LIFECYCLE = RE-ENTRY EPOCH -> MOMENTUM?`

- no Momentum + reverse confirmation -> close;
- opposite CSM while pending -> close;
- Momentum -> hold / wait next owner Re-Entry;
- next owner Re-Entry -> re-arm the same held position;
- opposite reversal-confirmed Extreme on owner TF -> old-cycle supersession -> close;
- broker hard SL / M20 emergency may close first.

This contract contains no universal static Re-Entry outer-BB TP, no numeric MinRR gate for current lifecycle trades, no fixed timeout, no lower-timeframe direct-close authority, and no unsupported management feature.
