# Non-blocking F7 chronology counterfactual replay — 2026-09-06

MODE: CHAT
STATUS: RESEARCH CHECKPOINT — NO CAUSAL HARD GATE AUTHORIZED
SCOPE: F7 / NMJE same-journey child-failure chronology

## Purpose

Replay the original baseline sequence without allowing any test rule to block, replace, reorder, or otherwise contaminate the trade sequence. Freeze and observe JourneyID, child-failure count, failure type, H1 confirmation chronology, and failure freshness, then test whether a consistently bad separator survives across four periods.

## Integrity boundary

- Baseline trade sequence remained unchanged.
- No CFABL / child-fail execution gate was active in the replay source.
- Current tester-vs-baseline source difference used for this analysis was telemetry after execution only; it did not alter entry selection or sequencing.
- Local replay artifact: `C:\Users\Afiq Mat Rahim\MT4_F7_TESTER\NONBLOCKING_COUNTERFACTUAL_20260906.txt`.

## Four-period result

### Same JourneyID + child failures >= 2

- 2024: n=35, net=-10.77, PF=0.41
- 2025H1: n=22, net=-7.04, PF=0.57
- 2025H2: n=22, net=-7.99, PF=0.35
- 2026YTD: n=27, net=-17.90, PF=0.22
- Pooled: n=106, net=-43.70, PF=0.37

### Same JourneyID + child failures >= 2 + latest failure = C->X

- 2024: n=15, net=-5.14, PF=0.48
- 2025H1: n=5, net=-7.32, PF=0.00
- 2025H2: n=8, net=-4.56, PF=0.00
- 2026YTD: n=9, net=-6.98, PF=0.25
- Pooled: n=37, net=-24.00, PF=0.23

Bootstrap probability that net remains negative by period:
- 2024: 0.886
- 2025H1: 1.000
- 2025H2: 1.000
- 2026YTD: 0.946

## Failure-type / freshness findings

`>=2 + latest C->X` is the strongest chronology separator found in this replay. However, once child-failure count + failure type + freshness are split into exact semantic cells, no exact cell has >=3 or >=5 trades in every period while remaining bad across all four periods.

`C_F_X + >=2 + freshness 61-240 min` is negative across all four periods, but is materially weaker and boundary-sensitive. Nearby freshness windows can fail in 2025H1.

## Conclusion

The broad `same JourneyID + >=2 failed child attempts` cohort is consistently poor. The sharper `>=2 + latest C->X` separator also survives all four periods and currently has the strongest non-blocking evidence. Freshness is not yet proven as a stable causal component.

Do **not** implement a causal hard gate from this checkpoint.

## Next gate

Freeze the `>=2 + latest C->X` definition and run untouched holdout validation / boundary-invariance testing without sequence mutation. Only if the separator survives data not used to select the rule should a second causal ablation be considered.
