# Re-Entry Outer-BB Value / Profit-Protection Counterfactual

Date: 2026-09-29
Issue: #289
Branch: `research/reentry-outerbb-value-289`
Baseline owner: `d1-owner-dev@459c0588e625d7f7630f0fb5612b7f04fda496de`
Classification: **ENGINEERING COUNTERFACTUAL / NOT BBMA CORE / NO EXECUTION AUTHORITY**

## 1. Question

Test whether the directional outer Bollinger Band has measurable value as a Re-Entry profit-protection reference without promoting it to a mandatory TP, partial-close rule, TP1/TP2/TP3, or new Strategy-Core authority.

Production EA source, C044 lifecycle authority, risk, selection and execution are unchanged.

## 2. Source / governance boundary

The accepted Core supports the recurring Re-Entry -> Momentum/CSM -> further Re-Entry lifecycle and treats the directional outer BB as structural context rather than a universal mandatory resting broker TP.

The 2026-09-04 F7 decision explicitly enables targetless Re-Entry lifecycle management and does not authorize partial close, TP2 or TP3. Therefore every realization tested here is shadow/counterfactual only.

## 3. Evidence baseline

Primary historical evidence is the previously verified Q8 Build 4.86 GBPUSD engineering profile:
- periods: 2024, 2025 H1, 2025 H2, 2026 YTD through 2026-09-01 exclusive;
- Q8 executions: 1,045 total; this study includes only C044-managed H1/H4 Re-Entry owners;
- included study cohort: 519 trades = 481 H1 standalone Re-Entry + 38 H4/REM;
- report/log identities are checked against the committed Q8 evidence manifest;
- GBPUSD M1/H1/H4 HST SHA-256 identities are checked against the verified Q8 hashes.

Historical classification remains **ENGINEERING HISTORICAL EVIDENCE / NOT FINAL TICK-ACCURATE**.

The simple displayed-price P&L reconstruction differs from the MT4 report by at most USD 0.07 per included trade. Baseline P&L therefore uses the MT4 report directly; reconstructed prices are used only for counterfactual reference calculations.

## 4. Counterfactual definitions

**Frozen outer BB**: BB(20,2) on the exact source-owner Re-Entry confirmation candle. The first later M1 structural reach is treated as the hypothetical realization coordinate. This can be known at entry, but it risks cutting a later valid Momentum continuation.

**Dynamic closed-candle outer BB**: first fully post-entry owner-TF candle whose range touches its own directional outer BB. The hypothetical action is evaluated only after that candle closes, using its close price. This avoids current-candle look-ahead.

**Dynamic no-Momentum reference (preferred research form)**: same dynamic event, but hypothetical realization is suppressed when that exact owner-TF candle emits canonical same-direction `MOMENTUM_HOLD`. This keeps valid Momentum continuation untouched.

For SELL, structural BB levels are Bid-chart references; hypothetical execution uses the fixed Q8 Strategy Tester spread of 20 points. For 25/50/75% realization, the un-realized remainder retains the exact baseline lifecycle close result.

## 5. Aggregate result
| Cohort | Trades | Dynamic events | No-Momentum events | Baseline P&L | Unconditional dynamic 25% delta | Dynamic no-Momentum 25% delta | Dynamic no-Momentum 100% delta |
|---|---:|---:|---:|---:|---:|---:|---:|
| H1 standalone RE | 481 | 147 | 85 | -18.11 | -2.94 | **+4.67** | +18.66 |
| H4 / REM | 38 | 11 | 10 | -44.32 | +3.52 | **+3.18** | +12.72 |

Unconditional outer-BB realization is not supported for H1. It reduces aggregate H1 outcome and therefore should not replace the current lifecycle.

The no-Momentum condition changes the result materially. In H1, 85 no-Momentum outer-BB events split 56 better / 29 worse than the eventual baseline close. The summed event outcome improves by 18.66 if 100% were realized, but a 25% realization improves the full H1 cohort by only 4.67.

For H4/REM, only 10 no-Momentum outer-BB events exist. Seven improve and three worsen versus baseline. This is directionally positive but underpowered.

## 6. Period stability — preferred no-Momentum reference

| Cohort / period | Trades | No-Momentum events | 25% delta | 100% delta |
|---|---:|---:|---:|---:|
| H1 2024 | 188 | 31 | **-3.76** | -15.02 |
| H1 2025 H1 | 87 | 17 | +3.57 | +14.29 |
| H1 2025 H2 | 84 | 17 | +2.60 | +10.39 |
| H1 2026 YTD | 122 | 20 | +2.25 | +9.00 |
| H4 2024 | 19 | 4 | +1.28 | +5.13 |
| H4 2025 H1 | 4 | 2 | +2.03 | +8.12 |
| H4 2025 H2 | 6 | 2 | **-0.20** | -0.78 |
| H4 2026 YTD | 9 | 2 | +0.06 | +0.25 |

H1 therefore fails a strict all-period consistency gate because 2024 is negative. H4 also fails an all-period gate because 2025 H2 is negative and the cohort is very small.

A descriptive event-level normal-approximation check also does not justify promotion:
- H1 no-Momentum event delta: n=85, mean +0.2195, median +0.45, approximate 95% interval -0.1915 to +0.6306;
- H4 no-Momentum event delta: n=10, mean +1.2720, median +0.725, approximate 95% interval +0.1419 to +2.4021, but n=10 is too small for strong inference.

## 7. What the result means

### ENGINEERING IMPROVEMENT — outer BB as observer/reference

**ISSUE:** The outer BB contains useful lifecycle information, particularly when an owner-TF candle reaches it without producing same-direction Momentum.

**IMPACT:** A read-only observer can quantify protected profit, give-back and continuation opportunity without changing C044 authority.

**FIX:** No production execution fix. Retain outer BB only as research/telemetry reference unless later independent evidence closes robustness.

### NO FIX — unconditional H1 outer-BB realization

**ISSUE:** Blind realization at H1 outer BB cuts valid continuation.

**IMPACT:** Aggregate H1 outcome is worse for both frozen and unconditional dynamic references.

**FIX:** Do not add a universal H1 outer-BB TP or unconditional partial close.

### VERIFICATION REQUIRED — conditional H1 profit protection
**ISSUE:** Dynamic outer-BB reach without same-candle Momentum improves H1 aggregate in this Q8 sample.

**IMPACT:** A 25% hypothetical realization changes H1 aggregate by +4.67, but 2024 is -3.76 while the three later periods are positive. Event-level uncertainty still spans zero.

**FIX:** Keep research-only. Do not promote to execution until broader pair/build/OOS evidence is positive without retuning.

### VERIFICATION REQUIRED — H4/REM outer-BB value

**ISSUE:** H4/REM frozen and conditional references look more favorable than H1.

**IMPACT:** The full cohort is only 38 trades and only 10 conditional no-Momentum events; one period is negative.

**FIX:** Expand H4/REM evidence before any policy decision. No partial-close authority is created.

## 8. Regression / architecture conclusion

No EA source was modified. No detector, candidate, confirmation, selection, validation, risk, execution or trade-lifecycle owner changed. No broker order or partial close was generated by this study.

The analyzer is read-only and consumes already-verified historical report/log/HST evidence. Python syntax validation and `git diff --check` pass. This study does not require or constitute a native MQL4 compile because the canonical MQ4 is unchanged.

## 9. Final classification

**NO NEW EXECUTABLE TP RULE.**

Outer BB is supported as a useful **value / profit-protection observation reference**. The strongest research form is:

`closed owner-TF outer-BB reach + no same-candle canonical Momentum -> observe hypothetical protection value; Momentum present -> preserve continuation`.

This remains **ENGINEERING RESEARCH / VERIFICATION REQUIRED**, not BBMA Core and not production authority.

Artifacts:
- analyzer: `blueprint/tools/reentry_outerbb_value_counterfactual.py`;
- compact result: `blueprint/research/evidence/ISSUE289_OUTERBB_VALUE_SUMMARY.json`;
- full per-trade rows remain local at `D:\BBMA\OUTERBB_VALUE_289\OUTERBB_VALUE_TRADE_ROWS.json`.
