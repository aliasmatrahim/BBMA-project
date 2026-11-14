# T04-B/E same-feed reopen watch — 2026-11-15

Task ID: `T04BE-HFM-REOPEN-OWNER-RECOVERY-WATCH-02`  
Status: **IN PROGRESS / HOLD / NOT VERIFIED**  
Branch: `feat/custom-mtf-v1-20261108`  
Parent feature checkpoint: `7aa0c7ccb92e4931f20b763bb9466d8ed29094ca`  
Live owner branch: `d1-owner-dev` at `7567af7dfbfaafff35a37c1d307b387e96273c78`  
PR: [#303](https://github.com/aliasmatrahim/BBMA-project/pull/303), Draft/open/unmerged; GitHub reports `mergeable=false`.

## Same-feed observation

Read-only G40 capture: `C:\Users\Afiq Mat Rahim\AppData\Roaming\MetaQuotes\Terminal\91DD9F8C3ED3720A3F71FC024EC6B483\MQL4\Files\BBMA_HFM_GBPUSD_SESSION_1794417276.csv`.

- Feed identity remains `HFMarketsSV-Demo Server` / `GBPUSD`; this is test-feed evidence, not confirmation of the unresolved primary deployment profile.
- Last captured `TICK`: UTC epoch `1794607198` = **2026-11-13 21:59:58Z**; the captured server and quote labels are frozen at `1794614398`.
- Latest inspected `HEARTBEAT`: UTC epoch `1794692226` = **2026-11-14 21:37:06Z**. It still reports `connected=1`, cached quote present, Bid `1.32103`, Ask `1.32130`, and unchanged server/quote labels. Elapsed time from last tick: **23h37m08s**.
- A read-only G40 watcher is running as PID `10872`, started at `2026-11-14T21:31:54Z`. It tails only newly appended rows and will stop after the first `TICK` later than baseline `1794607198` (or after 24 hours). It does not submit orders or modify AutoTrading.
- At the latest check, the watcher had produced no post-gap tick row. The weekend reopen and the exact quote-delivery boundary are therefore **not yet observed**.

## Owner/recovery status

The capture records quote/session labels only; it does not record the M08/M09 owner state at the first recovery observation. Existing HFM archive and seed probes remain diagnostic: they did not establish an independently source-proven full pre-gap owner epoch. No continuous-versus-recovered production owner parity run is admitted until the same-feed boundary and valid owner checkpoint/reconstruction are bound.

## Validation and gates

No EA source or executable test artifact changed in this checkpoint. Compile/regression were not rerun; reuse only the unchanged-source evidence in `T06_M15_AUTHORITY_VALIDATION_20261114.json`: strict compile 0 errors/0 warnings; T05/T06 harness 16/16; clock 14/14; observer 4/4; scheduler replay 12/12. That bounded replay is not weekend/session or owner-epoch acceptance.

T04-B/E and overall T06 remain HOLD. All 77 signal×TF availability cells and custom auto-entry remain OFF. No merge, deployment, or trading activation.

## Exact next action

When the watcher records the first post-weekend `TICK`, preserve its raw row and UTC/server labels. At the exact recovery-start batch, capture the read-only M08/M09 owner state with symbol/feed/history/build identity, source timeframe and cursor, owner fields and parent-cycle/TPW lineage. Then compare uninterrupted replay with restart/recovery replay over the same authenticated feed boundary and verify full owner-field parity plus stale-trigger suppression. Close T04-B/E only if those criteria pass; otherwise keep the owner unavailable and continue fail-closed.
