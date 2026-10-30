# D1 TPW During D1 Transition — Project Execution Decision

Date: 2026-10-27
Task: CORE-FIDELITY-292 / CP18
Decision scope: new-entry authority for D1_OPP_EXTREME_TPW only

## Decision

D1_TRANSITION and D1_OWNER_UNRESOLVED block every new-entry candidate, including D1_OPP_EXTREME_TPW. Apply the existing accepted Core §9.2 and M15 strategic-owner gate to this D1O-01 project extension.

The D1_OPP_EXTREME_TPW family may still oppose the direction of a confirmed D1 strategic owner when its existing valid/recovered aligned H4 and fresh confirmed H1 Re-Entry prerequisites pass. The decision does not add a D1-direction equality requirement to that family.

This is a deterministic fail-closed project execution mapping, not a new source-derived BBMA rule and not an accepted-Core edit. It applies only to new-entry authority; it does not introduce a close instruction for existing positions.

The dedicated D1 TPW lifecycle feature gate remains OFF. This decision does not authorize lifecycle activation, Strategy Tester use without qualified history, broker execution, live trading, merge or production deployment.

## Evidence and rationale

- Accepted Core §9.2 and the M15 contract already classify D1_TRANSITION and D1_OWNER_UNRESOLVED as blocking all new entries.
- D1O-01 separately allows D1_OPP_EXTREME_TPW to oppose the strategic owner under aligned H4 and fresh confirmed H1 Re-Entry prerequisites, but does not define a transition exception.
- The primary PDF p.2 describes the standard trend frame; it does not define this D1O-01 transition case. The secondary Re-Entry pages, Finale V01–V07 records and reviewed community/forum index yielded no explicit transition exception. Their silence is not represented as a direct source rule; the general accepted Core gate governs the extension.
- The selected mapping preserves the explicit Core contract and fails closed in an unresolved/transition state without removing the intended counter-direction case for a confirmed owner.

## Candidate implementation

Build 5.23 changes the D1O-TPW M15 authority check and M16 snapshot revalidation to call the existing IsD1MajorTrendOwnerExecutionReady helper. The helper admits only confirmed BUY/SELL owner states. M15/M16 retain the TPW family's direction exception; ordinary candidate direction equality is unchanged.

M11 owner production, M12/M13/M14 signatures, accepted Core, M17 lifecycle payload and the dedicated OFF gate are unchanged. Candidate source Git blob: be13aac3a2a0f2e2e9eeb2f5d4006eeedf7cd562.

## Verification and remaining status

Five focused portable exact-source regression scripts passed; the new transition regression contains four unittest methods. The exact source blob compiled on G40 HFM MetaEditor 5.0.0.2425 with 0 errors and 0 warnings. See CP18 logs and build523_manifest.json.

Qualified G40 history remains NOT VERIFIED. Strategy Tester, broker runtime and live execution were NOT RUN. The implementation owner remains Build 5.15; Draft PR #293 remains open, draft and unmerged, DO NOT MERGE.