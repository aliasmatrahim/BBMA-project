## CP26 — M11 D1 snapshot const boundary (2026-10-27)

Task: Issue #292 / Draft PR #293. Phase: Build 5.26 targeted static regression and exact-candidate native strict compile PASS; runtime NOT RUN.
Branch: `audit/core-fidelity-20261021`; parent: `2c5299f6409b610bbedf463253fc65dee3566e78`. Owner remains `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de` / Build 5.15.
- Candidate: `V526_M11_CONST_READONLY_SNAPSHOT_INPUTS_20261027`; source blob `f134ff476a16b5834798fff9b3de90bfafbeb495`; G40 raw SHA-256 `5360330D8B57CFB8DE5BAF12824CA18095D446E5CDD2D59D1E82A1920419AF9B`.
- Added const only to M11 `latestClosedD1` and the `data` snapshots of `DetectD1OpportunityCSD` and `DetectD1OpportunityECSDWatch`.
- Bodies and callers are unchanged; six call occurrences remain 2 per function. The CSD/eCSD helpers receive only scalar `barIndex`; TPW reads snapshot fields only.
- Targeted source regression: baseline RED for three missing const qualifiers; candidate GREEN, exact reverse allowlist restores the full Build 5.25 source, no snapshot writes and no call-count drift.
- HFM MetaEditor 5.0.0.2425 strict compile: PASS, 0 errors / 0 warnings, 981 ms. Log SHA-256 `142692ADC5EBEEE4D04DAD67E6A9661ACA8F5E66A28D94FC510D9C758867337D`; EX4 SHA-256 `9C4A2C0D3717416BDBCFE18F0061D6D0F45CFE2422956D022A3E6E84CEE50192`.
- Strategy Tester, broker runtime and orders were NOT RUN. Owner Build 5.15 is unchanged. No MT4/MetaEditor process remained after compile; no terminal restart.
- PR #293 remains open/draft/DO NOT MERGE. Q10 R5-14/R5-16 remain natural-event blockers; no event was synthesized.
Next action: continue auditing remaining M11 by-reference bodies and call paths; keep owner source and runtime authority unchanged.
