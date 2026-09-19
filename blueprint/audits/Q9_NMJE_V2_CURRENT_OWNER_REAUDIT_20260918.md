# Q9 NMJE v2 Current-Owner Re-Audit — 2026-09-18

Issue: #101
Branch: `q9-nmje-v2-current-owner-101`
Live owner base: `d1-owner-dev@01f7e8305f6ba558494fc559bb3c734dfc06124a`
Canonical baseline: Build `4.86` / `V486_STRUCTURAL_LIFETIME_20260917`

## Classification

**Q9 P1 MATERIALIZATION REQUIRED / CURRENT BASELINE AUTHORITY CLEAN**

This is not a Strategy-Core defect and does not authorize a new trading rule. The current owner correctly preserves NMJE as observation/read-only context, but it does not contain the provenance identity layer required by Issue #101 before M5 refinement can be introduced.

## Mandatory preflight result

- GitHub live owner and queue recovered.
- `SOURCE_INDEX.md` retrieval sequence re-read.
- Active Strategy Core V2 re-read; no new Core rule is required.
- M12N/NMJE contract re-read: observation-only, no create/reject/rank/execute authority.
- N3 staging contract re-read: `execution_policy = NONE`; activation remains forbidden.
- Q1 Build 4.83 read-only closure evidence re-read and preserved.
- Current Build 4.86 EA source audited directly.

## Current Build 4.86 findings

PASS:
- `NMJE_PassExecutionGate` absent.
- `REJ_NMJE_RELATION` absent.
- N1/N2 telemetry remains present.
- M15 remains sole processing/final-decision clock.
- M16 remains revalidation owner.
- M22 remains broker execution owner.
- no current `PERIOD_M5` NMJE processing/wiring exists.
- current `JourneyID` is deterministic from current parent kind/timeframe/signal/direction/anchor.

P1 gap:
- `D1MajorTrendOwner` has no `EpochStartCandleTime`;
- `NestedTFNode` has no canonical EventID;
- `NestedJourneyState` has no immutable `ParentEventID`;
- future M5 lineage therefore cannot yet bind deterministically through the current parent chain without adding provenance identity first.

## Historical reference boundary

The clean v4.63 N3 lineage used by PR #126 already contained provenance-only:
- D1 owner epoch anchoring;
- canonical EventID domains for Re-Entry, Extreme, MHV/MLV, D1 owner and H4 owner;
- exact parent EventID exposure.

That historical source is evidence/reference only. It must not be blindly cherry-picked because the current owner is Build 4.86 with materially newer Strategy-Core/lifecycle fixes.

## Authorized P1 scope

Rematerialize the smallest provenance-only identity layer against current Build 4.86:
1. stable D1 owner epoch metadata;
2. canonical owner/event identity helpers derived only from existing owner provenance;
3. canonical EventID on NMJE observation nodes;
4. exact ParentEventID on the selected descriptive parent;
5. diagnostics/static tests proving identity-domain separation and authority firewall.

Explicitly excluded from this P1 source-bearing stage:
- M5 data collection or `NMJE_BuildM5Node`;
- M5 processing-clock authority;
- candidate create/reject/rank/delay behavior;
- NMJE execution gate;
- D1/H4/H1/M15 Strategy-Core semantic changes;
- risk/MM/M17/M22/lifecycle changes;
- P2–P11 behavior beyond the identity prerequisites needed for later stages.

## Validation gate

Before P2/P3 may start:
- current-owner static authority suite PASS;
- Q9 P1 identity/replay static tests PASS;
- protected-surface diff review PASS;
- native MetaEditor compile 0E/0W;
- no runtime authority activation.

Remote G40 native execution is currently unavailable to this chat because Desktop Commander monthly remote-call quota is exhausted. Therefore any source-bearing P1 commit remains **NATIVE COMPILE PENDING / NOT RUNTIME VERIFIED** until an attributable native compile is obtained.
