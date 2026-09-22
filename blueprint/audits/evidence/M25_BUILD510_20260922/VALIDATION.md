# M25 Build 5.10 Dashboard Build Identity Validation

Date: 2026-09-22
Issue: #235 / downstream #101 M25 dashboard materialization
Base: `d1-owner-dev@419af6f9a9fcedcef3aee0852f651aed46ba71dd` / Build 5.09
Source-bearing commit: `b2c62601a697620b66ae625d0a76b72a19df16d0`
Candidate: Build 5.10 / `V510_M25_DASHBOARD_BUILD_IDENTITY_20260922`

## Classification
**CONFIRMED OBSERVABILITY / BUILD-ATTRIBUTION BUG -> SCOPED FIX VERIFIED OFFLINE.**

Build 5.09 dashboard still rendered the historical literal `V4.5.9 P0 EXEC_ID Persistence Fix` even though the canonical EA lineage had advanced. The visible dashboard could therefore misidentify the running source.

## Smallest repair
- unique Build 5.10 identity;
- `BuildDashboardSnapshot()` renders `BBMA_BUILD_TAG` instead of a frozen historical literal;
- existing live exact-owned trade count remains unchanged;
- no dashboard feature expansion;
- no Strategy Core, NMJE, risk/MM, execution, recovery or lifecycle semantics changed.

## TDD / static / cross-module
- exact Build 5.09 baseline: RED — stale literal present and canonical build-tag render absent;
- Build 5.10 M25 static guard: PASS;
- protected Build 5.09 bodies: 30/30 exact PASS;
- N1 P1, N2 F07 open/closed bridge, F07 model/static, NMJE read-only and M12N ordering regressions PASS;
- full pytest: 22/22 PASS;
- `git diff --check`: PASS;
- production `OrderSend()` count remains one;
- N3 execution activation markers remain absent.

## Compile identity
- source/native MQ4 SHA-256: `C1ED4648FF51C6B9FEE1274FEEF1E8D08B5BA0BAD08D24523A6F0158F912A821`;
- native EX4 SHA-256: `57D6771ECE18F28D024E56A6549438082A5DA6EBAE0C970EC58F5CFCDF57B277`;
- native MetaEditor: **0 errors / 0 warnings**;
- exact three-transform tester adapter MQ4 SHA-256: `52F27ACBE61ED7ED24C3FB0591E151A1A8797CA0D1AC670109E7D268E465FA56`;
- tester adapter EX4 SHA-256: `21E4A6E9358755F78B10A5BD122BCE615A1959D996B26D3E19AF3B7CEFFE8A86`;
- tester adapter MetaEditor: **0 errors / 0 warnings**;
- dashboard tester-only target compile: **0 errors / 0 warnings**.

## Normal-path EveryTick regression
GBPUSD M15, 2026-08-01 through 2026-09-01, isolated tester.

Build 5.10 is byte-exact to VERIFIED Build 5.09 across 11 protected trace families:
- M15_COUNTS 523;
- M15_SELECT 523;
- M16_PASS 523;
- DECISION_FINAL 523;
- PREFLIGHT_PASS 325;
- EXEC 14;
- F7 MOMENTUM_HOLD 3;
- F7 EXIT_LATCHED 10;
- F7 CLOSE_SUCCESS 10;
- N2-NMJE-DEC 523;
- N2-NMJE-OUT 14.

Fatal runtime markers = 0; mismatched chart errors = 0.

## Targeted dashboard snapshot runtime
Tester-only harness adds one read-only snapshot print after the production dashboard snapshot is built.

Observed one snapshot:
`[M25-DASH-TEST] === BBMA EA V510_M25_DASHBOARD_BUILD_IDENTITY_20260922 === | Time: 2026.08.03 00:00 | Balance: 10000.00 | Equity: 10000.00 | Trades: 0 | Protection Ref: 10000.00 | ...`

Acceptance:
- snapshot count = 1;
- current BuildTag count = 1;
- stale historical literal count = 0;
- fatal runtime markers = 0;
- mismatched chart errors = 0.

## Runtime isolation
Both tester runs restored `gvariables.dat` exactly to 240 bytes, SHA-256
`DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6`.

Primary MT4 PID 13064 remained the sole terminal after validation.

## Boundary
No production activation, primary MT4 restart, live/demo broker action or live-readiness claim.
Raw tester logs remain on G40 and are identified by `RUNTIME_MANIFEST.json`.
