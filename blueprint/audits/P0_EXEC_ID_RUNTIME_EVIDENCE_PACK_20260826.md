# P0 EXEC_ID Broker Runtime Evidence Pack — PREP ONLY

Date: 2026-08-26  
Preparation branch: `p0-exec-id-persistence-fix`  
Issue: `#94 — P0: EXEC_ID persistence fails when broker strips oversized OrderComment`  
Status: **PREPARED / BROKER-DEMO EXECUTION PENDING / DOCUMENTATION-ONLY**

## 1. Purpose

Provide one minimal, exact evidence pack for closing P0 Issue #94 after a fresh v4.59 HFM demo trade is opened and the same MT4 terminal/EA is restarted while that trade remains live.

This document does not modify EA source, lifecycle gates, strategy logic, SL/TP, MM/risk, or canonical branches. It is evidence preparation only.

## 2. Exact candidate identity

Runtime acceptance must use the P0-fixed candidate, not an order created by v4.58 or an older build.

Expected source identity:

- build marker: `Version 4.5.9 - P0 Execution Identity Persistence Fix`;
- `#property version "4.59"`;
- implementation commit: `03c4c3b90abbc6f669a89b1379218a26c5a57369`;
- source blob used by the P0 branch after the implementation: `dc83e62748c93171d89a312e9f7a53c06d97e261`;
- D1TPW lifecycle gate: OFF;
- C044 lifecycle gate: OFF.

Later documentation-only commits on `p0-exec-id-persistence-fix` do not change this EA source identity. Before runtime evidence is accepted, confirm the attached EA still identifies itself as v4.59 P0 EXEC_ID Persistence Fix.

## 3. Hard rule: fresh v4.59 trade only

Do not use old ticket `484600751` or any order opened before the P0 fix as proof of success. If its original DecisionID was lost because the broker persisted a blank comment, v4.59 cannot reconstruct that historical DecisionID from nothing.

The qualifying order must be:

1. opened automatically by the v4.59 EA;
2. opened after the v4.59 build is attached and initialized;
3. still live when the restart test is performed;
4. kept in the same MT4 terminal installation for the restart test.

Terminal GlobalVariables are the durable same-terminal identity store for this issue. Moving the order to a different terminal/VPS installation is outside this P0 acceptance scope.

## 4. Evidence set A — build / session identity

Capture before waiting for the new trade:

- screenshot or log showing `BBMA EA V4.5.9 P0 EXEC_ID Persistence Fix` initialization/build identity;
- HFM account classified as demo;
- AutoTrading enabled;
- EA attached and active;
- date/time of test;
- terminal remains the same installation for pre/post-restart evidence.

If build identity is not v4.59 P0 EXEC_ID Persistence Fix, stop: evidence is invalid for #94.

## 5. Evidence set B — fresh execution persistence

When the EA opens a fresh order, capture the complete `[P3S5][EXEC_ID]` line for that ticket.

Expected shape:

```text
[P3S5][EXEC_ID] Ticket=<ticket> Pair=<pair> Persist=<PASS/FAIL> Local=<Y/N> BrokerHashFound=<Y/N> BrokerHashMatch=<Y/N> ExpectedHash=<16hex> BrokerHash=<...> RawLen=<n> RawComment=<...>
```

Mandatory fields to record:

| Field | Required acceptance |
|---|---|
| `Ticket` | fresh v4.59 broker ticket |
| `Pair` | matches broker order |
| `Persist` | **PASS** |
| `Local` | **Y** |
| `ExpectedHash` | present / non-empty 16-hex execution hash |
| `BrokerHashFound` | Y or N both acceptable |
| `BrokerHashMatch` | Y or N depending on broker comment; not authoritative |
| `RawComment` | may be compact hash comment, blank, or broker-modified |

### P0-B PASS

`Persist=PASS` **and** `Local=Y` for the fresh ticket.

A blank broker comment is allowed. `BrokerHashFound=N` is not a failure if the local durable identity is proven.

### P0-B FAIL

Any of:

- `Persist=FAIL`;
- `Local=N`;
- expected execution hash missing/invalid;
- fresh order cannot be tied to the v4.59 execution event.

If P0-B fails, stop closure and keep Issue #94 open.

## 6. Evidence set C — pre-restart snapshot

Before restarting MT4/EA, record:

- ticket;
- pair;
- direction;
- magic;
- open time;
- execution hash from the fresh `[EXEC_ID]` line;
- order is still live;
- no second live ticket already exists for the same execution identity.

Minimal pre-restart record:

```text
P0_PRE_RESTART
Ticket=
Pair=
Direction=
Magic=
OpenTime=
ExecutionHash=
LiveTicketCountForHash=1
```

Do not close the qualifying demo order before restart.

## 7. Evidence set D — full restart recovery

Perform a complete EA/terminal restart while the fresh ticket remains live.

After restart, capture initialization plus the exact `[P3S5][RECOVERY]` line for the same ticket.

Healthy ordinary v4.59 recovery may be `REC_NORMAL` when full recoverable metadata is present, or `REC_IDENTITY_HASH_ONLY` for an ordinary managed trade where durable execution identity is proven but full legacy metadata is unavailable.

A representative acceptable hash-only state is:

```text
[P3S5][RECOVERY] Ticket=<same-ticket> Pair=<same-pair> State=REC_IDENTITY_HASH_ONLY Cause=EXECUTION_HASH_ONLY HashFound=Y FullMeta=N ...
```

Acceptance requirements:

1. exact same broker ticket is recovered;
2. durable execution hash is found/recognized locally;
3. the fresh ticket does **not** become `REC_IDENTITY_MISSING_FROZEN` solely because `OrderComment()` is blank or stripped;
4. ticket/magic/open-time/direction guards remain consistent;
5. no fabricated identity is created.

### P0-D FAIL

Fail if a fresh ticket that previously had `Persist=PASS Local=Y` becomes:

```text
REC_IDENTITY_MISSING_FROZEN
```

with the only reason being missing/blank broker comment, or if the wrong ticket/identity is recovered.

A truly corrupt/mismatched identity may still fail frozen; that is not a P0 defect if the inconsistency is real and evidenced.

## 8. Evidence set E — duplicate protection across restart

After recovery, leave the EA running through enough processing cycles to prove the same DecisionID/execution hash does not create another broker order.

Record:

```text
P0_DUPLICATE_CHECK
ExecutionHash=
OriginalTicket=
SecondTicketForSameHash=NONE
Result=PASS/FAIL
```

PASS requires exactly one live/executed ticket attributable to the qualifying execution hash across the restart window.

FAIL if the same execution hash / DecisionID maps to a second broker ticket.

## 9. Evidence set F — broker comment independence

Record broker comment state for the qualifying order after execution and after restart.

Accepted outcomes include:

- compact `BBMA|H:<16hex>` persisted;
- broker truncates/replaces it;
- broker persists an empty comment.

The acceptance question is not whether the comment survives. The question is whether durable local identity still persists and recovery/dedup remain correct without treating `OrderComment()` as authority.

## 10. Optional ambiguity evidence

If a genuine MT4 ambiguous execution result occurs naturally, capture it. Error 128 must not be blindly retried as a normal retryable error.

Do not deliberately sabotage connectivity or create repeated demo orders solely to manufacture error 128. Absence of a naturally occurring ambiguity event does not block the core P0 fresh-order/restart acceptance.

## 11. Minimal screenshot/log package to send for review

The smallest sufficient user-side evidence package is:

1. v4.59 initialization/build identity;
2. fresh broker order/ticket line;
3. complete fresh `[P3S5][EXEC_ID]` line showing `Persist=PASS Local=Y`;
4. pre-restart ticket/hash snapshot;
5. post-restart initialization;
6. complete `[P3S5][RECOVERY]` line for the same ticket;
7. later open-order/log view proving no duplicate ticket for that execution hash.

Screenshots may be used, but copy/pasted Experts/Journal log text is preferred when available because exact fields are easier to verify.

## 12. P0 acceptance matrix

| Case | Requirement | PASS | FAIL |
|---|---|---|---|
| P0-01 | Correct build | v4.59 P0 EXEC_ID fix visibly initialized | old/wrong build |
| P0-02 | Fresh EA-created order | order created automatically by v4.59 | legacy/manual surrogate |
| P0-03 | Immediate local persistence | `Persist=PASS Local=Y` | `Persist=FAIL` or `Local=N` |
| P0-04 | Broker-comment independence | local PASS even if comment blank/replaced | recovery depends solely on comment |
| P0-05 | Pre-restart attribution | ticket/hash/magic/open-time/direction recorded | identity attribution missing |
| P0-06 | Exact-ticket restart recovery | same live ticket reconstructed with durable hash | wrong/lost ticket identity |
| P0-07 | No false missing-identity freeze | no `REC_IDENTITY_MISSING_FROZEN` solely due blank comment | fresh persisted ticket freezes only because comment absent |
| P0-08 | Duplicate prevention | one ticket for same execution hash across restart | second ticket for same hash/DecisionID |
| P0-09 | No strategy drift | runtime evidence shows normal v4.59 strategy path; no P0-induced strategy semantic change observed | evidence points to strategy regression caused by P0 patch |

## 13. Closure rule for Issue #94

Issue #94 may be closed only when P0-01 through P0-08 are positively demonstrated on authenticated HFM demo runtime and no new P0-caused strategy regression is observed.

Required closure conclusion:

```text
P0 EXEC_ID RUNTIME ACCEPTANCE = PASS
Fresh v4.59 ticket: <ticket>
Immediate persistence: PASS / Local=Y
Broker comment dependency: NONE REQUIRED
Restart exact-ticket recovery: PASS
Duplicate execution across restart: NONE
Issue #94: READY TO CLOSE
```

If any mandatory case fails, conclusion is `FAIL` and #94 remains open. If the fresh trade or restart has not yet occurred, conclusion is `INCOMPLETE`, never PASS.

## 14. Post-P0 handoff

Only after P0 runtime PASS:

1. attach the evidence/summary to Issue #94;
2. close #94;
3. create a fresh integration branch from the then-current `d1-owner-dev`;
4. apply only the reviewed v4.59 production source delta — do not merge the hotfix branch wholesale;
5. run protected-surface regression;
6. compile exact integrated source with official MetaEditor at 0 errors / 0 warnings;
7. capture final integrated commit/blob/SHA/build identity;
8. materialize the prepared post-P0 v4.59 runtime tooling;
9. proceed with runtime order `R1 -> R2 -> R3 -> R4 -> R5 -> R6`.

## 15. Safety boundary

Use HFM demo only for this acceptance. Do not keep or manipulate a real-risk trade solely for debugging. Do not modify BBMA strategy, SL/TP, D1TPW/C044 gates, or risk semantics while collecting P0 evidence.

## 16. Preparation verdict

**P0 EXEC_ID RUNTIME EVIDENCE PACK READY. BROKER-DEMO FRESH-TRADE + RESTART EVIDENCE STILL PENDING.**
