# Interim Runtime Evidence Harvest — 2026-09-08

## Classification
SUPPLEMENTAL RUNTIME EVIDENCE / NO FORMAL STAGE CLOSURE / NO EA SOURCE CHANGE.

This record harvests already-existing authenticated/local runtime logs while the isolated C10 Build 4.81 physical-restart acceptance waits for a genuine ACTIVE shadow. It must not bypass the predecessor ordering in `MASTER_R1_R6_RUNTIME_EVIDENCE_INDEX_20260827.md`.

## Governance boundary
- Active implementation owner remains `d1-owner-dev` at `c3318c20970b9c4413b75b46e01976a6e511bf92` at audit time.
- Canonical EA path remains `blueprint/source/BBMA_EA.mq4`.
- No Strategy Core, risk/MM, execution, lifecycle or canonical EA source change is made by this audit.
- C10 Build 4.81 isolated runtime remains `Authority=NONE`, trading disabled / zero trade caps.

## 1. Build 4.81 D1-owner observation
Isolated Build 4.81 runtime log `20260908.log` contained 690 `[D1-03][OWNER]` observations at the sampled point:
- `D1_OWNER_BUY_CONFIRMED`: 344;
- `D1_OWNER_SELL_CONFIRMED`: 346;
- `D1_TRANSITION`: 0 in this exact Build 4.81 sample;
- `D1_OWNER_UNRESOLVED`: 0 in this exact Build 4.81 sample.

Older mixed-build primary logs contain at least three genuine `D1_TRANSITION` observations, but mixed-build evidence is not promoted to formal R3 acceptance. R3 remains predecessor-blocked and the UNRESOLVED case remains unobserved.

## 2. M17 structural-SL resolver runtime observations
Build 4.81 produced runtime resolver traces including:
- GBPJPY SELL: raw spread 2.5 pip -> rounded buffer 3.0 pip; StructuralSL 209.020 -> FinalBrokerSL 209.050.
- USDJPY SELL: raw spread 0.3 pip -> minimum buffer 2.0 pip; StructuralSL 153.366 -> FinalBrokerSL 153.386.
- USDCAD SELL: raw spread 0.1 pip -> minimum buffer 2.0 pip; StructuralSL 1.38121 -> FinalBrokerSL 1.38141.
- AUDUSD BUY: SpreadBufferPips 0.0; StructuralSL and FinalBrokerSL both 0.72138.
- EURUSD BUY: SpreadBufferPips 0.0; StructuralSL and FinalBrokerSL both 1.16229.

These traces support BUY-unchanged / SELL-buffer arithmetic and JPY/non-JPY runtime calculation. Because the isolated Build 4.81 runtime has no broker execution authority, they are resolver-runtime evidence only, not R4 broker-order acceptance.

## 3. F6 timing evidence remains provenance-limited
A v4.59 runtime example exists:
- DecisionID `CADJPY|2026.09.04 09:00|2|7|6CBB56ECF1A66D3C`;
- `[P3M2][PREFLIGHT_START]` ValidateCandle 09:00 / ProcessTime 09:15;
- ticket `1622728534` executed;
- `[P3M2][EXEC]` reported OrderOpen 09:15;
- later scans at 09:30 and 09:45 rejected the same DecisionID as `REJ_DUPLICATE`.

This is useful supporting chronology/dedup evidence, but it does NOT close CORE-V2-F6 because Issue #132 proves the current EXEC `OrderOpenTime()` field can depend on ambient selected-order state after registry compaction. Exact-ticket open-time telemetry must be fixed and re-run.

## 4. Execution-identity / restart observations
Multiple fresh v4.59 and v4.61 executions emitted `[P3S5][EXEC_ID] ... Persist=PASS Local=Y BrokerHashFound=Y BrokerHashMatch=Y`.
Ticket `1622779145` (GBPJPY) was opened under v4.59 with hash `0CEB014D0A39A3E9` and later reconstructed by v4.61 with `[P3S5][RECOVERY] ... State=REC_IDENTITY_HASH_ONLY Cause=EXECUTION_HASH_ONLY HashFound=Y`.

This demonstrates durable hash observation across a later reload/build transition, but it is not substituted for any formal same-build restart case whose matrix requires exact build attribution.

## 5. TradeLock / cumulative-risk runtime status
No `REJ_TRADE_LOCK` or `REJ_TOTAL_RISK` occurrence was found in the sampled 2026-09-02 through 2026-09-08 primary logs. Therefore no new runtime PASS is claimed for TradeLock or sequential cumulative-risk admission.

## 6. F7 harvested evidence
`BBMA_F7_TELEMETRY.log` currently contains:
- HEARTBEAT: 661;
- RECOVERY_RESTORED: 2;
- EXIT_LATCHED: 1;
- CLOSE_SUCCESS: 1.

Observed close path is failed-Momentum; Momentum-hold, Re-Entry re-arm, opposite-CSM and cycle-supersession remain unobserved. Build attribution is additionally limited by Issues #127/#133.

## 7. C10 Build 4.81 gate status
At 2026-09-08 12:15 runtime checkpoint state was:
- SEEN: 6;
- ACTIVE: 0.

The physical-restart watcher remains waiting for a genuine ACTIVE shadow. No synthetic signal is manufactured to satisfy this gate.

## Verdict
Useful runtime evidence was harvested without changing trading authority, but no predecessor-blocked R3/R4/R5 case is promoted to PASS. Build 4.81 physical-restart closure, F6 exact-ticket telemetry, F7 missing lifecycle paths, TradeLock and cumulative-risk traces remain verification items.