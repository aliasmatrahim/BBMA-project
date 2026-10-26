# CORE-FIDELITY-292 — CP06 current-source stale-owner gate
Date: 2026-10-26. Phase: AUDIT / PARTIAL. Issue #292.
Branch: `audit/core-fidelity-20261021`; parent checkpoint: CP05 / PR head `7627b9720a45d045820dc8736640b5a86c2655b7`.
Owner baseline unchanged: `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de`, Build 5.15.
Candidate: Build 5.21 / `V521_M12_CURRENT_SOURCE_ADMISSION_20261026`; source commit `9414608844874af4b6613783316fd8ccd5ce0a52`.
Checkpoint commit SHA is returned by this file's commit and recorded in Draft PR #293.

## VERIFIED
- Exact-source RED reproduction: invalid H1 and invalid H4 refresh retained old M12/H4 owners; candidate reached M15, passed M16 and entered the preflight dispatch.
- Build 5.21 GREEN: four portable exact-source unittest methods pass. Invalid H1/H4 now fail before M15 selection; forced stale decisions fail M16; valid closed H1/H4 control still passes.
- M15 checks each Re-Entry component against its exact latest closed snapshot and checks current H4 data/owner where candidate construction depends on H4 alignment. M16 repeats the check. M12/H4 owner persistence and no-age-expiry semantics are preserved.
- Preflight dispatch and M17 -> risk -> portfolio call order were checked statically. The test stub stops before broker APIs; no M17/risk/portfolio runtime or order call occurred.
- Evidence: `test_m12_stale_owner_refresh.py`, `m12_red.log`, `m12_green.log`, and `build521_manifest.json`. Build 5.21 source SHA-256: `2d484f2aca5eb9487e11f04197b6ce8a0db181df6c8b36c78b0605dfb0b24aff`.

## Modified candidate artifacts
- EA source, focused regression test and Build 5.21 manifest/logs.
- M12, M15 and M16 contracts; CURRENT, MASTER_QUEUE, source-fidelity matrix and cross-module candidate-delta ledger.
- No owner branch, production EX4 or Strategy Tester artifact changed.

## PARTIAL / NOT TESTED
- Native strict compile for Build 5.21: NOT TESTED.
- Strategy Tester and broker/runtime preflight: NOT TESTED. G40 qualified-history gate remains blocked.
- Full Core rule denominator, shared-field ownership and attributable runtime matrix remain PARTIAL. Draft PR remains unmerged; no trading activation.

## Exact next action
Run native strict compile on this exact Build 5.21 source in the approved compile environment. Only after compile, use Strategy Tester when the qualified G40 history gate is available; preserve the failure-injection fixture and do not send orders.