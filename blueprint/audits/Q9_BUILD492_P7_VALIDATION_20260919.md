# Q9 Build 4.92 P7 Validation — 2026-09-19

Status: **STATIC/MODEL/CROSS-MODULE/NATIVE COMPILE PASS + STRATEGY TESTER FUNCTIONAL REGRESSION PASS**

## Identity

- Version: `4.92`
- BuildTag: `V492_Q9_P7_STRUCTURAL_DENSITY_20260919`
- SourceRev: `Q9_P7_STRUCTURAL_DENSITY_101_20260919`
- canonical MQ4 SHA-256:
  `8EAA8CF57B003FC3E553260D2DFC52080680E6234176001650672B53FE67377E`
- exact runtime-name EX4 SHA-256:
  `72058BB9D266EFFDDCA47AA95536EF3509415229115B4D21A524EC05253FD266`

## Static / model / inherited regression

PASS:
- P7 structural-density static firewall;
- P7 structural-density/persistence model;
- P6 maturity static/model;
- P5 conflict refinement;
- P4 attribution static/persistence model;
- P2/P3 shadow;
- P1 epoch model;
- NMJE read-only authority;
- M12N orchestration order;
- D1O execution identity;
- N3 activation firewall;
- `git diff --check`.

Historical P1 current-owner static test is intentionally not part of this gate because it predates Stage-C M5 and globally forbids `PERIOD_M5`; the applicable P1 epoch regression passed.

## Protected-body comparison

P6 -> P7 exact body equality PASS for:
- `BuildPossibleCombinations`;
- `ValidateSequence`;
- `BuildConfirmedReEntryCandidate`;
- `BuildStandaloneExtremeCandidate`;
- `BuildD1OpportunityCandidate`;
- `CompareCanonicalCandidates`;
- `PriorityEngine_Atomic`;
- `InvalidationEngine_Atomic`;
- `CheckRiskBeforeTrade`;
- `RunEntryPreflightAndExecute`;
- `IsSignalAllowed`;
- `SendOrderWithRetry`.

## Native compile

Short-path exact-source compile:
`Result: 0 errors, 0 warnings, 840 msec elapsed`

Exact runtime-name compile:
`Result: 0 errors, 0 warnings, 1031 msec elapsed`

Tester-only adapter compile:
`Result: 0 errors, 0 warnings, 636 msec elapsed`

Tester adapter is local/non-canonical and changes only the already-established `IsTesting()` connection, symbol-resolution and timer environment paths.

## Strategy Tester

Pair/TF: GBPUSD M15
Window: 2026-08-01 through 2026-09-01
Model: 0
Zero-trade caps:
- `MaxTradePerPair=0`;
- `MaxTotalTrade=0`.

P7-A:
- exact `[F7-BUILD]` Build 4.92;
- 2016 tick events / 2016 bars / 3017 bar states;
- clean exit;
- 1494 `[Q9-P7-DENSITY]` observations;
- zero broker-action markers.

P7-B:
- same period/config;
- 2016 bars;
- clean exit;
- same captured log byte count as P7-A.

### Deterministic P7 A/B

After removing only the wall-clock performance summary line:
- normalized lines A: 22,156;
- normalized lines B: 22,156;
- exact equality: PASS;
- SHA-256 A/B:
  `EA44E26346C49C89D40AE4F3A09F6089AFD9933B3462D66945829E97468D0983`.

## P6 -> P7 authority regression

Verified P6-A baseline was reused; P6 was not rerun.

Exact equality:
- M15_COUNTS: 523 / 523
- M15_SELECT: 523 / 523
- M16_PASS: 523 / 523
- DECISION_FINAL: 523 / 523
- M15_CONFLICT: 0 / 0
- M16_REJECT: 0 / 0
- M16_OWNER_REJECT: 0 / 0
- D1O M15 block: 0 / 0
- D1O M16 reject: 0 / 0

Aggregate authority trace:
- P6 lines: 2,092
- P7 lines: 2,092
- exact equality: PASS
- P6/P7 SHA-256:
  `EFF894BAA8497EF6EB4A54AD43EB6354D80D61772B202E1ADBEAC430FEF2DDBF`.

Zero broker-action markers:
- P6: 0
- P7-A: 0
- P7-B: 0

## Natural P7 coverage

P7-A produced 1,494 density observations across 1,063 candidate timestamps.

Signal observations:
- RE_ENTRY: 1,058
- EXTREME: 336
- REM: 84
- RRE: 16

Existing D1 authority status was observed, not changed:
- D1Allowed=Y: 795
- D1Allowed=N: 699

Candidate-density coverage:
- 10 distinct structure masks;
- stage count range naturally included sparse through full-cycle fingerprints;
- full `ETHDRM` / mask 63 / count 6 observed 139 times;
- `ETHDR-` / mask 31 / count 5 observed 403 times.

Sole-candidate behavior was naturally exercised:
- candidate timestamps with exactly one density row: 715;
- multi-candidate timestamps: 348.

Authority regression equality proves P7 did not reject, delay or reorder those candidates.

## Environment restoration

OfflineDiag tester GlobalVariables were restored after validation.

Restored SHA-256:
`AA6F6663F81F2278953EF87147C53EA0A9FF8F7947C8BE6CAB1DC285D4F0F208`

No OfflineDiag tester terminal remained. The separate Q3 C10 terminal remained active and untouched.

## Result

**P7 Build 4.92 functional shadow scope: VERIFIED.**

P7 structural density is descriptive research metadata only. It has no candidate, M15, M16, risk or execution authority.

P2 deterministic ordering remains HOLD/UNRESOLVED.

Do not claim live-terminal/`OnTimer` verification from this Strategy Tester result. Live timer follow-up remains deferred to Monday.

No merge / no production activation.
