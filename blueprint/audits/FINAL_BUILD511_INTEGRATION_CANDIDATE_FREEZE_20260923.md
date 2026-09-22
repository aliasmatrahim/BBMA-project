# Final Build 5.11 Integration Candidate Freeze — 2026-09-23

Issue: #241 / downstream #101
Candidate owner baseline: `d1-owner-dev@e7752f30d046189aff4e003494f47fb59086de87`
EA: Build 5.11 / `V511_EVENT_DRIVEN_OBSERVER_20260922`
Canonical source: `blueprint/source/BBMA_EA.mq4`

## Result

**PASS — exact Build 5.11 final integration candidate frozen for offline/engineering acceptance.**

This stage changes no EA/Core/contract source. It proves exact candidate identity, reuses attributable exact-source native/static/runtime evidence, and adds fresh candidate-specific GBPUSD engineering historical regression for the four required windows.

This is **not** a profitability endorsement, final tick-accurate market-data claim, production/live activation, or HFM demo acceptance.

## Candidate identity

- owner head: `e7752f30d046189aff4e003494f47fb59086de87`;
- source-bearing commit: `c1da06ea15e6cc31d097765043fba26899090b7e`;
- source diff from source-bearing commit to frozen owner: **0**;
- canonical MQ4 SHA-256: `50E4A01A5768B5B5E9A80CABAE21B7260A2912AA058E67E5273386177970D038`;
- native EX4 SHA-256: `CFF8DA584C91AE177CA26E1C47518AA585A67F0E16C99295F932670E8CDEC6E1`;
- exact three-transform tester adapter MQ4: `D3ADEAA06888B1CEC03A10852EEF8491743336A95084D84DD2EFE8B703046832`;
- tester adapter EX4: `8F6B1D8F6665E6DC72CF5A463A99D1A67F0CBB5E8CA73C4E133A4CFFF4FE387F`;
- engineering regression settings SHA-256: `37BC585EB3AB5A73914FEC3C532023636D4FACCD7D3AAAF20B774269CF92DA70`.

The G40 CRLF checkout difference does not alter canonical Git content; the normalized worktree bytes match the canonical source hash.

## Reused exact-source gates

Because Build 5.11 source content is byte-exact to the previously validated source-bearing commit, the following evidence is reused rather than duplicated:

- native MetaEditor compile: **0 errors / 0 warnings**;
- exact tester adapter compile: **0 errors / 0 warnings**;
- Build 5.11 August-2026 GBPUSD M15 EveryTick DBG_OFF runtime acceptance;
- Build 5.11 August-2026 DBG_FULL override acceptance;
- fatal runtime markers = 0 and mismatched-chart errors = 0 in those runs;
- exact GlobalVariable restoration;
- Build 5.11 M01-M27 + M12N cross-module invariant audit: **68/68 PASS**.

References:
- `blueprint/audits/evidence/OBSERVER_BUILD511_20260922/COMPILE_MANIFEST.json`;
- `blueprint/audits/evidence/OBSERVER_BUILD511_20260922/VALIDATION.md`;
- `blueprint/audits/evidence/M01_M27_M12N_BUILD511_20260923/FINAL_INVARIANTS.json`.

Fresh current-branch pytest during this freeze: **22/22 PASS**.

## Historical data / tester boundary

Pair: **GBPUSD only**.
Timeframe: **M15**.
Model: **Every tick**.
Spread: **20 points**.
Optimization: **off**.

The six installed GBPUSD HST files (`M1/M5/M15/H1/H4/D1`) were hash-gated to the same verified engineering historical profile previously used by Q8. No native archive acquisition was restarted.

Evidence class remains:

**ENGINEERING HISTORICAL EVIDENCE / NOT FINAL TICK-ACCURATE**

The tester adapter is test-only and not a deployable replacement for the canonical Build 5.11 binary.

## Fresh Build 5.11 historical matrix

| Period | Trades | Net profit | Profit factor | Max DD | Mechanism acceptance |
|---|---:|---:|---:|---:|---|
| 2024 | 396 | -47.47 | 0.79 | 75.89 (0.76%) | PASS |
| 2025 H1 | 205 | -22.17 | 0.86 | 56.63 (0.57%) | PASS |
| 2025 H2 | 173 | +1.77 | 1.02 | 31.69 (0.32%) | PASS |
| 2026 YTD through 2026-09-01 exclusive | 270 | -50.81 | 0.70 | 62.88 (0.63%) | PASS |

Aggregate executions: **1,044**.
Aggregate M15-owner clock samples: **66,408**.

Performance figures are descriptive observations only. The four windows are independent test periods and must not be converted into a continuous-equity or profitability claim.

## Deep mechanism verification

All four period summaries are **PASS**.

Across every period:
- exact Build 5.11 marker present;
- EA initialization PASS and normal deinitialization observed;
- EveryTick model confirmed;
- mismatched chart errors = 0;
- M15 owner-clock samples monotonic/aligned;
- every execution has attributable prior `M16_PASS -> PREFLIGHT_PASS -> EXEC`;
- every execution has a final `DEC_EXECUTED` state;
- bad validation/open closed-candle chronology = 0;
- duplicate executed DecisionIDs = 0;
- duplicate tickets = 0;
- zero-divide / array-out-of-range / critical-error / unresolved-stack / access-violation occurrences = 0;
- required lifecycle families were positively exercised:
  `EXT_MAT_VOID`, `EXT_MAT_SUPERSEDED`, `EXT_MAT_RETEST_READY`,
  `EXT_MAT_REVERSAL_CONFIRMED`, `RE_STATE_CANDIDATE`,
  `RE_STATE_CONFIRMED`, `MLV_FORMATION_ESTABLISHED`,
  `MLV_RETEST_COMPLETE`, `MLV_SUPERSEDED`, `MLV_VOID`.

`EXPIRED` was not required as a positive state because current Strategy-Core lifetime is structural rather than a generic fixed TTL.

## Interruption recovery

The original sequential runner was interrupted after the 2024 tester had completed but before its `RUN_END` bookkeeping line was written.

2024 was not rerun. It was salvaged and independently verified using:
- complete HTML report;
- exact sliced tester log;
- exact Build 5.11 marker;
- init/deinit proof;
- deep mechanism checks;
- current `gvariables.dat` exact-equal to its pre-run 240-byte snapshot.

The resumed runner then executed only 2025 H1, 2025 H2 and 2026 YTD. Each completed without forced termination and restored `gvariables.dat` exactly.

This satisfies the no-duplicate/reuse-valid-evidence requirement.

## Isolation

Final state after matrix:
- isolated tester terminal: **not running**;
- primary MT4 PID **13064** preserved and remained the only terminal;
- `gvariables.dat`: 240 bytes;
- final GV SHA-256: `DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6`;
- no production activation;
- no primary MT4 restart;
- no live/demo broker action.

## Evidence package

Committed small evidence:
- `blueprint/audits/evidence/FINAL_BUILD511_INTEGRATION_20260923/FINAL511_2024_summary.json`;
- `FINAL511_2025H1_summary.json`;
- `FINAL511_2025H2_summary.json`;
- `FINAL511_2026YTD_summary.json`;
- `FINAL_BUILD511_GBPUSD_MATRIX.json`;
- `LOCAL_EVIDENCE_MANIFEST.json`.

Raw HTML reports and tester logs remain on G40 and are hash-addressed by the local manifest.

Local manifest SHA-256:
`34512E3A2EE16038F912A12DAB4875AC0EF96116CB024D067FCAFC26AD06CAFD`.

Matrix canonical JSON self-hash field:
`179F62FB47DAFF28DCA89EA86C06047634096F2EDDE554181EF8694FA5AF927E`.

## Classification

**NO FIX — Strategy Core / architecture / runtime.**
No final-integration evidence justifies an EA source change.

**PASS — final integration candidate freeze.**
Build 5.11 is the exact offline/engineering final candidate for the next acceptance stage.

**VERIFICATION REQUIRED — profitability.**
The historical windows do not establish profitable expectancy; three of four descriptive windows are net negative. No strategy change or optimization is authorized by this freeze.

**VERIFICATION REQUIRED — HFM demo/live broker acceptance.**
Issue #109 remains the final separate stage and must bind to this exact frozen candidate. Demo-account evidence/authentication is required before that programme can run; no live-account execution is authorized.

## Exit

Issue #241 acceptance criteria are satisfied.

Next queue boundary: **Issue #109 — final HFM demo acceptance**, with fail-closed demo identity and no production/live activation.
