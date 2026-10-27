## CP28 — M06 status correction and M10/M11 read-only inputs (2026-10-27)

Task: Issue #292 / Draft PR #293. Build 5.28 source regression PASS; native strict compile NOT TESTED because the G40 Desktop Commander monthly quota is exhausted.
Branch: `audit/core-fidelity-20261021`; parent: `02395c6db18607e8776c0d74c04ef0bac9885313`. Owner remains `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de` / Build 5.15.
- Correction: CP27's next action named M06, but the audit candidate already contains the verified Build 5.20 M06 repair. CP03, `m06_green.log`, and `build520_manifest.json` record 15 focused passes and native strict compile 0 errors / 0 warnings. Build 5.15 owner source still lacks this repair; do not repeat it.
- M12/H4 stale-source admission has candidate repairs in Builds 5.21/5.22; CP06/07 record exact-source probes and CP08 records Build 5.22 native compile PASS. These remain unmerged from owner Build 5.15.
- Candidate Build 5.28: `V528_M10_M11_CONST_DIRECTION_INPUTS_20261027`; source blob `388ee68b5b8071d50dcf1dab1ddcb10733a120a9`; G40 staging was NOT completed.
- Const-qualified five proven read-only parameters across `DetectCSD`, `DetectECSD`, `DetectD1OpportunityCSD`, and `UpdateD1OpportunityJourney`. Bodies and call sites are unchanged; all six/five/three/two function occurrence counts remain stable.
- Targeted source regression PASS: Build 5.27 baseline lacks the five const boundaries; candidate passes; reverse allowlist restores the exact baseline; zero direct input writes found.
- Desktop Commander reported monthly usage exhausted and instructed not to retry or reconnect. Native compile is BLOCKED / NOT TESTED; no compile log or EX4 exists for Build 5.28.
- Strategy Tester, broker runtime, and orders were NOT RUN. Owner source/release/runtime were not changed.
- PR #293 remains open/Draft/DO NOT MERGE. Q10 R5-14/R5-16 remain natural-event gates; no event synthesis or terminal restart.
Next action: after Desktop Commander usage resets, stage this exact blob on G40, verify `git hash-object`, run HFM MetaEditor strict compile, then checkpoint the result.
