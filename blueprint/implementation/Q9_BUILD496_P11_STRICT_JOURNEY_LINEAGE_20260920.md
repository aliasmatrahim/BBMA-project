# Q9 Build 4.96 P11 Strict Canonical Journey Lineage — 2026-09-20

Issue: #101
PR: #205
Base: P11 Build 4.95 commit `a114387d8a3054dfdd819d023165e07f2063f9e1`
Build: `4.96` / `V496_Q9_P11_STRICT_JOURNEY_LINEAGE_20260920`
SourceRev: `Q9_P11_STRICT_JOURNEY_LINEAGE_101_20260920`
Status: SHADOW / PROVENANCE METADATA ONLY / NO ACTIVATION

## Decision

User selected option A: **strict canonical JourneyID semantics**.

A P11 lineage journey is the exact canonical NMJE `ParentEventID/JourneyID` identity.
A stable broader D1/H4 owner family cannot merge multiple canonical JourneyIDs.

## Mapping

- current canonical ParentEventID is `LineageRootEventID`;
- previous valid ParentEventID/JourneyID differs -> `NEW_JOURNEY`;
- current canonical root remains -> `FIRST`;
- `CONTINUATION` requires a distinct source-owned continuation-event identity inside the unchanged JourneyID;
- current owner model exposes no such identity, so Build 4.96 never infers CONTINUATION from elapsed observations or higher-owner continuity;
- any attempted continuation without identity is fail-closed `UNRESOLVED`;
- durable persistence never writes CONTINUATION; a legacy 4.95 persisted CONTINUATION is normalized to UNRESOLVED on load.

## Corrected defect

Build 4.95 used D1/H4 higher-owner roots. That could classify a changed ParentEventID/JourneyID as `CONTINUATION`, while the verified P8 contract treats a ParentEventID/JourneyID transition as a new journey.

Build 4.96 removes that cross-contract mismatch. In the bounded GBPUSD August tester:
- `FIRST=1988`;
- `NEW_JOURNEY=28`;
- `CONTINUATION=0`;
- `UNRESOLVED=0`.

## Authority boundary

No change to:
- `NMJE_ResolveParent` or `NMJE_BuildJourneyID`;
- M13/M14 candidate/combo semantics;
- comparator/M15/M16;
- M17 SL/TP;
- risk/MM/preflight;
- `SendOrderWithRetry`;
- P2 ordering or M5 execution authority.

This is an engineering lineage correction only.
