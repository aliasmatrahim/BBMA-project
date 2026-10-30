# CORE-FIDELITY-292 — CP01 recovery checkpoint
Date: 2026-10-22 (Asia/Kuala_Lumpur). Issue: #292. Phase: AUDIT / PARTIAL.
Branch: `audit/core-fidelity-20261021`.
Owner/base SHA: `459c0588e625d7f7630f0fb5612b7f04fda496de`; Build 5.15.
Checkpoint commit: resolve the commit adding this file; exact SHA also recorded in linked Draft PR.
Governance: `main:docs/BBMA_TASK_ORCHESTRATOR_CONTRACT.md`, Sections 4–7 and 10–11.
Latest user protocol takes precedence: no merge, force push or unrelated overwrite.

## VERIFIED milestone
- Live README, branch ownership, governance, CURRENT/MASTER_QUEUE and SOURCE_INDEX recovered.
- Current owner EA bytes inspected; newer Build 5.19 remains in unmerged PR #282.
- Owner regression command `python -m pytest blueprint/tests -q`: 72 passed in 1.43s.
- G40 Build 5.15 MQ4, production EX4, harness EX4 and tester report hashes match historical manifest.
- Historical native/harness compile logs: 0 errors / 0 warnings; source LF/CRLF identity reconciled.
- Seven repository manifest artifacts match raw bytes or explicit LF-to-CRLF conversion.
Evidence: `pytest.log`, `recovery_evidence.json`; historical package `NMJE_V2_P2_TARGETLESS_REPLAY_20260925`.

## PARTIAL / unresolved
- Full source-rule→contract→module→code→test→runtime matrix remains unfinished.
- Existing main traceability maps only F1–F6, pins an older commit and marks runtime NOT VERIFIED.
- 49/49 historical family classification is semantic accounting, not executable/runtime coverage.
- Finding A: M06 SMA/StandardDeviation skip unavailable closes; GetDataForTimeframe marks valid without complete-window/OHLC checks. Focused reproduction pending.
- Finding B: invalid H1/H4 refresh preserves old owners; potential M15/M16 admission of stale state. Cross-module reproduction pending.
- Both findings remain VERIFICATION REQUIRED; no confirmed repair or runtime occurrence claimed.
- Detector and entry reviewer turns stopped at usage limit; their preliminary findings are retained above.

## BLOCKED / NOT TESTED
- Qualified 2024–2025 historical strategy gate remains BLOCKED in G40 market-data index (vendor gaps/session evidence).
- New native compile, Strategy Tester, injected-invalid-history test and full per-rule runtime replay: NOT TESTED.
- EA source/contract/release changes: NONE. No terminal restart, trading activation or merge performed.
Modified files: this checkpoint, `recovery_evidence.json`, `pytest.log` only.

## Exact next atomic task
1. Verify live owner SHA and checkpoint branch; if unchanged, reuse all VERIFIED evidence above.
2. Reproduce Finding A from exact M06 function bodies with complete vs missing/short BB20 history; trace downstream invalid-data consumers for Finding B.
3. Classify against accepted valid-closed-candle/data contracts before proposing the smallest patch.
4. Only a confirmed patch receives a new unique build and static/native/targeted/runtime gates; checkpoint each verified boundary.
Exit for next task: reproducible data-validity defect or evidence-backed NO FIX, with exact source/test references.
