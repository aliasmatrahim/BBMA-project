# P3 Step 5 — Recovery State Validation & Frozen-Trade Diagnostics

## Status
IN PROGRESS

## Triggering runtime finding
MT4 Experts showed repeated messages for ticket 483347962:
- corrupted/frozen
- recovery state: REC_RECOVERY_INVALID

The same ticket was logged on every management cycle, creating diagnostic spam. A newly executed USDCHF trade used a different ticket and completed normally, so the recovery issue is isolated from the new S4 execution path.

## P3 S5 Fix A scope
- Preserve fail-closed handling for REC_CORRUPTED and REC_RECOVERY_INVALID.
- Preserve emergency liquidation precedence.
- Classify recovery root cause explicitly during RecoverExistingOrders.
- Emit one structured P3S5 recovery diagnostic per recovered owned order.
- Suppress repeated frozen-trade log spam after the first management notification for that in-memory recovery instance.

## Root-cause classes added
- INVALID_GEOMETRY
- NONPOSITIVE_LIVE_LOT
- INVALID_LIVE_LOT_STEP
- LIVE_LOT_ABOVE_INTENDED
- LIVE_LOT_BELOW_INTENDED
- FULL_METADATA_MATCH
- EXECUTION_HASH_ONLY
- MISSING_EXECUTION_HASH

## Runtime acceptance criteria
1. Compile 0 errors / 0 warnings.
2. On restart/re-attach, recovered ticket prints one `[P3S5][RECOVERY]` line with State and Cause.
3. REC_RECOVERY_INVALID / REC_CORRUPTED remains frozen for normal lifecycle.
4. The same ticket does not spam the Experts log every tick/timer cycle.
5. Emergency portfolio close path remains able to close the frozen EA-owned order.
