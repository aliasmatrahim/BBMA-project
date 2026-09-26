# Build 5.19 GBPUSD Profitability Optimization Result

Date: 2026-09-27  
Issue: #283  
Draft PR: #284  
Baseline: `q9-nmje-v2-build516-forward-m5-prep-101@a6b8fca43d2ba39bbd76d537500db6b016f9fbd6`  
Candidate: Build 5.19 / `V519_NMJE_CURRENT_CANDIDATE_LIFECYCLE_20260926`

## Classification

**NO ROBUST WINNER**

This is `ENGINEERING HISTORICAL EVIDENCE / NOT FINAL TICK-ACCURATE`.

No Strategy Core rule was changed. No production authority is granted by this research.

## Data / binary identity

- Pair: GBPUSD
- Tester: M15 / Every Tick for strict validation stages
- Harness SHA-256: `22F1525B04DB37B2B5BB6594ADED4E1F2041EB87F0AE299FD8C1B33EA8FB049E`
- GBPUSD HST identities (M1/M5/M15/H1/H4/D1) matched the previously verified engineering profile before testing.

## Locked time split

- TRAIN: 2025-09-01 .. 2026-03-01
- OOS: 2026-03-01 .. 2026-05-01
- HOLDOUT: 2026-05-01 .. 2026-07-01
- ROBUST: 2026-07-01 .. 2026-09-01

The ROBUST window remained untouched until after winner selection.

## Structural screening

Structural candidate retained for strict RR/SL validation:

- EntryMode=1
- TradeLockMode=0
- MaxTradePerPair=1
- MinRRRatio=0.0

Strict TRAIN comparisons:

| MaxSLPips | Net profit | PF | Trades | DD | Runtime safety |
| ---: | ---: | ---: | ---: | ---: | --- |
| 60 | -21.77 | 0.47 | 64 | 0.25% | clean |
| 80 | -24.35 | 0.46 | 70 | 0.28% | clean |
| 100 | -25.08 | 0.45 | 73 | 0.28% | clean |

Coarse screening showed every `MinRRRatio > 0` variant produced zero trades. SL60 was retained as the least-negative strict TRAIN configuration and then tested forward through OOS/HOLDOUT.

## SL60 fixed-lot validation

- OOS: +2.28, PF 1.12, 27 trades, DD 0.20%
- HOLDOUT: +5.16, PF 1.90, 16 trades, DD 0.06%

Both windows were clean: zero targeted fatal errors, zero duplicate executed DecisionIDs, zero duplicate tickets, Build 5.19 identity present, NMJE active marker present.

## AutoLot sizing sweep

Frozen structure:

- EntryMode=1
- TradeLockMode=0
- MaxTradePerPair=1
- MinRRRatio=0.0
- MaxSLPips=60
- MMMode=1
- MaxAutoLot=1.0
- NMJE selection active

| AutoLot % | OOS profit | OOS PF | OOS DD | HOLDOUT profit | HOLDOUT PF | HOLDOUT DD | Eligibility |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 0.25 | +67.63 | 1.30 | 3.09% | -40.29 | 0.69 | 0.95% | FAIL: holdout negative |
| 0.50 | +193.27 | 1.46 | 5.92% | -28.09 | 0.87 | 1.74% | FAIL: holdout negative |
| 1.00 | +678.20 | 2.28 | 9.17% | +38.35 | 1.12 | 3.45% | PASS |
| 1.50 | +664.79 | 1.86 | 9.19% | +741.74 | 6.70 | 2.28% | PASS / selected |
| 2.00 | +288.49 | 1.30 | 10.26% | +665.60 | 3.44 | 3.15% | FAIL: DD > 10% |

Selected candidate before the final untouched robustness gate:

- AutoLotPercent=1.5
- Combined OOS+HOLDOUT profit: **+1406.53**
- Worst selection-window DD: **9.19%**
- zero targeted fatal errors
- zero duplicate executed DecisionIDs
- zero duplicate tickets

## Untouched Jul-Aug robustness

Frozen winner: AutoLotPercent=1.5.

Result:

- Net profit: **-369.57**
- Profit factor: **0.36**
- Trades: **15**
- Max / relative DD: **6.05%**
- zero targeted fatal errors
- zero duplicate executed DecisionIDs
- zero duplicate tickets
- Build 5.19 identity present
- NMJE active marker present
- tester deinit reason 0

Report SHA-256:

`9BE3E838DD46384DD555D0FDA82304DEF5A47B31F05EB6BB771977121B10639B`

## Final decision

The selected 1.5% configuration fails the pre-declared untouched robustness gate because the Jul-Aug window is negative.

Per the locked protocol, do **not** retune or fall back to another sizing candidate using the Jul-Aug result. Doing so would contaminate the untouched window and turn it into another optimization window.

Therefore:

**NO ROBUST WINNER.**

This research does not justify changing the canonical Build 5.19 production/demo settings or promoting an “optimized” risk preset.

## Evidence location on G40

`D:\BBMA\OPT_BUILD519_GBPUSD\`

Key files:

- `PRECHECK.json`
- `RECOVERED_STRUCTURAL_CHECKPOINT.json`
- `SIZING_SWEEP_SL60.json`
- `FINAL_WINNER_PCT1p5_ROBUST_ROBUST.json`
- `FINAL_OPTIMIZATION_RESULT.json`

The research tooling remains isolated from the canonical EA source.
