# CORE-FIDELITY-292 — CP31 Build 5.28 native compile and history gate

Date: 2026-10-30. Phase: **EXACT-CANDIDATE NATIVE STRICT COMPILE PASS / STRATEGY TESTER BLOCKED**. Issue #292 / Draft PR #293.
Branch: `audit/core-fidelity-20261021`; parent head before this checkpoint: `6b3d77a5e7e87495648a8f1d17001afb5d43e1cc`.
Owner unchanged: `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de`, Build 5.15.

## VERIFIED

- Desktop Commander is connected to G40; no MT4, MetaEditor, or Strategy Tester process was running at the initial read-only process check.
- Exact Build 5.28 source was fetched from PR head `6b3d77a5e7e87495648a8f1d17001afb5d43e1cc`, staged at `C:\Users\AFIQMA~1\AppData\Local\Temp\BBMA_CORE_FIDELITY_BUILD528_EXACT\BBMA_EA.mq4`, and verified as 542,962 bytes.
- `git hash-object --no-filters` returned the expected Git blob `388ee68b5b8071d50dcf1dab1ddcb10733a120a9`; staged raw SHA-256: `CF63E3A4F40C55470B393317CF3EF43A062CF11DE402A5C8181DA9BCA671D4CB`.
- The exact source contains `#property strict`. HFM MetaEditor `5.0.0.2425` compiled it: **0 errors, 0 warnings**, 1,209 ms. Compile log SHA-256: `BA82D0599FF2701E53679DE2735E3700FA0726B5EE8ADC736D638614D434E7AB`. EX4 SHA-256: `968CF867B7FFE880201F02F740ADC4FF4EE2FBF9594A252E71E92A52279A2D45`; 777,902 bytes.
- After compile, the process snapshot showed no MT4, MetaEditor, or Strategy Tester process. No MT4 terminal restart or live order occurred.
- Read `D:\BBMA\AGENTS.md` and its required shared `D:\MARKET_DATA_INDEX.md/.json`. The index still reports `BLOCKED_CONFIRMED_VENDOR_GAP_AND_UNVERIFIED_TARGET_SESSIONS` and `strategy_test_authorized=false` for its XAUUSD/GBPUSD research datasets. This does not establish qualified BBMA history for the pending Re-Entry timing trace.

## PARTIAL / NOT VERIFIED

- The CP30 qualified-history gate remains **NOT VERIFIED**. Strategy Tester, broker runtime, and attributable `OrderOpenTime` trace remain **NOT RUN**.
- Ordinary Re-Entry timing remains **NOT VERIFIED**; pseudocode and the compile do not prove candle-time/order-time alignment.
- Build 5.15 owner source and trading state are unchanged. PR #293 remains open, Draft, and **DO NOT MERGE**.

## Exact next safe action

Establish an approved qualified-history manifest for the isolated Re-Entry timing trace. Only after that gate passes, run the tester trace recording the confirmation candle, actual next source bar (including a session-gap case), M15/M16 checks, `OrderSend`, and `OrderOpenTime`. Keep owner Build 5.15 and live trading unchanged.
