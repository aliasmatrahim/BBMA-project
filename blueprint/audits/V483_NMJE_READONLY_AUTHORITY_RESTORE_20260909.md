# v4.83 NMJE Read-Only Authority Restore — 2026-09-09

Status: **SOURCE FIX / STATIC PASS / NATIVE METAEDITOR 0E0W / RUNTIME NOT VERIFIED**

Refs: Issue #141 / Draft PR #142.

## Scope
- remove `NMJE_PassExecutionGate()` from executable preflight authority;
- remove `REJ_NMJE_RELATION` rejection path from `RunEntryPreflightAndExecute()`;
- preserve N1/N2 journey, decision and outcome telemetry;
- retain legacy `BlockNMJEConflict` / `BlockNMJEBuilding` inputs as explicitly inactive compatibility fields;
- no replacement NMJE filter, score or ranking;
- no D1/M15/M16, risk/MM, M17, M22 or F7 lifecycle semantic change.

## Identity
- Build: `4.83` / `Version 4.8.3 - NMJE Read-Only Authority Restore`.
- MQ4 SHA-256: `FC6DEF0B225F473DDF81E5A3B027546256C8D76D462D1F6AC9230586A556D087`.
- EX4 SHA-256: `FCA3918C371A1A272B207E07FB1D3B81C07D80BCF65AF59216CE7DE39786592B`.

## Validation
- `test_nmje_readonly_authority.py` PASS.
- targeted NMJE/N3 regression PASS.
- `git diff --check` PASS.
- native MetaEditor: `Result: 0 errors, 0 warnings, 351 msec elapsed`.

Runtime remains **NOT RUNTIME VERIFIED**. No primary MT4 restart/re-attach or production activation was performed.