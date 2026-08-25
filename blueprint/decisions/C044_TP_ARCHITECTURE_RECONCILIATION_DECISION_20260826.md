# C044 TP Architecture Reconciliation Decision — 2026-08-26

Branch: `d1-owner-dev`

## Status
**APPROVED / C044 LIFECYCLE EXIT PRIMARY FOR RE-ENTRY-OWNED TRADES / STATIC OUTER-BB BROKER TP INCOMPATIBLE WHEN C044 IS ENABLED / TARGETLESS LIFECYCLE ARCHITECTURE LOCKED / NO MQL4 SOURCE CHANGE IN THIS DECISION RECORD**

## Purpose
Resolve the implementation-precedence question left open by `C044_POST_REENTRY_FAILED_MOMENTUM_TP_LIFECYCLE_DECISION_20260826.md`:

- whether the current static Re-Entry-owned outer-BB broker TP may coexist with C044; and
- what minimum lifecycle architecture is required before C044 can be implemented without inventing unsupported exit semantics.

This record is a strategy/architecture decision only. It does not modify `blueprint/source/BBMA_EA.mq4`.

## Authority reconciliation
The accepted C044 sequence is:

`VALID DIRECTION -> VALID RE-ENTRY -> CONTINUATION TO/TEST OF DIRECTION-SIDE OUTER BB -> CLOSED-CANDLE MOMENTUM TEST`

with:

- source-valid same-direction Momentum -> continuation survives;
- outer-BB test without source-valid same-direction Momentum -> TP/close the existing lifecycle position.

Current v4.52 instead places a resting broker TP at the selected Re-Entry owner's directional outer BB.

These two mechanisms cannot be equal coexisting exit authorities. A resting broker TP can close the order at the outer-BB price before the source timeframe candle closes, which prevents the strategy from observing whether that same outer-BB attempt produced valid Momentum or failed.

Therefore:

`STATIC OUTER-BB BROKER TP + C044 CLOSED-CANDLE FAILURE TEST`

is a semantic race and is **not an acceptable final C044 architecture**.

## Decision 1 — C044 exit precedence
For a position whose executable owner is a valid Re-Entry component, once C044 is implemented:

- C044 lifecycle management is the primary strategy exit mechanism;
- the current universal static outer-BB broker TP is removed for that C044-managed Re-Entry-owned position;
- the directional outer BB remains a structural/event boundary used to evaluate continuation versus failed Momentum, not a mandatory resting broker TP coordinate.

The current static H1/H4/D1 outer-BB TP table remains historically valid as project execution policy for v4.52, but it must not survive as a competing normal exit authority in the C044 implementation build.

This does **not** alter the separate normal Extreme TP-Wajib rule.

## Decision 2 — lifecycle owner identity
C044 must not invent a new timeframe owner.

The lifecycle owner is the exact frozen Re-Entry source component already selected by the executable decision identity.

Examples under the current mapping include:
- standalone H1 Re-Entry -> H1 owner;
- REM -> its selected H4 Re-Entry owner;
- RRE/REE -> their selected D1 Re-Entry owner;
- any approved D1 Opportunity identity exception -> use the exact selected frozen Re-Entry source timeframe rather than hard-coding a different owner.

Lifecycle management follows that same owner identity for the lifetime of the relevant epoch.

## Decision 3 — first C044 continuation epoch
After a C044-managed order opens from a valid Re-Entry owner:

`ORDER OPEN -> LIFE_WAIT_OUTER_TEST`

Observation is only on fully closed candles later than the Re-Entry validation/confirmation candle on the lifecycle-owner timeframe.

For each new owner-timeframe closed candle:

### BUY
- outer-BB test event: the closed candle reaches/tests the relevant current Top BB structure;
- valid continuation: the same closed candle is source-valid BUY Momentum under the canonical M10/Core Momentum rule;
- failed continuation: outer-BB test occurred but source-valid BUY Momentum did not occur.

### SELL
- outer-BB test event: the closed candle reaches/tests the relevant current Low BB structure;
- valid continuation: the same closed candle is source-valid SELL Momentum under the canonical M10/Core Momentum rule;
- failed continuation: outer-BB test occurred but source-valid SELL Momentum did not occur.

Deterministic implementation mapping for `reaches/tests` may use the closed candle's price range against the same candle's owner-TF outer-BB structure, while Momentum authority itself must come from the canonical source-valid Momentum detector/output. M23 must not create a second Momentum formula.

Transitions:

`LIFE_WAIT_OUTER_TEST + no outer-BB test -> HOLD`

`LIFE_WAIT_OUTER_TEST + outer-BB test + same-direction valid Momentum -> LIFE_WAIT_NEXT_REENTRY`

`LIFE_WAIT_OUTER_TEST + outer-BB test + no same-direction valid Momentum -> LIFE_EXIT_LATCHED / EXIT_C044_FAILED_MOMENTUM`

No one-candle timeout or arbitrary candle-count timeout is allowed.

## Decision 4 — post-Momentum continuation and re-arm
Source evidence states that Momentum is followed by another Re-Entry and that, while the expected Re-Entry has not yet occurred, the position may be held.

Therefore:

`LIFE_WAIT_NEXT_REENTRY`

means:
- ordinary candles -> HOLD;
- additional same-direction Momentum candles -> HOLD;
- elapsed time/candle count -> no automatic exit;
- generic outer-BB touch alone -> no automatic exit;
- wait for the next valid same-direction Re-Entry on the same lifecycle-owner timeframe.

When that later owner-timeframe Re-Entry becomes valid:

`LIFE_WAIT_NEXT_REENTRY -> LIFE_WAIT_OUTER_TEST`

and the new Re-Entry confirmation candle becomes the next lifecycle epoch anchor.

Re-arm is position management only. It does not create a new broker order and does not bypass M13/M14/M15/M16/M17/M19/M20/M22 for any additional entry.

## Decision 5 — final old-cycle profit exit
The accepted BBMA cycle places an opposite Extreme when the prior trend/Momentum ends and the cycle restarts/reverses. Home Course material also directly teaches profit-taking when Extreme appears.

For deterministic project execution, RAW Extreme alone remains insufficient because the accepted Extreme contract requires reversal confirmation before the Extreme is treated as valid/mature.

Therefore, for a still-open C044 lifecycle position, a valid opposite reversal-confirmed Extreme on the same lifecycle-owner timeframe is the conservative old-cycle termination boundary:

`ANY NON-LATCHED C044 LIFECYCLE STATE + OPPOSITE REVERSAL-CONFIRMED EXTREME -> LIFE_EXIT_LATCHED / EXIT_CYCLE_SUPERSEDED`

This is an exit of the old position only. It is not automatic opposite-entry authority.

Lower-timeframe opposite-looking structures must not directly close a higher-owner-timeframe lifecycle position under this rule.

## Decision 6 — broker payload
For C044-managed Re-Entry-owned trades in the future implementation build:

- broker hard SL remains present and authoritative under the already-approved M17 structural-range / EA-safety rules;
- normal broker TP is `0` / absent;
- M22 must support an approved SL-only C044 order payload;
- M23 becomes the normal full-position close executor when a C044 lifecycle exit is latched;
- no partial TP, breakeven, trailing stop, TP2 or TP3 is introduced.

M20 emergency protection retains precedence and remains available at all times.

## Decision 7 — MinRR
A targetless C044 lifecycle has no source-proven deterministic reward price at entry.

Therefore the existing static outer-BB project-policy TP must not be retained merely to manufacture an RR number.

Implementation rule:
- `MinRRRatio == 0` -> C044 lifecycle trade may proceed subject to all other gates;
- `MinRRRatio > 0` -> fail closed for a targetless C044 lifecycle trade unless a separately approved deterministic reward reference is later established.

Do not silently bypass an explicitly enabled MinRR filter and do not invent an estimated lifecycle reward distance.

M21 AutoLot remains SL/risk based and therefore does not require a TP to size the position.

## Decision 8 — module ownership
### M17
- resolve/validate the approved structural hard SL;
- preserve exact Re-Entry owner identity;
- classify the payload as C044 lifecycle-managed;
- stop requiring a non-zero broker TP for that payload;
- keep MaxSL/broker geometry checks;
- enforce the MinRR targetless rule above.

M17 does not decide live lifecycle closes.

### M22
- send the approved order with hard SL and `TP=0` for C044-managed payloads;
- retain execution idempotency and frozen decision identity.

### M23
- consume immutable owner-timeframe lifecycle evidence;
- latch and execute full-position C044 exits;
- preserve M20 emergency precedence;
- never recreate M08/M10/M12 strategy detection internally.

### M24
- persist/recover enough immutable state to reconstruct:
  - lifecycle-managed flag;
  - lifecycle owner timeframe / Re-Entry identity;
  - current lifecycle state;
  - current epoch Re-Entry anchor;
  - last processed owner-timeframe closed candle;
  - latched exit reason / idempotency state.

If that identity cannot be reconstructed safely after restart, fail frozen rather than fabricate lifecycle authority.

### M27 / owner pipeline
- publish the already-owned closed-candle Re-Entry, Momentum and mature-Extreme lifecycle events/snapshots needed by M23;
- preserve existing detector ownership and entry authority boundaries.

## Explicit non-authority / guards
This decision does not authorize:
- raw outer-BB touch as an immediate TP;
- first post-Re-Entry non-Momentum candle as an immediate close when no outer-BB test occurred;
- guaranteed reversal after failed Momentum;
- automatic opposite BUY/SELL after C044 close;
- a new opposite-CSM close rule outside separately approved lifecycle authority;
- a fixed candle timeout;
- a fixed-pip or RR-manufactured TP;
- lower-timeframe shortcuts that override the frozen lifecycle owner;
- removal or weakening of broker hard SL or M20 protection.

## Current-build boundary
Current source remains:
- version `4.52`;
- Git blob `4ccd444a96a34b494653143a7560516a4147b5bc` at the checkpoint used by the preceding M17/NMJE records.

This decision does not modify that source.

## Next implementation gate
A separate C044 implementation series may now be prepared with, at minimum:
1. targetless lifecycle state/persistence fields;
2. M17 SL-only C044 payload support;
3. M22 `TP=0` execution-path support;
4. owner-pipeline immutable lifecycle evidence;
5. M23 C044 close latching/idempotency;
6. M24 restart reconstruction/fail-frozen behavior;
7. MinRR targetless rejection path;
8. static regression proving entry eligibility, direction, SL, MM/risk and emergency precedence unchanged;
9. native MetaEditor 0 errors / 0 warnings;
10. broker/demo runtime traces for BUY/SELL failed-Momentum close, successful Momentum -> wait-next-ReEntry -> re-arm, opposite mature-Extreme cycle close, restart recovery and emergency precedence.

## Final verdict
C044 is now architecturally reconciled:

`RE-ENTRY-OWNED POSITION -> NO UNIVERSAL STATIC BROKER TP -> CLOSED-CANDLE OUTER-BB CONTINUATION TEST -> FAILED MOMENTUM = TP/CLOSE -> VALID MOMENTUM = HOLD/WAIT NEXT RE-ENTRY -> RE-ARM -> REPEAT -> OPPOSITE REVERSAL-CONFIRMED EXTREME = OLD-CYCLE EXIT`

The existing v4.52 static outer-BB TP remains frozen only in the current build for evidence continuity. It is not permitted to coexist as the normal Re-Entry exit authority in the future C044 implementation build.