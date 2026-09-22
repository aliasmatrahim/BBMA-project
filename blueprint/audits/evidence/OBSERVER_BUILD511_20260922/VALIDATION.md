# Build 5.11 Event-Driven Observer Validation

Date: 2026-09-22
Issue: #237 / downstream #101 Observer finalization
Base: `d1-owner-dev@0cb24d250ce77c7629ef83d11b6c9db9c0773b1c` / Build 5.10
Source-bearing commit: `c1da06ea15e6cc31d097765043fba26899090b7e`
Candidate: Build 5.11 / `V511_EVENT_DRIVEN_OBSERVER_20260922`

## Classification
**CONFIRMED OBSERVABILITY BUG -> SCOPED FIX VERIFIED OFFLINE.**

Build 5.10 repeatedly emitted unchanged observer diagnostics on every processing cycle, making runtime evidence unnecessarily noisy. This was an observability defect only; trading authority was not implicated.

## Exact Build 5.10 RED / spam baseline
Reused the already-verified Build 5.10 August GBPUSD EveryTick runtime log.

Observed:
- N1-NMJE: 2,016 lines / 1,775 identical consecutive duplicates;
- D1-10A: 2,016 / 1,943 duplicates;
- D1-10B: 2,016 / 1,453 duplicates;
- D1-10C: 2,016 / 1,580 duplicates;
- M15_SELECT: 523 / 502 duplicates;
- M16_PASS: 523 / 506 duplicates;
- DECISION_FINAL: 523 / 467 duplicates, intentionally retained as execution-critical;
- exact Build 5.10 source lacks observer cache/helper and contains the raw cycle-driven prints.

Evidence: `BASELINE_510_SPAM.json`.

## Smallest repair
- one in-memory observer-owned key/message cache;
- changed-only emission for N1 journey summary, D1-10A/B/C, M15_SELECT and M16_PASS;
- `DBG_FULL` bypasses suppression deliberately;
- M15 count diagnostics print only at `DebugLevel >= DBG_SIGNAL`;
- final decision, rejection/failure, preflight/execution, ticket/open, lifecycle invalid/reset, F07/recovery safety and N2 research telemetry remain direct/unconditional at their existing owners;
- cache allocation failure fails open for observability and cannot alter strategy/risk/execution authority.

No Strategy Core, candidate eligibility, M15 selection authority, M16 rejection semantics, SL/TP, risk/MM, execution, lifecycle or recovery behavior changed.

## Static / cross-module
- observer state model: PASS;
- observer source/critical-log guard: PASS;
- protected Build 5.10 bodies: 28/28 exact;
- M15 logic projection outside intended diagnostics: exact;
- M16 validation/rejection path through DEC_VALIDATED/REJ_NONE: exact;
- N1 P1 static + epoch model: PASS;
- N2 F07 open + closed bridges: PASS;
- F07 ambiguity model/static: PASS;
- NMJE read-only authority + M12N ordering: PASS;
- M25 dashboard guard: PASS;
- full pytest: 22/22 PASS;
- `git diff --check`: PASS;
- production `OrderSend(` count remains one;
- no NMJE execution gate / N3 activation / M5 processing marker introduced.

## Compile identity
- source/native MQ4 SHA-256: `50E4A01A5768B5B5E9A80CABAE21B7260A2912AA058E67E5273386177970D038`;
- native EX4 SHA-256: `CFF8DA584C91AE177CA26E1C47518AA585A67F0E16C99295F932670E8CDEC6E1`;
- native MetaEditor: **0 errors / 0 warnings**;
- exact three-transform tester adapter MQ4 SHA-256: `D3ADEAA06888B1CEC03A10852EEF8491743336A95084D84DD2EFE8B703046832`;
- adapter EX4 SHA-256: `8F6B1D8F6665E6DC72CF5A463A99D1A67F0CBB5E8CA73C4E133A4CFFF4FE387F`;
- adapter MetaEditor: **0 errors / 0 warnings**.

## DBG_OFF EveryTick acceptance
GBPUSD M15, 2026-08-01 through 2026-09-01, isolated tester.

Critical traces are byte-exact to Build 5.10:
- DECISION_FINAL 523;
- PREFLIGHT_PASS 325;
- EXEC 14;
- F7 MOMENTUM_HOLD 3;
- F7 EXIT_LATCHED 10;
- F7 CLOSE_SUCCESS 10;
- N2-NMJE-DEC 523;
- N2-NMJE-OUT 14.

Observer output equals the exact per-key changed-only projection of the Build 5.10 baseline:
- N1-NMJE: 2,016 -> 241;
- D1-10A: 2,016 -> 73;
- D1-10B: 2,016 -> 563;
- D1-10C: 2,016 -> 436;
- M15_SELECT: 523 -> 21;
- M16_PASS: 523 -> 17;
- M15_COUNTS: 523 -> 0 at DBG_OFF by explicit contract.

Every projected observer sequence is byte-exact to the expected baseline projection. Fatal runtime markers = 0; mismatched chart errors = 0.

## DBG_FULL override acceptance
Same GBPUSD M15 / August 2026 window with `DebugLevel=DBG_FULL`.

All 15 checked marker families are byte-exact to Build 5.10, including:
- full N1/D1 observer streams;
- M15_COUNTS / M15_SELECT / M16_PASS;
- final decision / preflight / execution;
- F07 lifecycle telemetry;
- N2 decision/outcome telemetry.

This proves verbose diagnostics can be deliberately restored without changing behavior. Fatal runtime markers = 0; mismatched chart errors = 0.

## Runtime isolation
Both tester runs restored `gvariables.dat` exactly to 240 bytes, SHA-256:
`DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6`.

Primary MT4 PID 13064 remained the sole terminal after each run.

## Boundary
No production activation, primary MT4 restart, live/demo broker action or live-readiness claim.
Raw tester logs remain on G40 and are identified by `RUNTIME_MANIFEST.json`.
