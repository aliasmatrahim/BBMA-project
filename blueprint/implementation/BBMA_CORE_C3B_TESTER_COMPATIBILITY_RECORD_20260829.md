# BBMA Core C3-B Tester Compatibility Record — 2026-08-29/30

Status: **IMPLEMENTED AND REGRESSION-CLEAN / NATIVE TESTER STARTUP EVIDENCE BLOCKED**

## Implemented boundary

Build 4.72 adds one tester-only branch to `FindActualSymbol`: the trimmed
request may be returned before broker-catalogue enumeration only when
`IsTesting()` is true and the request equals `Symbol()` exactly. The original
live `SymbolsTotal(false)`/`SymbolName`/`SymbolSelect` tail remains textually
unchanged with SHA-256:

`5b70b45e537efb8ba6ea65bf7acc83ca4e4b192f5da8489303f015e76d1a0a23`.

The shortcut does not bypass the downstream broker-specification reads or
`ValidateBrokerSpecificationWithRetry`. It has no signal, candidate, risk,
sizing, execution, lifecycle, recovery, or close authority.

Exact build-4.72 source SHA-256:

`0f461312d7d26d724c9738eddf88f1a226148f01eae894ce52d942e963f31e99`.

## Deterministic evidence

- tester-resolution model: PASS, 14 cases;
- tester-only/static/live-equivalence guard: PASS;
- complete Python regression set: PASS, 33 test files;
- Python harness compilation: PASS;
- D1 owner, D1TPW, NMJE N3, authority, identity, recovery, replay, truth-table,
  price-source, and end-to-end journey regressions: PASS;
- `OrderSend` source count remains exactly one;
- D1TPW, C044, and NMJE execution authority remain disabled.

## Native compilation

MetaTrader 4 build 1476 compiled the exact source twice in isolated portable
runtimes with **0 errors and 0 warnings**. The clean-runtime EX4 SHA-256 was:

`76fb78bd52af0af3f69fbe12de879bc476e4073b607d4114a2de01aa2a3012b8`.

EX4 identity is recorded per compile; source identity above is the canonical
change identity.

## Native Strategy Tester boundary

The pre-patch build-4.71 run generated 2,487 bars and 3,847,840 ticks at 90%
modelling quality with zero mismatches, then failed at disconnected symbol
resolution as recorded in C3-A.

After compiling build 4.72, repeated command-line smoke attempts did not create
a new tester log or report. A second portable runtime was built from the local
MT4 installation, seeded only with the exact build-4.72 source/EX4, the empty
20-byte portable account file, GBPUSD history, and the isolated one-pair test
configuration. Its terminal log reached:

- `05:27:31.630 Started with configuration file 'c3-smoke.ini'`; and
- `05:30:49.207 Started with configuration file 'c3-smoke.ini'`.

It then remained running without a tester-log entry. No EA initialization,
scan, order, or performance result occurred. The user's primary MT4 process,
profile, and account database were not stopped, edited, or copied.

Therefore build 4.72 is compile- and regression-clean, but the historical
four-timeframe baseline is **not locked**. Native runtime confirmation now
requires a manual visible MT4 Strategy Tester start (or separate explicit
authorization to use a connected demo-profile boundary). No performance claim
may be made from this record.

## Activation lock

This work remains draft-only. It does not authorize merge, release, demo/live
trading, NMJE execution authority, D1TPW, C044, W1, M30, or primary M1.
