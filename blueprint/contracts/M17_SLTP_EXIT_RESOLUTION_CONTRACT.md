# M17 SL / TP / Exit Resolution Contract

## Status

**F7 CANONICAL / PATH-A — IMPLEMENTATION PENDING AFTER P3 RUNTIME FREEZE**

This contract replaces the historical Step 8B/8C universal static Re-Entry outer-BB TP design for the **next implementation**. It does not retroactively describe the currently frozen P3 source, which still carries the older positive-TP logic.

Canonical integrated contract:
`blueprint/contracts/F7_REENTRY_LIFECYCLE_EXECUTION_CONTRACT.md`.

---

## 1. Provenance classes

Use these classes:
- `STRATEGY_CORE` — accepted BBMA/Oma Ally lifecycle semantics after source reconciliation;
- `EA_SAFETY` — project protective hard-stop/risk protection;
- `ENGINEERING` — broker, persistence, recovery and idempotency mechanics;
- `HISTORICAL / NOT CORE-AUTHORIZED` — prior implementation choices not sufficiently established as universal Core.

Do not use `FORUM_SUPPORTED` as proof of the old static H1/H4/D1 outer-BB TP mapping. The retained registered forum evidence did not establish that mapping strongly enough under Path A.

---

## 2. Strategy-Core exit distinction

### Normal Extreme

Normal Extreme remains separate and retains the accepted TP-Wajib rule:
- Extreme SELL -> opposite MA5/MA10 Low area as normal first TP-Wajib area;
- Extreme BUY -> opposite MA5/MA10 High area as normal first TP-Wajib area;
- Mid BB remains farther/maximum context.

This contract does not remove or generalize the Extreme TP-Wajib rule.

### Re-Entry-owned executable trades

For standalone H1 Re-Entry, REM, RRE and REE, accepted Strategy-Core post-entry management is lifecycle-based:

`Re-Entry -> Momentum/CSM -> wait next Re-Entry -> Re-Entry -> Momentum/CSM -> ...`

If a valid Re-Entry epoch fails to produce same-direction Momentum and a later reverse confirmation appears, close/TP the position.

A universal static outer-BB broker TP is **not Core-authorized** for these trades under Path A.

---

## 3. Lifecycle owner mapping

| Executable type | Lifecycle owner TF |
|---|---:|
| standalone H1 `RE_ENTRY` | H1 |
| `REM` | H4 |
| `RRE` | D1 |
| `REE` | D1 |

The owner mapping is source-derived from the parent Re-Entry hierarchy. Lower-TF components remain supporting setup context and do not become independent broker-close owners.

The fact that the owner TF matches the timeframe formerly used by Step 8C for outer-BB destination selection does **not** validate that old static TP formula.

---

## 4. Initial protective payload

Future strict-Path-A Re-Entry-owned order payload:

- protective hard SL = present;
- static broker TP = absent (`0.0`);
- explicit exit policy = `REENTRY_LIFECYCLE`;
- `HasStaticTakeProfit = false`;
- `MinRRRatio` = bypassed/inactive for these executable types.

Hard SL classification remains **EA_SAFETY**:
- BUY -> exact owner Re-Entry source-candle LOW minus one broker point;
- SELL -> exact owner Re-Entry source-candle HIGH plus one broker point.

No arbitrary swing scan, fixed-pip fallback, synthetic reward target or RR-manufactured TP is allowed.

---

## 5. Re-Entry lifecycle profit-taking

### Initial/re-armed pending epoch

`LIFE_MOMENTUM_PENDING`

On later fully closed owner-TF candles:
- same-direction source-valid CSM -> `LIFE_WAIT_NEXT_REENTRY`;
- source-valid opposite CSM before same-direction CSM -> `EXIT_OPPOSITE_CSM`;
- first later reverse-direction confirmation before same-direction CSM -> `EXIT_NO_MOMENTUM_REVERSE`;
- otherwise remain pending.

Reverse confirmation mapping:
- BUY -> bearish closed candle `Close < Open`;
- SELL -> bullish closed candle `Close > Open`.

The Re-Entry validation candle itself is not evaluated as its own failure candle.

### After Momentum succeeds

`LIFE_WAIT_NEXT_REENTRY`

While waiting:
- no Re-Entry yet -> HOLD;
- ordinary reverse candle -> HOLD;
- neutral candle -> HOLD;
- further same-direction CSM -> HOLD;
- outer-BB reach -> no automatic close;
- elapsed time/candle count -> no effect.

The next valid same-direction Re-Entry on the owner timeframe re-arms the held position:

`WAIT_NEXT_REENTRY -> owner-TF Re-Entry -> MOMENTUM_PENDING`

A new full REM/RRE/REE component set is not required merely to re-arm lifecycle management of the existing position.

---

## 6. Final old-cycle exit

The final structural close boundary is:

`OPPOSITE REVERSAL-CONFIRMED EXTREME ON THE LIFECYCLE-OWNER TIMEFRAME`

This event atomically supersedes the old cycle and latches the old-direction lifecycle-managed position for close:

`any ordinary state -> LIFE_EXIT_LATCHED / EXIT_CYCLE_SUPERSEDED`

Raw opposite Extreme is only a candidate and is insufficient.

Owner TF:
- H1 Re-Entry -> H1 Extreme lifecycle;
- REM -> H4 Extreme lifecycle;
- RRE/REE -> D1 Extreme lifecycle.

D1 support is specified separately in:
`blueprint/contracts/M08_D1_EXTREME_LIFECYCLE_SUPPORT_SPEC.md`.

Outside an active pending epoch, `any opposite CSM -> close` is not added as another universal final-exit rule.

---

## 7. Static outer-BB TP disposition

Historical Step 8C used:
- H1 Re-Entry -> H1 Top/Low BB;
- REM -> H4 Top/Low BB;
- RRE/REE -> D1 Top/Low BB.

F7 concludes:

**`NOT PROVEN / NOT CORE-AUTHORIZED AS UNIVERSAL RE-ENTRY BROKER TP`**.

Therefore the next strict-Path-A implementation must not:
- require these destinations as positive `TakeProfit`;
- use them to compute MinRR;
- reject a valid lifecycle trade because such a destination is crossed/stale;
- describe them as Oma Ally/PDF/Core mandatory TP.

They may remain historical records or research context only.

---

## 8. MinRR and reward model

For current lifecycle-managed executable types:
- there is no source-proven deterministic reward distance at entry;
- `MinRRRatio` is therefore inactive/bypassed;
- no projected lifecycle reward may be invented;
- `REJ_INVALID_RR` is not emitted solely because no static TP exists.

M21 lot sizing and M19 total-risk accounting remain Entry/SL based and require no reward estimator.

---

## 9. Broker / lifecycle ownership

- M17 validates initial protective payload and lifecycle owner identity.
- M22 executes `SL > 0, TP = 0` only when the explicit lifecycle policy is present.
- M23 owns recurring per-ticket lifecycle state and full-position `OrderClose()`.
- M24 owns restart reconstruction/replay and fail-frozen recovery.
- M20 emergency protection has higher operational close precedence.
- M16 signal invalidation does not directly close broker positions.

No trailing stop, breakeven, partial profit, TP2 or TP3 is introduced.

---

## 10. Legacy/frozen-build boundary

The current P3 runtime candidate remains unchanged and still uses its historical static TP contract. Existing older positive-TP broker positions must not be silently converted into F7 lifecycle-managed positions by a later EA build.

F7 lifecycle authority requires explicit new-build lifecycle identity/checkpoint proof.

---

## 11. Implementation references

Canonical integrated contract:
- `blueprint/contracts/F7_REENTRY_LIFECYCLE_EXECUTION_CONTRACT.md`

Supporting F7 audits:
- `blueprint/CORE_V2_F7_WORKBOOK_RULE_RECONCILIATION_AUDIT_20260824.md`;
- `blueprint/CORE_V2_F7_DETERMINISTIC_NO_MOMENTUM_EXIT_RESOLUTION_AUDIT_20260824.md`;
- `blueprint/CORE_V2_F7_COMBINATION_LIFECYCLE_EXIT_OWNERSHIP_AUDIT_20260824.md`;
- `blueprint/CORE_V2_F7_STATIC_TP_VS_LIFECYCLE_EXIT_COEXISTENCE_AUDIT_20260824.md`;
- `blueprint/CORE_V2_F7_MINRR_PROTECTIVE_PAYLOAD_RESOLUTION_AUDIT_20260824.md`;
- `blueprint/CORE_V2_F7_M23_M24_LIFECYCLE_STATE_RESTART_RECOVERY_AUDIT_20260824.md`;
- `blueprint/CORE_V2_F7_POST_MOMENTUM_REARM_FINAL_EXIT_RESOLUTION_AUDIT_20260824.md`.

No EA source change is authorized by this documentation reconciliation while P3 runtime closure remains pending.
