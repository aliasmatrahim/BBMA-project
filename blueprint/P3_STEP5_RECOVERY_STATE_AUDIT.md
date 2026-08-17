# P3 Step 5 — Recovery State Validation & Frozen-Trade Diagnostics

## Status
IN PROGRESS — FIX A RUNTIME DIAGNOSTICS VERIFIED; FIX B CONTRACT LOCKED, SOURCE IMPLEMENTATION PENDING

## Triggering runtime finding
MT4 Experts originally showed repeated messages for ticket `483347962`:
- corrupted/frozen;
- recovery state `REC_RECOVERY_INVALID`.

P3 S5 diagnostic instrumentation then isolated the root cause instead of treating the symptom generically.

## Latest runtime evidence
The latest MT4 Experts capture shows two exact EA-owned USDCHF tickets:
- `483347969`;
- `483347962`.

Both are classified by the diagnostic build as:
- `State=REC_RECOVERY_INVALID`;
- `Cause=MISSING_EXECUTION_HASH`;
- `HashFound=N`;
- `FullMeta=N`;
- empty broker comment (`RawLen=0`, `RawComment=<>`).

At the same time the P33/P34 signal pipeline continues operating and GBPUSD produced a valid eligible H1 Re-Entry SELL candidate. Therefore the observed failure is isolated to restart/recovery identity handling, not the signal pipeline.

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

The instrumentation successfully distinguishes `MISSING_EXECUTION_HASH` from geometry/lot corruption. This exposed a state-model problem: a valid exact-owned position with missing execution identity is currently collapsed into `REC_RECOVERY_INVALID`.

P3 Step 5 must not close on Fix A alone.

## P3 S5 Fix B — required state-model repair
The M24 recovery contract now defines:

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

## Fresh-order identity persistence gate
Missing `H:` on the two existing USDCHF tickets does not prove they are legacy orders.

Before P3 Step 5 can close, a freshly executed post-fix M22 order must be observed after broker acceptance and verified to retain an `OrderComment()` beginning with:

`BBMA|H:`

If a fresh order loses this prefix, restart idempotency is still unresolved at the broker-comment persistence boundary. M24 must not hide that condition by labeling it as legacy.

## Fix B source implementation requirements
1. Add `REC_IDENTITY_MISSING_FROZEN` to `ENUM_RECOVERY_STATE`.
2. In `RecoverExistingOrders()`, map valid exact-owned/no-`H:` positions to the new state.
3. Keep geometry/lot failures mapped to `REC_RECOVERY_INVALID`.
4. In M23, freeze the new state for ordinary lifecycle after emergency-close handling.
5. Leave M19/M20 portfolio accounting unchanged.
6. Leave M22 new-order `BBMA|H:` execution identity generation unchanged.
7. Native MetaEditor compile must remain **0 errors / 0 warnings**.

## P3 Step 5 closure criteria
P3 Step 5 is PASS only when all of the following are verified:
1. Native compile: 0 errors / 0 warnings.
2. Existing exact-owned/no-`H:` tickets with otherwise valid broker geometry recover as `REC_IDENTITY_MISSING_FROZEN`.
3. Genuine geometry/lot-invalid orders remain `REC_RECOVERY_INVALID`.
4. One recovery diagnostic is emitted per recovered order without per-tick/timer spam.
5. Emergency portfolio close can still close a frozen exact-owned order.
6. A newly executed M22 order retains the `BBMA|H:` prefix after broker acceptance/restart observation.

## Decision
**Do not close P3 Step 5 yet.**

Fix A diagnosed the issue correctly. Fix B is now contract-defined and is the next canonical source change before runtime closure.
