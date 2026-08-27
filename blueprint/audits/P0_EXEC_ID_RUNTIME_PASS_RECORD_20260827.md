# P0 EXEC_ID HFM Runtime PASS Record

Date: 2026-08-27  
Branch: `p0-exec-id-persistence-fix`  
Issue: #94  
Build under test: `Version 4.5.9 - P0 Execution Identity Persistence Fix` / `#property version "4.59"`  
Environment: authenticated HFM demo MT4, same terminal installation across restart  
Verdict: **P0 BROKER-RUNTIME PASS / READY FOR POST-P0 INTEGRATION**

## 1. Scope

This record preserves the operator-observed HFM demo evidence for the P0 execution-identity persistence defect. It does not modify EA source, lifecycle gates, BBMA strategy, SL/TP, MM/risk or canonical development state.

Raw screenshots were supplied by the operator during the authenticated runtime session. This file is the repository transcript of the visible evidence used for the PASS decision.

## 2. Build identity

Observed terminal initialization identified the tested EA as:

- `BBMA EA V4.5.9 P0 EXEC_ID Persistence Fix`
- initialization successful;
- HFM demo environment;
- default lifecycle activation was not changed for this test.

Isolated P0 source identity already locked by the branch:

- implementation commit: `03c4c3b90abbc6f669a89b1379218a26c5a57369`;
- source blob: `dc83e62748c93171d89a312e9f7a53c06d97e261`.

## 3. Fresh qualifying EA-created trade

Observed fresh EA-created order:

- ticket: `484701907`;
- pair: `CHFJPY`;
- direction: `SELL`;
- lot: `0.13`;
- open time shown in Trade tab: `2026.08.27 02:15:04`;
- open price: `197.789`;
- SL: `197.894`;
- TP: `197.694`;
- broker comment shown in Trade tab: `BBMA|H:7AADB1796BF36399`.

Visible fresh execution-identity fields:

```text
[P3S5][EXEC_ID] Ticket=484701907 Pair=CHFJPY Persist=PASS Local=Y BrokerHashFound=Y BrokerHashMatch=Y ExpectedHash=7AADB1796BF36399 BrokerHash=7AADB1796BF36399 RawLen=23
```

Immediate acceptance:

- `Persist=PASS` — PASS;
- `Local=Y` — PASS;
- broker hash found — YES;
- broker hash matches expected hash — YES;
- compact broker comment length — `23`;
- execution hash — `7AADB1796BF36399`.

## 4. Restart recovery

The exact ticket was intentionally kept live. MT4/EA was fully restarted in the same installation.

Visible post-restart recovery line:

```text
[P3S5][RECOVERY] Ticket=484701907 Pair=CHFJPY State=REC_IDENTITY_HASH_ONLY Cause=EXECUTION_HASH_ONLY HashFound=Y FullMeta=N
```

This is an explicitly accepted healthy ordinary-trade recovery outcome under the P0 runtime operator card.

Observed post-restart Trade tab:

- exact same ticket `484701907` still live;
- same `CHFJPY` SELL `0.13` order;
- same original open time and execution geometry;
- compact comment still identifies hash `7AADB1796BF36399`;
- only one live row for this execution was visible.

## 5. Duplicate-protection observation

No second live ticket for execution hash `7AADB1796BF36399` was visible after restart. The surviving live order remained ticket `484701907`.

Result: **NO DUPLICATE OBSERVED**.

## 6. Acceptance matrix

| Requirement | Result |
|---|---|
| Fresh order created by v4.59 P0 EA | PASS |
| `[P3S5][EXEC_ID] Persist=PASS` | PASS |
| Durable local identity `Local=Y` | PASS |
| Broker hash matches expected hash | PASS |
| Same ticket kept live through restart | PASS |
| Same-terminal restart performed | PASS |
| Exact ticket recovered | PASS |
| Recovery avoided `REC_IDENTITY_MISSING_FROZEN` | PASS |
| Healthy `REC_IDENTITY_HASH_ONLY` observed | PASS |
| No second ticket for same execution hash observed | PASS |

## 7. Runtime verdict

**P0 BROKER-RUNTIME PASS.**

The original oversized-comment defect is no longer reproduced by this fresh v4.59 HFM demo sequence. Durable local execution identity survived the same-terminal restart and the exact live ticket was recovered without identity-missing freeze or duplicate execution.

This PASS releases the post-P0 integration worksheet beginning at IP-01. It does **not** by itself authorize direct merge to `main`, lifecycle-gate activation, or Issue #94 closure before the canonical integration/compile/regression gates defined in the worksheet are completed.
