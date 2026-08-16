# M23 Position Lifecycle / Exit Ownership Contract

## Status
P0 Step 14 is **COMPLETED AT POSITION-LIFECYCLE / EXIT-OWNERSHIP CONTRACT LEVEL**.

## Purpose
M23 is the broker-side lifecycle owner for already-open EA positions. It must preserve the entry, SL and TP policy already resolved upstream and may not invent a second strategy-management layer.

## Locked normal-position behavior
For a normally managed position:
- broker-side SL and TP created from the M17-approved payload remain authoritative;
- M23 does not partially close at 1R;
- M23 does not migrate SL to breakeven automatically;
- M23 does not trail SL;
- M23 does not create TP2/TP3;
- M23 does not manually close a trade merely because price reaches the same TP already resting at the broker;
- M23 only synchronizes monitored state with live broker state.

The prior 50% partial close at 1R and automatic breakeven behavior are removed because they were not established by the locked PDF_CORE/FORUM_SUPPORTED exit contract and would alter the risk/reward profile after M17 approval.

## M20 emergency protection routing
M20 owns the decision that basket-loss emergency protection has tripped. M23 owns the actual broker `OrderClose()` action.

Requirements:
- emergency close acts only on live monitored EA-owned orders;
- live symbol magic must match the configured pair magic;
- full remaining broker lot is closed; no emergency partial close is introduced;
- if a close attempt fails, M20 keeps the emergency request latched so M23 can retry on a later tick;
- M23 logs the broker error but does not alter SL/TP or fabricate a different exit;
- once no live EA-owned monitored position remains, M20 may clear the latched request.

## Dynamic BBMA invalidation
The ForexFactory-supported concept of closing when an opposite confirmed CSM/momentum plus BB expansion invalidates the active thesis remains `FORUM_SUPPORTED` only.

It is **not enabled by Step 14**. Enabling it requires a separate, explicit lifecycle rule mapping from source-owned closed-candle state to M23. Until that mapping is approved, normal positions exit only through their broker SL/TP or M20 emergency protection.

## Ownership boundaries
### M23 may
- read live order state for already-open EA positions;
- synchronize monitored order fields;
- execute M20 emergency close requests;
- report close failures for later-tick retry/recovery.

### M23 may not
- change entry identity or direction;
- resize a position for profit-taking;
- change the structural M17 SL to breakeven;
- manufacture or extend TP;
- apply trailing stop;
- use M18 score/level/SignalMode;
- re-run M15 selection;
- close on forum-supported dynamic invalidation until separately approved.

## Recovery relationship
M24 remains responsible for rebuilding/reconciling monitored state after restart or uncertain state. M23 does not infer missing strategy identity from price action.

## Implementation record
Patch:
`blueprint/patches/0022-p0-step14-m23-position-lifecycle-exit-ownership.patch`

Patch commit:
`47ae3c91440667148df63fffc72f4081d54b1e21`

## Verification boundary
The M23 baseline block previously inspected showed:
- automatic 50% partial close at 1R;
- automatic SL migration to entry/breakeven;
- explicit manual `OrderClose()` when price reached `initial_take_profit`;
- M20 emergency-close routing added in Step 11.

Step 14 removes the unsupported normal-position management behaviors while retaining M20 emergency protection as the sole active M23-initiated close policy.

No new full-chain compile/SHA is claimed until the entire ordered patch chain is materialized and verified.

Do not merge to `main` until the full blueprint audit is clean and explicitly approved as MASTER BLUEPRINT LOCKED.
