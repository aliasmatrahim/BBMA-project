# BBMA Core C3-C Manual Visible Tester Evidence Checklist — 2026-08-30

Status: **PREPARED / READ-ONLY EVIDENCE / NO ACTIVATION**

## Fixed run identity

- isolated portable MT4 build 1476 only;
- EA build/header 4.72;
- GBPUSD, M15 processing, every-tick model;
- fixed 20-point spread;
- 2026-08-01 through 2026-08-28;
- one-pair `PairList=GBPUSD`;
- NMJE shadow-only; D1TPW and C044 disabled;
- primary MT4 profile and AutoTrading are outside scope.

## PASS evidence

The read-only evidence classifier requires all of the following:

1. `BBMA_EA` loads on GBPUSD M15;
2. exact tester resolution is `GBPUSD -> GBPUSD`;
3. broker specification emits `[P3S1][PASS]` for GBPUSD;
4. `LoadPairs completed count=1`;
5. build 4.72 initialization succeeds;
6. processing advances beyond one tick and zero bars;
7. the tester stops normally; and
8. a report exists.

Any non-exact symbol, broker-spec failure, zero valid pairs, or initialization
failure is `FAIL`. Missing completion evidence without an explicit failure is
`INCOMPLETE`. Profit, win rate, trade count, and drawdown must not be interpreted
unless the evidence status is `PASS`.

## Invocation after the manual run

```text
python blueprint/tools/c3_tester_evidence.py --log <tester-log> --report <html-report> --json
```

The classifier only reads the supplied files. It cannot launch MT4, change
inputs, place orders, enable authority, or modify a report.

## Stop boundary

This checklist does not lock the four-timeframe baseline by itself. A real
build-4.72 tester log and report remain mandatory. It does not authorize merge,
release, demo/live trading, NMJE execution authority, D1TPW, C044, W1, M30, or
primary M1.
