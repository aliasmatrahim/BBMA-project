# P0 Runtime Operator Quick Card — PREP ONLY

Date: 2026-08-27  
Preparation branch: `p0-exec-id-persistence-fix`  
Status: **READY FOR HFM DEMO OPERATOR USE / DOCUMENTATION-ONLY / ISSUE #94 STILL OPEN**

## 1. Purpose

One-page operator card for the exact P0 EXEC_ID runtime acceptance test. Use this when a fresh v4.59 trade appears on authenticated HFM demo.

This card does not modify EA source, strategy, lifecycle gates, SL/TP, MM/risk or canonical branches.

## 2. Build identity — verify before accepting any evidence

Accepted candidate must identify itself as:

- `Version 4.5.9 - P0 Execution Identity Persistence Fix`
- `#property version "4.59"`
- P0 implementation commit: `03c4c3b90abbc6f669a89b1379218a26c5a57369`
- isolated P0 source blob: `dc83e62748c93171d89a312e9f7a53c06d97e261`
- D1TPW default gate: OFF
- C044 default gate: OFF

Preparation-time repository state:

- `d1-owner-dev`: `5a1e7785f88c2ea1bf8f38917df413cb9cfcfce7`
- `p0-exec-id-persistence-fix` head before this card: `044c13dbef192a00aaebf20bdd37ee536077eaf0`

Do not use an old v4.58 ticket as P0 proof.

## 3. Fresh-trade capture

When v4.59 opens a new demo trade automatically:

1. Record ticket, pair, direction, magic, open time.
2. Capture the exact `[P3S5][EXEC_ID]` line.
3. Record `ExpectedHash`, `BrokerHash`, `RawLen`, `RawComment`, `Persist`, `Local`.
4. Keep the trade open for restart validation.

### Immediate PASS condition

Required:

`Persist=PASS` **and** `Local=Y`

Broker result may be:

- `BrokerHashFound=Y`, or
- `BrokerHashFound=N`, including blank broker comment.

Blank broker comment is **not a P0 failure by itself** after the fix.

### Immediate FAIL condition

Any fresh v4.59 trade showing:

- `Persist=FAIL`, or
- `Local=N`, or
- durable identity cannot be tied to the exact ticket.

Action: stop acceptance. Do not integrate to `d1-owner-dev`.

## 4. Restart test

After immediate PASS:

1. Keep the exact fresh ticket live.
2. Record pre-restart ticket/hash snapshot.
3. Fully restart the EA/MT4 terminal in the **same MT4 installation**.
4. Capture startup/recovery logs, especially `[P3S5][RECOVERY]`.
5. Confirm the exact same ticket remains managed.

### Healthy recovery outcomes

For an ordinary non-lifecycle trade, recovery may be normal or hash-only, for example:

- `REC_NORMAL`, or
- `REC_IDENTITY_HASH_ONLY Cause=EXECUTION_HASH_ONLY HashFound=Y FullMeta=N`

Hash-only recovery is acceptable when durable local execution identity is valid.

### Restart FAIL conditions

Fail P0 if the fresh v4.59 ticket that previously had `Persist=PASS Local=Y` becomes:

- `REC_IDENTITY_MISSING_FROZEN`

**solely because broker comment is blank/replaced**, or if:

- wrong ticket is reconstructed;
- ticket/hash identity changes without a new decision;
- recovery fabricates missing identity;
- durable local identity disappears unexpectedly in the same terminal installation.

## 5. Duplicate-protection test

After restart, continue normal EA processing long enough to observe the same decision identity again if it is revisited.

PASS:

- same DecisionID / execution hash remains associated with one broker ticket only;
- no second live order is created for the same execution identity.

FAIL:

- same execution hash maps to multiple broker tickets without a separately approved new decision identity.

## 6. Evidence package to save

Minimum evidence for Issue #94 closure:

- screenshot/log proving v4.59 build identity;
- fresh order ticket details;
- fresh `[P3S5][EXEC_ID]` line;
- pre-restart ticket/hash snapshot;
- post-restart `[P3S5][RECOVERY]` line(s);
- current Orders/Trade view showing exact ticket after restart;
- evidence that no duplicate ticket exists for the same DecisionID/hash;
- broker comment evidence if blank/replaced, to show local persistence is authoritative.

Do not use old ticket `484600751` as proof of the fix.

## 7. PASS / FAIL decision tree

```text
Fresh v4.59 order opened automatically?
  NO  -> INCOMPLETE. Wait for a fresh qualifying demo trade.
  YES
   |
   v
[EXEC_ID] Persist=PASS AND Local=Y?
  NO  -> FAIL. Keep P0 isolated. Do not integrate.
  YES
   |
   v
Broker comment blank/replaced?
  YES -> Allowed. Continue; broker comment is secondary evidence.
  NO  -> Continue.
   |
   v
Keep exact ticket live and restart SAME terminal installation.
   |
   v
Exact ticket recovered with durable hash identity?
  NO  -> FAIL.
  YES
   |
   v
REC_IDENTITY_MISSING_FROZEN solely because broker comment missing?
  YES -> FAIL.
  NO
   |
   v
Same DecisionID/hash creates second ticket?
  YES -> FAIL.
  NO
   |
   v
P0 BROKER-RUNTIME PASS CANDIDATE
   |
   v
Attach evidence to #94 -> execute post-PASS integration worksheet.
```

## 8. Operator verdict block

Fill only after the full sequence:

- Build confirmed: `YES / NO`
- Fresh qualifying ticket: `____________`
- Pair/direction: `____________`
- Execution hash: `____________`
- Immediate `Persist=PASS`: `YES / NO`
- Immediate `Local=Y`: `YES / NO`
- Broker comment blank/replaced: `YES / NO`
- Same-terminal restart performed: `YES / NO`
- Exact ticket recovered: `YES / NO`
- `REC_IDENTITY_MISSING_FROZEN` caused solely by broker comment loss: `YES / NO`
- Duplicate ticket for same DecisionID/hash: `YES / NO`
- Raw evidence location: `____________`

Final P0 runtime verdict:

`PASS / FAIL / INCOMPLETE`

## 9. Next action by verdict

### If PASS

1. attach exact evidence to Issue #94;
2. do not jump straight to `main`;
3. execute `P0_POST_PASS_INTEGRATION_EXECUTION_WORKSHEET_20260827.md` from IP-01;
4. re-fetch latest `d1-owner-dev` first;
5. integrate cleanly, protected-surface regression, official 0E0W, tooling re-baseline, freeze canonical candidate;
6. then release R1 according to the prepared runtime queue.

### If FAIL

Keep `d1-owner-dev` unchanged. Diagnose/fix only on the isolated P0 branch, then repeat a fresh qualifying v4.59 demo trade test.

### If INCOMPLETE

Do not infer PASS. Wait for the missing fresh-trade/restart/duplicate evidence.

## 10. Safety boundary

Use authenticated HFM **demo** evidence only for this acceptance gate. Do not deliberately create uncontrolled loss or use real-risk positions merely to force a test scenario.

## 11. Final preparation verdict

**OPERATOR QUICK CARD READY.**

This is the final practical safe-mode operator aid before the real P0 broker-runtime gate. Further progress that changes source/integration state remains blocked until the fresh v4.59 HFM demo acceptance sequence passes.
