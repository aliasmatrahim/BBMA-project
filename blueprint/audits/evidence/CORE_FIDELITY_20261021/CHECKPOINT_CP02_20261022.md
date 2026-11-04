# CORE-FIDELITY-292 — CP02 exact-source data-validity reproduction
Date: 2026-10-22 (Asia/Kuala_Lumpur). Phase: VALIDATION / PARTIAL. Issue #292, Draft PR #293.
Branch: `audit/core-fidelity-20261021`; parent checkpoint: `7d922f162c730bedebd3875d13dd2c71b9b68a93`.
Owner remains `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de`, Build 5.15.
Checkpoint SHA: commit adding this file, also recorded in PR #293.

## VERIFIED boundary
- Live owner/main/audit refs and Draft PR #293 unchanged since CP01; verified baseline evidence reused.
- G40 primary terminal remains PID 9508; no duplicate tester/compiler process observed.
- Exact M06 bodies compiled as C++ with deterministic terminal API fixtures (not native MQL4).
- Complete BB20 numerical control, minimum 50-source-bar control and flat-price control pass.
- Baseline has 12 expected assertion failures / 3 passing controls; `m06_red.log` records each case.
- Partial BB20 (19 observations), missing/nonfinite close, insufficient EMA50 history,
  missing High, invalid OHLC and unavailable/nonfinite MA can produce a valid snapshot.
- Finding A: CONFIRMED BUG at deterministic engineering boundary, not a proven live trade occurrence.
- No code repair yet; failing regression intentionally captures the pre-repair boundary.

## Traceability / scope
See `SOURCE_FIDELITY_MATRIX.md`: explicit indicator settings vs accepted Core vs data-integrity mapping.
No discretionary rule, signal threshold, strategy lifetime or M12N authority is added.
Modified files: this checkpoint, matrix, `m06_red.log`, `blueprint/tests/test_m06_data_validity.py`.
CP01 remains valid for its unchanged source and historical artifacts, not a claim about future builds.

## PARTIAL / BLOCKED / NOT TESTED
- Finding B stale owner admission remains VERIFICATION REQUIRED; M16 checks identities but not refreshed data.
- Full M01–M27/M12N matrix and runtime rule denominator remain unfinished; no percentage claim.
- G40 market-data index still BLOCKED for qualified 2024–2025 Strategy Tester data.
- Native compile/new runtime/qualified Strategy Tester for any repair: NOT TESTED.
- No source/contract/release change, merge, terminal restart or trading activation.

## Exact next atomic tasks
1. A-REPAIR: reject incomplete BB periods and unavailable snapshot inputs; preserve complete-data outputs.
   Unique build identity; static/native strict compile, focused tests and full suite; inspect runtime feasibility.
2. B-REPRO: prove whether invalid H1/H4 refresh can pass M15/M16 through actual functions;
   preserve structural owner lifetime and do not convert temporary missing data into invented expiry.
3. Append CP03 at next verified boundary; continue full traceability, carrying data gate separately.
