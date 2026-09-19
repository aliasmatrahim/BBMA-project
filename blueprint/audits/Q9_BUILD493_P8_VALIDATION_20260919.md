# Q9 Build 4.93 P8 Validation — 2026-09-19

Status: **STATIC/MODEL/CROSS-MODULE/NATIVE COMPILE PASS + STRATEGY TESTER FUNCTIONAL REGRESSION PASS**

## Identity

- Version: `4.93`
- BuildTag: `V493_Q9_P8_PROVENANCE_STABILITY_20260919`
- SourceRev: `Q9_P8_PROVENANCE_STABILITY_101_20260919`
- canonical MQ4 SHA-256:
  `C041423D53E0425D3070BB5F1C1BB8DC083A0DF65874CC848C1A30040E55E17E`
- exact runtime-name EX4 SHA-256:
  `CF9C02B041CC409F651F496F04E35A96D68523DE1D8AC4F0FFAC3BC6F1CACE2A`

## Static / model / inherited regression

PASS:
- P8 provenance-stability static;
- P8 provenance-stability model;
- P7 structural-density static/model;
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

## Protected-body comparison

P7 -> corrected P8 exact body equality PASS for:
- M13/M14 combination/candidate construction;
- canonical comparator;
- M15 PriorityEngine;
- M16 invalidation;
- risk;
- preflight;
- `IsSignalAllowed`;
- broker execution.

## Native compile

Short-path exact-source compile:
`0 errors, 0 warnings, 960 msec`

Exact runtime-name compile:
`0 errors, 0 warnings, 948 msec`

Tester-only adapter compile:
`0 errors, 0 warnings, 894 msec`

Tester adapter:
- canonical MQ4 SHA `C041423D53E0425D3070BB5F1C1BB8DC083A0DF65874CC848C1A30040E55E17E`;
- tester MQ4 SHA `FB1FDBF07FF776755A292652212AF79E7F01EAEC13294AAB0DA24CB0947EF41E`;
- tester EX4 SHA `5FBE0659E0B408DEA8C1F42B6D6F50561C3DAF201B3AAAA67960F94052B602A6`;
- adapter diff firewall PASS.

## Strategy Tester main deterministic regression

Pair/TF: GBPUSD M15
Window: 2026-08-01 through 2026-09-01
Inputs include:
- `MaxTradePerPair=0`;
- `MaxTotalTrade=0`;
- `MaxActivePair=1`;
- `InstanceID=93`.

P8-A and P8-B:
- each 2016 tick events / 2016 bars / 3017 bar states;
- clean deinit;
- zero broker-action markers.

After dropping only the wall-clock performance summary line:
- P8-A normalized lines: 24,172;
- P8-B normalized lines: 24,172;
- exact equality: PASS;
- A/B SHA-256:
  `C4562C5F5EE70EFD541A4C2BE24D65AECE72EFD3B7825D1B6B59DB41073D40DF`.

## P7 -> P8 authority regression

Exact equality:
- M15_COUNTS: 523 / 523
- M15_SELECT: 523 / 523
- M16_PASS: 523 / 523
- DECISION_FINAL: 523 / 523
- conflict/reject/D1O block families: 0 / 0 where absent in baseline.

Aggregate authority trace:
- P7: 2,092 lines;
- P8: 2,092 lines;
- exact equality: PASS;
- SHA-256 both:
  `EFF894BAA8497EF6EB4A54AD43EB6354D80D61772B202E1ADBEAC430FEF2DDBF`.

Raw N1 regression after stripping only P8-added observer tokens:
- P7: 2,016;
- P8: 2,016;
- exact equality: PASS;
- SHA-256 both:
  `B4843C86443C8C98830E10527CC05BC372715881F35A257A9E58FC29DD4C3952`.

## Natural P8 parent-transition coverage — August

P8 stability rows: 2,016.

Observed:
- parent transitions: 28;
- transition rows missing previous-parent identity: 0;
- non-transition rows incorrectly carrying previous-parent identity: 0.

The August sample is evidence of deterministic canonical parent transition tracking.

## Natural identity-hysteresis coverage — January

Targeted natural GBPUSD M15 January 2026 probe:
- 2016 bars;
- zero broker-action markers;
- `HOLD_LAST_PROVEN_RELATION`: 122 observations;
- raw relation != stable relation: 122 observations;
- parent transitions: 26.

Examples include raw `BUILDING` while last-proven stable relation remains `ALIGNED`, `SUPPORTING` or `CONFLICT` under the same immutable parent journey until new attributable canonical evidence arrives.

This proves P8 hysteresis executes naturally without adding a bar/timer threshold.

## M5 coverage

Current tested windows did not naturally provide stable confirmed/reversal-confirmed M5 context. M5 last-proven carry-forward remains static/model verified only.

Classification: **VERIFICATION REQUIRED for natural M5 stable-event coverage only**.

This does not authorize synthetic M5 context and does not block the base parent/child P8 exit gate.

## Environment restoration

OfflineDiag GlobalVariables restored after validation.

Restored SHA-256:
`AA6F6663F81F2278953EF87147C53EA0A9FF8F7947C8BE6CAB1DC285D4F0F208`.

No OfflineDiag tester terminal remains. Q3 isolated Build 4.81 terminal remains active and untouched. Q6 native archive downloader remains a separate long-running workstream.

## Result

**P8 Build 4.93 functional shadow scope: VERIFIED.**

P8 stable relation/provenance is observer metadata only. It does not create, reject, rank, delay, validate, risk-approve or execute a trade.

P2 deterministic active ordering remains HOLD/UNRESOLVED.

No merge / no production activation.
