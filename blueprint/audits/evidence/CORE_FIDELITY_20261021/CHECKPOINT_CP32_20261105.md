# CORE-FIDELITY-292 — CP32 history qualification recovery

Date: 2026-11-05 MYT. Status: PARTIAL / HISTORY QUALIFICATION IN PROGRESS.
Parent audit head: 37bbc57aa08255f5eb15c84101175bf6b8a53349. Issue #292 / Draft PR #293.
Owner remains d1-owner-dev / Build 5.15; candidate Build 5.28.

## Recovered evidence
- Live README, audit CURRENT/MASTER_QUEUE, SOURCE_INDEX, CP31 and PR #293 recovered. G40 online on device 92a22482-bf2c-41e2-af83-884f432a7e68.
- Q8 audit explicitly retains GBPUSD engineering history as READY FOR ISOLATED ENGINEERING STRATEGY TESTER USE, NOT FINAL TICK-ACCURATE / NOT DEPLOYMENT-BROKER CANONICAL.
- Canonical Q8 evidence: blueprint/audits/Q8_BUILD486_GBPUSD_ENGINEERING_HISTORICAL_REGRESSION_20260918.md and its local_evidence_manifest.json.
- Q8 covers six HST timeframes and includes an August 2026 smoke. Its old Build 4.86 runtime PASS does not verify Build 5.28 timing.
- Shared market-data index read remains dated 2026-10-31 and blocks its research-derived datasets. This must not be generalized into absence of the separate Q8 engineering profile. Applicability to the pending timing trace remains VERIFICATION REQUIRED.

## In-flight G40 verification
- First hash command failed because nested PowerShell expansion removed $_; no hash PASS was produced.
- Corrected read-only hash process PID 15244 hashes existing GBPUSD*.hst in D:\BBMA\MT4_TesterRunner_OfflineDiag\history\MetaQuotes-Demo using Get-FileHash SHA256.
- Last session inspection: PID 15244 active, Blocked=false, runtime 79s; no output yet. Do not duplicate the hash process. Resume using read_process_output for PID 15244.
- Expected six hashes are in the committed Q8 local_evidence_manifest.json. No file mutation or tester launch occurred.

## Exact next action
Collect PID 15244 output; compare all six paths/hashes with Q8 manifest. If identical, document narrow engineering-profile applicability, inspect actual candle coverage/warm-up and session-gap cases for the chosen window before approving any Build 5.28 trace. Hash equality alone does not clear coverage or exact-broker/tick gates. Retrieve accepted Core/contracts/current candidate before instrumentation or code changes.
Timing remains NOT VERIFIED; Strategy Tester for Build 5.28 NOT RUN. No EA/Core source change, merge, terminal restart or trading activation.
