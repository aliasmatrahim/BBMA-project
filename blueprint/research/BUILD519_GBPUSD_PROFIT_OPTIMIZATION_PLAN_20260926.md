# Build 5.19 GBPUSD Profitability Optimization Research

Issue: #283
Baseline: `q9-nmje-v2-build516-forward-m5-prep-101@a6b8fca43d2ba39bbd76d537500db6b016f9fbd6`
Candidate: Build 5.19 / `V519_NMJE_CURRENT_CANDIDATE_LIFECYCLE_20260926`

## Purpose

Find the highest-profit robust configuration for the exact Build 5.19 NMJE-active candidate on the already-verified GBPUSD engineering historical profile.

This is research/parameter selection only. It does not change BBMA Strategy Core, detector semantics, lifecycle authority, or the Q10 final-acceptance evidence chain.

## Historical profile

Primary pair: GBPUSD.

Reason: the Q8 engineering profile has verified M1/M5/M15/H1/H4/D1 HST identities, file integrity and cross-timeframe reconciliation.

Evidence class remains:

`ENGINEERING HISTORICAL EVIDENCE / NOT FINAL TICK-ACCURATE`

## Time split

- TRAIN: 2025-09-01 to 2026-03-01 — 6 months
- OOS: 2026-03-01 to 2026-05-01 — 2 months
- HOLDOUT: 2026-05-01 to 2026-07-01 — 2 months
- FINAL ROBUSTNESS: 2026-07-01 to 2026-09-01 — untouched 2-month check

All runs use M15 / Every Tick.

## Search order

Stage 1 — structural input sweep, FixedLot=0.01:
- EntryMode: 1, 2
- TradeLockMode: 0, 1, 2
- MaxTradePerPair: 1, 2

Stage 2 — top three Stage-1 candidates:
- MinRRRatio: 0.0, 1.0, 1.5
- MaxSLPips: 60, 80, 100, 120

Stage 3:
- top five TRAIN candidates -> OOS
- require clean runtime, no duplicate DecisionID/ticket and positive OOS result

Stage 4:
- top three OOS survivors -> HOLDOUT
- require positive HOLDOUT result

Stage 5 — sizing only after structure is frozen:
- MM_AUTO_LOT
- AutoLotPercent: 0.25, 0.5, 1.0, 1.5, 2.0
- select highest combined OOS+HOLDOUT profit subject to worst relative DD <= 10%

Stage 6:
- untouched July-August 2026 robustness run.

## Locked inputs / boundaries

- PairList=GBPUSD
- MaxActivePair=1 for single-pair research
- EnableNMJESelectionPolicy=true
- EnableNMJEForwardEvidence=true
- no source/code change to improve test results
- no new indicator/filter
- no synthetic NMJE event
- no Q10 evidence promotion from optimization results

## Winner rule

A candidate is eligible only when:
- native tester session completes;
- no targeted fatal runtime error;
- zero duplicate executed DecisionIDs;
- zero duplicate tickets;
- enough trades for the period;
- OOS and HOLDOUT are both positive.

Among eligible candidates, maximize profit. Drawdown is a hard engineering constraint, not a Strategy-Core rule.

If no candidate survives OOS/HOLDOUT, result is `NO ROBUST WINNER`; do not tune against holdout data.
