# CORE-FIDELITY-292 — CP30 Accepted Core pseudocode audit

Date: 2026-10-28. Phase: **STATIC RECONCILIATION COMPLETE / RUNTIME NOT VERIFIED**. Issue #292 / Draft PR #293.
Branch: `audit/core-fidelity-20261021`; parent: `00eb37be618e55358b6f02cdc807be8ceddbcb03` (CP30 pseudocode crosswalk added to the existing source-fidelity matrix).
Owner unchanged: `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de`, Build 5.15; source blob `09de8b80fdaeeb2fd614de0a1826134e9a8b2411`.
Authority reused per SOURCE_INDEX: accepted Core V2 blob `e3a5a97d1a0a76dc9aaef51701e74ec5bd6b5f84`; M12 contract blob `6d9f50ae07aec988de346ffb2cc66ed1a90e2559`; prior source/CP14 timing evidence reused.

## VERIFIED
- Added a closed-candle M12 Type 1–4 pseudocode and exact Build 5.15 static crosswalk to `SOURCE_FIDELITY_MATRIX.md`; extended the existing audit rather than creating a duplicate document.
- Type 1–4 lifecycles statically map to M12; empty-owner Type3→Type4→Type2→Type1 is explicit project policy from CP16, not source precedence or evidence of market overlap.
- Reused confirmed findings: Build 5.15 stale-source admission (CP06 reproduction; Build 5.22 candidate gate/CP08 compile) and M06 incomplete-history validity defect (Build 5.20 candidate). Owner remains unchanged.
- Ordinary timing is statically mapped: closed validation candle, `EntryCandle` nominal next-period metadata, M15/M16 final gates. D1O-01 separately consumes `EntryCandle` as activation.
- No MQL4/Core source, tests, compile, Strategy Tester, broker runtime, order, merge, terminal restart or trading activation changed/ran.

## PARTIAL / NOT VERIFIED
- No attributable `OrderOpenTime` trace proves an ordinary Re-Entry fill inside the immediately following actual source candle. Do not claim timing PASS from pseudocode or metadata.
- `ConfirmationCandle + timeframe seconds` may not equal the next actual bar timestamp at weekend/session gaps; test against the bar series, especially for the D1O-01 activation boundary.
- Strategy Tester remains gated on qualified history. G40 Desktop Commander remains quota-blocked; CP29 says do not retry or reconnect.

## Exact next safe action
- After Desktop Commander access is restored, continue CP29's exact Build 5.28 hash/staging/native-compile step. After the data gate passes, capture an isolated tester trace with confirmation, actual next-bar, M15/M16, OrderSend and OrderOpenTime timestamps, including a session-gap case.
- Keep PR #293 Draft/DO NOT MERGE; no terminal restart or live trading.