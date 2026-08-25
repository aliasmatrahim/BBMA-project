# CORE-V2-F7 — Post-Momentum Re-Arm / Final Exit Resolution Audit

> **2026-08-25 EXECUTABLE-PRECEDENCE NOTICE**
> This document is retained as historical/provisional evidence reconstruction. Where it treats post-Re-Entry no-Momentum, re-arm, hold/no-TP, or related lifecycle-close behavior as executable/source-spec `RESOLVED`, that promotion is superseded by `docs/references/HOME_COURSE_19P_CROSS_SOURCE_RECONCILIATION_20260825.md`, `docs/references/HOME_COURSE_49_FAMILY_CORE_REVALIDATION_20260825.md`, and the current authoritative Strategy Core. Those material lifecycle behaviors remain HOLD unless a later explicit strategy decision reopens them. No EA execution authority may be derived from the superseded conclusion alone.

Date: 2026-08-24  
Branch: `blueprint-dev`  
Scope: lifecycle behavior after same-direction Momentum/CSM has already been confirmed for a live Re-Entry-owned position  
Status: **AUDIT COMPLETE — POST-MOMENTUM RE-ARM RESOLVED; FINAL OLD-CYCLE EXIT RESOLVED AT OWNER-TF OPPOSITE REVERSAL-CONFIRMED EXTREME; TARGETLESS LIFECYCLE SEMANTICS NOW COMPLETE AT SOURCE/SPEC LEVEL; D1 EXTREME-LIFECYCLE SUPPORT IS A REQUIRED IMPLEMENTATION GAP; NO EA CODE CHANGE WHILE P3 CANDIDATE IS FROZEN**

---

## 1. Question

The previous M23/M24 lifecycle audit resolved the initial post-Re-Entry branch:

`OPEN -> MOMENTUM_PENDING`

- same-direction source-valid CSM -> `MOMENTUM_CONFIRMED`;
- first later reverse-confirmation candle before same-direction CSM -> close;
- source-valid opposite CSM while the initial pending branch is active -> stronger failure / close.

It deliberately left one material HOLD:

> What happens to an already-open position after same-direction Momentum has been confirmed?

This audit resolves:

1. whether the existing position waits for another Re-Entry;
2. whether that later Re-Entry re-arms the no-Momentum test;
3. whether re-arm requires a new REM/RRE/REE combination or only the lifecycle-owner Re-Entry;
4. what finally terminates the old-direction position if the BBMA cycle itself ends;
5. how the resolved behavior extends M23/M24 replay/persistence without inventing timers or static TP.

This audit supersedes only the `LS-04` HOLD in `CORE_V2_F7_M23_M24_LIFECYCLE_STATE_RESTART_RECOVERY_AUDIT_20260824.md`. All previously resolved close-idempotency, recovery, execution-hash and fail-frozen rules remain in force.

No EA source change is authorized while the current P3 runtime candidate remains frozen.

---

## 2. Mandatory source + GitHub preflight

Applied order:

`Original evidence -> canonical Core -> Finale -> forum corroboration -> accepted F7 decisions -> live contracts -> current code`

Checked live project governance/state:
- `PROJECT_INSTRUCTIONS.md`;
- `docs/references/SOURCE_INDEX.md`;
- `docs/references/BBMA_STRATEGY_CORE_SOURCE_OF_TRUTH_V2.md`;
- `BBMA_FINALE_MASTER_RULE_INDEX.md`;
- Finale V05/V06 extracted rules;
- conflict/HOLD register;
- retained Forex Factory deep extraction register;
- `blueprint/CURRENT.md` and `blueprint/MASTER_QUEUE.md`;
- M08, M10, M12, M23 and M24 contracts;
- active `blueprint/source/BBMA_EA.mq4`;
- prior F7 deterministic no-Momentum, owner-timeframe, static-TP, MinRR/protective-payload and M23/M24 recovery audits.

Original evidence checked directly:
- `Oma ally BBMA - AL.pdf`;
- authenticated Tier-B `BBMA Home Course Workbook`;
- secondary `BBMA technique.pdf`.

Forum evidence remains supplemental and does not provide a stronger contradictory post-Momentum exit rule.

---

## 3. Strongest direct evidence — Home Course Workbook

The workbook is unusually explicit about the repeating post-Momentum lifecycle.

### 3.1 Momentum is followed by another Re-Entry

Repeated statements include:

- `Bila ada Momentum akan ada reentry.`
- `Reentry - selepas momentum akan ada reentry semula.`
- `Extreme – MHV – CS Arah – ReEntry – Momentum – Reentry` is described as the repeating/mainframe sequence.
- `Tetapi kiranya berlaku momentum akan ada satu lagi reentry berterusan.`
- `Bila di momentum kita akan tunggu di reentry balik.`

This is direct evidence that same-direction Momentum is **not** the terminal state of the held position. The strategy expects a later Re-Entry and continues to manage the move through that recurring structure.

### 3.2 No Re-Entry yet means HOLD, not close

The workbook separately states:

`Arah - Tiada reentry - Boleh hold position, tunggu reentry selepas tu.`

It gives the same principle in examples where strong direction reaches an outer BB without the expected Re-Entry: do not take profit merely because Momentum is absent before the Re-Entry; wait for the Re-Entry.

Therefore after a confirmed Momentum:

> absence of the next Re-Entry is not a close event.

No fixed candle count, elapsed time, pip distance or simple reverse candle may be invented to replace the missing Re-Entry.

### 3.3 The no-Momentum test is repeated after the later Re-Entry

The workbook then states:

- `Kiranya ada reentry tidak ada momentum market akan buat satu pusingan.`
- `MHV – CS Arah - Reentry - turun tidak ada momentum, maknanya TP; ini kena TP kalau tidak dia akan naik balik.`

This links the close decision to a **Re-Entry followed by failure to produce Momentum**, not to Momentum merely becoming old or to an arbitrary number of candles.

Therefore the later same-direction Re-Entry starts a new continuation-test epoch.

---

## 4. Primary PDF reconciliation

The primary PDF gives the same recurring topology:

`... Re-Entry -> CSM/Momentum -> further Re-Entry opportunities -> opposite Extreme / cycle restart`

It also states that after a short Re-Entry retracement, price travels in the intended direction creating Momentum candles until Momentum diminishes.

The page-3 cycle diagram explicitly shows repeated structure of the form:

`CSM -> Re-Entry -> CSM -> Re-Entry -> CSM -> Extreme/MLV`

This strongly corroborates the workbook's repeated Re-Entry epochs.

The PDF does not prescribe a timer-based final exit after Momentum. It instead places the terminal structural boundary at the **opposite Extreme / cycle restart**.

---

## 5. Finale reconciliation

Finale evidence is consistent:

- V05 OA-F-V05-016: direction or Momentum repeatedly generates later Re-Entry opportunities as continuation persists;
- V06 OA-F-V06-001: the cycle is reiterated as `Extreme -> TP Wajib -> MHV -> direction -> Re-Entry -> Momentum/continuation` and repeats across timeframes;
- the Master Rule Index keeps the canonical sequence `Re-Entry -> Momentum/CSM -> further Re-Entry -> opposite Extreme / cycle restart`.

Finale does not establish a competing rule such as:
- close the existing position on the first ordinary reverse candle after confirmed Momentum;
- close after N candles without a new Re-Entry;
- close merely because outer BB was reached;
- close a higher-TF owner position from a lower-TF opposing-looking component.

---

## 6. Forum / secondary reconciliation

The retained Forex Factory extraction register contains useful state-machine and MTF corroboration but no sufficiently traceable higher-precedence rule that changes this lifecycle.

The secondary PDF supports:
- Momentum / BB expansion;
- MHV as loss of momentum near trend end;
- Re-Entry as recurring setup;

but it does not supply a different deterministic post-Momentum final-exit algorithm.

Therefore no forum/secondary exception overrides the workbook + primary-PDF + Finale convergence.

---

## 7. Post-Momentum state resolution

### PMR-01 — Replace terminal-looking `MOMENTUM_CONFIRMED` semantics with WAIT-NEXT-REENTRY semantics

**RESOLVED.**

A same-direction source-valid CSM does not end lifecycle management. Operationally it means:

`LIFE_MOMENTUM_PENDING -> SAME-DIRECTION CSM -> LIFE_WAIT_NEXT_REENTRY`

`LIFE_MOMENTUM_CONFIRMED` may remain as diagnostic/event terminology, but the durable state should represent what the strategy now expects: **wait for the next Re-Entry**.

Recommended state name:

`LIFE_WAIT_NEXT_REENTRY`

This is clearer and avoids treating confirmed Momentum as a terminal holding state with no next transition.

### PMR-02 — While waiting for the next Re-Entry, HOLD

**RESOLVED.**

While `LIFE_WAIT_NEXT_REENTRY`:

- ordinary neutral candles -> HOLD;
- ordinary reverse-colour candles -> HOLD;
- further same-direction CSM candles -> HOLD and remain waiting for Re-Entry;
- elapsed candle count/time -> no effect;
- reaching a generic outer-BB location -> no automatic close;
- lower-timeframe opposing-looking structures -> no direct broker close of the higher-TF owner position.

Reason: the source explicitly says to hold when the expected Re-Entry has not yet occurred.

This does not disable the broker hard SL or M20 emergency protection.

---

## 8. Re-arm resolution

### PMR-03 — Later same-direction owner-TF Re-Entry re-arms the existing position

**RESOLVED.**

After same-direction Momentum has been confirmed, the first later **valid same-direction Re-Entry on the resolved lifecycle-owner timeframe** starts the next continuation-test epoch.

Transition:

`LIFE_WAIT_NEXT_REENTRY`

`-> later valid same-direction owner-TF Re-Entry`

`-> LIFE_MOMENTUM_PENDING`

The active lifecycle epoch anchor becomes that later Re-Entry confirmation candle.

Observation begins only on later fully closed owner-TF candles. The Re-Entry validation candle itself is not tested as its own no-Momentum failure candle.

### PMR-04 — Re-arm applies to the already-open held position

**RESOLVED AS THE MINIMUM SOURCE-DERIVED POSITION-MANAGEMENT MAPPING.**

The workbook explicitly says an existing position may be held while waiting for Re-Entry and then bases the next TP/close decision on whether Momentum follows that Re-Entry.

Therefore a still-open lifecycle-managed position from the same owner thesis/cycle is re-armed by the later owner Re-Entry even if no new broker order is opened at that Re-Entry.

This is **lifecycle management**, not new-entry permission.

### PMR-05 — Re-arm does not require reconstructing a new REM/RRE/REE combination

**RESOLVED.**

The re-arm event belongs to the already-resolved lifecycle owner:

- standalone H1 Re-Entry position -> next valid H1 Re-Entry;
- REM -> next valid H4 Re-Entry;
- RRE -> next valid D1 Re-Entry;
- REE -> next valid D1 Re-Entry.

A new full REM/RRE/REE component set is **not required merely to re-arm lifecycle management of an already-open position**.

Reason:
- source teaches `Momentum -> Re-Entry` recurrence at the parent Re-Entry timeframe;
- lower-timeframe components are supporting completion/context;
- requiring a full new combination would add an unsupported gate to position management.

Whether a **new add-on order** may also be opened at that later setup remains governed separately by M13/M14/M15/M16/M17/M19/M20/M22 and the trade-lock/portfolio rules. M23 must never turn a lifecycle re-arm into entry authority.

### PMR-06 — Multiple existing positions

If several still-open lifecycle-managed tickets share the same pair, direction, lifecycle owner timeframe and surviving owner-cycle thesis, each ticket may consume the same later owner Re-Entry as its new lifecycle epoch anchor.

This does not create basket strategy ownership. Each ticket retains its own execution hash, checkpoint, exit latch and broker-close idempotency.

---

## 9. Re-armed pending epoch

After re-arm, the already accepted pending logic repeats unchanged:

`LIFE_MOMENTUM_PENDING`

- same-direction source-valid owner-TF CSM -> `LIFE_WAIT_NEXT_REENTRY`;
- first later approved reverse-confirmation candle before same-direction CSM -> `LIFE_EXIT_LATCHED / EXIT_NO_MOMENTUM_REVERSE`;
- source-valid opposite CSM while this pending epoch is active -> `LIFE_EXIT_LATCHED / EXIT_OPPOSITE_CSM` as the stronger failed-continuation event already accepted by the prior F7 audit;
- neutral/non-CSM/no-reverse structural noise -> remain pending.

No fixed timeout is introduced on any epoch.

---

## 10. Final old-cycle exit resolution

### PMR-07 — Source boundary

The primary PDF states that an **opposite Extreme is created once the trend or Momentum ends and the BBMA cycle restarts/reverses**.

The project has already resolved the deterministic old-cycle supersession boundary in F1:

`OPPOSITE RAW EXTREME = new-cycle candidate only`

`OPPOSITE REVERSAL-CONFIRMED EXTREME = atomic old-cycle supersession`

Raw Extreme alone is deliberately insufficient because Extreme is only an early signal and requires reversal confirmation.

### PMR-08 — Final position exit at old-cycle supersession

**RESOLVED AS SOURCE-DERIVED + EXISTING ACCEPTED CYCLE-BOUNDARY MAPPING.**

For an open targetless Re-Entry-owned position, a source-valid **opposite reversal-confirmed Extreme on the lifecycle-owner timeframe** terminates the old directional cycle and therefore terminates the old-cycle position authority.

Transition from any ordinary non-latched lifecycle state:

`OLD OWNER CYCLE`

`-> OPPOSITE REVERSAL-CONFIRMED EXTREME ON OWNER TF`

`-> LIFE_EXIT_LATCHED / EXIT_CYCLE_SUPERSEDED`

This is the minimum conservative final-exit mapping because:
- source explicitly identifies opposite Extreme with trend/Momentum end and cycle restart/reversal;
- the project already rejects RAW Extreme as sufficient cycle proof;
- keeping an old-direction targetless position alive after the old cycle is atomically superseded would contradict the accepted cycle ownership model;
- waiting for a new opposite Re-Entry/CSM would keep the old position into a new cycle without source support.

Classification:
- opposite Extreme marks end/restart = **DIRECT PRIMARY-PDF CYCLE PRINCIPLE**;
- reversal-confirmed maturity as the deterministic boundary = **EXISTING ACCEPTED F1/F2 PROJECT MAPPING**;
- broker close of the still-open old-cycle position at that boundary = **MINIMUM SOURCE-DERIVED LIFECYCLE MAPPING**.

### PMR-09 — MHV/MLV is not a separate earlier final-close trigger

A later MHV/MLV belongs after Extreme in the restarted/reversing cycle. It therefore does not need a second direct broker-close rule for the old position.

By the time canonical new-cycle MHV/MLV can develop, the old position should already have been latched for close at the opposite reversal-confirmed Extreme cycle boundary.

### PMR-10 — Opposite CSM after confirmed Momentum is not promoted into a second independent final-exit rule

Outside an active `MOMENTUM_PENDING` epoch, this audit does **not** create a new universal rule saying `any opposite CSM -> close`.

Reason:
- the direct post-Re-Entry opposite-CSM rule was accepted specifically as a stronger failure while expected same-direction Momentum had not yet appeared;
- after Momentum has succeeded, source returns to the recurring `Momentum -> Re-Entry` cycle;
- canonical final old-cycle termination is the opposite-Extreme restart boundary.

If complete chronological replay ever appears to show a source-valid opposite CSM in the old direction context without the expected prior cycle-supersession structure, treat it as a **sequence/provenance inconsistency requiring fail-frozen handling/diagnostics**, not permission for M23 to invent a second strategy exit formula.

---

## 11. Owner timeframe for final exit

The final-cycle boundary is evaluated on the same lifecycle-owner timeframe already resolved for the position:

| Position type | Re-arm Re-Entry TF | Final opposite-Extreme TF |
|---|---:|---:|
| standalone H1 `RE_ENTRY` | H1 | H1 |
| `REM` | H4 | H4 |
| `RRE` | D1 | D1 |
| `REE` | D1 | D1 |

Lower-TF Extremes do not directly close a higher-TF parent-owned position under this rule.

---

## 12. Full resolved recurring state machine

The future strict-Path-A lifecycle is now:

```text
ORDER OPEN FROM VALID RE-ENTRY-OWNED DECISION
        |
        v
LIFE_MOMENTUM_PENDING
        |
        |-- same-direction owner-TF CSM --------------------+
        |                                                   |
        |                                                   v
        |                                      LIFE_WAIT_NEXT_REENTRY
        |                                                   |
        |                         later valid same-direction owner-TF Re-Entry
        |                                                   |
        +<--------------------------------------------------+

While LIFE_MOMENTUM_PENDING:
  reverse-confirmation before same-direction CSM -> EXIT_NO_MOMENTUM_REVERSE
  opposite CSM before same-direction CSM         -> EXIT_OPPOSITE_CSM

From any ordinary state:
  opposite REVERSAL-CONFIRMED Extreme on owner TF -> EXIT_CYCLE_SUPERSEDED

While LIFE_WAIT_NEXT_REENTRY:
  no Re-Entry yet -> HOLD
  no fixed timeout
  ordinary reverse candle alone -> HOLD
```

The loop may repeat multiple times:

`Re-Entry -> Momentum -> wait Re-Entry -> Re-Entry -> Momentum -> ...`

until either:
- one Re-Entry epoch fails to produce Momentum and confirms reversal; or
- the old cycle is superseded by an opposite reversal-confirmed Extreme; or
- broker hard SL / M20 emergency protection closes the trade first.

---

## 13. Required lifecycle metadata update

The previous M23/M24 audit's minimum identity remains valid but needs one distinction for repeated epochs.

Persist at least:

### Immutable entry provenance
- `ExecutionHash`;
- ticket;
- signal type;
- direction;
- lifecycle-managed/no-static-TP marker;
- owner type/timeframe;
- **OriginalOwnerReEntryCandleTime**;
- original cycle identity/provenance (`CycleStartTime` or equivalent verified owner-cycle key).

### Mutable lifecycle epoch state
- `LifecycleState`;
- **ActiveEpochReEntryCandleTime**;
- `LastProcessedOwnerCandleTime`;
- latest Momentum event candle time where useful;
- state-event candle time;
- exit reason when latched.

The original owner Re-Entry candle must never be overwritten merely because the current epoch is re-armed. The active epoch anchor changes; immutable entry provenance does not.

---

## 14. Restart replay extension

M24 replay must now reproduce the recurring reducer, not stop after first Momentum.

Chronological owner-TF replay:

1. initialize at original valid Re-Entry/open boundary -> `MOMENTUM_PENDING`;
2. process each later closed owner candle exactly once;
3. same-direction CSM while pending -> `WAIT_NEXT_REENTRY`;
4. while waiting, detect only a **valid same-direction owner Re-Entry** as the normal re-arm event;
5. re-arm -> update `ActiveEpochReEntryCandleTime` and return to `MOMENTUM_PENDING`;
6. repeat pending success/failure rules;
7. detect authoritative opposite reversal-confirmed Extreme cycle supersession at any ordinary state -> `EXIT_LATCHED`;
8. once exit is latched, later replay cannot replace the original trigger/reason.

Replay must reuse source-owned producers/owner states. M24 may not create duplicate Re-Entry, CSM or Extreme formulas.

History insufficiency remains fail-frozen exactly as resolved in the preceding M23/M24 audit.

---

## 15. Newly exposed implementation gap — D1 Extreme lifecycle

### PMR-11 — Required D1 cycle-boundary support

**IMPLEMENTATION GAP CONFIRMED.**

Current active `PairState` contains:
- H1 Extreme lifecycle BUY/SELL;
- H4 Extreme lifecycle BUY/SELL;
- M15 Extreme lifecycle BUY/SELL;

but no corresponding D1 `ExtremeLifecycleData` state.

That was sufficient for the prior executable combination/component architecture, but the newly resolved final lifecycle boundary for `RRE` and `REE` is on **D1**.

Therefore future F7 implementation must provide source-aligned D1 Extreme maturity/cycle-supersession support using the existing M08/F2 semantics, without enabling D1 standalone Extreme entry merely because D1 lifecycle tracking now exists.

This is a support-state extension, not a new entry type.

Required guard:
- D1 RAW Extreme remains only a candidate;
- D1 opposite reversal-confirmed Extreme is the cycle-supersession event;
- D1 standalone Extreme execution remains governed by existing entry eligibility and is not activated by this lifecycle requirement.

---

## 16. M23/M24 ownership consequences

### M23
Future M23 must:
- consume already-resolved owner lifecycle events;
- maintain the recurring state machine per ticket;
- re-arm an existing held position on the later owner-TF Re-Entry;
- latch `EXIT_NO_MOMENTUM_REVERSE`, `EXIT_OPPOSITE_CSM` or `EXIT_CYCLE_SUPERSEDED` where applicable;
- preserve the previously resolved full-position, idempotent `OrderClose()` contract;
- never create new entry authority.

### M24
Future M24 must:
- persist original entry provenance separately from the mutable active Re-Entry epoch;
- replay multiple `Re-Entry -> Momentum -> Re-Entry` epochs;
- verify same-cycle/same-owner re-arm;
- replay/verify final opposite-Extreme cycle supersession;
- freeze ordinary lifecycle if required source history/identity is missing;
- never fabricate static TP, Re-Entry, Momentum or Extreme state.

### M08 / F2 support
Future implementation must add D1 lifecycle tracking needed for RRE/REE final-cycle proof while preserving M08's detector-only / no-direct-entry boundary.

---

## 17. Relationship to targetless `TP=0` architecture

With this audit, the Strategy-Core lifecycle semantics needed by the targetless Re-Entry design are now closed at specification/source level:

- initial Re-Entry epoch -> resolved;
- no-Momentum failure event -> resolved;
- same-direction Momentum success -> resolved;
- combination owner timeframe -> resolved;
- static outer-BB TP not required -> resolved;
- MinRR bypass / protective `TP=0` payload -> resolved;
- restart/idempotent close model -> resolved;
- post-Momentum wait/re-arm -> **resolved here**;
- final old-cycle exit -> **resolved here**.

This does **not** mean the EA is production-ready yet. Contracts/code/current Core consolidation still need a deliberate post-freeze reconciliation/implementation series and fresh compile/runtime evidence.

---

## 18. Runtime freeze

**NO EA CODE CHANGE NOW.**

The active P3 candidate remains unchanged so its pending runtime evidence stays attributable to one build/source.

No About/header/build identifier is changed by this documentation-only audit.

---

## 19. Future implementation sequence after P3 runtime closure

1. update canonical Strategy Core with the accepted Re-Entry lifecycle exit loop;
2. reconcile F7 decision/audit status in `CURRENT.md` and `MASTER_QUEUE.md`;
3. redesign M17 for explicit `Entry + protective SL + no static TP` payload;
4. make `MinRRRatio` structurally dormant for current lifecycle-managed executable types;
5. update M22 to allow authorized `TP=0`;
6. add lifecycle enum/metadata/checkpoint schema;
7. add D1 Extreme lifecycle/cycle-supersession support without enabling standalone D1 Extreme entries;
8. update M23 recurring lifecycle reducer + latched idempotent close;
9. update M24 repeated-epoch replay/recovery and targetless geometry;
10. update contracts before/with code so spec and implementation remain aligned;
11. assign a new unique left-aligned build/header identifier;
12. native MetaEditor compile: 0 errors / 0 warnings;
13. static cross-module / Strategy-Core purity regression;
14. fresh runtime tests covering at least:
   - initial Re-Entry -> same-direction Momentum -> HOLD/wait;
   - Momentum -> later same-direction Re-Entry -> re-arm;
   - re-armed Re-Entry -> no Momentum + reverse confirmation -> close;
   - repeated Momentum/Re-Entry epochs;
   - opposite reversal-confirmed Extreme -> cycle-supersession close;
   - REM H4 owner;
   - RRE/REE D1 owner and D1 Extreme lifecycle;
   - restart while pending;
   - restart while waiting for Re-Entry;
   - restart after re-arm;
   - restart with exit already latched;
   - TP=0 broker acceptance;
   - hard-SL protection;
   - M20 emergency-close precedence;
   - duplicate-close/idempotency behavior.

---

## 20. Final verdict

### Post-Momentum Re-Arm

**RESOLVED.**

`Re-Entry -> Momentum` does not end the trade lifecycle.

After same-direction Momentum:

`HOLD -> WAIT FOR NEXT SAME-DIRECTION OWNER-TF RE-ENTRY`

That later Re-Entry re-arms the already-open same-cycle position into a new `MOMENTUM_PENDING` epoch, whether or not a new add-on order is opened.

### No-Momentum after any re-armed Re-Entry

**RESOLVED.**

The same accepted rule repeats:

`Re-Entry -> no same-direction Momentum -> first later reverse confirmation -> CLOSE`

with opposite CSM remaining the stronger failure event while that pending epoch is active.

### Final old-cycle exit

**RESOLVED.**

`OPPOSITE REVERSAL-CONFIRMED EXTREME ON THE OWNER TIMEFRAME`

is the final structural old-cycle supersession event and latches the remaining old-direction lifecycle-managed position for close.

### Current implementation status

**NOT IMPLEMENTED.**

The source/spec blocker is now closed, but the active EA still reflects the older static-TP architecture. RRE/REE additionally require D1 Extreme lifecycle support for the resolved final-cycle exit.

### Path-A status

For the targetless Re-Entry-owned `TP=0 + M23 lifecycle exit` design:

**STRATEGY/LIFECYCLE SEMANTICS: COMPLETE ENOUGH FOR CONTRACT RECONCILIATION AND IMPLEMENTATION AFTER P3 RUNTIME FREEZE.**

No fixed timeout, synthetic reward target, trailing stop, breakeven, TP2/TP3, RSI/MACD/Stochastic/ADX/news/session/correlation filter, or unsupported lower-TF close authority is introduced.