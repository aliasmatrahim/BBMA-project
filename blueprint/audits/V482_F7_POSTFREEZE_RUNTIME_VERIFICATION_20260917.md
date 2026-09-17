# Build 4.82 F7/C044 Post-Freeze Verification — 2026-09-17

Refs: #127, #132, #133, #138, PR #140.
Branch: `upgrade/f7-infra-postfreeze-20260909`.
Base synchronized to `d1-owner-dev@0d8c8ac71aeb9947d48f89239f46a88c31981182`.

## Classification
**BRANCH-LEVEL VERIFIED / INTEGRATION PENDING.**

No Strategy-Core rule was added or changed. This package is infrastructure/provenance hardening only.

## Static and deterministic gates
- F7 source guards: **4/4 PASS**.
- C044 generation model: **PASS** — normal failure points 145, frozen failure points 85.
- Cross-module direct guards: **13/13 PASS**.
- `git diff --check`: PASS before packaging.
- `[F7-BUILD]` remains before `InitializeEA()`.
- EXEC telemetry uses exact-ticket `info.open_time`.
- C044 old commit marker is invalidated before payload mutation and new commit marker is published last.
- Legacy/unprovable generation recovery remains fail-frozen.

## Native compile / identity
- Build: **4.82 — Post-Freeze F7 Infrastructure**.
- MetaEditor: **0 errors / 0 warnings**, 721 ms.
- MQ4 SHA-256: `B2CA9D90951094C17F96482C8A7CFDFB3F0C5D6F49C79DAE01F02FD16DF59AC3`.
- Fresh EX4 SHA-256: `D4AABC343F56106D206D2C49619737E8235345153796CB1A7980D17C6BDD9724`.
## Exact-binary isolated broker smoke
The exact fresh MQ4/EX4 bytes were deployed in an isolated MetaQuotes-Demo data folder with `ExpertsTrades=false`, `MaxTradePerPair=0`, `MaxTotalTrade=0` and `TradeLockMode=2`.

Observed after log flush:
- `[F7-BUILD]` emitted before `InitializeEA` and ordinary runtime state telemetry;
- broker specification, PairID and Magic validation PASS;
- EA initialization PASS;
- D1/NMJE state processing active;
- `[F7-TELEM] Init=1 Connected=1`;
- graceful deinitialization;
- zero `OrderSend` / `DEC_EXECUTED` / broker-order markers.

Committed runtime evidence excludes demo account and IP identifiers.

## Claim boundary
This smoke proves exact Build 4.82 attribution, startup ordering and broker-connected initialization. It does **not** claim a live C044 torn-write event or live exact-ticket EXEC event because trading was deliberately disabled. C044 interruption safety is verified by the deterministic 145/85 failure model; exact-ticket EXEC open-time behavior is covered by the source guard and remains available for later integrated-candidate runtime coverage.

Primary MT4 was not restarted or modified. No merge or production activation is included.