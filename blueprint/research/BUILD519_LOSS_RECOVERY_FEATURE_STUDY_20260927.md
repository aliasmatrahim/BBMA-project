# Build 5.19 — Loss-Exit Recovery Feature Study

Issue: #287  
Classification: **ENGINEERING HYPOTHESIS / HOLD — NOT STRATEGY CORE / NOT EXECUTABLE AUTHORITY**

## Question

Among Build 5.19 GBPUSD losing lifecycle exits, what observable-at-exit features distinguish trades that return to original entry before original SL from trades that hit original SL first?

No canonical EA/Core change was made.

## Discovery population — Mar to Aug 2026

Population:
- 25 losing lifecycle exits
- 19 recovered to original entry before original SL within 24h
- 6 hit original SL first

All 25 execution records were `SIGNAL_RE_ENTRY`; signal type therefore did not separate the groups.

C044 exit reason was only weakly descriptive:
- `C044_EXIT_CYCLE_SUPERSEDED`: 5/6 recovered (83.3%)
- `C044_EXIT_FAILED_MOMENTUM`: 14/19 recovered (73.7%)

## Strongest descriptive differences

### 1. Fraction of SL already consumed at lifecycle exit

`sl_used_frac = adverse excursion at exit / original SL distance`

- recover median: **14.2%**
- SL-first median: **42.4%**
- pairwise separation score: **0.754**

Direction was stable across all three temporal blocks:
- Mar-Apr: recover lower
- May-Jun: recover lower
- Jul-Aug: recover lower

### 2. Remaining absolute distance to original SL

- recover median: **30.8 pips**
- SL-first median: **12.15 pips**
- separation score: **0.544**

Direction was also stable across all three blocks.

### 3. M15 BBMA context at the latest valid closed candle before exit

Recover trades were generally less adverse relative to BBMA M15 structure:
- M15 close vs BB mid, direction-normalized: recover median **-3.28 pips**, SL-first **-7.93 pips**
- M15 close vs directional MA10: recover median **+1.37 pips**, SL-first **-6.21 pips**
- M15 close vs directional MA5: recover median **+2.18 pips**, SL-first **-2.59 pips**

The sign/direction of these differences was consistent in Mar-Apr, May-Jun and Jul-Aug, but group overlap remained material.

## No deterministic separator

No single predeclared feature perfectly separated the 19 recover trades from the 6 SL-first trades.

A notable false-positive was 2026-04-27:
- SL used only 18.5%
- remaining SL buffer only 14.5 pips
- M15 MA5/MA10 context still favorable
- outcome nevertheless = SL first

This is why a percentage-only delay gate is unsafe.

## In-sample selective-delay exploration

Engineering gate:

`sl_used_frac <= 0.25 AND remaining_sl_pips >= 20`

Mar-Aug discovery result:
- selected: 10/25
- recovered: 10
- SL-first: 0
- apparent recovery precision: 100%
- loss-subset counterfactual improvement: **+152.71**

By temporal block:
- Mar-Apr: +50.55
- May-Jun: +44.73
- Jul-Aug: +57.43

This result is in-sample and cannot authorize implementation.

## Frozen-gate temporal check — Sep 2025 to Feb 2026

A fresh strict Build 5.19 Every-Tick run was executed with:
- GBPUSD
- EntryMode=1
- AutoLotPercent=1.5
- MaxSLPips=60
- MinRRRatio=0
- NMJE selection ACTIVE
- same frozen gate; no threshold retuning

Tester result:
- 59 total trades
- net: -1108.05
- PF: 0.52
- DD: 15.84%
- zero targeted fatal runtime errors
- zero duplicate DecisionIDs/tickets
- Build 5.19 + NMJE ACTIVE identity confirmed

Losing exits:
- 31 total
- gate selected 9
- 8 recovered before SL
- 1 hit SL first
- recovery rate among selected: 88.9%

Counterfactual effect on loss subset:
- actual losses: **-1490.16**
- selective-delay counterfactual: **-1462.51**
- overall delta: **+27.65**

But temporal stability failed:
- Sep-Nov: **-51.40 worse**
- Dec-Feb: **+79.05 better**

## Decision

**HOLD / NO EXECUTABLE RULE.**

The study supports a real descriptive relationship: loss exits that still have substantial SL room and have consumed only a small portion of the original SL distance are more likely to recover.

However, the frozen gate did not remain positive in every temporal segment. One selected failure was enough to reverse the benefit in Sep-Nov.

Therefore:
- do not delay C044 exits in production;
- do not convert the 25% / 20-pip gate into Strategy Core or Risk/Execution authority;
- do not retune the threshold against the failed Sep-Nov sample;
- preserve the gate only as a research hypothesis.

## Next safe research

The next evidence-expansion step should be **multi-pair / multi-period counterfactual validation** using the same frozen feature definitions, without threshold retuning.

A candidate may advance only if recovery precision and P/L benefit remain stable across independently selected pairs/periods and the downside tail from false positives remains bounded.
