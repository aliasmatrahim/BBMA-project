# R1 D1 TP-Wajib Broker Runtime Acceptance Matrix — PREP ONLY

Date: 2026-08-26  
Preparation branch: `p0-exec-id-persistence-fix`  
Status: **PREPARED / NOT AUTHORIZED TO RUN UNTIL P0 EXEC_ID #94 PASSES AND A POST-P0 CANONICAL TEST BUILD EXISTS**

## 1. Purpose

Prepare the exact authenticated MT4 demo/broker acceptance matrix for the D1 Extreme TP-Wajib lifecycle so R1 can start immediately after the P0 execution-identity blocker is closed.

This record is documentation/test preparation only. It does not modify BBMA strategy logic, does not activate any lifecycle gate, and does not authorize a merge to `d1-owner-dev`.

## 2. Predecessor gate — hard block

R1 must not start until all P0 EXEC_ID acceptance conditions are PASS on a fresh v4.59 trade:

1. fresh order opened by the P0-fixed build;
2. immediate execution identity persistence reports `Persist=PASS` and local durable identity is present;
3. EA/terminal restart with that order live reconstructs the same ticket without identity-missing freeze caused only by broker-comment loss;
4. same DecisionID / execution hash cannot create a second ticket across restart;
5. Issue #94 is closed only after the above runtime evidence is recorded;
6. the exact P0 delta is integrated from the latest canonical `d1-owner-dev` head, protected-surface regression passes, and official MetaEditor compiles the exact integrated source at 0 errors / 0 warnings.

Until then, this R1 matrix is **READY BUT BLOCKED**.

## 3. Source contract being tested

R1 is governed by `blueprint/contracts/D1_EXTREME_TPW_LIFECYCLE_CONTRACT.md` for `D1_OPP_EXTREME_TPW` only.

Ownership invariants to preserve:

- `D1 EXTREME = TP SEMANTIC OWNER`;
- `FRESH LTF RE-ENTRY = ENTRY / DEDUP / HARD-SL STRUCTURAL OWNER`;
- `M15 = FINAL NEW-ENTRY AUTHORITY`;
- `M23 = NORMAL LIFECYCLE BROKER CLOSE OWNER`;
- `M24 = PERSISTENCE / RECOVERY OWNER`;
- `M20 = EMERGENCY PRECEDENCE`.

No R1 test may reinterpret generic Re-Entry/C044 rules as the D1 TP-Wajib lifecycle.

## 4. Important tooling re-baseline requirement discovered during prep

The existing v4.58 runtime package is intentionally source-bound:

- `blueprint/tools/v458_runtime_variant_builder.py` requires canonical Git blob `5c1b93d7783a00877cb7fd233673ca1ac1340151` and SHA-256 `6fd9eb52b63dee8861ebf205b1c031d80646b58e0b4941ef21ece9431fe6be5a`;
- `blueprint/tools/v458_runtime_analyzer.py` is also bound to the older v4.58 source identity;
- its R1 profile is `R1_D1TPW = D1TPW ON / C044 OFF`.

Therefore, after P0 v4.59 is accepted and integrated, **do not reuse the current v4.58 builder/analyzer unchanged**. They must first be re-baselined to the exact new canonical source blob/SHA/build identity and re-self-tested. Re-baselining may update only source/build identity bindings and test packaging needed for the already-approved R1 profile; it must not change R1 strategy semantics.

This is a preparation dependency, not a reason to modify the current frozen canonical source now.

## 5. Required post-P0 R1 test profile

Dedicated test-only profile:

- authenticated broker/demo MT4 session;
- exact post-P0 canonical integrated source identity recorded;
- exact EX4 produced from that source;
- `EnableD1TPWLifecycle = true` in the test-only R1 variant;
- `EnableC044Lifecycle = false`;
- `MinRRRatio = 0` for targetless lifecycle acceptance;
- Mode 2 for D1 Opportunity execution;
- debug/telemetry level sufficient to capture M17, D1/D1O, P3 execution, M23/M24 lifecycle/recovery and observer records;
- runtime observer attached on a separate chart if the re-baselined package retains the existing observer architecture;
- demo risk kept non-production and controlled.

Never run both lifecycle gates ON in the normal R1 acceptance profile.

## 6. Evidence identity to record for every executable R1 case

For each relevant ticket capture at minimum:

- canonical commit / Git blob / SHA-256 / build string / `#property version`;
- test-variant SHA-256 and gate state;
- broker/server + demo account classification;
- pair, ticket, magic, direction, open time;
- DecisionID / execution hash;
- D1 Opportunity family = `D1_OPP_EXTREME_TPW`;
- frozen D1 Extreme source / confirmation candle;
- selected fresh H1 Re-Entry identity used for entry/dedup/hard-SL provenance;
- hard SL and broker TP at order open;
- D1TPW lifecycle checkpoint identity;
- last processed fully closed D1 cursor;
- latch state / latched D1 candle if completion occurs;
- close time / close result;
- recovery state before and after any restart.

Evidence without exact build/ticket/identity attribution is not sufficient to close a case.

# 7. R1 test matrix

| Case | Scenario | Required positive evidence | PASS condition | FAIL condition |
|---|---|---|---|---|
| R1-00 | Gate-OFF fail-closed control | Baseline/test build with D1TPW OFF encounters valid `D1_OPP_EXTREME_TPW` candidate | candidate does not execute and does not receive legacy Re-Entry outer-BB TP fallback | order executes as legacy fixed-TP trade or silently falls back |
| R1-01 | Targetless initial payload | R1 profile ON/OFF = D1TPW/C044; fresh valid D1 EXTREME_TPW + H1 Re-Entry execution | market order has valid hard SL, broker TP=0, D1TPW-managed identity/checkpoint, C044 not owner | fixed outer-BB TP appears, hard SL missing, wrong lifecycle owner, or ambiguous targetless identity |
| R1-02 | Restart checkpoint recovery | live R1 ticket + persisted checkpoint, then full EA/terminal restart | exact ticket reconstructs as valid managed lifecycle, normally `REC_NORMAL`; source/cursor/ticket/magic/direction remain consistent | identity/checkpoint is lost, wrong ticket attached, unjustified freeze, fabricated cursor/source, or duplicate entry |
| R1-03 | Missed-D1-candle replay | keep lifecycle trade live, create restart/offline interval spanning one or more completed D1 candles | on recovery M23/M24 process missed fully closed D1 candles oldest -> newest from persisted cursor exactly once | replay skips/reorders candles, uses forming D1 candle, duplicates event, or guesses missing history |
| R1-04 | BUY completion via MA5 High | D1 Extreme BUY trade, later fully closed D1 candle range reaches same-candle D1 MA5 High first/validly | first canonical TPW completion latches same ticket and M23 full-closes it | close occurs before fully closed D1 evidence, wrong MA side, partial close, or no close after proven canonical event |
| R1-05 | BUY completion via MA10 High | distinct BUY evidence where MA10 High is the qualifying canonical alternative | same-ticket full close from MA10 alternative proves MA10 path independently | MA10 path ignored or result cannot distinguish MA10 alternative |
| R1-06 | SELL completion via MA5 Low | D1 Extreme SELL trade, later fully closed D1 candle range reaches same-candle D1 MA5 Low | first canonical TPW completion latches same ticket and M23 full-closes it | close occurs on wrong side/current-forming candle, partial close, or no close after proven event |
| R1-07 | SELL completion via MA10 Low | distinct SELL evidence where MA10 Low is the qualifying canonical alternative | same-ticket full close from MA10 alternative proves MA10 path independently | MA10 path ignored or result cannot distinguish MA10 alternative |
| R1-08 | Dynamic MA semantics | record qualifying D1 candle OHLC + same-candle MA5/MA10 values used by lifecycle | evaluation uses MA values belonging to each closed D1 candle, not a frozen entry-time numeric TP | fixed entry-time TP coordinate is used as lifecycle completion authority |
| R1-09 | First-event latch / duplicate-close prevention | canonical completion occurs; keep logs through subsequent ticks/M15 clocks and preferably restart after latch/close | one lifecycle close intent/one broker close for the ticket; later processing/restart does not close again | duplicate close attempt, second lifecycle latch for same completed ticket, or duplicate ticket from same identity |
| R1-10 | No automatic opposite entry | observe completion close and immediate subsequent processing | TPW completion itself does not manufacture an opposite-direction entry | opposite entry is created as a direct consequence of TPW close without a separate valid M15 decision |
| R1-11 | C044 mutual exclusion | inspect targetless lifecycle checkpoint/flags for R1 ticket | D1TPW owns lifecycle; C044 is not owner and no C044 checkpoint claims the same position | both lifecycle families claim same targetless trade without fail-frozen handling |
| R1-12 | Ambiguous dual-checkpoint fail-closed | controlled corruption/recovery test only if existing test tooling can create it safely; never manually corrupt a normal forward run | if both D1TPW+C044 checkpoint families appear for one targetless ticket, recovery fails frozen and never guesses owner | recovery chooses one owner arbitrarily or continues normal management |
| R1-13 | Missing/corrupt checkpoint fail-closed | controlled negative recovery test only | missing/corrupt/ambiguous targetless lifecycle identity freezes the affected trade safely; no fabricated source/cursor | EA reconstructs guessed lifecycle identity and manages/closes from fabricated state |
| R1-14 | M20 emergency precedence | controlled demo scenario or existing deterministic test facility produces an M20 emergency close condition while D1TPW close is also potentially actionable | M20 emergency liquidation wins; M23 normal lifecycle does not issue a competing/duplicate close | normal lifecycle close races/precedes M20 or duplicate broker close occurs |
| R1-15 | No legacy outer-BB TP fallback | inspect all R1 EXTREME_TPW executions and gate-OFF control | R1 managed order TP remains 0; gate-OFF candidate fails closed | generic selected-Re-Entry outer-BB broker TP is substituted |
| R1-16 | Fully-closed-D1-only timing | observe intraday/current D1 price touch before D1 close and subsequent completed D1 processing | forming D1 candle touch does not close; canonical completion is evaluated only after D1 candle is fully closed on existing M15 processing clock | lifecycle closes from current/forming D1 candle or tick-level touch alone |

## 8. Alternative MA-path coverage rule

One D1 candle may touch both MA5 and MA10. That proves a valid completion event but **does not by itself prove both alternative code paths independently**.

Runtime closure should obtain distinct attributable evidence for MA5 and MA10 alternatives across BUY/SELL cases where practical. If authenticated runtime has not naturally produced a distinct alternative case, status is `INCOMPLETE`, not PASS and not a strategy defect.

## 9. Restart sequence for R1-02 / R1-03

For the accepted runtime candidate:

1. record live ticket + execution hash + D1TPW checkpoint + current closed-D1 cursor;
2. preserve the ticket open;
3. restart the EA/terminal completely;
4. record startup/recovery epoch and exact-ticket recovery state;
5. verify checkpoint fields reconstruct consistently;
6. for missed-candle replay, the terminal must actually miss one or more D1 closes before restart/reconnect;
7. verify replay order oldest -> newest and cursor advancement;
8. verify no duplicate entry and no duplicate close intent.

A restart test without a pre-restart identity/checkpoint snapshot is insufficient evidence.

## 10. M20 precedence safety rule

Do not endanger a live/real account or deliberately create uncontrolled loss merely to force R1-14.

R1-14 must be demonstrated only on demo through a controlled configuration/test facility where the evidence can be attributed clearly. If no safe controlled occurrence is available, retain the case as `INCOMPLETE`; do not manufacture a PASS.

## 11. Expected analyzer classifications

Reuse the existing status vocabulary:

- `PASS` — the exact case is positively demonstrated;
- `FAIL` — contradictory/unsafe/identity-invalid behavior is observed;
- `INCOMPLETE` — authenticated runtime exists but the case has not produced enough evidence;
- `BLOCKED` — no authenticated connected broker session or predecessor P0 gate is not closed.

`INCOMPLETE` and `BLOCKED` must never be promoted to PASS.

## 12. Existing analyzer semantics to preserve when re-baselining

The current v4.58 analyzer already checks important R1 invariants that should be preserved in its post-P0 re-baseline:

- `R1_CHECKPOINT_RESTART`: requires at least two observer START epochs plus checkpoint evidence and exact-ticket `REC_NORMAL`, and fails on D1TPW lifecycle freeze;
- `R1_TPW_COMPLETION_CLOSE`: requires a latched D1TPW state followed by the same ticket appearing in closed history;
- execution-hash identity check fails if one execution hash maps to multiple tickets;
- hosted/disconnected/unauthenticated bundles are `BLOCKED`;
- assertion references must point to actual raw log evidence.

The re-baseline should extend/index the detailed R1-00..R1-16 cases without weakening these existing checks.

## 13. Mandatory R1 closure gate

R1 can be called **CLOSED / PASS** only when authenticated broker/demo evidence positively proves, at minimum:

1. gate-OFF fail-closed and no legacy outer-BB fallback;
2. targetless hard-SL + TP=0 managed execution under R1 profile;
3. exact-ticket checkpoint restart recovery;
4. missed-D1-candle replay;
5. BUY TP-Wajib completion close;
6. SELL TP-Wajib completion close;
7. MA5 and MA10 alternative completion paths;
8. duplicate-close prevention / idempotency;
9. M20 emergency precedence;
10. no C044/D1TPW lifecycle ambiguity;
11. no automatic opposite entry from the close event;
12. fully-closed-D1-only evaluation;
13. no duplicate execution identity across tickets.

If any mandatory scenario is `FAIL`, R1 fails. If any mandatory scenario has not occurred, R1 remains `INCOMPLETE` rather than being force-closed.

## 14. Post-R1 action boundary

Even after R1 broker/demo PASS:

- do not silently enable D1TPW in production/default canonical source;
- record a dedicated R1 closure audit tied to exact source/EX4/runtime bundle identities;
- require an explicit project activation decision before changing the default lifecycle gate;
- then proceed to R2 C044 runtime gate according to the canonical runtime queue.

## 15. Preparation verdict

**R1 TEST MATRIX READY. EXECUTION REMAINS BLOCKED BY P0 #94.**

No source patch, lifecycle activation, canonical merge or strategy-semantic change is performed by this preparation record.
