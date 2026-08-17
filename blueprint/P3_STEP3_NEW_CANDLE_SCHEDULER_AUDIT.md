# P3 Step 3 — New-Candle Scheduler Runtime Validation

Status: FIX A READY FOR COMPILE / RUNTIME TEST

## Objective
Prove that each enabled pair is processed exactly once for each newly closed M15 candle, with no duplicate ProcessPair pass caused by OnTick/OnTimer sharing the same orchestration entry point.

## Static baseline
- IsNewCandle compares the latest closed M15 candle against g_processed_candle_time[pairIndex].
- OnTickMain is the single scanning authority and guards with g_is_scanning.
- OnTimer calls the same OnTickMain authority rather than maintaining a second strategy scheduler.
- ProcessPair advances g_processed_candle_time after a completed cycle; the P3 S2 blocked-readiness path also advances the scheduled M15 timestamp before returning.

## Fix A instrumentation
Diagnostic-only state is added per pair:
- last ProcessPair M15 candle
- ProcessPair count since initialization

DebugLevel=4 output:
- [P3S3][START] pair, candle, count, previous processed candle
- [P3S3][END] pair, candle, count, stored processed candle
- [P3S3][END-BLOCK] if P3 S2 readiness blocks the cycle
- [P3S3][DUPLICATE] if the same M15 candle enters ProcessPair more than once

No BBMA detector, signal, risk, SL/TP, portfolio or execution logic is changed.

## Runtime PASS criteria
For at least two consecutive newly closed M15 candles:
1. All 7 enabled pairs receive one START and one END (or END-BLOCK) per candle.
2. The candle timestamps advance by one M15 close between cycles.
3. No [P3S3][DUPLICATE] is emitted.
4. No enabled pair is silently skipped when its M15 history is ready.

Compile target: 0 Errors / 0 Warnings.
