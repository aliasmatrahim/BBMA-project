# T04-B/E — HFM Demo GBPUSD weekend boundary classification

Date: 2026-11-16 MYT  
Task ID: `T04BE-HFM-WEEKEND-BOUNDARY-CLASSIFY-03`  
Requested starting checkpoint: `e7c8086af2b0488b90909a701a8c3f0c12a97c0f`  
Branch: `feat/custom-mtf-v1-20261108`  
Status: **T04-B PARTIAL/HOLD; T04-E HOLD; replay not admitted**  
Custom auto-entry: **OFF**. Trades: **none**. Merge: **not performed**.

## Exact capture identity

- Terminal profile: `91DD9F8C3ED3720A3F71FC024EC6B483`.
- File: `MQL4/Files/BBMA_HFM_GBPUSD_SESSION_1794417276.csv`.
- Server/symbol/account: `HFMarketsSV-Demo Server` / `GBPUSD` / DEMO.
- Init flag: `AUTO_TRADING_OFF`.
- Final file size: 14,824,100 bytes.
- SHA-256: `55B4573D250A1D0F4C79152A9C8B14B17F63D03BABC94F4B70E0F34B193BC9DC`.
- Rows: 244,601: INIT 1; QUOTE_SESSION 5; QUOTE_SESSION_COUNT 1; TICK 215,035; HEARTBEAT 29,559.
- Capture interval: 2026-11-11 17:14:36Z through 2026-11-15 03:23:37Z.
- Configured stop: 2026-11-16 12:00:00Z. The file stopped 32h36m23s early. Original capture terminal PID 1264 is no longer running; the currently observed terminal process is a separate MT5 process. No terminal/recorder close marker identifies why coverage ended.

## Quote-session versus observed delivery

The server/API report recorded five quote sessions: day indices 1–5, each `00:00–86400`. This is a broad Monday–Friday quote-session declaration; it is not an exact delivered-tick boundary.

| Evidence | Observed value | Classification |
|---|---|---|
| Last delivered tick | UTC 2026-11-13 21:59:58Z; server/quote label 2026-11-13 23:59:58 GMT+2; Bid 1.32103 / Ask 1.32130; connected=1 | Real terminal-observed final tick in this file |
| First heartbeat after final tick | 2026-11-13 21:59:59Z; connected=1; quote label frozen at 23:59:58 | Tick cessation did not begin with a disconnect |
| Last heartbeat | 2026-11-15 03:23:37Z; connected=1; cached quote unchanged | Recorder lived 29h23m39s after final tick |
| First post-weekend tick | Missing | Reopen not covered |
| HFM November schedule | Forex Friday to 23:58 and Monday from 00:05, GMT+2 | Trading schedule; not proof of exact quote delivery |

The official schedule and the broad quote-session API do not exactly equal the observed terminal tick boundary: the capture received a tick at 23:59:58 server label. HFM also distinguishes pre-open rate refresh from executable market hours. The file therefore proves terminal-observed quote cessation, but does not establish the exact server-wide quote policy.

## Heartbeat, connection, and coverage classification

- Heartbeats continued every 9–11 seconds across the file; UTC order is monotonic.
- There were 56 `connected=0` heartbeat rows grouped into eight short episodes:
  - 2026-11-12 09:05:57Z–09:06:17Z, reconnect by 09:06:22Z;
  - 2026-11-12 11:29:32Z–11:31:22Z, reconnect by 11:31:32Z;
  - 2026-11-12 12:15:53Z–12:17:23Z, reconnect by 12:17:31Z;
  - 2026-11-13 11:26:18Z–11:28:19Z, reconnect by 11:28:29Z;
  - 2026-11-13 13:12:22Z–13:12:42Z, reconnect by 13:12:52Z;
  - 2026-11-13 22:21:30Z–22:22:20Z, reconnect by 22:22:30Z;
  - 2026-11-14 11:23:06Z–11:24:16Z, reconnect by 11:24:26Z;
  - 2026-11-14 11:25:26Z, reconnect by 11:25:36Z.
- The first post-close disconnect begins 21m32s after the final tick. After reconnecting, ticks remain absent while heartbeat/connection resumes. This supports a market/session closure rather than a connection loss causing the final tick cutoff.
- `has_quote=1` on every row means the terminal retained a cached quote; it does not mean fresh quotes continued.
- Because coverage stops on Sunday before the expected Monday reopen, the missing first post-weekend tick is a **coverage failure**, not evidence that the server failed to reopen.
- The shutdown/termination cause of the recorder is not evidenced and is not inferred.

## Owner epoch and replay gate

The CSV contains no M08/M09 owner fields. Accepted project evidence requires the same symbol/feed/history revision, source TF/cursor, full M08 and both M09 owners (plus M12 where applicable), parent-cycle/TPW origin, and intervening accepted events.

Existing evidence does not fill that gap:

- bounded source-epoch inventory found no accepted actual M08/M09 cycle-origin checkpoint;
- the H1 origin diagnostic matched only 1/6 exact M08/M09/M12 owner states against its zero-initialized baseline;
- the H1 seed diagnostic converged in its July case, but the October pre-gap case did not reach exact M09/full-owner convergence;
- bounded natural-history restart tests prove selected contiguous engineering cases, not the 13–16 November same-feed owner epoch;
- production-admission tests prove safe refusal/freeze on an unauthenticated gap, not successful recovery.

Therefore the pre-gap owner-state prerequisite is **not proven**. The same-feed close/reopen prerequisite is also incomplete because the first post-weekend tick is absent. Per the T04-B/E gate, continuous-versus-recovery replay was not run.

## Validation disposition

No EA source changed. Native compile/regression were not rerun for this read-only evidence classification. Existing unchanged-source compile and bounded regression evidence remains reusable but does not close session/owner recovery.

Exact next action:

1. Run a recorder that remains alive through both final Friday tick and first Monday tick on the same HFM Demo server, retaining connection and coverage markers.
2. At the last valid pre-gap source candle, persist a read-only full M08/M09/M12 owner snapshot with symbol/feed/history/build/TF/cursor and lineage identity.
3. At the exact recovery-start batch, run production continuous and restart/recovery paths over the same authenticated inputs; compare every owner field and confirm stale-trigger suppression.
4. Close T04-B/E only if both prerequisites and parity pass. Until then keep all 77 custom availability cells and custom auto-entry OFF.
