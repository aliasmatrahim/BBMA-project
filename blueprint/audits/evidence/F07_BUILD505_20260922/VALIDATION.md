# F07 Build 5.05 validation

Date: 2026-09-22 UTC
Issue: #224 / downstream Issue #101 F07
Baseline: `d1-owner-dev@e9f239583a130e5168f75413d2610ec4f6a98674` / Build 5.04
Candidate: Build 5.05 / `V505_F07_EXECUTION_AMBIGUITY_HOLD_20260922`
Source revision: `F07_EXECUTION_AMBIGUITY_HOLD_224_20260922`

## Scope
F07 only: persistent fail-closed new-entry HOLD after unresolved M22 execution ambiguity.
No Strategy-Core detector/confirmation/ranking change, no TradeLock policy change, no M19/M21 formula change, no automatic resend, no timeout release.

## Current-head implementation
- M22 ambiguity paths latch one EA-instance HOLD.
- HOLD persists through terminal GlobalVariables; partial payload reload remains fail-closed.
- M20/M23 protection runs before F07 reconciliation.
- A tick beginning with HOLD is reconciliation-only after protection; even successful reconciliation cannot admit new exposure until the next operational tick.
- Matching live late execution is materialized from broker truth as `REC_AMBIGUOUS_EXECUTION_FROZEN`.
- Matching closed execution is tombstoned; no live row is invented.
- Missing evidence never auto-clears the HOLD.
- Restart recovery remains M24-owned and cannot assumption-clear F07.

## Static / regression
- F07 deterministic model: PASS.
- F07 source/authority static guard: PASS.
- Protected Build 5.04 bodies: 17/17 exact PASS.
- Full pytest: 22 passed.
- 13 specialized regression scripts: PASS.
- `git diff --check`: PASS.

## Compile identity
- Current source SHA-256: `2857f46f43a97ed478f0d7675de5ec92884ba2283d7cd7a0dc4cebaa031bce0b`.
- Native MQ4 copy hash matches worktree exactly.
- Native EX4 SHA-256: `0fe64f4d1f058e9651095eee814dd2b1193d2344529ec2f306dc34439aadd789`.
- Native MetaEditor: 0 errors / 0 warnings.
- Exact three-transform tester adapter invariant: PASS.
- Tester adapter MetaEditor: 0 errors / 0 warnings.

## Normal-path isolated runtime
GBPUSD M15 EveryTick, 2026-08-01 through 2026-09-01, compared with VERIFIED Build 5.04.
523 M15 counts/selects/decisions, 325 preflight and 14 executions.
All 9 protected traces are exact-equal; F07 hold/adopt events = 0; fatal runtime markers = 0.
GlobalVariables restored byte-for-byte: 240 bytes, SHA-256 `dd8320c5529d41eb90f55290cbf3d5aafe74f7a30964a647af075ddfd7ba91a6`.
Primary MT4 PID 13064 remained present; isolated tester exited 0.

## Targeted active-HOLD runtime
Test-only harness seeds an incomplete-persistence HOLD; no broker order is synthesized.
Build identity present; seeded HOLD=1; M15 counts=0; decision final=0; preflight=0; execution=0; hold-cleared=0.
Total trades=0; mismatched chart errors=0; fatal runtime markers=0; tester exited 0.
GlobalVariables restored exactly to the same 240-byte hash.

## Evidence hygiene / limitations
Preliminary artifacts under `D:/BBMA/Compile/F07_505_224` and earlier F07 smoke/HOLD evidence were produced before the same-tick protection fix and are superseded. They are not current-head evidence.
Current-head evidence is the R2 native/normal path plus HOLD R3 artifacts copied into this directory.
The targeted runtime proves active-HOLD admission suppression, not a real broker ambiguous fill/late-fill event.
No primary MT4 restart, broker live/demo ambiguity, trading enablement or production-readiness claim was performed.
TradeLock F03, shared-helper F05, broader F08 and F10 remain separate Issue #101 scopes.
