# D1TPW Monday Demo Verification Checklist

Status: prepared only. Do not execute without explicit activation approval.

## Preconditions

- Use a demo account and a dedicated terminal/profile only.
- Create a separate demo-activation branch and increment the visible EA build.
- Keep C044 and NMJE execution authority `OFF`.
- Limit scope to one approved pair, one position, minimum valid fixed lot,
  `LOCK_ONE_POSITION`, and no other EA instance sharing strategy/instance IDs.
- Record branch, commit, EX4 hash, compiler 0E0W result, account server, symbol
  suffix, digits, tick size, stop level, freeze level and spread.
- Back up terminal logs and capture existing D1TPW Global Variables before attach.

## Restart proof

- Use only an organically authorized D1 Extreme TPW demo decision; do not inject
  a live/manual targetless order.
- Confirm checkpoint v2 is complete and bound to ticket, pair, direction,
  CycleID, execution identity, open time and magic.
- Restart the terminal after checkpoint persistence and before D1 completion.
- Confirm exactly one recovered registry row and the identical D1 cursor.
- Repeat the restart once; no duplicate ticket, latch or close attempt is allowed.

## Close-idempotency proof

- On the first qualifying fully closed D1 candle, capture exactly one durable
  exit latch and its candle identity.
- Confirm M23 performs the only normal-strategy `OrderClose` attempt.
- If the broker returns a retryable failure, confirm latch/checkpoint retention
  and no re-detection; the next attempt must reuse the same identity.
- After successful close, confirm the ticket is closed once, the checkpoint is
  cleared, registry compaction is safe, and repeated ticks cannot close again.
- Restart once after close and confirm no lifecycle resurrection.

## Immediate abort/freeze conditions

- Any pair, ticket, magic, open-time, CycleID or execution-hash mismatch.
- Missing/torn/version-1 checkpoint or simultaneous D1TPW+C044 checkpoint.
- Cursor reversal, unavailable exact closed-D1 history or invalid MA history.
- D1TPW/C044 mutual-exclusion failure, duplicate OrderSend/OrderClose, geometry
  drift, unexpected targetless trade, or any production/live account exposure.

On any condition above: detach the demo EA, preserve logs and Global Variables,
leave the trade protected by its hard SL, and do not infer/rebuild lifecycle
identity manually.

## Required evidence before any further decision

- Terminal Experts/Journal logs covering attach, checkpoint, both restarts,
  latch, close result, cleanup and final restart.
- Before/after Global Variable export and broker order-history screenshot/export.
- Exact D1 source/completion candle times and MA5/MA10 high/low values.
- A signed result of PASS, FAIL-CLOSED or INCONCLUSIVE. Only PASS may be brought
  back for a separate merge/release decision; it still does not authorize live
  trading.

