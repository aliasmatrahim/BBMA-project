# CORE-FIDELITY-292 — CP18 D1 TPW transition policy and candidate fix

Date: 2026-10-27. Phase: POLICY RESOLVED / PORTABLE REGRESSION + NATIVE COMPILE VERIFIED; RUNTIME PARTIAL.
Branch: audit/core-fidelity-20261021; parent CP17: 289eaa0bbdb5c0cbacb5234a85c5af0d9af11bc3.
Owner: d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de, Build 5.15.
PR #293 remains open, draft, unmerged and DO NOT MERGE. Exact checkpoint commit is recorded in the PR body after push.

## VERIFIED
- User-approved project mapping: D1_TRANSITION and D1_OWNER_UNRESOLVED block D1_OPP_EXTREME_TPW under accepted Core §9.2/M15; no Core/source rule changed.
- Candidate Build 5.23 uses IsD1MajorTrendOwnerExecutionReady in M15 admission and M16 revalidation; counter-direction remains allowed against a confirmed owner with existing D1O-01 H4/H1 prerequisites.
- Five focused portable scripts passed (four new exact-source unittest methods); see build523_regression_g40_20261027.log.
- Exact Git-blob source be13aac3a2a0f2e2e9eeb2f5d4006eeedf7cd562; source SHA-256 and compiler/log/EX4 hashes are in build523_manifest.json.
- G40 HFM MetaEditor 5.0.0.2425 strict compile: 0 errors / 0 warnings; see build523_native_compile_g40_20261027.log.
- Code and governance changes are isolated to candidate branch; owner Build 5.15 and M17 OFF gate are unchanged.

## NOT VERIFIED / NOT RUN
- Qualified G40 history remains NOT VERIFIED; Strategy Tester, broker/runtime and live execution NOT RUN. Terminal stayed stopped.
- Full Core rule denominator, C039/C040 observer extension, and end-to-end runtime mapping remain PARTIAL.
- No merge, terminal restart, lifecycle activation or trading authorization.

## Files and exact next action
- Decision: blueprint/decisions/D1_TPW_D1_TRANSITION_FAIL_CLOSED_DECISION_20261027.md; M15/D1 contracts, cross-module ledger, fidelity matrix, CURRENT, MASTER_QUEUE and Finale gap/index reconciled.
- Continue the next eligible static audit at accepted Core §10; revisit Strategy Tester only after qualified history and required runtime gates are resolved.