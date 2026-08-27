# R1 Runtime Log Full Review — 2026-08-27

Status: ATTRIBUTED SESSION REVIEW / NO R1 D1TPW CASE PROMOTED  
Scope: authenticated HFM demo runtime evidence only  
Input artifact: operator-supplied `20260827.log`  
Artifact SHA-256: `6bcf07c0e07cae48e44561af6f22ba07eabdec1d2f4d862c69f703ee736bf9eb`

## 1. Session configuration observed

The R1 test EA `BBMA_EA_V459_R1_D1TPW` loaded at approximately `11:01:48`.

Observed input checkpoints:

- `11:01:50`: EntryMode=2, MinRRRatio=0.0, DebugLevel=0, StrategyID=1, InstanceID=0, AutoLotPercent=1.0, MaxSLPips=100.0.
- `11:11:02`: same profile with DebugLevel=4.
- `18:36:49`: AutoLotPercent changed to 0.1; MinRRRatio remained 0.0; DebugLevel remained 4.
- `19:26:03`: MaxSLPips changed to 500.0; AutoLotPercent remained 0.1; MinRRRatio remained 0.0; DebugLevel remained 4.

These input changes are recorded for attribution. They do not by themselves prove or disprove D1TPW lifecycle behavior.

## 2. D1TPW scan result

For the `BBMA_EA_V459_R1_D1TPW` lines in the supplied log:

- `[M17-SL][STRUCT]` records observed: 50.
- `D1TPW=Y` records observed: 0.
- `D1TPW=N` records observed: 50.
- exact `D1_OPP_EXTREME_TPW` records observed: 0.
- exact `EXTREME_TPW` records observed: 0.
- `[D1-TPW]` records observed: 0.
- D1 opportunity families observed in `[D1-OPP]`: `NONE` and `MOM_RE` only.

Therefore the supplied log contains no attributable D1 Extreme TP-Wajib targetless lifecycle activation. This is an absence-of-occurrence finding for this log, not evidence that the R1 binary gate is globally OFF.

## 3. Attributable broker executions after R1 activation

Three `[P3M2][EXEC]` records are present under the R1 EA name.

### 3.1 AUDCAD ticket 484792192

- Signal: `SIGNAL_RE_ENTRY`
- Direction: `DIR_BUY`
- Validate candle: `2026.08.27 15:30`
- M17 source TF: M15 (`TF=15`)
- Final SL: `0.99601`
- TP: `0.99735`
- `C044=N`
- `D1TPW=N`
- Lot: `0.16`
- Ticket: `484792192`
- Broker open: `0.99676`
- Execution hash: `CB9A8014BBF8C16E`
- Broker comment: `BBMA|H:CB9A8014BBF8C16E`
- `[P3S5][EXEC_ID]`: `Persist=PASS Local=Y BrokerHashFound=Y BrokerHashMatch=Y`
- Final state: `DEC_EXECUTED / REJ_NONE`

Classification: ordinary attributable RE execution; not R1-01 and not R1-04..R1-09.

### 3.2 GBPAUD ticket 484809344

- Signal: `SIGNAL_RE_ENTRY`
- Direction: `DIR_SELL`
- Validate candle: `2026.08.27 16:00`
- M17 source TF: H1 (`TF=60`)
- Structural anchor: `1.89092`
- Final broker SL: `1.89123`
- TP: `1.88855`
- `C044=N`
- `D1TPW=N`
- Lot: `0.08`
- Ticket: `484809344`
- Broker open: `1.88984`
- Execution hash: `58221C9B37F940EC`
- Broker comment: `BBMA|H:58221C9B37F940EC`
- `[P3S5][EXEC_ID]`: `Persist=PASS Local=Y BrokerHashFound=Y BrokerHashMatch=Y`
- Final state: `DEC_EXECUTED / REJ_NONE`
- Later `[N2-NMJE-OUT]`: `NET=7.49000000`, `REC=REC_NORMAL`.

Classification: ordinary attributable RE execution that later closed normally; not R1-01 and not an R1 D1TPW completion case.

### 3.3 AUDJPY ticket 484818688

- Signal: `SIGNAL_RE_ENTRY`
- Direction: `DIR_BUY`
- Validate candle: `2026.08.27 17:00`
- M17 source TF: H1 (`TF=60`)
- Structural anchor: `114.467`
- Final broker SL: `114.466`
- TP: `114.639`
- `C044=N`
- `D1TPW=N`
- Lot: `0.09`
- Ticket: `484818688`
- Broker open: `114.625`
- Execution hash: `9AFDF374F4043F71`
- Broker comment: `BBMA|H:9AFDF374F4043F71`
- `[P3S5][EXEC_ID]`: `Persist=PASS Local=Y BrokerHashFound=Y BrokerHashMatch=Y`
- Final state: `DEC_EXECUTED / REJ_NONE`

Classification: ordinary attributable RE execution; not R1-01 and not an R1 D1TPW completion case.

## 4. Runtime-health finding

All three attributable post-activation executions show execution-identity persistence PASS with local persistence and broker-hash match. This is useful continuity evidence for P0 execution identity but does not replace the R1 D1TPW acceptance matrix.

## 5. R1 disposition

No mandatory R1 case is promoted to PASS from this full-log review.

In particular:

- R1-01 targetless initial payload remains INCOMPLETE because no `D1TPW=Y` / `TP=0.0` execution is present.
- R1-04..R1-09 remain INCOMPLETE because no attributable D1TPW lifecycle completion event is present.
- R1-02/R1-03/R1-10..R1-16 are not satisfied by these ordinary RE executions.

The correct next runtime evidence is a naturally occurring D1 Opportunity Extreme TP-Wajib decision whose M17 record shows `D1TPW=Y`, `C044=N`, and `TP=0.0`, followed by the relevant D1TPW lifecycle/recovery/completion evidence.

## 6. Safety boundary

This review changes documentation only on the isolated branch `r1-runtime-log-review-20260827`. It does not modify `blueprint/source/BBMA_EA.mq4`, the running R1 EA, the running Observer, canonical lifecycle gates, or trading authority.
