# M19 Build 5.00 validation — 2026-09-21

Issue: #218  
PR: #219  
Base checkpoint: PR #217 / Build 4.99 head `2c963917e498c10f71cef7998fc62223571084ce`  
Validated head: `147155750260568f30cb5197650994e32e479fa6`

## Source and compile

- canonical MQ4 SHA-256: `524B9860692755AD9AF69F956E12B794C4629DBDF914BCE15503D09D79161CFB`
- native MetaEditor: **0 errors / 0 warnings**
- native EX4 SHA-256: `E7AAD92946CABD1FE32EEA15D602940DDA36852B52F6EB83D8A4C7A2245D9255`
- tester adapter MQ4 SHA-256: `9F28BBD26E77F5274F413788D7FB01992C44ACBF912C9BB525C7F9198E6DAF83`
- tester adapter MetaEditor: **0 errors / 0 warnings**
- tester adapter EX4 SHA-256: `61DAB52389198657047CEA0DD064ED894FF90FDB0E304CA2260FC78C5EF7BEC7`

## Deterministic tests

- M19 ownership model: **PASS**
- M19 source/static guard: **PASS**
- M17 broker-distance model: **PASS**
- legacy M17 static identity test is not a M19 gate because it intentionally requires the prior 4.99 identity.

## GBPUSD M15 Every-Tick smoke

Scope: 2026-08-01 through 2026-09-01, spread 20, isolated tester terminal.

- report generated: **yes**
- report SHA-256: `500D732F2DDB2ED1E6AA4AA4230505BFA64E2A8A7B6D6A19A64320E886AB6206`
- tester log delta SHA-256: `053ED4C918ED38ACB69631AA33B0278B7CC700C5BA10EAA1A8F7FEC1884AC518`
- M19 identity present in runtime log: **yes**
- build tag present: **yes**
- DECISION_FINAL: **523**
- EXEC: **14**
- fatal runtime scan: **0**
- Global Variables pre/post restore SHA-256: `DD8320C5529D41EB90F55290CBF3D5AAFE74F7A30964A647AF075DDFD7BA91A6`
- Global Variables bytes: **240 → 240**

## Protected comparison against Build 4.99 smoke

All exact-equal:

- M15_COUNTS: 523 / 523
- M15_SELECT: 523 / 523
- M16_PASS: 523 / 523
- DECISION_FINAL: 523 / 523
- PREFLIGHT_PASS: 325 / 325
- EXEC: 14 / 14
- MOMENTUM_HOLD: 3 / 3
- EXIT_LATCHED: 10 / 10
- CLOSE_SUCCESS: 10 / 10

## Boundary

This is source/native/tester/runtime verified in an isolated engineering smoke only. No merge, primary MT4 restart, production activation, live-broker acceptance, or profitability claim.
