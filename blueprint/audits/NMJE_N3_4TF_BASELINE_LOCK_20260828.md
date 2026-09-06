# NMJE N3 4-TF Baseline Lock — 2026-08-28

## Locked lineage

- PR: #97 `nmje-n3-hardening-dev` -> `d1-owner-dev`
- Materialized source commit: `0609ef6dfc2da09f2a97c19f84517a38eae79b0b`
- Reconciled base: `1052f3ce1399082bf6ce73e82b67f8551a6d0329`
- EA identifier: `Version 4.6.0 - N3 D1 Owner Epoch Provenance Fix`
- MQL property: `4.60`

## Locked topology and authority

The clean N3 baseline is exactly:

`D1 -> H4 -> H1 -> M15`

- D1 remains the strategic owner.
- H4 remains higher-owner / journey context.
- H1 remains setup context.
- M15 remains the sole processing and final decision clock.
- M15/M16 remain final entry/revalidation authorities.
- M22 remains the sole OrderSend owner.
- NMJE relations remain deterministic diagnostic/shadow provenance.
- M5 is not part of this baseline and must be developed only in the isolated Issue #101 workstream.

## D1 owner epoch invariant

- `SourceCandleTime` remains the latest closed-D1 snapshot.
- `EpochStartCandleTime` changes only when canonical owner State/Direction changes.
- `NMJE_D1OwnerEventID` derives identity from `EpochStartCandleTime`.
- Ordinary closed-D1 refreshes cannot rotate the canonical owner identity.
- Replay/recovery remains fail-closed.

## Verification evidence

Local verification against the materialized source:

- D1 owner epoch materializer selftest: PASS
- N3 policy readiness: PASS
- N3 replay identity: PASS
- N3 recovery fail-closed: PASS
- N3 authority matrix: PASS
- N3 identity-domain separation: PASS
- Python `py_compile`: PASS
- NMJE N3 static guard: PASS
- Native MT4 MetaEditor: `Result: 0 errors, 0 warnings, 1677 msec elapsed`
- Compiler: `C:\Program Files (x86)\InstaTrader\metaeditor.exe`

The first `metaeditor64.exe` attempt was an MT5 compiler mismatch and is not source evidence. GitHub Actions runs and one retry terminated with `steps=null` / `logs_url=null`; those remain runner-availability anomalies, not source failures.

## Safety lock

- PR #97 remains DRAFT / NO MERGE.
- NMJE execution authority remains disabled.
- `EnableD1TPWLifecycle=false`.
- `EnableC044Lifecycle=false`.
- No D1TPW, C044, M5, M30, M1, or W1 activation is authorized by this lock.
- Any rule that can reduce eligible trade count, delay an otherwise executable M15 decision, or change strategy authority requires a separate explicit strategy-policy approval and attributable evidence.

## Next isolated workstream

Issue #101 may proceed on a separate branch only. Initial work is contract, lineage schema, shadow metadata, deterministic tests, and sequencing. No M5 source integration or activation belongs in PR #97.
