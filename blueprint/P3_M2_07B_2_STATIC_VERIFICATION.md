# P3-M2-07B.2 — Opposite Extreme / F1 Boundary Static Verification

Date: 2026-08-23  
Branch: `blueprint-dev`  
Build: **P3-M2-07B.2 F1 Boundary Reconciliation**  
Status: **STATIC PASS — NATIVE METAEDITOR 0E0W REQUIRED; RUNTIME EVIDENCE KIV**

## 1. Mandatory source cross-check

This verification follows the project source hierarchy and does not use current code as evidence of BBMA semantics.

### Primary PDF / canonical digest
Accepted project Core sequence remains:

`Extreme -> TP Wajib -> MHV/MLV -> direction -> Re-Entry -> Momentum/CSM -> further Re-Entry -> opposite Extreme / cycle restart`.

The primary PDF-derived F1 contract also requires prior Extreme provenance for MHV/MLV and distinguishes completed structural provenance from current active-stage ownership.

### BBMA Finale V01–V07
- V01 OA-F-V01-008 (`00:57:06–00:58:01`, `00:58:31–00:59:17`) corroborates the cycle and that an opposite Extreme can close/restart the cycle.
- V05 OA-F-V05-006..009 (`00:18:07–00:27:23`) places MHV after Extreme + TP Wajib and describes MHV as a setup / early new-journey stage.
- V05 OA-F-V05-010..016 then progresses through direction -> Re-Entry -> continuation.

### Forum corroboration
ForexFactory BBMA discussion post #832 / post `14092719` states that an Extreme SELL becomes invalid when an opposite Extreme BUY is formed. This is supporting evidence only and does not outrank the PDF/Finale Core contract.

Reference: `https://www.forexfactory.com/thread/post/14092719`

## 2. Locked source-derived distinction

Two different ownership boundaries must not be collapsed:

1. **M08 Extreme lifecycle ownership** — a newer reversal-confirmed opposite Extreme supersedes the older opposite Extreme on the same source timeframe. RAW opposite Extreme alone is insufficient.
2. **M09 F1 MHV/MLV lifecycle ownership** — completed MHV/MLV provenance is governed by the already-resolved F1 lifecycle. F1 terminates its current-cycle provenance through its own opposite-to-current-cycle reversal-confirmed Extreme transition. A later M08 change to the historical parent Extreme object must not automatically and retroactively erase already-established F1 provenance unless the F1 cycle event itself requires it.

This separation is required by `CORE_V2_F1_MHV_MLV_LIFECYCLE_DECISION.md`, especially Decisions 2, 10, 11 and 12.

## 3. P3-M2-07B implementation — PASS

Current M08/controller behavior now:

- adds `EXT_MAT_SUPERSEDED` as a distinct lifecycle terminal state;
- requires reversal-confirmed-or-later maturity before an Extreme can own/supersede a source-TF cycle;
- updates BUY and SELL Extreme lifecycles for M15 before resolving opposite ownership;
- updates both H1 directions before exporting either H1 Extreme component;
- updates both H4 directions before exporting either H4 Extreme component;
- resolves opposite Extreme supersession before M13/M14 candidate construction;
- chooses the newer `ConfirmationCandleTime` as the source-TF Extreme owner;
- leaves an equal-time opposite confirmation structurally ambiguous instead of inventing a winner;
- exports only post-resolution mature Extreme state;
- marks superseded old Extreme `IsValid=false`, so persistent H1/H4 component snapshots are cleared;
- does not call `OrderClose()` as part of Extreme/cycle supersession.

This removes the previous BUY-first/SELL-second lifecycle ordering hazard.

## 4. P3-M2-07B.1 regression found and corrected

A follow-up patch (`P3-M2-07B.1 Extreme Descendant Supersession`) initially added a generic M09 rule:

> if the exact historical parent Extreme becomes `EXT_MAT_SUPERSEDED`, immediately supersede its MHV/MLV descendant.

Static source-contract re-check showed that this was too broad.

Why:
- F1 deliberately distinguishes historical parent provenance from current active-stage ownership;
- after MHV/MLV formation and same-cycle progression, parent validity is not a generic retroactive eraser;
- `CORE_V2_F1_MHV_MLV_LIFECYCLE_DECISION.md` already defines its own opposite-cycle supersession transition;
- the existing M09 `TryAdvanceMHVSupersessionCandidate()` / `InstallMHVSupersessionParent()` path encodes that F1-specific transition and was previously covered by the F1 implementation audit.

Therefore the B.1 generic cross-module descendant gate was removed in **P3-M2-07B.2**. This is a regression correction, not a weakening of M08 Extreme supersession.

## 5. M09 F1 supersession path — KEEP

Focused review result: **KEEP / no new strategy patch**.

The M09 supersession path:
- treats opposite RAW Extreme as candidate-only;
- waits for the later reversal-direction confirmation;
- installs the new reversal-confirmed parent/cycle state;
- marks old MHV/MLV provenance `MLV_SUPERSEDED`;
- never uses a fixed candle/session timer as the cycle boundary;
- never closes a live broker order.

This matches the already-locked F1 Decision 12 and its implementation audit. It is not replaced by the new M08 Extreme-vs-Extreme arbitration.

## 6. M13/M14/M15/M16 regression — PASS

- M13 continues to collect only owner-provided immutable snapshots.
- M14 continues to validate the exact REM/RRE/REE signatures and direction consistency.
- M15 remains final entry authority and retains fail-closed opposite-candidate behavior.
- M16 exact-owner validation rejects an Extreme component when its persistent M08/M16 snapshot has been cleared after supersession.
- M09 `MLV_SUPERSEDED` remains non-executable and cannot satisfy REM maturity/owner validation.
- No scoring/manual-tier rule was added to resolve an opposite cycle.

## 7. M22/M23 live-position boundary — PASS

The patch changes strategy signal/cycle ownership only.

It does **not** add:
- forced `OrderClose()` on opposite Extreme;
- automatic hedge closure;
- breakeven/trailing/partial close;
- live-position direction as Strategy-Core cycle ownership.

Already-open positions remain governed by the approved broker SL/TP, M23 synchronization, and M20 emergency protection. A source-valid new cycle and an older still-open order are deliberately not treated as the same state object.

## 8. Static integrity checks

PASS:
- build identifier updated to `P3-M2-07B.2 F1 Boundary Reconciliation`;
- source patch carrier ran `git diff --check` during materialization;
- patch script asserted balanced `{}` before write;
- new M08 supersession helpers are declared before controller use;
- no B.1 generic `parent.Maturity == EXT_MAT_SUPERSEDED` M09 descendant gate remains;
- old hard live-position pair-direction PR #35 is closed and unmerged;
- temporary PR #39 is not a merge vehicle;
- temporary carrier script was restored after patching.

## 9. Hard gate remaining

**Native MT4 MetaEditor compile is now required for the current B.2 source.**

Required result:

`0 errors / 0 warnings (0E0W)`

Do not reuse the earlier 0E0W record because the EA source changed after that compile.

Canonical file to compile:

`blueprint/source/BBMA_EA.mq4` on `blueprint-dev`.

After 0E0W:
1. close P3-M2-07B compile gate;
2. run M2-11 diagnostic/runtime-readiness audit;
3. run M2-12 final Mode-2 offline gate;
4. keep live/runtime evidence KIV until market/data execution is available.
