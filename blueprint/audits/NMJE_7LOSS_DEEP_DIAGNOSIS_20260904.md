# NMJE 7-Loss Deep Diagnosis — 2026-09-04

Status: READ-ONLY DIAGNOSIS / NO EA SOURCE CHANGE
Build: BBMA_EA_V459_NMJE_FORWARD / v4.59
Active MT4 data folder re-verified: 50CA3DFB510CC5A8F28B48D1BF2A5702
Evidence: active MQL4 log + terminal log only; legacy C10/Strategy Tester excluded.

## Result
All 7 genuine forward outcomes closed by broker stop-loss. They were all `SIGNAL_RE_ENTRY` trades.

Relation distribution: ALIGNED 2/2 loss, BUILDING 2/2 loss, CONFLICT 3/3 loss.
Authority distribution: STRAT 2/2 loss; OPP 5/5 loss.

## Finding 1 — NMJE is observation-only, not an execution gate
Source explicitly defines nested relation states as observation-only. A `CONFLICT` label does not reject a trade. Therefore 3 trades executed despite confirmed H1 Re-Entry opposing the parent direction. This is not evidence that NMJE classified incorrectly; it is an intentional current policy limitation.

Candidate next action: keep source frozen for now; use forward evidence to decide whether CONFLICT/BUILDING should become an execution filter or risk modifier. This would be a strategy-policy change, not a bug fix.

## Finding 2 — Initial SL geometry can be extremely tight
M17 uses the source-owned Re-Entry lifecycle structural high/low and only one `Point` beyond the anchor. BUY adds no spread buffer by design; SELL adds a rounded minimum 2-pip spread buffer.

Observed initial risk distances:
- EURAUD SELL ALIGNED: ~7.2 pips; TP ~6.7 pips; RR ~0.93; stopped after ~2m48s.
- CADJPY SELL CONFLICT #1622728534: ~8.7 pips; TP ~23.4 pips; RR ~2.69; stopped after ~2h25m.
- AUDJPY SELL CONFLICT: ~11.6 pips; TP ~14.7 pips; RR ~1.27; stopped after ~2h08m.
- EURGBP BUY BUILDING: ~1.1 pips; TP ~10.7 pips; RR ~9.73; stopped after ~10m36s.
- CADJPY SELL CONFLICT #1622756094: ~5.5 pips; TP ~6.4 pips; RR ~1.16; stopped after ~22m21s.
- GBPUSD BUY ALIGNED: ~3.4 pips; TP ~15.6 pips; RR ~4.59; stopped after ~1m57s.
- GBPJPY SELL BUILDING: ~7.1 pips; TP ~24.8 pips; RR ~3.49; stopped after ~38m25s.

The EURGBP and GBPUSD losses are especially consistent with normal price noise defeating a very close structural stop before the intended move can develop. This is a profitability/runtime-design risk, not yet a proven coding defect.

## Finding 3 — Minimum RR protection is disabled
`MinRRRatio` defaults to 0.0, so low-RR trades are not rejected. EURAUD executed below 1:1 and the later CADJPY trade was only ~1.16:1. This does not explain all seven losses but weakens expectancy protection.

## Finding 4 — The common denominator is Re-Entry execution
All seven outcomes are `SIGNAL_RE_ENTRY`; labels and authority modes vary. Therefore current evidence points more strongly to Re-Entry timing/SL geometry than to one NMJE relation label alone. The two ALIGNED strategic-owner trades also lost, so simply blocking CONFLICT would not have prevented the full loss streak.

## Finding 5 — Execution log timestamp is unreliable
`[P3M2][EXEC]` prints `OrderOpenTime()` without selecting the newly opened ticket first. Runtime lines show stale OrderOpen values (for example a newly opened trade can report an earlier 09:30 value). Broker terminal log confirms the real open times. This is an observability defect only and is not the cause of the losses.

## Conclusion
No evidence currently proves NMJE classification is wrong. The strongest actionable hypotheses are: (1) NMJE CONFLICT/BUILDING is not yet used to gate execution, and (2) Re-Entry structural stops can be too tight for live noise, especially BUY cases. A third issue is disabled minimum RR protection. Do not patch frozen source until these hypotheses are tested against more forward outcomes or an explicitly approved strategy-policy experiment.
