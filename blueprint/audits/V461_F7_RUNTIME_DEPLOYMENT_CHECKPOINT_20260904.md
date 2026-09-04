# v4.61 F7 Runtime Deployment Checkpoint

Date: 2026-09-04
Branch: `d1-owner-dev`
Build: `BBMA_EA_v461_F7`
Status: **DEPLOYED / INITIAL ATTACH PASS / F7 EVENT + RECOVERY EVIDENCE PENDING**

## Verified runtime identity
- MT4 executable: `C:\Program Files (x86)\MetaTrader 4\terminal.exe`
- Active Data Folder: `C:\Users\Afiq Mat Rahim\AppData\Roaming\MetaQuotes\Terminal\50CA3DFB510CC5A8F28B48D1BF2A5702`
- Terminal log: `logs\20260904.log`
- Expert log: `MQL4\Logs\20260904.log`
- Terminal build: 1479
- Demo broker connection observed through active terminal TCP session.

## Deployment
- v4.61 compile artifact copied into active `MQL4\Experts` as `BBMA_EA_v461_F7`.
- Active default profile chart changed from `BBMA_EA_V459_NMJE_FORWARD` to `BBMA_EA_v461_F7` after backup.
- Terminal log confirms `Expert BBMA_EA_v461_F7 GBPUSD,M15: loaded successfully`.

## Current validation boundary
- Native MetaEditor compile for v4.61: **0 errors / 0 warnings**.
- Initial live attach identity: PASS.
- F7 lifecycle event traces are not yet available because no new source-backed targetless F7 trade has been observed after deployment.
- Restart/recovery is **not claimed PASS** merely from absence of errors; current Expert-log buffering did not expose sufficient recovery trace detail.
- Pre-existing v4.59 broker order `1622803124` had broker-side SL/TP before restart and is not treated as proof of v4.61 targetless F7 lifecycle.

## Evidence still required
1. New v4.61 targetless F7 execution with structural SL and broker TP=0.
2. Same-direction owner-TF CSM -> WAIT_NEXT_REENTRY trace.
3. Later owner-TF Re-Entry -> MOMENTUM_PENDING re-arm trace.
4. Reverse-confirmation or opposite CSM -> latched close trace.
5. Opposite reversal-confirmed owner-TF Extreme -> cycle-supersession close trace when encountered.
6. Controlled restart with an open F7 position proving checkpoint load/replay/fail-frozen behavior and close idempotency.

No source change is authorized by this checkpoint.