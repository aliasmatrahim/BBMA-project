# P3-M2-07B — Opposite Extreme Lifecycle & Cycle Supersession Audit

Date: 2026-08-23
Status: **SOURCE RULE RESOLVED / IMPLEMENTATION GAP CONFIRMED / PR #35 MUST NOT MERGE AS-IS**

## Mandatory source cross-check

### 1. Primary PDF / canonical Core
The accepted Core sequence is:

`Extreme -> TP Wajib -> MHV/MLV -> direction -> Re-Entry -> Momentum/CSM -> further Re-Entry -> opposite Extreme / cycle restart`.

The canonical Core also distinguishes RAW Extreme from reversal-confirmed Extreme. RAW alone is not enough for executable REM/REE component authority.

### 2. BBMA Finale V01–V07
Finale V01 `00:57:06–00:58:01; 00:58:31–00:59:17` is recorded as OA-F-V01-008:

- the cycle progresses through Extreme, TP Wajib, MHV, direction, Re-Entry, Momentum and later Re-Entries;
- an **opposite Extreme can close/restart the cycle**.

V01 also records Extreme as an early signal, not proof that reversal is already complete. Therefore cycle supersession must not be triggered by an unconfirmed RAW Extreme merely appearing.

### 3. Forum corroboration
ForexFactory BBMA discussion post #832 (Aug 7 2022) states that an Extreme SELL becomes invalid when an opposite Extreme BUY is formed. This is corroborating evidence, not higher authority than the PDF/Finale contract.

## Resolved Strategy-Core rule

A **source-valid opposite Extreme that has reached the project's accepted reversal-confirmed maturity** supersedes the prior opposite Extreme/cycle authority on the same source timeframe.

Required semantic distinction:

1. Opposite RAW Extreme = new-cycle candidate only; it does **not** erase the old cycle yet.
2. Opposite reversal-confirmed Extreme = old opposite Extreme is superseded and old-cycle descendants lose authority / must be invalidated or exact-owner revalidated.
3. This event does **not** by itself prove that a new trend is fully confirmed.
4. This event does **not** authorize automatic `OrderClose()` of an already-open trade. Live positions remain under the approved trade lifecycle / SL/TP unless separate source evidence authorizes an exit.
5. A live old-direction position must not itself own or freeze BBMA Strategy-Core direction after the source cycle has legitimately superseded it.

## Static implementation audit

### PASS — M09 contains a local supersession concept
The current M09 MHV/MLV engine already contains a useful source-aligned pattern:

- opposite RAW Extreme is treated only as a supersession candidate;
- a later reversal-confirmation candle installs the new parent;
- the old MHV/MLV is marked `MLV_SUPERSEDED`.

This is conceptually aligned with the resolved source rule.

### GAP A — M08 opposite Extreme lifecycles are independent
`PairState` stores separate BUY and SELL Extreme lifecycle objects for M15, H1 and H4. `UpdateExtremeLifecycle()` updates one direction at a time and has no cross-direction peer parameter or pair-level supersession operation.

Result: when a new reversal-confirmed BUY Extreme forms, the previous SELL `ExtremeLifecycleData` can remain `IsValid=true` / mature until its own independent invalidation path happens. The reverse is also possible.

This violates the resolved single active opposite-Extreme cycle authority on the same source timeframe.

### GAP B — persistent H1/H4 Extreme Signal snapshots can retain superseded authority
The current controller exports each directional lifecycle independently into persistent H1/H4 Extreme `Signal` state. Without atomic cross-direction supersession, an old opposite snapshot can remain available to combination construction after the newer opposite Extreme has become reversal-confirmed.

This can contaminate REM/RRE/REE candidate construction with a component belonging to the superseded cycle.

### GAP C — controller ordering is not atomic for cross-direction supersession
The direction loop currently processes BUY and SELL sequentially and can construct candidates for the first direction before the second direction's lifecycle update has established a superseding opposite Extreme on that same processing pass.

A correct fix must establish the source-timeframe Extreme lifecycle/supersession snapshot **before** downstream combination candidates are built.

### GAP D — PR #35 uses live-position direction as Strategy-Core ownership
PR #35 blocks a new opposite-direction entry while an old opposite EA-owned position remains live. This is now rejected as the primary cycle policy because Finale/PDF evidence assigns lifecycle authority to BBMA structure, not `OrdersTotal()` / live-position direction.

PR #35 must remain unmerged and be replaced/reworked after the lifecycle fix.

## Required implementation design

The smallest source-faithful implementation is:

1. Add an explicit superseded terminal state for Extreme lifecycle (or an equivalent unambiguous peer-supersession marker); do not misuse Momentum `VOID` when the reason is opposite-cycle supersession.
2. For each source timeframe used by executable combinations (M15/H1/H4), update both BUY and SELL Extreme lifecycles first.
3. After both updates, resolve cross-direction supersession atomically:
   - if exactly one side has a newly established reversal-confirmed Extreme newer than the opposite active lifecycle, mark the older opposite lifecycle superseded;
   - RAW does not supersede;
   - ambiguous simultaneous opposite confirmations fail closed for cycle ownership rather than choosing by score/order.
4. Clear/invalidate persistent exported Extreme component state belonging to the superseded lifecycle.
5. Ensure M09 descendants and M13/M14/M15 candidate construction cannot consume superseded owner components.
6. Do **not** close live trades merely because their source cycle was superseded.
7. Do **not** use live open-position direction as a permanent BBMA cycle lock.
8. Add diagnostic trace for `RAW_OPPOSITE_CANDIDATE`, `EXTREME_SUPERSEDED`, descendant invalidation and ambiguous simultaneous confirmation.
9. Update About/header build identifier in the same source patch.
10. Native MetaEditor compile `0E0W` is mandatory after the source patch.

## Verification cases

- SELL Extreme active -> BUY RAW only: SELL remains authoritative.
- SELL Extreme active -> BUY reversal-confirmed: SELL becomes superseded; stale SELL Extreme component cannot enter REM/RRE/REE.
- BUY mirror case: identical behavior.
- Superseded old live trade remains open: no forced close solely from supersession.
- New-cycle candidate must still satisfy its normal BBMA confirmation/combination/risk path; opposite Extreme alone is not direct entry authority.
- Simultaneous newly confirmed BUY and SELL Extreme on same TF/pass: fail closed / no arbitrary owner.
- Restart/recovery must not resurrect a superseded Extreme component as current authority.

## Gate

**P3-M2-07B strategy semantics: PASS / RESOLVED.**

**Implementation: FAIL / PATCH REQUIRED.**

Do not close M2-07 or merge PR #35 until the atomic M08/controller supersession patch is compiled 0E0W and static regression confirms stale descendants cannot execute.
