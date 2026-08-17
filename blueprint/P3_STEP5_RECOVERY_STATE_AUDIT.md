# P3 Step 5 — Recovery State Validation & Frozen-Trade Diagnostics

## Status
IN PROGRESS — FIX A VERIFIED; FIX B IMPLEMENTED; S5B + S5C NATIVE COMPILE PASS; FINAL MT4 RUNTIME CLOSURE PENDING

## Triggering runtime finding
MT4 Experts originally showed repeated messages for ticket `483347962`:
- corrupted/frozen;
- recovery state `REC_RECOVERY_INVALID`.

P3 S5 diagnostic instrumentation isolated the root cause instead of treating the symptom generically.

## Latest runtime evidence before Fix B
The latest pre-Fix-B MT4 Experts capture showed two exact EA-owned USDCHF tickets:
- `483347969`;
- `483347962`.

Both were classified by the diagnostic build as:
- `State=REC_RECOVERY_INVALID`;
- `Cause=MISSING_EXECUTION_HASH`;
- `HashFound=N`;
- `FullMeta=N`;
- empty broker comment (`RawLen=0`, `RawComment=<>`).

At the same time the P33/P34 signal pipeline continued operating and GBPUSD produced a valid eligible H1 Re-Entry SELL candidate. Therefore the observed failure is isolated to restart/recovery identity handling, not the signal pipeline.

## P3 S5 Fix A — diagnostic result
**PASS for root-cause isolation.**

Recovery causes are explicitly separated:
- `INVALID_GEOMETRY`
- `NONPOSITIVE_LIVE_LOT`
- `INVALID_LIVE_LOT_STEP`
- `LIVE_LOT_ABOVE_INTENDED`
- `LIVE_LOT_BELOW_INTENDED`
- `FULL_METADATA_MATCH`
- `EXECUTION_HASH_ONLY`
- `MISSING_EXECUTION_HASH`

Fix A proved that missing execution identity was being collapsed into `REC_RECOVERY_INVALID` even when broker geometry/lot were otherwise preservable.

## P3 S5 Fix B — state-model repair
The M24 recovery contract defines:

`REC_IDENTITY_MISSING_FROZEN`

Use this state only when:
- broker symbol + configured magic + market order type prove exact live EA ownership;
- Entry/SL/TP directional geometry is valid;
- live lot is positive and broker-step valid;
- no valid `BBMA|H:` execution hash is observable.

This state is intentionally not called `LEGACY`. An empty comment cannot prove whether an order predates execution hashes or whether the broker/server removed the comment.

Required behavior remains locked:
- preserve broker Entry/SL/TP/lot exactly;
- keep the order inside M19/M20 risk, basket and portfolio accounting;
- preserve M23 emergency-close precedence;
- freeze ordinary identity-dependent lifecycle actions;
- never fabricate `DecisionID`, hash, signal type, sequence, candle time or tombstone;
- emit one structured `MISSING_EXECUTION_HASH` diagnostic;
- do not classify the position as `REC_RECOVERY_INVALID` solely because `H:` is missing.

Hard broker-state failures remain `REC_RECOVERY_INVALID`, including invalid directional Entry/SL/TP geometry, non-positive live lot, and invalid live lot step.

## Fix B canonical source implementation
**IMPLEMENTED on `blueprint-dev`.**

Canonical source commit:
`8f4f9abb88557aacb584d4390a140fbaba351301`

Implemented changes:
1. Added `REC_IDENTITY_MISSING_FROZEN` to `ENUM_RECOVERY_STATE`.
2. M24 separates invalid geometry, non-positive lot and invalid lot-step causes before identity classification.
3. Valid exact-owned/no-`H:` positions map to `REC_IDENTITY_MISSING_FROZEN`.
4. `REC_RECOVERY_INVALID` remains reserved for actual hard broker-state invalidity.
5. M23 freezes `REC_IDENTITY_MISSING_FROZEN` only after emergency-liquidation precedence.
6. Repeated per-cycle frozen logging was removed from M23.
7. M24 emits one structured `[P3S5][RECOVERY]` line during reconstruction.
8. No tombstone or full strategy identity is fabricated when `H:` is absent.
9. M22 `BBMA|H:` generation for new executions remains unchanged.

Source applicator verification:
- Workflow: `P3 S5B Apply Source`
- GitHub Actions run: `32025266024`
- Result: **SUCCESS**
- Exact-anchor/static postconditions: **PASS**

## P3 S5B native compile gate
**PASS.**

Compile evidence:
- Workflow: `P3 S5B Recovery Identity Fix`
- GitHub Actions run: `32024947673`
- Compile job: `95372340171`
- MetaEditor result: `0 errors, 0 warnings, 103 msec elapsed`
- Workflow marker: `P3_S5B_NATIVE_MT4_COMPILE=PASS`
- EX4 artifact produced successfully.

## P3 S5C — fresh-order execution identity persistence instrumentation
**IMPLEMENTED AND COMPILE-VERIFIED.**

Canonical S5C source commit:
`0b57f042c4c90a5a00531c152252c1e53332eb3f`

At the successful M22 `OrderSelect(ticket)` boundary, the EA now:
1. reads the broker-returned `OrderComment()`;
2. extracts the persisted `H:` value;
3. compares it with `SHORT_HASH(decision.DecisionID)`;
4. stores `TradeInfo.execution_hash` only when the broker-returned hash matches;
5. emits one `[P3S5][EXEC_ID]` runtime diagnostic;
6. never rewrites broker comment metadata and never fabricates a restart identity.

Expected fresh-order runtime line:

`[P3S5][EXEC_ID] Ticket=... Pair=... Persist=PASS HashFound=Y HashMatch=Y ExpectedHash=... PersistedHash=... RawComment=<BBMA|H:...>`

If `Persist=FAIL`, restart idempotency remains unresolved at the broker-comment persistence boundary even though the live position remains managed safely during the current process.

S5C CI evidence:
- Workflow: `P3 S5C Execution Identity Persistence`
- GitHub Actions run: `32026948381`
- Prepare/source patch: **PASS**
- Native MetaEditor compile: **PASS**
- Compile job: `95378287873`
- MetaEditor result: `0 errors, 0 warnings, 88 msec elapsed`
- Workflow marker: `P3_S5C_NATIVE_MT4_COMPILE=PASS`
- EX4 artifact: `p3-s5c-compile-output`, artifact ID `9287742252`
- Canonical commit stage: **PASS**
- Canonical source commit: `0b57f042c4c90a5a00531c152252c1e53332eb3f`

## Final MT4 runtime closure protocol
Deploy/re-attach the latest S5C build and collect only the following evidence:

1. **Restart recovery of existing no-H tickets**
   - Tickets `483347969` / `483347962`, if still open and geometry/lot remain valid, must report:
   - `State=REC_IDENTITY_MISSING_FROZEN`
   - `Cause=MISSING_EXECUTION_HASH`
   - `HashFound=N`
   - `FullMeta=N`

2. **No recovery log spam**
   - one `[P3S5][RECOVERY]` line per reconstructed order;
   - no repeated frozen-state line every tick/timer cycle.

3. **Fresh execution persistence**
   - wait for one valid post-S5C M22 execution;
   - require `[P3S5][EXEC_ID] ... Persist=PASS HashFound=Y HashMatch=Y ...`.

4. **Restart the EA after that fresh trade remains open**
   - the fresh order must recover with an observable execution hash;
   - it must not fall into `REC_IDENTITY_MISSING_FROZEN` solely because of broker comment loss.

5. **Safety invariants**
   - genuine invalid geometry/lot remains `REC_RECOVERY_INVALID`;
   - M19/M20 continue counting exact-owned frozen trades;
   - emergency-close precedence remains above the recovery freeze.

## P3 Step 5 closure criteria
P3 Step 5 is PASS only when all of the following are verified:
1. **PASS** — Native compile: 0 errors / 0 warnings.
2. Existing exact-owned/no-`H:` tickets with otherwise valid broker geometry recover as `REC_IDENTITY_MISSING_FROZEN`.
3. Genuine geometry/lot-invalid orders remain `REC_RECOVERY_INVALID`.
4. One recovery diagnostic is emitted per recovered order without per-tick/timer spam.
5. Emergency portfolio close can still close a frozen exact-owned order.
6. A newly executed M22 order retains the `BBMA|H:` prefix after broker acceptance and still exposes the hash after restart observation.

## Decision
**Do not close P3 Step 5 yet.**

All source and compile gates are now complete. The only remaining gate is live MT4 runtime evidence using the canonical S5C build.
