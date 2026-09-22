# M19 Selection Failure Implementation Plan
> Execute inline using executing-plans; one final independent review.
Goal: reject prospective entry when a monitored ticket cannot be selected.
Architecture: select once in CalculateTotalRisk, reject failure, then apply the unchanged registry/pair/magic ownership predicate to the selected order.
Tech stack: MQL4, Python, source-extracted C++ broker-stub diagnostic, native MetaEditor, isolated offline MT4.
Spec: blueprint/contracts/M19_RISK_FILTER_CONTRACT.md; Issue101 comment5768064904 F01; user chose option1.
## Constraints
Baseline f48a74e9d87c8c7ae2ac5b9f0ac6cf28e87391fd Build5.03 only.
TradeLock/source conflict and execution ambiguity remain HOLD. No M20/M22/M24 changes.
No primary restart, broker live/demo, production enablement. Standing merge authorization applies after verified exit criteria.
## Review focus
Unknown selection must reject, including transient first-call failure.
Closed and foreign selected rows remain excluded.
Owned/breakeven/empty/unknown-SL behavior remains unchanged.
No second selector can silently erase an already selected position.
All source outside CalculateTotalRisk and unique build identity remains byte-for-byte equivalent after newline normalization.
## Task 1: scoped M19 repair
Files: blueprint/source/BBMA_EA.mq4; blueprint/tests/run_m19_selection_probe.py; blueprint/tests/test_m19_owned_risk_aggregation_static.py.
Interface unchanged: CalculateTotalRisk(..., RiskValidationSnapshot &snapshot, bool &valid).
- [x] Recover owner/worktrees/processes and reuse prior audit. New isolated worktree at D:/BBMA/Workspace/m19-selection-failclosed-101.
- [x] Create source-extracted behavior test; baseline RED for first/persistent selection failures and duplicate selection.
- [x] Replace early boolean ownership helper in total-risk only: existing OrderSelect failure sets valid=false; selected closed rows skip; then identical FindPairStateIndex/expectedMagic/registry magic/live magic checks skip nonowned rows.
- [x] Assign Build5.04 and M19_SELECTION_FAIL_CLOSED_101_20260921 header/property/build/source/telemetry identity.
- [x] Run behavior probe GREEN; updated static guard and original ownership model; project pytest and relevant protected suites.
- [x] Compare complete source with f48 baseline, permitting only that function and identity fields.
## Task 2: validate and integrate
- [x] Native and exact three-transform tester adapter compile both 0E/0W.
- [x] Reuse prior Build503 offline smoke as comparator; run only new Build504 isolated smoke with existing blocked-network settings.
- [x] Backup then restore exact tester Global Variables bytes/hash; primary process unchanged.
- [x] Record evidence and scope limitations; independent whole-branch review.
- [ ] Commit, push unique branch, create fresh owner PR, verify exact head, mergeability/required checks, merge under standing authorization.
Ledger: task1 complete: RED3 to GREEN0,13 targeted scripts and22 pytest PASS, protected comparison PASS. Task2 validation complete: native/adapter0E0W, offline smoke and exact GV restore PASS; independent review no Critical/Important. Integration remains pending exact-head PR checks.
Ruling: retain identical ownership predicate locally after one broker selection, avoiding shared-helper changes or a second silent selection failure; cost if wrong is drift from shared predicate, guarded by preserved owner fixtures and review.

Final: minor (deferred): runner PREFIX comment retains Build5.03 wording; extraction operates on supplied candidate source.
