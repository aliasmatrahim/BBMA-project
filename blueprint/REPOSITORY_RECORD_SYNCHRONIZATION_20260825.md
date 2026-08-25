# Repository Record Synchronization — 2026-08-25

## Purpose
Synchronize canonical project records on `blueprint-dev` with newer D1/NMJE/N2/D1O work performed on the parallel `d1-owner-dev` lineage without force-merging divergent EA source histories.

## Branch state at synchronization
- `blueprint-dev` head before this sync: `221131ac13b6680fa967750489209c8c4e14bcbf` — Home Course Workbook page-by-page audit.
- `d1-owner-dev` observed head: `5cf240fcf426074e2bbfc4c6b5280bd3f42c057d` — `D1O-02: materialize opportunity execution native 0E0W`.
- GitHub compare status: **DIVERGED**.
- `d1-owner-dev` was 59 commits ahead and 6 commits behind `blueprint-dev` at comparison time.
- Because both lineages contain unique work, no force branch move and no blind tree replacement is permitted.

## Canonical records synchronized now
The following latest decisions/contracts from the parallel workstream are now present on `blueprint-dev`:
1. `blueprint/decisions/N1_NESTED_MTF_MAPPING_DECISION_20260824.md`
2. `blueprint/contracts/M12N_NESTED_MTF_JOURNEY_ENGINE_CONTRACT.md`
3. `blueprint/decisions/D1_OPPORTUNITY_JOURNEY_EXECUTION_DECISION_20260825.md`

## Accepted latest project state
### D1 strategic owner
D1/MA50 strategic owner is no longer merely a future specification. The parallel D1 lineage contains implementation work through M11/M15/M16 and a native 0E0W materialization record. Canonical documentation must not describe the D1 implementation as simply "not started" without branch context.

### Nested / recursive MTF (NMJE)
Nesting is an approved and implemented workstream, not merely an informal concept.
- Source meaning: BBMA structures are recursive/nested across related timeframes.
- N1 architecture: M12N/NMJE is read-only/context/lineage first and consumes existing M08–M12 owner states.
- Supported hierarchy: `D1 -> H4 -> H1 -> M15`.
- N1 does not alter REM/RRE/REE signatures or M15 execution authority.
- Relation states include BUILDING, SUPPORTING, ALIGNED, CONFLICT, UNRESOLVED and NOT_APPLICABLE.
- JourneyID is engineering metadata, not signal authority.

### N2 shadow/research progression
The newer lineage contains N2 work for decision shadowing, closed-outcome attribution, telemetry, exact outcome identity hardening, runtime smoke dispatch and research/analyzer self-tests. These remain research/validation infrastructure unless a specific approved execution decision says otherwise.

### D1 Opportunity Journey (D1O)
The latest approved execution extension is recorded in `D1_OPPORTUNITY_JOURNEY_EXECUTION_DECISION_20260825.md`.
Key boundary:
- MA50 D1 Strategic Owner and D1 BBMA Opportunity Journey are distinct authorities;
- opportunity context is not a direct order trigger;
- M15 remains final new-entry authority and M16 remains fail-closed;
- initial D1O executable LTF structures are confirmed H1/M15 Re-Entry in Mode 2 under the decision's alignment/freshness rules;
- watch-only D1 MHV/MLV and eCSD have no independent execution authority.

## Important code-lineage boundary
This synchronization is a **record synchronization**, not a blind EA-source merge.

`blueprint/source/BBMA_EA.mq4` differs materially between the two branches. The compare showed about 1,999 changed lines in that file on the D1 lineage, alongside many workflow/tools/audit additions. The two lineages must be reconciled deliberately before declaring one source file canonical across both histories.

Do NOT:
- force `blueprint-dev` to the `d1-owner-dev` head;
- replace the `blueprint-dev` tree with the D1 tree;
- claim all D1/NMJE/N2 code is already present on `blueprint-dev` merely because its records are synchronized.

## Canonical interpretation rule after this sync
When answering project-status questions:
1. use `blueprint-dev` for canonical source/governance records;
2. consult the active parallel implementation lineage for D1/NMJE/N2/D1O implementation evidence;
3. distinguish **record synchronized** from **code merged**;
4. do not regress to older descriptions such as "nesting is only conceptual" or "D1 implementation is pending" without checking the latest branch state.

## Next repository action
Perform a deliberate implementation-lineage reconciliation/merge plan for `blueprint-dev` and `d1-owner-dev`, preserving:
- the six commits unique to `blueprint-dev` after the merge base;
- all accepted D1/NMJE/N2/D1O implementation commits;
- latest source-governance and Home Course audit records;
- build identity and native 0E0W traceability.

Until that merge is explicitly completed, this document is the canonical cross-branch synchronization marker.
