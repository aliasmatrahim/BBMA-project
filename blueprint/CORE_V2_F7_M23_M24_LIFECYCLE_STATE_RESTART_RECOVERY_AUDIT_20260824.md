# CORE-V2-F7 — M23/M24 Lifecycle State + Restart Recovery Contract Audit

Date: 2026-08-24  
Branch: `blueprint-dev`  
Scope: minimum lifecycle state, restart reconstruction, owner-candle idempotency, and broker `OrderClose()` idempotency for Path-A Re-Entry-owned trades  
Status: **AUDIT COMPLETE — MINIMUM STATE / REPLAY / CLOSE-IDEMPOTENCY CONTRACT RESOLVED FOR THE CURRENT INITIAL POST-RE-ENTRY BRANCH; POST-MOMENTUM RE-ARM / FINAL EXIT SEMANTICS REMAIN HOLD; NO EA CODE CHANGE WHILE P3 CANDIDATE IS FROZEN**

---

## 1. Question

For future strict-Path-A lifecycle-managed positions, determine:

1. the minimum state that must survive restart;
2. how `MOMENTUM_PENDING` / `MOMENTUM_CONFIRMED` must be rebuilt without fabricating BBMA semantics;
3. which owner candle is the idempotency boundary;
4. how M23 may execute and retry `OrderClose()` without double-closing;
5. how degraded or incomplete recovery must fail safely.

This audit is architecture / recovery engineering. It does **not** change the currently frozen P3 EA source.

---

## 2. Mandatory preflight and evidence boundary

Applied project order:

`Original evidence -> canonical Strategy Core -> accepted F7 decisions -> live contracts -> current code -> recovery design`

Checked live governance/state:
- `PROJECT_INSTRUCTIONS.md`;
- `docs/references/SOURCE_INDEX.md`;
- `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`;
- `blueprint/CURRENT.md`;
- `blueprint/MASTER_QUEUE.md`;
- M10, M12, M23 and M24 contracts;
- active `blueprint/source/BBMA_EA.mq4`.

Accepted F7 inputs to this audit:
- deterministic no-Momentum event audit;
- combination lifecycle-owner audit;
- static TP vs lifecycle-exit audit;
- MinRR/protective-payload audit.

Strategy semantics used here are already source-reconciled:
- Re-Entry expects Momentum/CSM continuation;
- initial failure is not elapsed-time based;
- before same-direction Momentum is confirmed, the first later reverse-confirmation candle on the owner timeframe confirms no-Momentum failure;
- owner timeframe is H1 for standalone H1 Re-Entry, H4 for REM, D1 for RRE, D1 for REE;
- current Path-A Re-Entry trades have no mandatory static broker TP;
- M10 remains the sole canonical CSM/Momentum producer.

Persistence format, checkpoint atomicity, replay mechanics and broker-close reconciliation below are **EA engineering mappings**, not claimed BBMA/Oma Ally rules.

---

## 3. Current architecture gap

### 3.1 `TradeInfo` has no lifecycle identity/state

Current `TradeInfo` contains broker/order fields, `decision_id`, `execution_hash`, `sequence_hash_short` and recovery state, but no:
- lifecycle owner timeframe;
- owner Re-Entry candle identity;
- lifecycle state;
- last processed owner candle;
- exit-trigger reason/candle.

Therefore M23 cannot currently execute the accepted F7 lifecycle without either inventing identity or adding explicit metadata.

### 3.2 Current M23 has no ordinary strategy close path

Current `ManagePositions()`:
- synchronizes broker state;
- executes M20 emergency close;
- freezes corrupted / invalid / missing-execution-hash positions;
- otherwise performs no normal lifecycle close.

This is correct for the frozen P3 candidate, but it is incomplete for the future F7 lifecycle design.

### 3.3 Current M24 is not targetless-lifecycle aware

Current recovery validates `Entry + SL + positive TP` geometry and has no owner-TF lifecycle replay.

The previous F7 protective-payload audit already established that a future targetless Re-Entry position (`TP == 0`) must not be classified invalid merely because TP is absent.

### 3.4 Existing execution hash remains valuable

M24 already treats:

`BBMA|H:<SHORT_HASH(DecisionID)>`

as the restart-stable execution identity and refuses to fabricate full `DecisionID` when only the hash survives.

This remains the correct lifecycle registry key. Full `DecisionID` is not required for the new M23 close state machine.

---

## 4. Minimum lifecycle state model

### LS-01 — Lifecycle states

**RESOLVED.**

Minimum ordinary lifecycle states required for the currently resolved F7 branch:

- `LIFE_NONE` — no authorized lifecycle identity / not lifecycle-managed;
- `LIFE_MOMENTUM_PENDING` — position is open and no same-direction owner-TF CSM has yet confirmed continuation;
- `LIFE_MOMENTUM_CONFIRMED` — a later same-direction owner-TF source-valid CSM has confirmed continuation;
- `LIFE_EXIT_LATCHED` — an approved close event has already occurred and must remain latched until broker closure is reconciled.

A separate persistent `LIFE_CLOSED` state is optional, not required for broker correctness, because broker history + execution tombstone already prove that the ticket is no longer live. A short-lived in-memory closed state may still be useful for diagnostics before registry compaction.

### LS-02 — Initial state

**RESOLVED.**

Immediately after a lifecycle-managed Re-Entry-owned order is confirmed open by the broker:

`LifecycleState = LIFE_MOMENTUM_PENDING`

The Re-Entry validation candle itself must not be evaluated as a post-entry failure candle.

### LS-03 — State transition while pending

For each **new fully closed owner-timeframe candle after the position actually opened**:

1. if source-valid **same-direction CSM** exists under M10 -> `LIFE_MOMENTUM_CONFIRMED`;
2. else if the first later approved reverse-confirmation candle exists -> `LIFE_EXIT_LATCHED` with reason `EXIT_NO_MOMENTUM_REVERSE`;
3. if a source-valid opposite CSM occurs while the initial pending branch is still active -> `LIFE_EXIT_LATCHED` with reason `EXIT_OPPOSITE_CSM` under the already accepted F7 pending-state invalidation rule;
4. otherwise remain `LIFE_MOMENTUM_PENDING`.

Precedence on one owner candle:
- canonical CSM classification is evaluated before the simple reverse-colour test;
- therefore a candle that is a same-direction source-valid CSM is continuation evidence and is not simultaneously treated as the weaker no-Momentum reverse event;
- opposite CSM is a stronger invalidation event.

No fixed candle count, timer, pip threshold, ATR, ADX or session expiry is introduced.

### LS-04 — `MOMENTUM_CONFIRMED` is not a license to invent a later exit

**NEW MATERIAL GAP FOUND.**

The prior F7 deterministic audit explicitly closes the **initial post-Re-Entry no-Momentum window** once same-direction Momentum is confirmed and says the lifecycle then proceeds through normal `Momentum -> further Re-Entry` progression.

The current source/audit set does **not yet provide a fully reconciled deterministic rule for what the already-open position does after `LIFE_MOMENTUM_CONFIRMED`**, specifically:
- whether a later same-owner Re-Entry re-arms that position into a new `MOMENTUM_PENDING` epoch;
- whether only the newly added position, if any, gets the new pending epoch;
- whether a simple later reverse candle can close the original position after confirmed Momentum;
- whether opposite CSM alone is sufficient after Momentum has already been confirmed, or whether a later cycle event / opposite Extreme is required.

Therefore M23/M24 may safely implement/recover the state `LIFE_MOMENTUM_CONFIRMED`, but **must not invent a post-confirmation ordinary close transition until a separate source reconciliation resolves it**.

This is now a **HOLD / REQUIRED FOLLOW-UP** before the targetless lifecycle design can be considered production-complete.

---

## 5. Minimum immutable lifecycle identity

### LS-05 — Required immutable identity per open trade

**RESOLVED.**

A future lifecycle-managed `TradeInfo` / durable checkpoint needs, at minimum:

1. `ExecutionHash` — canonical restart key already used by M24;
2. broker `Ticket` — live broker object identity;
3. `SignalType` — `RE_ENTRY`, `REM`, `RRE`, or `REE`;
4. `Direction` — BUY/SELL;
5. explicit `ExitPolicy` / `LifecycleManaged=true` marker, so `TP==0` cannot be mistaken for missing TP;
6. `LifecycleOwnerType = SIGNAL_RE_ENTRY`;
7. `LifecycleOwnerTimeframe`;
8. exact `LifecycleOwnerReEntryCandleTime`;
9. current `LifecycleState`;
10. `LastProcessedOwnerCandleTime`;
11. `LifecycleStateEventCandleTime` — CSM candle when confirmed, or exit-trigger candle when latched;
12. `ExitReason` when `LIFE_EXIT_LATCHED`.

Broker truth remains authoritative for pair, magic, open/closed status, Entry, SL, TP and live lot. Those need not become an independent strategy source merely because they may also be cached.

### LS-06 — Owner mapping

The immutable owner mapping is:

| Executable type | Lifecycle owner TF |
|---|---|
| standalone H1 `RE_ENTRY` | H1 |
| `REM` | H4 |
| `RRE` | D1 |
| `REE` | D1 |

The exact owner Re-Entry candle identity must be preserved from the selected/validated source component. It must not be reconstructed later merely from component order or the current chart.

### LS-07 — Full `DecisionID` is not required for lifecycle recovery

**RESOLVED.**

The lifecycle can remain restart-safe using the stable execution hash plus verified owner metadata. M24 must continue its existing rule:

> do not fabricate a full `DecisionID` from lossy broker comments.

---

## 6. Persistence contract

### LS-08 — Durable checkpoint keyed by execution hash

**RESOLVED AS ENGINEERING POLICY.**

The lifecycle record must be persisted under the stable execution hash, not under mutable array index or chart-local state.

The existing MT4 GlobalVariable mechanism is a suitable implementation option because the project already uses it for owner checkpoints, but the exact storage backend is not a BBMA rule.

If GlobalVariables are used, persistence should be transaction-like:
1. write all required fields under a schema/versioned execution-hash key;
2. write a final `READY/COMMIT` marker last;
3. flush;
4. recovery accepts the checkpoint only if the commit marker and all mandatory fields are present and internally consistent.

This prevents a terminal crash during a multi-field write from turning a partial checkpoint into false lifecycle authority.

### LS-09 — Checkpoint is cache/provenance, not unquestioned truth

**RESOLVED.**

A persisted state must be verified against:
- exact live broker ownership;
- execution hash;
- trade direction;
- allowed owner timeframe for the signal type;
- existence of the exact owner Re-Entry candle as a historical closed candle;
- available closed owner-TF history.

Where enough history exists, deterministic replay is authoritative over a stale cached state.

---

## 7. Restart reconstruction algorithm

### RR-01 — Live-order discovery

On restart M24 first applies its existing exact-ownership rules:
- market order only;
- exact configured symbol;
- exact configured pair magic;
- live order state.

Then:
- valid `H:` execution hash -> eligible for lifecycle identity lookup;
- missing `H:` -> preserve current `REC_IDENTITY_MISSING_FROZEN` behavior: risk/emergency visibility remains, ordinary lifecycle is frozen.

### RR-02 — Lifecycle identity load

For an exact-owned live order with valid execution hash:

1. load the committed lifecycle checkpoint keyed by the hash;
2. verify ticket/signal type/direction/exit-policy/owner-TF/owner-candle consistency;
3. verify that owner timeframe matches the accepted mapping for the executable signal type;
4. verify that the owner Re-Entry candle exists exactly and is closed.

If this minimum identity cannot be proven, do **not** guess from current price, MA state, signal type heuristics or present chart structure.

Result:

`REC_LIFECYCLE_IDENTITY_MISSING_FROZEN` conceptually (or an extension of the existing frozen recovery classification).

Emergency close remains available; ordinary M23 lifecycle close remains frozen.

### RR-03 — Replay start boundary

**RESOLVED.**

Replay begins from the first owner-timeframe candle satisfying both:
- it is strictly later than the owner Re-Entry validation candle; and
- it fully closed after the actual broker `OrderOpenTime()`.

This prevents:
- the validation candle being misread as post-entry failure;
- historical candles that occurred before the actual broker fill from altering the position lifecycle.

Only fully closed owner-TF candles are replayed.

### RR-04 — Deterministic replay

Start reconstructed state at:

`LIFE_MOMENTUM_PENDING`

Then replay eligible owner-TF candles chronologically using the same live-state reducer:

- call/reuse canonical M10 historical CSM semantics; M24 must not create a second momentum formula;
- same-direction CSM while pending -> `MOMENTUM_CONFIRMED`;
- approved reverse confirmation before same-direction CSM -> `EXIT_LATCHED`;
- approved opposite CSM while the initial pending branch is active -> `EXIT_LATCHED`;
- neutral/non-CSM candle -> no state transition.

`LastProcessedOwnerCandleTime` becomes the latest replayed candle.

The recovered result must equal the result that uninterrupted runtime would have produced from the same closed-candle sequence.

### RR-05 — History insufficiency

**RESOLVED FAIL-SAFE.**

If the required closed owner-TF history from the post-open boundary to the current point is not available, M24 cannot prove that no earlier exit event was missed.

Therefore it must not trust a later `MOMENTUM_CONFIRMED` or no-Momentum state solely because a checkpoint says so.

Required behavior:
- preserve broker Entry/SL/TP/lot;
- retain M19/M20 exposure accounting;
- retain M20 emergency-close authority;
- freeze ordinary lifecycle;
- expose a recovery diagnostic such as `LIFECYCLE_HISTORY_INSUFFICIENT`;
- do not fabricate a static TP or lifecycle result.

### RR-06 — Recovery of an already-latched exit

If replay reaches an exit event while the broker order is still live:

`LifecycleState = LIFE_EXIT_LATCHED`

with immutable:
- exit reason;
- trigger owner candle time.

M23 may then resume closing the live order. It must not wait for a new signal/candle merely because the terminal restarted.

### RR-07 — Order already closed while terminal was down

If no live order remains but broker history contains the ticket / execution hash:
- rebuild the execution tombstone as M24 already does;
- do not recreate a monitored open position;
- do not issue `OrderClose()`;
- lifecycle checkpoint may be marked/compacted as historical after reconciliation.

---

## 8. Live owner-candle idempotency

### ID-01 — One reducer pass per owner candle

**RESOLVED.**

M15 remains the sole orchestration clock. It may notice that a new H1/H4/D1 closed candle has become available, but lifecycle state changes only once per unique:

`ExecutionHash + LifecycleOwnerTimeframe + OwnerCandleTime`

`LastProcessedOwnerCandleTime` is the per-position idempotency boundary.

Repeated M15 scans/ticks seeing the same owner candle must not:
- re-transition state;
- create another exit intent;
- duplicate lifecycle logs;
- reset the exit event candle.

### ID-02 — Exit intent is immutable once latched

When an approved exit event occurs, persist:
- `LifecycleState = LIFE_EXIT_LATCHED`;
- `ExitReason`;
- `LifecycleStateEventCandleTime`.

Until the broker order is confirmed closed, later candles do not replace the original exit reason/candle merely because another signal appears.

M20 emergency liquidation remains higher operational precedence and may close the order first.

---

## 9. `OrderClose()` idempotency and retry contract

### OC-01 — Full-position close only

M23 closes the full current broker `OrderLots()` for the exact-owned live ticket.

No partial close, breakeven, trailing, TP2 or TP3 is introduced.

### OC-02 — Pre-attempt reconciliation

Before **every** ordinary lifecycle close attempt M23 must:

1. `OrderSelect()` the exact ticket;
2. verify exact symbol + configured magic + expected direction;
3. check `OrderCloseTime()` / live status;
4. if already closed, treat the close intent as satisfied and do not call `OrderClose()` again;
5. if live, use current broker-side close price (BUY -> BID, SELL -> ASK) and current remaining `OrderLots()`.

This alone prevents the common restart/tick double-close case.

### OC-03 — Success / ambiguous result reconciliation

After `OrderClose()`:
- definite success -> reselect/reconcile ticket and mark lifecycle close satisfied;
- failure that may be transient or ambiguous -> immediately reselect/reconcile before deciding to retry;
- if the ticket is now closed in broker truth, treat it as success even if the local API result was ambiguous;
- if still live, keep `LIFE_EXIT_LATCHED`; never clear the exit intent merely because one close call failed.

### OC-04 — Retry policy

Retry is **execution engineering**, not BBMA timing.

Required behavior:
- no new strategy signal is required to retry an already-latched exit;
- retry only while exact live ownership still holds;
- transient broker/price errors may retry on later ticks after `RefreshRates()`;
- hard metadata/ownership inconsistency freezes ordinary lifecycle and raises diagnostics rather than closing an uncertain/foreign order;
- no alternative TP, reverse order or hedge is manufactured after close failure.

No fixed strategy timeout is added.

### OC-05 — Emergency precedence

If `g_portfolio_emergency_close_requested` is active:
- M20 emergency policy takes precedence;
- M23 performs the emergency full close using the existing emergency path;
- ordinary lifecycle close logic must not make a second close attempt on the same tick;
- after broker closure reconciliation, the lifecycle latch is satisfied by the fact that the order no longer exists live.

### OC-06 — Close-intent identity

A separate broker order is not created for a close, so the ticket + execution hash + immutable exit event candle/reason are sufficient to identify the close intent.

A derived `CloseIntentHash` may be used for diagnostics/persistence, e.g. from:

`ExecutionHash | OwnerTimeframe | ExitEventCandleTime | ExitReason`

but this is optional engineering metadata, not required BBMA semantics.

---

## 10. Current source changes that will eventually be required

After the P3 runtime freeze closes, the future implementation will need at least:

### M02 / structures
- lifecycle state enum;
- exit-reason enum;
- explicit exit-policy / no-static-TP marker;
- lifecycle owner metadata in decision/trade payload;
- `TradeInfo` lifecycle fields.

### M17
- protective `Entry + SL + no-static-TP` validation from prior F7 audit;
- no MinRR gate for current lifecycle-managed Re-Entry-owned trades.

### M22
- allow authorized `TP=0`;
- preserve lifecycle owner metadata into the confirmed `TradeInfo`;
- do not reinterpret lifecycle state.

### M23
- owner-candle lifecycle reducer consumption;
- latched close intent;
- idempotent full `OrderClose()` + reconciliation;
- emergency precedence unchanged.

### M24
- targetless protective geometry;
- lifecycle checkpoint load/verification;
- deterministic owner-TF replay;
- history-insufficient / lifecycle-identity-missing frozen state;
- recovery of latched exits;
- closed-order reconciliation / checkpoint compaction.

### M27
- preserve M15 sole processing clock while allowing one per-position lifecycle reducer pass when a new owner-TF closed candle is observed.

---

## 11. New blocker exposed: post-Momentum continuation lifecycle

This audit can fully specify restart safety for:
- initial `MOMENTUM_PENDING`;
- transition to `MOMENTUM_CONFIRMED`;
- initial no-Momentum / opposite-CSM exit latch while pending;
- restart reconstruction of those states;
- close idempotency.

It cannot legitimately invent what happens **after Momentum has already been confirmed**.

Before removing the static TP and shipping a targetless lifecycle-managed production build, the project still needs a dedicated source reconciliation for:

> **After a same-direction CSM has confirmed continuation, what exact source-owned event re-arms or terminates the position lifecycle?**

Candidate source concepts to audit, without pre-selecting one:
- next same-owner Re-Entry -> new Momentum/no-Momentum epoch;
- Momentum diminishes / MHV transition;
- opposite Extreme / cycle restart;
- opposite CSM after confirmed Momentum.

Until that is resolved, `LIFE_MOMENTUM_CONFIRMED` must be recoverable but ordinary exit behavior after that state remains `HOLD`.

---

## 12. Runtime freeze

**NO EA CODE CHANGE NOW.**

The current P3 candidate remains unchanged so existing runtime evidence continues to identify one exact build.

This audit is documentation/architecture only.

Future implementation must use a new unique left-aligned build/header identifier and fresh compile/runtime evidence.

---

## 13. Final verdict

### Minimum persistent lifecycle record

`ExecutionHash + Ticket + SignalType + Direction + ExitPolicy + OwnerType + OwnerTF + OwnerReEntryCandleTime + LifecycleState + LastProcessedOwnerCandleTime + StateEventCandleTime + ExitReason`

### Restart authority

`BROKER TRUTH + VERIFIED LIFECYCLE IDENTITY + DETERMINISTIC CLOSED-OWNER-TF REPLAY`

Checkpoint alone is not Strategy-Core truth.

### Initial state machine

`OPEN -> MOMENTUM_PENDING`

`MOMENTUM_PENDING -> same-direction source-valid CSM -> MOMENTUM_CONFIRMED`

`MOMENTUM_PENDING -> approved reverse confirmation before same-direction CSM -> EXIT_LATCHED -> M23 CLOSE`

`MOMENTUM_PENDING -> approved opposite CSM -> EXIT_LATCHED -> M23 CLOSE`

### Close idempotency

`EXIT_LATCHED` is immutable until broker truth proves the position is closed. M23 reconciles the exact ticket before and after every `OrderClose()` attempt and never issues a second close against an already-closed ticket.

### Remaining HOLD

`MOMENTUM_CONFIRMED -> ?`

The exact post-Momentum re-arm/final-exit lifecycle is not yet sufficiently reconciled and must be audited before the targetless Path-A design can be considered production-complete.
