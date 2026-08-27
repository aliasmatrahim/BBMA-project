# R2 C044 Broker Runtime Acceptance Matrix — PREP ONLY

Date: 2026-08-26  
Preparation branch: `p0-exec-id-persistence-fix`  
Status: **PREPARED / NOT AUTHORIZED TO RUN UNTIL P0 #94 PASSES, POST-P0 TOOLING IS RE-BASELINED, AND R1 PREDECESSOR GATE IS CLOSED**

## 1. Purpose

Prepare the exact authenticated MT4 demo/broker acceptance matrix for the approved C044 post-Re-Entry failed-Momentum lifecycle.

This record is documentation/test preparation only. It does not modify `blueprint/source/BBMA_EA.mq4`, does not enable C044, does not change BBMA entry logic, SL/MM/risk rules, M20 authority, detector ownership, or merge anything into `d1-owner-dev`.

## 2. Predecessor gates — hard block

R2 execution must not start until:

1. P0 EXEC_ID Issue #94 passes fresh-order + restart + duplicate-protection runtime acceptance;
2. the accepted P0 delta is integrated onto the latest canonical `d1-owner-dev` history;
3. exact integrated source compiles with official MetaEditor at 0 errors / 0 warnings;
4. post-P0 runtime tooling is re-baselined to the exact integrated source identity and its native/self-test matrix passes;
5. R1 D1 TP-Wajib runtime gate has been processed according to the canonical runtime order and has no unresolved blocker that would invalidate R2 evidence attribution.

Until then this matrix is **READY BUT BLOCKED**.

## 3. Governing C044 semantics

The accepted bounded sequence is:

`VALID DIRECTION -> VALID RE-ENTRY -> CONTINUATION TO/TEST OF DIRECTION-SIDE OUTER BB -> CLOSED-CANDLE MOMENTUM TEST`

Then:

- outer-BB test + source-valid same-direction Momentum -> continuation survives and lifecycle enters `LIFE_WAIT_NEXT_REENTRY`;
- outer-BB test + no source-valid same-direction Momentum -> latch `EXIT_C044_FAILED_MOMENTUM` and close the existing position;
- later valid same-direction Re-Entry on the same frozen lifecycle-owner timeframe -> create a newer epoch and return to `LIFE_WAIT_OUTER_TEST`;
- opposite reversal-confirmed/mature Extreme on the same lifecycle-owner timeframe -> latch `EXIT_CYCLE_SUPERSEDED` and close the old-cycle position;
- no C044 close event creates automatic opposite-entry authority.

Explicitly forbidden interpretations include first-post-Re-Entry non-Momentum immediate close, one-candle/fixed-count timeout, guaranteed reversal, automatic opposite order, lower-timeframe shortcuts, fixed-pip/RR-manufactured TP, or weakening broker hard SL/M20 protection.

## 4. Lifecycle ownership / module invariants

For a C044-managed position:

- lifecycle owner = exact frozen Re-Entry source component/timeframe selected by the executable decision;
- M17 = structural hard-SL resolution + targetless payload classification/validation;
- M22 = approved execution transport, with hard SL and `TP=0` for C044-managed payloads;
- M23 = normal C044 exit latch/full-close executor; it must consume canonical events and must not recreate M08/M10/M12 formulas;
- M24 = lifecycle persistence/recovery/replay state owner;
- M20 = emergency-close precedence;
- M15 remains the final authority for any new entry;
- re-arm is position management only and must never create another broker order by itself.

C044 and D1TPW must not both own one targetless position.

## 5. Required R2 test profile

Dedicated test-only R2 profile after post-P0 re-baseline:

- authenticated broker/demo MT4 session;
- exact integrated canonical source identity recorded;
- exact EX4 and variant SHA-256 recorded;
- `EnableD1TPWLifecycle = false`;
- `EnableC044Lifecycle = true`;
- `MinRRRatio = 0` for normal targetless acceptance scenarios;
- debug/observer level sufficient to capture M17, owner-TF Re-Entry/Momentum/Extreme events, P3 execution identity, M23 close/latch state and M24 checkpoint/recovery/replay;
- non-production demo risk only.

Never run both lifecycle gates ON in the normal R2 profile.

## 6. Evidence identity required for every executable case

Record at minimum:

- canonical commit / source blob / MQ4 SHA-256 / build / property version;
- test variant SHA-256 and exact gate states;
- broker/server and demo classification;
- ticket, pair, magic, direction, open time;
- DecisionID / execution hash;
- executable family and exact frozen Re-Entry source component;
- lifecycle-owner timeframe + Re-Entry validation/confirmation candle;
- structural hard SL and broker TP at open;
- C044 checkpoint fields, current state, epoch and processed owner-TF cursor;
- replay seed identity when restart/replay is involved;
- canonical Momentum/Re-Entry/mature-Extreme evidence used by lifecycle evaluation;
- exit reason/latch candle and broker close/history result;
- recovery state across restart.

Evidence without exact build/ticket/owner/epoch attribution is insufficient.

## 7. R2 acceptance matrix

| Case | Scenario | Required positive evidence | PASS condition | FAIL condition |
|---|---|---|---|---|
| R2-00 | Gate-OFF control | baseline with C044 OFF and ordinary approved Re-Entry-owned trade path | current non-C044 behavior remains attributable; no dormant C044 lifecycle close authority fires | C044 event/latch/close executes while gate is OFF |
| R2-01 | Targetless initial payload | C044 ON, D1TPW OFF, valid Re-Entry-owned execution | valid hard SL, broker TP=0, C044-managed flag/checkpoint present, exact frozen owner identity | static outer-BB TP remains as competing normal exit, hard SL missing, wrong/ambiguous lifecycle owner |
| R2-02 | Frozen owner identity | record executable Re-Entry source component/timeframe and later lifecycle events | owner timeframe remains the exact frozen selected Re-Entry owner for the lifecycle/epoch | M23 hard-codes another TF or lower-TF structures override the frozen owner |
| R2-03 | Restart checkpoint recovery | live C044 ticket + checkpoint + replay seed, then full terminal/EA restart | same ticket reconstructs normally (normally `REC_NORMAL`) with direction/owner/epoch/cursor/identity intact | wrong ticket, identity loss, fabricated lifecycle state, unjustified freeze or duplicate entry |
| R2-04 | Deterministic multi-candle replay | restart/offline gap spans multiple fully closed owner-TF candles | every missed closed owner candle is replayed oldest -> newest through canonical producer logic exactly once | skip/reorder/forming-candle use, duplicated event, or guessed missing history |
| R2-05 | Missing/corrupt replay fail-frozen | controlled negative test for replay seed/history/cursor corruption or absence | affected lifecycle freezes safely and does not invent Re-Entry/Momentum/Extreme history | recovery guesses an event/cursor/owner and continues normal management |
| R2-06 | BUY failed-Momentum close | BUY owner-TF closed candle tests current Top BB after valid epoch but has no source-valid BUY Momentum | same ticket latches `EXIT_C044_FAILED_MOMENTUM` and M23 full-closes it | close before outer test/closed candle, wrong direction side, no close after proven event, or partial close |
| R2-07 | SELL failed-Momentum close | SELL owner-TF closed candle tests current Low BB with no source-valid SELL Momentum | same ticket latches failed-Momentum exit and M23 full-closes it | wrong-side/event timing, no close after proof, or partial close |
| R2-08 | No one-candle timeout | post-Re-Entry owner candles that do not test direction-side outer BB and are not exit events | lifecycle remains `LIFE_WAIT_OUTER_TEST`; elapsed bars alone do not close | first non-Momentum candle or arbitrary bar count causes close |
| R2-09 | Valid Momentum survives | closed owner-TF outer-BB test has canonical same-direction Momentum | trade stays open and enters `LIFE_WAIT_NEXT_REENTRY` | trade closes as failed Momentum despite canonical same-direction Momentum |
| R2-10 | WAIT_NEXT_REENTRY hold semantics | ordinary/additional same-direction Momentum/outer interactions while waiting for next RE | no timeout and no generic outer-BB-touch exit; position remains managed/open unless a separately approved exit event occurs | candle count/time or generic touch closes position |
| R2-11 | Same-direction Re-Entry re-arm | later fresh confirmed same-direction Re-Entry on exact lifecycle-owner TF | newer epoch is created and lifecycle returns `LIFE_WAIT_OUTER_TEST` with new anchor | no epoch advance, wrong owner TF, or stale epoch retained |
| R2-12 | Re-arm creates no new broker order | observe R2-11 through M15/M22/P3 identities | re-arm changes management epoch only; ticket count/DecisionID execution does not increase solely from re-arm | re-arm directly opens/adds an order outside normal entry pipeline |
| R2-13 | Opposite mature Extreme supersession | opposite reversal-confirmed/mature Extreme on same owner TF while C044 state is non-latched | same old ticket latches `EXIT_CYCLE_SUPERSEDED` then full-closes | raw/unconfirmed Extreme closes it, lower-TF Extreme closes higher-owner trade, or no close after valid mature event |
| R2-14 | Lower-TF shortcut rejection | opposite-looking lower-TF structure occurs while lifecycle owner is higher TF | lower-TF structure alone does not terminate higher-owner C044 lifecycle | lower-TF shortcut directly closes the position |
| R2-15 | No automatic opposite entry | observe failed-Momentum/cycle-superseded close and subsequent processing | close event does not manufacture opposite order; any later opposite order has a separate valid M15-authorized DecisionID | opposite trade appears as direct consequence of lifecycle close |
| R2-16 | M20 emergency precedence | controlled demo condition where M20 emergency closure competes with/arrives before C044 normal close | M20 wins and no second competing M23 broker close is issued | C044 races/overrides M20 or duplicate close occurs |
| R2-17 | Close idempotency | after C044 exit latch/close, continue cycles and preferably restart | one latch / one broker full-close for exact ticket; closed checkpoint state cannot re-close | repeated close intent/broker close or duplicate execution identity |
| R2-18 | D1TPW mutual exclusion | inspect R2 targetless ticket flags/checkpoints | C044 owns targetless lifecycle; D1TPW does not claim same ticket | dual lifecycle ownership continues normally instead of failing safe |
| R2-19 | Dual/missing lifecycle checkpoint fail-safe | controlled negative recovery test only | dual C044+D1TPW or otherwise irreconcilable targetless identity fails frozen, never guesses owner | arbitrary owner chosen and management continues |
| R2-20 | MinRR targetless policy | compare C044 candidate with `MinRRRatio=0` and controlled `MinRRRatio>0` test | zero may proceed through normal gates; positive MinRR fails closed without invented reward coordinate | static/fake TP is retained merely to compute RR or positive MinRR silently bypassed |
| R2-21 | Fully-closed owner-TF evaluation | price tests outer BB intrabar/forming owner candle before that candle closes | no lifecycle state transition/close from forming-candle touch alone | C044 reacts to tick/forming candle instead of fully closed owner-TF evidence |
| R2-22 | Canonical Momentum ownership | capture C044 decision event alongside canonical M10/Core Momentum output | lifecycle result matches canonical `DetectCSM()`/owned output; no second Momentum formula in M23 | M23 computes an independent Momentum definition or disagrees with canonical producer |
| R2-23 | Canonical Re-Entry/Extreme ownership | capture re-arm and cycle-supersession against M12/M08 mature owner events | lifecycle consumes existing canonical producer state/replay functions | lifecycle recreates alternate Re-Entry/Extreme detector semantics |
| R2-24 | Static outer-BB TP non-coexistence | inspect all R2 C044-managed order opens | broker TP remains 0; outer BB acts as event boundary only | resting outer-BB broker TP remains and can race the closed-candle C044 test |
| R2-25 | C035 separation | pre-Re-Entry direction reaches outer BB without the required C044 post-Re-Entry lifecycle epoch | no C044 close is manufactured from the earlier C035 stage | pre-Re-Entry outer-BB event is incorrectly treated as C044 failed-Momentum exit |
| R2-26 | P0 execution identity survives R2 | fresh R2 ticket across restart and lifecycle processing | local durable execution hash/ticket identity remains unique and recoverable even if broker comment is blank | R2 regresses to broker-comment-only identity or duplicate DecisionID/ticket appears |

## 8. Exact BUY/SELL event semantics

For `LIFE_WAIT_OUTER_TEST` on a fully closed owner-timeframe candle later than the epoch Re-Entry anchor:

### BUY
- outer test: candle range reaches/tests the current same-candle Top BB structure;
- continuation survives only if that same closed candle has source-valid BUY Momentum from canonical Momentum authority;
- otherwise failed-Momentum exit may latch.

### SELL
- outer test: candle range reaches/tests the current same-candle Low BB structure;
- continuation survives only if that same closed candle has source-valid SELL Momentum;
- otherwise failed-Momentum exit may latch.

Do not replace the canonical Momentum authority with a test-local approximation.

## 9. Restart / replay procedure for R2-03..R2-05

For a valid C044-managed demo ticket:

1. record ticket, execution hash, frozen owner TF/Re-Entry anchor, state, epoch, cursor and replay-seed identity before restart;
2. preserve the ticket open;
3. restart EA/terminal completely on the same test environment;
4. capture new observer/start epoch and exact-ticket recovery state;
5. verify immutable fields reconstruct identically;
6. for multi-candle replay, allow one or more owner-TF candles to complete while the terminal cannot process them;
7. on recovery verify chronological oldest -> newest processing through canonical functions;
8. verify cursor advances once per processed candle and no duplicate execution/close occurs;
9. if exact history or replay seed cannot be proven, expected behavior is fail-frozen, not inference.

## 10. M20 safety boundary

Do not manufacture uncontrolled loss or use a real-money account merely to force R2-16. M20 precedence must be demonstrated using a controlled demo condition/test facility. If safe attributable evidence does not occur, classify the case `INCOMPLETE` rather than forcing PASS.

## 11. Existing v4.58 analyzer semantics to preserve after post-P0 re-baseline

The current runtime analyzer already recognizes core R2 evidence families. The post-P0 analyzer must preserve at least:

- `R2_CHECKPOINT_RESTART`: restart checkpoint/replay and exact-ticket normal recovery, with lifecycle freeze treated as failure for a normal positive case;
- `R2_FAILED_MOMENTUM_CLOSE`: latched C044 state + failed-Momentum reason + same ticket in closed history;
- `R2_MOMENTUM_REARM`: `WAIT_NEXT_REENTRY` followed by `WAIT_OUTER_TEST` with a newer epoch;
- `R2_CYCLE_SUPERSESSION`: cycle-superseded latch + same-ticket closed history;
- `R2_M20_PRECEDENCE` evidence indexing;
- execution-hash uniqueness across tickets;
- hosted/disconnected/unauthenticated evidence = `BLOCKED`;
- missing/invalid assertion references cannot create PASS.

The detailed R2-00..R2-26 matrix should extend these checks without weakening them.

## 12. Evidence status vocabulary

Use only:

- `PASS` — exact case positively demonstrated;
- `FAIL` — contradictory, unsafe or identity-invalid behavior observed;
- `INCOMPLETE` — authenticated runtime exists but required scenario has not occurred or evidence is insufficient;
- `BLOCKED` — predecessor gate or authenticated connected broker environment unavailable.

Never reinterpret `INCOMPLETE` or `BLOCKED` as PASS.

## 13. Mandatory R2 closure gate

R2 may be called **CLOSED / PASS** only when authenticated broker/demo evidence positively demonstrates at minimum:

1. C044 targetless hard-SL + TP=0 payload with exact frozen Re-Entry owner identity;
2. no competing static outer-BB broker TP in C044-managed execution;
3. restart checkpoint recovery and deterministic missed-owner-candle replay;
4. fail-frozen behavior for missing/corrupt replay/history/cursor identity;
5. BUY failed-Momentum close;
6. SELL failed-Momentum close;
7. valid Momentum -> `WAIT_NEXT_REENTRY` without close;
8. later same-direction Re-Entry -> newer epoch -> `WAIT_OUTER_TEST`;
9. re-arm does not create a new broker order;
10. opposite mature owner-TF Extreme -> cycle-superseded close;
11. no lower-TF shortcut / no raw-Extreme shortcut;
12. M20 emergency precedence;
13. close idempotency / no duplicate execution identity;
14. no automatic opposite entry;
15. C044/D1TPW mutual exclusion and fail-safe ambiguous recovery;
16. fully-closed owner-TF-only lifecycle evaluation;
17. canonical detector ownership preserved;
18. P0 durable EXEC_ID behavior remains intact across R2 restart.

If any mandatory scenario is `FAIL`, R2 fails. If required broker-authenticated scenarios have not occurred, R2 remains `INCOMPLETE`.

## 14. Historical implementation evidence boundary

Earlier C044 implementation stages already provide strong static/native/deterministic evidence, including:

- targetless M17/M22 plumbing with hard SL and TP=0 behind a gate;
- M24 checkpoint state and M23 idempotent close plumbing;
- canonical closed-owner event evaluation using existing BBMA detectors;
- deterministic oldest-to-newest multi-candle replay with fail-frozen behavior on missing/corrupt evidence;
- native MetaEditor 0E0W and deterministic self-test PASS at the recorded v4.56 stage.

Those records are prerequisites/background evidence only. They are not substitutes for the authenticated post-P0 broker/demo R2 evidence tied to the exact integrated build.

## 15. Preparation verdict

**R2 C044 TEST MATRIX READY. EXECUTION REMAINS BLOCKED BY P0/POST-P0 TOOLING AND PREDECESSOR R1 GATES.**

No MQL4 source patch, lifecycle activation, canonical merge or strategy-semantic change is performed by this preparation record.
