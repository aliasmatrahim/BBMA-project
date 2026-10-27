## CP25 — M08/M09 leaf input const hardening (2026-10-27)

Task: Issue #292 / Draft PR #293. Phase: **Build 5.25 static regression and exact-candidate native strict compile PASS; runtime NOT RUN**.
Branch: `audit/core-fidelity-20261021`; parent: `5d4e001f18932eba02ea3c41cfc139e43e01377e` (CP24). Owner remains `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de` / Build 5.15.

- Candidate: Build 5.25 / `V525_M08_M09_CONST_LEAF_INPUTS_20261027`; canonical Git blob `9eb016ed13d90a57a992aa14c18072a44c3c4ab2`; G40 staging SHA-256 `5C25B25FF0AD2E75E9DD84E061150F5AE35FC6835C57681678FE39661E236524`.
- Added `const TimeframeData &data` to six audited leaf helpers: `IsExtremeReversalDirection` (2 callsites), `IsExtremeRetestStart` (1), `IsMHVTPWajibCompleted` (1), `GetMHVBodyEdge` (1), `IsMHVFormationMoveAway` (1), and `IsMHVRetestInteraction` (1).
- Complete bodies are unchanged and contain no writes to the `TimeframeData` input. Five are direct read-only predicates; `GetMHVBodyEdge` calls `MathMin/MathMax` with scalar open/close values only. All six callsite counts are unchanged.
- HFM MetaEditor 5.0.0.2425 strict compile: **PASS — 0 errors / 0 warnings, 934 ms**. G40 log SHA-256: `A8B8AD4B10EC3926616DF97AE680711CB27087E0D68DEF3A7B1994F1C456A6B9`; EX4 SHA-256: `7E7FB5B69E6610AB20651740027C0A72B9D5B40678044AAA2D237DDC8C1945BC`. Manifest: `build525_manifest.json`.
- Strategy Tester, broker/runtime and orders were NOT RUN. Owner source and release state are unchanged; PR #293 remains Draft/DO NOT MERGE.
- Q10 Phase L R5 remains highest-priority global acceptance, gated on natural R5-14/R5-16 events. No Q10 event was generated. Next safe action: continue auditing remaining by-reference bodies and call paths; only qualify inputs whose complete read-only behavior is proven.
