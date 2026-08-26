# Master R1–R6 Runtime Evidence Index / Tracker — PREP ONLY

Date: 2026-08-27  
Preparation branch: `p0-exec-id-persistence-fix`  
Status: **PREPARED / DOCUMENTATION-ONLY / ALL FORMAL RUNTIME STAGES BLOCKED BY P0 #94**

## 1. Purpose

Provide one canonical tracker for the already-prepared authenticated MT4 broker/demo runtime sequence:

`P0 -> R1 -> R2 -> R3 -> R4 -> R5 -> R6`

This tracker indexes **115 prepared runtime cases**:

- R1: 17 cases (`R1-00..R1-16`)
- R2: 27 cases (`R2-00..R2-26`)
- R3: 16 cases (`R3-00..R3-15`)
- R4: 17 cases (`R4-00..R4-16`)
- R5: 21 cases (`R5-00..R5-20`)
- R6: 17 cases (`R6-00..R6-16`)

This is an **index/status ledger only**. Detailed scenario semantics, required evidence, PASS conditions and FAIL conditions remain authoritative in the stage-specific matrices.

This record does not modify `blueprint/source/BBMA_EA.mq4`, does not merge branches, does not activate D1TPW/C044/N3, and does not change BBMA strategy, SL/TP, MM/risk, lifecycle, execution or portfolio semantics.

## 2. Current blocker snapshot

At tracker creation:

- Issue #94 is still OPEN;
- P0 code/static/native compile status is PASS;
- fresh v4.59 HFM demo trade + restart + no-duplicate runtime acceptance remains pending;
- P0 branch head before this tracker: `37aecf4230d42ca825ace370c1cbf67229f64631`;
- P0 production implementation commit: `03c4c3b90abbc6f669a89b1379218a26c5a57369`;
- build: `Version 4.5.9 - P0 Execution Identity Persistence Fix`;
- D1TPW default gate remains OFF;
- C044 default gate remains OFF.

Therefore every formal R1–R6 case starts as `BLOCKED` until its predecessor gates are satisfied.

## 3. Status vocabulary

Only these runtime statuses are valid:

- `BLOCKED` — predecessor gate or authenticated connected broker/demo environment unavailable.
- `INCOMPLETE` — authenticated runtime exists, but required scenario/evidence is not yet sufficient.
- `PASS` — exact case positively demonstrated with attributable evidence.
- `FAIL` — contradictory, unsafe, identity-invalid or semantically wrong behavior observed.

Do not reinterpret `BLOCKED` or `INCOMPLETE` as PASS.

## 4. Update rule

A case status may change only when the tracker records enough identity to locate the evidence:

- canonical commit/blob/MQ4 SHA/build/version;
- test profile and lifecycle gate state;
- broker/demo/authenticated classification;
- ticket/pair/magic/direction where applicable;
- DecisionID/execution hash where applicable;
- restart epoch where applicable;
- bundle/log/assertion path or dedicated closure audit reference.

The tracker must never manufacture a PASS from a narrative claim without raw attributable evidence.

## 5. Stage summary

| Stage | Scope | Case count | Current status | Immediate blocker |
|---|---|---:|---|---|
| P0 | EXEC_ID durable identity + restart + duplicate protection | gate | `BLOCKED` | fresh v4.59 HFM demo runtime evidence |
| R1 | D1 Extreme TP-Wajib lifecycle | 17 | `BLOCKED` | P0 PASS + canonical integration + post-P0 tooling |
| R2 | C044 failed-Momentum lifecycle | 27 | `BLOCKED` | R1 predecessor + P0/tooling lineage |
| R3 | D1 owner + D1O identity/dedup | 16 | `BLOCKED` | R2 predecessor |
| R4 | validation timing + M17 live SL geometry | 17 | `BLOCKED` | R3 predecessor |
| R5 | TradeLock + cumulative risk + P3/ambiguity | 21 | `BLOCKED` | R4 predecessor |
| R6 | N1/N2 forward identity/outcome + N3 firewall | 17 | `BLOCKED` | R5 predecessor |

---

# 6. R1 tracker — D1 Extreme TP-Wajib lifecycle

Authority: `R1_D1_TPW_BROKER_RUNTIME_TEST_MATRIX_PREP_20260826.md`

| Case | Scenario | Status | Evidence / bundle | Notes |
|---|---|---|---|---|
| R1-00 | Gate-OFF fail-closed control | `BLOCKED` | — | P0 predecessor |
| R1-01 | Targetless initial payload | `BLOCKED` | — | P0 predecessor |
| R1-02 | Restart checkpoint recovery | `BLOCKED` | — | P0 predecessor |
| R1-03 | Missed-D1-candle replay | `BLOCKED` | — | P0 predecessor |
| R1-04 | BUY completion via MA5 High | `BLOCKED` | — | P0 predecessor |
| R1-05 | BUY completion via MA10 High | `BLOCKED` | — | P0 predecessor |
| R1-06 | SELL completion via MA5 Low | `BLOCKED` | — | P0 predecessor |
| R1-07 | SELL completion via MA10 Low | `BLOCKED` | — | P0 predecessor |
| R1-08 | Dynamic same-candle MA semantics | `BLOCKED` | — | P0 predecessor |
| R1-09 | First-event latch / duplicate-close prevention | `BLOCKED` | — | P0 predecessor |
| R1-10 | No automatic opposite entry | `BLOCKED` | — | P0 predecessor |
| R1-11 | C044 mutual exclusion | `BLOCKED` | — | P0 predecessor |
| R1-12 | Ambiguous dual-checkpoint fail-closed | `BLOCKED` | — | controlled negative only |
| R1-13 | Missing/corrupt checkpoint fail-closed | `BLOCKED` | — | controlled negative only |
| R1-14 | M20 emergency precedence | `BLOCKED` | — | safe demo evidence only |
| R1-15 | No legacy outer-BB TP fallback | `BLOCKED` | — | P0 predecessor |
| R1-16 | Fully-closed-D1-only timing | `BLOCKED` | — | P0 predecessor |

R1 formal closure remains governed by the detailed R1 matrix; this tracker cannot relax any mandatory case.

---

# 7. R2 tracker — C044 lifecycle

Authority: `R2_C044_BROKER_RUNTIME_TEST_MATRIX_PREP_20260826.md`

| Case | Scenario | Status | Evidence / bundle | Notes |
|---|---|---|---|---|
| R2-00 | Gate-OFF control | `BLOCKED` | — | predecessor chain |
| R2-01 | Targetless initial payload | `BLOCKED` | — | predecessor chain |
| R2-02 | Frozen owner identity | `BLOCKED` | — | predecessor chain |
| R2-03 | Restart checkpoint recovery | `BLOCKED` | — | predecessor chain |
| R2-04 | Deterministic multi-candle replay | `BLOCKED` | — | predecessor chain |
| R2-05 | Missing/corrupt replay fail-frozen | `BLOCKED` | — | controlled negative only |
| R2-06 | BUY failed-Momentum close | `BLOCKED` | — | predecessor chain |
| R2-07 | SELL failed-Momentum close | `BLOCKED` | — | predecessor chain |
| R2-08 | No one-candle timeout | `BLOCKED` | — | predecessor chain |
| R2-09 | Valid Momentum survives | `BLOCKED` | — | predecessor chain |
| R2-10 | WAIT_NEXT_REENTRY hold semantics | `BLOCKED` | — | predecessor chain |
| R2-11 | Same-direction Re-Entry re-arm | `BLOCKED` | — | predecessor chain |
| R2-12 | Re-arm creates no new broker order | `BLOCKED` | — | predecessor chain |
| R2-13 | Opposite mature Extreme supersession | `BLOCKED` | — | predecessor chain |
| R2-14 | Lower-TF shortcut rejection | `BLOCKED` | — | predecessor chain |
| R2-15 | No automatic opposite entry | `BLOCKED` | — | predecessor chain |
| R2-16 | M20 emergency precedence | `BLOCKED` | — | safe demo evidence only |
| R2-17 | Close idempotency | `BLOCKED` | — | predecessor chain |
| R2-18 | D1TPW mutual exclusion | `BLOCKED` | — | predecessor chain |
| R2-19 | Dual/missing lifecycle checkpoint fail-safe | `BLOCKED` | — | controlled negative only |
| R2-20 | MinRR targetless policy | `BLOCKED` | — | predecessor chain |
| R2-21 | Fully-closed owner-TF evaluation | `BLOCKED` | — | predecessor chain |
| R2-22 | Canonical Momentum ownership | `BLOCKED` | — | predecessor chain |
| R2-23 | Canonical Re-Entry/Extreme ownership | `BLOCKED` | — | predecessor chain |
| R2-24 | Static outer-BB TP non-coexistence | `BLOCKED` | — | predecessor chain |
| R2-25 | C035 separation | `BLOCKED` | — | predecessor chain |
| R2-26 | P0 execution identity survives R2 | `BLOCKED` | — | predecessor chain |

---

# 8. R3 tracker — D1 strategic owner + D1O identity/dedup

Authority: `R3_R6_CONSOLIDATED_BROKER_RUNTIME_ACCEPTANCE_MATRIX_PREP_20260826.md`

| Case | Scenario | Status | Evidence / bundle | Notes |
|---|---|---|---|---|
| R3-00 | Authenticated baseline identity | `BLOCKED` | — | R2 predecessor |
| R3-01 | D1 BUY confirmed | `BLOCKED` | — | R2 predecessor |
| R3-02 | D1 SELL confirmed | `BLOCKED` | — | R2 predecessor |
| R3-03 | D1 TRANSITION | `BLOCKED` | — | R2 predecessor |
| R3-04 | D1 UNRESOLVED | `BLOCKED` | — | R2 predecessor |
| R3-05 | H4 same-direction under D1 owner | `BLOCKED` | — | R2 predecessor |
| R3-06 | H4 opposite D1 | `BLOCKED` | — | R2 predecessor |
| R3-07 | H4 no-owner where H4 ownership is required | `BLOCKED` | — | R2 predecessor |
| R3-08 | D1O DecisionID attribution | `BLOCKED` | — | R2 predecessor |
| R3-09 | Stable execution hash across non-executable D1 attribution changes | `BLOCKED` | — | R2 predecessor |
| R3-10 | Direction invariance | `BLOCKED` | — | R2 predecessor |
| R3-11 | D1O dedup | `BLOCKED` | — | R2 predecessor |
| R3-12 | D1O restart continuity | `BLOCKED` | — | R2 predecessor |
| R3-13 | Tactical D1_OPP_EXTREME_TPW separation | `BLOCKED` | — | R2 predecessor |
| R3-14 | No D1-close side effect | `BLOCKED` | — | R2 predecessor |
| R3-15 | Fully closed D1 only | `BLOCKED` | — | R2 predecessor |

---

# 9. R4 tracker — validation timing + M17 live structural SL

Authority: `R3_R6_CONSOLIDATED_BROKER_RUNTIME_ACCEPTANCE_MATRIX_PREP_20260826.md`

| Case | Scenario | Status | Evidence / bundle | Notes |
|---|---|---|---|---|
| R4-00 | Exact validation provenance | `BLOCKED` | — | R3 predecessor |
| R4-01 | Order opens after validation candle | `BLOCKED` | — | R3 predecessor |
| R4-02 | No forming-candle validation | `BLOCKED` | — | R3 predecessor |
| R4-03 | BUY structural window | `BLOCKED` | — | R3 predecessor |
| R4-04 | BUY final hard SL | `BLOCKED` | — | R3 predecessor |
| R4-05 | SELL structural window | `BLOCKED` | — | R3 predecessor |
| R4-06 | SELL structural SL before broker buffer | `BLOCKED` | — | R3 predecessor |
| R4-07 | SELL spread buffer | `BLOCKED` | — | R3 predecessor |
| R4-08 | Frozen snapshot consistency | `BLOCKED` | — | R3 predecessor |
| R4-09 | AutoLot reacts to final SL | `BLOCKED` | — | R3 predecessor |
| R4-10 | FixedLot unaffected by AutoLot formula | `BLOCKED` | — | R3 predecessor |
| R4-11 | JPY geometry | `BLOCKED` | — | R3 predecessor |
| R4-12 | non-JPY geometry | `BLOCKED` | — | R3 predecessor |
| R4-13 | Broker stop/freeze-level handling | `BLOCKED` | — | R3 predecessor |
| R4-14 | Targetless lifecycle payload guard | `BLOCKED` | — | R3 predecessor |
| R4-15 | RR non-manufacture | `BLOCKED` | — | R3 predecessor |
| R4-16 | Source-owner mismatch fail-closed | `BLOCKED` | — | R3 predecessor |

---

# 10. R5 tracker — TradeLock + cumulative risk + P3/ambiguity

Authority: `R3_R6_CONSOLIDATED_BROKER_RUNTIME_ACCEPTANCE_MATRIX_PREP_20260826.md`

| Case | Scenario | Status | Evidence / bundle | Notes |
|---|---|---|---|---|
| R5-00 | TradeLock mode attribution | `BLOCKED` | — | R4 predecessor |
| R5-01 | TradeLock allow case | `BLOCKED` | — | R4 predecessor |
| R5-02 | TradeLock block case | `BLOCKED` | — | R4 predecessor |
| R5-03 | Opposite-direction integrity | `BLOCKED` | — | R4 predecessor |
| R5-04 | Sequential risk decision A | `BLOCKED` | — | R4 predecessor |
| R5-05 | Decision B sees A consumed budget | `BLOCKED` | — | R4 predecessor |
| R5-06 | REJ_TOTAL_RISK arithmetic | `BLOCKED` | — | R4 predecessor |
| R5-07 | No phantom reservation | `BLOCKED` | — | R4 predecessor |
| R5-08 | Existing-risk resolution fail-closed | `BLOCKED` | — | R4 predecessor |
| R5-09 | Portfolio limit positive rejection | `BLOCKED` | — | R4 predecessor |
| R5-10 | P3 Test B — frozen-state log suppression | `BLOCKED` | — | R4 predecessor |
| R5-11 | P3 Test C — fresh post-P0 EXEC_ID | `BLOCKED` | — | R4 predecessor |
| R5-12 | P3 Test D — restart after fresh persisted trade | `BLOCKED` | — | R4 predecessor |
| R5-13 | Execution hash uniqueness | `BLOCKED` | — | R4 predecessor |
| R5-14 | Broker comment stripped/blank | `BLOCKED` | — | R4 predecessor |
| R5-15 | Error 128 timeout ambiguity | `BLOCKED` | — | controlled/safe evidence |
| R5-16 | Other retryable errors | `BLOCKED` | — | controlled/safe evidence |
| R5-17 | Ambiguous-result reconciliation | `BLOCKED` | — | R4 predecessor |
| R5-18 | Hard-invalid recovery separation | `BLOCKED` | — | natural or deterministic case |
| R5-19 | Emergency precedence over frozen/normal management | `BLOCKED` | — | safe demo evidence only |
| R5-20 | Dashboard/registry exact-owned consistency | `BLOCKED` | — | R4 predecessor |

---

# 11. R6 tracker — N1/N2 forward chain + N3 firewall

Authority: `R3_R6_CONSOLIDATED_BROKER_RUNTIME_ACCEPTANCE_MATRIX_PREP_20260826.md`

| Case | Scenario | Status | Evidence / bundle | Notes |
|---|---|---|---|---|
| R6-00 | N1 observation present | `BLOCKED` | — | R5 predecessor |
| R6-01 | N2 validated decision shadow | `BLOCKED` | — | R5 predecessor |
| R6-02 | N2 closed outcome shadow | `BLOCKED` | — | R5 predecessor |
| R6-03 | End-to-end one-ticket chain | `BLOCKED` | — | R5 predecessor |
| R6-04 | Direction invariance | `BLOCKED` | — | R5 predecessor |
| R6-05 | Duplicate decision observation | `BLOCKED` | — | R5 predecessor |
| R6-06 | Restart continuity | `BLOCKED` | — | R5 predecessor |
| R6-07 | Closed-history reconciliation | `BLOCKED` | — | R5 predecessor |
| R6-08 | Identity ambiguity fail-closed | `BLOCKED` | — | controlled/natural evidence |
| R6-09 | Multiple simultaneous tracked trades | `BLOCKED` | — | R5 predecessor |
| R6-10 | N3 execution policy is NONE | `BLOCKED` | — | R5 predecessor |
| R6-11 | N3 cannot alter entry | `BLOCKED` | — | R5 predecessor |
| R6-12 | N3 cannot alter sizing/risk | `BLOCKED` | — | R5 predecessor |
| R6-13 | N3 cannot alter SL/TP/lifecycle | `BLOCKED` | — | R5 predecessor |
| R6-14 | Observer remains read-only | `BLOCKED` | — | R5 predecessor |
| R6-15 | Bundle assertion integrity | `BLOCKED` | — | R5 predecessor |
| R6-16 | Forward sample incompleteness handling | `BLOCKED` | — | R5 predecessor |

---

# 12. P0 handoff rule

The first status transition in this tracker occurs only after Issue #94 runtime acceptance:

1. fresh v4.59 EA-created HFM demo order;
2. `[P3S5][EXEC_ID]` proves durable local persistence (`Persist=PASS`, `Local=Y` or exact accepted equivalent);
3. broker comment may be blank/replaced without invalidating local identity;
4. restart same MT4 terminal/EA while trade remains live;
5. exact ticket recovers without identity-missing freeze caused only by broker comment loss;
6. same DecisionID/execution hash does not create a duplicate ticket;
7. P0 is integrated from latest `d1-owner-dev`, protected-surface regression passes, official MetaEditor is 0E0W, and post-P0 tooling is re-baselined.

Only then should R1 cases move from `BLOCKED` to `INCOMPLETE` as runtime collection begins.

## 13. Sequential release rule

Formal stage release remains:

- P0 accepted -> R1 may run;
- R1 formally closed -> R2 may be formally closed;
- R2 formally closed -> R3;
- R3 -> R4;
- R4 -> R5;
- R5 -> R6.

Evidence from later stages may be collected opportunistically during the same authenticated demo lineage, but it must not be used to skip formal predecessor closure.

## 14. Safety boundary

Do not force dangerous broker conditions merely to turn rare emergency/negative cases into PASS. Controlled demo fixtures or naturally occurring evidence are acceptable. Otherwise the correct state is `INCOMPLETE`.

No runtime evidence from hosted/disconnected/unauthenticated MT4 may be promoted to broker-runtime PASS.

## 15. Preparation verdict

**MASTER R1–R6 TRACKER READY — 115 CASES INDEXED.**

Current formal state remains:

`P0 BLOCKED -> R1 BLOCKED -> R2 BLOCKED -> R3 BLOCKED -> R4 BLOCKED -> R5 BLOCKED -> R6 BLOCKED`

The only executable project gate remains the fresh v4.59 HFM demo EXEC_ID persistence + restart + duplicate-protection validation for Issue #94.
