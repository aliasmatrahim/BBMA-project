# CORE-FIDELITY-292 — CP03 M06 repair / native compile
Date: 2026-10-22 (Asia/Kuala_Lumpur). Phase: VALIDATION / PARTIAL. Issue #292, Draft PR #293.
Branch: `audit/core-fidelity-20261021`; parent: `ad738fa6314fb544fdb6e9fddb6f90a911936357` (CP02).
Owner unchanged: `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de`.
Checkpoint SHA: commit adding this file; exact SHA recorded in PR #293.

## VERIFIED boundary
- Finding A repaired in scoped source Build 5.20 / `V520_M06_COMPLETE_DATA_20261022`.
- M06 requires full indicator-period inputs, finite positive prices, valid target OHLC and indicator outputs.
- BB20 no longer reduces its divisor on unavailable closes; zero deviation remains valid for flat prices.
- Source SHA256: `ebb139f00ba24fe5c1b0f9a26fcb4a027f36c8b074e001201ef3bfe35b0f2d79`.
- Exact-body portable regression: 15 passed; full `python -m pytest -q`: 87 passed.
- Initial full run caught four stale runtime build-label assertions; corrected label, full rerun green.
- Native strict MetaEditor compile on G40: 0 errors, 0 warnings, 882 ms; EX4 hash in manifest.
- Static diff scope: M06 + build identifiers only; M15 clock, M12N and downstream trade policy unchanged.
- Direct BB consumers already reject unavailable/zero-width bands; standalone indicator wrappers now require their periods.

## Evidence / files
`build520_manifest.json`, `compile520.txt`, `m06_green.log`, `pytest_520.log`, `pytest_520_identity_red.log`.
Source: `blueprint/source/BBMA_EA.mq4`; CP02 test retained unchanged; matrix updated.
G40 isolated files: `D:\BBMA\Workspace\CORE_FIDELITY_292_20261022\BBMA_EA_520.{mq4,ex4}` / `compile520.log`.
Failed PowerShell script launch changed no execution policy; materialized with Python, compiled via direct MetaEditor.
No deploy, terminal restart, merge, forced update or trading activation.

## PARTIAL / BLOCKED / NOT TESTED
- Build 5.20 is NOT RUNTIME VERIFIED. Native compile is not Strategy Tester or broker execution evidence.
- Qualified Strategy Tester data gate remains BLOCKED in G40 MARKET_DATA_INDEX.md/json.
- No new source-to-runtime replay, signal timing, order/SL/TP/exit or profitability verification.
- Finding B stale-owner admission remains VERIFICATION REQUIRED; M06 validity does not itself close this path.
- Full M01–M27/M12N rule denominator and traceability remain PARTIAL; no coverage percentage claimed.

## Exact next step
1. Reproduce B from actual candidate/admission/revalidation functions with valid D1/M15 and unreadable H1/H4.
2. Determine whether M17/risk can actually mask it; they cannot substitute for Strategy-Core validity.
3. Any further confirmed fix requires its own unique build and gates. Do not merge/release Build 5.20.
4. Runtime closure requires eligible data or a separately scoped native fixture replay; preserve blocked historical gate.
