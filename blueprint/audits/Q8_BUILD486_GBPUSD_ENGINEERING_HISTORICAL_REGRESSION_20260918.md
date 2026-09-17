# Q8 Build 4.86 GBPUSD Engineering Historical Regression — 2026-09-18

Status: **VERIFIED / COMPLETE FOR SCOPED Q8 ENGINEERING HISTORICAL REGRESSION**
Evidence class: **ENGINEERING HISTORICAL EVIDENCE / NOT FINAL TICK-ACCURATE**
Issue: **#188**
Pair: **GBPUSD only**

## Scope and authority

This audit validates mechanism/runtime behaviour of the Q7-frozen Build 4.86 lineage on the already-verified GBPUSD engineering historical profile. It does not authorize production/live activation, parameter optimization, a new Strategy-Core rule, or a final tick-accurate claim.

Canonical candidate identity was freshly reverified before the remaining runs:
- owner lineage: `d1-owner-dev@3fdd918151f99f1b57db8929efbe39e07f61a697`;
- BuildTag: `V486_STRUCTURAL_LIFETIME_20260917`;
- SourceRev: `Q5_STRUCTURAL_LIFETIME_173_20260917`;
- canonical MQ4 SHA-256: `D737A25FD01D6BA879118479401B5E7969DF20F528E53E43515852C555DD3308`;
- frozen canonical EX4 SHA-256: `6A7116B26CDB7BA87B8CCC3415D2309BF414C32D274A66B4903D6E47FC93A5C6`.

No canonical EA/Core/contract source was modified by Q8.

## Tester adapter boundary

The exact frozen EX4 was first exercised in the offline isolated tester and failed closed during initialization because that environment exposed no selectable broker symbol through the production `SymbolsTotal(false)` path. This was classified as a tester-environment limitation, not a Strategy-Core mismatch.

A Q8-only harness was therefore derived from the exact Build 4.86 MQ4 with three tester-only environment guards:
1. during `IsTesting()`, permit the current tester `Symbol()` to satisfy exact/suffix-normalized symbol resolution;
2. during `IsTesting()`, treat terminal connectivity as available to the historical simulator;
3. during `IsTesting()`, skip unsupported `EventSetTimer()` registration while preserving `OnTick` as the processing driver.

The invariant verifier proves the harness equals the exact base plus only those three transforms. No detector, confirmation, selection, validation, risk, SL/TP, execution, lifecycle, NMJE or combination rule was changed.

Harness MQ4 SHA-256: `E0FDE68F1EFE082F032785CAABA4DFE603FC53B6FB89323A583296E43432BBC4`.
Harness EX4 SHA-256: `FFD0F34121B75C15F42009FE83F01BE69F005FA464D49FAB7715F0007D27EE7A`.
Native MetaEditor compile: **0 errors / 0 warnings**.

This harness is test evidence only and is not a deployable replacement Build 4.86 binary.

## Historical-data identity

Before continuation, all six installed GBPUSD HST files were freshly hashed against the existing isolated-v3 install manifest and passed:
`M1`, `M5`, `M15`, `H1`, `H4`, `D1` = **PASS**.

The complete file-level hashes are retained in `blueprint/audits/evidence/Q8_BUILD486_GBPUSD_20260918/local_evidence_manifest.json` and the local G40 source package. This profile remains an engineering mapping; native Dukascopy archive/provenance and deployment broker-time mapping remain separate final-authority gates under Issue #128.

## Regression matrix

| Period | Trades | Net profit | Profit factor | Max DD | Mechanism acceptance |
|---|---:|---:|---:|---:|---|
| 2024 | 396 | -47.47 | 0.79 | 75.89 (0.76%) | PASS |
| 2025 H1 | 206 | -23.14 | 0.86 | 56.63 (0.57%) | PASS |
| 2025 H2 | 173 | +1.77 | 1.02 | 31.69 (0.32%) | PASS |
| 2026 YTD through 2026-09-01 exclusive | 270 | -50.81 | 0.70 | 62.88 (0.63%) | PASS |

The smoke window `2026-08` also passed before the wider matrix. Performance figures are descriptive observations only. The four runs are independent tester windows and must not be combined into a continuous-equity profitability claim.

## Deep mechanism verification

Fresh deep verifier result: **PASS for all four matrix periods**.

Across the matrix:
- executions: `1045`;
- M15 owner-clock samples: `66408`, monotonic and aligned to the M15 processing cadence;
- every execution had a matching prior `M16_PASS -> PREFLIGHT_PASS -> EXEC` sequence;
- every execution had a matching final `DEC_EXECUTED` state;
- bad ValidateCandle/OrderOpen closed-candle chronology: `0`;
- duplicate executed DecisionIDs: `0`;
- duplicate tickets: `0`;
- fatal runtime occurrences for zero-divide, array-out-of-range, critical error, unresolved stack function and access violation: `0`.

Every matrix period positively exercised the required lifecycle families: `EXT_MAT_VOID`, `EXT_MAT_SUPERSEDED`, `EXT_MAT_RETEST_READY`, `EXT_MAT_REVERSAL_CONFIRMED`, `RE_STATE_CANDIDATE`, `RE_STATE_CONFIRMED`, `MLV_FORMATION_ESTABLISHED`, `MLV_RETEST_COMPLETE`, `MLV_SUPERSEDED`, and `MLV_VOID`.

`EXPIRED` observations were `0` in all four periods and were not treated as a required positive state because this Build 4.86 lineage uses structural lifetime authority rather than an arbitrary Strategy-Core TTL.

## Classification and closure

**NO FIX — Strategy/Core/architecture:** no Q8 evidence requires a canonical EA change.
**NO FIX — duplicate/order safety:** no duplicate executed decision or ticket was observed.
**NO FIX — runtime stability:** no targeted fatal runtime fault was observed.
**VERIFICATION REQUIRED — final tick authority:** Q8 does not close the native Dukascopy/deployment-time provenance gates under Issue #128.
**VERIFICATION REQUIRED — final broker/demo acceptance:** remains Q10 / Issue #109 and must use the exact final deployable candidate.

Q8 scoped exit criteria are therefore satisfied for **GBPUSD engineering historical regression only**. This is mechanism evidence, not a profitability endorsement and not production readiness.

## Evidence package

Committed small evidence package:
- `blueprint/audits/evidence/Q8_BUILD486_GBPUSD_20260918/matrix_deep.json`;
- four period summary JSON files;
- `local_evidence_manifest.json` containing SHA-256 references to the retained G40 reports, raw tester logs, HST files, exact candidate bytes and harness bytes.

Local evidence-manifest SHA-256: `110442FDE33D618498578889E3DDC482BE20E9ACFB0EEBA6BA888BA869C48AF8`.
Deep-matrix SHA-256: `5940383CF49226861802CF040FED3EEC981FFAABE16B8D934D79AE30F70FDB25`.

Q3 Build 4.81 isolated watcher/runtime was not restarted or modified by this work.
