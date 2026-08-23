# P3-M2-11 — Mode 2 Diagnostic / Runtime Readiness

Date: 2026-08-23  
Branch: `blueprint-dev`  
Canonical build: **P3-M2-11.1 Mode2 Diagnostic Closure**  
Status: **STATIC READY / NATIVE METAEDITOR 0E0W PENDING / LIVE RUNTIME EVIDENCE KIV**

## Purpose
Prepare a deterministic runtime evidence path for Mode 2 without changing BBMA Strategy-Core eligibility. This patch is diagnostic-only on top of the source-resolved P3-M2-07B.2 lifecycle implementation.

## Strategy boundary
No Mode-2 entry family, source signature, priority rule, SL/TP rule, risk rule, or live-position exit rule is changed by M2-11.

Mode 2 remains executable only for:
- standalone H1 `SIGNAL_RE_ENTRY` under its accepted H4 directional owner;
- `SIGNAL_REM`;
- `SIGNAL_RRE`;
- `SIGNAL_REE`.

Opposite eligible Mode-2 candidates in the same decision pool remain fail-closed. Scoring remains metadata-only.

## Trace matrix

| Runtime question | Canonical trace |
|---|---|
| New reversal-confirmed opposite Extreme supersedes old source-TF Extreme | `[P3M2][EXT_SUPERSEDE]` |
| F1 MHV/MLV sees opposite-cycle RAW Extreme candidate | `[P3M2][MLV_SUPER_CAND]` |
| F1 MHV/MLV cycle is superseded after reversal confirmation | `[P3M2][MLV_SUPERSEDE]` |
| Eligible Mode-2 BUY/SELL counts at M15 | `[P3M2][M15_COUNTS]` |
| Opposite candidate conflict / no winner | `[P3M2][M15_CONFLICT]` |
| Canonical Mode-2 selection | `[P3M2][M15_SELECT]` |
| M16 conflict rejection | `[P3M2][M16_REJECT]` |
| M16 exact-owner/freshness rejection | `[P3M2][M16_OWNER_REJECT]` |
| M16 validation pass | `[P3M2][M16_PASS]` |
| Execution preflight starts | `[P3M2][PREFLIGHT_START]` |
| SL/TP + lot + risk/portfolio preflight passes | `[P3M2][PREFLIGHT_PASS]` |
| Broker execution succeeds | `[P3M2][EXEC]` |
| Final state/rejection after the complete decision path | `[P3M2][DECISION_FINAL]` |

## Required runtime scenarios after market/data availability

1. **Standalone RE path**
   - prove H1 Re-Entry is admitted only with a valid/recovered same-direction H4 owner;
   - trace `M15_SELECT -> M16_PASS -> PREFLIGHT -> EXEC` or a deterministic rejection.

2. **REM path**
   - prove exact H4 RE + H1 Extreme + M15 MHV/MLV identity;
   - prove M16 exact-owner validation and source-owned M17 SL/TP.

3. **RRE path**
   - prove exact D1 RE + H4 RE + H1 Extreme identity and direction consistency.

4. **REE path**
   - prove exact D1 RE + H4 Extreme + H1 Extreme identity and direction consistency.

5. **Opposite candidate conflict**
   - if Mode-2 BUY and SELL candidates coexist in one frozen M15 decision pool, prove `[M15_CONFLICT]` and no execution.

6. **M08 opposite Extreme supersession**
   - prove RAW opposite Extreme alone does not produce `[EXT_SUPERSEDE]`;
   - prove a newer reversal-confirmed opposite Extreme supersedes the old Extreme before combination construction.

7. **F1 MHV/MLV cycle supersession**
   - prove `[MLV_SUPER_CAND]` occurs at RAW candidate stage without immediate MLV supersession;
   - prove `[MLV_SUPERSEDE]` only after the later accepted reversal confirmation.

8. **Stale-owner rejection**
   - prove a decision/component whose exact M08/M09 owner has been voided/superseded cannot pass M16.

9. **Live-order separation**
   - prove Extreme/cycle supersession itself never emits a forced `OrderClose()`;
   - an older live position continues under approved broker SL/TP/M23/M20 lifecycle while Strategy-Core may progress to a new cycle.

10. **Multiple same-direction entry / risk overlay**
    - a distinct valid later same-direction setup may proceed only if duplicate, portfolio and risk gates pass;
    - no relative setup-score comparison is introduced.

## Static readiness result

PASS:
- trace points cover detector/cycle transition, M15 selection/conflict, M16 owner validation, preflight and successful execution;
- `[DECISION_FINAL]` provides the final lifecycle state/rejection for any created Mode-2 decision, avoiding strategy changes merely to increase logging;
- all trace statements are conditional on `EntryMode == 2`;
- traces do not affect candidate eligibility, direction, SL/TP, lot, risk, portfolio or OrderSend inputs;
- P3-M2-07B.2 F1 boundary remains intact;
- no forced close is introduced.

## Remaining hard gates

1. **Native MetaEditor compile of this exact canonical build:** `0 errors / 0 warnings`.
2. Runtime evidence scenarios above when market/data execution is available.

Earlier compile evidence cannot be reused because the source changed for P3-M2-07B and M2-11 diagnostics.
