# BBMA Core C3 Tester Compatibility Contract

Status: **TESTER-ONLY IMPLEMENTATION / NO LIVE OR STRATEGY AUTHORITY**

## Purpose

Allow an intentionally disconnected MT4 Strategy Tester to resolve its exact
chart symbol without requiring connected-broker Market Watch selection. This
unblocks historical evidence while retaining the complete build-4.71 live
symbol-resolution path unchanged.

## Exact boundary

`FindActualSymbol` may return the trimmed request before broker-catalogue lookup
only when both conditions are true:

- `IsTesting()` is true; and
- the request equals `Symbol()` exactly.

It must not accept a base-name, suffix/prefix approximation, another symbol, or
an arbitrary history file through this shortcut. A disconnected portable run
must therefore set `PairList` to the exact single Strategy Tester chart symbol.

After resolution, `LoadPairs` still reads point, digits, tick value, tick size,
lot limits, stop/freeze levels and requires
`ValidateBrokerSpecificationWithRetry` before enabling the pair. The shortcut
does not manufacture broker specifications or suppress fail-closed validation.

## Live equivalence

When `IsTesting()` is false, the source continues at the original
`SymbolsTotal(false)`/`SymbolName`/`SymbolSelect` path without textual change.
The frozen SHA-256 of that live-resolution tail is:

`5b70b45e537efb8ba6ea65bf7acc83ca4e4b192f5da8489303f015e76d1a0a23`.

The tester shortcut has no candidate, detector, D1/H4/H1/M15 owner, NMJE,
geometry, risk, sizing, execution, lifecycle, recovery, or close authority.

## Build and activation boundary

- visible source/header build: 4.72;
- D1TPW remains disabled;
- C044 remains disabled;
- NMJE/M5 remains shadow-only;
- W1, M30 and primary M1 remain excluded;
- no daily-loss gate is added; same-currency exposure and cooldown remain KIV;
- no merge, demo/live activation, or release is authorized by this contract.
