# Build 4.81 — C10 zero/missing-history fail-closed repair

Status: **CODE IMPLEMENTED / STATIC PASS / NATIVE METAEDITOR 0E0W / RUNTIME VALIDATION PENDING**.

## Governance boundary
- Refs Issue #122 and stacks on Draft PR #130 / Build 4.80.
- Canonical implementation owner remains `d1-owner-dev`; this branch is isolated staging only.
- C10 remains research/shadow only with `Authority=NONE`.
- No BBMA Strategy Core, M15 authority, risk/MM, M22 execution, D1TPW/C044 or NMJE execution semantics changed.
- Do not merge or activate from this record alone.

## Confirmed defect inherited from Build 4.80
`C10_UpdateShadowOutcomes()` only treated missing replay history as UNKNOWN when
`latestClosed > last_m5_closed && priorShift < 1`.

Therefore the deterministic state `latestClosed=0`, `priorShift=-1` bypassed the guard. If the shadow was already at/after expiry, code could reach the EXPIRED branch although M5 chronology was unprovable.

Classification: **CONFIRMED BUG / Issue #122 acceptance gap**.

## Smallest fix
Before replay or expiry evaluation, Build 4.81 now requires all of:
- valid M5 timeframe seconds;
- `latestClosed > 0`;
- stored `last_m5_closed > 0`;
- no history regression (`latestClosed >= last_m5_closed`);
- exact prior replay anchor (`priorShift >= 1`).

Failure of any condition writes conservative `UNKNOWN / REPLAY_HISTORY_UNAVAILABLE` for that shadow and does not globally disable the C10 ledger.

## Exact identity
- Version header: `4.8.1 - C10 Shadow Missing-History Fail-Closed Fix`.
- MQL4 property: `4.81`.
- Source SHA-256: `5DE9FD783BB930CC0591612479FE9D9440C938C142D91CB3BA978A233A658D57`.
- Embedded C10 SourceHash: `D6B0ADB94BB4EFB2829B33519550D349FABCB8C77251B6477E17489651F2089D`.
- Verification compile EX4 SHA-256: `9A09401B1F05F3A092BF81AA63E64BD1B77AB0E82FAAFA460A969D984635E21B`.
- Runtime-deployment EX4 SHA-256: `05733566540A2E5F0BA109BADA7EB17920DF5853201DAA5D9E8023E65C1912C0`.

## Validation produced
- `C10_122_STATIC_AUTHORITY=PASS`.
- `C10_122_LAGGED_M5_MODEL=PASS`.
- `C10_122_PREENTRY_REPLAY_MODEL=PASS`.
- `C10_122_ZERO_HISTORY_FAILCLOSED_MODEL=PASS`.
- `C10_122_REGRESSED_HISTORY_FAILCLOSED_MODEL=PASS`.
- `C10_122_MISSING_HISTORY_FAILCLOSED_MODEL=PASS`.
- `C10_122_CHECKPOINT_INTEGRITY_STATIC=PASS`.
- inherited Issue #123 writer-namespace checks: PASS.
- source-file SHA / embedded source-hash / stale-build-literal guards: PASS.
- reporter provenance-domain dedupe fixture: `PASS cases=11`.
- broker callsite counts unchanged: OrderSend=1, OrderModify=0, OrderClose=3, OrderDelete=0.
- native MetaEditor verification compile: **0 errors / 0 warnings / 464 ms**.
- exact deployment-name MetaEditor compile: **0 errors / 0 warnings / 419 ms**.
- compile-copy MQ4 SHA matched exact staged source before compile.

## Regression boundary
The 4.80 -> 4.81 EA semantic delta is restricted to build/source identity and the strengthened C10 replay-history fail-closed guard. No detector, candidate, combination, validation, risk, sizing, broker execution or trade-lifecycle authority is added.

## Remaining gate
**NOT RUNTIME VERIFIED.** Issue #122 remains open until Build 4.81 itself demonstrates the corrected missing-history/restart path under isolated runtime evidence. Build 4.80 evidence cannot substitute for Build 4.81 runtime identity.
- `git diff --check` with repository CRLF handling (`core.whitespace=cr-at-eol`): PASS.

## Runtime tooling hardening
- Hardened Build 4.81 physical-restart verifier ignores unrelated historical provenance domains while still enforcing duplicate-free IDs inside the exact BuildID/SourceHash/Config domain.
- Blank CSV lines are ignored; malformed non-empty row widths still fail verification.
- Verifier positive fixture: PASS; duplicate EventID negative fixture: FAIL as expected; synthetic `OrderSend` negative fixture: FAIL as expected.
- Restart watcher now parses ACTIVE rows with `Import-Csv` instead of treating a data row as a CSV header, and waits for exact ACTIVE checkpoint recovery before stopping the restarted terminal so buffered MQL4 logs can be verified after flush.
- Isolated runtime launched with Build 4.81, `InstanceID=81`, `ExpertsTrades=false`, `MaxTradePerPair=0`, `MaxTotalTrade=0`; current checkpoint remains `SEEN`, so physical-restart acceptance is still pending a fresh ACTIVE row.
