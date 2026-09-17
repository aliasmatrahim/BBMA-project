# Build 4.86 post-Build-4.85 integration closure

Task: Q5 / Issue #173 / PR #177
Date: 2026-09-17
Owner base: d1-owner-dev@ab2649634fc5ec03340de414920697a7fa1fa171 (Build 4.85)
Candidate: Build 4.86 ? Structural Lifetime Authority Repair

## Authority
- SOURCE_INDEX -> Core V2 -> `P3_FINAL_DELTA_R1_LIFETIME_SOURCE_RESOLUTION.md`.
- Generic `MaxWaitBars_Extreme` and `MaxWaitBars_ReEntry` are not Strategy-Core death authority.
- Structural invalidation/reset/supersession remains authoritative.
- Legacy age fields may remain diagnostic metadata only.

## Integrated source result
- Original #173 semantic delta was reapplied on top of owner Build 4.85.
- Q1 NMJE read-only authority, Q2 F7/C044, #175 standalone Extreme, and #174 M12N-before-M13 ordering are preserved.
- Re-Entry Type 2/3/4 candidate/confirmed validity has no generic fixed-age expiry.
- Extreme persistent validity has no fixed-age rejection path.
- Remaining `MaxWaitBars_Extreme` exported `ExpiryBar` value is metadata-only; persistent owner validation does not consume it as expiry authority.

## Verification
- Focused + inherited pytest: 23/23 PASS.
- C044 deterministic model: 145 normal + 85 frozen failure points PASS.
- Cross-module direct selftests: 13/13 PASS.
- Historical lifetime analyzer: PASS.
  - Mode1 Re-Entry owners 73; 26 survive >5 bars; max 15 bars.
  - Mode1 Extreme owners 276; 169 survive >5 bars; max 20.75 bars.
  - Mode2 47 standalone Re-Entry selections older than 5h; 47/47 M16 PASS.
  - zero legacy expiry reasons; zero order markers.
- Native MetaEditor compile: 0 errors / 0 warnings, 729 ms.
- MQ4 SHA-256: D737A25FD01D6BA879118479401B5E7969DF20F528E53E43515852C555DD3308.
- EX4 SHA-256: 6A7116B26CDB7BA87B8CCC3415D2309BF414C32D274A66B4903D6E47FC93A5C6.

## Exact final-binary broker smoke
Isolated `MT4_Q5_173_Demo`, EURUSD/M15, EntryMode=2, zero trade caps, TradeLockMode=2, ExpertsTrades=false.
Observed Build 4.86 BuildTag/SourceRev, broker-spec/PairID/Magic/init PASS, heartbeat `Init=1 Connected=1`, live N1 observation, zero `[NMJE-GATE]`, zero `OrderSend`, zero `DEC_EXECUTED`, and graceful deinit/removal.

## Boundary
Type 2 did not naturally occur in the bounded historical window; its shared no-TTL path is covered by static/TDD proof and no event was fabricated. This closure is mechanism/integration evidence only, not profitability or release-readiness evidence. Primary MT4 was not restarted or modified.
