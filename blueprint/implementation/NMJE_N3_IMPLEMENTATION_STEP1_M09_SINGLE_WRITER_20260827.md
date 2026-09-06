# NMJE N3 Implementation — Step 1: M09 Single-Writer Hardening

Date: 2026-08-27
Branch: `nmje-n3-hardening-dev`
Status: IMPLEMENTATION PREP / SOURCE PATCH NOT YET APPLIED
Baseline: forked from `d1-owner-dev` at runtime-candidate head so the live/frozen runtime line is not modified.

## Objective
Enforce the queued N3 single-writer invariant for M08/M09 without changing BBMA strategy semantics.

## Current issue
M09 contains a private supersession path (`InstallMHVSupersessionParent()` / `TryAdvanceMHVSupersessionCandidate()`) that can directly mutate/install an `ExtremeLifecycleData` parent. This violates the desired architecture in which M08 is the sole writer of canonical Extreme lifecycle state and M09 only consumes that owner.

## Source behaviour already available
The normal `ProcessPair()` order updates M08 M15 Extreme lifecycle and resolves opposite Extreme supersession before M09/MHV processing. `UpdateCanonicalMLVState()` already receives the canonical M08 parent and already handles a newer parent confirmation candle by superseding/reattaching the MHV/MLV cycle.

Therefore M09 does not need to redetect/install its own Extreme owner to preserve the intended lifecycle.

## Approved implementation direction
1. Remove M09 authority to call `ResetExtremeLifecycle()` and populate a parent `ExtremeLifecycleData` directly.
2. Remove/retire the private M09 RAW->reversal supersession candidate path as an Extreme producer.
3. Let M09 consume only the canonical M08 parent passed into `UpdateCanonicalMLVState()`.
4. Preserve M09's own `MLV_SUPERSEDED` / `MLV_VOID` provenance and state transitions.
5. A newly reversal-confirmed M08 parent with a different confirmation identity is the only canonical trigger for M09 cycle handover.
6. RAW M08 Extreme remains observational/non-authoritative for MHV parentage.
7. No score, timer, indicator, new entry condition, or BBMA rule is introduced.

## Regression invariants
- M08 remains sole writer of `ExtremeLifecycleData` strategy state.
- M09 remains sole writer of `MLVData` strategy state.
- M09 may read parent Extreme direction/maturity/timestamps but may not fabricate or mutate the parent.
- Existing F1 lifecycle stages remain: parent ready -> TP complete -> loss developing -> formation established -> retest complete/direction taken, with VOID/SUPERSEDED terminal handling.
- New reversal-confirmed opposite M08 parent still atomically supersedes old MHV/MLV provenance.
- M13 exact REM signature remains unchanged.
- N1/N2 remain observational on this step; no N3 execution gate is enabled.

## Runtime-candidate protection
Do not merge this branch into `d1-owner-dev` while the current runtime evidence candidate is being collected. Validation and implementation can proceed here independently.

## Next implementation action
Apply the source refactor on this branch, then run static checks for direct M09 writes to Extreme lifecycle state before moving to EventID/OwnerID schema hardening.
