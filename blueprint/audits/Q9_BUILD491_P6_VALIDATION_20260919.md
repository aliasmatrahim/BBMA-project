# Q9 Build 4.91 P6 Validation — 2026-09-19

Status: **STATIC/CROSS-MODULE/NATIVE COMPILE PASS — NOT RUNTIME VERIFIED**

## Exact identity

- Version: `4.91`
- BuildTag: `V491_Q9_P6_MATURITY_FINGERPRINT_20260919`
- SourceRev: `Q9_P6_MATURITY_FINGERPRINT_101_20260919`
- Git source blob before commit: `3818e4befd3a71981d6aeca33c86f19192cea7d6`
- MQ4 SHA-256: `B9AB1289153DD3505E1B96C1970F30435A4819A2EDC3C8ED6E7E4E23140102E4`
- exact runtime-name EX4 SHA-256: `DBC4BA11AB2FE507E55B49283CD0D0A44F7434BB8710027D4EA7673B94377FDC`
- EX4 size: 619134 bytes

## Static / model / regression

PASS:
- Q9 P6 maturity static firewall
- Q9 P6 maturity persistence/model
- P5 conflict refinement
- P4 attribution static
- P4 persistence model
- P2/P3 shadow
- P1 epoch model
- NMJE read-only authority
- M12N orchestration order
- D1O execution identity
- N3 policy-readiness activation firewall
- protected authority function-body comparison vs P5
- `git diff --check`

## Cross-module authority

Protected function bodies are unchanged from P5:
- combination construction;
- canonical comparator;
- M15 priority;
- M16 invalidation;
- risk;
- preflight;
- signal-allowed;
- broker send/retry.

No P6 maturity symbol occurs in those authority bodies.

Order primitive counts remain 1/3/0/0 for Send/Close/Modify/Delete.

## Native compile

Exact runtime deployment filename:
`D:\BBMA\MT4_NMJE_141_Demo\MQL4\Experts\BBMA_EA_Q9_491_P6.mq4`

MetaEditor:
`Result: 0 errors, 0 warnings, 1141 msec elapsed`

The deployed MQ4 hash equals the worktree source hash.

## Runtime

Profile: `Q9_491_P6_READONLY`
- EURUSD M15
- ExpertsTrades=false
- MaxTradePerPair=0
- MaxTotalTrade=0
- InstanceID=91

Two bounded attempts both reached:
- terminal start;
- Expert `BBMA_EA_Q9_491_P6` loaded;
- zero-trade inputs logged.

Neither attempt reached broker login / attributable OnInit completion / `[F7-BUILD]` / NMJE observer logs. Both therefore fail the P6 runtime exit criterion.

Classification: **VERIFICATION REQUIRED / RUNTIME-ENVIRONMENT BLOCKED**.

No natural P6 maturity transition was observed and no synthetic signal was created.

## Result

P6 code is compile-ready and statically authority-safe, but **P6 is not yet VERIFIED as a runtime checkpoint**. Do not advance to P7 from this state.
