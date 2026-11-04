## CP27 — M11 read-only owner and predicate inputs (2026-10-27)

Task: Issue #292 / Draft PR #293. Build 5.27 targeted static regression and exact-candidate native strict compile PASS; runtime NOT RUN.
Branch: `audit/core-fidelity-20261021`; parent: `98a7a0eacb18ad5301ab6b9bd9396cef67d6054e`. Owner: `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de` / Build 5.15.
- Candidate: `V527_M11_CONST_READONLY_OWNER_INPUTS_20261027`; source blob `3cac5ac00d8c8241201a435e7284bd5092c847d4`; G40 raw SHA-256 `D1E687DDFEBB19FA0020A46D28954E00D4E0D47A0F91A2D33437FAF036F43D37`.
- Const-qualified nine proven read-only parameters across seven M11 functions: D1 owner epoch input, trace state, confirmed-ReEntry predicate/selector inputs, mature-Extreme predicate/selector inputs, and TPW Extreme input.
- Bodies and call sites are unchanged. All seven function call-occurrence counts match Build 5.26; selector outputs and classifier outputs remain mutable.
- Static regression: Build 5.26 baseline RED; candidate GREEN; 11 unique allowlisted source replacements; reverse allowlist restores the exact baseline; zero direct writes found for the nine inputs.
- HFM MetaEditor 5.0.0.2425 strict compile: PASS, 0 errors / 0 warnings, 954 ms. Log SHA-256 `2130A74B495035C8AC215DB51F9946985CEAF8EF0230C2B196C3E97B454CBF2B`; EX4 SHA-256 `0734C90F4DFAFA54357C4C9282DA88CC53DF64CD4AA1ED595AEE7087E351140C`.
- Strategy Tester, broker runtime, and orders were NOT RUN. G40 check after compile found no MT4/MetaEditor process; no terminal restart or trading activation.
- Owner-branch `CURRENT.md`/`MASTER_QUEUE.md` still name prior owner head `0034f31a...`; live branch/PR base is `459c0588...`. Live refs win; status-file drift remains to reconcile.
- PR #293 remains open/Draft/DO NOT MERGE. Q10 R5-14/R5-16 still require natural broker events; do not synthesize.
Next action: audit M06 SMA/StandardDeviation handling of incomplete BB20 history against the TimeframeData validity contract and call paths; do not patch until a focused reproduction confirms impact.
