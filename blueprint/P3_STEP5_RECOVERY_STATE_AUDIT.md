# P3 Step 5 — Recovery State Validation & Frozen-Trade Diagnostics

## Status
IN PROGRESS — FIX A VERIFIED; FIX B IMPLEMENTED; NATIVE COMPILE PASS; S5C RUNTIME EVIDENCE PENDING

## Triggering runtime finding
MT4 Experts originally showed repeated messages for ticket `483347962`:
- corrupted/frozen;
- recovery state `REC_RECOVERY_INVALID`.

P3 S5 diagnostic instrumentation then isolated the root cause instead of treating the symptom generically.

## Latest runtime evidence
The latest MT4 Experts capture shows two exact EA-owned USDCHF tickets:
- `483347969`;
- `483347962`.

Both were classified by the pre-Fix-B diagnostic build as:
- `State=REC_RECOVERY_INVALID`;
- `Cause=MISSING_EXECUTION_HASH`;
- `HashFound=N`;
- `FullMeta=N`;
- empty broker comment (`RawLen=0`, `RawComment=<>`).

At the same time the P33/P34 signal pipeline continued operating and GBPUSD produced a valid eligible H1 Re-Entry SELL candidate. Therefore the observed failure is isolated to restart/recovery identity handling, not the signal pipeline.

## P3 S5 Fix A — diagnostic scope
- Preserve fail-closed handling for `REC_CORRUPTED` and `REC_RECOVERY_INVALID`.
- Preserve emergency liquidation precedence.
- Classify recovery root cause explicitly during `RecoverExistingOrders()`.
- Emit one structured P3S5 recovery diagnostic per recovered owned order.
- Suppress repeated frozen-trade log spam after the first management notification for that in-memory recovery instance.

## Root-cause classes
- `INVALID_GEOMETRY`
- `NONPOSITIVE_LIVE_LOT`
- `INVALID_LIVE_LOT_STEP`
- `LIVE_LOT_ABOVE_INTENDED`
- `LIVE_LOT_BELOW_INTENDED`
- `FULL_METADATA_MATCH`
- `EXECUTION_HASH_ONLY`
- `MISSING_EXECUTION_HASH`

## Fix A runtime result
**PASS for root-cause isolation.**

The instrumentation successfully distinguished `MISSING_EXECUTION_HASH` from geometry/lot corruption. This exposed a state-model problem: a valid exact-owned position with missing execution identity was being collapsed into `REC_RECOVERY_INVALID`.

P3 Step 5 must not close on Fix A alone.

## P3 S5 Fix B — state-model repair
The M24 recovery contract defines:

`REC_IDENTITY_MISSING_FROZEN`

Use this state only when:
- broker symbol + configured magic + market order type prove exact live EA ownership;
- Entry/SL/TP directional geometry is valid;
- live lot is positive and broker-step valid;
- no valid `BBMA|H:` execution hash is observable.

This state is intentionally not called `LEGACY`. An empty comment cannot prove whether the order predates execution hashes or whether the broker/server removed the comment.

### Required behavior
- Preserve broker Entry/SL/TP/lot exactly.
- Keep the order inside M19/M20 risk, basket and portfolio accounting.
- Preserve M23 emergency-close precedence.
- Freeze ordinary identity-dependent lifecycle actions.
- Never fabricate `DecisionID`, hash, signal type, sequence, candle time or tombstone.
- Emit one structured `MISSING_EXECUTION_HASH` diagnostic.
- Do not classify the position as `REC_RECOVERY_INVALID` solely because `H:` is missing.

### Hard invalid state remains separate
`REC_RECOVERY_INVALID` remains mandatory for actual hard failures such as:
- invalid directional Entry/SL/TP geometry;
- non-positive live lot;
- invalid live lot step;
- another broker-state inconsistency that cannot safely be preserved.

## Fix B canonical source implementation
**IMPLEMENTED on `blueprint-dev`.**

Canonical source commit:
`8f4f9abb88557aacb584d4390a140fbaba351301`

Implemented changes:
1. Added `REC_IDENTITY_MISSING_FROZEN` to `ENUM_RECOVERY_STATE`.
2. M24 now separates invalid geometry, non-positive lot and invalid lot-step causes before identity classification.
3. Valid exact-owned/no-`H:` positions now map to `REC_IDENTITY_MISSING_FROZEN`.
4. `REC_RECOVERY_INVALID` remains reserved for actual hard broker-state invalidity.
5. M23 freezes `REC_IDENTITY_MISSING_FROZEN` only after emergency-liquidation precedence.
6. Repeated per-cycle frozen logging was removed from M23.
7. M24 emits one structured `[P3S5][RECOVERY]` line during reconstruction.
8. No tombstone or full strategy identity is fabricated when `H:` is absent.
9. M22 `BBMA|H:` generation for new executions is unchanged.

Source applicator verification:
- Workflow: `P3 S5B Apply Source`
- GitHub Actions run: `32025266024`
- Result: **SUCCESS**
- Exact-anchor/static postconditions: **PASS**

## Native compile gate
**PASS.**

GitHub-hosted Windows native MetaEditor compiled the exact prepared P3 S5B source using official MT4 MetaEditor.

Compile evidence:
- Workflow: `P3 S5B Recovery Identity Fix`
- GitHub Actions run: `32024947673`
- Compile job: `95372340171`
- MetaEditor result: `0 errors, 0 warnings, 103 msec elapsed`
- Workflow marker: `P3_S5B_NATIVE_MT4_COMPILE=PASS`
- EX4 artifact produced successfully.

This closes closure criterion #1 for the Fix-B source.

## P3 S5C — fresh-order execution identity persistence gate
Missing `H:` on the two existing USDCHF tickets does not prove they are legacy orders.

A fresh-order persistence diagnostic is being added at the successful M22 `OrderSelect(ticket)` boundary. It reads the broker-returned `OrderComment()` and compares the observed `H:` against `SHORT_HASH(decision.DecisionID)` without modifying broker metadata or fabricating identity.

Expected one-time runtime line for a fresh execution:

`[P3S5][EXEC_ID] Ticket=... Pair=... Persist=PASS HashFound=Y HashMatch=Y ... RawComment=<BBMA|H:...>`

If `Persist=FAIL`, restart idempotency remains unresolved at the broker-comment persistence boundary even though the live position can still be managed safely during the current process.

S5C workflow:
- `P3 S5C Execution Identity Persistence`
- GitHub Actions run: `32026948381`
- Prepare/source patch stage: **PASS**
- Native compile/commit stages: pending at the time of this record.

## P3 Step 5 closure criteria
P3 Step 5 is PASS only when all of the following are verified:
1. **PASS** — Native compile: 0 errors / 0 warnings.
2. Existing exact-owned/no-`H:` tickets with otherwise valid broker geometry recover as `REC_IDENTITY_MISSING_FROZEN`.
3. Genuine geometry/lot-invalid orders remain `REC_RECOVERY_INVALID`.
4. One recovery diagnostic is emitted per recovered order without per-tick/timer spam.
5. Emergency portfolio close can still close a frozen exact-owned order.
6. A newly executed M22 order retains the `BBMA|H:` prefix after broker acceptance/restart observation.

## Decision
**Do not close P3 Step 5 yet.**

Compile is now proven clean. The next remaining evidence is runtime: restart/re-attach against the existing no-`H:` positions, plus one fresh post-S5C M22 execution to prove broker persistence of `BBMA|H:`.
