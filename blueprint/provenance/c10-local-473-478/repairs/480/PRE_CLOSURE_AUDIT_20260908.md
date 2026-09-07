# Build 4.80 C10 pre-closure audit — 2026-09-08

Status: **READY FOR FINAL LIVE PHYSICAL-RESTART EVIDENCE / ISSUES #122 AND #123 REMAIN OPEN**.

## Governance boundary
- Canonical implementation owner remains `d1-owner-dev`; this repair branch does not replace it.
- Build 4.80 is Draft PR #130 stacked on Build 4.79 / Draft PR #129.
- C10 remains shadow/research only: `Authority=NONE`.
- Validation launch is isolated with `ExpertsTrades=false`, `MaxTradePerPair=0`, `MaxTotalTrade=0`, `InstanceID=80`.
- No Strategy Core, risk, sizing, M15 authority, M22 execution authority, D1TPW/C044 gate or NMJE execution semantics are changed by this closure work.

## Exact identity
- Build 4.80 source SHA-256: `E9C8CFBE574786BE22003D76F015E5438E9D2EEFD8BF11E377DD93FE61BAE0E1`.
- Embedded C10 SourceHash: `5C672778E35AA2602702824778F8F7F6EE4BCDCDFB99B7E32679A17CC0DA2DC6`.
- Compiled EX4 SHA-256: `98A6A7C58E33190152E4309A12C6C3FEFC5DFEAC7BF6921208692E9E05A9B40F`.
- Live launch INI SHA-256: `7318CA442DEECC06DAEFEFE8A9D55029AC270457AD544D4F57F05BAFAE7EB58C`.
- Instance-80 SET SHA-256: `C30B361DC9D336CC53E5D2F232E15DEE09AE75927754CCEC5E023CF50844F128`.
- Native MetaEditor evidence remains `0 errors / 0 warnings / 498 ms`.

## Fresh regression rerun
- `C10_122_STATIC_AUTHORITY=PASS`.
- `C10_122_LAGGED_M5_MODEL=PASS`.
- `C10_122_PREENTRY_REPLAY_MODEL=PASS`.
- `C10_122_MISSING_HISTORY_FAILCLOSED_MODEL=PASS`.
- `C10_122_CORRUPT_HISTORY_FAILCLOSED_MODEL=PASS`.
- `C10_122_CHECKPOINT_INTEGRITY_STATIC=PASS`.
- `C10_122_SOURCE_IDENTITY_480=PASS`.
- `C10_123_STATIC_AUTHORITY=PASS`.
- `C10_123_WRITER_NAMESPACE=PASS`.
- `C10_123_REPORTER_GLOB_COMPAT=PASS`.
- `C10_123_READY_OWNER_DIAGNOSTIC=PASS`.
- reporter provenance-domain dedupe model: `PASS cases=11`.
- source-file SHA / embedded hash / stale-build-literal guards: PASS.

## 4.79 -> 4.80 regression review
Exact EA-source diff was reviewed from Build 4.79 commit `68d608a...` to Build 4.80 materialization commit `1631db6...`.

Observed semantic delta is restricted to:
- build/version/source identity;
- deterministic `C10_LedgerOwnerToken()`;
- owner token in daily signal/outcome filenames;
- owner token in `[C10][READY]` diagnostics;
- outcome-rebuild glob restricted to the current owner namespace;
- matching BuildID literals in signal/checkpoint/outcome rows and validation.

The Issue #122 chronology functions remain intact through the 4.80 stack. No new detector, candidate, validation, risk or broker-execution authority was introduced.

## Hardened final verifier
`verify_runtime_closure.py` now independently validates the final evidence bundle rather than trusting a marker-only PASS.

Required checks:
1. pre-restart and post-restart checkpoints contain the exact same ACTIVE DecisionID and frozen identity fields;
2. BuildID, C10 SourceHash and ConfigFingerprint are exact across checkpoint and C10 ledgers;
3. M5 enrollment anchor is derivable from `EntryTime` and is not older than the proven prior-M5 boundary;
4. launch config proves `ExpertsTrades=false`; parameter set proves InstanceID=80 and zero trade caps;
5. all signal/outcome CSV rows have exact schema width;
6. duplicate EventID/OutcomeEventID is checked across all files within each provenance domain, not only within one file;
7. the target DecisionID cannot produce more than one outcome and cannot produce an outcome before enrollment;
8. post-restart log must contain `[C10][SHADOW_RECOVERY] Active=1` and exact-config `[C10][READY] ... Authority=NONE`;
9. post-restart segment must contain no `LEDGER_DISABLED`, `OrderSend`, `OrderClose`, `OrderModify`, `OrderDelete` or `DEC_EXECUTED`.

Verifier self-tests:
- clean synthetic fixture based on authentic 4.80 checkpoint/ledger data: PASS;
- injected duplicate EventID: correctly FAIL;
- injected `OrderSend`: correctly FAIL.

## Acceptance matrix before final live restart
### Issue #122 — timeline provenance
- deterministic lagged-M5 reproduction/regression: PASS;
- no pre-enrollment candle accepted by model/static guard: PASS;
- unprovable M5 enrollment becomes per-shadow UNKNOWN rather than invalid ACTIVE/global disable: PASS in live/isolated observations;
- missing or timestamp-corrupt M5 enrollment/replay history fails closed in the extended deterministic #122 regression; checkpoint checksum/schema corruption is rejected by the existing integrity guard: PASS;
- native MetaEditor 0E0W: PASS;
- Authority=NONE / zero broker actions in existing runtime evidence: PASS;
- **fresh live ACTIVE -> physical restart -> exact recovery/replay:** PENDING.

### Issue #123 — concurrent writer ownership
- deterministic writer namespace/static regression: PASS;
- Build 4.74 + 4.80 concurrent owner-separated ledger evidence: PASS;
- no malformed/interleaved rows in observed concurrent ledgers: PASS;
- no same-provenance duplicate EventID/OutcomeEventID in observed ledgers: PASS;
- checkpoint ownership remains instance/config bound: PASS;
- native MetaEditor 0E0W: PASS;
- **restart test reaches exact live ACTIVE recovery path with final hardened verifier PASS:** PENDING.

## Closure rule
Do not close #122 or #123, merge PR #129/#130, promote Build 4.80, or modify `d1-owner-dev` merely because the pre-closure checks are green.

Final closure evidence must be generated by the isolated broker-connected Build 4.80 terminal at the live clock:
`fresh ACTIVE -> physical process stop -> same terminal restart -> exact ACTIVE recovery -> hardened verifier PASS`.

Until that occurs, status remains **VERIFICATION REQUIRED / NOT FULLY RUNTIME VERIFIED**.

## Exact live harness retained
The currently used same-terminal restart harness is retained as `live_physical_restart_automation_20260908.ps1` on the Draft PR branch. It snapshots the launch INI/SET, freezes and captures the fresh ACTIVE checkpoint, stops only the isolated terminal executable, measures the pre-restart log boundary, restarts without an 8-second blind window, captures the post-restart segment, then delegates the acceptance decision to `verify_runtime_closure.py`.

Harness hardening after review: post-restart acceptance no longer treats the pre-existing checkpoint file alone as proof of recovery. It now waits for all three conditions: exact ACTIVE identity still present, a new post-boundary `[C10][SHADOW_RECOVERY] Active=1` marker, and the exact-config `[C10][READY] ... Authority=NONE` marker before proceeding to the final verifier. PowerShell parser and synthetic recovery/READY regex checks PASS.
