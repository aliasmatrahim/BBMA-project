# F05 Build 5.06 validation

Date: 2026-09-22 UTC
Issue: #226 / downstream Issue #101 F05
Baseline: `d1-owner-dev@2e524cdfe8829da774698cb96c8fc848518250d3` / Build 5.05
Candidate: Build 5.06 / `V506_F05_SELECTION_UNCERTAINTY_FAIL_CLOSED_20260922`
Source revision: `F05_SELECTION_UNCERTAINTY_FAIL_CLOSED_226_20260922`

## Scope
F05 only: distinguish monitored-order broker selection uncertainty from proven exclusion.
No Strategy-Core change, no TradeLock mode change, no universal opposite-direction guard, no M19 total-risk/F01 rewrite, no M21/F07/M24/broker-send change.

## Confirmed baseline defect
Build 5.05 mapped monitored-ticket `OrderSelect()` failure to boolean false.
Source-bound fault injection reproduced:
- basket observation 1.3% -> 0.0% on selection failure;
- M20 observed one actual monitored live row as zero and could admit a second trade at `MaxTotalTrade=1`;
- TradeLock mode 1 opposite and mode 2 second-entry checks could fail open;
- M19 selection could succeed earlier in the same attempt while later M20/TradeLock selection failed.

## Implementation
- one canonical tri-state ownership observation: UNKNOWN / EXCLUDED / LIVE_OWNED;
- broker ticket-selection failure -> UNKNOWN;
- proven closed/mismatched/foreign rows remain EXCLUDED;
- M19 basket pretrade validation fails closed on UNKNOWN with existing `REJ_BASKET_LOSS`;
- M20 prospective admission fails closed on UNKNOWN through existing atomic portfolio rejection;
- TradeLock modes 1/2 fail closed on UNKNOWN; mode 0 unchanged;
- UNKNOWN alone does not fabricate a basket-loss breach or emergency-close request;
- already-latched emergency release logic remains unchanged.

## Static / regression
- F05 deterministic model: PASS.
- F05 source/authority static guard: PASS.
- 22 protected Build 5.05 bodies: exact PASS.
- Full pytest: 22 passed.
- 17 additional specialized/cross-module scripts: PASS.
- F07 model/static: PASS.
- `git diff --check`: PASS.
- Canonical ownership helper count: one; legacy boolean helper removed.
- `OrderSend()` count remains one.

## Compile identity
- Current source SHA-256: `869eadf8d1a10735cce655d234ebdb06982bc76f332c89845ab37061c3769b7a`.
- Native MQ4 compile copy hash matches worktree exactly.
- Native EX4 SHA-256: `551c1f72620672618a0ae2bb4c93ee85677bfea619dcf3b356283f879023125a`.
- Native MetaEditor: 0 errors / 0 warnings.
- Exact three-transform tester adapter invariant: PASS.
- Tester adapter MetaEditor: 0 errors / 0 warnings.
- Targeted UNKNOWN harness MetaEditor: 0 errors / 0 warnings.

## Normal-path isolated runtime R3
GBPUSD M15 EveryTick, 2026-08-01 through 2026-09-01, compared with VERIFIED Build 5.05.
523 M15 counts/selects/decisions, 325 preflight passes and 14 executions.
All 9 protected traces are exact-equal; F07 hold/adopt events = 0; fatal runtime markers = 0.
Total trades remain 14; mismatched chart errors = 0.
GlobalVariables restored byte-for-byte to 240 bytes, SHA-256 `dd8320c5529d41eb90f55290cbf3d5aafe74f7a30964a647af075ddfd7ba91a6`.
Primary MT4 PID 13064 remained present; isolated tester exited 0.

## Targeted UNKNOWN-selection runtime R3
Test-only harness seeds one monitored row whose ticket cannot be selected.
523 M15 counts and 523 final decisions still occur; 523 preflight starts occur.
Preflight passes = 0; executions = 0; total trades = 0.
Uncertain basket observation is detected; unexpected emergency-latch marker = 0; F07 hold marker = 0.
Mismatched chart errors = 0; fatal runtime markers = 0; tester exited 0.
GlobalVariables restored exactly to the same 240-byte hash.

## Evidence hygiene / limitations
Pre-current-head artifacts under `D:/BBMA/Compile/F05_506_226` are superseded.
An intermediate UNKNOWN R2 run wrote its report to the normal R2 path because of a helper-config path bug; both runtime captures were therefore repeated cleanly as separate NORMAL_R3 and UNKNOWN_R3 evidence. Only R3 runtime evidence is authoritative here.
The legacy M17 standalone static script still hard-codes the historical Build 4.99 header; M17 model passes and protected M17-relevant bodies remain exact. This is stale fixture identity text, not an F05 semantic failure.
No primary MT4 restart, live/demo broker selection fault reproduction, trading activation or production-readiness claim was performed.
F03 TradeLock source conflict, broader F08 and F10 remain separate Issue #101 scopes.
