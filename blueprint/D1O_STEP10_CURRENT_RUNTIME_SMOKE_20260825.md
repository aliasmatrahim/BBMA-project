# D1O Step 10 — Current D1O-07 Runtime Smoke Closure

Date: 2026-08-25
Branch: `d1-owner-dev`
Build: `Version 4.5.1 - D1O-07 Canonical LTF Dedup`
Validated source SHA-256: `adf92d9c1ac0117cbe5e75172511cce5ed5a7d4648669af522fe653c026ea492`
Validation workflow run: `32811091166`
Artifact: `d1o10-current-runtime-evidence` (artifact id `9549848838`)

Status: **RUNTIME SMOKE PASS / ATTACH_OK_NO_BROKER_DATA**

Validated gates:
- official MT4 terminal + MetaEditor acquired successfully;
- native pre-runtime compile: 0 errors / 0 warnings;
- EX4 produced successfully;
- MT4 portable terminal launched on EURUSD M15;
- `ExpertsTrades=false` for the entire smoke run;
- Journal and Experts logs were produced;
- no fatal runtime signatures detected (array out of range, zero divide, critical runtime error, access violation, stack overflow, invalid pointer, cannot load expert, expert initialization failed, init failed).

Runtime classification: `ATTACH_OK_NO_BROKER_DATA`.

The GitHub runner did not have broker-connected market data, so no `[D1-OPP]` / `[N2-NMJE-DEC]` decision telemetry was emitted. The canonical telemetry analyzer therefore correctly deferred semantic live-data validation. This is an environment limitation, not a source failure.

Remaining runtime evidence gate:
- capture broker-data D1 opportunity/decision telemetry and run `blueprint/tools/d1o_canonical_dedup_log_analyzer.py` against it;
- specifically verify same LTF execution hash remains stable across D1 attribution changes and no same-hash direction conflict occurs.
