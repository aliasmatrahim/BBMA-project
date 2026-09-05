# F7 Strategy Tester Evidence — 2026-09-05

Scope: GBPUSD, M15 Strategy Tester, multi-TF BBMA logic on M15/H1/H4/D1. `H2` in notes means half-year, not timeframe H2.

## Baseline / OOS
- Full 2024-01-01 to 2026-08-31 Model2 baseline: net -82.78, PF 0.83, max DD 1.29%, 867 trades.
- 2025 H1 selected training setup: net +70.12, PF 1.77, 174 trades.
- 2025 H2 Every-Tick OOS: net -19.22, PF 0.68, 133 trades.
- 2026 YTD Open-price OOS: net -41.67, PF 0.69, 216 trades.
- Conclusion: low drawdown but no stable cross-regime edge.

## F7 targetless attribution
- 2025 H2 Every-Tick F7 targetless: 57 trades, net -6.52, PF 0.77, 25 SL, 32 lifecycle closes.
- All 25 F7 SL trades were SIGNAL_RE_ENTRY and NMJE ALIGNED.
- Therefore ALIGNED alone does not remove the losing cohort.

## Post-SL direction audit
- Across 2024, 2025 H1, 2025 H2 and 2026 YTD: 174 F7 SL trades.
- 172/174 (98.9%) later moved back in the original trade direction within 12h.
- 150/174 (86.2%) reached at least +1R from the original entry within 12h.
- 104/174 (59.8%) reached at least +2R within 12h.
- This supports a timing/placement problem, not proof that every direction is correct.
## Entry timing / adverse excursion
- Among SL trades that later recovered >=1R, median adverse excursion was ~14-16 pips and ~1.75-1.82R.
- 75th percentile adverse excursion was ~24-26 pips / ~3.2-3.4R.
- Median reversal-point delay was ~30 minutes; 75th percentile ~105 minutes.
- Widening structural SL alone did not solve profitability: +3 pip buffer modestly improved 2025 H2 but remained negative; wider buffers degraded again.

## Re-Entry type attribution
Pooled mapped F7 cohorts:
- Type 1: 129 trades, net -9.54, PF 0.88; 67 SL, 57 recovered >=1R within 12h.
- Type 3 CSM: 150 trades, net +0.85, PF 1.01; 62 SL, 57 recovered >=1R within 12h.
- Type 4 CSD: 82 trades, net -26.06, PF 0.62; 44 SL, 36 recovered >=1R within 12h.
- Type 2 was enabled but produced no mapped F7 executions in the four samples; Type 3/4 precedence can take ownership first.

## Causal ablations
- Type4 OFF on 2024 worsened F7 from about -42.16 / PF 0.56 to -62.70 / PF 0.48.
- Type1+Type4 OFF on 2024 improved loss to -26.17 / PF 0.60 but remained negative; therefore failed holdout and was not promoted.
- Post-hoc type filtering is not trustworthy because disabling a type changes later ownership/trade sequence.

## Causal timing gate
Tester-only rule: after H1 Re-Entry confirmation, require at least one closed M15 adverse candle followed by a closed M15 favorable candle before F7 execution.
- 2024 result: F7 113 trades, net -38.06, PF 0.55, 51 SL.
- Baseline comparison: F7 about 134 trades, net -42.16, PF 0.56.
- Loss reduced slightly, but PF did not improve and edge remained negative. Candidate failed holdout and was not promoted.
## Pre-entry M15 feature audit
Simple pre-entry features were compared without future data: adverse/favorable candle counts, latest M15 candle direction, and adverse->favorable turn sequence.
- 2025 H1: adverse->favorable turn cohort was strong (PF 2.20).
- 2025 H2: same cohort was near break-even (PF 1.04).
- 2024: same cohort remained negative (PF 0.62).
- 2026 YTD: same cohort remained negative (PF 0.77).
- No simple pre-entry M15 timing feature was stable across all regimes.

## Current interpretation
- Profitable F7 trades clearly exist; the problem is unstable expectancy across regimes, not absence of winners.
- Direction selection is often eventually correct after an SL, but that does not by itself create a tradable timing rule.
- Current evidence does not justify a production change to RE Type ownership, SL width, NMJE relation gate, or a fixed timing delay.
- Tester-only experimental changes were restored. Neutral tester adapter compiles 0 errors / 0 warnings.
- Production/live EA was not modified by these experiments.

## Future improvement boundary
Use this document as negative/positive evidence to avoid repeating failed searches. New timing or entry changes must be causal, closed-candle, BBMA-native, and validated out-of-sample before production promotion.
## BBMA-native maturity investigation
Tester-only candidate: require same-direction M15 Extreme lifecycle at least `EXT_MAT_REVERSAL_CONFIRMED` before F7 Re-Entry execution.
- 2024 holdout: 22 F7 trades, +8.55, PF 1.64.
- 2025 H1: 10 trades, +40.86, PF 6.86.
- 2025 H2 Every-Tick: 13 trades, +0.28, PF 1.05.
- 2026 YTD: 15 trades, -8.92, PF 0.14.
This is the strongest timing improvement found so far, but it fails 2026 and is not production-safe.

Stricter `EXT_MAT_RETEST_READY` was too restrictive: 2024 had 16 F7 trades, -1.38, PF 0.84.
A D1 closed-body alignment gate looked strong retrospectively but failed causally: 2024 +15.82/PF2.27; 2025H1 +42.25/PF7.66; 2025H2 -0.32/PF0.96; 2026 -12.18/PF0.18.

## Clean 2026 subtype diagnosis
A dedicated clean 2026 rerun/log segment removed DecisionID contamination from previous tester reruns.
- RE Type1: 8 targetless trades, net -4.70; 2 winners / 6 losers.
- RE Type4 CSD: 3 trades, net -1.75; 0 winners / 3 losers.
- RE Type3 CSM: 1 trade, net +0.06; 1 winner.
- Other targetless lifecycle identities: 5 trades, net -4.96.
Parent context alone did not cleanly separate winners from losers; failures occurred under both H4 owner and H4 Re-Entry contexts.

Causal subtype filters failed 2024 holdout:
- EXTREV + block Type4: 24 F7 trades, -2.22, PF 0.85.
- EXTREV + Type3 only: 9 F7 trades, -2.73, PF 0.58.
Therefore subtype filtering is stopped; further search here would be overfit-prone.

## Pre-Extreme cycle-progression diagnosis
A telemetry-only rerun recorded the M15 Extreme RAW candle and reversal-confirmation candle before F7 execution across 2024, 2025 H1, 2025 H2 Every-Tick, and 2026 YTD.

Key findings:
- Immediate RAW -> reversal confirmation (15 minutes) was not a universal solution: 2024 +4.84/PF1.48; 2025H1 +2.58/PF1.46; 2025H2 +1.55/PF1.36; 2026 -3.03/PF0.20 for mapped standard H1 Re-Entry trades.
- Longer RAW -> confirmation lags also did not provide a stable separator; 30-minute pooled PF was 0.24, while 45/60-minute groups were sparse and regime-dependent.
- Pre-RAW NMJE parent, D1/H4 ownership, H1 Re-Entry, M15 MHV, and existing Extreme-state combinations repeatedly changed sign between periods. No repeated pre-RAW context separated winners from losers across all regimes.
- Therefore neither an immediate-reversal rule nor a pre-RAW parent/state filter is justified for production.

Causal boundary:
- M15 Extreme reversal-confirmed remains the strongest timing lead found, but 2026 regime failure is not explained by RAW->confirmation speed, H4 owner/Re-Entry parent, D1 body alignment, or Re-Entry subtype alone.
- Further historical gate search is stopped here to avoid combinatorial overfitting. New production changes require new independent/runtime evidence or a BBMA-native causal mechanism not selected from these same four periods.
- Tester-only provenance instrumentation was removed after diagnosis; neutral tester adapter recompiles 0 errors / 0 warnings. Production EA remains unchanged.