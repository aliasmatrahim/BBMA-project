## CP24 — M08 const read-only input hardening (2026-10-27)

Task: Issue #292 / Draft PR #293. Phase: **Build 5.24 static regression and exact-candidate native strict compile PASS; runtime NOT RUN**.
Branch: `audit/core-fidelity-20261021`; parent/head before this checkpoint: `913e7eaafcf564a763c7a4093d7475be16b3d2be`.
Owner remains `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de` / Build 5.15. Draft PR #293 remains DO NOT MERGE.

- Candidate: Build 5.24 / `V524_M08_CONST_READONLY_INPUTS_20261027`; canonical Git blob `98d5403283782922ba85d1459d12eaf1ce921316`; G40 Windows staging SHA-256 `A251BBECCD4DF59B28C4A1E429DACF6EC68417B85F04405192E828CFDE8C5937`.
- Scope: added `const` to the `TimeframeData &data` inputs of `GetExtremeRelevantMA5` and `GetExtremeReversalBodyEdge`; updated the unique version/header/build tag. No helper body or caller changed.
- Static targeted regression PASS: normalized source diff is limited to those five lines; both helper bodies are byte-identical to Build 5.23; callsite counts remain 8 and 2.
- Clarification to CP23 wording: `GetExtremeReversalBodyEdge` calls built-in `MathMax/MathMin` with scalar open/close values. It does not pass the `TimeframeData` reference onward or mutate it.
- HFM MetaEditor 5.0.0.2425 strict compile: **PASS — 0 errors / 0 warnings, 1081 ms**. G40 log SHA-256: `46BDD47820011E2A72C8403F2243BC6C4F952FB84249666033B2D7C82732ACB0`; EX4 SHA-256: `053DAE5F4D844229639856C2B7C8BF97627B7C43C3A024BCA9BE1860CEA0DFDE`. Manifest: `build524_manifest.json`.
- After compile, no MT4 terminal or MetaEditor process remained. Strategy Tester, broker/runtime and orders were NOT RUN. No owner source, release state or live trading changed.
- Q10 Phase L R5 remains the global acceptance priority; the live queue gates R5-14/R5-16 on natural broker events. G40's inspected `Q10_109/STATE.json` is dated 2026-09-23 and reports `DEMO_LOG_MISSING`; it is older than the 2026-10-27 queue reconciliation and does not replace the queue's R3/R4 PASS / R5 pending record. No event was synthesized.
- Next safe action: continue body-and-callee review of remaining no-write reference parameters. Do not infer read-only status from the analyzer alone; compile any new candidate against its exact Git blob.
